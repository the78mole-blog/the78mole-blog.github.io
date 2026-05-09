#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
restore-missing-assets.py

Reads failed link entries from a check-links log file (produced with --log),
and for each missing file whose original URL points to your site's old domain:

  1. Locates the asset in local WordPress import directories.
  2. Copies it to  public/uploads/<year>/<month>/<file>.
  3. Rewrites the original URL in the Markdown source files to /uploads/…

Generalisation:
  Edit the constants at the top of this file to match your project:
    SITE_HOSTS      – old domain(s) whose assets are imported locally
    SEARCH_ROOTS    – folders inside import/ where WP uploads live
    UPLOADS_DIR     – destination inside public/ for restored assets

Usage:
  uv run --script scripts/restore-missing-assets.py [--log FILE] [--dry-run]
"""

import argparse
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

# ── Project-specific configuration (adapt for your project) ─────────────────

REPO_ROOT   = Path(__file__).resolve().parents[1]
PUBLIC_DIR  = REPO_ROOT / "public"
CONTENT_DIR = REPO_ROOT / "content"
IMPORT_DIR  = REPO_ROOT / "import"

# Destination directory inside public/ for restored WP uploads
UPLOADS_DIR = PUBLIC_DIR / "uploads"

# Hostnames whose missing assets should be searched for locally
SITE_HOSTS = {"example.de", "blog.example.de", "www.example.de"}

# Search order for local WP files (adjust paths to match your import layout)
SEARCH_ROOTS = [
    IMPORT_DIR / "wp-content",
    IMPORT_DIR / "WordPress_SecureMode_01" / "wp-content",
]

# ── Internals ────────────────────────────────────────────────────────────────

RE_FAIL_URL = re.compile(r'^\[FAIL\s+\]\s+(\S+)', re.MULTILINE)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--log", type=Path, default=Path("/tmp/links.log"),
                   help="Path to the check-links log file (default: /tmp/links.log)")
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would happen without touching any files")
    return p.parse_args()


def url_to_wp_subpath(url: str) -> str | None:
    """Extract the wp-content-relative subpath from a URL, or None if not applicable."""
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname not in SITE_HOSTS:
        return None
    path = parsed.path
    if path.startswith("/wp-content/"):
        return path[len("/wp-content/"):]
    return None


def find_in_imports(subpath: str) -> Path | None:
    for root in SEARCH_ROOTS:
        candidate = root / subpath
        if candidate.exists():
            return candidate
    return None


def dest_path(subpath: str) -> Path:
    """Map a wp-content-relative subpath to its destination in public/uploads/."""
    rel = subpath[len("uploads/"):] if subpath.startswith("uploads/") else subpath
    return UPLOADS_DIR / rel


def dest_url(subpath: str) -> str:
    rel = subpath[len("uploads/"):] if subpath.startswith("uploads/") else subpath
    return "/uploads/" + rel


def rewrite_sources(old_url: str, new_url: str, dry_run: bool) -> list[str]:
    changed = []
    for md in sorted(CONTENT_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        if old_url in text:
            if not dry_run:
                md.write_text(text.replace(old_url, new_url), encoding="utf-8")
            changed.append(str(md.relative_to(REPO_ROOT)))
    return changed


def main() -> int:
    args = parse_args()

    if not args.log.exists():
        sys.exit(f"ERROR: log file not found: {args.log}")

    failed_urls = RE_FAIL_URL.findall(args.log.read_text(encoding="utf-8"))
    site_urls = sorted({u for u in failed_urls
                        if urllib.parse.urlparse(u).hostname in SITE_HOSTS})

    if not site_urls:
        print("No failed site URLs found in the log.")
        return 0

    print(f"Found {len(site_urls)} unique failed site URL(s).\n")

    copied = missing = skipped = 0

    for url in site_urls:
        subpath = url_to_wp_subpath(url)
        if not subpath or not subpath.startswith("uploads/"):
            print(f"  SKIP  {url}")
            skipped += 1
            continue

        dst  = dest_path(subpath)
        repl = dest_url(subpath)

        if dst.exists():
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
            print(f"         →  {dst.relative_to(REPO_ROOT)}")
            print(f"         rewrite: {url}  →  {repl}")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dst)
            sources = rewrite_sources(url, repl, dry_run=False)
            print(f"  COPY  {source.relative_to(REPO_ROOT)}")
            print(f"         →  {dst.relative_to(REPO_ROOT)}")
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
