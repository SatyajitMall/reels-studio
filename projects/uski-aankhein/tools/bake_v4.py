#!/usr/bin/env python3
"""v3 bake (round 2, story B; from bake_v2.py): adds shots from any source (src/fps/res/rot in the EDL row), mode "plain" (full frame, e.g. the AI esraj), and "overlay": "esraj" (the AI clip screened over the shot, fading out at its end).
Round 1b bake: stabilised, primary-corrected V1 shots with dissolve handles, then one composed V1 timeline.

Director notes on the v1 previz -> what this does:
  1 "jumps are odd"      eye-match dissolves (analysis/transitions_v2.json) instead of hard cuts
  2 "videos unstable"    eye-lock: the crop follows the tracked eyes (analysis/eye_tracks_v2.json, tools/track_eyes.py)
  3 "not cinematic"      dissolves + a bloom flash on the rhythm drop (replaces the flat dip to white)
  4 "grading not there"  per-shot primary baked here (grey balance + exposure to one target, so shots match) and a
                         pre-look halation glow; the G2 Gold & Shadow look itself stays a .cube on Premiere's V3 layer.
Stage 1: renders/bakes_v2/NN_<key>.mov  (each shot + handles, ProRes 422 HQ 1080x1920 25 fps)
Stage 2: renders/bakes_v2/V1_timeline_v2.mov (550 frames: fade-in, dissolves, bloom, freeze, last frame black)
Usage: python tools/bake_v2.py [--only 4,8] [--compose-only]
"""
import json, subprocess, math, argparse
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

FPS = 25; REEL = Path(__file__).resolve().parents[1]; OUT = REEL / "renders" / "bakes_v4"
DEC = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc"
EDL = json.loads((REEL / "analysis/edl_v3.json").read_text())
TR = json.loads((REEL / "analysis/transitions_v4.json").read_text())
TRK = json.loads((REEL / "analysis/eye_tracks_v4.json").read_text())
ROWS = {f"{r['shoot']}:{r['clip_id'].split('_')[-1]}": r for r in json.loads((REEL / "analysis/survey/eyes_candidates.json").read_text())}
HAL = 0.22            # G2 halation strength (tools/grade_options.py)
LAST = 549            # last picture frame; frame 549 is black, the audio ends at 550 (22.00 s)

def tl_frame(t):
    x = t * FPS; f = math.floor(x); return f if x - f <= 0.5 else f + 1
def luma(x): return x @ np.array([0.2126, 0.7152, 0.0722], np.float32)
def ease(f): return 0.5 - 0.5 * math.cos(math.pi * min(max(f, 0), 1))

def handles(f_in, f_out):
    hin = hout = 0
    for c in TR["cuts"]:
        if c["type"] == "dissolve":
            if c["frame"] == f_in: hin = c["L"] // 2
            if c["frame"] == f_out: hout = c["L"] // 2
    return hin, hout

def crop_box(W, H, ex, ey, cw):
    cwp = cw * W; chp = cwp * 16 / 9
    l = min(max(ex * W - cwp * 0.5, 0), W - cwp); t = min(max(ey * H - chp * 0.40, 0), H - chp)
    return (l, t, l + cwp, t + chp)

def frames(src, t0, n, rot, W, H):
    vf = DEC + (",hflip,vflip" if rot else "") + ",format=rgb24"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{max(t0,0):.4f}", "-i", src, "-frames:v", str(n), "-vf", vf,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    sz = W * H * 3
    for _ in range(n):
        b = p.stdout.read(sz)
        if len(b) < sz: break
        yield Image.frombuffer("RGB", (W, H), b, "raw", "RGB", 0, 1)
    p.stdout.close(); p.wait()

def encoder(path, pix_in="rgb24"):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", pix_in, "-s", "1080x1920", "-r", str(FPS), "-i", "-",
                             "-vf", "scale=out_color_matrix=bt709:out_range=tv", "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le",
                             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv", str(path)], stdin=subprocess.PIPE)

def reader(path):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "scale=in_range=tv:out_range=pc:in_color_matrix=bt709,format=rgb48le",
                          "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], stdout=subprocess.PIPE)
    sz = 1080 * 1920 * 6
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz: break
        yield np.frombuffer(b, "<u2").reshape(1920, 1080, 3).astype(np.float32) / 65535
    p.wait()

