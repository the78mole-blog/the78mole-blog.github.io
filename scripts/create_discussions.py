#!/usr/bin/env python3
"""create_discussions.py

Erstellt GitHub Discussions aus discussions/_all.json.
Nutzt die "Blog Comments"-Kategorie, damit giscus die Kommentare
mit den Blog-Posts verknüpft (mapping="pathname").

Idempotent: Markdown-Dateien mit vorhandenem `discussion_id:`-Feld
werden übersprungen.

Nach erfolgreicher Erstellung wird `discussion_id` und
`discussion_number` in das YAML-Frontmatter der Markdown-Datei
geschrieben.

Usage:
  uv run --project scripts scripts/create_discussions.py [--test] [--dry-run]

  --test     Nur den ersten Eintrag verarbeiten
  --dry-run  Keine API-Aufrufe, nur Ausgabe was passieren würde
"""

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import httpx
import yaml

# Regex zum Parsen des Kommentar-Headers (für Repair-Modus)
COMMENT_HEADER_RE = re.compile(
    r'_Historisch(?:er|e) (?:Bewertung|Kommentar|Antwort) von \*\*(.+?)\*\* \((\d{4}-\d{2}-\d{2})\)_'
)

# ── Konstanten ────────────────────────────────────────────────────────────────
REPO_OWNER  = "the78mole-blog"
REPO_NAME   = "the78mole-blog.github.io"
# Repo-Node-ID (aus nuxt.config.ts / giscus)
REPO_ID     = "R_kgDOSNCPlg"
# Kategorie "Blog Comments" – gleiche wie giscus
CATEGORY_ID = "DIC_kwDOSNCPls4C7zVP"

GH_GRAPHQL  = "https://api.github.com/graphql"

# Pause zwischen API-Aufrufen (Sekunden) – Rate-Limit-Schutz
API_DELAY      = 1.5
# Maximale Retry-Versuche bei Rate-Limit
MAX_RETRIES    = 5


# ── Auth ──────────────────────────────────────────────────────────────────────

def get_token() -> str:
    """GitHub-Token via `gh auth token` oder env GITHUB_TOKEN."""
    import os
    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True
        )
        token = result.stdout.strip()
    if not token:
        raise RuntimeError(
            "Kein GitHub Token gefunden. "
            "Bitte 'gh auth login' ausführen oder GITHUB_TOKEN setzen."
        )
    return token


# ── GraphQL-Helfer ────────────────────────────────────────────────────────────

