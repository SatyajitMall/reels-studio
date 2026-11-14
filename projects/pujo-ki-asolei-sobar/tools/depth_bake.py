#!/usr/bin/env python3
"""Natural depth bake: mild background defocus behind the person, at full source resolution.

For each shot in the EDL marked depth = "tonal+defocus":
  1. cut the used range (+ handles) as a 1080x1920 proxy;
  2. person matte per frame with HyperFrames `remove-background` (u2net_human_seg, CPU);
  3. matte smoothed over 3 frames (less flicker), dilated 9 px + feathered 6 px (no halo);
  4. composite at full res (2160x3840): sharp source where the person is, and a background
     blurred at 1080 (sigma --blur, default 3) and up to 0.15 stop darker, weighted by a distance
     ramp (0 below the subject's feet -> 1 near the top of frame), upscaled;
  5. ProRes 422 HQ + the source's own audio, a compare strip, and frame_scan.py.

The bake starts at (src_in - handle). Place it with in = handle, out = handle + (src_out - src_in).
Usage: depth_bake.py <reel_dir> <edl.json> [--only 3a,10] [--blur 5] [--handle 0.5]
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[3]
ap = argparse.ArgumentParser()
ap.add_argument("reel"); ap.add_argument("edl")
ap.add_argument("--only", default=""); ap.add_argument("--blur", type=float, default=3.0)
ap.add_argument("--handle", type=float, default=0.5); ap.add_argument("--falloff", type=float, default=0.90)
a = ap.parse_args()
reel = Path(a.reel); out_dir = reel / "renders" / "depth"; out_dir.mkdir(parents=True, exist_ok=True)
edl = json.loads(Path(a.edl).read_text())
only = set(filter(None, a.only.split(",")))
PW, PH = 1080, 1920

def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)],
                                  capture_output=True, text=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    n, d = v["avg_frame_rate"].split("/")
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        rot = int(sd.get("rotation", rot))
    w, h = int(v["width"]), int(v["height"])
    if abs(rot) in (90, 270): w, h = h, w
    fps = float(n) / float(d)
    if 28.0 < fps < 31.0: fps = 30.0   # Blackmagic Cam: 30.0066 etc., and VFR clips with dropped frames (C004 avg 29.28) -> exact 30 grid
    return float(j["format"]["duration"]), fps, w, h

def frames(src, t0, dur, w, h, fps):
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(src), "-an", "-vf", f"scale={w}:{h}",
           "-r", f"{fps}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE); sz = w * h * 3
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz: break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    p.wait()

summary = []
for s in edl["shots"]:
    if s.get("depth") != "tonal+defocus" or (only and s["n"] not in only): continue
    src = next((reel / "raw" / "b-roll").glob(f"*_{s['clip']}.mov"))
    dur_src, fps, W, H = probe(src)
    t0 = max(0.0, s["in"] - a.handle); t1 = min(dur_src - 0.05, s["out"] + a.handle); dur = t1 - t0
    name = f"{s['n']}_{s['clip']}_depth"; mov = out_dir / f"{name}.mov"
    print(f"▸ {name}: src {t0:.2f}-{t1:.2f} ({dur:.2f}s) {W}x{H} @{fps:g}", flush=True)
    with tempfile.TemporaryDirectory(prefix="depth_") as td:
        td = Path(td); proxy = td / "proxy.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(src), "-an",
                        "-vf", f"scale={PW}:{PH}", "-r", f"{fps}", "-c:v", "libx264", "-crf", "12", str(proxy)], check=True)
        r = subprocess.run(["npx", "hyperframes", "remove-background", str(proxy), "-o", str(td / "fg.mov"), "--device", "cpu"],
                           capture_output=True, text=True, cwd=td)
        if r.returncode != 0 or not (td / "fg.mov").exists():
            print(f"✗ matte failed for {name}:\n{(r.stdout + r.stderr)[-600:]}"); continue
        araw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(td / "fg.mov"), "-vf", "alphaextract", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                              capture_output=True).stdout
        alpha = np.frombuffer(araw, np.uint8).reshape(-1, PH, PW).astype(np.float32) / 255
        # temporal smoothing (3-frame mean) -> less matte flicker
        sm = alpha.copy(); sm[1:-1] = (alpha[:-2] + alpha[1:-1] + alpha[2:]) / 3
        cover = float(sm.mean())
        vid = td / "v.mov"
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", f"{fps}",
                                "-i", "-", "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(vid)], stdin=subprocess.PIPE)
        n = 0
        for i, fr in enumerate(frames(src, t0, dur, W, H, fps)):
            al = sm[min(i, len(sm) - 1)]
            al = ndimage.gaussian_filter(ndimage.grey_dilation(al, size=(9, 9)), 6)
            # distance ramp: nothing below the subject's feet blurs (foreground / near ground stays sharp);
            # blur weight rises toward the top of frame, where the far background is
            rows = np.where(sm[min(i, len(sm) - 1)].max(axis=1) > 0.5)[0]
            feet = rows.max() if len(rows) else int(PH * 0.8)
            top = int(PH * 0.15)
            yy = np.arange(PH, dtype=np.float32)
            ramp = np.clip((feet - yy) / max(feet - top, 1), 0, 1) ** 0.8
            w = (1 - al) * ramp[:, None]
            small = np.asarray(Image.fromarray(fr).resize((PW, PH), Image.BILINEAR), np.float32)
            bg = np.stack([ndimage.gaussian_filter(small[..., c], a.blur) for c in range(3)], -1)
            bg = bg * (1 - (1 - a.falloff) * w[..., None])          # light falloff only where it's far
            bg4 = np.asarray(Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32)
            w4 = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR), np.float32)[..., None] / 255
            o = fr.astype(np.float32) * (1 - w4) + bg4 * w4
            enc.stdin.write(np.clip(o, 0, 255).astype(np.uint8).tobytes()); n += 1
        enc.stdin.close(); enc.wait()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vid), "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(src),
                        "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "pcm_s16le", "-shortest", str(mov)], check=True)
    cmp_png = out_dir / f"{name}_compare.png"
    mid = a.handle + (s["out"] - s["in"]) / 2
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0 + mid:.3f}", "-i", str(src), "-ss", f"{mid:.3f}", "-i", str(mov),
                    "-filter_complex", "[0:v]scale=540:960[a];[1:v]scale=540:960[b];[a][b]hstack", "-frames:v", "1", str(cmp_png)], check=True)
    scan = subprocess.run([sys.executable, str(ROOT / "scripts" / "frame_scan.py"), str(mov), "-o", str(out_dir / f"{name}.scan.json")],
                          capture_output=True, text=True).stdout.strip().splitlines()
    rec = {"n": s["n"], "clip": s["clip"], "bake": str(mov.relative_to(reel)), "bake_src_start": round(t0, 3),
           "place_in": round(s["in"] - t0, 3), "place_out": round(s["out"] - t0, 3), "frames": n, "matte_cover": round(cover, 3),
           "scan": scan[-1] if scan else "?"}
    summary.append(rec); print(f"  ✓ {mov.name} frames={n} cover={cover:.2f} scan: {rec['scan']}", flush=True)

prev = out_dir / "bakes.json"
old = json.loads(prev.read_text()) if prev.exists() else []
keep = [r for r in old if r["n"] not in {x["n"] for x in summary}]
prev.write_text(json.dumps(keep + summary, indent=1)); print(f"✓ {prev}")
