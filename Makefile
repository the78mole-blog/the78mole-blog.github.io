# ── the78mole-blog Makefile ───────────────────────────────────────────────────
# Common development tasks for the Nuxt 4 / GitHub Pages blog.
#
# Prerequisites:
#   - Node.js + npm   (for Nuxt tasks)
#   - uv              (for Python scripts)
#
# Usage:
#   make              → shows this help
#   make dev          → starts Nuxt dev server
#   make check-links  → full external + internal link check with interactive review
# ─────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
.PHONY: help dev build generate preview install \
        generate-taxonomy \
        check-links check-links-fast check-links-ci \
        check-links-reset restore-assets \
        optimize-images optimize-images-dry

# ── Variables ─────────────────────────────────────────────────────────────────

LOG      ?= /tmp/links.log
WORKERS  ?= 10
TIMEOUT  ?= 15
MIN_SIZE_KB ?= 500

# ── Help ──────────────────────────────────────────────────────────────────────

help:
	@echo ""
	@echo "  the78mole-blog – available targets"
	@echo ""
	@echo "  Nuxt"
	@echo "    make install            Install npm dependencies"
	@echo "    make dev                Start Nuxt dev server  (http://localhost:3000)"
	@echo "    make build              Build for SSR"
	@echo "    make generate           Static site generation (GitHub Pages)"
	@echo "    make preview            Preview generated site"
	@echo ""
	@echo "  Link checking"
	@echo "    make check-links        Full check: external + internal (interactive)"
	@echo "    make check-links-fast   Internal links only, no HTTP requests"
	@echo "    make check-links-ci     Non-interactive check (for CI pipelines)"
	@echo "    make check-links-log    Full check + write log to \$$LOG (default: $(LOG))"
	@echo "    make check-links-reset  Clear the link cache (.link_cache.json)"
	@echo ""
	@echo "  Assets"
	@echo "    make restore-assets       Dry-run: show missing WP assets to restore"
	@echo "    make restore-assets-do    Actually copy missing WP assets to public/"
	@echo "    make optimize-images      Compress blog images in-place (JPEG+PNG)"
	@echo "    make optimize-images-dry  Report image sizes without changing files"
	@echo "    (override: MIN_SIZE_KB=50 to lower the skip threshold, default: $(MIN_SIZE_KB) KB)"
	@echo ""

# ── Nuxt ──────────────────────────────────────────────────────────────────────

install:
	npm install

dev:
	npm run dev

build:
	npm run build

generate:
	npm run generate

preview:
	npm run preview

generate-taxonomy:
	uv run --script scripts/generate-taxonomy.py

# ── Link checking ─────────────────────────────────────────────────────────────

check-links:
	uv run --script scripts/check-links.py \
		--workers $(WORKERS) --timeout $(TIMEOUT)

check-links-fast:
	uv run --script scripts/check-links.py --no-external

check-links-ci:
	uv run --script scripts/check-links.py \
		--workers $(WORKERS) --timeout $(TIMEOUT) \
		--non-interactive

check-links-log:
	uv run --script scripts/check-links.py \
		--workers $(WORKERS) --timeout $(TIMEOUT) \
		--log $(LOG)
	@echo ""
	@echo "  Log written to $(LOG)"

check-links-reset:
	@rm -f .link_cache.json
	@echo "  Link cache cleared."

# ── Assets ────────────────────────────────────────────────────────────────────

restore-assets:
	uv run --script scripts/restore-missing-assets.py --dry-run \
		--log $(LOG)

restore-assets-do:
	uv run --script scripts/restore-missing-assets.py \
		--log $(LOG)

optimize-images:
	MIN_SIZE_KB=$(MIN_SIZE_KB) bash scripts/optimize-images.sh

optimize-images-dry:
	MIN_SIZE_KB=$(MIN_SIZE_KB) bash scripts/optimize-images.sh --dry-run
