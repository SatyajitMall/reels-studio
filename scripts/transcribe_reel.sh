#!/usr/bin/env bash
# Word-level transcribe every A-roll clip of a reel and pack them into takes_packed.md.
# Usage: scripts/transcribe_reel.sh <reel-name> [--language en]
set -euo pipefail
cd "$(dirname "$0")/.."
NAME="${1:?Usage: scripts/transcribe_reel.sh <reel-name>}"; shift || true
DIR="projects/$NAME"
PY=./.venv/bin/python
H=.vendor/video-use/helpers
[ -d "$DIR/raw/a-roll" ] || { echo "No $DIR/raw/a-roll"; exit 1; }

shopt -s nullglob nocaseglob
clips=("$DIR"/raw/a-roll/*.{mp4,mov,m4v,mxf,mkv})
[ ${#clips[@]} -gt 0 ] || { echo "No clips in $DIR/raw/a-roll"; exit 1; }

for c in "${clips[@]}"; do
  echo "▸ transcribing $(basename "$c")"
  "$PY" "$H/transcribe.py" "$c" --edit-dir "$DIR" "$@"   # cached: skips if JSON exists
done

"$PY" "$H/pack_transcripts.py" --edit-dir "$DIR" -o "$DIR/transcripts/takes_packed.md"
echo "✓ $DIR/transcripts/takes_packed.md"
