#!/usr/bin/env python3
"""Bake plan for the baked look (HQ brief 2026-10-30): one tools/shot_look.py render per V1 shot of v5e.

Reads the v5e dump (analysis/_es_out_bake.txt from analysis/_es_v5e_bakeparams.jsx) and writes analysis/look/bake_plan.json:
per shot the raw clip, --in in the camera file's own seconds (interpreted clips: Premiere in × 25 / native fps), --frames,
and --crop m,u0,v0 at the middle of the played span (m = Scale/50 on vertical 4K, u = 0.5 + (0.5 - pos)/m).

Usage: bake_plan.py  [prints the shot_look commands]
"""
import json, os, subprocess
from pathlib import Path

R = Path(__file__).resolve().parents[1]
FPS = 25


def native_fps(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True).stdout.split()[0].rstrip(",")
    n, d = p.split("/")
    return float(n) / float(d)


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


def main():
    dump = json.loads((R / "analysis/_es_out_bake.txt").read_text())
    plan = []
    for n, s in enumerate(dump["shots"], 1):
        frames = s["end"] - s["start"]
        mid = s["inP"] + frames / FPS / 2
        m = at(s["Scale"], mid) / 50
        px, py = s["Position"]["val"]
        u, v = 0.5 + (0.5 - px) / m, 0.5 + (0.5 - py) / m
        clip = "raw/b-roll/" + os.path.basename(s["path"])
        nf = native_fps(str(R / clip))
        # Premiere time is frame/25 (every clip interpreted at 25); the camera file's time is frame/native fps.
        # Premiere shows the frame whose span contains the in point (4.70 s at 25 fps is frame 117, not 118): floor, not round.
        # Seek a quarter frame early so ffmpeg can't land one frame late on files whose timestamps aren't exact multiples
        # (C056: 24.94 fps average but 25 fps timestamps there); a quarter, not a half, keeps shot_look's handle rounding exact.
        idx = int(s["inP"] * FPS + 1e-3)
        t_in = round(max(0.0, (idx - 0.25) / nf), 4)
        name = f"{n:02d}_{Path(clip).stem.split('_')[-1]}"
        plan.append({"shot": n, "name": name, "seq": [s["start"], s["end"]], "clip": clip, "native_fps": round(nf, 3), "prem_in": s["inP"],
                     "in": t_in, "src_index": idx, "frames": frames, "crop": [round(m, 4), round(u, 4), round(v, 4)],
                     "warp": "Warp Stabilizer" in s["fx"], "out": f"renders/baked/{name}.mov"})
    (R / "analysis/look/bake_plan.json").write_text(json.dumps(plan, indent=1))
    for p in plan:
        print(f"{p['name']}: --clip {p['clip']} --in {p['in']} --frames {p['frames']} --crop {','.join(map(str, p['crop']))}"
              f"{'  (Warp)' if p['warp'] else ''}{'  (native ' + str(p['native_fps']) + ' fps)' if abs(p['native_fps'] - 25) > 0.01 else ''}")


if __name__ == "__main__":
    main()
