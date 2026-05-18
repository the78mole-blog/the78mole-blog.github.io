#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.31"]
# ///
"""check-links.py – Dead-link checker for content/*.md files.

Checks:
  - External links (http/https) via HTTP HEAD → GET fallback
  - Internal /images/… links against public/
  - Internal /blog/… and /pages/… links against content/

Usage:
  python3 scripts/check-links.py [OPTIONS] [FILE ...]

  If no FILE arguments are given, all *.md files under content/ are scanned.

Options:
  --no-external      Skip external HTTP checks (fast mode, e.g. for CI pre-check)
  --workers N        Parallel HTTP workers (default: 10)
  --timeout N        HTTP timeout in seconds (default: 10)
  --ignore-file F    File with URL prefixes to ignore (one per line, comments with #)
  --no-check-cache   Ignore cache TTL rules; re-check every URL (except manual/captcha status)
  --non-interactive  Skip the interactive error-handling prompt at the end

Cache (.link_cache.json in repo root):
  passed  – re-checked after 28 days
  manual  – re-checked after 365 days
  captcha – re-checked after 365 days (CAPTCHA-protected, manually verified)
  failed  – re-checked on every run
"""

import argparse
import json
import re
import sys
import threading
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    sys.exit("ERROR: 'requests' library not found. Run: pip install requests")

# ── ANSI colours (disabled when stdout is not a TTY) ────────────────────────

def _ansi(code: str, text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text

def green(t: str)  -> str: return _ansi("32", t)
def yellow(t: str) -> str: return _ansi("33", t)
def red(t: str)    -> str: return _ansi("31", t)

SLOW_MS = 300  # threshold for yellow warning


# ── Constants ────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = REPO_ROOT / "content"
PUBLIC_DIR = REPO_ROOT / "public"

# Schemes we never check
SKIP_SCHEMES = {"mailto", "tel", "data", "vscode-remote", "vscode", "javascript"}

# Regex: captures URL from Markdown inline links  [text](url)
# Deliberately simple (no nested-bracket support) to avoid ReDoS.
RE_MD_LINK = re.compile(r'\[[^\[\]\n]{0,500}\]\(([^)\s]{1,2000})(?:\s+"[^"]*")?\)')
# Regex: captures URL from Markdown reference definitions  [id]: url
RE_MD_REF = re.compile(r'^\s{0,3}\[(?:[^\[\]]+)\]:\s+(\S+)', re.MULTILINE)
# Regex: captures value from frontmatter  image: /path
RE_FM_IMAGE = re.compile(r'^image:\s*["\']?(/[^\s"\']+)["\']?', re.MULTILINE)
# Regex: HTML href / src in markdown
RE_HTML_ATTR = re.compile(r'(?:href|src)=["\']([^"\']+)["\']')


# ── Argument parsing ─────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="*", type=Path,
                   help="Markdown files to check (default: all content/**/*.md)")
    p.add_argument("--no-external", action="store_true",
                   help="Skip external HTTP checks")
    p.add_argument("--workers", type=int, default=10,
                   help="Parallel HTTP workers (default: 10)")
    p.add_argument("--timeout", type=int, default=10,
                   help="HTTP timeout in seconds (default: 10)")
    p.add_argument("--ignore-file", type=Path, default=None,
                   help="File with URL prefixes to ignore (one per line)")
    p.add_argument("--log", type=Path, default=None, metavar="FILE",
                   help="Write a full check log (all URLs) to FILE")
    p.add_argument("--no-check-cache", action="store_true",
                   help="Ignore cache TTL; re-check every URL except those with 'manual' status")
    p.add_argument("--non-interactive", action="store_true",
                   help="Skip interactive error-handling prompt at the end")
    return p.parse_args()


# ── Link extraction ──────────────────────────────────────────────────────────

