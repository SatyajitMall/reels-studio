#!/usr/bin/env python3
"""Round 5b bake (director: "We are only using one idol?" -> "One idol per shot": red clay Durga, white sholapith Durga,
giant clay face). Same reference structure and cut frames as bake_r5:
  A  0.00-7.88  singer x red clay Durga (reused from renders/bakes_r5/A.mov)
  -- blink 7.88
  B  7.88-16.00 white sholapith Durga (Oct18 C208 0.00-4.03, eye-locked, AI-upscaled, slowed ~1.68x by motion interpolation)
  -- blink 16.00
  C 16.00-21.96 giant clay face (Oct17 C162 5.77-7.14: the glide lands on her, eye-locked; then held under a constant push)
Output renders/bakes_r7/V1_timeline_r7.mov. Usage: python tools/bake_r7.py [--only B,C] [--compose-only]
"""
import sys, json, subprocess, shutil, argparse
from pathlib import Path
import numpy as np
from PIL import Image
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R
B = R.B
OUT = REEL / "renders/bakes_r7"
TRK = json.loads((REEL / "analysis/eye_tracks_r5b.json").read_text())
C208 = str(REEL / "raw/b-roll/A001_10182155_C208.mov"); C162 = str(REEL / "raw/b-roll/A001_10172021_C162.mov")
F_B, F_C, F_END = R.F_B, R.F_C, R.F_END

def shot_B():
    """v8 (director: "shot stabilisation and video enhancement need to be done"): v7's per-frame AI + motion interpolation
    made textures shimmer frame to frame. The idol is still, so B is her sharpest frame, denoised at source resolution,
    AI-enhanced once, carried by a smooth push with a gentle drift: no shake, no shimmer."""
    N = F_C - F_B; tr = TRK["2"]; px = 235; pr = dict(exp=-0.12)
    t_s = R.sharpest_time(C208, 0.2, 4.0, 0.533, 0.43); j = int(round(t_s * 30)); j = min(j, len(tr["ex"]) - 1)
    ex, ey = tr["ex"][j], tr["ey"][j]
    cw0, cw1 = R.CW(px, 0.42), R.CW(px, 0.54)
    im = next(B.frames(C208, t_s, 1, False, R.W4, R.H4)).crop(tuple(round(v) for v in R.box_for(ex, ey, cw0)))
    big = R.ai_still(R.denoise(im))
    gains = B.primary_params(R.push_from_big(big, cw0, cw0), wb=0.5, exp=pr["exp"])
    enc = B.encoder(OUT / "B.mov", "rgb48le")
    for k in range(N):
        f = k / (N - 1); cw = cw0 + (cw1 - cw0) * B.ease(f)
        x = R.push_from_big(big, cw0, cw, du=0.012 * (f - 0.5))          # slow push + a 1 %-of-frame lateral drift for life
        x = B.halation(R.grade(x, gains, pr)); enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "B", "clip": "Oct18 C208", "frames": N, "still_t": t_s}

def shot_C():
    # the clay face's eye pair is ~800 source px: the crop is a native-resolution downscale, so no AI upscaling is needed
    N = F_END - F_C; tr = TRK["3"]; n_live = 36; px = 800; pr = dict()   # v8: live part ends before the track kink (5 px jolt at 17.56)
    ex_s = B.smooth(tr["ex"][:n_live], 3.0); ey_s = B.smooth(tr["ey"][:n_live], 3.0)   # v8: smoother path
    cw0, cw1 = R.CW(px, 0.60), R.CW(px, 0.72)
    cwk = lambda k: cw0 + (cw1 - cw0) * B.ease(k / (N - 1))
    src = list(B.frames(C162, 5.77, n_live, False, R.W4, R.H4))
    # v8: crop, then a gentle denoise of the crop at source resolution, then Lanczos down (no AI on C: it is a native downscale)
    live = [np.asarray(R.denoise(src[j].crop(tuple(round(v) for v in R.box_for(ex_s[j], ey_s[j], cwk(j))))).resize((1080, 1920), Image.LANCZOS)).astype(np.float32) / 255 for j in range(n_live)]
    hold_cw = cwk(n_live); big = R.denoise(src[-1].crop(tuple(round(v) for v in R.box_for(ex_s[-1], ey_s[-1], hold_cw))))
    # v9 (director: "there are some light flickering issue"): the pandal's mains-powered lights beat against 30 fps (a 3-frame
    # ~0.8 % pulse on the face). Per-frame gain matching the face-region luma to its 9-frame moving average; the hold keeps the
    # last frame's gain so nothing jumps at the switch.
    from scipy.ndimage import uniform_filter1d
    Lf = np.array([float(B.luma(x[600:1300, 240:840]).mean()) for x in live]); trend = uniform_filter1d(Lf, 9, mode="nearest")
    dg = trend / np.maximum(Lf, 1e-4); live = [np.clip(x * g, 0, 1) for x, g in zip(live, dg)]
    gains = B.primary_params(live[n_live // 2], wb=0.5, exp=0.0)
    enc = B.encoder(OUT / "C.mov", "rgb48le")
    for k in range(N):
        x = live[k] if k < n_live else np.clip(R.push_from_big(big, hold_cw, hold_cw + (cw1 * 0.97 - hold_cw) * (k - n_live + 1) / (N - n_live)) * dg[-1], 0, 1)
        x = B.halation(R.grade(x, gains, pr)); enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "C", "clip": "Oct17 C162", "frames": N, "live": n_live}

from scipy import ndimage as _nd
def clarity(x, amt=0.18, sigma=22):
    bl = np.stack([_nd.gaussian_filter(x[..., c], sigma) for c in range(3)], -1)
    return np.clip(x + amt * (x - bl), 0, 1)

def compose():
    seq = [B.reader(OUT / "A.mov"), B.reader(OUT / "B.mov"), B.reader(OUT / "C.mov")]
    enc = B.encoder(OUT / "V1_timeline_r7.mov", "rgb48le"); n = 0
    for t in range(550):
        if t >= F_END: x = np.zeros((1920, 1080, 3), np.float32)
        else:
            s = 0 if t < F_B else (1 if t < F_C else 2); x = next(seq[s])
            x = clarity(x)                                                       # v9 Rich & deep: local contrast, baked (a cube can't do it)
            if t < 8: x = x * (t / 8)
            for c in (F_B, F_C):
                k = t - c
                if -3 <= k < 0: x = B.slit(x, B.BL_CLOSE[k + 3])
                elif k == 0: x = np.zeros_like(x)
                elif 1 <= k <= 3: x = B.slit(x, B.BL_OPEN[k - 1])
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print("V1_timeline_r7.mov:", n, "frames")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default="B,C"); ap.add_argument("--compose-only", action="store_true"); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not (OUT / "A.mov").exists(): shutil.copy(REEL / "renders/bakes_r5/A.mov", OUT / "A.mov")
    if not a.compose_only:
        for s in a.only.split(","): print({"B": shot_B, "C": shot_C}[s.strip()](), flush=True)
    compose()

if __name__ == "__main__":
    main()
