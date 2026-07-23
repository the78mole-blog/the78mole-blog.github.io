#!/usr/bin/env bash
# check-blog-images.sh
# Called by pre-commit with staged markdown files as arguments.
# Checks that every image referenced in frontmatter (image:) or
# inline Markdown syntax (![...](/images/...)) exists in public/.
# Lines inside fenced code blocks (``` ... ```) are skipped.
# Output includes the source line number.
#
# Generalisation notes:
#   - IMAGE_PREFIX: change if your static images live under a different path
#                   (e.g. /uploads/ or /assets/). The grep pattern below must
#                   match the same prefix.
#   - The script expects to run inside a git repository. REPO_ROOT is resolved
#     via `git rev-parse --show-toplevel`.

REPO_ROOT="$(git rev-parse --show-toplevel)"
PUBLIC="$REPO_ROOT/public"

# Prefix that local image paths must start with to be checked.
# Adjust to match your project (e.g. /uploads/ or /assets/).
IMAGE_PREFIX="/images/"

MISSING=()

for FILE in "$@"; do
  ABS="$REPO_ROOT/$FILE"
  [[ ! -f "$ABS" ]] && continue

  in_fence=0
  lineno=0

  while IFS= read -r LINE; do
    (( lineno++ ))

    # Toggle code-fence state (lines starting with ```)
    if [[ "$LINE" =~ ^[[:space:]]*\`\`\` ]]; then
      (( in_fence = 1 - in_fence ))
      continue
    fi
    [[ $in_fence -eq 1 ]] && continue

    # Frontmatter: image: /images/...
    if [[ "$LINE" =~ ^image:[[:space:]]*(.*) ]]; then
      IMG="${BASH_REMATCH[1]}"
      IMG="${IMG#"${IMG%%[![:space:]]*}"}"
      IMG="${IMG%"${IMG##*[![:space:]]}"}"
      IMG="${IMG#\'}" ; IMG="${IMG%\'}"
      IMG="${IMG#\"}" ; IMG="${IMG%\"}"
      if [[ -n "$IMG" && ! -f "$PUBLIC$IMG" ]]; then
        MISSING+=("$FILE:$lineno  →  $IMG")
      fi
      continue
    fi

    # Inline Markdown: ![...]( /images/... ) – skip URLs with query strings
    while IFS= read -r IMG; do
      [[ -n "$IMG" && ! -f "$PUBLIC$IMG" ]] && MISSING+=("$FILE:$lineno  →  $IMG")
    done < <(echo "$LINE" | grep -oE "!\[[^]]*\]\(${IMAGE_PREFIX}[^) ?]+\)" | grep -oE "${IMAGE_PREFIX}[^)]+")

  done < "$ABS"
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
