#!/usr/bin/env python3
"""Remove a thin light band that crawls across a STATIC part of a locked-off shot (round 13, gate v13 loop 2: on C213 an LED's
rolling-shutter beat draws a teal line that drifts down the dark cabinet; it is in the camera original).
Inside a region (rows y0..y1, feathered), each pixel is replaced by its temporal median over a sliding window of `win` frames:
the band covers any one pixel for only a few frames, so the median keeps the static cabinet and drops the band. Outside the
region nothing changes. Only for regions with no real motion (check the result on consecutive frames).
--inpaint: instead, per frame, find rows where a thin teal stripe stands out (row-mean of (G+B)/2 - R above its 41-row running median)
and fill them by interpolating each column between the rows just above and below (works at any band speed).
Usage: band_remove.py <file n> <in suffix> <out suffix> --clip Cnnn --y0 1470 [--y1 1920] [--win 11] [--feather 40] [--inpaint [--thr 3]]
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
n, SIN, SOUT = sys.argv[1], sys.argv[2], sys.argv[3]
def opt(k, d): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
CLIP = opt("--clip", "*"); Y0, Y1 = int(opt("--y0", 1470)), int(opt("--y1", 1920)); WIN = int(opt("--win", 11)); FE = int(opt("--feather", 40))
js = next(R.glob(f"{int(n):02d}_{CLIP}_{SIN}.json")); r = json.loads(js.read_text()); src = R / r["file"]
W, H = 1080, 1920
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint16).reshape(-1, H, W, 3); N = len(F)
yy = np.arange(H, dtype=np.float32)[:, None, None]
wmap = (np.clip((yy - (Y0 - FE)) / FE, 0, 1) * np.clip(((Y1 + FE) - yy) / FE, 0, 1)) * np.ones((1, W, 1), np.float32)
if "--inpaint" not in sys.argv:
    reg = F[:, max(0, Y0 - FE):min(H, Y1 + FE)].astype(np.float32)
    med = ndimage.median_filter(reg, size=(WIN, 1, 1, 1), mode="nearest")
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-i", str(src),
                        "-map", "0:v", "-map", "1:a?", "-vf", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+write_colr", str(R / f"_tmp_band_{n}.mov")], stdin=subprocess.PIPE)
a, b = max(0, Y0 - FE), min(H, Y1 + FE); w = wmap[a:b]
INP = "--inpaint" in sys.argv; THR = float(opt("--thr", 3.0)); hits = 0
def inpaint(o, strips=int(opt("--strips", 8)), dil=6):
    """per column strip: rows where a teal stripe stands out of its 41-row running median get filled by vertical interpolation."""
    global hits
    reg = o[Y0:Y1]; teal = ((reg[..., 1] + reg[..., 2]) / 2 - reg[..., 0]) / 257.0; sw = W // strips
    for s in range(strips):
        c0, c1 = s * sw, (s + 1) * sw if s < strips - 1 else W
        prof = teal[:, c0:c1].mean(1); base = ndimage.median_filter(prof, size=41, mode="nearest")
        m = ndimage.binary_dilation((prof - base) > THR, iterations=dil); lab, nl = ndimage.label(m)
        for k in range(1, nl + 1):
            rows = np.where(lab == k)[0]; r0, r1 = rows[0] - 1, rows[-1] + 1
            if r0 < 0 or r1 >= len(prof) or (r1 - r0) > 70: continue
            top, bot = reg[r0, c0:c1].copy(), reg[r1, c0:c1].copy(); n_ = r1 - r0
            for j, r in enumerate(range(r0 + 1, r1), 1):
                reg[r, c0:c1] = top * (1 - j / n_) + bot * (j / n_)
            hits += 1
    o[Y0:Y1] = reg
    return o
for i in range(N):
    o = F[i].astype(np.float32)
    if INP: o = inpaint(o)
    else: o[a:b] = o[a:b] * (1 - w) + med[i] * w
    enc.stdin.write((o + 0.5).clip(0, 65535).astype(np.uint16).tobytes())
enc.stdin.close(); enc.wait()
name = js.name.replace(f"_{SIN}.json", f"_{SOUT}"); (R / f"_tmp_band_{n}.mov").rename(R / f"{name}.mov")
(R / f"{name}.json").write_text(json.dumps(dict(r, file=f"{name}.mov", band_remove={"y0": Y0, "y1": Y1, "win": WIN, "feather": FE, "inpaint": INP, "thr": THR, "bands_filled": hits}), indent=1))
print(f"✓ {name}: {N} frames, " + (f"inpainted {hits} band segments" if INP else f"temporal median {WIN}") + f" on rows {Y0}-{Y1}", flush=True)