def _mask_code_blocks(text: str) -> str:
    """Replace the content lines of fenced code blocks with spaces.

    Preserves character positions (same line lengths, same newline count) so
    that line-number lookups based on character offsets remain valid.
    Handles both ``` and ~~~ fences, including language-tagged openings.
    """
    lines = text.split('\n')
    result: list[str] = []
    in_fence = False
    fence_marker: str = ''
    for line in lines:
        stripped = line.lstrip()
        if not in_fence:
            if stripped.startswith('```') or stripped.startswith('~~~'):
                fence_marker = stripped[:3]
                in_fence = True
                result.append(line)          # keep opening fence line
            else:
                result.append(line)
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
                result.append(line)          # keep closing fence line
            else:
                result.append(' ' * len(line))  # blank out, preserve length
    return '\n'.join(result)


def extract_links(path: Path) -> list[tuple[int, str]]:
    """Return list of (line_number, url) from a Markdown file."""
    text = path.read_text(encoding="utf-8", errors="replace")
    results: list[tuple[int, str]] = []

    # Build line-start index for fast line-number lookup
    line_starts = [0]
    for m in re.finditer(r'\n', text):
        line_starts.append(m.end())

    def lineno(pos: int) -> int:
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    # Frontmatter image: only scan the leading ---...--- block so that
    # example frontmatter snippets inside code blocks are ignored.
    fm_match = re.match(r'^---\r?\n.*?\r?\n---[ \t]*\r?\n', text, re.DOTALL)
    frontmatter = fm_match.group(0) if fm_match else ''
    for m in RE_FM_IMAGE.finditer(frontmatter):
        results.append((lineno(m.start()), m.group(1)))

    # For all other patterns, mask fenced code blocks first so that
    # example links inside ``` blocks are not reported as real links.
    masked = _mask_code_blocks(text)

    # Inline Markdown links
    for m in RE_MD_LINK.finditer(masked):
        results.append((lineno(m.start()), m.group(1)))

    # Reference-style link definitions
    for m in RE_MD_REF.finditer(masked):
        results.append((lineno(m.start()), m.group(1)))

    # HTML href/src
    for m in RE_HTML_ATTR.finditer(masked):
        results.append((lineno(m.start()), m.group(1)))

    return results


# ── URL classification ───────────────────────────────────────────────────────

def classify(url: str) -> str:
    """Return 'external', 'internal', or 'skip'."""
    url = url.strip()
    if not url or url.startswith('#'):
        return 'skip'
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme in SKIP_SCHEMES:
        return 'skip'
    if parsed.scheme in ('http', 'https'):
        return 'external'
    if parsed.path.startswith('/') and not parsed.scheme:
        return 'internal'
    # Relative path (no leading slash, no scheme) – skip for now
    return 'skip'


# ── Internal link resolution ─────────────────────────────────────────────────

def check_internal(url: str) -> tuple[str | None, int]:
    """Return (error message or None, duration_ms)."""
    t0 = time.monotonic()
    path = urllib.parse.urlparse(url).path.split('?')[0].split('#')[0]

    def done(reason: str | None) -> tuple[str | None, int]:
        return reason, int((time.monotonic() - t0) * 1000)

    # /images/… → public/
    if path.startswith('/images/'):
        target = PUBLIC_DIR / path.lstrip('/')
        if not target.exists():
            return done(f"file not found: public{path}")
        return done(None)

    # /blog/<slug> or /blog/<slug>/ → content/blog/**
    if path.startswith('/blog/') or path.startswith('/pages/'):
        slug = path.rstrip('/').split('/')[-1]
        if not slug:
            return done(None)  # bare /blog/ – valid index
        prefix = 'blog' if path.startswith('/blog/') else 'pages'
        matches = list((CONTENT_DIR / prefix).rglob(f"*{slug}*.md"))
        if not matches:
            return done(f"no content file found for slug '{slug}'")
        return done(None)

    # Everything else under public/
    target = PUBLIC_DIR / path.lstrip('/')
    if target.exists():
        return done(None)

    return done(f"file not found: public{path}")


