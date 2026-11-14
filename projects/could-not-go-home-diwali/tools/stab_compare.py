"""Shake before (bake) vs after (Premiere Warp render) for every shot of a stabilisation sequence, over the span the
reel uses; reel-local. Uses the measure() of motion_audit.py on the upright 4:3 middle that the window shows.
  .venv/bin/python -I projects/could-not-go-home-diwali/tools/stab_compare.py <stab.mov> <layout.json> -o <out.json>"""
import json, sys, argparse
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import motion_audit as ma
STUDIO = ma.STUDIO; REEL = ma.REEL
BAKE = {"01_C049_auto_step": "raw/baked/v3/C049_f2_00.60.mov", "02_C048_auto_turn": "raw/baked/v2/02_C048_auto_turn.mov",
        "05_C054_hands": "raw/baked/v2b/05_C054_hands.mov", "06_C056_juice": "raw/baked/v2/06_C056_juice.mov",
        "09_C053_serve": "raw/baked/v2/09_C053_serve.mov", "10_C062_vendor": "raw/baked/v3b/C062_f2_03.60.mov",
        "11_C062_vendor_close": "raw/baked/v3b/C062_f2_03.60.mov", "12_C058_show_step": "raw/baked/v2/04_C058_diwali_show.mov",
        "14_C051_paan_look": "raw/baked/v2/14_C051_paan_look.mov", "15_C059_icecream": "raw/baked/v2/15_C059_icecream.mov",
        "17_C064_wash": "raw/baked/v2/17_C064_wash.mov", "18_C064_look": "raw/baked/v2/18_C064_look.mov"}
# sideways 2160×3840 display → upright landscape (transpose=2), then the 4:3 middle the window shows
VF = "transpose=2,crop=ih*4/3:ih"
ap = argparse.ArgumentParser(); ap.add_argument("stab"); ap.add_argument("layout"); ap.add_argument("-o", required=True); a = ap.parse_args()
lay = json.loads(Path(a.layout).read_text())["placed"]
res = []
for p in lay:
    n = p["name"]; t_in = (p["in_f"] - p["src_start_f"]) / 25; need = p["need_f"] / 25
    b = ma.measure(ma.frames(REEL / BAKE[n], VF, ma.W, ma.H, ss=p["in_f"] / 25, t=need), ma.K)
    s = ma.measure(ma.frames(a.stab, VF, ma.W, ma.H, ss=p["seq_start_f"] / 25 + t_in, t=need), ma.K)
    r = {"shot": n}
    for tag, m in (("bake", b), ("stab", s)):
        r[tag] = {k: m[k] for k in ("jit_rms", "jit_max", "jerk_p95", "pan_px_s")}; r[tag]["jumps"] = [j["t"] for j in m["jumps"]]
    res.append(r)
    print(f"{n:22s} jit {r['bake']['jit_rms']:6.2f} → {r['stab']['jit_rms']:6.2f}   max {r['bake']['jit_max']:5.1f} → {r['stab']['jit_max']:5.1f}   "
          f"jerk95 {r['bake']['jerk_p95']:5.2f} → {r['stab']['jerk_p95']:5.2f}   jumps {len(r['bake']['jumps'])} → {len(r['stab']['jumps'])} {r['stab']['jumps'][:4]}")
Path(a.o).write_text(json.dumps(res, indent=1))
