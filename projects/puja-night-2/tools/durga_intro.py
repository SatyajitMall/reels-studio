#!/usr/bin/env python3
"""DURGA intro card (puja-night-2 round 5): the word with the reel's footage, Marvel-intro style.

Modes:
  fill    footage flips INSIDE tall DURGA letters on the beats while the camera pulls back out of the letters
          (3.6x -> 1x over 0-2.54 s), dark red background, cream edge;
  behind  footage flips full-frame BEHIND solid cream letters that land one per beat (D U R G A on
          0 / 0.63 / 1.28 / 1.89 / 2.54 s), dark halo.
Both: flips every half beat after 2.54, PUJA NIGHTS · 2026 under the word from 2.54, smash cut with a white
flash on the 3.79 hit (the song's biggest).

Footage is sampled from a graded render of the reel (so the card matches the grade); place the result
above the look (V5) so it isn't graded twice.

Usage:
  .venv/bin/python projects/puja-night-2/tools/durga_intro.py --mode fill --source <graded.mp4> \
      --picks 17.6,22.4,28.2,34.4,41.0,14.2,37.6,46.2 [--after 3.80] [--audio music/x.mp3 --audio-start 105.6] -o out.mp4
"""
from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 25
BEATS = [0.0, 0.63, 1.28, 1.89, 2.54, 2.84, 3.14, 3.46]
SLAM = 3.79
WORD = "DURGA"
CREAM = np.array([245, 230, 200], np.float32)
FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"
SUBFONT = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
WORD_W, WORD_H, WORD_CY = 980, 640, 880


def grab(src: str, t0: float, n: int) -> np.ndarray:
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", src, "-frames:v", str(n),
                        "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, H, W, 3)


