#!/usr/bin/env python3
"""Quality pass (director on the v9c file on iPhone: soft / plastic faces / blocky darks). Prototype: a multi-frame stack
instead of AI repainting. For a static idol, N eye-locked source crops around the sharpest frame are aligned (phase
correlation, sub-pixel) and averaged: noise falls ~sqrt(N) with real texture kept, so no strong denoise or AI is needed.
Usage: python tools/stack_r9d.py B|A [--n 21]  -> analysis/ig/quality/stack_<shot>.png (+ the single-frame plain crop)
"""
import sys, json, argparse
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R, bake_r7 as R7
B = R.B; OUT = REEL / "analysis/ig/quality"

def phase_shift(ref, im):
    """sub-pixel (dy, dx) that aligns im to ref (luma, windowed phase correlation + parabolic peak)"""
    w = np.outer(np.hanning(ref.shape[0]), np.hanning(ref.shape[1]))
    F = np.fft.fft2(ref * w) * np.conj(np.fft.fft2(im * w)); F /= np.abs(F) + 1e-9
    c = np.fft.ifft2(F).real; py, px = np.unravel_index(np.argmax(c), c.shape)
    def sub(a, b, cc): return 0.5 * (a - b) / (a - 2 * cc + b) if (a - 2 * cc + b) != 0 else 0.0
    dy = py + sub(c[(py - 1) % c.shape[0], px], c[(py + 1) % c.shape[0], px], c[py, px])
    dx = px + sub(c[py, (px - 1) % c.shape[1]], c[py, (px + 1) % c.shape[1]], c[py, px])
    if dy > c.shape[0] / 2: dy -= c.shape[0]
    if dx > c.shape[1] / 2: dx -= c.shape[1]
    return dy, dx

def stack(src, track, t_s, cw0, n, fps=30):
    j0 = int(round(t_s * fps)); js = [j for j in range(j0 - n // 2, j0 + n // 2 + 1) if 0 <= j < len(track["ex"])]
    frames = list(B.frames(src, js[0] / fps, len(js), False, R.W4, R.H4))
    pad = 0.06; crops = []
    for j, im in zip(js, frames):
        l, t, r, b = R.box_for(track["ex"][j], track["ey"][j], cw0); pw, ph = (r - l) * pad, (b - t) * pad
        crops.append(np.asarray(im.crop((round(l - pw), round(t - ph), round(r + pw), round(b + ph)))).astype(np.float32) / 255)
    h = min(c.shape[0] for c in crops); w = min(c.shape[1] for c in crops); crops = [c[:h, :w] for c in crops]
    ref = crops[js.index(j0) if j0 in js else len(crops) // 2]; L = lambda x: x @ np.array([.2126, .7152, .0722], np.float32)
    al = []; sh = []
    for c in crops:
        dy, dx = phase_shift(L(ref), L(c)); sh.append((round(dy, 2), round(dx, 2)))
        al.append(np.stack([ndimage.shift(c[..., k], (dy, dx), order=3, mode="nearest") for k in range(3)], -1))
    st = np.median(np.stack(al), 0) if len(al) < 9 else np.mean(np.sort(np.stack(al), 0)[len(al) // 6: len(al) - len(al) // 6], 0)   # trimmed mean
    py, px = round(h * pad / (1 + 2 * pad)), round(w * pad / (1 + 2 * pad))
    return st[py:h - py, px:w - px], ref[py:h - py, px:w - px], sh

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("shot"); ap.add_argument("--n", type=int, default=21); a = ap.parse_args()
    if a.shot == "B": src, tr, t_s, cw0 = R7.C208, R7.TRK["2"], 0.8, R.CW(235, 0.42)
    else: src, tr, t_s, cw0 = R.C163, R.TRK["2"], json.loads((REEL / "renders/bakes_r9b/A_big.json").read_text())["t_s"], R.CW(R.EYE163, 0.36)
    st, one, sh = stack(src, tr, t_s, cw0, a.n)
    Image.fromarray((np.clip(st, 0, 1) * 255 + .5).astype(np.uint8)).save(OUT / f"stack_{a.shot}.png")
    Image.fromarray((np.clip(one, 0, 1) * 255 + .5).astype(np.uint8)).save(OUT / f"single_{a.shot}.png")
    L = lambda x: x @ np.array([.2126, .7152, .0722], np.float32)
    hp = lambda x: L(x) - ndimage.gaussian_filter(L(x), 1.5)
    print(json.dumps({"shot": a.shot, "n": a.n, "size": st.shape[:2], "shifts": sh[:5] + ["..."] + sh[-3:],
                      "hf_noise_single": float(hp(one)[:200, :200].std()), "hf_noise_stack": float(hp(st)[:200, :200].std())}))

if __name__ == "__main__":
    main()
