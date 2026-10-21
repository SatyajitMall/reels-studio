#!/usr/bin/env python3
"""Photo-print inserts: the character takes a picture, and the picture appears as a print on paper.

From "Two Sides of Bangkok": the host raises a compact camera, then 6 prints follow, 0.7 s each and cut on the beat,
portrait and landscape alternating, each on a plain off-white paper background with no frame. This renders that
sequence for a 9:16 reel: one ProRes 422 HQ clip (BT.709 tags) plus a sheet and timings.

  photos     stills or clip@seconds. Take them from a GRADED render (or the reel's look) so they match the film
  shape      cropped to camera-print shapes, 3:4 portrait and 3:2 landscape (--keep-aspect to skip)
  paper      off-white with a fine paper grain and a soft shadow under each print; --border adds a white print edge
  timing     --hold seconds for every print, or --durations 0.7,0.7,1.2 (beat-synced from analysis/beats.json)
  motion     static by default (as the reference); --settle drops each print in (104 % → 100 % over 5 frames);
             --tilt N alternates ±N° for a hand-laid look; --flash puts 2 white frames first (pair with the shutter SFX)
Place it on V4 in Normal mode, above the V3 look, so the paper stays neutral (CLAUDE.md §3). Sound: a shutter click
on the first frame (assets/sfx/gemini_camera_shutter.wav after sfx_prep.py).

Usage:
  ./.venv/bin/python scripts/photo_prints.py renders/exports/<reel>_v2.mp4@3.2 …@7.9 -o renders/fx/prints.mov --fps 25
  ./.venv/bin/python scripts/photo_prints.py stills/*.png -o renders/fx/prints.mov --durations 0.72,0.72,0.72,1.44 --settle --flash
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def grab(src: str, dst: Path) -> Image.Image:
    path, _, t = src.partition("@")
    if not t and Path(path).suffix.lower() in (".png", ".jpg", ".jpeg", ".tif", ".tiff"):
        return Image.open(path).convert("RGB")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *(["-ss", t] if t else []), "-i", path, "-frames:v", "1", str(dst)], check=True)
    return Image.open(dst).convert("RGB")


def to_print_shape(photo: Image.Image, portrait: float, landscape: float) -> Image.Image:
    """Centre-crop to a camera-print shape (3:4 portrait, 3:2 landscape by default). A 9:16 'print' reads as a phone screen."""
    want = landscape if photo.width >= photo.height else portrait
    have = photo.width / photo.height
    if abs(have - want) < 0.01:
        return photo
    if have > want:
        w = round(photo.height * want)
        x = (photo.width - w) // 2
        return photo.crop((x, 0, x + w, photo.height))
    h = round(photo.width / want)
    y = (photo.height - h) // 2
    return photo.crop((0, y, photo.width, y + h))


def paper(w: int, h: int, tone: tuple[int, int, int], seed: int = 7) -> Image.Image:
    rng = np.random.default_rng(seed)
    base = np.ones((h, w, 3), np.float32) * np.array(tone, np.float32)
    fibre = Image.fromarray((rng.normal(128, 40, (h // 2, w // 2))).clip(0, 255).astype(np.uint8)).resize((w, h)).filter(
        ImageFilter.GaussianBlur(1.2))
    base += (np.asarray(fibre, np.float32)[..., None] - 128) * 0.035          # fine grain, about ±1.5 levels
    yy, xx = np.mgrid[0:h, 0:w]
    vig = 1 - 0.05 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)  # very soft falloff
    return Image.fromarray((base * vig[..., None]).clip(0, 255).astype(np.uint8))


def place(bg: Image.Image, photo: Image.Image, scale: float, tilt: float, border: int, box: tuple[float, float]) -> Image.Image:
    W, H = bg.size
    bw, bh = W * box[0], H * box[1]
    r = min(bw / photo.width, bh / photo.height) * scale
    ph = photo.resize((max(1, round(photo.width * r)), max(1, round(photo.height * r))), Image.LANCZOS)
    if border:
        framed = Image.new("RGB", (ph.width + 2 * border, ph.height + 2 * border), (250, 249, 246))
        framed.paste(ph, (border, border))
        ph = framed
    mask = Image.new("L", ph.size, 255)
    if tilt:
        ph = ph.rotate(tilt, resample=Image.BICUBIC, expand=True)
        mask = mask.rotate(tilt, resample=Image.BICUBIC, expand=True)
    cx, cy = W // 2, round(H * 0.46)                                           # a little above centre: room for a subtitle
    x, y = cx - ph.width // 2, cy - ph.height // 2
    out = bg.copy()
    shadow = Image.new("L", (W, H), 0)
    shadow.paste(mask, (x, y + round(H * 0.006)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(H * 0.009))
    out = Image.composite(Image.new("RGB", (W, H), (60, 55, 50)), out, shadow.point(lambda v: int(v * 0.22)))
    out.paste(ph, (x, y), mask)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photos", nargs="+", help="stills or clip@seconds, in order")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--fps", type=float, default=25.0)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--hold", type=float, default=0.7, help="seconds per print (the reference: 0.7)")
    ap.add_argument("--durations", help="comma-separated seconds per print (overrides --hold)")
    ap.add_argument("--paper", default="239,237,232", help="paper tone R,G,B")
    ap.add_argument("--border", type=int, default=0, help="white print edge in px")
    ap.add_argument("--tilt", type=float, default=0.0, help="alternate ±N degrees per print")
    ap.add_argument("--settle", action="store_true", help="each print drops in 104 %% → 100 %% over 5 frames")
    ap.add_argument("--flash", action="store_true", help="2 white frames before the first print")
    ap.add_argument("--keep-aspect", action="store_true", help="don't crop photos to print shapes (3:4 / 3:2)")
    a = ap.parse_args()
    W, H = map(int, a.size.lower().split("x"))
    durs = [float(x) for x in a.durations.split(",")] if a.durations else [a.hold] * len(a.photos)
    if len(durs) != len(a.photos):
        sys.exit(f"{len(durs)} durations for {len(a.photos)} photos")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    bg = paper(W, H, tuple(int(v) for v in a.paper.split(",")))
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{a.fps:g}",
                           "-i", "-", "-vf", "format=yuv422p10le,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                           "-c:v", "prores_ks", "-profile:v", "3", "-color_primaries", "bt709", "-color_trc", "bt709",
                           "-colorspace", "bt709", "-movflags", "+write_colr", str(a.out)], stdin=subprocess.PIPE)
    timeline, frame_no, sheet = [], 0, []
    if a.flash:
        white = Image.new("RGB", (W, H), (255, 255, 255)).tobytes()
        for _ in range(2):
            ff.stdin.write(white)
        frame_no += 2
    with tempfile.TemporaryDirectory() as td:
        for i, (src, d) in enumerate(zip(a.photos, durs)):
            photo = grab(src, Path(td) / f"p{i}.png")
            if not a.keep_aspect:
                photo = to_print_shape(photo, 3 / 4, 3 / 2)
            landscape = photo.width >= photo.height
            box = (0.86, 0.50) if landscape else (0.70, 0.58)                  # landscape fills the width; portrait stays a print
            tilt = (a.tilt if i % 2 == 0 else -a.tilt) if a.tilt else 0.0
            n = max(1, round(d * a.fps))
            final = place(bg, photo, 1.0, tilt, a.border, box)
            for f in range(n):
                if a.settle and f < 5:
                    e = 1 - (1 - (f + 1) / 5) ** 3                             # ease-out
                    img = place(bg, photo, 1.04 - 0.04 * e, tilt, a.border, box)
                else:
                    img = final
                ff.stdin.write(img.tobytes())
            timeline.append({"photo": src, "start_s": round(frame_no / a.fps, 3), "frames": n, "orientation": "landscape" if landscape else "portrait"})
            frame_no += n
            sheet.append(final.resize((W // 4, H // 4)))
    ff.stdin.close()
    if ff.wait():
        sys.exit("ffmpeg failed")
    strip = Image.new("RGB", (sum(s.width for s in sheet), sheet[0].height))
    for i, s in enumerate(sheet):
        strip.paste(s, (i * s.width, 0))
    strip.save(a.out.with_name(a.out.stem + "_sheet.png"))
    a.out.with_suffix(".json").write_text(json.dumps({"out": str(a.out), "fps": a.fps, "size": [W, H], "flash": a.flash,
                                                      "settle": a.settle, "frames": frame_no, "prints": timeline}, indent=1))
    print(f"✓ {a.out}  {len(timeline)} prints, {frame_no} frames ({frame_no / a.fps:.2f} s)  sheet {a.out.stem}_sheet.png")


if __name__ == "__main__":
    main()
