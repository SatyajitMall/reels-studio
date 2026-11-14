#!/bin/sh
# Render EDL shots in parallel (5 at a time). Usage: [VER=v1h] render_all.sh <shot> [<shot> ...]
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar
PY=$HOME/Documents/reels-studio/.venv/bin/python
V=${VER:-v1h}
run() { $PY $R/tools/shot_render.py "$1" --ver $V > $R/renders/final_shots/_log_${V}_$1.txt 2>&1; }
i=0
for n in "$@"; do
  run "$n" &
  i=$((i+1)); if [ $((i % 5)) -eq 0 ]; then wait; fi
done
wait
for n in "$@"; do grep -h "✓\|matte\|Error\|Traceback" $R/renders/final_shots/_log_${V}_$n.txt; done
