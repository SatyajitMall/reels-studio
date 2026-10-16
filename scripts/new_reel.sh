#!/usr/bin/env bash
# Create a new reel folder from the template.
# Usage: scripts/new_reel.sh <reel-name>
set -euo pipefail
cd "$(dirname "$0")/.."
NAME="${1:?Usage: scripts/new_reel.sh <reel-name>}"
NAME="$(echo "$NAME" | tr ' ' '-' | tr -cd '[:alnum:]-_')"
DEST="projects/$NAME"
[ -e "$DEST" ] && { echo "projects/$NAME already exists"; exit 1; }
cp -R projects/_template "$DEST"
find "$DEST" -name .gitkeep -delete
sed -i '' "s/^| Reel name | |/| Reel name | $NAME |/" "$DEST/project.md" 2>/dev/null || true
sed -i '' "s/^| Arch version | |/| Arch version | $(cat studio/VERSION) |/" "$DEST/project.md" 2>/dev/null || true
echo "Created $DEST"
echo "  1. Drop main / hero clips in   $DEST/raw/a-roll/"
echo "  2. Drop cutaways in            $DEST/raw/b-roll/   (music-only reel: everything can go here)"
echo "  3. (optional) Reference reels in $DEST/references/"
echo "  4. Open a NEW Code session at the reels-studio root and say:  /cinematic-reel $NAME"
open "$DEST" 2>/dev/null || true
