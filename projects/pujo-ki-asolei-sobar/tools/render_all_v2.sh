#!/bin/sh
# Round 2 renderer in parallel (4 at a time). Usage: [VER=v2] render_all_v2.sh <shot> ...
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar
PY=$HOME/Documents/reels-studio/.venv/bin/python
V=${VER:-v2}
run() { $PY $R/tools/shot_render_v2.py "$1" --ver $V > $R/renders/final_shots/_log_${V}_$1.txt 2>&1; }
i=0
for n in "$@"; do run "$n" & i=$((i+1)); if [ $((i % 4)) -eq 0 ]; then wait; fi; done
wait
for n in "$@"; do grep -h "✓\|stabilise\|correction\|Error\|Traceback" $R/renders/final_shots/_log_${V}_$n.txt; done
