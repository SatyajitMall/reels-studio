#!/usr/bin/env python3
"""Round 10 gate bar for synthesised slow motion (review_v10.md method): per frame, Laplacian-variance sharpness (subtitle band
y 1380-1600 of 1920 masked), the sharp/soft alternation index (mean |Δsharp| between consecutive frames ÷ mean sharpness) and the
blend-like share (moving pixels, |L(k+1) − L(k−1)| > 0.08, whose L(k) sits within 20 % of that swing of the neighbours' mean, i.e. a
frame blend rather than a displaced edge). Pass bar: no frame > 50 % blend share, alternation ≤ 0.10, sharpness within 10 % of real.
Usage (reel folder): ../../.venv/bin/python tools/r10_slowmo_metrics.py <video> <first frame> <n frames> [label]
Frames are scaled to 1080×1920 (a 4K render is measured at the reel's pixel pitch)."""
import subprocess, sys
import numpy as np

video, a, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); label = sys.argv[4] if len(sys.argv) > 4 else video
W, H = 1080, 1920
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a / 25:.3f}", "-i", video, "-frames:v", str(n), "-vf", f"scale={W}:{H}:flags=area",
                      "-f", "rawvideo", "-pix_fmt", "gray16le", "-"], capture_output=True).stdout
L = np.frombuffer(raw, np.uint16).reshape(-1, H, W).astype(np.float32) / 65535
mask = np.ones((H, W), bool); mask[1380:1600] = False


def sharp(x):
    lap = -4 * x[1:-1, 1:-1] + x[:-2, 1:-1] + x[2:, 1:-1] + x[1:-1, :-2] + x[1:-1, 2:]
    return float(lap[mask[1:-1, 1:-1]].var())


s = np.array([sharp(x) for x in L])
alt = float(np.abs(np.diff(s)).mean() / s.mean())
blend = []
for k in range(1, len(L) - 1):
    sw = L[k + 1] - L[k - 1]; mv = (np.abs(sw) > 0.08) & mask
    if mv.sum() < 500: blend.append(0.0); continue
    m = (L[k + 1] + L[k - 1]) / 2
    blend.append(float((np.abs(L[k] - m)[mv] <= 0.2 * np.abs(sw)[mv]).mean()))
blend = np.array(blend)
worst = np.argsort(blend)[::-1][:5]
print(f"{label}: {len(L)} frames  sharp mean {s.mean():.5f}  alternation {alt:.3f}  blend mean {blend.mean()*100:.1f}% max {blend.max()*100:.1f}%"
      f"  >50%: {(blend > 0.5).sum()}  >75%: {(blend > 0.75).sum()}  worst " + " ".join(f"{a + 1 + w}:{blend[w]*100:.0f}%" for w in worst))
