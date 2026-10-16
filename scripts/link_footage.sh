#!/usr/bin/env bash
# Link footage that already lives elsewhere into a reel, without copying or moving the originals.
# Creates one symlink per clip in projects/<reel>/raw/<role>/ and records the source in raw/SOURCES.md.
# Skips macOS "._*" metadata files and camera proxy folders (Proxy/, Proxies/). Safe to re-run: existing links are kept.
# Usage: scripts/link_footage.sh <reel-name> <source-dir> [a-roll|b-roll]   (default b-roll)
set -euo pipefail
cd "$(dirname "$0")/.."
NAME="${1:?Usage: scripts/link_footage.sh <reel-name> <source-dir> [a-roll|b-roll]}"
SRC="${2:?source dir required}"
ROLE="${3:-b-roll}"
DEST="projects/$NAME/raw/$ROLE"
[ -d "projects/$NAME" ] || { echo "No projects/$NAME (run scripts/new_reel.sh $NAME first)"; exit 1; }
[ -d "$SRC" ] || { echo "No such folder: $SRC"; exit 1; }
SRC="$(cd "$SRC" && pwd)"
mkdir -p "$DEST"

n=0; skipped=0
while IFS= read -r -d '' f; do
  base="$(basename "$f")"
  if [ -e "$DEST/$base" ] || [ -L "$DEST/$base" ]; then skipped=$((skipped+1)); continue; fi
  ln -s "$f" "$DEST/$base"; n=$((n+1))
done < <(find "$SRC" \( -type d \( -iname proxy -o -iname proxies \) -prune \) -o -type f ! -name '._*' \( -iname '*.mov' -o -iname '*.mp4' -o -iname '*.m4v' -o -iname '*.mxf' -o -iname '*.mkv' \) -print0 | sort -z)

printf -- '- %s → `raw/%s/` (%s clips linked on %s)\n' "$SRC" "$ROLE" "$n" "$(date +%F)" >> "projects/$NAME/raw/SOURCES.md"
echo "✓ linked $n clips into $DEST ($skipped already there). Originals untouched: $SRC"