def primary_params(x, target=0.30, wb=0.5, exp=0.0):
    y = luma(x); m = (y > 0.10) & (y < 0.85)
    r, g, b = (x[..., i][m].mean() for i in range(3))
    gains = np.array([(g / r) ** wb, 1.0, (g / b) ** wb], np.float32)
    k = min((target / max(float(luma(x * gains).mean()), 1e-3)) ** 0.8, 2.0) * 2 ** exp
    return gains * k

def halation(x, a=HAL):
    y = luma(x); hi = np.clip((y - 0.62) / 0.38, 0, 1)[..., None] * x
    small = hi[::4, ::4]
    bl = np.stack([ndimage.gaussian_filter(small[..., c], 7) for c in range(3)], -1)
    bl = np.repeat(np.repeat(bl, 4, 0), 4, 1)[:1920, :1080] * np.array([1.0, 0.55, 0.30], np.float32)
    return 1 - (1 - x) * (1 - a * bl * 1.6)

def bloom(x, a):
    small = x[::4, ::4]
    bl = np.stack([ndimage.gaussian_filter(small[..., c], 10) for c in range(3)], -1)
    bl = np.repeat(np.repeat(bl, 4, 0), 4, 1)[:1920, :1080]
    return np.clip(1 - (1 - x) * (1 - a * (bl * 1.3 + 0.18) * np.array([1.0, 0.92, 0.80], np.float32)), 0, 1)

def smooth(v, sigma): return ndimage.gaussian_filter1d(np.asarray(v, np.float64), sigma, mode="nearest") if sigma > 0 else np.asarray(v)

def probe_wh(path):
    o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:stream_side_data=rotation",
                        "-of", "json", path], capture_output=True, text=True).stdout
    st = json.loads(o)["streams"][0]; w, h = st["width"], st["height"]
    rot = [d.get("rotation", 0) for d in st.get("side_data_list", [])]
    return (h, w) if rot and abs(rot[0]) == 90 else (w, h)

def source_info(s):
    if "src" in s:
        src = str(REEL / s["src"]); W, H = probe_wh(src); return src, bool(s.get("rot")), float(s["fps"]), W, H
    r = ROWS[s["key"]]; src = str(REEL / "raw/b-roll" / Path(r["source"]).name)
    return src, "UPSIDE" in r["orientation"], float(r["fps"]), *((2160, 3840) if "3840" in r["resolution_display"] else (1080, 1920))