def letter_masks() -> list[Image.Image]:
    """One full-word-sized mask per letter (word stretched to WORD_W x WORD_H), in word-box space."""
    font = ImageFont.truetype(FONT, 400)
    d = ImageDraw.Draw(Image.new("L", (10, 10)))
    bb = d.textbbox((0, 0), WORD, font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    out = []
    for i, ch in enumerate(WORD):
        m = Image.new("L", (tw + 40, th + 40), 0)
        x = 20 - bb[0] + font.getlength(WORD[:i])
        ImageDraw.Draw(m).text((x, 20 - bb[1]), ch, font=font, fill=255)
        out.append(m.resize((int((tw + 40) * WORD_W / tw), WORD_H), Image.LANCZOS))
    return out


def place(mask: Image.Image, s: float, cy: int = WORD_CY) -> np.ndarray:
    m = mask.resize((max(1, int(mask.width * s)), max(1, int(mask.height * s))), Image.BILINEAR)
    canvas = Image.new("L", (W, H), 0)
    canvas.paste(m, (int(W / 2 - m.width / 2), int(cy - m.height / 2)))
    return np.asarray(canvas, np.float32) / 255


def ease_out(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["fill", "behind"], required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--picks", required=True, help="source start times, one per flip (8)")
    ap.add_argument("--after", type=float, default=None, help="source time of the shot after the slam (preview tail)")
    ap.add_argument("--tail", type=float, default=0.8)
    ap.add_argument("--audio")
    ap.add_argument("--audio-start", type=float, default=0.0)
    ap.add_argument("--sub-size", type=int, default=86, help="PUJA NIGHTS · 2026 size in px (62 in v5 read too small)")
    ap.add_argument("--word-size", type=int, nargs=2, default=None, metavar=("W", "H"),
                    help="stretched word box at scale 1 (default 980 640; 840 600 keeps the A out of IG's right 120 px)")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    global WORD_W, WORD_H
    if a.word_size:
        WORD_W, WORD_H = a.word_size
    picks = [float(x) for x in a.picks.split(",")]
    assert len(picks) == len(BEATS)

    segs = []
    for i, b in enumerate(BEATS):
        e = BEATS[i + 1] if i + 1 < len(BEATS) else SLAM
        segs.append((b, grab(a.source, picks[i], int(round((e - b) * FPS)) + 2)))
    after = grab(a.source, a.after, int(a.tail * FPS) + 2) if a.after is not None else None
    letters = letter_masks()
    whole = Image.fromarray(np.maximum.reduce([np.asarray(m) for m in letters]))
    sub = ImageFont.truetype(SUBFONT, a.sub_size)
    yy, xx = np.mgrid[0:H, 0:W]
    glow = np.exp(-(((xx - 540) / 700) ** 2 + ((yy - 900) / 900) ** 2))[..., None]
    red_bg = (np.array([10, 4, 3]) + np.array([70, 12, 6]) * glow).astype(np.float32)
    vig = (1 - 0.55 * np.clip(np.sqrt(((xx - 540) / 620) ** 2 + ((yy - 960) / 1100) ** 2) - 0.35, 0, 1))[..., None]

    total = SLAM + (a.tail if after is not None else 0)
    n = int(round(total * FPS))
    with tempfile.TemporaryDirectory() as td:
        for f in range(n):
            t = f / FPS
            if t >= SLAM:
                fr = after[min(f - int(round(SLAM * FPS)), len(after) - 1)].astype(np.float32)
                if t < SLAM + 0.08:
                    fr = fr + 140 * (1 - (t - SLAM) / 0.08)
                Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)).save(f"{td}/f{f:04d}.png")
                continue
            k = max(i for i, b in enumerate(BEATS) if b <= t + 1e-6)
            b, clip = segs[k]
            foot = clip[min(int((t - b) * FPS), len(clip) - 1)].astype(np.float32)
            if a.mode == "fill":
                s = 3.6 - 2.6 * ease_out(t / 2.54) if t < 2.54 else 1.0 + 0.07 * ((t - 2.54) / (SLAM - 2.54)) ** 2
                mimg = whole.resize((int(whole.width * s), int(whole.height * s)), Image.BILINEAR)
                canvas = Image.new("L", (W, H), 0)
                canvas.paste(mimg, (int(W / 2 - mimg.width / 2), int(WORD_CY - mimg.height / 2)))
                ma = np.asarray(canvas, np.float32) / 255
                edge = np.asarray(canvas.filter(ImageFilter.MaxFilter(5)), np.float32) / 255 - ma
                halo = np.asarray(canvas.filter(ImageFilter.GaussianBlur(28)), np.float32) / 255
                fr = red_bg * (1 - 0.75 * halo[..., None])
                fr = fr * (1 - ma[..., None]) + foot * 1.08 * ma[..., None]
                fr = fr * (1 - 0.8 * edge[..., None]) + CREAM * 0.8 * edge[..., None]
                word_h = mimg.height
            else:
                fr = foot * 0.62 * vig                                    # footage behind, darkened so the word reads
                push = 1.0 + 0.06 * max(0.0, t - 2.54) / (SLAM - 2.54)
                ma = np.zeros((H, W), np.float32)
                for i, m in enumerate(letters):
                    if t < BEATS[i]:
                        continue
                    p = ease_out((t - BEATS[i]) / 0.22)
                    s = push * (1.25 - 0.25 * p)
                    ma = np.maximum(ma, place(m, s) * p)
                    if t - BEATS[i] < 0.08:                               # a small light flick as each letter lands
                        fr = fr + 40 * (1 - (t - BEATS[i]) / 0.08)
                halo = np.asarray(Image.fromarray((ma * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(24)), np.float32) / 255
                fr = fr * (1 - 0.7 * halo[..., None])
                fr = fr * (1 - ma[..., None]) + CREAM * ma[..., None]
                word_h = WORD_H * push
            img = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8))
            if t >= 2.54:
                al = int(255 * min(1, (t - 2.54) / 0.4))
                lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                dd = ImageDraw.Draw(lay)
                txt = "PUJA NIGHTS · 2026"
                tb = dd.textbbox((0, 0), txt, font=sub)
                dd.text((W / 2 - (tb[2] - tb[0]) / 2, WORD_CY + word_h / 2 + 20), txt, font=sub, fill=(245, 230, 200, al))
                img = Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")
            img.save(f"{td}/f{f:04d}.png")
        cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{td}/f%04d.png"]
        if a.audio:
            cmd += ["-ss", str(a.audio_start), "-t", f"{total:.2f}", "-i", a.audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
        cmd += ["-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.out]
        subprocess.run(cmd, check=True)
    print(f"✓ {a.out} ({n} frames, {a.mode})")


if __name__ == "__main__":
    main()
