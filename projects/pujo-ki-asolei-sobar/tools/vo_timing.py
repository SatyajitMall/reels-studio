"""Line timings from burned-in subtitle changes + speech-band envelope dips."""
import subprocess, sys, json
import numpy as np
vid, wav, out = sys.argv[1:4]
# 1) subtitle band: bottom of 1280x720 frame, centre
W, H = 900, 50
cmd = ["ffmpeg", "-v", "error", "-i", vid, "-vf", f"crop={W}:{H}:190:640", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
raw = subprocess.run(cmd, capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.int16)
r, g, b = fr[..., 0], fr[..., 1], fr[..., 2]
mask = (r > 170) & (g > 120) & (b < 110) & (r - b > 90)       # yellow-ish subtitle text
cnt = mask.sum(axis=(1, 2))
fps = 24.0
lines, cur, start = [], None, None
for i, m in enumerate(mask):
    on = cnt[i] > 150
    if not on:
        if cur is not None:
            lines.append((start, i / fps)); cur = None
        continue
    if cur is None:
        cur, start = m, i / fps; continue
    inter = (cur & m).sum(); uni = (cur | m).sum()
    if uni and inter / uni < 0.55:        # text changed
        lines.append((start, i / fps)); cur, start = m, i / fps
    else:
        cur = cur | m if inter / uni > 0.8 else m
if cur is not None: lines.append((start, len(mask) / fps))
lines = [(round(a, 2), round(b, 2)) for a, b in lines if b - a > 0.3]
# 2) speech-band envelope (300-3400 Hz), 20 ms hop
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-af", "highpass=f=300,lowpass=f=3400", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
hop = 320
n = len(a) // hop
rms = np.sqrt((a[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
db = 20 * np.log10(rms)
sm = np.convolve(db, np.ones(5) / 5, mode="same")
thr = np.percentile(sm, 35)
dips, inq = [], False
for i, v in enumerate(sm):
    if v < thr and not inq: inq, s0 = True, i
    if v >= thr and inq:
        inq = False
        if (i - s0) * 0.02 >= 0.12: dips.append((round(s0 * 0.02, 2), round(i * 0.02, 2)))
json.dump({"subtitle_lines": lines, "speech_dips": dips, "dip_threshold_db": float(thr)}, open(out, "w"), indent=1)
print("subtitle lines:"); [print(f"  {a:6.2f}-{b:6.2f}") for a, b in lines]
print(f"speech-band dips (< {thr:.1f} dB, >=0.12 s):"); print("  " + ", ".join(f"{a}-{b}" for a, b in dips))
