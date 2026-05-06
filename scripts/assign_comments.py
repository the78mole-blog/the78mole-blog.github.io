"""
Gruppiert WordPress-Kommentare und Reviews nach Blog-Post und schreibt
eine fertige Discussion-Struktur nach discussions/.

Pro Post entsteht:
  discussions/<slug>.json   – maschinenlesbar (GitHub API / gh CLI)
  discussions/<slug>.md     – Vorschau zum manuellen Lesen

Ausserdem:
  discussions/_all.json     – alle Discussions als Array

Verwendung (aus Repo-Root):
    uv run --project scripts scripts/assign_comments.py [--dry-run]

Quellen:
    import/wp_comments.json   – erzeugt von extract_comments.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT     = Path(__file__).resolve().parent.parent
COMMENTS_JSON = REPO_ROOT / 'import' / 'wp_comments.json'
CONTENT_DIR   = REPO_ROOT / 'content'
OUT_DIR       = REPO_ROOT / 'discussions'

DRY_RUN = '--dry-run' in sys.argv


def slug_from_url(url: str) -> str:
    return url.rstrip('/').split('/')[-1]


def find_content_file(slug: str) -> Path | None:
    matches = list(CONTENT_DIR.rglob(f'{slug}.md'))
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    blog = [m for m in matches if 'blog' in m.parts]
    return blog[0] if blog else matches[0]


def iso_date(date_str: str) -> str:
    """Gibt 'YYYY-MM-DDTHH:MM:SS' zurueck."""
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%Y-%m-%dT%H:%M:%S')
    except Exception:
        return date_str


def build_comment_node(c: dict, id_map: dict, depth: int = 0) -> dict:
    """Baut einen Kommentar-Node mit optionalem Eltern-Zitat fuer tief verschachtelte Antworten.

    GitHub Discussions unterstuetzt nur 1 Ebene von Replies (Kommentar → Antwort).
    Antworten auf Antworten (depth >= 2) erhalten einen zitierten Kontext-Header,
    damit der Gespraechsfaden ohne strukturelle Verschachtelung lesbar bleibt.
    """
    stars     = '⭐' * int(c['rating']) if c.get('rating', '').isdigit() else ''
    rev_title = c.get('review_title', '')

    parts = []
    # Bei tief verschachtelten Antworten (depth >= 2): Eltern-Autor zitieren
    if depth >= 2:
        parent = id_map.get(c.get('parent', '0'))
        if parent:
            quote_lines = (parent['content'].strip().splitlines() or [''])[:3]
            quote = '\n'.join(f'> {ln}' for ln in quote_lines)
            if len(parent['content'].strip().splitlines()) > 3:
                quote += '\n> …'
            parts.append(f'*Antwort auf **{parent["author"]}**:*')
            parts.append(quote)
            parts.append('')
    if stars:
        parts.append(f'**{stars}**')
    if rev_title:
        parts.append(f'*{rev_title}*')
    if parts:
        parts.append('')
    parts.extend(c['content'].strip().splitlines())

    return {
        'created_at': iso_date(c['date']),
        'author':     c['author'],
        'email':      c.get('email', ''),
        'type':       c['type'],
        'wp_id':      c['id'],
        'body':       '\n'.join(parts).strip(),
    }


def build_discussion(post_url: str, post_title: str, content_file: Path | None,
                     comments: list[dict]) -> dict:
    """Erstellt das Discussion-Dict fuer einen Blog-Post.

    Kommentar-Hierarchie (comment_parent) wird auf GitHub-Discussions-Ebenen gemappt:
      parent=0       → top-level comment
      parent=<id>    → reply unter dem jeweiligen top-level-Vorfahren
    Replies-auf-Replies werden mit zitiertem Kontext flachgedrückt (GitHub erlaubt
    nur eine Verschachtelungsebene).
    """
    rel_path = str(content_file.relative_to(REPO_ROOT)) if content_file else ''
    blog_url = ''
    if content_file:
        rel      = content_file.relative_to(CONTENT_DIR)
        blog_url = '/' + str(rel.with_suffix(''))

    body_lines = [
        'Historische Kommentare aus WordPress, importiert aus dem alten Blog.',
        '',
        f'**Ursprünglicher Post:** [{post_title}]({post_url})  ',
    ]
    if blog_url:
        body_lines.append(f'**Neuer Post:** [{blog_url}]({blog_url})')

    # Index: wp_id → raw comment dict (für Eltern-Zitate)
    id_map: dict[str, dict] = {c['id']: c for c in comments if 'id' in c}

    # Tiefe im Baum ermitteln (iterativ, max-Sicherung gegen Kreise)
    def depth_of(cid: str, seen: set | None = None) -> int:
        seen = seen or set()
        if cid in seen:
            return 0
        seen.add(cid)
        parent_id = (id_map.get(cid) or {}).get('parent', '0')
        if not parent_id or parent_id == '0':
            return 0
        return 1 + depth_of(parent_id, seen)

    # Oberstes Top-Level-Vorfahren-ID ermitteln
    def root_of(cid: str, seen: set | None = None) -> str:
        seen = seen or set()
        if cid in seen:
            return cid
        seen.add(cid)
        parent_id = (id_map.get(cid) or {}).get('parent', '0')
        if not parent_id or parent_id == '0':
            return cid
        return root_of(parent_id, seen)

    # Reviews (kein parent-Feld) → immer top-level
    top_level:  list[dict] = []
    replies_by_root: dict[str, list[tuple[int, dict]]] = {}  # root_id → [(depth, comment)]

    for c in sorted(comments, key=lambda x: x['date']):
        parent = c.get('parent', '0')
        if parent == '0' or not parent:
            top_level.append(c)
        else:
            root_id = root_of(c['id'])
            d       = depth_of(c['id'])
            replies_by_root.setdefault(root_id, []).append((d, c))

    # Discussion-Kommentare mit replies[] aufbauen
    discussion_comments = []
    for c in top_level:
        node    = build_comment_node(c, id_map, depth=0)
        replies = []
        for depth, reply in replies_by_root.get(c['id'], []):
            replies.append(build_comment_node(reply, id_map, depth=depth))
        # _response des Blog-Autors als synthetische Reply anhängen
        if c.get('response'):
            replies.append({
                'created_at': iso_date(c['date']),
                'author':     'the78mole',
                'email':      'me@the78mole.de',
                'type':       'response',
                'wp_id':      c['id'] + '_response',
                'body':       c['response'].strip(),
            })
        if replies:
            node['replies'] = replies
        discussion_comments.append(node)

    return {
        'title':        f'Kommentare: {post_title}',
        'category':     'General',
        'blog_post': {
            'title':        post_title,
            'wp_url':       post_url,
            'content_file': rel_path,
            'blog_url':     blog_url,
        },
        'body':     '\n'.join(body_lines),
        'comments': discussion_comments,
    }


def render_markdown(disc: dict) -> str:
    total = sum(1 + len(c.get('replies', [])) for c in disc['comments'])
    bp    = disc['blog_post']
    lines = [
        '---',
        f'title: {json.dumps(disc["title"])}',
        f'category: {disc["category"]}',
        f'wp_url: {bp["wp_url"]}',
        f'blog_url: {bp["blog_url"]}',
        f'content_file: {bp["content_file"]}',
        f'total_comments: {total}',
        '---',
        '',
        f'## Kommentare ({total})',
        '',
    ]
    for c in disc['comments']:
        lines.append(f'**{c["author"]}** – {c["created_at"][:10]}')
        lines.append('')
        for line in c['body'].splitlines():
            lines.append(f'> {line}' if line.strip() else '>')
        lines.append('')
        for r in c.get('replies', []):
            lines.append(f'↳ **{r["author"]}** – {r["created_at"][:10]}')
            lines.append('')
            for line in r['body'].splitlines():
                lines.append(f'>> {line}' if line.strip() else '>>')
            lines.append('')
        lines.append('---')
        lines.append('')
    return '\n'.join(lines)


def main() -> None:
    if not COMMENTS_JSON.exists():
        print(f'ERROR: {COMMENTS_JSON} nicht gefunden. Bitte erst extract_comments.py ausfuehren.')
        sys.exit(1)

    data = json.loads(COMMENTS_JSON.read_text(encoding='utf-8'))

    relevant = [c for c in data
                if c['type'] in ('comment', 'review')
                and c['approved'] == '1'
                and c.get('content', '').strip()]

    by_url: dict[str, list[dict]] = {}
    for c in relevant:
        url = c.get('post_link', '') or ''
        if not url:
            continue
        by_url.setdefault(url, []).append(c)

    print(f'Posts mit Kommentaren/Reviews: {len(by_url)}')
    print(f'Eintraege gesamt: {len(relevant)}')
    print()

    if not DRY_RUN:
        OUT_DIR.mkdir(parents=True, exist_ok=True)

    all_discussions = []
    missing = 0

    for url, comments in sorted(by_url.items()):
        slug         = slug_from_url(url)
        content_file = find_content_file(slug)
        post_title   = comments[0].get('post_title') or slug

        if content_file is None:
            print(f'  NICHT GEFUNDEN: {slug}  ({url})')
            missing += 1

        disc = build_discussion(url, post_title, content_file, comments)
        all_discussions.append(disc)

        rel = str(content_file.relative_to(REPO_ROOT)) if content_file else '(nicht gefunden)'
        print(f'  {len(comments):2d} Eintr.  {slug}')
        print(f'       → {rel}')

        if not DRY_RUN:
            json_path = OUT_DIR / f'{slug}.json'
            md_path   = OUT_DIR / f'{slug}.md'
            json_path.write_text(json.dumps(disc, indent=2, ensure_ascii=False), encoding='utf-8')
            md_path.write_text(render_markdown(disc), encoding='utf-8')

    if not DRY_RUN:
        all_path = OUT_DIR / '_all.json'
        all_path.write_text(json.dumps(all_discussions, indent=2, ensure_ascii=False), encoding='utf-8')
        print()
        print(f'Geschrieben nach: {OUT_DIR.relative_to(REPO_ROOT)}/')
        print(f'  {len(all_discussions)} *.json + *.md Dateien + _all.json')
    else:
        print()
        print(f'DRY-RUN: {len(all_discussions)} Discussions wuerden erzeugt ({missing} Posts nicht gefunden).')

    if missing:
        print(f'WARNUNG: {missing} Post(s) ohne Treffer in content/')


if __name__ == '__main__':
    main()
