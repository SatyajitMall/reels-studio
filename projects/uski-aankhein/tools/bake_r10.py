#!/usr/bin/env python3
"""v10 quality pass (director on the v9c file on iPhone: "very poor quality": soft, plastic faces, blocky darks; picked
"Real frames + wider"). Same structure, cuts, blinks, ghost and title plate as v9c; what changes:
  A, B  the base is a stack of 21 aligned real source frames (tools/stack_r9d.py) instead of one frame + nlmeans + Real-ESRGAN,
        with a fine unsharp at output size; framed wider so the enlargement stays <= ~1.4x
        (A eye pair 27 -> 31 % of the width, was 36 -> 42 %; B 26 -> 31 %, was 42 -> 54 %).
  C     same framing (a native downscale); the nlmeans denoise now only in the shadows, so the clay keeps its texture.
  all   clarity 0.08 (was 0.18).
Output renders/bakes_r10/V1_timeline_v10.mov. Usage: python tools/bake_r10.py [--only A,B,C] [--compose-only]
"""
import sys, json, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import uniform_filter1d, gaussian_filter, zoom
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R, bake_r7 as R7, bake_r9b as R9, bake_r9c as R9C, stack_r9d as S
B = R.B
OUT = REEL / "renders/bakes_r10"
F_B, F_C, F_END = R.F_B, R.F_C, R.F_END
CLARITY = 0.08
A_SPAN, B_SPAN = (0.27, 0.31), (0.26, 0.31)      # eye pair as a fraction of the output width, start -> end of the push
N_STACK = 21

def sharpen(x, r=1.0, p=55):
    im = Image.fromarray((np.clip(x, 0, 1) * 255 + .5).astype(np.uint8)).filter(ImageFilter.UnsharpMask(radius=r, percent=p, threshold=1))
    return np.asarray(im).astype(np.float32) / 255

def stacked(src, track, t_s, cw0, tag):
    p = OUT / f"{tag}_stack.png"
    if p.exists(): return Image.open(p).convert("RGB")
    st, _, sh = S.stack(src, track, t_s, cw0, N_STACK); im = Image.fromarray((np.clip(st, 0, 1) * 255 + .5).astype(np.uint8))
    im.save(p); (OUT / f"{tag}_stack.json").write_text(json.dumps({"t_s": t_s, "cw0": cw0, "n": N_STACK, "shifts": sh})); return im

