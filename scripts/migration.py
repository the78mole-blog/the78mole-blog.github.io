#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "lxml>=5.0",
#     "beautifulsoup4>=4.12",
#     "markdownify>=0.13",
#     "pyyaml>=6.0",
# ]
# ///
"""
WordPress WXR to Nuxt Content Migration Script

Parses a WordPress export XML (WXR) and produces:
- Markdown files with YAML frontmatter in content/blog/YEAR/slug.md
- Copied media files in public/images/blog/YEAR/MM/filename

Usage:
    uv run migration.py
"""

import re
import shutil
from datetime import datetime
from pathlib import Path

import yaml
from bs4 import BeautifulSoup
from lxml import etree
import markdownify

# ---------------------------------------------------------------------------
# WXR XML namespace map
# ---------------------------------------------------------------------------
NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "dc": "http://purl.org/dc/elements/1.1/",
}

# ---------------------------------------------------------------------------
# Paths  (relative to the repository root)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent.parent
IMPORT_DIR = BASE_DIR / "import"
UPLOADS_SRC = IMPORT_DIR / "wp-content" / "uploads"
CONTENT_DIR = BASE_DIR / "content" / "blog"
PAGES_DIR = BASE_DIR / "content" / "pages"
IMAGES_DST = BASE_DIR / "public" / "images" / "blog"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_xml_file() -> Path:
    """Return the first *.xml file found in ./import/."""
    xml_files = list(IMPORT_DIR.glob("*.xml"))
    if not xml_files:
        raise FileNotFoundError(f"No XML export file found in {IMPORT_DIR}")
    return xml_files[0]


def wp_text(element, tag: str) -> str:
    """Return stripped text of a child element addressed by namespace-prefixed tag."""
    child = element.find(tag, NS)
    if child is not None and child.text:
        return child.text.strip()
    return ""


def transform_image_url(url: str) -> str:
    """Rewrite a wp-content/uploads/... URL to /images/blog/..."""
    match = re.search(r"wp-content/uploads/(.+)$", url)
    if match:
        return "/images/blog/" + match.group(1)
    return url


def copy_image(url: str) -> None:
    """Copy a media file from import/wp-content/uploads to public/images/blog."""
    match = re.search(r"wp-content/uploads/(.+)$", url)
    if not match:
        return
    rel = match.group(1)
    src = UPLOADS_SRC / rel
    dst = IMAGES_DST / rel
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    else:
        print(f"    [WARN] Image source not found: {src}")


# ---------------------------------------------------------------------------
# XML extraction helpers
# ---------------------------------------------------------------------------

def build_attachment_map(root) -> dict:
    """Return {post_id: attachment_url} for all attachment items."""
    attachments: dict[str, str] = {}
    for item in root.findall(".//item"):
        if wp_text(item, "wp:post_type") != "attachment":
            continue
        post_id = wp_text(item, "wp:post_id")
        # wp:attachment_url is the canonical field; fall back to <guid>
        url = wp_text(item, "wp:attachment_url")
        if not url:
            guid_el = item.find("guid")
            url = (guid_el.text or "").strip() if guid_el is not None else ""
        if post_id and url:
            attachments[post_id] = url
    return attachments


def get_thumbnail(item, attachment_map: dict) -> str:
    """Return the new /images/blog/... path for the post's featured image."""
    for meta in item.findall("wp:postmeta", NS):
        if wp_text(meta, "wp:meta_key") == "_thumbnail_id":
            thumb_id = wp_text(meta, "wp:meta_value")
            original_url = attachment_map.get(thumb_id, "")
            if original_url:
                copy_image(original_url)
                return transform_image_url(original_url)
    return ""


def get_categories_and_tags(item) -> tuple[list, list]:
    """Return (categories, tags) lists from <category> child elements."""
    categories: list[str] = []
    tags: list[str] = []
    for cat in item.findall("category"):
        domain = cat.get("domain", "")
        text = (cat.text or "").strip()
        if not text:
            continue
        if domain == "category":
            categories.append(text)
        elif domain == "post_tag":
            tags.append(text)
    return categories, tags


# ---------------------------------------------------------------------------
# HTML → Markdown conversion
# ---------------------------------------------------------------------------

class WPMarkdownConverter(markdownify.MarkdownConverter):
    """Extends markdownify to handle WP specifics: code blocks and images."""

    def convert_pre(self, el, text, convert_as_inline=False, **kwargs):
        """Produce fenced code blocks, detecting language from CSS class."""
        code_el = el.find("code")
        lang = ""
        if code_el is not None:
            for cls in code_el.get("class") or []:
                if cls.startswith("language-"):
                    lang = cls[9:]
                    break
            code_text = code_el.get_text()
        else:
            code_text = el.get_text()
        return f"\n\n```{lang}\n{code_text.strip(chr(10))}\n```\n\n"

    def convert_img(self, el, text, convert_as_inline=False, **kwargs):
        """Transform wp-content image URLs and copy the files."""
        src = el.get("src", "")
        alt = el.get("alt", "")
        title = el.get("title", "")
        new_src = transform_image_url(src)
        if "wp-content/uploads" in src:
            copy_image(src)
        title_part = f' "{title}"' if title else ""
        return f"![{alt}]({new_src}{title_part})"


