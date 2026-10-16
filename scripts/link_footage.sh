#!/usr/bin/env bash
# Link footage that already lives elsewhere into a reel, without copying or moving the originals.
# Creates one symlink per clip in projects/<reel>/raw/<role>/ (or projects/<reel>/references/) and records the source in raw/SOURCES.md.
# Skips macOS "._*" metadata files, camera proxy folders (Proxy/, Proxies/) and, for footage roles, reference folders. Safe to re-run: existing links are kept.
# Usage: scripts/link_footage.sh <reel-name> <source-dir> [a-roll|b-roll|references]   (default b-roll)
set -euo pipefail
cd "$(dirname "$0")/.."
NAME="${1:?Usage: scripts/link_footage.sh <reel-name> <source-dir> [a-roll|b-roll|references]}"
SRC="${2:?source dir required}"
ROLE="${3:-b-roll}"
case "$ROLE" in
  a-roll|b-roll) DEST="projects/$NAME/raw/$ROLE" ;;
  references)    DEST="projects/$NAME/references" ;;
  *) echo "Role must be a-roll, b-roll or references"; exit 1 ;;
esac
[ -d "projects/$NAME" ] || { echo "No projects/$NAME (run scripts/new_reel.sh $NAME first)"; exit 1; }
[ -d "$SRC" ] || { echo "No such folder: $SRC"; exit 1; }
SRC="$(cd "$SRC" && pwd)"
mkdir -p "$DEST"

# Footage roles skip reference folders (Reference, References, Refference, …) so reference reels never become footage.
if [ "$ROLE" = references ]; then REFPAT='__none__'; else REFPAT='*ref*rence*'; fi
n=0; skipped=0
while IFS= read -r -d '' f; do
  base="$(basename "$f")"
  if [ -e "$DEST/$base" ] || [ -L "$DEST/$base" ]; then skipped=$((skipped+1)); continue; fi
  ln -s "$f" "$DEST/$base"; n=$((n+1))
done < <(find "$SRC" \( -type d \( -iname proxy -o -iname proxies -o -iname "$REFPAT" \) -prune \) -o -type f ! -name '._*' \( -iname '*.mov' -o -iname '*.mp4' -o -iname '*.m4v' -o -iname '*.mxf' -o -iname '*.mkv' \) -print0 | sort -z)

printf -- '- %s → `%s/` (%s clips linked on %s)\n' "$SRC" "${DEST#projects/$NAME/}" "$n" "$(date +%F)" >> "projects/$NAME/raw/SOURCES.md"
echo "✓ linked $n clips into $DEST ($skipped already there). Originals untouched: $SRC"