# ── External link checking ───────────────────────────────────────────────────

def make_session(timeout: int) -> requests.Session:
    session = requests.Session()
    retry = Retry(total=2, backoff_factor=0.5,
                  status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=["HEAD", "GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (compatible; the78mole-link-checker/1.0; "
            "+https://the78mole-blog.github.io)"
        )
    })
    return session


def check_external(url: str, session: requests.Session, timeout: int) -> tuple[str | None, int]:
    """Return (error message or None, duration_ms)."""
    t0 = time.monotonic()
    try:
        r = session.head(url, timeout=timeout, allow_redirects=True)
        if r.status_code == 405:
            # HEAD not allowed – try GET
            r = session.get(url, timeout=timeout, allow_redirects=True, stream=True)
        ms = int((time.monotonic() - t0) * 1000)
        if r.status_code < 400:
            return None, ms
        if r.status_code == 999:
            # Bot-protection response (e.g. LinkedIn) – treat as OK but slow
            return None, max(ms, SLOW_MS)
        return f"HTTP {r.status_code}", ms
    except requests.exceptions.SSLError as e:
        return f"SSL error: {e}", int((time.monotonic() - t0) * 1000)
    except requests.exceptions.ConnectionError as e:
        return f"connection error: {e}", int((time.monotonic() - t0) * 1000)
    except requests.exceptions.Timeout:
        return f"timeout after {timeout}s", int((time.monotonic() - t0) * 1000)
    except requests.exceptions.RequestException as e:
        return f"request error: {e}", int((time.monotonic() - t0) * 1000)


# ── Main ─────────────────────────────────────────────────────────────────────

def load_ignores(ignore_file: Path | None) -> list[str]:
    if not ignore_file or not ignore_file.exists():
        return []
    lines = ignore_file.read_text().splitlines()
    return [l.strip() for l in lines if l.strip() and not l.strip().startswith('#')]


def should_ignore(url: str, ignores: list[str]) -> bool:
    return any(url.startswith(prefix) for prefix in ignores)


def load_manual_ok(manual_ok_file: Path | None) -> frozenset[str]:
    """Load exact URLs from the manual-ok whitelist (default: .checked-manual.txt)."""
    path = manual_ok_file if manual_ok_file else REPO_ROOT / ".checked-manual.txt"
    if not path.exists():
        return frozenset()
    lines = path.read_text(encoding="utf-8").splitlines()
    return frozenset(l.strip() for l in lines if l.strip() and not l.strip().startswith('#'))


# ── Link cache (.link_cache.json) ────────────────────────────────────────────

CACHE_FILE = REPO_ROOT / ".link_cache.json"
CACHE_TTL_PASSED  = 28   # days before re-checking a 'passed' URL
CACHE_TTL_MANUAL  = 365  # days before re-checking a 'manual' URL
CACHE_TTL_CAPTCHA = 365  # days before re-checking a 'captcha' URL


