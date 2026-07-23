---
name: wp-to-giscus-migration
description: >
  Migration von WordPress-Kommentaren und -Bewertungen in GitHub Discussions für Giscus.
  Verwende diesen Skill für: extract_comments.py debuggen oder erweitern; assign_comments.py
  anpassen (Threading, Frontmatter, Slugs); create_discussions.py tunen (Rate-Limit,
  Idempotenz, Kategorie); neues WP-Backup importieren; discussions/-Dateien regenerieren;
  PHP-Serialisierung parsen; WXR-XML-Format verstehen; giscus-pathname-Mapping konfigurieren;
  neue WordPress-Plugin-Daten extrahieren.
---

# WordPress → GitHub Discussions Migration (Giscus)

## Überblick

Dieses Repo migriert Kommentare und Bewertungen aus einem WordPress-Backup (WXR-Format)
in GitHub Discussions, damit **giscus** (`mapping="pathname"`) sie als Blog-Kommentare anzeigt.

### Drei-Schritt-Pipeline

```
import/molesblog.WordPress.*.xml
        │
        ▼  scripts/extract_comments.py
import/wp_comments.json
        │
        ▼  scripts/assign_comments.py
discussions/<slug>.json + <slug>.md + _all.json
        │
        ▼  scripts/create_discussions.py
GitHub Discussions #13–#22 (Kategorie "Blog Comments")
```

---

## Quelldaten: WordPress-Export (WXR)

### Datei

```
import/molesblog.WordPress.2026-04-26.xml
```

### WordPress-Plugins, deren Daten migriert wurden

| Plugin | Post-Typ / Meta-Key | Beschreibung |
|---|---|---|
| **Site Reviews** (v7.x) | `post_type = site-review` | Sternebewertungen mit Text. Jeder Review ist ein eigener WP-Post. |
| Site Reviews | `_glsr_export` (postmeta) | PHP-serialisiertes Array mit Autor, E-Mail, Rating, verknüpften Post-IDs |
| Site Reviews | `_glsr_average`, `_glsr_ranking`, `_glsr_reviews` | Aggregierte Statistiken auf dem zugehörigen Blog-Post |
| **WordPress Core** | `wp:comment` mit `wp:comment_type = comment` | Standard-Blog-Kommentare mit Threading via `wp:comment_parent` |
| WordPress Core | `wp:comment_type = pingback` | Pingbacks (werden beim Import ignoriert) |
| **Contact Form 7** | `post_type = wpcf7_contact_form` | Kontaktformulare (nicht migriert) |
| **W3 Total Cache** | diverse `_w3tc_*` meta | Cache-Metadaten (ignoriert) |
| **Yoast SEO** | `_yoast_*` meta | SEO-Metadaten (nicht migriert) |
| **WP Last Modified Info** | `wp_last_modified_info`, `wplmi_shortcode` | Zeitstempel (ignoriert) |

### Relevante XML-Namespaces

| Präfix | URI | Inhalt |
|---|---|---|
| `wp:` | `http://wordpress.org/export/1.2/` | WordPress-spezifische Felder |
| `content:` | `http://purl.org/rss/1.0/modules/content/` | `content:encoded` = Volltext des Posts/Reviews |
| *(kein)* | – | `title`, `link`, `pubDate` aus RSS-Core |

### Häufige Fallstricke beim XML-Parsen

- Das WXR-XML enthält ungültige XML-1.0-Steuerzeichen (`\x00-\x08`, `\x0B`, `\x0C`, `\x0E-\x1F`).
  → Vor dem Parsen per `re.sub(b'[\x00-\x08\x0B\x0C\x0E-\x1F]', b'', raw)` entfernen.
- `lxml` mit `recover=True, huge_tree=True` initialisieren.
- PHP-Serialisierung in `_glsr_export` enthält Byte-Längen (nicht Zeichen-Längen).
  Bei UTF-8-Zeichen > 1 Byte (z. B. Umlaute) **muss** die Extraktion auf Bytes arbeiten.

---

## Skripte

Alle Skripte liegen in `scripts/` als eigenständiges `uv`-Projekt.

### Ausführung

```bash
# Aus dem Repo-Root:
uv run --project scripts scripts/<script>.py [Optionen]
```

### Abhängigkeiten (`scripts/pyproject.toml`)

```toml
dependencies = [
    "lxml>=5.0",          # XML-Parser für WXR
    "beautifulsoup4>=4.12", # HTML-Cleanup in Kommentartexten
    "markdownify>=0.13",  # HTML → Markdown für Blog-Post-Migration
    "pyyaml>=6.0",        # YAML-Frontmatter lesen/schreiben
    "httpx>=0.27",        # GitHub GraphQL API
]
```

Systemvoraussetzung: `gh` CLI muss angemeldet sein (`gh auth login`).

---

### `scripts/extract_comments.py`

**Zweck:** Rohdaten aus dem WXR-XML extrahieren.

**Ausgabe:**
- `import/wp_comments.json` – alle Einträge (Kommentare + Reviews, ohne Pingbacks)
- `import/wp_comments.md` – menschenlesbare Vorschau

**Wichtige Funktionen:**

```python
parse_php_string(s, key)   # Byte-korrekte PHP-Serialisierungs-Extraktion
extract_comments(tree)     # wp:comment-Einträge (type=comment), mit parent-Feld
extract_glsr_reviews(tree) # site-review-Posts: Text aus content:encoded,
                            # Metadaten aus _glsr_export
```

**JSON-Struktur eines Eintrags:**

