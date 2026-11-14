#!/usr/bin/env python3
"""Review v9 fixes (analysis/review_v9.md), v9b. Same structure and cut frames as bake_r7; only what the review found changes:
  A  #1 the esraj ghost sat down the centre of her face (neck between the eyes, fretting hand on her eye) and its white kurta
        veiled the whole shot (p10 0.20 vs 0.07 in B/C). Now the player sits left, as the reference: the layer is moved left/up,
        weighted by a left-to-right ramp with a soft hole over her eyes, then the black point and level are restored to B/C's.
  B  #2/#3 Real-ESRGAN drew the gold nath as a smear and gave the shola/silver a waxy, invented texture. Now AI 55 % over the
        plain denoised enlargement, AI 20 % over the nath.
  C  #5 the scaffold band (lower ~40 %) pulled the eye: a soft graduated darkening on the bottom of the frame.
  (#4 end card: moved up on V5, not baked.)
Output renders/bakes_r9b/V1_timeline_v9b.mov. Usage: python tools/bake_r9b.py [--only A,B,C] [--compose-only] [--test-A]
"""
import sys, json, argparse
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter1d
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R, bake_r7 as R7
B = R.B
OUT = REEL / "renders/bakes_r9b"
F_B, F_C, F_END = R.F_B, R.F_C, R.F_END
TGT_MEAN, TGT_P10 = 0.306, 0.072          # B/C pre-look bake means (mean 0.305/0.306, p10 0.074/0.069)

# --- A: singer placement (output px) and ghost weights
SING_DX, SING_DY, SING_SC = -380, -220, 1.0
SING_W = 0.78                              # peak Screen weight on the left; the ramp and the eye hole cut it over her face
RAMP_X0, RAMP_X1, RAMP_MIN = 0.26, 0.62, 0.30
FEATHER = 160                              # px: soft right / bottom edges of the moved layer
DEVEIL = 0.75                              # share of the ghost's low-frequency veil taken back out (keeps its lines and forms)
EYE_HOLE = (540, 768, 300, 150, 0.70)      # centre x, y, radius x, y, depth (her eyes at v .40)

def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

def ghost_mask():
    yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
    m = 1 - (1 - RAMP_MIN) * smoothstep(RAMP_X0 * 1080, RAMP_X1 * 1080, xx)
    cx, cy, rx, ry, d = EYE_HOLE
    m *= 1 - d * np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))
    return (SING_W * m)[..., None]

def place(im):
    """singer frame (PIL 1080x1920) scaled and moved onto a black canvas"""
    if SING_SC != 1.0: im = im.resize((round(1080 * SING_SC), round(1920 * SING_SC)), Image.LANCZOS)
    cv = Image.new("RGB", (1080, 1920)); ox = round((1080 - im.width) / 2 + SING_DX); oy = round((1920 - im.height) / 2 + SING_DY)
    cv.paste(im, (ox, oy)); return np.asarray(cv).astype(np.float32) / 255

def edge_feather():
    w, h = round(1080 * SING_SC), round(1920 * SING_SC)
    xr = (1080 - w) / 2 + SING_DX + w; yb = (1920 - h) / 2 + SING_DY + h
    yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32)
    return (smoothstep(0, FEATHER, xr - xx) * smoothstep(0, FEATHER, yb - yy))[..., None]

def veil(s):
    """low-frequency part of the ghost (sigma ~32 px), at quarter resolution for speed"""
    from scipy.ndimage import gaussian_filter, zoom
    q = s[::4, ::4]; q = np.stack([gaussian_filter(q[..., c], 8) for c in range(3)], -1)
    return zoom(q, (4, 4, 1), order=1)[:1920, :1080]

def a_base():
    """C163's sharpest frame, cropped and AI-upscaled once (cached: it is the v6-v9 base, unchanged)"""
    p = OUT / "A_big.png"; j = OUT / "A_big.json"
    if p.exists(): return Image.open(p).convert("RGB"), json.loads(j.read_text())
    tr = R.TRK["2"]; t_s = R.sharpest_time(R.C163, 0.0, 2.0, 0.4311, 0.4837)
    k = int(round(t_s * 30)); ex, ey = tr["ex"][min(k, len(tr["ex"]) - 1)], tr["ey"][min(k, len(tr["ey"]) - 1)]
    cw0 = R.CW(R.EYE163, 0.36); im = next(B.frames(R.C163, t_s, 1, False, R.W4, R.H4))
    big = R.ai_still(im.crop(tuple(round(v) for v in R.box_for(ex, ey, cw0)))); big.save(p)
    meta = {"t_s": t_s, "cw0": cw0, "cw1": R.CW(R.EYE163, 0.42)}; j.write_text(json.dumps(meta)); return big, meta

