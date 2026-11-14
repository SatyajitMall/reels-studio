"""Cover options for the Instagram package (reel-local, Phase 8, v4f).

instagram-strategy.md: the profile grid shows a 3:4 crop of the cover (y 240-1680 on 1080x1920), and a frame from a
windowed reel shows the black band there, so the cover is a full 9:16 picture from the camera file (here the Apple
Cinematic bake, the director's depth) with the reel's grade and title.

Grade: per-channel CDF match of the bake frame to the reel's own render of the same moment (inside the 4:3 window),
so the cover carries the per-clip balance and the roti look exactly as the reel shows them (no second grade by hand).
Title: the reel's type (make_type_v4d.py, Kolkata family): Amita Bold + Eczar SemiBold caps, cream, glow + shadow.

Decoding goes to raw RGB (ffmpeg -noautorotate): ffmpeg's PNG output carries the clips' display-matrix rotation and
re-reads come back sideways.
Usage (reel folder): ../../.venv/bin/python tools/make_cover_v4f.py
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from make_type_v4d import CREAM, compose, font, width  # noqa: E402

MASTER = "renders/masters/could-not-go-home-diwali_v5b_master.mov"   # 4:3 window grade reference (same grade as v6)
WIN = (0, 505, 1080, 810)
# name, bake, bake frame, reel frame, crop centre x (0-1 of 3840), title block top y (cover px)
OPTS = [
    ("A_paan", "raw/baked/C051_f2_00.00.mov", 25, 535, 0.49, 1230),
    ("B_vendor", "raw/baked/v4/C062_f4_03.60.mov", 35, 380, 0.40, 1230),   # 10's f/4 bake (camera 5.0 s)
]
TITLE = [("Maa, is baar ghar", "AVENIR", 80, 0, CREAM, 0),          # v6: Hinglish only, Avenir Next Medium (director 2026-11-12)
         ("nahi aa paaunga.", "AVENIR", 80, 0, CREAM, 14)]


def raw(path, n, w, h):
    """One frame as float RGB 0-1, decoded at 16 bit (smooth curves, no 8-bit steps)."""
    b = subprocess.run(["ffmpeg", "-v", "error", "-noautorotate", "-i", path, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
    if len(b) != w * h * 6:
        raise SystemExit(f"{path} frame {n}: got {len(b)} bytes")
    return np.frombuffer(b, "<u2").reshape(h, w, 3).astype(np.float32) / 65535


def cdf_match(src, ref, sample, knots=24):
    """Per channel: a smooth monotone curve through matched quantiles (sample → ref), applied to src in float.
    sample = the camera region the reel's window shows, so the curve is fitted like for like (fitting on the cover
    crop itself pushed the skin red). Coarse knots keep it a grade-like curve; a per-value CDF contoured the shirt."""
    q = np.linspace(0, 1, knots)
    out = np.empty_like(src)
    for c in range(3):
        sq = np.quantile(sample[..., c], q); rq = np.quantile(ref[..., c], q)
        sq = np.maximum.accumulate(sq + np.arange(knots) * 1e-6)
        out[..., c] = np.interp(src[..., c], sq, rq)
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)


def title_layer(y0):
    rows, y = [], y0
    for t, fn, size, tr, col, gap in TITLE:
        mk = (lambda sz: ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", sz, index=5)) if fn == "AVENIR" else (lambda sz: font(fn, sz, "SemiBold" if "Eczar" in fn else None))
        f = mk(size)
        while width(t, f, tr) > 840:
            f = mk(f.size - 2)
        y += gap; bb = f.getbbox(t)
        rows.append((t, f, tr, col, 540 - width(t, f, tr) / 2, y - bb[1])); y += bb[3] - bb[1]
    return compose(rows, None), y


def main():
    out = Path("deliver"); out.mkdir(exist_ok=True)
    notes = Path("analysis/ig_v4f"); notes.mkdir(parents=True, exist_ok=True)
    sheet = []
    for name, bake, bn, rn, cx, ty in OPTS:
        cam = raw(bake, bn, 3840, 2160)
        ren = raw(MASTER, rn, 1080, 1920)[WIN[1]:WIN[1] + WIN[3]]
        cw = round(2160 * 9 / 16)
        x0 = int(min(max(cx * 3840 - cw / 2, 0), 3840 - cw))
        crop = cam[:, x0:x0 + cw]
        # match on the camera region the reel's window shows (75 % of the width, centred on the shot's framing)
        sample = cam[86:2074, 576:3264]   # ~70 % x 92 %: the window at the shots' stabilised framing
        graded = cdf_match(crop, ren, sample)
        img = Image.fromarray(graded).resize((1080, 1920), Image.LANCZOS).convert("RGBA")
        layer, yb = title_layer(ty)
        img = Image.alpha_composite(img, layer).convert("RGB")
        img.save(out / f"cover_{name}.jpg", quality=93)
        g = img.copy(); d = ImageDraw.Draw(g)
        for yy in (240, 1680):
            d.line((0, yy, 1080, yy), fill=(255, 80, 80), width=5)
        sheet.append(g.resize((405, 720), Image.LANCZOS))
        print(name, "crop x", x0, "title bottom", round(yb))
    S = Image.new("RGB", (len(sheet) * 415, 720), (20, 20, 20))
    for i, t in enumerate(sheet):
        S.paste(t, (i * 415, 0))
    S.save(notes / "cover_options.jpg", quality=90)
    print("wrote deliver/cover_*.jpg and", notes / "cover_options.jpg")


if __name__ == "__main__":
    main()
