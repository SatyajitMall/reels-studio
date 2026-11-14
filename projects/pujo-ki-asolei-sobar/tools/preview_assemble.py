#!/usr/bin/env python3
"""Offline preview of a version, mirroring the Premiere timeline (used while Premiere is busy with another reel):
V1 shots at their EDL frames (with the 100->105 % pushes and the 10-frame dissolve at f886), V5 subtitles, V6 title
(alpha mov) + end card, A3 = reference VO. Output H.264 1080x1920 @ 30 + AAC.
Usage: preview_assemble.py <ver> <edl_ver> <out.mp4> [--shot1 <suffix>] [--bw-text]
       --shot1: shot 1 from 01_<clip>_<suffix>.json instead of <ver> (e.g. bwfade); --bw-text: neutral title / end card (B&W version)
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

REEL = Path(__file__).resolve().parents[1]
VER, EDLV, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SHOT1 = sys.argv[sys.argv.index("--shot1") + 1] if "--shot1" in sys.argv else VER; BWT = "--bw-text" in sys.argv
W, H, FPS, END = 1080, 1920, 30, 1075
edl = json.loads((REEL / "analysis" / f"edl_{EDLV}.json").read_text())
PUSH = set(edl.get("push", [0, 288, 797, 886, 969])); DISS = tuple(edl.get("dissolve", [881, 891]))   # v9 EDL carries its own
def load(path, a, nfr):
    # read by frame index (an -ss seek into rawvideo repeats the first frame under cfr: gate v10 #7)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"select='between(n,{a},{a + nfr - 1})'", "-fps_mode", "passthrough",
                          "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
shots = []
for s in edl["shots"]:
    r = json.loads((REEL / "renders" / "final_shots" / f"{int(s['n']):02d}_{s['clip']}_{SHOT1 if s['n'] == '1' else VER}.json").read_text())
    a = round(r["place_in"] * FPS); nfr = s["endF"] - s["startF"]
    pre = 5 if s["startF"] == 886 else 0; post = 5 if s["endF"] == 886 else 0        # dissolve handles
    fr = load(REEL / "renders" / "final_shots" / r["file"], a - pre, nfr + pre + post)
    shots.append((s, fr, pre))
def push(img, k):   # scale about centre
    if k <= 1.0001: return img
    im = Image.fromarray(img).resize((int(W * k), int(H * k)), Image.BICUBIC); x0 = (im.width - W) // 2; y0 = (im.height - H) // 2
    return np.asarray(im.crop((x0, y0, x0 + W, y0 + H)))
def frame_of(s, fr, pre, f):
    i = f - s["startF"] + pre; img = fr[min(max(i, 0), len(fr) - 1)]
    if s["startF"] in PUSH:
        k = 1 + 0.05 * (f - s["startF"]) / max(s["endF"] - s["startF"] - 1, 1); img = push(img, k)
    return img.astype(np.float32)
subs = json.loads((REEL / "analysis" / "subtitles_v1.json").read_text())["blocks"]
subimg = {}
for i, (a, b, _) in enumerate(subs, 1):
    nm = {1: "sub_01_side", 2: "sub_02_side"}.get(i, f"sub_{i:02d}")
    subimg[i] = (round(a * FPS), round(b * FPS), np.asarray(Image.open(REEL / "renders/overlays/subs" / f"{nm}.png").convert("RGBA"), np.float32) / 255)
endc = np.asarray(Image.open(REEL / ("renders/overlays/endcard_handle_v2_bw.png" if BWT else "renders/overlays/endcard_handle_v2.png")).convert("RGBA"), np.float32) / 255
traw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(REEL / ("renders/overlays/title-alpha_bw.mov" if BWT else "graphics/title/renders/title-alpha.mov")), "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True).stdout
title = np.frombuffer(traw, np.uint8).reshape(-1, H, W, 4); T0 = 8
def over(base, rgba):
    a = rgba[..., 3:4]; return base * (1 - a) + rgba[..., :3] * 255 * a
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-i", str(REEL / "audio/ref_audio_vo.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-af", "apad", "-t", f"{END / FPS:.4f}", OUT], stdin=subprocess.PIPE)
for f in range(END):
    cur = next(x for x in shots if x[0]["startF"] <= f < x[0]["endF"])
    img = frame_of(*cur, f)
    if DISS[0] <= f < DISS[1]:
        a_s = next(x for x in shots if x[0]["endF"] == 886); b_s = next(x for x in shots if x[0]["startF"] == 886)
        w = (f - DISS[0] + 0.5) / (DISS[1] - DISS[0]); img = frame_of(*a_s, f) * (1 - w) + frame_of(*b_s, f) * w
    for a, b, rgba in subimg.values():
        if a <= f < b: img = over(img, rgba)
    if T0 <= f < T0 + len(title): img = over(img, title[f - T0].astype(np.float32) / 255)
    if 1032 <= f: img = over(img, endc)
    enc.stdin.write(np.clip(img + 0.5, 0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print("✓", OUT)
