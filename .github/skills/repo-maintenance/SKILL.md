---
name: repo-maintenance
description: >
  Repo-spezifisches Wissen für the78mole-blog.github.io. Verwende diesen Skill für:
  Neue Blog-Posts oder Seiten erstellen; Abhängigkeiten aktualisieren; CI/CD-Workflow
  (publish.yml) verstehen; Umgebungsvariablen und GitHub-Secrets verwalten;
  Routing (routeRules / WordPress-Redirects) erweitern; content.config.ts Schema
  anpassen; AdSense-Slots konfigurieren; Renovate-PRs beurteilen.
---

# the78mole-blog.github.io – Repo-Wissen

## Projekt-Überblick

- **URL**: https://the78mole-blog.github.io
- **Framework**: Nuxt 4, SSG (`nuxt generate`), deployed auf GitHub Pages
- **Content**: Markdown-Dateien in `content/blog/` und `content/pages/`
- **Branch-Strategie**: direkt auf `main` → triggert CI/CD automatisch

## Verzeichnisstruktur

```
content/
  blog/          # Blog-Posts als *.md (Frontmatter: title, date, description, image, categories)
  pages/         # Statische Seiten als *.md (Frontmatter: title, description)
pages/
  index.vue      # Blog-Index (queryCollection('blog'))
  blog/
    [...slug].vue  # Blog-Post-Detail
  pages/
    [slug].vue     # Statische Seiten
    contact.vue    # Kontaktformular (StaticForms, API-Key via CI-Secret)
components/
  AdBlock.vue        # Google AdSense – isMounted-Guard gegen SSR-Mismatch
  ConsentBanner.vue  # DSGVO-Banner – Cookie + useState('consent')
  GiscusComments.vue # Kommentarfunktion via GitHub Discussions (giscus) – immer in <ClientOnly>
layouts/
  default.vue    # Header, Footer, ConsentBanner-Slot
app.vue          # <ClientOnly><ConsentBanner /></ClientOnly>
content.config.ts # @nuxt/content v3 Collections + Zod-Schemas
nuxt.config.ts   # Module, runtimeConfig, routeRules (WP-Redirects), highlight langs
renovate.json    # Renovate-Bot-Konfiguration
```

## Umgebungsvariablen

| Variable | Wo | Beschreibung |
|---|---|---|
| `GOOGLE_ANALYTICS_MEAS_ID` | GitHub Vars (`vars.*`) | GA4 Measurement-ID (z.B. `G-XXXXXXXXXX`) |
| `GOOGLE_ADSENSE_PUB_ID` | GitHub Vars (`vars.*`) | Ohne `ca-`-Präfix (z.B. `pub-12345`) |
| `STATIC_FORMS_KEY` | GitHub Secrets (`secrets.*`) | StaticForms API-Key für Kontaktformular |
| `GISCUS_REPO_ID` | GitHub Vars (`vars.*`) | `R_kgDOSNCPlg` – Repo-ID für giscus |
| `GISCUS_CATEGORY_ID` | GitHub Vars (`vars.*`) | `DIC_kwDOSNCPls4C7zVP` – Kategorie „Blog Comments" |

**Lokal**: `.env`-Datei (bereits in `.gitignore`). Schema:
```
GOOGLE_ANALYTICS_MEAS_ID=G-XXXXXXXXXX
GOOGLE_ADSENSE_PUB_ID=pub-XXXXXXXXXXXXXXXX
GISCUS_REPO_ID=R_kgDOSNCPlg
GISCUS_CATEGORY_ID=DIC_kwDOSNCPls4C7zVP
```

**Achtung**: Der CI-Schritt ersetzt `YOUR_STATICFORMS_API_KEY` per `sed` in `contact.vue` direkt vor dem Build – die Datei im Repo enthält bewusst den Platzhalter.

## CI/CD – `.github/workflows/publish.yml`

- **Trigger**: Push auf `main`, PRs auf `main`, manuell (`workflow_dispatch`)
- **Node**: 24 (via `actions/setup-node@v6`)
- **Env**: `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true`
- **Build-Output**: `.output/public/`
- **Deploy**: nur bei Push auf `main` (nicht bei PRs)
- **PR-Previews**: Upload als Artifact `pr-preview-<nr>`, 7 Tage Retention

```
build job → upload-pages-artifact (main) oder upload-artifact (PR)
deploy job → actions/deploy-pages@v5  (nur main + push)
```

**GitHub Actions Versionen aktuell**:
- `actions/checkout@v6`
- `actions/setup-node@v6`
- `actions/upload-pages-artifact@v5`
- `actions/upload-artifact@v7`
- `actions/deploy-pages@v5`

## AdSense-Slot-IDs (`nuxt.config.ts` → `runtimeConfig.public.adsenseSlots`)

| Key | Slot-ID | Platzierung |
|---|---|---|
| `left` | `3478648998` | Sidebar links (Desktop) |
| `right` | `9230728617` | Sidebar rechts (Desktop) |
| `bottom` | `8012270852` | Unterhalb Artikel (Mobile) |
| `inArticle` | `5913240643` | In-Article (fluid) |

Slot-IDs sind öffentlich und eingecheckt (kein Secret).

## Content erstellen

### Neuer Blog-Post

