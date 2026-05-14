# the78mole-blog.github.io

Personal website and blog of **the78mole** – written from the perspective of a nerdy, tech-obsessed mole.

Built with [Nuxt 4](https://nuxt.com) and [@nuxt/content](https://content.nuxt.com) v3, deployed as a static site on GitHub Pages, migrated from WordPress.

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Framework | Nuxt 4, SSG via `nuxi generate` |
| Content | `@nuxt/content` v3 – Markdown in `content/blog/` and `content/pages/` |
| Styling | Tailwind CSS v4 + `@tailwindcss/typography` |
| Comments | Giscus (GitHub Discussions) |
| Analytics | Google Analytics 4 with Consent Mode v2 |
| Hosting | GitHub Pages – auto-deploy on push to `main` |

---

## Repository Structure

```text
.
├── .github/
│   ├── copilot-instructions.md   # Copilot persona & blog conventions
│   ├── skills/                   # Copilot skill definitions
│   └── workflows/
│       └── publish.yml           # Build & deploy to GitHub Pages
├── components/                   # Vue SFCs (AdBlock, ConsentBanner, GiscusComments)
├── content/
│   ├── blog/
│   │   └── YYYY/                 # Markdown blog posts per year
│   └── pages/                    # Static pages (about, contact, …)
├── discussions/                  # Giscus discussion data (imported WP comments)
├── layouts/                      # Default layout (header, footer)
├── pages/                        # Vue route pages
├── public/
│   └── images/blog/YYYY/MM/      # Post images
├── scripts/
│   ├── migration.py              # WordPress WXR → Markdown migration
│   ├── extract_comments.py       # Extract WP comments from WXR
│   ├── assign_comments.py        # Assign comments to post slugs
│   ├── create_discussions.py     # Create GitHub Discussions via GraphQL
│   ├── check-links.py            # Dead-link checker with cache
│   ├── restore-missing-assets.py # Restore missing WP media to public/
│   ├── check-blog-images.sh      # Verify image frontmatter references
│   └── pyproject.toml            # Python project metadata (uv)
├── content.config.ts             # @nuxt/content v3 collection schemas
├── nuxt.config.ts                # Nuxt configuration (modules, highlight, routeRules)
└── tailwind.config.js            # Tailwind + typography plugin
```

---

## Day-to-Day Workflow

```bash
make dev                # Start dev server at http://localhost:3000
make check-links-fast   # Verify internal links before pushing
git add -A && git commit -m "new post: …"
git push                # Triggers publish.yml → live in ~90 seconds
```

### All available targets

```
make install            Install npm dependencies
make dev                Start Nuxt dev server  (http://localhost:3000)
make build              Build for SSR
make generate           Static site generation (GitHub Pages)
make preview            Preview generated site

make check-links        Full check: external + internal (interactive)
make check-links-fast   Internal links only, no HTTP requests
make check-links-ci     Non-interactive check (for CI pipelines)
make check-links-log    Full check + write log to $LOG
make check-links-reset  Clear the link cache (.link_cache.json)

make restore-assets     Dry-run: show missing WP assets to restore
make restore-assets-do  Actually copy missing WP assets to public/
```

---

## Writing a New Post

Create a Markdown file in `content/blog/YYYY/`:

```markdown
---
title: "My Post Title"
date: '2026-05-14'
description: 'One sentence that sells the post.'
image: /images/blog/2026/05/cover.png
categories:
  - Dev
tags:
  - keyword
---

Post content here.
```

| Field | Type | Required |
| --- | --- | --- |
| `title` | string | yes |
| `date` | `'YYYY-MM-DD'` | yes |
| `description` | string | yes |
| `image` | string (path under `public/`) | no |
| `categories` | string[] | no |
| `tags` | string[] | no |

Syntax highlighting is enabled for: `bash` · `c` · `cpp` · `css` · `dockerfile` · `go` · `html` · `java` · `javascript` · `json` · `makefile` · `markdown` · `python` · `rust` · `shell` · `sql` · `toml` · `typescript` · `vim` · `xml` · `yaml`

---

## WordPress Migration

All posts were migrated from a WordPress WXR export. The scripts in `scripts/` handle the full pipeline:

```bash
# Requires uv (https://docs.astral.sh/uv/)
uv run --project scripts scripts/migration.py          # WXR → Markdown
uv run --project scripts scripts/extract_comments.py   # Extract WP comments
uv run --project scripts scripts/assign_comments.py    # Assign to post slugs
uv run --project scripts scripts/create_discussions.py # Create GitHub Discussions
```

Scripts use [PEP 723](https://peps.python.org/pep-0723/) inline metadata – `uv` installs all dependencies automatically.

---

## Environment Variables

| Variable | Where | Description |
| --- | --- | --- |
| `GOOGLE_ANALYTICS_MEAS_ID` | GitHub Vars | GA4 Measurement ID |
| `GOOGLE_ADSENSE_PUB_ID` | GitHub Vars | AdSense publisher ID (without `ca-` prefix) |
| `GISCUS_REPO_ID` | GitHub Vars | Giscus repository ID |
| `GISCUS_CATEGORY_ID` | GitHub Vars | Giscus discussion category ID |
| `STATIC_FORMS_KEY` | GitHub Secrets | StaticForms API key for contact form |

For local development, copy to `.env` (already in `.gitignore`).

---

## CI/CD

Push to `main` triggers `.github/workflows/publish.yml`:

1. `npm ci` + `npm run generate` → `.output/public/`
2. Upload as GitHub Pages artifact
3. Deploy via `actions/deploy-pages`

The workflow skips builds for pushes that only touch non-site files (Copilot skills, `discussions/`, `scripts/`, `README.md`, `renovate.json`).

Pull requests upload a preview artifact (`pr-preview-<nr>`, 7-day retention).

---

## License

See [LICENSE](LICENSE).
