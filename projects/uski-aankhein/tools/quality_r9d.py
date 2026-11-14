#!/usr/bin/env python3
"""Quality pass options (director on v9c on iPhone: "very poor quality": soft, plastic faces, blocky darks, worse than on the Mac).
Per shot, three graded stills (the V3 cube applied, no grain or type) + 100 % crops of the eyes:
  NOW    v9c (single sharpest frame, nlmeans denoise, Real-ESRGAN, clarity .18)
  REAL   same framing; 21 aligned real frames averaged (tools/stack_r9d.py) instead of denoise + AI; fine sharpen; clarity .08
  WIDER  REAL, framed wider so the enlargement stays <= ~1.4x (eyes smaller in frame)
C (giant clay face) is a native downscale: REAL = no nlmeans; WIDER = same as REAL.
Writes analysis/ig/quality/options_<A|B|C>.jpg. Usage: python tools/quality_r9d.py
"""
import sys, json, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R, bake_r7 as R7, bake_r9b as R9, stack_r9d as S
B = R.B; OUT = REEL / "analysis/ig/quality"; CUBE = REEL / "grade/uski_aankhein_G2r_rich_deep.cube"

def look(x):
    with tempfile.TemporaryDirectory() as td:
        i, o = Path(td) / "i.png", Path(td) / "o.png"; Image.fromarray((np.clip(x, 0, 1) * 255 + .5).astype(np.uint8)).save(i)
        f = str(CUBE).replace(":", "\\:")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(i), "-vf", f"format=gbrp,lut3d=file='{f}',vignette=angle=0.42,format=rgb24", str(o)], check=True)
        return Image.open(o).convert("RGB")

def sharpen(x, r=1.0, p=55):
    im = Image.fromarray((np.clip(x, 0, 1) * 255 + .5).astype(np.uint8)).filter(ImageFilter.UnsharpMask(radius=r, percent=p, threshold=1))
    return np.asarray(im).astype(np.float32) / 255

def finish(x, gains, pr, amt): return look(R7.clarity(B.halation(R.grade(x, gains, pr)), amt=amt))

def shot_B(f=0.26):
    pr = dict(exp=-0.12); px = 235; c0, c1 = R.CW(px, 0.42), R.CW(px, 0.54); cw = c0 + (c1 - c0) * B.ease(f)
    big = Image.open(REEL / "renders/bakes_r9b/B_big.png").convert("RGB")
    g = B.primary_params(R.push_from_big(big, c0, c0), wb=0.5, exp=pr["exp"])
    now = finish(R.push_from_big(big, c0, cw), g, pr, .18)
    st, _, _ = S.stack(R7.C208, R7.TRK["2"], 0.8, c0, 21); sb = Image.fromarray((np.clip(st, 0, 1) * 255 + .5).astype(np.uint8))
    real = finish(sharpen(R.push_from_big(sb, c0, cw)), g, pr, .08)
    w0 = R.CW(px, 0.30); stw, _, _ = S.stack(R7.C208, R7.TRK["2"], 0.8, w0, 21); sw = Image.fromarray((np.clip(stw, 0, 1) * 255 + .5).astype(np.uint8))
    wider = finish(sharpen(R.push_from_big(sw, w0, w0)), g, pr, .08)
    return now, real, wider, {"now_enlarge": round(1080 / (px / (0.42 + 0.12 * B.ease(f))), 2), "wider_enlarge": round(1080 / (px / 0.30), 2)}

def shot_A():
    big, meta = R9.a_base(); c0, c1 = meta["cw0"], meta["cw1"]; pr = R.PRIM163
    g = B.primary_params(R.push_from_big(big, c0, c0), wb=0.5, exp=pr["exp"])
    now = finish(R.push_from_big(big, c0, c0), g, pr, .18)
    st, _, _ = S.stack(R.C163, R.TRK["2"], meta["t_s"], c0, 21); sb = Image.fromarray((np.clip(st, 0, 1) * 255 + .5).astype(np.uint8))
    real = finish(sharpen(R.push_from_big(sb, c0, c0)), g, pr, .08)
    w0 = R.CW(R.EYE163, 0.28); stw, _, _ = S.stack(R.C163, R.TRK["2"], meta["t_s"], w0, 21); sw = Image.fromarray((np.clip(stw, 0, 1) * 255 + .5).astype(np.uint8))
    wider = finish(sharpen(R.push_from_big(sw, w0, w0)), g, pr, .08)
    return now, real, wider, {"now_enlarge": round(1080 / (R.EYE163 / 0.36), 2), "wider_enlarge": round(1080 / (R.EYE163 / 0.28), 2)}

def shot_C(j=20):
    tr = R7.TRK["3"]; n_live = 36; N = R.F_END - R.F_C; px = 800
    ex = B.smooth(tr["ex"][:n_live], 3.0); ey = B.smooth(tr["ey"][:n_live], 3.0); c0, c1 = R.CW(px, 0.60), R.CW(px, 0.72)
    cw = c0 + (c1 - c0) * B.ease(j / (N - 1)); src = list(B.frames(R7.C162, 5.77, j + 1, False, R.W4, R.H4))[-1]
    crop = src.crop(tuple(round(v) for v in R.box_for(ex[j], ey[j], cw)))
    raw = np.asarray(crop.resize((1080, 1920), Image.LANCZOS)).astype(np.float32) / 255
    dn = np.asarray(R.denoise(crop).resize((1080, 1920), Image.LANCZOS)).astype(np.float32) / 255
    g = B.primary_params(dn, wb=0.5, exp=0.0)
    now = finish(dn, g, {}, .18); real = finish(raw, g, {}, .08)
    return now, real, real, {"now_enlarge": round(1080 / (px / 0.60), 2)}

def sheet(name, ims, crop):
    lab = ["NOW (v9c)", "REAL frames, same framing", "REAL + WIDER"]
    from PIL import ImageDraw, ImageFont
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    s = Image.new("RGB", (3 * 560, 60 + 960 + 20 + 560), (16, 16, 16)); d = ImageDraw.Draw(s)
    for i, (im, l) in enumerate(zip(ims, lab)):
        d.text((i * 560 + 8, 14), l, font=f, fill=(255, 215, 120)); s.paste(im.resize((540, 960), Image.LANCZOS), (i * 560, 60))
        s.paste(im.crop(crop), (i * 560, 60 + 960 + 20))                      # 100 % crop (540 x 560) around the eyes
    s.save(OUT / f"options_{name}.jpg", quality=92)

def main():
    eyes = (270, 520, 810, 1080)
    for name, fn in (("B", shot_B), ("A", shot_A), ("C", shot_C)):
        now, real, wider, info = fn(); sheet(name, (now, real, wider), eyes); print(name, info, flush=True)

if __name__ == "__main__":
    main()
