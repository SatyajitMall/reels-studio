#!/usr/bin/env python3
"""Review v9b minors (analysis/review_v9b.md, PASS with 4 minors), v9c. A and B are v9b's bakes, unchanged; only:
  C  #1 the global deflicker left the two cheeks pulsing in anti-phase (~1.2 %, one lamp beating at 30 fps): a regional
        deflicker (low-res luma gain field matched to its 9-frame moving average) on the live frames; the hold keeps the last
        live frame's field, so nothing jumps at the handover.
  C  #2 the bright panel in the bottom-right corner (16-20 s) still popped under the bottom grad: a corner darkening on top.
  B  #3 the title's sub-line sat on the gold chest ornament: a soft dark plate (-28 %) under the title while it is up.
  (#4 nath: the real jewellery, overexposed in the source; accepted.)
Output renders/bakes_r9c/V1_timeline_v9c.mov. Usage: python tools/bake_r9c.py [--compose-only]
"""
import sys, argparse
from pathlib import Path
import numpy as np
from scipy.ndimage import uniform_filter1d, gaussian_filter, zoom
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r9b as R9, bake_r7 as R7
B = R9.B
OUT = REEL / "renders/bakes_r9c"
F_B, F_C, F_END = R9.F_B, R9.F_C, R9.F_END
N_LIVE = 36                                  # bake_r7.shot_C: live frames, then the hold
BLK = 40                                     # gain-field block size (px); 27 x 48 blocks
CORNER = (0.80, 1.00, 0.45, 0.95, 0.45)      # y0, y1, x0, x1 (fractions), extra depth in the bottom-right corner
TITLE = (215, 230, 280, 295)                 # V5 title in / full / out frames
PLATE = (540, 1470, 430, 140, 0.28)          # centre x, y, radius x, y, depth

def gain_fields(path):
    """streamed: only the live frames' block means are kept"""
    lo = []
    for k, x in enumerate(B.reader(path)):
        if k < N_LIVE: lo.append(B.luma(x).reshape(1920 // BLK, BLK, 1080 // BLK, BLK).mean((1, 3)))
    lo = np.stack(lo)
    lo = np.stack([gaussian_filter(m, 1.5) for m in lo]); trend = uniform_filter1d(lo, 9, axis=0, mode="nearest")
    return trend / np.maximum(lo, 1e-4)

def shot_C():
    path = REEL / "renders/bakes_r7/C.mov"; g = gain_fields(path); up = lambda m: zoom(m, BLK, order=1)[..., None]
    yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32); yy /= 1920; xx /= 1080
    grad = 1 - (1 - R9.GRAD_MIN) * R9.smoothstep(R9.GRAD_Y0, R9.GRAD_Y1, yy)
    y0, y1, x0, x1, d = CORNER; grad = (grad * (1 - d * R9.smoothstep(y0, y1, yy) * R9.smoothstep(x0, x1, xx)))[..., None]
    enc = B.encoder(OUT / "C.mov", "rgb48le"); last = up(g[-1]); n = 0
    for k, x in enumerate(B.reader(path)):
        n += 1
        x = x * (up(g[k]) if k < N_LIVE else last)
        enc.stdin.write((np.clip(x * grad, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "C", "frames": n, "gain_range": [float(g.min()), float(g.max())]}

def plate(t):
    a, b, c, e = TITLE
    env = 0.0 if t < a or t >= e else (min(1.0, (t - a) / (b - a)) if t < b else (1.0 if t < c else (e - t) / (e - c)))
    if env <= 0: return None
    cx, cy, rx, ry, d = PLATE; yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
    return (1 - d * env * np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)))[..., None]

def compose():
    seq = [B.reader(R9.OUT / "A.mov"), B.reader(R9.OUT / "B.mov"), B.reader(OUT / "C.mov")]
    enc = B.encoder(OUT / "V1_timeline_v9c.mov", "rgb48le"); n = 0
    for t in range(550):
        if t >= F_END: x = np.zeros((1920, 1080, 3), np.float32)
        else:
            s = 0 if t < F_B else (1 if t < F_C else 2); x = R7.clarity(next(seq[s]))
            p = plate(t)
            if p is not None: x = x * p
            if t < 8: x = x * (t / 8)
            for c in (F_B, F_C):
                k = t - c
                if -3 <= k < 0: x = B.slit(x, B.BL_CLOSE[k + 3])
                elif k == 0: x = np.zeros_like(x)
                elif 1 <= k <= 3: x = B.slit(x, B.BL_OPEN[k - 1])
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print("V1_timeline_v9c.mov:", n, "frames")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--compose-only", action="store_true"); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not a.compose_only: print(shot_C(), flush=True)
    compose()

if __name__ == "__main__":
    main()
