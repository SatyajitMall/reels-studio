"""Preview of the planned grade on stills (intent only; the real grade is Lumetri in Premiere).

Per frame: primary match toward one reel target (partial grey balance + exposure) -> one look
(warm film .cube mixed at --mix) -> natural depth (gentle S-curve with deeper shadows + highlight
roll-off, soft vignette, and where a person matte exists: mild background defocus + -0.15 stop
background falloff, feathered so there's no halo).
Usage: look_preview.py <raw_dir> <matte_dir> <out_dir> --lut assets/luts/x.cube [--mix 0.4]
"""
import argparse, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument("raw"); ap.add_argument("matte"); ap.add_argument("out")
ap.add_argument("--lut", required=True); ap.add_argument("--mix", type=float, default=0.4)
ap.add_argument("--target-luma", type=float, default=0.38)
ap.add_argument("--target-rb", default="1.06,0.90", help="target midtone R/G, B/G (slightly warm)")
ap.add_argument("--blur", type=float, default=5.0, help="background defocus sigma, px at 1080 wide")
a = ap.parse_args()
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
tr, tb = map(float, a.target_rb.split(","))

def luma(x): return 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]

def primary(img):
    y = luma(img); m = (y > 0.15) & (y < 0.85)
    r, g, b = (img[..., i][m].mean() for i in range(3))
    # partial (70 %) grey-balance toward the reel's slightly warm target
    gr = (tr * g / r) ** 0.7; gb = (tb * g / b) ** 0.7
    img = img * np.array([gr, 1.0, gb])
    # partial (60 %) exposure match toward target, in gamma space
    k = (a.target_luma / max(luma(img).mean(), 1e-3)) ** 0.6
    return np.clip(img * k, 0, 1)

def apply_lut(img, path):
    tmp = out / "_tmp_in.png"; tmp2 = out / "_tmp_lut.png"
    Image.fromarray((img * 255).astype(np.uint8)).save(tmp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-vf", f"lut3d=file={path}", str(tmp2)], check=True)
    lut = np.asarray(Image.open(tmp2).convert("RGB"), np.float32) / 255
    return img * (1 - a.mix) + lut * a.mix

def depth_grade(img):
    # gentle S: deeper shadows, roll off highlights (natural, not crushed)
    x = np.clip(img, 0, 1)
    x = np.where(x < 0.5, 0.5 * (2 * x) ** 1.12, 1 - 0.5 * (2 * (1 - x)) ** 1.12)
    x = 0.015 + x * 0.97          # keep a hint of black lift, soft white roll-off
    h, w = x.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.46) / (h / 2)) ** 2)
    vig = 1 - 0.22 * np.clip((d - 0.55) / 0.75, 0, 1) ** 1.6
    return np.clip(x * vig[..., None], 0, 1)

def defocus(img, alpha):
    a2 = ndimage.grey_dilation(alpha, size=(9, 9))          # protect the subject edge
    a2 = ndimage.gaussian_filter(a2, 6)                      # feather, no halo line
    bg = np.stack([ndimage.gaussian_filter(img[..., i], a.blur) for i in range(3)], -1) * 0.90  # ~ -0.15 stop falloff
    return img * a2[..., None] + bg * (1 - a2[..., None])

for f in sorted(Path(a.raw).glob("*.png")):
    img = np.asarray(Image.open(f).convert("RGB"), np.float32) / 255
    g = apply_lut(primary(img), a.lut)
    mp = Path(a.matte) / f.name
    if mp.exists():
        al = np.asarray(Image.open(mp).convert("RGBA"), np.float32)[..., 3] / 255
        if al.shape != g.shape[:2]:
            al = np.asarray(Image.fromarray((al * 255).astype(np.uint8)).resize((g.shape[1], g.shape[0])), np.float32) / 255
        if 0.02 < al.mean() < 0.6: g = defocus(g, al)
        else: print(f"  {f.name}: matte coverage {al.mean():.2f}, skipped defocus")
    g = depth_grade(g)
    Image.fromarray((g * 255).astype(np.uint8)).save(out / f.name)
    y0, y1 = luma(img).mean(), luma(g).mean()
    print(f"{f.name}: luma {y0:.3f} -> {y1:.3f}  matte={'yes' if mp.exists() else 'no'}")
for t in out.glob("_tmp_*"): t.unlink()
