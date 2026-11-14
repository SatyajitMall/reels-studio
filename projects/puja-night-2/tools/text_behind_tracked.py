#!/usr/bin/env python3
"""Reel-local variant of scripts/text_behind.py (puja-night-2 workaround, see CR-20261018-puja-night-2-motion-ai).

Differences from the studio script:
  - the word is anchored to the subject's own matte every frame (top of the subject, horizontal centre of
    its upper part), smoothed, so it rides with the subject on a hold that still drifts (C095 drifts up to
    ~60 px/s) instead of being fixed to the screen;
  - the word fades in and out inside the bake (--fade-in / --fade-out windows, seconds from clip start);
  - dark soft halo by default (this reel's brief), not the gold glow.

Usage:
  .venv/bin/python projects/puja-night-2/tools/text_behind_tracked.py <clip> --in 7.40 --dur 2.76 --text MAA \
      --size 420 --above 210 --fade-in 0.08 0.58 --fade-out 1.80 2.28 -o projects/puja-night-2/renders/behind/C095_MAA
Writes <out>.mov (ProRes 422 HQ, 25 fps, 1080x1920), <out>_compare.png and <out>_track.json.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 25
ROOT = Path(__file__).resolve().parents[3]


def frames(path: Path, pix: str, ch: int) -> np.ndarray:
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", pix, "-"],
                       capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, ch)


def smooth(v: np.ndarray, k: int = 7) -> np.ndarray:
    pad = np.pad(v, (k // 2, k // 2), mode="edge")
    return np.convolve(pad, np.ones(k) / k, mode="valid")


def ramp(t: float, a: float, b: float) -> float:
    return 0.0 if t <= a else 1.0 if t >= b else (t - a) / (b - a)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("--in", dest="in_s", type=float, required=True)
    ap.add_argument("--dur", type=float, required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--size", type=int, default=420)
    ap.add_argument("--above", type=int, default=210, help="word top = subject top minus this many px")
    ap.add_argument("--x-shift", type=int, default=0)
    ap.add_argument("--fade-in", type=float, nargs=2, default=[0.0, 0.5])
    ap.add_argument("--fade-out", type=float, nargs=2, default=[9e9, 9e9])
    ap.add_argument("--font", default="/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf")
    ap.add_argument("--color", default="#F5E6C8")
    ap.add_argument("--halo", default="#1A0F05")
    ap.add_argument("--halo-alpha", type=int, default=210)
    ap.add_argument("-o", "--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="tbt_") as td:
        tmp = Path(td)
        clip = tmp / "clip.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.in_s), "-t", str(a.dur), "-i", str(a.source), "-an",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                        "-c:v", "libx264", "-crf", "10", "-pix_fmt", "yuv420p", str(clip)], check=True)
        print("▸ cutting out the subject (CPU)…", flush=True)
        r = subprocess.run(["npx", "hyperframes", "remove-background", str(clip), "-o", str(tmp / "fg.mov"), "--device", "cpu"],
                           capture_output=True, text=True, cwd=tmp)
        if r.returncode or not (tmp / "fg.mov").exists():
            sys.exit(f"✗ remove-background failed:\n{(r.stdout + r.stderr)[-800:]}")
        base = frames(clip, "rgb24", 3)
        fg = frames(tmp / "fg.mov", "rgba", 4)
        n = min(len(base), len(fg))

        # Anchor per frame from the matte: subject top row and the centre of its upper 300 px.
        tops, cxs = [], []
        for i in range(n):
            al = fg[i, :, :, 3] > 128
            rows = np.where(al.sum(1) > 25)[0]
            top = int(rows[0]) if len(rows) else (tops[-1] if tops else H // 3)
            band = al[top:top + 300]
            xs = np.where(band.any(0))[0]
            cx = float(np.average(np.arange(W), weights=band.sum(0))) if band.sum() else (cxs[-1] if cxs else W / 2)
            tops.append(top); cxs.append(cx)
        tops_s, cxs_s = smooth(np.array(tops, float)), smooth(np.array(cxs, float))

        font = ImageFont.truetype(a.font, a.size)
        tw = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(a.text, font=font)
        rgb = tuple(int(a.color.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        hrgb = tuple(int(a.halo.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        out_png = tmp / "out"
        out_png.mkdir()
        for i in range(n):
            t = i / FPS
            alpha = ramp(t, *a.fade_in) * (1 - ramp(t, *a.fade_out))
            frame = Image.fromarray(base[i]).convert("RGBA")
            if alpha > 0:
                x, y = cxs_s[i] - tw / 2 + a.x_shift, tops_s[i] - a.above
                txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                ImageDraw.Draw(halo).text((x, y), a.text, font=font, fill=(*hrgb, a.halo_alpha))
                ImageDraw.Draw(txt).text((x, y), a.text, font=font, fill=(*rgb, 255))
                layer = Image.alpha_composite(halo.filter(ImageFilter.GaussianBlur(20)), txt)
                layer.putalpha(layer.split()[3].point(lambda v: int(v * alpha)))
                frame = Image.alpha_composite(frame, layer)
                frame = Image.alpha_composite(frame, Image.fromarray(fg[i]))
            frame.convert("RGB").save(out_png / f"f{i:04d}.png")
        mov = a.out.with_suffix(".mov")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", str(out_png / "f%04d.png"),
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(mov)], check=True)
        cmp_png = a.out.parent / (a.out.name + "_compare.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mov), "-vf", f"fps=4/{a.dur},scale=270:480,tile=4x1",
                        "-frames:v", "1", str(cmp_png)], check=True)
        json.dump({"frames": n, "top": tops, "cx": cxs, "top_smooth": tops_s.tolist(), "cx_smooth": cxs_s.tolist()},
                  open(a.out.with_name(a.out.name + "_track.json"), "w"))
    scan = subprocess.run([sys.executable, str(ROOT / "scripts" / "frame_scan.py"), str(mov), "-o", str(a.out.with_suffix(".scan.json"))],
                          capture_output=True, text=True).stdout.strip().splitlines()
    print(f"✓ {mov}  ({n} frames)\n  compare: {cmp_png}\n  scan: {scan[-1] if scan else '?'}")


if __name__ == "__main__":
    main()
