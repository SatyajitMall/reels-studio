"""v9 (reel-local, 2026-11-12): the director on v8b's auto blur, with a reference image (a car interior, the city streaking
past in long radial light trails): "I was talking this kind of motion graphic in the auto frames."

A ZOOM (radial) blur outside the auto: streaks radiate from the point the auto is heading for, as if it's racing forward.
  - Source: renders/stab_v3/STAB_v3d.mov frames 0-42 (01's stabilised material; the reel uses 4-42), stored 2160x3840,
    shown in Premiere at Rotation -90. Processing is done upright at half size (1920x1080).
  - Mask: the openings traced for v8 (tools/blur_01_v8.py; scratch mask_540x960.png), minus the driver.
  - Normalised radial blur in linear light: only outside pixels feed the streaks (sum of mask*image / sum of mask over the
    zoom samples), so the pillars, roof and driver never smear into the street, and lights keep their energy.
    Recursive doubling: pass p averages the image with itself zoomed by (1+D)^(2^p) about the vanishing point, P passes
    = 2^P samples, up to (1+D)^(2^P - 1).
  - Back to gamma, to stored orientation, up to 2160x3840, yuv422p10le (bt709, tv), then merged into the original inside the
    mask exactly as v8 (native planes, interior untouched).
  - Light trails (--trail k): the highlights above --thr (linear) get the same zoom streak and are added back x k, so
    lamps and tail lights become glowing trails like the reference.
Usage (reel folder): ../../.venv/bin/python tools/zoomblur_v9.py [--vp 500,240] [--d 0.012] [--passes 5] [--trail 0] [--thr 0.35] [--tag a]
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
import scipy.ndimage as nd
from PIL import Image

SRC = "renders/stab_v3/STAB_v3d.mov"
N = 43
SCR = Path("/private/tmp/claude-503/-Users-SATYAJIT-MALL-Documents-reels-studio/38511ef6-44ef-4f27-9bc7-2168969c5ba6/scratchpad/blur01")
OUT = Path("renders/v9")


def arg(name, default, cast=float):
    return cast(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


VP = tuple(float(v) for v in arg("--vp", "500,240", str).split(","))   # upright 960x540 coordinates
D, PASSES, GAIN, TAG = arg("--d", 0.012), arg("--passes", 5, int), arg("--gain", 1.0), arg("--tag", "a", str)
TRAIL, THR = arg("--trail", 0.0), arg("--thr", 0.35)   # light trails: highlights above THR (linear) streaked again and added x TRAIL
UW, UH = 1920, 1080                                      # upright working size
MIRRORS = [(14, 132, 128, 278), (892, 112, 960, 292)]   # left / right mirror housings, upright 960x540 (01_median_grid.jpg)
vx, vy = VP[0] * 2, VP[1] * 2


def zoom(a, s):
    """Sample a (H, W[, C]) at VP + (p - VP) / s: content moves outward from the vanishing point by factor s."""
    m = np.array([1 / s, 1 / s]); off = np.array([vy - vy / s, vx - vx / s])
    if a.ndim == 2:
        return nd.affine_transform(a, m, offset=off, order=1, mode="nearest")
    return np.stack([nd.affine_transform(a[..., c], m, offset=off, order=1, mode="nearest") for c in range(a.shape[2])], -1)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m_st = np.asarray(Image.open(SCR / "mask_540x960.png"), np.float32) / 255       # stored 540 wide x 960 tall
    m_up = np.ascontiguousarray(np.rot90(m_st, 1))                                    # upright 540 x 960
    # the mirror housings belong to the auto: keep them sharp and out of the streaks (upright 960x540 boxes + margin)
    from PIL import ImageDraw
    cut = Image.new("L", (960, 540), 0); dc = ImageDraw.Draw(cut)
    for box in MIRRORS: dc.rectangle(box, fill=255)
    cut = nd.gaussian_filter(np.asarray(cut, np.float32) / 255, 3)
    m_up = m_up * (1 - np.clip(cut * 1.5, 0, 1))
    m_st = np.ascontiguousarray(np.rot90(m_up, -1))
    M = np.asarray(Image.fromarray(np.ascontiguousarray(m_up)).resize((UW, UH), Image.BILINEAR), np.float32)
    hard = (M > 0.02).astype(np.float32)                                             # which pixels may feed the streaks
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-frames:v", str(N), "-vf",
                            "scale=1080:1920:in_color_matrix=bt709:in_range=tv,format=rgb48le", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    blurfile = SCR / f"zoom_{TAG}.mov"
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", "1080x1920", "-r", "25", "-i", "-",
                            "-vf", "scale=2160:3840:flags=bicubic:out_color_matrix=bt709:out_range=tv,format=yuv422p10le",
                            "-c:v", "prores_ks", "-profile:v", "3", "-color_range", "tv", "-colorspace", "bt709",
                            "-color_primaries", "bt709", "-color_trc", "bt709", str(blurfile)], stdin=subprocess.PIPE)
    fb = 1080 * 1920 * 3 * 2; n = 0
    while True:
        buf = dec.stdout.read(fb)
        if len(buf) < fb:
            break
        st = np.frombuffer(buf, np.uint16).reshape(1920, 1080, 3).astype(np.float32) / 65535
        up = np.rot90(st, 1)                                                      # upright 1080 x 1920
        lin = np.power(up, 2.2)
        num = lin * hard[..., None]; den = hard.copy()
        hl = np.maximum(lin - THR, 0) * hard[..., None] if TRAIL > 0 else None
        for p in range(PASSES):
            s = (1 + D) ** (2 ** p)
            num = 0.5 * (num + zoom(num, s)); den = 0.5 * (den + zoom(den, s))
            if hl is not None: hl = 0.5 * (hl + zoom(hl, s))
        out = np.where(den[..., None] > 1e-3, num / np.maximum(den[..., None], 1e-3), lin) * GAIN
        if hl is not None:
            out = out + TRAIL * hl / np.maximum(den[..., None], 0.05)
        g = np.power(np.clip(out, 0, 1), 1 / 2.2)
        back = np.rot90(g, -1)                                                    # stored 1920 tall x 1080 wide
        enc.stdin.write((np.clip(back, 0, 1) * 65535 + 0.5).astype(np.uint16).tobytes()); n += 1
    enc.stdin.close(); enc.wait(); dec.wait()
    print(blurfile, n, "frames; vp", VP, "d", D, "passes", PASSES, "max zoom %.3f" % ((1 + D) ** (2 ** PASSES - 1)))
    # merge into the full-size original inside the mask (native planes), as v8
    sys.argv = [sys.argv[0], "merge"]
    import importlib.util
    spec = importlib.util.spec_from_file_location("b01", str(Path(__file__).parent / "blur_01_v8.py")); b01 = importlib.util.module_from_spec(spec); spec.loader.exec_module(b01)
    b01.OUT = OUT
    src_blur = blurfile
    W, H = b01.W, b01.H
    my = np.asarray(Image.fromarray(m_st).resize((W, H), Image.BILINEAR), np.float32)
    mc = np.asarray(Image.fromarray(m_st).resize((W // 2, H), Image.BILINEAR), np.float32)
    out = OUT / f"01_C049_zoom_{TAG}.mov"
    enc2 = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv422p10le", "-s", f"{W}x{H}", "-r", "25",
                             "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-i", "-",
                             "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(out)], stdin=subprocess.PIPE)
    k = 0
    for (y0, u0, v0), (y1, u1, v1) in zip(b01.read_planes(SRC), b01.read_planes(src_blur)):
        planes = []
        for a, b, mm in ((y0, y1, my), (u0, u1, mc), (v0, v1, mc)):
            a = a.astype(np.float32); b = b.astype(np.float32)
            planes.append(np.clip(np.rint(np.where(mm > 0, a + mm * (b - a), a)), 0, 1023).astype(np.uint16))
        enc2.stdin.write(b"".join(p.tobytes() for p in planes)); k += 1
    enc2.stdin.close(); enc2.wait()
    print(out, k, "frames")


if __name__ == "__main__":
    main()
