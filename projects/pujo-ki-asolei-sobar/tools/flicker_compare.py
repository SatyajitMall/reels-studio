#!/usr/bin/env python3
"""Before/after flicker for given shots: global, row-band and tile 10 Hz amplitude (%), p95 frame-to-frame luma step.
Usage: flicker_compare.py <suffix a> <suffix b> <shot n> [...]"""
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
import importlib.util
spec = importlib.util.spec_from_file_location("fs", Path(__file__).resolve().parent / "flicker_scan.py")
src = open(spec.origin).read().split("out = {}")[0].replace("SUF = sys.argv[1]; SUF1 = sys.argv[2] if len(sys.argv) > 2 else SUF", "")
ns = {"__file__": spec.origin}; exec(src, ns); frames, amp10 = ns["frames"], ns["amp10"]
A, B = sys.argv[1], sys.argv[2]
edl = {s["n"]: s for s in json.loads((REEL / "analysis/edl_v5.json").read_text())["shots"]}
res = {}
for n in sys.argv[3:]:
    s = edl[n]
    for suf in (A, B):
        js = R / f"{int(n):02d}_{s['clip']}_{suf}.json"; js = js if js.exists() else R / f"{int(n):02d}_{s['clip']}_v5.json"; r = json.loads(js.read_text()); a0 = round(r["place_in"] * 30); nf = s["endF"] - s["startF"]
        Fr = frames(R / r["file"])[a0:a0 + nf]; g = Fr.reshape(len(Fr), -1).mean(1)
        bands = [amp10(Fr[:, y:y + 20].reshape(len(Fr), -1).mean(1))[0] for y in range(0, 240, 20)]
        tiles = [amp10(Fr[:, y:y + 30, x:x + 34].reshape(len(Fr), -1).mean(1))[0] for y in range(0, 240, 30) for x in range(0, 135, 34)]
        step = np.percentile(np.abs(np.diff(np.log(g))) * 100, 95)
        res.setdefault(n, {})[suf] = {"global": round(amp10(g)[0], 2), "bands_max": round(max(bands), 2), "tiles_p90": round(float(np.percentile(tiles, 90)), 2), "tiles_max": round(max(tiles), 2), "step_p95": round(float(step), 2)}
        print(f"shot {n:>2} {s['clip']} {suf:>4}: global {amp10(g)[0]:5.2f}%  bands max {max(bands):5.2f}%  tiles p90 {np.percentile(tiles, 90):5.2f}% max {max(tiles):5.2f}%  p95 step {step:5.2f}%", flush=True)
(REEL / f"analysis/flicker/compare_{A}_{B}.json").write_text(json.dumps(res, indent=1))
