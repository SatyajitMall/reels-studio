#!/usr/bin/env python3
"""Per-shot grade trims after the look (review gate v9 loop 1): bring new shots in line with the reel without re-rendering.
Ops (all optional, from analysis/trim_v9.json["<n>"]), applied in this order on each frame (code values 0..1):
  shadow   a      : luma toe lift  Y' = Y + a * Y * exp(-Y / 0.08)  (monotonic for a <= 2.7; lifts faces in the dark, mids barely move)
  mid_rgb  [r,g,b]: channel gains weighted to the midtones (w = 4 Y (1 - Y)), luminance kept
  sat      k      : saturation about luma
  luma     L      : final gain so the frame mean luma (on-screen frames) = L
  luma_gamma L    : as luma, but by a luma power curve (Y^g), so highlights don't clip (round 11: brightness follows the original)
  sharpen  amt    : unsharp mask on luma (radius 1.2 px)
  protect_skin    : mid_rgb and sat act only outside skin hues (hue 10-45 deg, sat 0.12-0.8, feathered), so faces keep the skin anchor
  protect "person": as protect_skin, but only skin inside a person matte (round 10: orange walls in the skin hue band get graded too)
  face_lift {target, cap}: exposure on faces only (person matte x skin hues): local luma raised toward target, gain <= cap
  floor    f      : shared black floor, x = f + x (1 - f)
  desat_hue {center, width, k}: saturation x k on one hue band (degrees, feathered), e.g. a teal cabinet
  black_target b  : after the brightness curve, a toe-only pull (y - k (1-y)^3) takes the darkest 1 % of luma down to b; highlights untouched
                    (round 13: a power-curve lift had greyed the blacks; a subtract-and-rescale pull clipped whites)
  shoulder  knee  : soft roll-off of every channel above knee instead of a hard clip (default 0.9 whenever luma_gamma is used)
  skin_gain [r,g,b]: channel gains on skin inside the person matte only, luminance kept (round 12: fix a face without tinting the scene)
  window  [a, b]  : render frames used to measure luma (the on-screen frames; default place_in..place_out)
Usage: shot_trim.py <file n> <in suffix> <out suffix> [--clip Cnnn] [--key k]   (key into trim_v9.json, default <file n>;
       constants are measured once on the on-screen frames, same on every frame; person mattes cached in analysis/mattes/)
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
n, SIN, SOUT = sys.argv[1], sys.argv[2], sys.argv[3]
def opt(k): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else None
CLIP = opt("--clip"); T = json.loads((REEL / "analysis/trim_v9.json").read_text())[opt("--key") or n]
js = next(R.glob(f"{int(n):02d}_{CLIP or '*'}_{SIN}.json")); r = json.loads(js.read_text()); src = R / r["file"]
W, H = 1080, 1920; LW = np.array([0.2126, 0.7152, 0.0722], np.float32)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint16).reshape(-1, H, W, 3); N = len(F)
ALPHA = None
if T.get("protect") == "person" or "face_lift" in T or "skin_gain" in T:      # person mattes at 540x960 (hyperframes remove-background), cached
    import tempfile
    md = REEL / "analysis/mattes"; md.mkdir(exist_ok=True); cache = md / f"{js.stem}.npz"
    if cache.exists(): ALPHA = np.load(cache)["a"]
    else:
        with tempfile.TemporaryDirectory(prefix="mat_") as td:
            px = Path(td) / "p.mp4"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", "scale=540:960", "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", "-an", str(px)], check=True)
            subprocess.run(["npx", "hyperframes", "remove-background", str(px), "-o", str(Path(td) / "fg.mov"), "--device", "cpu"], capture_output=True, cwd=td)
            araw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(Path(td) / "fg.mov"), "-vf", "alphaextract", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        ALPHA = np.frombuffer(araw, np.uint8).reshape(-1, 960, 540); np.savez_compressed(cache, a=ALPHA)
    print(f"  person mattes: {len(ALPHA)} frames", flush=True)
def alpha_at(i):
    a = ALPHA[min(i, len(ALPHA) - 1)].astype(np.float32) / 255
    a = ndimage.gaussian_filter(ndimage.grey_dilation(a, size=(5, 5)), 2)
    return ndimage.zoom(a, 2, order=1)[:H, :W]
def skin_w(x):
    mx = x.max(-1); mn = x.min(-1); d = np.maximum(mx - mn, 1e-6); s = (mx - mn) / np.maximum(mx, 1e-6)
    r_, g_, b_ = x[..., 0], x[..., 1], x[..., 2]
    h = np.where(mx == r_, ((g_ - b_) / d) % 6, np.where(mx == g_, (b_ - r_) / d + 2, (r_ - g_) / d + 4)) * 60
    wh = np.clip((h - 5) / 5, 0, 1) * np.clip((50 - h) / 5, 0, 1); ws = np.clip((s - 0.08) / 0.04, 0, 1) * np.clip((0.85 - s) / 0.05, 0, 1)
    return ndimage.gaussian_filter(wh * ws, 2)[..., None]
def ops(x, gain=1.0, i=0):
    if "floor" in T:
        x = T["floor"] + x * (1 - T["floor"])
    y = x @ LW
    if "face_lift" in T:
        fl = T["face_lift"]; wf = ndimage.gaussian_filter(skin_w(x)[..., 0] * alpha_at(i), 6)
        L = ndimage.gaussian_filter(y, 12); g = np.clip(fl["target"] / np.maximum(L, 1e-3), 1, fl["cap"])
        x = x * (1 + (g - 1) * wf)[..., None]; y = x @ LW
    if "skin_gain" in T:
        ws = (skin_w(x)[..., 0] * alpha_at(i))[..., None]; g = np.array(T["skin_gain"], np.float32)
        x2 = x * (1 + (g - 1) * ws); y2 = x2 @ LW; x = x2 * (y / np.maximum(y2, 1e-5))[..., None]
    if "shadow" in T:
        y2 = y + T["shadow"] * y * np.exp(-y / 0.08); x = x * (y2 / np.maximum(y, 1e-5))[..., None]; y = y2
    x_keep = x.copy() if (T.get("protect_skin") or T.get("protect") == "person") else None
    if "mid_rgb" in T:
        g = np.array(T["mid_rgb"], np.float32); w = np.clip(4 * y * (1 - y), 0, 1)[..., None]
        x2 = x * (1 + (g - 1) * w); y2 = x2 @ LW; x = x2 * (y / np.maximum(y2, 1e-5))[..., None]
    if "sat" in T:
        yy = (x @ LW)[..., None]; x = yy + (x - yy) * T["sat"]
    if "desat_hue" in T:
        dh = T["desat_hue"]; mx = x.max(-1); mn = x.min(-1); dd = np.maximum(mx - mn, 1e-6)
        r_, g_, b_ = x[..., 0], x[..., 1], x[..., 2]
        h = np.where(mx == r_, ((g_ - b_) / dd) % 6, np.where(mx == g_, (b_ - r_) / dd + 2, (r_ - g_) / dd + 4)) * 60
        dist = np.abs((h - dh["center"] + 180) % 360 - 180); w = np.clip(1 - (dist - dh["width"] / 2) / 15, 0, 1)[..., None]
        yy = (x @ LW)[..., None]; x = x * (1 - w) + (yy + (x - yy) * dh["k"]) * w
    if x_keep is not None:
        w = skin_w(x_keep)
        if T.get("protect") == "person": w = w * alpha_at(i)[..., None]
        x = x * (1 - w) + x_keep * w
    x = x * gain
    if LG != 1.0:
        yy = np.clip(x @ LW, 1e-5, 1); x = x * ((yy ** LG) / yy)[..., None]
    if BP > 0:
        yy = np.clip(x @ LW, 1e-5, 1); yb = np.maximum(yy - BP * (1 - yy) ** 3, 0); x = x * (yb / yy)[..., None]
    if KNEE < 1:
        hi = x > KNEE; x = np.where(hi, KNEE + (1 - KNEE) * np.tanh((x - KNEE) / (1 - KNEE)), x)
    if "sharpen" in T:
        yy = x @ LW; d = yy - ndimage.gaussian_filter(yy, 1.2); x = x + (T["sharpen"] * d)[..., None]
    return np.clip(x, 0, 1)
LG = 1.0; BP = 0.0; KNEE = float(T.get("shoulder", 0.9 if "luma_gamma" in T else 1.0))
pa, pb = T.get("window") or (int(round(r.get("place_in", 0) * 30)), int(round(r.get("place_out", N / 30) * 30)))
pa, pb = max(0, min(pa, N - 1)), max(1, min(pb, N))                   # clamp to the render (shorter re-renders)
gain = 1.0
if "luma" in T:
    sample = [ops(F[i].astype(np.float32) / 65535, 1.0, i) for i in np.linspace(pa, max(pa, pb - 1), 6).astype(int)]
    gain = T["luma"] / float(np.mean([s @ LW for s in sample]))
if "luma_gamma" in T:
    ys = np.concatenate([(ops(F[i].astype(np.float32) / 65535, 1.0, i) @ LW).ravel()[::9] for i in np.linspace(pa, max(pa, pb - 1), 6).astype(int)])
    lo, hi = 0.3, 2.0
    for _ in range(40):
        LG = (lo + hi) / 2
        if np.mean(np.clip(ys, 1e-5, 1) ** LG) > T["luma_gamma"]: lo = LG
        else: hi = LG
if "black_target" in T:   # solve the brightness curve and the black pull together, so the mean still hits luma_gamma (round 13b)
    bt = T["black_target"]; ys_c = np.clip(ys if "luma_gamma" in T else np.concatenate([(ops(F[i].astype(np.float32) / 65535, 1.0, i) @ LW).ravel()[::9] for i in np.linspace(pa, max(pa, pb - 1), 6).astype(int)]), 1e-5, 1)
    for _ in range(4):
        yl = ys_c ** LG; p1 = float(np.percentile(yl, 1)); BP = max(0.0, (p1 - bt) / max((1 - p1) ** 3, 1e-3))
        if "luma_gamma" not in T: break
        lo, hi = 0.2, 2.0
        for _ in range(40):
            LG = (lo + hi) / 2; yl = ys_c ** LG
            if np.mean(np.maximum(yl - BP * (1 - yl) ** 3, 0)) > T["luma_gamma"]: lo = LG
            else: hi = LG
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-i", str(src),
                        "-map", "0:v", "-map", "1:a?", "-vf", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+write_colr", str(R / f"_tmp_trim_{n}.mov")], stdin=subprocess.PIPE)
for i in range(N):
    enc.stdin.write((ops(F[i].astype(np.float32) / 65535, gain, i) * 65535 + 0.5).astype(np.uint16).tobytes())
enc.stdin.close(); enc.wait()
name = js.name.replace(f"_{SIN}.json", f"_{SOUT}"); (R / f"_tmp_trim_{n}.mov").rename(R / f"{name}.mov")
(R / f"{name}.json").write_text(json.dumps(dict(r, file=f"{name}.mov", trim=dict(T, luma_gain=round(gain, 4), luma_gamma_g=round(LG, 4), black_pull=round(BP, 4), shoulder=KNEE)), indent=1))
print(f"✓ {name}: {N} frames, trims {T}, gain {gain:.3f}", flush=True)
