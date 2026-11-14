#!/usr/bin/env python3
"""Check a baked shot before it goes into Premiere: reframe the --full bake exactly as the v5e Motion will (scale, position at
that reel time), put it beside the v5e export frame, and print luma / saturation / R-B for both.

Usage (reels-studio root): .venv/bin/python projects/<reel>/tools/bake_check.py -o sheet.png <name>@<reel_s> ...
<name> is a bake_plan.json shot name (e.g. 08_C020); Motion values come from analysis/_es_out_bake.txt (the v5e dump)."""
import argparse, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[1]
FPS, W, H = 25, 1080, 1920


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


def grab(path, t=None, vf="null", w=W, h=H, frame=None):
    sel = ["-vf", f"select=eq(n\\,{frame}),{vf}"] if frame is not None else ["-vf", vf]
    pre = ["-ss", f"{t:.3f}"] if t is not None else []
    raw = subprocess.run(["ffmpeg", "-v", "error", *pre, "-i", str(path), "-frames:v", "1", *sel, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8)[: w * h * 3].reshape(h, w, 3)


def stats(a):
    x = a.astype(np.float32) / 255
    y = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    mx, mn = x.max(-1), x.min(-1)
    s = np.where(mx > 1e-3, (mx - mn) / np.maximum(mx, 1e-3), 0)
    m = (y > 0.2) & (y < 0.6)
    return {"luma": round(float(y.mean()), 3), "sat": round(float(s.mean()), 3),
            "mid_R/G": round(float(x[..., 0][m].mean() / x[..., 1][m].mean()), 3), "mid_B/G": round(float(x[..., 2][m].mean() / x[..., 1][m].mean()), 3)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("-o", required=True); ap.add_argument("items", nargs="+")
    ap.add_argument("--ours", default=str(R / "renders/previews/v5e_quality.mp4"))
    a = ap.parse_args()
    plan = {p["name"]: p for p in json.loads((R / "analysis/look/bake_plan.json").read_text())}
    dump = {s["start"]: s for s in json.loads((R / "analysis/_es_out_bake.txt").read_text())["shots"]}
    rows = []
    for it in a.items:
        name, t = it.split("@"); t = float(t); p = plan[name]; s = dump[p["seq"][0]]
        side = json.loads((R / p["out"]).with_suffix(".json").read_text())
        k = round(t * FPS) - p["seq"][0]                                   # frame within the shot
        t_src = s["inP"] + k / FPS                                         # Premiere source time
        sc = at(s["Scale"], t_src) / 100; px, py = s["Position"]["val"]
        cw, ch = W / sc, H / sc; left, top = (0 - px * W) / sc + side["size"][0] / 2, (0 - py * H) / sc + side["size"][1] / 2
        vf = f"crop={cw:.2f}:{ch:.2f}:{left:.2f}:{top:.2f},scale={W}:{H}:flags=lanczos"
        baked = grab(R / p["out"], vf=vf, frame=side["place_in_frames"] + k)
        ours = grab(a.ours, t=round(t * FPS) / FPS)
        sb, so = stats(baked), stats(ours)
        print(f"{name} @ {t:.2f}s  v5e {so}  baked {sb}")
        rows.append(np.concatenate([ours, baked], 1))
    img = Image.fromarray(np.concatenate(rows, 0)); img = img.resize((img.width // 3, img.height // 3), Image.LANCZOS); img.save(a.o)
    print("✓", a.o)


if __name__ == "__main__":
    main()