class LinkCache:
    """Persistent JSON cache for external link check results."""

    def __init__(self, path: Path = CACHE_FILE) -> None:
        self._path = path
        self._data: dict[str, dict] = {}
        if path.exists():
            try:
                self._data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                print(f"WARNING: could not load cache {path}, starting fresh.",
                      file=sys.stderr)

    def _entry(self, url: str) -> dict | None:
        return self._data.get(url)

    def should_skip(self, url: str, no_cache: bool) -> bool:
        """Return True if this URL can be skipped based on cache."""
        entry = self._entry(url)
        if not entry:
            return False
        status = entry.get("status")
        last_check = entry.get("last_check")
        if not last_check:
            return False
        try:
            checked_at = datetime.fromisoformat(last_check)
        except ValueError:
            return False
        age_days = (datetime.now(timezone.utc) - checked_at).days
        if status == "manual":
            # Manual URLs are always skipped unless older than TTL
            return age_days < CACHE_TTL_MANUAL
        if status == "captcha":
            # CAPTCHA-protected URLs are skipped unless older than TTL
            return age_days < CACHE_TTL_CAPTCHA
        if no_cache:
            return False
        if status == "passed":
            return age_days < CACHE_TTL_PASSED
        # 'failed' → never skip
        return False

    def get_cached_result(self, url: str) -> tuple[str | None, int]:
        """Return (reason, 0) from cache (0 ms = from cache).

        For 'manual' and 'captcha' status, reason is suppressed (treated as OK).
        """
        entry = self._entry(url)
        if not entry:
            return None, 0
        status = entry.get("status")
        if status in ("manual", "captcha"):
            return None, 0
        reason = entry.get("reason") or None
        return reason, 0

    def update(self, url: str, status: str, reason: str | None,
              sources: list[str] | None = None) -> None:
        entry: dict = {
            "status": status,
            "last_check": datetime.now(timezone.utc).isoformat(),
            "reason": reason or "",
        }
        if sources is not None:
            entry["sources"] = sorted(set(sources))
        elif url in self._data and "sources" in self._data[url]:
            entry["sources"] = self._data[url]["sources"]  # preserve existing
        self._data[url] = entry

    def save(self) -> None:
        self._path.write_text(
            json.dumps(self._data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


# ── Interactive error handling ────────────────────────────────────────────────

def correct_url_in_sources(old_url: str, new_url: str,
                            all_occurrences: dict[str, list[tuple[Path, int]]]) -> int:
    """Replace old_url with new_url in all source files. Returns number of replacements."""
    files = {f for f, _ in all_occurrences.get(old_url, [])}
    count = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        if old_url in text:
            n = text.count(old_url)
            path.write_text(text.replace(old_url, new_url), encoding="utf-8")
            count += n
            rel = path.relative_to(REPO_ROOT)
            print(f"  → replaced {n}× in {rel}")
    return count


def interactive_review(
    errors: list[tuple[Path, int, str, str, int]],
    cache: LinkCache,
    session: "requests.Session | None" = None,
    timeout: int = 10,
) -> None:
    """Walk through failed links interactively and let the user decide."""
    # Collect all occurrences per URL
    all_occurrences: dict[str, list[tuple[Path, int]]] = {}
    seen: dict[str, tuple[Path, int, str, int]] = {}
    for f, lineno, url, reason, ms in errors:
        all_occurrences.setdefault(url, []).append((f, lineno))
        if url not in seen:
            seen[url] = (f, lineno, reason, ms)

    if not seen:
        return

    print(f"\n{'═'*72}")
    print("  Interactive review of failed links")
    print(f"  {len(seen)} unique URL(s) to review")
    print(f"{'═'*72}\n")

    for url, (f, lineno, reason, ms) in seen.items():
        rel = f.relative_to(REPO_ROOT)
        n_occ = len(all_occurrences.get(url, []))
        occ_str = f"  ({n_occ} occurrence(s))" if n_occ > 1 else ""
        print(f"  URL:    {url}{occ_str}")
        print(f"  File:   {rel}:{lineno}")
        print(f"  Reason: {red(reason)}  ({ms} ms)")
        print(f"  [{yellow('o')}] OK/passed")
        print(f"  [{yellow('r')}] Retry now")
        print(f"  [{yellow('f')}] Fail (keep)")
        print(f"  [{yellow('i')}] Ignore/manual")
        print(f"  [{yellow('p')}] CAPTCHA-protected (manually verified)")
        print(f"  [{yellow('c')}] Correct URL")
        print(f"  [{yellow('q')}] Quit & save")
        while True:
            try:
                choice = input("  Your choice [o/r/f/i/p/c/q]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n  Aborted – remaining links kept as 'failed'.")
                cache.save()
                return
            if choice in ("o", "r", "f", "i", "c", "p", "q"):
                break
            print("  Please enter o, r, f, i, p, c, or q.")
        if choice == "q":
            cache.save()
            print(f"  {yellow('Review stopped – cache saved. Remaining links kept as \'failed\'.')}")
            return
        srcs = [str(f.relative_to(REPO_ROOT)) for f, _ in all_occurrences.get(url, [])]
        if choice == "r":
            if session is None:
                print(f"  {yellow('No HTTP session available – kept as failed.')}")
                cache.update(url, "failed", reason, sources=srcs)
            else:
                print(f"  Retrying …", end="", flush=True)
                new_reason, new_ms = check_external(url, session, timeout)
                if new_reason:
                    print(f"\r  → {red('still failing')}: {new_reason}  ({new_ms} ms)")
                    cache.update(url, "failed", new_reason, sources=srcs)
                else:
                    status_str = yellow(f"slow ({new_ms} ms)") if new_ms >= SLOW_MS else green("passed")
                    print(f"\r  → {status_str}")
                    cache.update(url, "passed", None, sources=srcs)
        elif choice == "o":
            cache.update(url, "passed", None, sources=srcs)
            print(f"  → {green('passed')}")
        elif choice == "i":
            cache.update(url, "manual", reason, sources=srcs)
            print(f"  → {yellow('manual')} (checked again in {CACHE_TTL_MANUAL} days)")
        elif choice == "p":
            cache.update(url, "captcha", "CAPTCHA-protected, manually verified", sources=srcs)
            print(f"  → {yellow('captcha')} (checked again in {CACHE_TTL_CAPTCHA} days)")
        elif choice == "c":
            try:
                new_url = input("  New URL: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n  Aborted – remaining links kept as 'failed'.")
                cache.save()
                return
            if not new_url:
                print(f"  {yellow('No URL entered – kept as failed.')}")
                cache.update(url, "failed", reason, sources=srcs)
            else:
                n = correct_url_in_sources(url, new_url, all_occurrences)
                if n:
                    # Remove old URL from cache; new URL will be checked next run
                    cache._data.pop(url, None)
                    print(f"  → {green(f'corrected in {n} place(s)')} – new URL will be checked next run")
                else:
                    print(f"  {yellow('URL not found in sources (already fixed?).')}")
                    cache.update(url, "failed", reason, sources=srcs)
        else:
            cache.update(url, "failed", reason, sources=srcs)
            print(f"  → {red('failed')} (will be re-checked next run)")
        print()

    cache.save()
    print(f"Cache saved to {CACHE_FILE}")


# ── Progress ─────────────────────────────────────────────────────────────────

def _progress(done: int, total: int, fails: int) -> None:
    """Overwrite the current stderr line with a progress bar."""
    bar_w = 28
    filled = round(bar_w * done / total) if total else 0
    bar = '█' * filled + '░' * (bar_w - filled)
    pct = round(100 * done / total) if total else 0
    fail_str = f"  {red(str(fails) + ' ✗')}" if fails else ''
    sys.stderr.write(f"\r  [{bar}] {pct:3d}%  {done}/{total}{fail_str}   ")
    sys.stderr.flush()


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> int:
    args = parse_args()
    ignores = load_ignores(args.ignore_file)
    cache = LinkCache()

    files: list[Path] = args.files if args.files else sorted(CONTENT_DIR.rglob("*.md"))

    # Collect all links: {url: [(file, lineno), …]}
    all_links: dict[str, list[tuple[Path, int]]] = {}
    n_files = len(files)
    for fi, f in enumerate(files, 1):
        if not f.exists():
            print(f"WARNING: file not found: {f}", file=sys.stderr)
            continue
        for lineno, url in extract_links(f):
            url = url.strip()
            if should_ignore(url, ignores):
                continue
            all_links.setdefault(url, []).append((f, lineno))
        n_links = len(all_links)
        sys.stderr.write(
            f"\r  Scanning files … {fi}/{n_files}  ({n_links} unique links found)   "
        )
        sys.stderr.flush()
    sys.stderr.write('\r' + ' ' * 72 + '\r')
    sys.stderr.flush()

    internal_urls = {u: occ for u, occ in all_links.items() if classify(u) == 'internal'}
    external_urls = {} if args.no_external else {
        u: occ for u, occ in all_links.items() if classify(u) == 'external'
    }
    total = len(internal_urls) + len(external_urls)

    # (file, line, url, reason, duration_ms)
    errors:   list[tuple[Path, int, str, str, int]] = []
    log_rows: list[tuple[str, str | None, int, Path, int]] = []

    done  = 0
    fails = 0
    lock  = threading.Lock()

    def record(url: str, occurrences: list[tuple[Path, int]],
               reason: str | None, ms: int) -> None:
        nonlocal done, fails
        f0, ln0 = occurrences[0]
        log_rows.append((url, reason, ms, f0, ln0))
        if reason:
            fails += 1
            for f, lineno in occurrences:
                errors.append((f, lineno, url, reason, ms))
        done += 1
        _progress(done, total, fails)

    # ── Internal links (fast, sequential) ────────────────────────────────────
    for url, occurrences in internal_urls.items():
        reason, ms = check_internal(url)
        record(url, occurrences, reason, ms)

    # ── External links (parallel, with cache) ───────────────────────────────
    if external_urls:
        # Split into cached-skip and to-check
        skip_cached: dict[str, list[tuple[Path, int]]] = {}
        to_check:    dict[str, list[tuple[Path, int]]] = {}
        for url, occ in external_urls.items():
            if cache.should_skip(url, args.no_check_cache):
                skip_cached[url] = occ
            else:
                to_check[url] = occ

        # Record cached results immediately (ms=0 → shown as 'cached')
        for url, occ in skip_cached.items():
            reason, ms = cache.get_cached_result(url)
            record(url, occ, reason, ms)

        session = make_session(args.timeout)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(check_external, url, session, args.timeout): url
                       for url in to_check}
            for future in as_completed(futures):
                url = futures[future]
                reason, ms = future.result()
                # Update cache
                status = "failed" if reason else "passed"
                srcs = [str(f.relative_to(REPO_ROOT)) for f, _ in to_check[url]]
                cache.update(url, status, reason, sources=srcs)
                with lock:
                    record(url, to_check[url], reason, ms)

        cache.save()

    # Clear progress line
    sys.stderr.write('\r' + ' ' * 72 + '\r')
    sys.stderr.flush()

    # ── Write log file ────────────────────────────────────────────────────────
    if args.log:
        log_rows.sort(key=lambda r: r[0])
        n_log_fail = sum(1 for _, r, _, _, _ in log_rows if r)
        n_log_slow = sum(1 for _, r, ms, _, _ in log_rows if not r and ms >= SLOW_MS)
        n_log_ok   = len(log_rows) - n_log_fail - n_log_slow
        with args.log.open('w', encoding='utf-8') as lf:
            for url, reason, ms, f, lineno in log_rows:
                rel = f.relative_to(REPO_ROOT)
                if reason:
                    prefix = "[FAIL        ]"
                elif ms >= SLOW_MS:
                    prefix = f"[OK - {ms:5d} ms] (slow)"
                else:
                    prefix = f"[OK - {ms:5d} ms]"
                lf.write(f"{prefix}  {url}\n")
                lf.write(f"               {rel}:{lineno}\n")
                if reason:
                    lf.write(f"               REASON: {reason}\n")

            # Summary block
            lf.write(f"\n{'═'*72}\n")
            lf.write(f"SUMMARY\n")
            lf.write(f"  Checked:          {len(log_rows)}\n")
            lf.write(f"  OK:               {n_log_ok}\n")
            lf.write(f"  Slow (>{SLOW_MS} ms): {n_log_slow}\n")
            lf.write(f"  FAILED:           {n_log_fail}\n")
            lf.write(f"  Total:            {len(log_rows)}\n")
            lf.write(f"{'═'*72}\n")

            if errors:
                lf.write(f"\nFAILED LINKS\n{'─'*72}\n")
                for fe, lineno_e, url_e, reason_e, ms_e in \
                        sorted(errors, key=lambda e: (str(e[0]), e[1])):
                    rel_e = fe.relative_to(REPO_ROOT)
                    lf.write(f"  {url_e}\n")
                    lf.write(f"    {rel_e}:{lineno_e}\n")
                    lf.write(f"    REASON: {reason_e}\n\n")

        print(f"Log written to {args.log}", file=sys.stderr)

    # ── Console output (summary + dead links only) ────────────────────────────
    errors.sort(key=lambda e: (str(e[0]), e[1]))

    n_total   = len(log_rows)
    n_fail    = sum(1 for _, r, _, _, _ in log_rows if r)
    n_slow    = sum(1 for _, r, ms, _, _ in log_rows if not r and ms >= SLOW_MS)
    n_ok      = n_total - n_fail - n_slow

    # Dead links
    if errors:
        print(f"\n{'─'*72}")
        print(f"  {red('FAILED LINKS')}")
        print(f"{'─'*72}\n")
        for f, lineno, url, reason, ms in errors:
            rel = f.relative_to(REPO_ROOT)
            print(f"  {red('[FAIL]')}  {rel}:{lineno}")
            print(f"    URL:    {url}")
            print(f"    REASON: {reason}  ({ms} ms)")
            print()

    # Summary
    print(f"{'─'*72}")
    ok_part     = green(f"OK: {n_ok}")
    slow_part   = ("  " + yellow(f"Slow (>{SLOW_MS} ms): {n_slow}")) if n_slow else ""
    fail_part   = ("  " + red(f"FAILED: {n_fail}")) if n_fail else ""
    print(f"  {ok_part}{slow_part}{fail_part}  |  Total: {n_total} URL(s)")
    print(f"{'─'*72}")

    if not errors:
        print(green("All links OK."))

    # ── Recheck schedule ─────────────────────────────────────────────────────
    now = datetime.now(timezone.utc)
    ttl_map = {"passed": CACHE_TTL_PASSED, "manual": CACHE_TTL_MANUAL,
               "captcha": CACHE_TTL_CAPTCHA}
    # bucket: months_remaining (1-based, 0 = overdue/this run) → count
    recheck_buckets: dict[int, int] = {}
    for url, entry in cache._data.items():
        status = entry.get("status")
        ttl = ttl_map.get(status)
        if ttl is None:
            continue  # 'failed' – not scheduled
        last_check = entry.get("last_check")
        if not last_check:
            continue
        try:
            checked_at = datetime.fromisoformat(last_check)
        except ValueError:
            continue
        days_remaining = ttl - (now - checked_at).days
        if days_remaining <= 0:
            continue  # already overdue / being checked this run
        months_remaining = max(1, (days_remaining + 29) // 30)  # ceiling months
        recheck_buckets[months_remaining] = recheck_buckets.get(months_remaining, 0) + 1

    if recheck_buckets:
        print(f"\n  {'Recheck in':}")
        max_count = max(recheck_buckets.values())
        count_width = len(str(max_count))
        for month in sorted(recheck_buckets):
            count = recheck_buckets[month]
            label = f"{month} Monat" if month == 1 else f"{month} Monaten"
            print(f"    {count:{count_width}d} URLs     < {label}")
    print(f"{'─'*72}")

    if errors:
        pass  # fall through to interactive review

    # ── Interactive review ────────────────────────────────────────────────────
    if not errors:
        return 0

    if not args.non_interactive and sys.stdin.isatty():
        _session = make_session(args.timeout) if not args.no_external else None
        interactive_review(errors, cache, session=_session, timeout=args.timeout)

    return 1


if __name__ == "__main__":
    sys.exit(main())
