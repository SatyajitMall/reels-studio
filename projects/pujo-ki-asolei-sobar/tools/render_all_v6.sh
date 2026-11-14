#!/bin/zsh
# Round 8: deflicker every 30 fps shot (v5 / v5b -> v6); the 25 fps shots (3 C043, 11 C052) have no 10 Hz flicker and pass through.
cd $HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar
P=$HOME/Documents/reels-studio/.venv/bin/python
$P tools/deflicker.py 1 v5 v6 || exit 1
for n in 2 4 5 6 7 8 9 10 12 13; do $P tools/deflicker.py $n v5b v6 || exit 1; done
$P - <<'PY'
import json
from pathlib import Path
R = Path("renders/final_shots")
for n in ("03", "11"):
    j = next(R.glob(f"{n}_*_v5b.json")); r = json.loads(j.read_text())
    r["deflicker"] = {"skipped": "25 fps source: 100 Hz = 4 x 25, no 10 Hz flicker (scan 0.10 % / 0.01 %)", "from": r["file"]}
    Path(str(j).replace("_v5b.json", "_v6.json")).write_text(json.dumps(r, indent=1)); print("pass-through", j.name)
PY
$P tools/flicker_compare.py v5b v6 2 3 4 5 6 7 8 9 10 11 12 13