def html_to_markdown(html: str) -> str:
    """Full HTML → clean Markdown pipeline."""
    if not html:
        return ""

    # Replace WordPress shortcodes with HTML comments so nothing is lost
    html = re.sub(
        r"\[(\w[^\]\n]*)\]",
        lambda m: f"<!-- wp:shortcode {m.group(1)} -->",
        html,
    )

    soup = BeautifulSoup(html, "lxml")

    # Strip unwanted tags
    for tag in soup.find_all(["script", "style"]):
        tag.decompose()
    # Remove embedded Google Fonts links
    for tag in soup.find_all("link", href=re.compile(r"fonts\.googleapis\.com")):
        tag.decompose()

    cleaned_html = str(soup.body if soup.body else soup)

    md = WPMarkdownConverter(
        heading_style=markdownify.ATX,
        bullets="-",
        strip=["script", "style"],
    ).convert(cleaned_html)

    # Collapse more than two consecutive blank lines
    return re.sub(r"\n{3,}", "\n\n", md).strip()


# ---------------------------------------------------------------------------
# File writer
# ---------------------------------------------------------------------------

def write_post(post: dict) -> None:
    """Write a Markdown file with YAML frontmatter for one post."""
    year = post["date"][:4]
    out_dir = CONTENT_DIR / year
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{post['slug']}.md"

    frontmatter: dict = {
        "title": post["title"],
        "date": post["date"],
        "description": post["description"],
        "categories": post["categories"],
        "tags": post["tags"],
    }
    if post["image"]:
        frontmatter["image"] = post["image"]

    yaml_str = yaml.dump(
        frontmatter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )

    comment_section = (
        "\n\n---\n\n"
        "## Kommentare / Comments\n\n"
        "Hast du Fragen oder Anmerkungen zu diesem Artikel? "
        "[Erstelle ein GitHub Issue]"
        "(https://github.com/the78mole-blog/the78mole-blog.github.io/issues/new"
        f"?title=Kommentar+zu%3A+{post['slug']}&labels=comment) "
        "oder starte eine "
        "[Diskussion](https://github.com/the78mole-blog/the78mole-blog.github.io/discussions).\n"
    )

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"---\n{yaml_str}---\n\n{post['content']}{comment_section}")

    print(f"  -> {out_file.relative_to(BASE_DIR)}")


def write_page(page: dict) -> None:
    """Write a Markdown file with YAML frontmatter for one WordPress page."""
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PAGES_DIR / f"{page['slug']}.md"

    frontmatter: dict = {
        "title": page["title"],
        "date": page["date"],
        "description": page["description"],
    }
    if page["image"]:
        frontmatter["image"] = page["image"]

    yaml_str = yaml.dump(
        frontmatter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"---\n{yaml_str}---\n\n{page['content']}")

    print(f"  -> {out_file.relative_to(BASE_DIR)}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def migrate() -> None:
    xml_file = find_xml_file()
    print(f"Parsing XML: {xml_file.name}")

    parser = etree.XMLParser(recover=True, encoding="utf-8")
    tree = etree.parse(str(xml_file), parser)
    root = tree.getroot()

    attachment_map = build_attachment_map(root)
    print(f"Attachments indexed: {len(attachment_map)}")

    posts = [
        item
        for item in root.findall(".//item")
        if wp_text(item, "wp:post_type") == "post"
        and wp_text(item, "wp:status") == "publish"
    ]
    print(f"Published posts found: {len(posts)}\n")

    for item in posts:
        title = (item.findtext("title") or "").strip()
        slug = wp_text(item, "wp:post_name")
        date_raw = wp_text(item, "wp:post_date")
        description = wp_text(item, "excerpt:encoded")
        html_content = wp_text(item, "content:encoded")

        try:
            date_str = datetime.strptime(date_raw, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except ValueError:
            date_str = date_raw[:10] if len(date_raw) >= 10 else "1970-01-01"

        categories, tags = get_categories_and_tags(item)
        image = get_thumbnail(item, attachment_map)

        print(f"Processing: {title[:70]}")
        content_md = html_to_markdown(html_content)

        write_post(
            {
                "title": title,
                "slug": slug,
                "date": date_str,
                "description": description,
                "categories": categories,
                "tags": tags,
                "image": image,
                "content": content_md,
            }
        )

    wp_pages = [
        item
        for item in root.findall(".//item")
        if wp_text(item, "wp:post_type") == "page"
        and wp_text(item, "wp:status") == "publish"
    ]
    print(f"\nPublished pages found: {len(wp_pages)}\n")

    for item in wp_pages:
        title = (item.findtext("title") or "").strip()
        slug = wp_text(item, "wp:post_name")
        date_raw = wp_text(item, "wp:post_date")
        description = wp_text(item, "excerpt:encoded")
        html_content = wp_text(item, "content:encoded")

        try:
            date_str = datetime.strptime(date_raw, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        except ValueError:
            date_str = date_raw[:10] if len(date_raw) >= 10 else "1970-01-01"

        image = get_thumbnail(item, attachment_map)
        print(f"Processing page: {title[:70]}")
        content_md = html_to_markdown(html_content)

        write_page({
            "title": title,
            "slug": slug,
            "date": date_str,
            "description": description,
            "image": image,
            "content": content_md,
        })

    print(f"\nDone! Migrated {len(posts)} posts + {len(wp_pages)} pages.")
    print(f"Content  -> {CONTENT_DIR.relative_to(BASE_DIR)}/")
    print(f"Pages    -> {PAGES_DIR.relative_to(BASE_DIR)}/")
    print(f"Images   -> {IMAGES_DST.relative_to(BASE_DIR)}/")


if __name__ == "__main__":
    migrate()
