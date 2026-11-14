"""v8 (reel-local, 2026-11-12): motion blur OUTSIDE the auto on shot 01, the director's note:
  "in first auto shot can we not add motion blur outside the auto? making it more cinematic"

Source: renders/stab_v3/STAB_v3d.mov frames 0-42 (01's stabilised material; the reel uses 4-42). Stored 2160x3840
(Premiere shows it with Rotation -90). The stabiliser holds the auto's interior and the driver still; the street moves.

  1. mask   the openings (windscreen, side openings) traced as polygons on the clip's median frame, minus the driver's
            silhouette (the dark region connected to his back, dilated 7 px), eroded, feathered. A statistical mask
            (temporal std) took in the pillars and left holes in the bus, so it was dropped. PNG + overlay sheet.
  2. blur   ffmpeg at half size (1080x1920 stored): minterpolate to 8 sub-frames per frame (motion-compensated), tmix over
            --sub sub-frames (8 = one frame interval = a 360° shutter; 32 = 4 frames), centred on each frame, back to 25 fps, scaled
            to 2160x3840. Smooth streaks, not stepped copies.
  3. merge  out = orig + mask x (blur - orig), per plane in the native yuv422p10le (chroma mask at chroma size), so the
            interior is bit-exact. ProRes 422 HQ, 43 frames, same size/orientation as STAB_v3d, so 01's in-point (4),
            Rotation, Scale/Position keys and Lumetri carry over unchanged.
Usage (reel folder): ../../.venv/bin/python tools/blur_01_v8.py mask|blur|merge|all [--sub 8]
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import scipy.ndimage as nd
from PIL import Image

SRC = "renders/stab_v3/STAB_v3d.mov"
N = 43                      # frames 0-42 hold 01
W, H = 2160, 3840           # stored
SCR = Path("/private/tmp/claude-503/-Users-SATYAJIT-MALL-Documents-reels-studio/38511ef6-44ef-4f27-9bc7-2168969c5ba6/scratchpad/blur01")
OUT = Path("renders/v8"); NOTES = Path("analysis/v8_notes")
SUB = int(sys.argv[sys.argv.index("--sub") + 1]) if "--sub" in sys.argv else 8


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


# The openings, traced on the clip's median frame, upright 960x540 coordinates (analysis/v8_notes/01_median_grid.jpg).
# The stabiliser holds the auto: its pillars drift ~10 px at this size over the clip, so the polygons keep that margin.
OPENINGS = [
    [(190, 150), (225, 128), (440, 112), (810, 112), (833, 133), (843, 172), (846, 350), (828, 366), (600, 366), (440, 340), (190, 312)],  # windscreen
    [(0, 118), (86, 124), (96, 140), (96, 330), (54, 362), (36, 540), (0, 540)],                                                       # left side
    [(938, 100), (960, 100), (960, 540), (944, 540), (938, 330)],                                                                         # right side
]


def make_mask():
    from PIL import ImageDraw
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", SRC, "-frames:v", str(N), "-vf", "scale=540:960", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    fr = np.frombuffer(b, np.uint8).reshape(-1, 960, 540, 3).astype(np.float32) / 255
    med = np.rot90(np.median(fr[4:N], 0), 1)                     # upright 540 x 960
    poly = Image.new("L", (960, 540), 0); d = ImageDraw.Draw(poly)
    for pts in OPENINGS: d.polygon(pts, fill=255)
    m = np.asarray(poly) > 0
    # the driver: the dark region connected to his back, from the median frame, with a margin
    lum = med @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    lab, _ = nd.label(lum < 0.22)
    drv = lab == lab[450, 330]
    drv = nd.binary_dilation(drv, disk(7))
    m &= ~drv
    lab2, n2 = nd.label(m)
    if n2:
        sizes = nd.sum(m, lab2, range(1, n2 + 1))
        m = np.isin(lab2, [i + 1 for i, s in enumerate(sizes) if s >= 800])
    soft = nd.gaussian_filter(nd.binary_erosion(m, disk(2)).astype(np.float32), 3)
    soft = np.clip(soft * 1.2, 0, 1)
    stored = np.rot90(soft, -1)                                   # back to stored 540 x 960
    Image.fromarray((stored * 255).astype(np.uint8)).save(SCR / "mask_540x960.png")
    tiles = []
    for k in (4, 23, 42):
        im = np.rot90(fr[k], 1); red = np.zeros_like(im); red[..., 0] = 1
        ov = im * (1 - 0.45 * soft[..., None]) + red * 0.45 * soft[..., None]
        tiles.append(np.concatenate([im, ov], 1))
    sheet = np.concatenate(tiles, 0)
    Image.fromarray((np.clip(sheet, 0, 1) * 255).astype(np.uint8)).save(NOTES / "01_blur_mask_overlay.jpg", quality=85)
    print("mask cover %.1f %%" % (100 * soft.mean()), NOTES / "01_blur_mask_overlay.jpg")


def make_blur():
    off = SUB // 2
    # tmix's window ends at sub-frame n, so the frame centred on source frame k is n = 8k + SUB/2
    vf = (f"trim=end_frame={N},tpad=stop_mode=clone:stop={SUB // 16 + 2},scale=1080:1920,format=yuv422p,"
          f"minterpolate=fps=200:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
          f"tmix=frames={SUB},select='gte(n\\,{off})*not(mod(n-{off}\\,8))',setpts=N/(25*TB),scale=2160:3840:flags=bicubic,format=yuv422p10le")
    out = SCR / f"blur_sub{SUB}.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-vf", vf, "-frames:v", str(N), "-c:v", "prores_ks", "-profile:v", "3", str(out)], check=True)
    print(out)


def read_planes(path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-frames:v", str(N), "-f", "rawvideo", "-pix_fmt", "yuv422p10le", "-"],
                         stdout=subprocess.PIPE)
    ny, nc = W * H, (W // 2) * H
    while True:
        buf = p.stdout.read((ny + 2 * nc) * 2)
        if len(buf) < (ny + 2 * nc) * 2:
            break
        a = np.frombuffer(buf, np.uint16)
        yield a[:ny].reshape(H, W), a[ny:ny + nc].reshape(H, W // 2), a[ny + nc:].reshape(H, W // 2)
    p.wait()


def merge():
    m = np.asarray(Image.open(SCR / "mask_540x960.png"), np.float32) / 255
    my = np.asarray(Image.fromarray(m).resize((W, H), Image.BILINEAR), np.float32)
    mc = np.asarray(Image.fromarray(m).resize((W // 2, H), Image.BILINEAR), np.float32)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"01_C049_blur_sub{SUB}.mov"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv422p10le", "-s", f"{W}x{H}", "-r", "25",
                            "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-i", "-",
                            "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(out)], stdin=subprocess.PIPE)
    n = 0; worst = 0
    for (y0, u0, v0), (y1, u1, v1) in zip(read_planes(SRC), read_planes(SCR / f"blur_sub{SUB}.mov")):
        planes = []
        for a, b, mm in ((y0, y1, my), (u0, u1, mc), (v0, v1, mc)):
            a = a.astype(np.float32); b = b.astype(np.float32)
            o = np.where(mm > 0, a + mm * (b - a), a)
            planes.append(np.clip(np.rint(o), 0, 1023).astype(np.uint16))
        enc.stdin.write(b"".join(p.tobytes() for p in planes)); n += 1
    enc.stdin.close(); enc.wait()
    print(out, n, "frames")


if __name__ == "__main__":
    SCR.mkdir(parents=True, exist_ok=True); NOTES.mkdir(parents=True, exist_ok=True)
    what = sys.argv[1]
    if what in ("mask", "all"): make_mask()
    if what in ("blur", "all"): make_blur()
    if what in ("merge", "all"): merge()
