"""
Extrahiert wp:comment-Kommentare UND glsr-Reviews aus dem WordPress-XML-Export.
Reviews sind als PHP-serialisierte _glsr_export-Postmeta gespeichert.

Verwendung (aus Repo-Root):
    uv run --project scripts scripts/extract_comments.py [XML_PATH]

Ausgabe:
    import/wp_comments.json   – alle Eintraege als JSON
    import/wp_comments.md     – lesbare Markdown-Uebersicht (ohne Pingbacks)
"""

import re
import json
import sys
from pathlib import Path
from lxml import etree

REPO_ROOT = Path(__file__).resolve().parent.parent
XML_PATH  = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / 'import' / 'molesblog.WordPress.2026-04-26.xml'
OUT_JSON  = REPO_ROOT / 'import' / 'wp_comments.json'
OUT_MD    = REPO_ROOT / 'import' / 'wp_comments.md'

WP = 'http://wordpress.org/export/1.2/'
Q  = '{' + WP + '}'

CONTENT_NS = 'http://purl.org/rss/1.0/modules/content/'
QC = '{' + CONTENT_NS + '}'


def load_xml(path: Path):
    """Laedt und bereinigt das WXR-XML (entfernt ungueltite XML-1.0-Steuerzeichen)."""
    raw     = path.read_bytes()
    cleaned = re.sub(b'[\x00-\x08\x0B\x0C\x0E-\x1F]', b'', raw)
    parser  = etree.XMLParser(recover=True, huge_tree=True)
    return etree.fromstring(cleaned, parser)


def parse_php_string(s: str, key: str) -> str:
    """Extrahiert einen Wert aus einem PHP-serialisierten Array (byte-korrekt).
    PHP-Serialisierung verwendet Byte-Laengen; multi-byte UTF-8-Zeichen (z.B. ü, …)
    haben Byte-Laenge > 1, weshalb die Suche auf Bytes operieren muss.
    Format: s:<byte_len>:"<key>";s:<byte_len>:"<value>";
    """
    s_bytes   = s.encode('utf-8')
    key_bytes = key.encode('utf-8')
    pattern   = b's:' + str(len(key_bytes)).encode() + b':"' + key_bytes + b'";s:'
    idx       = s_bytes.find(pattern)
    if idx == -1:
        return ''
    after  = s_bytes[idx + len(pattern):]
    colon  = after.index(b':"')
    length = int(after[:colon])
    start  = colon + 2
    return after[start:start + length].decode('utf-8', errors='replace')


def extract_comments(tree) -> list[dict]:
    """Alle wp:comment-Eintraege (Kommentare + Pingbacks)."""
    results = []
    for item in tree.findall('.//item'):
        title = item.findtext('title') or ''
        link  = item.findtext('link')  or ''
        for c in item.findall(Q + 'comment'):
            results.append({
                'source':       'wp_comment',
                'post_title':   title,
                'post_link':    link,
                'id':           c.findtext(Q + 'comment_id')           or '',
                'parent':       c.findtext(Q + 'comment_parent')       or '0',
                'type':         c.findtext(Q + 'comment_type')         or 'comment',
                'approved':     c.findtext(Q + 'comment_approved')     or '',
                'date':         c.findtext(Q + 'comment_date')         or '',
                'author':       c.findtext(Q + 'comment_author')       or '',
                'email':        c.findtext(Q + 'comment_author_email') or '',
                'url':          c.findtext(Q + 'comment_author_url')   or '',
                'rating':       '',
                'review_title': '',
                'content':      (c.findtext(Q + 'comment_content') or '').strip(),
            })
    return results


