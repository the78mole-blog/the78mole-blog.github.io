# ── Nuxt / GitHub Pages Blog – Makefile ──────────────────────────────────────
# Common development tasks for a Nuxt 4 / GitHub Pages static blog.
#
# Prerequisites:
#   - Node.js + npm   (for Nuxt tasks)
#   - uv              (for Python scripts, https://docs.astral.sh/uv/)
#
# Usage:
#   make              → shows this help
#   make dev          → starts Nuxt dev server
#   make check-links  → full external + internal link check with interactive review
# ─────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
.PHONY: help dev build generate preview install \
        check-links check-links-fast check-links-ci \
        check-links-reset restore-assets restore-assets-do

# ── Variables ─────────────────────────────────────────────────────────────────

LOG      ?= /tmp/links.log
WORKERS  ?= 10
TIMEOUT  ?= 15

# ── Help ──────────────────────────────────────────────────────────────────────

help:
	@echo ""
	@echo "  Blog – available targets"
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
	@echo "    make restore-assets     Dry-run: show missing WP assets to restore"
	@echo "    make restore-assets-do  Actually copy missing WP assets to public/"
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