def shot_A(test=None):
    N = F_B; big, meta = a_base(); cw0, cw1 = meta["cw0"], meta["cw1"]
    gains = B.primary_params(R.push_from_big(big, cw0, cw0), wb=0.5, exp=R.PRIM163["exp"])
    sing = list(B.frames(R.SINGER, 0.0, N, False, 1080, 1920)); sing += [sing[-1]] * (N - len(sing))
    sg = B.primary_params(np.asarray(sing[N // 2]).astype(np.float32) / 255, wb=0.0, exp=0.0)
    M = ghost_mask() * edge_feather()
    def raw(k):
        cw = cw0 + (cw1 - cw0) * B.ease(k / (N - 1))
        x = B.halation(R.grade(R.push_from_big(big, cw0, cw), gains, R.PRIM163))
        s = np.clip(place(sing[k]) * sg * R.SING_GAIN, 0, 1) ** 1.2
        y = 1 - (1 - x) * (1 - M * s)                                        # Screen, weighted by the mask
        v = DEVEIL * M * veil(s)                                             # then the Screen's own inverse on the ghost's veil:
        return np.clip((y - v) / (1 - v), 0, 1)                              # lines and forms stay, the haze goes
    # one black point and one gain for the whole shot (no pumping): p10 and mean to B/C's
    smp = [raw(k) for k in range(0, N, 24)]
    p10 = float(np.median([np.percentile(B.luma(x), 10) for x in smp])); blk = max(p10 - TGT_P10, 0) / (1 - TGT_P10)
    lev = lambda x: np.clip((x - blk) / (1 - blk), 0, 1)
    mean = float(np.median([B.luma(lev(x)).mean() for x in smp])); g = TGT_MEAN / mean
    fix = lambda x: np.clip(lev(x) * g, 0, 1)
    if test:
        for k in test: Image.fromarray((fix(raw(k)) * 255 + 0.5).astype(np.uint8)).save(OUT / f"testA_{k:03d}.png")
        return {"blk": blk, "gain": g, "p10_raw": p10}
    enc = B.encoder(OUT / "A.mov", "rgb48le")
    for k in range(N): enc.stdin.write((fix(raw(k)) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "A", "frames": N, "blk": blk, "gain": g}

# --- B: AI share, global and over the nath (big-image px of the 2236x3980 AI still)
AI_MIX, AI_NATH = 0.55, 0.20
NATH = (1290, 1830, 330, 300)              # ellipse centre x, y, radius x, y: nose stud, chain to the right ear

def shot_B():
    N = F_C - F_B; tr = R7.TRK["2"]; px = 235; pr = dict(exp=-0.12)
    t_s = R.sharpest_time(R7.C208, 0.2, 4.0, 0.533, 0.43); j = min(int(round(t_s * 30)), len(tr["ex"]) - 1)
    ex, ey = tr["ex"][j], tr["ey"][j]; cw0, cw1 = R.CW(px, 0.42), R.CW(px, 0.54)
    im = next(B.frames(R7.C208, t_s, 1, False, R.W4, R.H4)).crop(tuple(round(v) for v in R.box_for(ex, ey, cw0)))
    dn = R.denoise(im); ai = R.ai_still(dn); plain = dn.resize(ai.size, Image.LANCZOS)
    yy, xx = np.mgrid[0:ai.height, 0:ai.width].astype(np.float32); cx, cy, rx, ry = NATH
    w = AI_MIX - (AI_MIX - AI_NATH) * np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) * 2.0)
    a = np.asarray(ai).astype(np.float32); p = np.asarray(plain).astype(np.float32)
    big = Image.fromarray(np.clip(p + (a - p) * w[..., None] + 0.5, 0, 255).astype(np.uint8))
    big.save(OUT / "B_big.png")
    gains = B.primary_params(R.push_from_big(big, cw0, cw0), wb=0.5, exp=pr["exp"])
    enc = B.encoder(OUT / "B.mov", "rgb48le")
    for k in range(N):
        f = k / (N - 1); cw = cw0 + (cw1 - cw0) * B.ease(f)
        x = R.push_from_big(big, cw0, cw, du=0.012 * (f - 0.5))
        x = B.halation(R.grade(x, gains, pr)); enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "B", "frames": N, "still_t": t_s, "ai_mix": AI_MIX, "ai_nath": AI_NATH}

# --- C: graduated darkening of the scaffold band
GRAD_Y0, GRAD_Y1, GRAD_MIN = 0.60, 1.00, 0.52

def shot_C():
    """v9's shot C unchanged (bake_r7.shot_C: live glide, deflicker, constant-speed hold), then the bottom grad."""
    yy = np.arange(1920, dtype=np.float32)[:, None, None] / 1920
    grad = 1 - (1 - GRAD_MIN) * smoothstep(GRAD_Y0, GRAD_Y1, yy)
    src = B.reader(REEL / "renders/bakes_r7/C.mov"); enc = B.encoder(OUT / "C.mov", "rgb48le"); n = 0
    for x in src: enc.stdin.write((np.clip(x * grad, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()); n += 1
    enc.stdin.close(); enc.wait(); return {"shot": "C", "frames": n, "grad": [GRAD_Y0, GRAD_Y1, GRAD_MIN]}

def compose():
    seq = [B.reader(OUT / "A.mov"), B.reader(OUT / "B.mov"), B.reader(OUT / "C.mov")]
    enc = B.encoder(OUT / "V1_timeline_v9b.mov", "rgb48le"); n = 0
    for t in range(550):
        if t >= F_END: x = np.zeros((1920, 1080, 3), np.float32)
        else:
            s = 0 if t < F_B else (1 if t < F_C else 2); x = R7.clarity(next(seq[s]))
            if t < 8: x = x * (t / 8)
            for c in (F_B, F_C):
                k = t - c
                if -3 <= k < 0: x = B.slit(x, B.BL_CLOSE[k + 3])
                elif k == 0: x = np.zeros_like(x)
                elif 1 <= k <= 3: x = B.slit(x, B.BL_OPEN[k - 1])
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print("V1_timeline_v9b.mov:", n, "frames")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default="A,B,C"); ap.add_argument("--compose-only", action="store_true")
    ap.add_argument("--test-A", action="store_true"); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.test_A: print(shot_A(test=[10, 60, 100, 150, 190])); return
    if not a.compose_only:
        for s in a.only.split(","): print({"A": shot_A, "B": shot_B, "C": shot_C}[s.strip()](), flush=True)
    compose()

if __name__ == "__main__":
    main()
