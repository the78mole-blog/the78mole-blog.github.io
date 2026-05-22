#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML"]
# ///
"""Generate public/tags.json and public/categories.json from blog frontmatter.

Each file maps a tag/category name to a list of matching posts, sorted by date
descending.  Run before `nuxi generate` so the static site can fetch them.

Usage:
    uv run --script scripts/generate-taxonomy.py
"""

import json
import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "blog"
PUBLIC_DIR = REPO_ROOT / "public"

FRONTMATTER_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        print(f"  WARN: YAML error in {path}: {exc}")
        return {}


def file_to_path(md_path: Path) -> str:
    """content/blog/2024/my-post.md  →  /blog/2024/my-post"""
    rel = md_path.relative_to(CONTENT_DIR.parent)  # blog/2024/my-post.md
    return "/" + str(rel.with_suffix("")).replace("\\", "/")


def build_taxonomy() -> None:
    tags: dict[str, list] = {}
    categories: dict[str, list] = {}

    posts = sorted(CONTENT_DIR.rglob("*.md"), reverse=True)
    skipped = 0
    for md in posts:
        fm = parse_frontmatter(md)
        title = fm.get("title", "").strip()
        if not title:
            skipped += 1
            continue

        entry = {
            "title": title,
            "path": file_to_path(md),
            "date": str(fm.get("date", "")).strip(),
            "description": (fm.get("description") or "").strip(),
            "image": fm.get("image") or None,
        }

        for tag in fm.get("tags") or []:
            tag = str(tag).strip()
            if tag:
                tags.setdefault(tag, []).append(entry)

        for cat in fm.get("categories") or []:
            cat = str(cat).strip()
            if cat:
                categories.setdefault(cat, []).append(entry)

    if skipped:
        print(f"  Skipped {skipped} posts without a title.")

    PUBLIC_DIR.mkdir(exist_ok=True)

    tags_path = PUBLIC_DIR / "tags.json"
    categories_path = PUBLIC_DIR / "categories.json"

    tags_path.write_text(
        json.dumps(tags, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    categories_path.write_text(
        json.dumps(categories, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total_tag_entries = sum(len(v) for v in tags.values())
    total_cat_entries = sum(len(v) for v in categories.values())
    print(f"tags.json        → {len(tags):3d} tags,       {total_tag_entries} entries")
    print(f"categories.json  → {len(categories):3d} categories, {total_cat_entries} entries")
    print(f"Written to {PUBLIC_DIR}/")


if __name__ == "__main__":
    build_taxonomy()
