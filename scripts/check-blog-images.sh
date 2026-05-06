#!/usr/bin/env bash
# check-blog-images.sh
# Called by pre-commit with staged markdown files as arguments.
# Checks that every image referenced in frontmatter (image:) or
# inline Markdown syntax (![...](/images/...)) exists in public/.

REPO_ROOT="$(git rev-parse --show-toplevel)"
PUBLIC="$REPO_ROOT/public"

MISSING=()

for FILE in "$@"; do
  ABS="$REPO_ROOT/$FILE"
  [[ ! -f "$ABS" ]] && continue

  # Frontmatter: image: /images/...
  while IFS= read -r IMG; do
    IMG="${IMG#"${IMG%%[![:space:]]*}"}"
    IMG="${IMG%"${IMG##*[![:space:]]}"}"
    IMG="${IMG#\'}" ; IMG="${IMG%\'}"
    IMG="${IMG#\"}" ; IMG="${IMG%\"}"
    [[ -z "$IMG" ]] && continue
    [[ ! -f "$PUBLIC$IMG" ]] && MISSING+=("$FILE  →  $IMG")
  done < <(grep -E '^image:' "$ABS" | sed 's/^image:[[:space:]]*//')

  # Inline Markdown: ![...]( /images/... )  – skip URLs with query strings
  while IFS= read -r IMG; do
    [[ "$IMG" == *'?'* ]] && continue
    [[ ! -f "$PUBLIC$IMG" ]] && MISSING+=("$FILE  →  $IMG")
  done < <(grep -oE '!\[[^]]*\]\(/images/[^)]+\)' "$ABS" | grep -oE '/images/[^)]+')
done

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo ""
  echo "Missing images – add them to public/ or fix the paths:"
  echo ""
  for ENTRY in "${MISSING[@]}"; do
    echo "  MISSING  $ENTRY"
  done
  echo ""
  exit 1
fi

exit 0
