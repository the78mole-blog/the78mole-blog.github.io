#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
restore-missing-assets.py

Reads failed link entries from a check-links log file, and for each missing
file whose *original* URL pointed to the78mole.de (wp-content/uploads/…):

  1. Locates the asset in the two local WordPress import directories.
  2. Copies it to  public/uploads/<year>/<month>/<file>.
  3. Rewrites the original URL in the Markdown source to  /uploads/…

Search order:
  1. import/wp-content/…
  2. import/WordPress_SecureMode_01/wp-content/…

Usage:
  uv run --script scripts/restore-missing-assets.py [--log FILE] [--dry-run]
"""

import argparse
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

REPO_ROOT   = Path(__file__).resolve().parents[1]
PUBLIC_DIR  = REPO_ROOT / "public"
CONTENT_DIR = REPO_ROOT / "content"
IMPORT_DIR  = REPO_ROOT / "import"
UPLOADS_DIR = PUBLIC_DIR / "uploads"

SEARCH_ROOTS = [
    IMPORT_DIR / "wp-content",
    IMPORT_DIR / "WordPress_SecureMode_01" / "wp-content",
]

MOLE_HOSTS = {"the78mole.de", "blog.the78mole.de", "www.the78mole.de"}
RE_FAIL_URL = re.compile(r'^\[FAIL\s+\]\s+(\S+)', re.MULTILINE)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--log", type=Path, default=Path("/tmp/links.log"))
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def url_to_wp_subpath(url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname not in MOLE_HOSTS:
        return None
    path = parsed.path
    if path.startswith("/wp-content/"):
        return path[len("/wp-content/"):]
    return None


def find_in_imports(subpath: str) -> Path | None:
    for root in SEARCH_ROOTS:
        c = root / subpath
        if c.exists():
            return c
    return None


def new_public_path(subpath: str) -> Path:
    rel = subpath[len("uploads/"):] if subpath.startswith("uploads/") else subpath
    return UPLOADS_DIR / rel


def new_url(subpath: str) -> str:
    rel = subpath[len("uploads/"):] if subpath.startswith("uploads/") else subpath
    return "/uploads/" + rel


def rewrite_sources(old_url: str, repl: str, dry_run: bool) -> list[str]:
    changed = []
    for md in sorted(CONTENT_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        if old_url in text:
            if not dry_run:
                md.write_text(text.replace(old_url, repl), encoding="utf-8")
            changed.append(str(md.relative_to(REPO_ROOT)))
    return changed


def main() -> int:
    args = parse_args()

    if not args.log.exists():
        sys.exit(f"ERROR: log file not found: {args.log}")

    failed_urls = RE_FAIL_URL.findall(args.log.read_text(encoding="utf-8"))
    mole_urls = sorted({u for u in failed_urls
                        if urllib.parse.urlparse(u).hostname in MOLE_HOSTS})

    if not mole_urls:
        print("No failed the78mole.de URLs found in the log.")
        return 0

    print(f"Found {len(mole_urls)} unique failed the78mole.de URL(s).\n")

    copied = missing = skipped = 0

    for url in mole_urls:
        subpath = url_to_wp_subpath(url)
        if not subpath or not subpath.startswith("uploads/"):
            print(f"  SKIP  {url}")
            skipped += 1
            continue

        dest = new_public_path(subpath)
        repl = new_url(subpath)

        if dest.exists():
            sources = rewrite_sources(url, repl, args.dry_run)
            tag = "DRY-REWRITE" if args.dry_run else "REWRITE    "
            if sources:
                for s in sources:
                    print(f"  {tag}  {s}")
                    print(f"         {url}  →  {repl}")
            else:
                print(f"  OK     {repl}  (already present, source up to date)")
            skipped += 1
            continue

        source = find_in_imports(subpath)
        if source is None:
            print(f"  MISS  {url}")
            missing += 1
            continue

        if args.dry_run:
            print(f"  DRY   {source.relative_to(REPO_ROOT)}")
            print(f"         →  {dest.relative_to(REPO_ROOT)}")
            print(f"         rewrite: {url}  →  {repl}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            sources = rewrite_sources(url, repl, dry_run=False)
            print(f"  COPY  {source.relative_to(REPO_ROOT)}")
            print(f"         →  {dest.relative_to(REPO_ROOT)}")
            for s in sources:
                print(f"         edited: {s}")
        copied += 1

    print(f"\n{'─'*64}")
    action = "Would copy/rewrite" if args.dry_run else "Copied+rewrote"
    print(f"  {action}: {copied}  |  Not found: {missing}  |  Skipped: {skipped}")
    print(f"{'─'*64}")
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
