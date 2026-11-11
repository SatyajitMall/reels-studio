#!/usr/bin/env python3
"""HQ test: compare any gap fills against the real C047 stretch (3.0–7.0 s) between the same two stills.

Usage: hf_compare.py <workdir with real.mp4 a.jpg b.jpg> <out_stem> "LABEL=path" ...
Per clip: frames, distance of first frame to still A and last frame to still B, when it best matches B,
luma/saturation, motion (mean and max frame-to-frame luma step = a pop), and the mean difference to the real
camera at the same time. Also a contact sheet (0, 0.8, 1.6, 2.4, 3.2 s, last) and the JSON.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = Path(sys.argv[1]); STEM = sys.argv[2]
VIDS = [("REAL CAMERA (C047 3.0-7.0 s)", W / "real.mp4")] + [(s.split("=", 1)[0], Path(s.split("=", 1)[1])) for s in sys.argv[3:]]
SW, SH, FPS = 320, 180, 25
LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)


def frames(path: Path, w=SW, h=SH) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={FPS},scale={w}:{h}:flags=area", "-pix_fmt", "rgb24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)


def still(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB").resize((SW, SH), Image.BILINEAR), np.float32)


def sat(f: np.ndarray) -> float:
    mx, mn = f.max(axis=-1), f.min(axis=-1)
    return float(np.mean((mx - mn) / np.maximum(mx, 1)))


a, b = still(W / "a.jpg"), still(W / "b.jpg")
rep, data = {}, {}
for name, p in VIDS:
    fr = frames(p); data[name] = fr
    luma = fr @ LUMA / 255
    step = np.abs(np.diff(luma, axis=0)).mean(axis=(1, 2))
    dB = [np.abs(f - b).mean() for f in fr]
    rep[name] = {"file": str(p), "frames_at_25fps": int(len(fr)),
                 "first_vs_still_A": round(float(np.abs(fr[0] - a).mean()), 2),
                 "last_vs_still_B": round(float(dB[-1]), 2),
                 "best_match_to_B": round(float(min(dB)), 2), "best_match_to_B_at_s": round(float(np.argmin(dB) / FPS), 2),
                 "mean_luma": round(float(luma.mean()), 3), "mean_sat": round(float(np.mean([sat(f) for f in fr[::5]])), 3),
                 "motion_mean_step": round(float(step.mean()), 4), "motion_max_step": round(float(step.max()), 4),
                 "max_step_at_s": round(float(np.argmax(step) / FPS + 1 / FPS), 2)}
real = data[VIDS[0][0]]
for name, fr in data.items():
    n = min(len(fr), len(real))
    rep[name]["vs_real_same_time_mean_diff"] = round(float(np.abs(fr[:n] - real[:n]).mean()), 2)
print(json.dumps(rep, indent=1))
(W / f"{STEM}.json").write_text(json.dumps(rep, indent=1))

cols = [0, 20, 40, 60, 80, -1]
TW, TH = 400, 225
font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
sheet = Image.new("RGB", (TW * len(cols), (TH + 44) * len(VIDS)), (14, 14, 14))
draw = ImageDraw.Draw(sheet)
for r, (name, p) in enumerate(VIDS):
    big = frames(p, TW, TH)
    draw.text((10, r * (TH + 44) + 8), name, font=font, fill=(245, 230, 200))
    for c, i in enumerate(cols):
        k = min(i if i >= 0 else len(big) - 1, len(big) - 1)
        sheet.paste(Image.fromarray(big[k].astype(np.uint8)), (c * TW, r * (TH + 44) + 44))
        draw.text((c * TW + 8, r * (TH + 44) + 50), f"{k / FPS:.1f}s", font=font, fill=(255, 255, 255))
sheet.save(W / f"{STEM}_sheet.jpg", quality=90)
print(f"✓ {W / (STEM + '_sheet.jpg')}")
