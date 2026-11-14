#!/bin/zsh
# Round 13 (director, on the phone: "a lot of shots have the light flickering issue"): stronger deflicker on every 30 fps shot
# (8 passes, clamp 0.35, 64x24 tiles, temporal sigma 3: residual 6.9 % -> 1.2 % max on C028), then the skin post-pass where used.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
S="--iters 8 --clamp 0.35 --grid 64x24 --sig 3"
for a in "1 C152" "2 C027" "15 C028" "3 C190" "4 C032" "5 C222" "6 C212" "8 C201" "9 C213" "9 C215" "11 C216" "13 C193"; do
  set -- ${=a}; $P tools/deflicker.py $1 m1 m2d --clip $2 ${=S} || exit 1
done
$P - <<'PY'
import json
from pathlib import Path
R = Path("renders/final_shots"); j = R / "11_C052_m1d.json"; r = json.loads(j.read_text()); (R / "11_C052_m2d.json").write_text(json.dumps(r, indent=1)); print("pass-through C052 (25 fps)")
PY
$P tools/skin_post.py m2d m2s 3 13 2>&1 | grep -v Warn
echo DEFLICKER DONE
