#!/usr/bin/env python3
"""Put a word BEHIND the subject of a shot (text occluded by the idol / person), locally and free.

How: cut the subject out of the shot with HyperFrames' `remove-background` (u2net_human_seg, CPU,
about 4 frames/s at 1080×1920), then stack footage → glowing text → subject cut-out.
Writes <out>.mov (ProRes 422 HQ, baked) plus <out>_compare.png (three frames) and runs
scripts/frame_scan.py on the result so matte flicker shows up as flags.

Verified on my-reel (2026-10-18):
  works    an idol or person in medium or close-up shot, against a contrasting background (blue Durga):
           clean matte, stable over 2 s of handheld footage, 0 scan flags
  weak     wide shots with a small subject (little to occlude)
  fails    busy, ornate full-frame close-ups (gold Durga): the matte turns to mush
The text is fixed to the screen, so use it on steady holds (scripts/motion_holds.py). On a moving
shot the subject drifts under the word. The model is trained on people; check every new subject type.

Usage:
  ./.venv/bin/python scripts/text_behind.py <source clip> --in 12.3 --dur 3.0 --text DURGA \
      -o projects/<reel>/renders/behind/s07_C011 [--y 640] [--x-shift 0] [--size 400] \
      [--font "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"] [--color "#F5E6C8"] [--glow "#D4A017"]
--y is the top of the text in 1080×1920 pixels. Put it so the word crosses the subject's head or shoulders
(about 30–55 % occluded), never over the face.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H = 1080, 1920


def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path)
    ap.add_argument("--in", dest="in_s", type=float, required=True)
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("-o", "--out", type=Path, required=True, help="output path without extension")
    ap.add_argument("--y", type=int, default=640)
    ap.add_argument("--x-shift", type=int, default=0)
    ap.add_argument("--size", type=int, default=400)
    ap.add_argument("--font", default="/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf")
    ap.add_argument("--color", default="#F5E6C8")
    ap.add_argument("--glow", default="#D4A017")
    args = ap.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="text_behind_") as tmpd:
        tmp = Path(tmpd)
        clip = tmp / "clip.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(args.in_s), "-t", str(args.dur), "-i", str(args.source),
                        "-an", "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-c:v", "libx264", "-crf", "12", str(clip)], check=True)
        print("▸ cutting out the subject (CPU)…", flush=True)
        r = subprocess.run(["npx", "hyperframes", "remove-background", str(clip), "-o", str(tmp / "fg.mov"), "--device", "cpu"],
                           capture_output=True, text=True, cwd=tmp)
        if r.returncode != 0 or not (tmp / "fg.mov").exists():
            sys.exit(f"✗ remove-background failed:\n{(r.stdout + r.stderr)[-800:]}")

        font = ImageFont.truetype(args.font, args.size)
        txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(txt)
        x = (W - d.textlength(args.text, font=font)) / 2 + args.x_shift
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(glow).text((x, args.y), args.text, font=font, fill=(*hex_rgb(args.glow), 200))
        d.text((x, args.y), args.text, font=font, fill=(*hex_rgb(args.color), 255))
        Image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(22)), txt).save(tmp / "text.png")

        mov = args.out.with_suffix(".mov")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(clip), "-loop", "1", "-i", str(tmp / "text.png"), "-i", str(tmp / "fg.mov"),
                        "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1[a];[a][2:v]overlay=0:0:format=auto",
                        "-t", str(args.dur), "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(mov)], check=True)
        cmp_png = args.out.parent / (args.out.name + "_compare.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mov), "-vf",
                        f"fps=3/{args.dur},scale=360:640,tile=3x1", "-frames:v", "1", str(cmp_png)], check=True)
    scan = subprocess.run([sys.executable, str(ROOT / "scripts" / "frame_scan.py"), str(mov), "-o", str(args.out.with_suffix(".scan.json"))],
                          capture_output=True, text=True).stdout.strip().splitlines()
    print(f"✓ {mov}\n  compare: {cmp_png}\n  scan: {scan[-1] if scan else '?'}")


if __name__ == "__main__":
    main()
