#!/usr/bin/env python3
"""Skin hue / saturation per rendered shot over its placed frames. Usage: skin_report.py <ver> [shot ...]"""
import sys, json, glob, subprocess, colorsys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import skin_match as sm
R = Path(__file__).resolve().parents[1] / "renders" / "final_shots"; ver = sys.argv[1]; only = set(sys.argv[2:])
for j in sorted(glob.glob(str(R / f"*_{ver}.json"))):
    r = json.load(open(j)); n = r["n"]
    if only and n not in only: continue
    X = []
    for k in range(1, 6):
        t = r["place_in"] + (r["place_out"] - r["place_in"]) * k / 6
        raw = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",str(R / r["file"]),"-frames:v","1","-vf","scale=540:960","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
        X.append(np.frombuffer(raw, np.uint8).reshape(960, 540, 3).astype(np.float32) / 255)
    import tempfile
    with tempfile.TemporaryDirectory() as td: pp = sm.people_alphas([x[::2, ::2] for x in X], td)
    s = sm.skin_of([x[::2, ::2] for x in X], people=pp); y = np.mean([x @ np.array([0.2126, 0.7152, 0.0722]) for x in X])
    h, sa, v = colorsys.rgb_to_hsv(*s) if s is not None else (0, 0, 0)
    print(f"{r['file']:<16} skin hue {h*360:5.1f}  sat {sa:.2f}  val {v:.2f}  frame luma {y:.3f}")
