#!/usr/bin/env python3
"""Re-word burned-in subtitle cards on an export without going back to Premiere (round 14: the director's own VO says
"pehla kehta hai" and "...sapnon mein khoya rehta hai", so cards 10, 17 and 18 change).
For each changed card's frames: clean background from the baked shot render (same frame, same 100->105 % push; matched to
the export within 2-3/255), the new card on top, feathered into the export only inside the subtitle band. Everything else
in the picture is the export, untouched. Re-encoded once (x264 CRF 14, BT.709), audio copied from the input.
Usage: sub_patch.py <in.mp4> <out.mp4>
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders/final_shots"; S = REEL / "renders/overlays/subs"
W, H, FPS = 1080, 1920, 30
# card frames (from subtitles_v1.json timing) -> new card, shot render, render frame offset, shot span (for the push)
CARDS = [(539, 576, "sub_10_v17.png", "06_C212_m5e.mov", 7, None),
         (969, 1008, "sub_17_v17.png", "12_C193_v13h.mov", 5, (969, 1075)),
         (1008, 1071, "sub_18_v17.png", "12_C193_v13h.mov", 5, (969, 1075))]
BAND = (1330, 1610); FEATHER = 18
IN, OUT = sys.argv[1], sys.argv[2]

def push(img, k):
    if k <= 1.0001: return img
    im = Image.fromarray(img).resize((int(W * k), int(H * k)), Image.BICUBIC); x0 = (im.width - W) // 2; y0 = (im.height - H) // 2
    return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)))
def frames(path, a, n):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"select='between(n,{a},{a + n - 1})'", "-fps_mode", "passthrough",
                          "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)

mask = np.zeros((H, W), np.float32); mask[BAND[0]:BAND[1], 60:W - 60] = 1; mask = ndimage.gaussian_filter(mask, FEATHER)[..., None]
patch = {}
for f0, f1, card, shot, off, span in CARDS:
    c = np.asarray(Image.open(S / card).convert("RGBA"), np.float32) / 255
    src = frames(R / shot, off + (f0 - (span[0] if span else 539)), f1 - f0)
    for i, fr in enumerate(src):
        f = f0 + i
        if span: fr = push(fr, 1 + 0.05 * (f - span[0]) / (span[1] - span[0] - 1))
        bg = fr.astype(np.float32); patch[f] = bg * (1 - c[..., 3:]) + c[..., :3] * 255 * c[..., 3:]
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", IN, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", IN,
                        "-map", "0:v", "-map", "1:a", "-vf", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv,format=yuv420p",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-maxrate", "16M", "-bufsize", "24M", "-color_primaries", "bt709",
                        "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
f = 0
while True:
    b = dec.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    if f in patch:
        x = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32)
        b = (x * (1 - mask) + patch[f] * mask + 0.5).clip(0, 255).astype(np.uint8).tobytes()
    enc.stdin.write(b); f += 1
enc.stdin.close(); enc.wait(); dec.wait()
print(f"✓ {OUT}: {f} frames, {len(patch)} re-worded")