def shot_A():
    N = F_B; t_s = json.loads((REEL / "renders/bakes_r9b/A_big.json").read_text())["t_s"]
    c0, c1 = R.CW(R.EYE163, A_SPAN[0]), R.CW(R.EYE163, A_SPAN[1]); base = stacked(R.C163, R.TRK["2"], t_s, c0, "A")
    gains = B.primary_params(R.push_from_big(base, c0, c0), wb=0.5, exp=R.PRIM163["exp"])
    sing = list(B.frames(R.SINGER, 0.0, N, False, 1080, 1920)); sing += [sing[-1]] * (N - len(sing))
    sg = B.primary_params(np.asarray(sing[N // 2]).astype(np.float32) / 255, wb=0.0, exp=0.0)
    M = R9.ghost_mask() * R9.edge_feather()
    def raw(k):
        cw = c0 + (c1 - c0) * B.ease(k / (N - 1))
        x = B.halation(R.grade(sharpen(R.push_from_big(base, c0, cw)), gains, R.PRIM163))
        s = np.clip(R9.place(sing[k]) * sg * R.SING_GAIN, 0, 1) ** 1.2
        y = 1 - (1 - x) * (1 - M * s); v = R9.DEVEIL * M * R9.veil(s)
        return np.clip((y - v) / (1 - v), 0, 1)
    smp = [raw(k) for k in range(0, N, 24)]
    p10 = float(np.median([np.percentile(B.luma(x), 10) for x in smp])); blk = max(p10 - R9.TGT_P10, 0) / (1 - R9.TGT_P10)
    lev = lambda x: np.clip((x - blk) / (1 - blk), 0, 1)
    g = R9.TGT_MEAN / float(np.median([B.luma(lev(x)).mean() for x in smp]))
    enc = B.encoder(OUT / "A.mov", "rgb48le")
    for k in range(N): enc.stdin.write((np.clip(lev(raw(k)) * g, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "A", "frames": N, "span": A_SPAN, "enlarge": [round(1080 * s / R.EYE163, 2) for s in A_SPAN], "blk": blk, "gain": g}

def shot_B():
    N = F_C - F_B; pr = dict(exp=-0.12); px = 235
    c0, c1 = R.CW(px, B_SPAN[0]), R.CW(px, B_SPAN[1]); base = stacked(R7.C208, R7.TRK["2"], 0.8, c0, "B")
    gains = B.primary_params(R.push_from_big(base, c0, c0), wb=0.5, exp=pr["exp"])
    enc = B.encoder(OUT / "B.mov", "rgb48le")
    for k in range(N):
        f = k / (N - 1); cw = c0 + (c1 - c0) * B.ease(f)
        x = B.halation(R.grade(sharpen(R.push_from_big(base, c0, cw, du=0.012 * (f - 0.5))), gains, pr))
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "B", "frames": N, "span": B_SPAN, "enlarge": [round(1080 * s / px, 2) for s in B_SPAN]}

def shadow_mix(raw, dn):
    """nlmeans only where it is dark (luma < ~0.25), the source's own texture elsewhere"""
    w = R9.smoothstep(0.28, 0.06, B.luma(raw))[..., None]; return raw * (1 - w) + dn * w

def shot_C():
    """bake_r7.shot_C (live glide, eye-locked, then held under a constant push), with the denoise in the shadows only, the global
    + regional deflicker (bake_r9c) and the bottom grad + corner (bake_r9c)."""
    N = F_END - F_C; tr = R7.TRK["3"]; n_live = R9C.N_LIVE; px = 800
    ex = B.smooth(tr["ex"][:n_live], 3.0); ey = B.smooth(tr["ey"][:n_live], 3.0)
    c0, c1 = R.CW(px, 0.60), R.CW(px, 0.72); cwk = lambda k: c0 + (c1 - c0) * B.ease(k / (N - 1))
    src = list(B.frames(R7.C162, 5.77, n_live, False, R.W4, R.H4))
    up = lambda im: np.asarray(im.resize((1080, 1920), Image.LANCZOS)).astype(np.float32) / 255
    live = []
    for j in range(n_live):
        cr = src[j].crop(tuple(round(v) for v in R.box_for(ex[j], ey[j], cwk(j)))); live.append(shadow_mix(up(cr), up(R.denoise(cr))))
    hold_cw = cwk(n_live); big = src[-1].crop(tuple(round(v) for v in R.box_for(ex[-1], ey[-1], hold_cw))); big_dn = R.denoise(big)
    Lf = np.array([float(B.luma(x[600:1300, 240:840]).mean()) for x in live]); dg = uniform_filter1d(Lf, 9, mode="nearest") / np.maximum(Lf, 1e-4)
    live = [np.clip(x * d, 0, 1) for x, d in zip(live, dg)]
    lo = np.stack([gaussian_filter(B.luma(x).reshape(1920 // R9C.BLK, R9C.BLK, 1080 // R9C.BLK, R9C.BLK).mean((1, 3)), 1.5) for x in live])
    fields = uniform_filter1d(lo, 9, axis=0, mode="nearest") / np.maximum(lo, 1e-4); upf = lambda m: zoom(m, R9C.BLK, order=1)[..., None]
    gains = B.primary_params(live[n_live // 2], wb=0.5, exp=0.0)
    yy, xx = np.mgrid[0:1920, 0:1080].astype(np.float32); yy /= 1920; xx /= 1080
    grad = 1 - (1 - R9.GRAD_MIN) * R9.smoothstep(R9.GRAD_Y0, R9.GRAD_Y1, yy)
    y0, y1, x0, x1, d = R9C.CORNER; grad = (grad * (1 - d * R9.smoothstep(y0, y1, yy) * R9.smoothstep(x0, x1, xx)))[..., None]
    last = upf(fields[-1]); enc = B.encoder(OUT / "C.mov", "rgb48le")
    for k in range(N):
        if k < n_live: x = live[k] * upf(fields[k])
        else:
            cw = hold_cw + (c1 * 0.97 - hold_cw) * (k - n_live + 1) / (N - n_live)
            x = shadow_mix(R.push_from_big(big, hold_cw, cw), R.push_from_big(big_dn, hold_cw, cw)) * dg[-1] * last
        x = B.halation(R.grade(np.clip(x, 0, 1), gains, {})) * grad
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "C", "frames": N, "live": n_live}

def compose():
    seq = [B.reader(OUT / "A.mov"), B.reader(OUT / "B.mov"), B.reader(OUT / "C.mov")]
    enc = B.encoder(OUT / "V1_timeline_v10.mov", "rgb48le"); n = 0
    for t in range(550):
        if t >= F_END: x = np.zeros((1920, 1080, 3), np.float32)
        else:
            s = 0 if t < F_B else (1 if t < F_C else 2); x = R7.clarity(next(seq[s]), amt=CLARITY)
            p = R9C.plate(t)
            if p is not None: x = x * p
            if t < 8: x = x * (t / 8)
            for c in (F_B, F_C):
                k = t - c
                if -3 <= k < 0: x = B.slit(x, B.BL_CLOSE[k + 3])
                elif k == 0: x = np.zeros_like(x)
                elif 1 <= k <= 3: x = B.slit(x, B.BL_OPEN[k - 1])
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print("V1_timeline_v10.mov:", n, "frames")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default="A,B,C"); ap.add_argument("--compose-only", action="store_true"); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not a.compose_only:
        for s in a.only.split(","): print({"A": shot_A, "B": shot_B, "C": shot_C}[s.strip()](), flush=True)
    compose()

if __name__ == "__main__":
    main()