def bake_shot(job):
    s0 = job[0]; key = s0["key"]; src, rot, sfps, W, H = source_info(s0)
    name = f"{s0['n']:02d}_{key.replace(':', '_')}" + ("_sweep_freeze" if len(job) == 2 else "")
    enc = encoder(OUT / f"{name}.mov"); meta = {"name": name, "parts": []}; gains = None
    for s in job:
        n = s["n"]; last_n = max(x["n"] for x in EDL["shots"]); f_in = tl_frame(s["seq_in"]); f_out = LAST if n == last_n else tl_frame(s["seq_out"]); hin, hout = handles(f_in, f_out)
        N = f_out - f_in; mode = TR["eyelock"][str(n)]
        if mode == "none":                       # freeze: one source frame, eased push about her eyes (u .5, v .40)
            im0 = next(frames(src, s["src_in"], 1, rot, W, H)); seq = [im0] * N; ex_s = [s["ex"]] * N; ey_s = [s["ey"]] * N
        elif mode == "plain":                    # full frame, frame-for-frame conform (AI clip)
            seq = frames(src, s["src_in"] - hin / sfps, N + hin + hout, rot, W, H)
        else:
            t = TRK[str(n)]
            if mode == "lock":                   # eyes pinned to the eye-line: the crop follows the (lightly smoothed) track
                ex_s = smooth(t["ex"], 1.5); ey_s = smooth(t["ey"], 1.5)
            else:                                # "smooth": keep the real camera move, cancel only the jitter
                jx = np.asarray(t["ex"]) - smooth(t["ex"], 6.0); jy = np.asarray(t["ey"]) - smooth(t["ey"], 6.0)
                taper = np.clip((len(jx) - 1 - np.arange(len(jx))) / 6.0, 0, 1)   # loop-2 fix: no compensation on the last frames,
                ex_s = s["ex"] + jx * taper; ey_s = s["ey"] + jy * taper           # so the sweep's last frame = the freeze crop
            seq = frames(src, t["src_t0"], N + hin + hout, rot, W, H)
            if "play_until" in s:                # v1c C076: play the sharp stretch, then hold its last frame
                n_play = len(t["ex"]); total_ = N + hin + hout
                seq = list(frames(src, t["src_t0"], n_play, rot, W, H)); seq = seq + [seq[-1]] * (total_ - len(seq))
                ex_s = list(ex_s) + [ex_s[-1]] * (total_ - len(ex_s)); ey_s = list(ey_s) + [ey_s[-1]] * (total_ - len(ey_s))
        total = N + (0 if mode == "none" else hin + hout); k = 0
        ov = None
        if s.get("overlay") == "esraj":         # the AI esraj continues over her eye as a Screen layer (55 %), fading out over the shot's last 0.56 s
            a = next(x for x in EDL["shots"] if x["n"] == s["n"] - 1); osrc, orot, ofps, OW, OH = source_info(a)
            ov = frames(osrc, a["src_in"] + (tl_frame(s["seq_in"]) - hin - tl_frame(a["seq_in"])) / ofps, total, orot, OW, OH)
        for im in seq:
            kk = k - (0 if mode == "none" else hin)          # frame index relative to the shot's main range
            f = kk / max(N - 1, 1)
            cw = s["cw"] + (s.get("cw_end", s["cw"]) - s["cw"]) * ease(f)
            if mode == "plain":
                box = (0, 0, W, H)
            elif mode == "none":
                cwp = cw * W; chp = cwp * 16 / 9
                l = s["ex"] * W - 0.5 * cwp; t_ = s["ey"] * H - 0.40 * chp
                l = min(max(l, 0), W - cwp); t_ = min(max(t_, 0), H - chp); box = (l, t_, l + cwp, t_ + chp)
            elif mode == "lock":
                # eyes pinned at output point (u, v); zoom about the eye; defaults: centre, the 0.40 eye-line
                u = s.get("u", 0.5); v = s.get("v", 0.40); cwp = cw * W; chp = cwp * 16 / 9
                l = ex_s[k] * W - u * cwp; t_ = ey_s[k] * H - v * chp
                l = min(max(l, 0), W - cwp); t_ = min(max(t_, 0), H - chp); box = (l, t_, l + cwp, t_ + chp)
            else:
                ex = ex_s[k]; ey = ey_s[k] + (s.get("ey_end", s["ey"]) - s["ey"]) * ease(f)
                box = crop_box(W, H, ex, ey, cw)
            rs = im.resize((1080, 1920), Image.LANCZOS, box=box)
            if s.get("prim", {}).get("sharp"):   # review v2 #3/#9: mild unsharp on the soft upscaled faces
                rs = rs.filter(ImageFilter.UnsharpMask(radius=1.6, percent=int(s["prim"]["sharp"]), threshold=3))
            fr = np.asarray(rs).astype(np.float32) / 255
            if k == 0 and s is job[0]:
                tmid = s["src_in"] + (N / 2) / sfps
                if "play_until" in s: tmid = min(tmid, s["play_until"] - 0.2)
                mid = list(frames(src, tmid, 1, rot, W, H))[0] if mode != "none" else im
                mfr = np.asarray(mid.resize((1080, 1920), Image.LANCZOS, box=crop_box(W, H, s["ex"], s["ey"], s["cw"]))).astype(np.float32) / 255
                pr = job[0].get("prim", {}) if mode != "plain" else {"wb": 0.0}
                gains = primary_params(mfr, wb=pr.get("wb", 0.5), exp=pr.get("exp", 0.0))   # one primary per clip (sweep + freeze share it)
                gains = gains * np.array(pr.get("rgb", [1.0, 1.0, 1.0]), np.float32)          # optional per-shot channel trim
                sat = pr.get("sat", 1.0)
            x = np.clip(fr * gains * (2 ** (s.get("exp_ramp", 0.0) * (1 - f)) if "exp_ramp" in s else 1.0), 0, 1)
            if sat != 1.0:
                yy = luma(x)[..., None]; x = np.clip(yy + (x - yy) * sat, 0, 1)
            if "blk" in pr: x = np.clip((x - pr["blk"]) / (1 - pr["blk"]), 0, 1)   # review v2 #3: black point (C163 incense haze)
            if "lift" in pr: x = pr["lift"] + (1 - pr["lift"]) * x                  # review v2 #7: lift (C037 corner under the vignette)
            if "green" in pr:   # review v3 #4: pull green-dominant pixels toward neutral (C056's lime glass panel), k = how much green survives
                mrb = np.maximum(x[..., 0], x[..., 2]); g = x[..., 1]; x[..., 1] = np.where(g > mrb, mrb + (g - mrb) * pr["green"], g)
            if ov is not None:
                o = np.asarray(next(ov).resize((1080, 1920), Image.LANCZOS)).astype(np.float32) / 255
                tl = f_in - hin + k; fo = float(np.clip(1 - (tl - f_in) / 16.0, 0, 1))   # review v3 #1: ghost gone by f_in+16 (2.80 s) so the title (from 2.40) never reads over the instrument   # v2 fix: ghost clears by ~0.9 s so the eye gets a clean beat
                x = 1 - (1 - x) * (1 - 0.45 * fo * o)
            x = halation(x)
            enc.stdin.write((np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes()); k += 1
        if k != total: raise SystemExit(f"row {n}: wrote {k} of {total}")
        meta["parts"].append({"n": n, "f_in": f_in, "f_out": f_out, "hin": 0 if mode == "none" else hin, "hout": 0 if mode == "none" else hout, "frames": k})
    enc.stdin.close(); enc.wait(); meta["gains"] = [round(float(g), 4) for g in gains]
    print(name, meta["parts"], "gains", meta["gains"], flush=True); return meta

def compose(metas):
    # timeline -> (file, frame index) lists; dissolve alphas; bloom
    segs = []
    for m in metas:
        off = 0
        for p in m["parts"]:
            segs.append({"file": OUT / f"{m['name']}.mov", "n": p["n"], "f_in": p["f_in"], "f_out": p["f_out"], "hin": p["hin"], "hout": p["hout"], "off": off})
            off += p["frames"]
    segs.sort(key=lambda s: s["f_in"])
    files = {}
    def get(path, idx):   # sequential frame access per file
        st = files.get(path)
        if st is None or st["pos"] > idx:
            st = {"gen": reader(path), "pos": 0, "cur": None}; files[path] = st
        while st["pos"] <= idx:
            st["cur"] = next(st["gen"]); st["pos"] += 1
        return st["cur"]
    diss = {c["frame"]: c for c in TR["cuts"]}
    enc = encoder(OUT / "V1_timeline_v4.mov", "rgb48le")
    for t in range(550):
        if t >= LAST: x = np.zeros((1920, 1080, 3), np.float32)
        else:
            layers = []
            for s in segs:
                lo = s["f_in"] - s["hin"]; hi = s["f_out"] + s["hout"]
                if lo <= t < hi: layers.append(s)
            if len(layers) == 1:
                s = layers[0]; x = get(s["file"], s["off"] + (t - s["f_in"] + s["hin"]))
            else:
                a_s, b_s = layers[0], layers[1]; c = diss[b_s["f_in"]]; L = c["L"]
                u = (t - (b_s["f_in"] - L // 2) + 0.5) / L
                xa = get(a_s["file"], a_s["off"] + (t - a_s["f_in"] + a_s["hin"])); xb = get(b_s["file"], b_s["off"] + (t - b_s["f_in"] + b_s["hin"]))
                x = xa * (1 - u) + xb * u
            if t < 8: x = x * (t / 8)                                   # fade in from black
            b = {196: 0.5, 197: 1.0, 198: 0.55, 199: 0.25}.get(t)      # bloom flash on the rhythm drop
            if b: x = bloom(x, b)
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); print("V1_timeline_v4.mov: 550 frames")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default=""); ap.add_argument("--compose-only", action="store_true")
    a = ap.parse_args(); OUT.mkdir(parents=True, exist_ok=True); only = {int(x) for x in a.only.split(",") if x}
    shots = {s["n"]: s for s in EDL["shots"]}; last = max(shots); jobs = [[shots[n]] for n in range(1, last - 1)] + [[shots[last - 1], shots[last]]]
    mpath = OUT / "bakes_v2.json"; metas = {m["name"]: m for m in json.loads(mpath.read_text())} if mpath.exists() else {}
    if not a.compose_only:
        for job in jobs:
            if only and not ({s["n"] for s in job} & only): continue
            m = bake_shot(job); metas[m["name"]] = m
        mpath.write_text(json.dumps(sorted(metas.values(), key=lambda m: m["parts"][0]["f_in"]), indent=1))
    compose(sorted(metas.values(), key=lambda m: m["parts"][0]["f_in"]))

if __name__ == "__main__":
    main()
