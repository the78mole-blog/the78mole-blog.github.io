#!/usr/bin/env bash
# optimize-images.sh – Reduce blog image file sizes in-place using ImageMagick.
#
# Strategy:
#   JPEG  – resize to ≤ MAX_WIDTH, re-encode at JPEG_QUALITY, strip EXIF
#   PNG   – lossless: strip metadata, max zlib compression (no quality loss)
#
# Requires: ImageMagick (convert)
#
# Usage:
#   bash scripts/optimize-images.sh            # optimise all images
#   bash scripts/optimize-images.sh --dry-run  # report only, no changes

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_DIR="$(dirname "$SCRIPT_DIR")/public/images/blog"

MAX_WIDTH=1400     # px – resize JPEG only if wider than this
JPEG_QUALITY=82    # 0-100, good balance between quality and size
MIN_SIZE_KB=100    # skip images already smaller than this

DRY_RUN=0
for arg in "$@"; do
  [[ "$arg" == "--dry-run" ]] && DRY_RUN=1
done

total_before=0
total_after=0
count_shrunk=0
count_skipped=0

# ── convert helpers (write to stdout for size probing or to file) ─────────────

convert_jpeg() { # args: input output_or_-
  convert "$1" -resize "${MAX_WIDTH}x>" -quality "${JPEG_QUALITY}" -strip "jpg:$2"
}

convert_png() {  # args: input output_or_-
  convert "$1" \
    -resize "${MAX_WIDTH}x>" \
    -strip \
    -define png:compression-level=9 \
    -define png:compression-strategy=1 \
    "png:$2"
}

# ── main loop ─────────────────────────────────────────────────────────────────

echo ""
echo "  Blog Image Optimiser"
echo "  ────────────────────"
echo "  Directory:    $IMAGE_DIR"
echo "  Max width:    ${MAX_WIDTH}px  (JPEG only)"
echo "  JPEG quality: ${JPEG_QUALITY}"  echo "  Min size:     ${MIN_SIZE_KB} KB  (smaller files are skipped)"echo "  Dry-run:      $( [[ $DRY_RUN -eq 1 ]] && echo yes || echo no )"
echo ""

while IFS= read -r -d '' file; do
  ext="${file##*.}"
  ext_lower="${ext,,}"
  size_before=$(stat -c%s "$file")
  total_before=$(( total_before + size_before ))
  rel="$(realpath --relative-to="$IMAGE_DIR" "$file")"

  case "$ext_lower" in
    jpg|jpeg) convert_fn=convert_jpeg ;;
    png)      convert_fn=convert_png  ;;
    *)
      total_after=$(( total_after + size_before ))
      count_skipped=$(( count_skipped + 1 ))
      continue
      ;;
  esac

  if (( size_before < MIN_SIZE_KB * 1024 )); then
    total_after=$(( total_after + size_before ))
    count_skipped=$(( count_skipped + 1 ))
    printf "     %6d KB -> %6d KB  (%3d%%)  T  %s\n" \
      "$(( size_before / 1024 ))" "$(( size_before / 1024 ))" 0 "$rel"
    continue
  fi

  if [[ $DRY_RUN -eq 1 ]]; then
    size_after=$( $convert_fn "$file" - 2>/dev/null | wc -c )
    if (( size_after < size_before )); then
      total_after=$(( total_after + size_after ))
      count_shrunk=$(( count_shrunk + 1 ))
      printf "     %6d KB -> %6d KB  (%3d%%)  C  %s\n" \
        "$(( size_before / 1024 ))" "$(( size_after / 1024 ))" \
        "$(( (size_before - size_after) * 100 / size_before ))" "$rel"
    else
      total_after=$(( total_after + size_before ))
      count_skipped=$(( count_skipped + 1 ))
      printf "     %6d KB -> %6d KB  (%3d%%)  O  %s\n" \
        "$(( size_before / 1024 ))" "$(( size_before / 1024 ))" 0 "$rel"
    fi
    continue
  fi

  tmp="${file}.optimg_tmp"
  $convert_fn "$file" "$tmp"
  size_after=$(stat -c%s "$tmp")

  if [[ $size_after -lt $size_before ]]; then
    mv "$tmp" "$file"
    total_after=$(( total_after + size_after ))
    count_shrunk=$(( count_shrunk + 1 ))
    printf "     %6d KB -> %6d KB  (%3d%%)  C  %s\n" \
      "$(( size_before / 1024 ))" "$(( size_after / 1024 ))" \
      "$(( (size_before - size_after) * 100 / size_before ))" "$rel"
  else
    rm -f "$tmp"
    total_after=$(( total_after + size_before ))
    count_skipped=$(( count_skipped + 1 ))
    printf "     %6d KB -> %6d KB  (%3d%%)  O  %s\n" \
      "$(( size_before / 1024 ))" "$(( size_before / 1024 ))" 0 "$rel"
  fi

done < <(find "$IMAGE_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) -print0 | sort -z)

# ── summary ───────────────────────────────────────────────────────────────────

saved_total=$(( total_before - total_after ))
echo ""
echo "  ────────────────────"
if [[ $DRY_RUN -eq 1 ]]; then
  printf "  Would shrink: %d files\n" "$count_shrunk"
  printf "  Would skip:   %d files  (already optimal or below %d KB)\n" "$count_skipped" "$MIN_SIZE_KB"
  printf "  Before:       %d KB\n" "$(( total_before / 1024 ))"
  printf "  After:        %d KB\n" "$(( total_after  / 1024 ))"
  printf "  Would save:   %d KB\n" "$(( saved_total  / 1024 ))"
else
  printf "  Shrunk:   %d files\n" "$count_shrunk"
  printf "  Skipped:  %d files\n" "$count_skipped"
  printf "  Before:   %d KB\n" "$(( total_before / 1024 ))"
  printf "  After:    %d KB\n" "$(( total_after  / 1024 ))"
  printf "  Saved:    %d KB\n" "$(( saved_total  / 1024 ))"
fi
echo ""
