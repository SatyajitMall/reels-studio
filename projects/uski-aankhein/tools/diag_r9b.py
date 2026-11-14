#!/usr/bin/env python3
"""Review v9 #2/#3 diagnosis: shot B's still (C208 sharpest frame) as source (denoised, Lanczos) vs Real-ESRGAN, nose and crown.
Writes analysis/round5/r9b/b_still.json (still time + crop box) and b_nose_compare.jpg. Usage: python tools/diag_r9b.py"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R, bake_r7 as R7
B = R.B; OUT = REEL / "analysis/round5/r9b"
tr = R7.TRK["2"]; px = 235
t_s = R.sharpest_time(R7.C208, 0.2, 4.0, 0.533, 0.43); j = min(int(round(t_s * 30)), len(tr["ex"]) - 1)
ex, ey = tr["ex"][j], tr["ey"][j]; cw0 = R.CW(px, 0.42); box = tuple(round(v) for v in R.box_for(ex, ey, cw0))
src = next(B.frames(R7.C208, t_s, 1, False, R.W4, R.H4)); crop = src.crop(box); dn = R.denoise(crop)
big = R.ai_still(dn); plain = dn.resize(big.size, Image.LANCZOS)
dn.save(OUT / "b_crop_denoised.png"); big.save(OUT / "b_esrgan.png"); crop.save(OUT / "b_crop_raw.png")
(OUT / "b_still.json").write_text(json.dumps({"t_s": t_s, "ex": ex, "ey": ey, "box": box, "big": big.size}))
bw, bh = big.size
reg = lambda im: im.crop((int(.30 * bw), int(.45 * bh), int(.80 * bw), int(.68 * bh)))   # nose / mouth / right cheek
tiles = [reg(crop.resize(big.size, Image.NEAREST)), reg(plain), reg(big), reg(Image.blend(plain, big, 0.5))]
w, h = tiles[0].size; sheet = Image.new("RGB", (w * 2, h * 2))
for k, t in enumerate(tiles): sheet.paste(t, ((k % 2) * w, (k // 2) * h))
sheet.save(OUT / "b_nose_compare.jpg", quality=92); print(json.dumps({"t_s": t_s, "box": box, "big": big.size, "tile": (w, h)}))
