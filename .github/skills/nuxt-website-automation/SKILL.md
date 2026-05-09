---
name: nuxt-website-automation
description: >
  Dev-Workflow und Skript-Dokumentation für das Nuxt/GitHub-Pages-Blog-Repo.
  Verwende diesen Skill für: Make-Targets erklären oder ergänzen; check-links.py
  debuggen oder erweitern; check-blog-images.sh anpassen; restore-missing-assets.py
  konfigurieren; neues Skript inkl. Make-Target und help-Zeile anlegen;
  Makefile-Struktur verstehen.
---

# Blog Dev-Workflow – Make-Targets & Skripte

Alle häufig genutzten Befehle sind im `Makefile` im Repo-Root zusammengefasst.
`make` (ohne Argument) zeigt die vollständige Hilfe. Die unterstützenden Python-
und Shell-Skripte liegen unter `scripts/`.

Referenz-Implementierungen der Skripte liegen unter
`.github/skills/nuxt-website-automation/assets/`.

---

## Make-Targets im Überblick

### Nuxt

| Target | Befehl | Zweck |
|---|---|---|
| `make install` | `npm install` | npm-Abhängigkeiten installieren |
| `make dev` | `npm run dev` | Nuxt-Dev-Server (http://localhost:3000) |
| `make build` | `npm run build` | SSR-Build |
| `make generate` | `npm run generate` | Statische Seite für GitHub Pages |
| `make preview` | `npm run preview` | Generierten Output lokal betrachten |

### Link-Checking

| Target | Beschreibung |
|---|---|
| `make check-links` | Vollständige Prüfung: extern + intern, interaktiv |
| `make check-links-fast` | Nur interne Links (kein HTTP), sehr schnell |
| `make check-links-ci` | Vollständig, nicht-interaktiv (für CI-Pipelines) |
| `make check-links-log LOG=/tmp/links.log` | Vollständig + Log-Datei |
| `make check-links-reset` | Link-Cache (`.link_cache.json`) löschen |

### Assets

| Target | Beschreibung |
|---|---|
| `make restore-assets` | Dry-Run: zeigt fehlende WP-Assets |
| `make restore-assets-do` | Kopiert fehlende WP-Assets nach `public/` |

### Makefile-Variablen

```makefile
LOG     ?= /tmp/links.log   # Pfad für Logdatei
WORKERS ?= 10               # Parallele HTTP-Worker für check-links
TIMEOUT ?= 15               # HTTP-Timeout in Sekunden
```

Überschreiben per CLI: `make check-links WORKERS=5 TIMEOUT=30`

---

## Skripte

### `scripts/check-links.py`

PEP-723-Inline-Skript (kein venv nötig, direkt mit `uv run --script`).

**Prüft drei Kategorien:**

1. **Externe Links** (`http`/`https`) – HTTP HEAD, Fallback auf GET, misst Latenz
2. **Interne Bildpfade** (`/images/…`) – Dateiexistenz in `public/`
3. **Interne Routen** (`/blog/…`, `/pages/…`) – Passendes `.md` in `content/`

**Cache (`.link_cache.json`):**

| Status | Bedeutung | TTL |
|---|---|---|
| `passed` | Erfolgreich geprüft | 28 Tage |
| `manual` | Manuell verifiziert | 365 Tage |
| `captcha` | Hinter CAPTCHA – manuell OK | 365 Tage |
| `failed` | Fehlgeschlagen | Jeder Run |

**Optionen:**

```
--no-external        Externe Checks überspringen
--workers N          Parallele HTTP-Worker (Standard: 10)
--timeout N          HTTP-Timeout in Sekunden (Standard: 10)
--ignore-file FILE   URL-Präfixe zum Ignorieren (eine je Zeile, # = Kommentar)
--log FILE           Alle URLs in Datei protokollieren
--no-check-cache     Cache-TTL ignorieren, alles neu prüfen
--non-interactive    Kein interaktiver Prompt am Ende
```

**Interaktiver Modus:** Am Ende wird für jeden Fehler gefragt:
`[s]kip / [m]anual / [c]aptcha / [i]gnore-prefix / [q]uit`

**Erweiterung:** Neue Linktypen in `check_internal()` eintragen, neue CLI-Flags
in `parse_args()`.

---

### `scripts/check-blog-images.sh`

Wird von **pre-commit** aufgerufen (Hook `check-blog-images`).
Überprüft, ob jedes in Markdown referenzierte Bild unter `public/` existiert.

**Prüft:**
- Frontmatter `image: /images/…`
- Inline-Markdown `![alt](/images/…)`

**Überspringt:** Zeilen innerhalb von ` ``` `-Code-Blöcken.

**Ausgabe:** `<datei>:<zeilennummer>  →  /images/pfad`

**pre-commit-Konfiguration (`.pre-commit-config.yaml`):**
```yaml
- id: check-blog-images
  name: Check blog post images exist in public/
  language: script
  entry: scripts/check-blog-images.sh
  types: [markdown]
  pass_filenames: true
```

**Anpassen:** Um andere Bildpfade (z.B. `/uploads/`) einzuschließen, das `grep`-Pattern
in den `while IFS= read` Schleifen erweitern.

---

### `scripts/restore-missing-assets.py`

Liest eine Log-Datei von `check-links.py` (mit `--log`) und sucht für jede
fehlende `[FAIL]`-URL nach der Original-Datei im lokalen WordPress-Import.

**Workflow:**
1. `make check-links-log LOG=/tmp/links.log`
2. `make restore-assets` (Dry-Run, zeigt was passieren würde)
3. `make restore-assets-do` (kopiert Dateien + rewrites Markdown-Quellen)

**Konfigurierbare Parameter (oben in der Datei):**
```python
# Hosts, deren fehlende Assets lokal gesucht werden sollen
SITE_HOSTS = {"yourdomain.de", "blog.yourdomain.de"}

# Suchreihenfolge für lokale WP-Dateien
SEARCH_ROOTS = [
    IMPORT_DIR / "wp-content",
    IMPORT_DIR / "WordPress_SecureMode_01" / "wp-content",
]
```

**CLI-Optionen:**
```
--log FILE    Pfad zur check-links Logdatei (Standard: /tmp/links.log)
--dry-run     Nur Ausgabe, keine Dateioperationen
```

---

## Neues Skript + Target hinzufügen

Checkliste:

1. Skript unter `scripts/` anlegen (Python: PEP 723 Inline-Metadata, Shell: `#!/usr/bin/env bash`)
2. Make-Target im `Makefile` eintragen
3. **`help`-Zeile im `help`-Target ergänzen** – sonst findet es der Maulwurf nach drei Wochen nicht mehr
4. Referenz-Kopie in `.github/skills/nuxt-website-automation/assets/` aktualisieren

```makefile
# Beispiel: neues Target
my-tool:
    uv run --script scripts/my-tool.py

# help-Block:
@echo "    make my-tool            Was es tut"
```

---

## Typische Workflows

### Vor einem Commit (schnell)

```bash
make check-links-fast    # Interne Links + fehlende Bilder prüfen
git add -A && git commit
```

### Vor einem Release (vollständig)

```bash
make check-links         # Externe + interne Links, interaktiver Cache-Update
make restore-assets      # Fehlende WP-Assets anzeigen (Dry-Run)
make restore-assets-do   # Ggf. Assets wirklich kopieren
git push                 # → publish.yml startet, ~90 s bis live
```

### CI-Pipeline

```bash
make check-links-ci      # Nicht-interaktiv, Exit-Code 1 bei Fehlern
```
