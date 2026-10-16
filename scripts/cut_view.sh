#!/usr/bin/env bash
# Filmstrip + waveform PNG for a time range, to check a cut visually.
# Usage: scripts/cut_view.sh <video> <start_sec> <end_sec> [out.png]
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${4:-/tmp/cut_$(basename "$1")_$2-$3.png}"
./.venv/bin/python .vendor/video-use/helpers/timeline_view.py "$1" "$2" "$3" -o "$OUT"
echo "$OUT"
