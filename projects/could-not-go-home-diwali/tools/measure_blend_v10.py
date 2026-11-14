"""v10 (reel-local, 2026-11-12): the director on 12 (Pexels diya, AE Timewarp 50 %) and 19 (Veo cracker man, Timewarp 50 %):
"looks a little fake ... different from the rest of the footage ... the hand is not shaking, not moving, and the pan looks too
good to be true. Don't change it, optimise it so they blend."

Measures, per shot of an export, inside the 16:9 window, what makes a shot read as the director's handheld phone footage:
  camera path   frame-to-frame shift of the window's outer ring (scripts/motion_audit.py ring_shift), cumulated.
                wander = the path minus its straight-line fit (rms, px at 1080 wide): the slow drift of a hand.
                micro  = the path minus a 6-frame gaussian of itself (rms): the fine shake.
  grain         luma minus its 3x3 median, std over the flattest 30 % of the picture (8-bit codes): sensor noise.
  detail        p90 of |Laplacian| of luma at full res: how crisp edges are.
Usage: ../../.venv/bin/python tools/measure_blend_v10.py <export> <map.json> [-o out.json]
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import motion_audit as ma  # noqa: E402

WIN = (0, 606, 1080, 608)


def full_frames(path, t0, t1):
    import subprocess
    x, y, w, h = WIN
    b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", path, "-vf",
                        f"crop={w}:{h}:{x}:{y},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.uint8).reshape(-1, h, w).astype(np.float32)


def main():
    exp, mp = sys.argv[1], sys.argv[2]
    out = sys.argv[sys.argv.index("-o") + 1] if "-o" in sys.argv else None
    shots = json.load(open(mp))
    small, _ = ma.frames(Path(exp), WIN, 25.0); fps = 25.0
    rep = []
    for s in shots:
        name, st, en = s["name"], s["start"], s["end"]
        i0, i1 = int(round(st * fps)) + 2, int(round(en * fps)) - 2
        if i1 - i0 < 10:
            continue
        d = np.array([ma.ring_shift(small[i], small[i + 1]) for i in range(i0, i1 - 1)]) * (1080 / small.shape[2])
        p = np.vstack([[0, 0], np.cumsum(d, 0)]); t = np.arange(len(p))
        lin = np.stack([np.polyval(np.polyfit(t, p[:, k], 1), t) for k in range(2)], 1)
        wander = float(np.sqrt(((p - lin) ** 2).sum(1).mean()))
        micro = float(np.sqrt(((p - ndimage.gaussian_filter1d(p, 6, axis=0)) ** 2).sum(1).mean()))
        ff = full_frames(exp, st + 0.12, en - 0.12)[::3]
        gr, de = [], []
        for f in ff:
            r = f - ndimage.median_filter(f, 3)
            loc = ndimage.uniform_filter(np.abs(ndimage.sobel(f)), 9)
            flat = loc < np.quantile(loc, 0.3)
            gr.append(r[flat].std()); de.append(np.quantile(np.abs(ndimage.laplace(f)), 0.9))
        rec = {"shot": name, "wander_px": round(wander, 2), "micro_px": round(micro, 2),
               "pan_px_s": round(float(np.hypot(*(p[-1] - p[0])) / (len(p) / fps)), 1),
               "grain": round(float(np.mean(gr)), 2), "detail": round(float(np.mean(de)), 2)}
        rep.append(rec)
        print(f"{name[:34]:34s} wander {rec['wander_px']:5.2f}  micro {rec['micro_px']:4.2f}  pan {rec['pan_px_s']:5.1f} px/s  "
              f"grain {rec['grain']:4.2f}  detail {rec['detail']:5.2f}")
    if out:
        Path(out).write_text(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