def graphql(query: str, variables: dict, token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Github-Next-Global-ID": "1",
    }
    for attempt in range(1, MAX_RETRIES + 1):
        resp = httpx.post(
            GH_GRAPHQL,
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        errors = data.get("errors", [])
        if errors:
            # Rate-Limit? Mit Backoff wiederholen.
            rate_limited = any(
                "too quickly" in e.get("message", "").lower() or
                "rate limit" in e.get("message", "").lower()
                for e in errors
            )
            if rate_limited and attempt < MAX_RETRIES:
                wait = 2 ** attempt
                print(f"    ⏳ Rate-Limit (Versuch {attempt}/{MAX_RETRIES}), warte {wait}s …")
                time.sleep(wait)
                continue
            raise RuntimeError(f"GraphQL Fehler: {errors}")
        return data["data"]
    raise RuntimeError("Maximale Anzahl an Retries erreicht.")


def find_existing_discussion(token: str, title: str) -> tuple[str, int] | None:
    """Sucht eine vorhandene Discussion nach Titel. Gibt (node_id, number) oder None zurück."""
    query = """
    query FindDiscussion($owner: String!, $name: String!, $categoryId: ID!) {
      repository(owner: $owner, name: $name) {
        discussions(first: 100, categoryId: $categoryId) {
          nodes { id number title }
        }
      }
    }
    """
    data = graphql(query, {
        "owner": REPO_OWNER, "name": REPO_NAME, "categoryId": CATEGORY_ID
    }, token)
    for node in data["repository"]["discussions"]["nodes"]:
        if node["title"] == title:
            return node["id"], node["number"]
    return None


def create_discussion(token: str, title: str, body: str) -> tuple[str, int]:
    """Erstellt eine neue Discussion. Gibt (node_id, number) zurück."""
    mutation = """
    mutation CreateDiscussion($input: CreateDiscussionInput!) {
      createDiscussion(input: $input) {
        discussion { id number url }
      }
    }
    """
    data = graphql(mutation, {
        "input": {
            "repositoryId": REPO_ID,
            "categoryId": CATEGORY_ID,
            "title": title,
            "body": body,
        }
    }, token)
    d = data["createDiscussion"]["discussion"]
    print(f"    → #{d['number']} {d['url']}")
    return d["id"], d["number"]


def add_comment(
    token: str,
    discussion_id: str,
    body: str,
    reply_to_id: str | None = None,
) -> str:
    """Fügt einen Kommentar (oder Reply) hinzu. Gibt comment node_id zurück."""
    mutation = """
    mutation AddComment($input: AddDiscussionCommentInput!) {
      addDiscussionComment(input: $input) {
        comment { id }
      }
    }
    """
    inp: dict = {"discussionId": discussion_id, "body": body}
    if reply_to_id:
        inp["replyToId"] = reply_to_id
    data = graphql(mutation, {"input": inp}, token)
    return data["addDiscussionComment"]["comment"]["id"]


# ── Formatierung ──────────────────────────────────────────────────────────────

def format_discussion_body(disc: dict) -> str:
    bp = disc["blog_post"]
    path = bp["blog_url"].lstrip("/") + "/"
    wp_url   = bp["wp_url"]
    new_url  = f"https://the78mole.de/{path}"
    return (
        f"# {path}\n\n"
        f"Historische Kommentare aus WordPress, importiert aus dem alten Blog.\n\n"
        f"**Ursprünglicher Post:** {wp_url}  \n"
        f"**Neuer Post:** {new_url}\n\n"
        f"> _Diese Discussion enthält historische Kommentare, die aus WordPress migriert wurden._"
    )


def format_comment_body(comment: dict) -> str:
    date_str = comment["created_at"][:10]
    body     = (comment.get("body") or "").strip() or "_[kein Inhalt]_"

    # Blog-Autoren-Antwort auf eine Bewertung
    if comment.get("type") == "response":
        return (
            f"_Historische Antwort von **the78mole** ({date_str})_\n\n"
            f"{body}"
        )

    author = comment["author"]
    ctype  = "Bewertung" if comment.get("type") == "review" else "Kommentar"

    # Rating für Reviews ergänzen
    extra = ""
    if comment.get("type") == "review" and comment.get("rating"):
        stars = "★" * int(comment["rating"]) + "☆" * (5 - int(comment["rating"]))
        extra = f"\n\n**Bewertung:** {stars} ({comment['rating']}/5)"

    return (
        f"_Historischer {ctype} von **{author}** ({date_str})_\n\n"
        f"{body}"
        f"{extra}"
    )


# ── Repair-Helfer ────────────────────────────────────────────────────────────

def parse_comment_header(body: str) -> tuple[str, str] | None:
    """Extrahiert (author, date_str) aus dem Kommentar-Header."""
    m = COMMENT_HEADER_RE.search(body)
    return (m.group(1), m.group(2)) if m else None


def fetch_github_comments(token: str, discussion_number: int) -> list[dict]:
    """Holt alle Top-Level-Kommentare einer Discussion mit ID und Reply-Anzahl."""
    query = """
    query GetComments($owner: String!, $name: String!, $number: Int!, $cursor: String) {
      repository(owner: $owner, name: $name) {
        discussion(number: $number) {
          comments(first: 100, after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes { id body replies { totalCount } }
          }
        }
      }
    }
    """
    all_comments: list[dict] = []
    cursor: str | None = None
    while True:
        data = graphql(query, {
            "owner": REPO_OWNER, "name": REPO_NAME,
            "number": discussion_number, "cursor": cursor,
        }, token)
        page = data["repository"]["discussion"]["comments"]
        all_comments.extend(page["nodes"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
        time.sleep(API_DELAY)
    return all_comments


def read_frontmatter(md_path: Path) -> dict:
    """Liest YAML-Frontmatter aus einer .md-Datei."""
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.index("---\n", 4)
    return yaml.safe_load(text[4:end]) or {}


def repair_discussion(
    disc: dict,
    disc_id: str,
    disc_number: int,
    token: str,
    dry_run: bool = False,
) -> None:
    """Ergänzt fehlende Top-Level-Kommentare und Replies in einer vorhandenen Discussion."""
    print(f"    🔧 Repariere Discussion #{disc_number}...")

    gh_comments = fetch_github_comments(token, disc_number)
    time.sleep(API_DELAY)

    # Lookup: (author_lower, date_yyyy-mm-dd) → {id, reply_count}
    gh_map: dict[tuple[str, str], dict] = {}
    for ghc in gh_comments:
        parsed = parse_comment_header(ghc["body"])
        if parsed:
            author, date = parsed
            gh_map[(author.lower(), date)] = {
                "id":          ghc["id"],
                "reply_count": ghc["replies"]["totalCount"],
            }

    added_comments = 0
    added_replies  = 0

    for comment in disc["comments"]:
        key          = (comment["author"].lower(), comment["created_at"][:10])
        json_replies = comment.get("replies", [])

        if key not in gh_map:
            # Fehlender Top-Level-Kommentar
            if dry_run:
                print(f"    [DRY] + NEU: {comment['author']} ({comment['created_at'][:10]})")
                for r in json_replies:
                    print(f"    [DRY]   ↳ NEU Reply: {r['author']}")
                added_comments += 1
                added_replies  += len(json_replies)
                continue

            cbody      = format_comment_body(comment)
            comment_id = add_comment(token, disc_id, cbody)
            print(f"    + NEU: {comment['author']} (wp#{comment['wp_id']}) → {comment_id}")
            added_comments += 1
            time.sleep(API_DELAY)

            for reply in json_replies:
                rbody = format_comment_body(reply)
                add_comment(token, disc_id, rbody, reply_to_id=comment_id)
                print(f"      ↳ NEU Reply: {reply['author']} (wp#{reply['wp_id']})")
                added_replies += 1
                time.sleep(API_DELAY)
        else:
            gh_info = gh_map[key]
            if json_replies and gh_info["reply_count"] < len(json_replies):
                # Nicht alle Replies vorhanden → fehlende hinzufügen
                # Einfachster Fall: gh hat 0 replies, wir fügen alle hinzu
                # (keine Teilidempotenz nötig, da replies bisher nie erstellt wurden)
                if dry_run:
                    for r in json_replies[gh_info["reply_count"]:]:
                        print(f"    [DRY]   ↳ NEU Reply zu {comment['author']}: {r['author']}")
                    added_replies += len(json_replies) - gh_info["reply_count"]
                    continue

                for reply in json_replies[gh_info["reply_count"]:]:
                    rbody = format_comment_body(reply)
                    add_comment(token, disc_id, rbody, reply_to_id=gh_info["id"])
                    print(f"      ↳ NEU Reply: {reply['author']} (wp#{reply['wp_id']})")
                    added_replies += 1
                    time.sleep(API_DELAY)

    print(f"    ✓ Reparatur: {added_comments} Kommentare, {added_replies} Replies hinzugefügt.")


# ── Frontmatter-Update ────────────────────────────────────────────────────────

def update_md_frontmatter(
    md_path: Path, discussion_id: str, discussion_number: int
) -> None:
    """Fügt discussion_id und discussion_number in das YAML-Frontmatter ein."""
    text = md_path.read_text(encoding="utf-8")
    # Zweites '---' finden (Ende des Frontmatters)
    end_idx = text.index("---\n", 4)  # überspringt das erste ---
    insertion = (
        f"discussion_id: {discussion_id}\n"
        f"discussion_number: {discussion_number}\n"
    )
    new_text = text[:end_idx] + insertion + text[end_idx:]
    md_path.write_text(new_text, encoding="utf-8")


# ── Hauptlogik ────────────────────────────────────────────────────────────────

def process_discussion(
    disc: dict,
    md_path: Path,
    token: str,
    dry_run: bool = False,
    repair: bool = False,
) -> None:
    bp    = disc["blog_post"]
    title = bp["blog_url"].lstrip("/") + "/"  # giscus pathname-mapping
    body  = format_discussion_body(disc)
    n_comments = sum(1 + len(c.get("replies", [])) for c in disc["comments"])

    print(f"\n  Discussion: {title}")
    print(f"    Kommentare: {len(disc['comments'])} top-level, {n_comments} gesamt")

    if dry_run and not repair:
        print(f"    [DRY RUN] Kein API-Aufruf.")
        for c in disc["comments"]:
            print(f"      + {c['author']} ({c['created_at'][:10]})")
            for r in c.get("replies", []):
                print(f"        ↳ {r['author']} ({r['created_at'][:10]})")
        return

    # Im Repair-Modus: discussion_id aus Frontmatter lesen (spart API-Call)
    if repair and md_path.exists():
        fm = read_frontmatter(md_path)
        disc_id  = fm.get("discussion_id")
        disc_num = fm.get("discussion_number")
        if disc_id and disc_num:
            repair_discussion(disc, disc_id, disc_num, token, dry_run=dry_run)
            return

    # Bereits auf GitHub vorhandene Discussion suchen (Idempotenz)
    existing = find_existing_discussion(token, title)
    if existing:
        disc_id, disc_num = existing
        if repair:
            update_md_frontmatter(md_path, disc_id, disc_num)
            repair_discussion(disc, disc_id, disc_num, token, dry_run=dry_run)
        else:
            print(f"    ⚠ Discussion bereits vorhanden: #{disc_num} – Frontmatter wird ergänzt, Kommentare NICHT erneut importiert.")
            update_md_frontmatter(md_path, disc_id, disc_num)
            print(f"    ✓ Frontmatter aktualisiert: {md_path.name}")
        return

    # Discussion erstellen
    disc_id, disc_num = create_discussion(token, title, body)
    time.sleep(API_DELAY)

    # Frontmatter SOFORT nach Erstellung sichern (vor Kommentaren)
    update_md_frontmatter(md_path, disc_id, disc_num)
    print(f"    ✓ Frontmatter gesichert: {md_path.name}")

    # Kommentare und Replies hinzufügen
    for comment in disc["comments"]:
        cbody      = format_comment_body(comment)
        comment_id = add_comment(token, disc_id, cbody)
        print(f"    + {comment['author']} (wp#{comment['wp_id']}) → {comment_id}")
        time.sleep(API_DELAY)

        for reply in comment.get("replies", []):
            rbody    = format_comment_body(reply)
            reply_id = add_comment(token, disc_id, rbody, reply_to_id=comment_id)
            print(f"      ↳ {reply['author']} (wp#{reply['wp_id']}) → {reply_id}")
            time.sleep(API_DELAY)

    print(f"    ✓ Alle Kommentare importiert.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Erstellt GitHub Discussions aus discussions/_all.json"
    )
    parser.add_argument(
        "--test", action="store_true",
        help="Nur den ersten (noch nicht vorhandenen) Eintrag verarbeiten"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Keine API-Aufrufe – nur anzeigen, was passieren würde"
    )
    parser.add_argument(
        "--repair", action="store_true",
        help="Fehlende Kommentare und Replies zu vorhandenen Discussions hinzufügen"
    )
    args = parser.parse_args()

    base           = Path(__file__).parent.parent
    all_json       = base / "discussions" / "_all.json"
    discussions_dir = base / "discussions"

    if not all_json.exists():
        print(f"FEHLER: {all_json} nicht gefunden. Bitte zuerst assign_comments.py ausführen.")
        sys.exit(1)

    discussions = json.loads(all_json.read_text(encoding="utf-8"))
    token       = get_token() if (not args.dry_run or args.repair) else "dry-run"

    created = skipped = repaired = 0

    for disc in discussions:
        slug    = disc["blog_post"]["blog_url"].strip("/").split("/")[-1]
        md_path = discussions_dir / f"{slug}.md"

        # Idempotenz-Check: Frontmatter bereits mit discussion_id?
        already_done = md_path.exists() and "discussion_id:" in md_path.read_text(encoding="utf-8")

        if already_done and not args.repair:
            print(f"  SKIP (bereits vorhanden): {slug}")
            skipped += 1
            continue

        process_discussion(disc, md_path, token, dry_run=args.dry_run, repair=args.repair or already_done)
        if already_done:
            repaired += 1
        else:
            created += 1

        if args.test:
            print(f"\n  Test-Modus: Stoppe nach erstem Eintrag.")
            break

    print(f"\nFertig: {created} erstellt, {repaired} repariert, {skipped} übersprungen.")


if __name__ == "__main__":
    main()
