# the78mole-blog.github.io

Personal website and blog of **the78mole** – built with [Nuxt 3](https://nuxt.com) and [Nuxt Content](https://content.nuxt.com), migrated from WordPress.

---

## Repository-Struktur

```
.
├── content/
│   └── blog/
│       └── YYYY/          # Markdown-Blogposts je Jahrgang
├── public/
│   └── images/
│       └── blog/
│           └── YYYY/MM/   # Migrierte Bilder aus WordPress
├── scripts/
│   ├── migration.py       # WordPress-WXR → Nuxt-Content-Migrationsskript
│   └── pyproject.toml     # Python-Projektmetadaten (uv)
├── import/                # (gitignored) WordPress-Export-Daten
│   ├── *.xml              # WXR-Export-Datei
│   └── wp-content/uploads/
├── MIGRATION.md           # Migrations-Konzept und Copilot-Anweisungen
└── README.md
```

---

## WordPress-Migration

Der Inhalt dieses Blogs wurde aus einem WordPress-Export (WXR) migriert.
Das Migrationsskript liegt unter `scripts/migration.py` und erledigt folgende Aufgaben:

- Parst die WXR-XML-Datei und extrahiert alle veröffentlichten Beiträge
- Konvertiert HTML-Inhalte in sauberes Markdown
- Erzeugt YAML-Frontmatter (title, date, description, categories, tags, image)
- Kopiert Mediadateien von `import/wp-content/uploads/` nach `public/images/blog/`
- Passt alle Bildpfade im Markdown automatisch an

### Migration ausführen

Voraussetzung: [uv](https://docs.astral.sh/uv/) installiert (`pip install uv` oder `curl -Ls https://astral.sh/uv/install.sh | sh`)

```bash
# WordPress-Export-Datei nach import/ legen, dann:
uv run scripts/migration.py
```

Das Skript verwendet PEP 723 Inline-Metadaten – alle Python-Abhängigkeiten werden von `uv` automatisch installiert, kein separater `pip install` nötig.

---

## Nuxt Content – Kurzreferenz

### Entwicklungsserver starten

```bash
npm install
npm run dev
```

Der Dev-Server läuft standardmäßig auf [http://localhost:3000](http://localhost:3000) mit Hot Reload.

### Produktion bauen

```bash
npm run build      # SSR-Build (Node.js-Server)
npm run generate   # Statische HTML-Generierung (für GitHub Pages)
```

### Neuen Blogpost anlegen

Einfach eine Markdown-Datei in `content/blog/YYYY/` erstellen:

```markdown
---
title: Mein neuer Post
date: '2026-04-26'
description: Kurze Beschreibung für SEO und Preview-Karten
categories:
  - Hardware
tags:
  - STM32
  - Embedded
image: /images/blog/2026/04/titelbild.png
---

## Inhalt hier

Normales Markdown...
```

Nuxt Content erkennt die Datei automatisch – kein Build-Schritt nötig im Dev-Modus.

### Frontmatter-Felder

| Feld          | Typ      | Beschreibung                                      |
|---------------|----------|---------------------------------------------------|
| `title`       | string   | Titel des Posts (H1 und `<title>`-Tag)            |
| `date`        | string   | Veröffentlichungsdatum (ISO 8601: `YYYY-MM-DD`)   |
| `description` | string   | Kurzbeschreibung (Meta-Description, Previews)     |
| `categories`  | string[] | Kategorien (werden als Tags gerendert)            |
| `tags`        | string[] | Zusätzliche Schlagwörter                          |
| `image`       | string   | Pfad zum Titelbild unter `public/`                |

### Nützliche Links

- [Nuxt 3 Docs](https://nuxt.com/docs)
- [Nuxt Content Docs](https://content.nuxt.com)
- [Nuxt Content – Querying](https://content.nuxt.com/usage/content-helpers)
- [MDC (Markdown Components) Syntax](https://content.nuxt.com/usage/markdown)

---

## Lizenz

Siehe [LICENSE](LICENSE).
