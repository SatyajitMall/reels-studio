#!/usr/bin/env python3
"""HQ test: compare AI gap-fills (Veo, Omni) against the real camera stretch between the same two stills."""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W = Path(sys.argv[1])
VIDS = [("REAL CAMERA (C047, 3.0 to 7.0 s, f/2 bake)", W / "real.mp4"),
        ("VEO 3.1 LITE  ($0.12)", W / "veo.mp4"),
        ("GEMINI OMNI 1.2 FLASH  ($0.28)", W / "omni.mp4"),
        ("OMNI, CINEMATIC PROMPT, 1080p  ($0.42)", W / "omni_cine.mp4")]
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 34)
SW, SH = 320, 180


def frames(path: Path, w=SW, h=SH, fps=25) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={w}:{h}", "-pix_fmt", "rgb24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)


def still(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB").resize((SW, SH), Image.BILINEAR), np.float32)


def sat(f: np.ndarray) -> float:
    mx, mn = f.max(axis=-1), f.min(axis=-1)
    return float(np.mean((mx - mn) / np.maximum(mx, 1)))


a, b = still(W / "a.jpg"), still(W / "b.jpg")
report = {}
data = {}
for name, p in VIDS:
    fr = frames(p)
    data[name] = fr
    luma = fr @ np.array([0.2126, 0.7152, 0.0722], np.float32) / 255
    step = np.abs(np.diff(luma, axis=0)).mean(axis=(1, 2))
    report[name] = {
        "frames_at_25fps": int(len(fr)),
        "first_vs_still_A": round(float(np.abs(fr[0] - a).mean()), 2),
        "last_vs_still_B": round(float(np.abs(fr[-1] - b).mean()), 2),
        "best_match_to_B_at_s": round(float(np.argmin([np.abs(f - b).mean() for f in fr]) / 25), 2),
        "mean_luma": round(float(luma.mean()), 3),
        "mean_sat": round(float(np.mean([sat(f) for f in fr[::5]])), 3),
        "motion_mean_step": round(float(step.mean()), 4),
        "motion_max_step": round(float(step.max()), 4),
        "max_step_at_s": round(float(np.argmax(step) / 25 + 0.04), 2),
    }
real = data[VIDS[0][0]]
for name, fr in data.items():
    n = min(len(fr), len(real))
    report[name]["vs_real_same_time_mean_diff"] = round(float(np.abs(fr[:n] - real[:n]).mean()), 2)
print(json.dumps(report, indent=1))
(W / "compare2.json").write_text(json.dumps(report, indent=1))

# Contact sheet: 6 moments per row.
cols = [0, 20, 40, 60, 80, -1]
TW, TH = 400, 225
sheet = Image.new("RGB", (TW * len(cols), (TH + 44) * len(VIDS)), (14, 14, 14))
draw = ImageDraw.Draw(sheet)
small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
for r, (name, p) in enumerate(VIDS):
    big = frames(p, TW, TH)
    draw.text((10, r * (TH + 44) + 8), name, font=small, fill=(245, 230, 200))
    for c, i in enumerate(cols):
        k = min(i if i >= 0 else len(big) - 1, len(big) - 1)
        sheet.paste(Image.fromarray(big[k].astype(np.uint8)), (c * TW, r * (TH + 44) + 44))
        draw.text((c * TW + 8, r * (TH + 44) + 50), f"{k / 25:.1f}s", font=small, fill=(255, 255, 255))
sheet.save(W / "compare_sheet2.jpg", quality=90)

# Labels for the phone video.
for k, (name, _) in enumerate(VIDS):
    lab = Image.new("RGBA", (1080, 56), (0, 0, 0, 170))
    ImageDraw.Draw(lab).text((16, 9), name, font=FONT, fill=(245, 230, 200, 255))
    lab.save(W / f"label{k}.png")
print("✓ compare_sheet.jpg, labels")