def extract_glsr_reviews(tree, post_map: dict) -> list[dict]:
    """Alle Site-Reviews aus site-review-Posts.
    Jede Review ist ein eigener WP-Post vom Typ 'site-review':
      - title           = Review-Ueberschrift (vom Autor)
      - content:encoded = Review-Text
      - _glsr_export    = PHP-serialisiertes Dict mit name, email, rating, post_ids
    post_ids zeigt auf den Blog-Post, dem die Review zugeordnet ist.
    """
    results   = []
    review_num = 0
    for item in tree.findall('.//item'):
        if (item.findtext(Q + 'post_type') or '') != 'site-review':
            continue
        review_num += 1

        date    = item.findtext(Q + 'post_date') or ''
        title   = (item.findtext('title') or '').strip()
        content = (item.findtext(QC + 'encoded') or '').strip()

        # Alle relevanten Postmeta-Felder einsammeln
        meta_map: dict[str, str] = {}
        for meta in item.findall(Q + 'postmeta'):
            k = meta.findtext(Q + 'meta_key') or ''
            v = meta.findtext(Q + 'meta_value') or ''
            meta_map[k] = v

        export_val = meta_map.get('_glsr_export', '')
        response   = (meta_map.get('_response',    '') or '').strip()

        author   = parse_php_string(export_val, 'name')     if export_val else ''
        email    = parse_php_string(export_val, 'email')    if export_val else ''
        rating   = parse_php_string(export_val, 'rating')   if export_val else ''
        post_ids = parse_php_string(export_val, 'post_ids') if export_val else ''

        # Erster verknuepfter Blog-Post
        linked_id = post_ids.split(',')[0].strip() if post_ids else ''
        post_info = post_map.get(linked_id, {})

        results.append({
            'source':       'glsr_review',
            'post_id':      linked_id,
            'post_title':   post_info.get('title', ''),
            'post_link':    post_info.get('link', ''),
            'id':           f'r{review_num}',
            'type':         'review',
            'approved':     '1',
            'date':         date,
            'author':       author,
            'email':        email,
            'url':          '',
            'rating':       rating,
            'review_title': title,
            'content':      content,
            'response':     response,
        })
    return results


def write_markdown(entries: list[dict], all_entries: list[dict], path: Path) -> None:
    """Schreibt eine lesbare Markdown-Uebersicht (Pingbacks und leere Eintraege ausgefiltert)."""
    relevant = sorted(
        [c for c in entries if c['type'] in ('comment', 'review', '')
         and c['approved'] == '1' and c['content']],
        key=lambda x: (x['post_title'], x['date']),
    )
    by_type: dict[str, int] = {}
    for c in all_entries:
        by_type[c['type']] = by_type.get(c['type'], 0) + 1

    lines = [
        '# WordPress-Kommentare & Reviews\n',
        f'Exportiert aus `{XML_PATH.name}`  ',
        'Gesamt: **' + str(len(all_entries)) + '** Eintraege | ' +
        ' | '.join(f'{t or "(leer)"}: {n}' for t, n in sorted(by_type.items(), key=lambda x: -x[1])),
        f'Davon relevant (comment/review, approved, mit Inhalt): **{len(relevant)}**\n',
        '---\n',
    ]

    current_post = None
    for c in relevant:
        if c['post_title'] != current_post:
            current_post = c['post_title']
            lines.append(f'\n## {c["post_title"]}\n')
            if c['post_link']:
                lines.append(f'<{c["post_link"]}>\n')

        stars = ('⭐' * int(c['rating'])) if c.get('rating', '').isdigit() else ''
        star_str = f' | {stars} ({c["rating"]}/5)' if stars else ''

        lines.append(f'**{c["author"]}** ({c["email"]}) — {c["date"]}  ')
        lines.append(f'*Typ: {c["type"]} | ID: {c["id"]}*{star_str}\n')
        if c.get('review_title'):
            lines.append(f'**{c["review_title"]}**  ')
        for line in c['content'].splitlines():
            lines.append(f'> {line}  ')
        lines.append('\n---\n')

    path.write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    print(f'Reading: {XML_PATH}')
    tree = load_xml(XML_PATH)

    items = tree.findall('.//item')
    print(f'Posts/Pages found: {len(items)}')

    post_map = {
        (item.findtext(Q + 'post_id') or ''): {
            'title': item.findtext('title') or '',
            'link':  item.findtext('link')  or '',
        }
        for item in items
        if item.findtext(Q + 'post_id')
    }

    comments = extract_comments(tree)
    print(f'wp:comment entries: {len(comments)}')

    reviews = extract_glsr_reviews(tree, post_map)
    print(f'glsr reviews found: {len(reviews)}')

    everything = comments + reviews

    OUT_JSON.write_text(
        json.dumps(everything, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f'Written: {OUT_JSON}')

    write_markdown(everything, everything, OUT_MD)
    print(f'Written: {OUT_MD}')

    by_type: dict[str, int] = {}
    for c in everything:
        by_type[c['type']] = by_type.get(c['type'], 0) + 1
    print('\nBy type:')
    for t, n in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f'  {t or "(empty)"}: {n}')


if __name__ == '__main__':
    main()
