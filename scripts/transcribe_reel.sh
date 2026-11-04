#!/usr/bin/env bash
# Word-level transcribe a reel's speech and pack it into transcripts/takes_packed.md.
# Default: local Whisper (scripts/transcribe_local.py, free and offline). --scribe uses ElevenLabs Scribe instead
# (needs a working ELEVENLABS_API_KEY in .env).
# Files: every clip in raw/a-roll/, or the files you name (an external VO, a reference's audio).
# Usage: scripts/transcribe_reel.sh <reel-name> [--language en] [--model small] [--vad] [--force] [--scribe] [file ...]
set -euo pipefail
cd "$(dirname "$0")/.."
NAME="${1:?Usage: scripts/transcribe_reel.sh <reel-name> [--language en] [--model small] [--vad] [--force] [--scribe] [file ...]}"; shift
DIR="projects/$NAME"
PY=./.venv/bin/python
H=.vendor/video-use/helpers
[ -d "$DIR" ] || { echo "No $DIR"; exit 1; }

scribe=0; lang=(); model=(); flags=(); files=()
while [ $# -gt 0 ]; do
  case "$1" in
    --scribe) scribe=1 ;;
    --language|--model) [ $# -ge 2 ] || { echo "$1 needs a value"; exit 1; }
                        if [ "$1" = --language ]; then lang=(--language "$2"); else model=(--model "$2"); fi; shift ;;
    --language=*) lang=(--language "${1#*=}") ;;
    --model=*) model=(--model "${1#*=}") ;;
    --vad|--force) flags+=("$1") ;;
    -*) echo "Unknown option $1"; exit 1 ;;
    *) files+=("$1") ;;
  esac
  shift
done

if [ ${#files[@]} -eq 0 ]; then
  shopt -s nullglob nocaseglob
  files=("$DIR"/raw/a-roll/*.{mp4,mov,m4v,mxf,mkv})
  shopt -u nullglob nocaseglob
fi
[ ${#files[@]} -gt 0 ] || { echo "No clips in $DIR/raw/a-roll: name the files to transcribe (e.g. $DIR/audio/vo.wav)"; exit 1; }

if [ $scribe -eq 1 ]; then
  for c in "${files[@]}"; do
    echo "▸ Scribe: $(basename "$c")"
    "$PY" "$H/transcribe.py" "$c" --edit-dir "$DIR" ${lang[@]+"${lang[@]}"}   # cached: skips if JSON exists
  done
else
  "$PY" scripts/transcribe_local.py "${files[@]}" --edit-dir "$DIR" ${lang[@]+"${lang[@]}"} ${model[@]+"${model[@]}"} ${flags[@]+"${flags[@]}"}
fi

"$PY" "$H/pack_transcripts.py" --edit-dir "$DIR" -o "$DIR/transcripts/takes_packed.md"
echo "✓ $DIR/transcripts/takes_packed.md"