Datei anlegen: `content/blog/<slug>.md`

```markdown
---
title: "Titel des Posts"
date: "2026-04-27"
description: "Kurzbeschreibung für SEO und Index-Karte"
image: "/uploads/bild.jpg"
categories:
  - Embedded
  - Smart Home
---

# Inhalt hier
```

Felder die im Zod-Schema (`content.config.ts`) definiert sind: `date`, `description`, `image`, `categories`.
**Neue Felder** → Schema in `content.config.ts` ergänzen sonst `no such column`-Fehler.

### Neue statische Seite

Datei anlegen: `content/pages/<slug>.md`

```markdown
---
title: "Seitentitel"
description: "Kurzbeschreibung"
---

# Inhalt
```

Route ist automatisch erreichbar unter `/pages/<slug>`.

## WordPress-Redirects (`nuxt.config.ts → routeRules`)

GitHub Pages hat keinen Server → Nuxt generiert statische Meta-Refresh-Seiten.

```ts
routeRules: {
  '/alter-wp-slug': { redirect: '/pages/neue-route' },
  '/alter-wp-slug/': { redirect: '/pages/neue-route' },
}
```

Immer **mit und ohne trailing slash** eintragen.

## Tailwind & CSS

- `tailwind.config.js` vorhanden – dort Typography-Plugin und Content-Pfade
- `viewer: false` in `nuxt.config.ts` verhindert HMR-Loop
- **Kritisch**: `tailwindcss` muss auf `^3.4.x` bleiben (Renovate sperrt v4+)

## Renovate-Bot-Regeln

Aktuelle Schutzregeln in `renovate.json`:
- Minor/Patch-Updates werden gruppiert → ein PR für alle
- `tailwindcss` → max `^3.0.0` (v4 blockiert)
- `@nuxtjs/tailwindcss` Major-Update → Label `needs-review` → manuell prüfen ob v4-Support bereit

**Wann tailwindcss v4 entsperren**: wenn `@nuxtjs/tailwindcss` tailwindcss als `peerDependency` (nicht `dependency`) listet:
```bash
cat node_modules/@nuxtjs/tailwindcss/package.json | python3 -c \
  "import json,sys; p=json.load(sys.stdin); \
   print('dep:', p.get('dependencies',{}).get('tailwindcss','none')); \
   print('peer:', p.get('peerDependencies',{}).get('tailwindcss','none'))"
```

## Giscus – Kommentarfunktion

- **Paket**: `@giscus/vue` (reguläre Dependency)
- **Komponente**: `components/GiscusComments.vue` – `import Giscus from '@giscus/vue'` (nur default-Export!) + `<ClientOnly>`
- **Eingebaut in**: `pages/blog/[...slug].vue` und `pages/pages/[slug].vue`
- **Mapping**: `pathname` → jede URL bekommt eine eigene Diskussion
- **Kategorie**: „Blog Comments" (Typ Announcements – nur giscus/Maintainer öffnen neue Threads)
- **Theme**: `transparent_dark`
- **IDs nachschlagen**:
  ```bash
  gh api graphql -f query='{ repository(owner:"the78mole-blog", name:"the78mole-blog.github.io") { id discussionCategories(first:20) { nodes { id name } } } }'
  ```
- **Aktuelle IDs** (als Fallback in `nuxt.config.ts` hinterlegt, Env-Vars überschreiben):
  - Repo-ID: `R_kgDOSNCPlg`
  - Kategorie-ID: `DIC_kwDOSNCPls4C7zVP`
- **Voraussetzung**: [giscus App](https://github.com/apps/giscus) muss auf dem Repo installiert sein

## Häufige Fehler

| Fehler | Ursache | Fix |
|---|---|---|
| `no such column: "date"` | Frontmatter-Feld fehlt im Zod-Schema | Feld in `content.config.ts` ergänzen |
| `queryContent is not defined` | @nuxt/content v2 API-Call | Auf `queryCollection()` migrieren |
| `Hydration mismatch` | Cookie-abhängige Komponente SSR-seitig gerendert | In `<ClientOnly>` wrappen |
| CI hängt bei `better-sqlite3` | Paket fehlt in devDeps | `better-sqlite3` in `package.json` devDeps |
| Build bricht nach Renovate-PR | tailwindcss v4 installiert | `tailwindcss` in `package.json` auf `^3.4.17` zurücksetzen |

## Lokale Entwicklung

```bash
npm run dev       # Dev-Server (HMR)
npm run generate  # Statischen Build erzeugen → .output/public/
npx serve .output/public  # Lokale Vorschau des Builds
```

## Checklist vor jedem Commit

- [ ] `npm run generate` lokal durchläuft ohne Fehler
- [ ] Alle neuen Frontmatter-Felder in `content.config.ts` Zod-Schema eingetragen
- [ ] Neue WordPress-Redirects mit und ohne trailing slash
- [ ] Keine Secrets in eingecheckten Dateien (`.env` ist in `.gitignore`)
- [ ] Kontaktformular-Placeholder `YOUR_STATICFORMS_API_KEY` in `contact.vue` nicht überschrieben
- [ ] Nach Änderungen an `GiscusComments.vue`: nur `default`-Import von `@giscus/vue` (kein `{ GiscusComponent }`)
