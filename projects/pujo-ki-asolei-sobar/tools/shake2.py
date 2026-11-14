#!/usr/bin/env python3
"""Residual shake per shot (translation px @1080, roll deg, zoom %) with the similarity estimator. Usage: shake2.py <video> <edl.json> [--from-render <ver>]"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent)); import stab2
REEL = Path(__file__).resolve().parents[1]
vid, edl = sys.argv[1], json.load(open(sys.argv[2]))
raw = subprocess.run(["ffmpeg","-v","error","-i",vid,"-an","-vf","scale=540:960","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
X = np.frombuffer(raw, np.uint8).reshape(-1, 960, 540).astype(np.float32)
out = {}
for s in edl["shots"]:
    a, b = s["startF"] + 1, min(len(X), s["endF"] - 1)
    m = stab2.measure([X[i] for i in range(a, b)]); m["trans_px"] *= 2; out[s["n"]] = m
    print(f"{s['n']:>2} {s['clip']}  trans {m['trans_px']:5.2f}px  roll {m['rot_deg']:5.3f}°  zoom {m['scale_pct']:5.3f}%")
json.dump(out, open(sys.argv[3] if len(sys.argv) > 3 else "/dev/null", "w"), indent=1)
