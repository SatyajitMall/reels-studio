#!/usr/bin/env python3
"""Round 9: colour fidelity of a v9-family still pass against the camera file at the same framing, per shot (mid-frame).
Director, on v9b: "0:23 the pandal lost its original colour ... same at 0:07, same at 0:10". Reports luma, saturation (HSV, pixels
with V > 0.1), midtone hue and contrast (p98 − p02) for camera and graded, and the Saturation factor that would bring the grade back
to the camera's saturation. Usage (reels-studio root): .venv/bin/python projects/<reel>/tools/v9_fidelity.py <pass dir name> [out.jpg]"""
import json, sys
import numpy as np
from PIL import Image
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bake_check as B, shot_look as S  # noqa: E402
from process_ab import reframe  # noqa: E402

R = B.R
F = json.loads((R / "analysis/_v9_frame.jsx").read_text()[len("var V9F="):-2])
old = {c["start"]: c for c in json.loads((R / "analysis/_es_out_v9read.txt").read_text())["clips"]}
NATIVE = {"10192144_C017": 30.004, "10202144_C056": 24.941}


def st(a):
    x = a.astype(np.float32) / 255; y = x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    m = np.ones(y.shape, bool); m[int(y.shape[0] * .72):int(y.shape[0] * .82)] = False
    mx, mn = x.max(-1), x.min(-1); v = mx > 0.1; sat = np.where(mx > 1e-3, (mx - mn) / np.maximum(mx, 1e-3), 0)
    mid = m & (y > 0.2) & (y < 0.6); c = x[mid].mean(0); cmx, cmn = c.max(), c.min()
    hue = 0.0 if cmx - cmn < 1e-6 else (60 * (((c[1] - c[2]) / (cmx - cmn)) % 6) if cmx == c[0] else 60 * ((c[2] - c[0]) / (cmx - cmn) + 2) if cmx == c[1] else 60 * ((c[0] - c[1]) / (cmx - cmn) + 4))
    yy = y[m]
    return {"luma": round(float(yy.mean()), 3), "sat": round(float(sat[m & v].mean()), 3), "hue": round(float(hue), 1), "contrast": round(float(np.percentile(yy, 98) - np.percentile(yy, 2)), 3)}


def main():
    pdir = R / "analysis/v9_stills" / sys.argv[1]; tiles = []
    print(f"{'shot':8s} {'camera L/sat/hue/contrast':32s} {'graded':32s} sat factor")
    for i, f in enumerate(F):
        o = old[f["f"]]; n = f["n"]; a, b = o["start"], o["end"]; mfr = a + (b - a) // 2; k = mfr - a; tp = o["inP"] + k / 25
        g = np.asarray(Image.open(pdir / f"{mfr:03d}.png").convert("RGB"))
        nf = NATIVE.get(n, 25.0); tn = tp * 25 / nf if n == "10192144_C017" else ((round(tp * 25) - 1) / nf if n == "10202144_C056" else tp)
        clip = str(R / "raw/b-roll" / f"A001_{n}.mov"); size = S.frame_size(clip)
        raw = next(S.decode_stream(clip, max(0, tn - 0.25 / nf), 1, "format=rgb24", size))
        s9 = f["s"][0] + (f["s"][1] - f["s"][0]) * k / (b - a)
        p9 = f["p"][0] if len(f["p"]) == 1 else [f["p"][0][j] + (f["p"][1][j] - f["p"][0][j]) * k / (b - a) for j in range(2)]
        cam = reframe((raw * 255 + 0.5).clip(0, 255).astype(np.uint8), s9, p9)
        c, v = st(cam), st(g)
        print(f"#{i+1:<2d} {n.split('_')[1]}  L{c['luma']:.2f} s{c['sat']:.2f} h{c['hue']:5.1f} c{c['contrast']:.2f}      L{v['luma']:.2f} s{v['sat']:.2f} h{v['hue']:5.1f} c{v['contrast']:.2f}      x{c['sat']/max(v['sat'],1e-3):.2f}")
        tiles.append(np.concatenate([cam, g], 1))
    if len(sys.argv) > 2:
        rows = [np.concatenate(tiles[r * 7:(r + 1) * 7], 1) for r in range(2)]
        Image.fromarray(np.concatenate(rows, 0)).resize((7 * 2 * 160, 2 * 284), Image.LANCZOS).save(sys.argv[2], quality=90); print("✓", sys.argv[2])


if __name__ == "__main__":
    main()
