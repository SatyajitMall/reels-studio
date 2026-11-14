#!/usr/bin/env python3
"""Write analysis/_v6_data.jsx (a JS data file for analysis/_es_v6_build.jsx): per V1 shot of v5e, the baked file, its in/out
(place_in_frames handle + shot length, in the baked file's own 25 fps time), the static Position and the Scale at the baked
in/out (interpolated from the v5e keys over the played span), and whether Warp goes back on. Needs every bake's .json sidecar."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
FPS = 25
# Measured (scratchpad align1.py, NCC at shot frames 2/12/22/33): Premiere shows C056 (24.94 fps, interpreted at 25) one frame
# earlier than ffmpeg's frame index, all through the shot, so its bake is placed one handle frame earlier.
PLACE_OFFSET = {"18_C056": -1}


def at(keys, t):
    if "val" in keys:
        return keys["val"]
    k = keys["keys"]
    if t <= k[0][0]:
        return k[0][1]
    for (t0, v0), (t1, v1) in zip(k, k[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * (t - t0) / (t1 - t0)
    return k[-1][1]


plan = json.loads((R / "analysis/look/bake_plan.json").read_text())
dump = {s["start"]: s for s in json.loads((R / "analysis/_es_out_bake.txt").read_text())["shots"]}
rows = []
for p in plan:
    s = dump[p["seq"][0]]
    side = json.loads((R / p["out"]).with_suffix(".json").read_text())
    assert side["frames"] >= side["place_in_frames"] + p["frames"], p["name"]
    b_in = (side["place_in_frames"] + PLACE_OFFSET.get(p["name"], 0)) / FPS
    b_out = b_in + p["frames"] / FPS
    keyed = "keys" in s["Scale"]
    sc = [round(at(s["Scale"], s["inP"]), 4), round(at(s["Scale"], s["outP"]), 4)] if keyed else [s["Scale"]["val"]]
    rows.append({"name": p["name"], "start": p["seq"][0], "end": p["seq"][1], "path": str(R / p["out"]), "orig": Path(p["clip"]).name,
                 "bin": round(b_in, 4), "bout": round(b_out, 4), "pos": s["Position"]["val"], "scale": sc, "warp": p["warp"]})
(R / "analysis/_v6_data.jsx").write_text("var V6=" + json.dumps(rows) + ";\n")
for r in rows:
    print(r["name"], r["start"], r["end"], r["bin"], r["bout"], r["scale"], r["pos"], "Warp" if r["warp"] else "")