```json
{
  "id":         "37",
  "parent":     "0",
  "post_url":   "https://the78mole.de/km271-wifi-howto/",
  "post_title": "KM271 WiFi Howto",
  "author":     "Petr Novotný",
  "email":      "petr@example.com",
  "date":       "2023-05-03 17:22:01",
  "content":    "Kommentartext …",
  "type":       "comment",
  "rating":     ""
}
```

Reviews haben zusätzlich `"rating": "5"` und `"type": "review"`.

---

### `scripts/assign_comments.py`

**Zweck:** Einträge nach Blog-Post gruppieren, Threading aufbauen,
GitHub-Discussions-kompatible JSON- und Markdown-Dateien schreiben.

**Ausgabe:**
- `discussions/<slug>.json` – ein Objekt pro Post
- `discussions/<slug>.md` – YAML-Frontmatter + Markdown-Vorschau
- `discussions/_all.json` – alle Discussions als Array

**Threading-Regeln:**
- `comment_parent = 0` → top-level
- `comment_parent != 0` → Reply (max. 1 Ebene, GitHub-Discussions-Limit)
- Tiefe ≥ 2 → als Reply des Wurzel-Kommentars, mit zitiertem Kontext vorangestellt

**Frontmatter-Format der `.md`-Dateien:**

```yaml
---
title: "Kommentare: <Post-Titel>"
category: General
wp_url: https://the78mole.de/<slug>/
blog_url: /blog/<year>/<slug>
content_file: content/blog/<year>/<slug>.md
total_comments: 4
discussion_id: D_kwDOSNCPls4Al_Ro       # nach Erstellung durch create_discussions.py
discussion_number: 13                    # nach Erstellung durch create_discussions.py
---
```

---

### `scripts/create_discussions.py`

**Zweck:** Liest `discussions/_all.json`, erstellt GitHub Discussions via GraphQL,
fügt Kommentare und Replies ein, schreibt `discussion_id` + `discussion_number`
ins Frontmatter der `.md`-Datei.

**Idempotenz:** `.md`-Dateien mit vorhandenem `discussion_id:`-Feld werden übersprungen.
Vorhandene Discussions werden per Titel gesucht und nur das Frontmatter aktualisiert
(keine doppelten Kommentare).

**Flags:**

```bash
--test      Nur den ersten noch-nicht-vorhandenen Eintrag verarbeiten
--dry-run   Keine API-Aufrufe, Ausgabe was passieren würde
```

**GitHub GraphQL Mutationen:**

```graphql
createDiscussion(input: { repositoryId, categoryId, title, body })
addDiscussionComment(input: { discussionId, body, replyToId? })
```

**Rate-Limit:** Exponentieller Backoff bei `"was submitted too quickly"` (bis zu 5 Versuche).
Delay zwischen Calls: `1.5 s`.

**Wichtige Konstanten:**

```python
REPO_OWNER  = "the78mole-blog"
REPO_NAME   = "the78mole-blog.github.io"
REPO_ID     = "R_kgDOSNCPlg"
CATEGORY_ID = "DIC_kwDOSNCPls4C7zVP"  # "Blog Comments" – gleiche Kategorie wie giscus
```

---

## Giscus-Integration

giscus nutzt `mapping="pathname"` – der Discussion-**Title** muss dem URL-Pfad entsprechen:

```
Blog-URL: /blog/2020/freertos-debugging-on-stm32-cpu-usage
→ Discussion-Title: blog/2020/freertos-debugging-on-stm32-cpu-usage/
```

Die Kategorie **"Blog Comments"** (`DIC_kwDOSNCPls4C7zVP`) ist dieselbe, die in
`nuxt.config.ts` und `GiscusComments.vue` konfiguriert ist.

---

## Ergebnis-Übersicht

Nach der Migration:

| Discussion | Nummer | Kommentare |
|---|---|---|
| blog/2020/freertos-debugging-on-stm32-cpu-usage/ | #13 | 2 |
| blog/2021/get-the-hell-out-of-my-wall-box-…/ | #14 | 1 |
| blog/2019/how-to-build-a-private-storage-cluster-with-ceph/ | #15 | 4 |
| blog/2019/integrating-wmbus-devices-into-iobroker/ | #16 | 4 |
| blog/2018/orangepi-2g-iot-android-sdk/ | #17 | 4 |
| pages/km271-wifi-howto/ | #18 | 12 |
| blog/2021/reverse-engineering-the-buderus-km217/ | #19 | 62 |
| blog/2020/stm32-uart-continuous-receive-with-interrupt/ | #20 | 1 |
| blog/2020/stm32cubemx-and-sdram/ | #21 | 2 |
| blog/2021/taking-your-m-bus-online-with-mqtt/ | #22 | 9 |

---

## Häufige Aufgaben

### Neues WP-Backup importieren

```bash
# 1. XML durch neue Datei ersetzen
cp molesblog.WordPress.YYYY-MM-DD.xml import/

# 2. Kommentare extrahieren
uv run --project scripts scripts/extract_comments.py import/molesblog.WordPress.YYYY-MM-DD.xml

# 3. Discussion-Struktur neu aufbauen
uv run --project scripts scripts/assign_comments.py

# 4. Neue Discussions erstellen (vorhandene werden übersprungen)
uv run --project scripts scripts/create_discussions.py
```

### Nur Frontmatter synchronisieren (ohne API-Calls)

```bash
uv run --project scripts scripts/create_discussions.py --dry-run
```

### Einzelnen Eintrag testen

```bash
uv run --project scripts scripts/create_discussions.py --test
```

### Discussion-Kategorie ändern

In `scripts/create_discussions.py` die Konstante `CATEGORY_ID` anpassen.
Verfügbare Kategorien via:

```bash
gh api graphql -f query='{repository(owner:"the78mole-blog",name:"the78mole-blog.github.io"){discussionCategories(first:20){nodes{id name}}}}'
```
