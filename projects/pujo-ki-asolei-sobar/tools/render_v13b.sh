#!/bin/zsh
# Round 13b: display-domain fine-grid deflicker (residual 0.76 -> 0.14 % mean tile on C215) on every 30 fps shot; skin post-pass;
# trims (+1/2 stop, black floor, extra lift on 7/9/2a/3, 2a cast); build v13g; preview; scan; watch.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
S="--iters 8 --clamp 0.35 --sig 3 --grid 160x90 --sps 1.0 --display"
for a in "1 C152" "2 C027" "15 C028" "3 C190" "4 C032" "5 C222" "6 C212" "8 C201" "9 C213" "9 C215" "11 C216" "13 C193"; do
  set -- ${=a}; $P tools/deflicker.py $1 m1 m4d --clip $2 ${=S} || exit 1
done
$P - <<'PY'
import json
from pathlib import Path
R = Path("renders/final_shots"); r = json.loads((R / "11_C052_m1d.json").read_text()); (R / "11_C052_m4d.json").write_text(json.dumps(r, indent=1)); print("pass-through C052")
PY
$P tools/skin_post.py m4d m4s 3 13 2>&1 | grep -v Warn
for a in "1 C152 v13_C152 m4d" "2 C027 v13_C027a m4d" "15 C028 v13_C028 m4d" "3 C190 v13_C190 m4s" "4 C032 v13_C032 m4d" "5 C222 v13_C222 m4d" "6 C212 v13_C212 m4d" "8 C201 v13_C201 m4d" "9 C213 v13_C213 m4d" "9 C215 v13_C215 m4d" "11 C052 v13_C052 m4d" "11 C216 v13_C216 m4d" "13 C193 v13_C193 m4s"; do
  set -- ${=a}; $P tools/shot_trim.py $1 $4 m4e --clip $2 --key $3 | sed 's/trims {.*}, gain/gain/' || exit 1
done
$P tools/v9_build.py --edl v13 --out v13g || exit 1
$P tools/preview_assemble.py v13g v13 renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 -o $R/analysis/review_v13/scan.json --shots $R/analysis/shots_v13.json 2>&1 | tail -1
rm -rf $R/analysis/review_v13/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 -o $R/analysis/review_v13/watch --fps 2 --shots $R/analysis/shots_v13.json 2>&1 | tail -1
echo V13B DONE
