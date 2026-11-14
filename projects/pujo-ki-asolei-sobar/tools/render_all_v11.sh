#!/bin/zsh
# Round 11: every source shot re-rendered in --natural-matched mode (m1), deflickered (m1d), built (v11f), B&W (bw11), previews.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R; L=renders/final_shots
r5() { $P tools/shot_render_v5.py $1 --ver m1 --edl v5 --natural-matched > $L/_log_m1_v5_$1.txt 2>&1; }
r9() { $P tools/shot_render_v5.py $1 --ver m1 --edl v9r --natural-matched > $L/_log_m1_v9r_$1.txt 2>&1; }
r5 1 & r5 4 & r5 8 & wait
r5 9 & r5 11 & r5 13 & wait
r9 2 & r9 3 & r9 5 & wait
r9 6 & r9 9 & r9 11 & wait
r9 14
grep -h "✓\|Traceback\|Error" $L/_log_m1_*.txt
# deflicker the 30 fps shots; C052 (25 fps) passes through
for a in "1 C152" "4 C032" "8 C201" "9 C213" "13 C193" "2 C027" "3 C190" "5 C222" "6 C212" "9 C215" "11 C216" "14 C027"; do
  set -- ${=a}; $P tools/deflicker.py $1 m1 m1d --clip $2 || exit 1
done
$P - <<'PY'
import json
from pathlib import Path
R = Path("renders/final_shots"); j = R / "11_C052_m1.json"; r = json.loads(j.read_text())
r["deflicker"] = {"skipped": "25 fps source", "from": r["file"]}; (R / "11_C052_m1d.json").write_text(json.dumps(r, indent=1)); print("pass-through C052")
PY
$P tools/v9_build.py --edl v11 --out v11f || exit 1
for n in 2 3 4 5 6 7 8 9 10 11 12; do $P tools/bw_render.py $n --src v11f --out bw11 || exit 1; done
$P tools/preview_assemble.py v11f v11 renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 || exit 1
$P tools/preview_assemble.py bw11 v11 renders/previews/pujo-ki-asolei-sobar_v11bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio; mkdir -p $R/analysis/review_v11
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -3
$P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V11 DONE
