#!/usr/bin/env python3
"""Bake every V1 shot of the EDL into a reel-ready 1080x1920 25 fps ProRes 422 HQ clip of EXACTLY its timeline length.

Per shot: frame-for-frame conform to 25 fps (30 fps sources play 0.83x, as interpretation would), 180-degree fix for
upside-down clips, the eye-line-locked 9:16 crop (eye centre ex/ey, crop width cw) with eased push (cw_end/ey_end),
crop-follow (track), freeze (repeat one source frame), plus the planned fade-in (shot 1) and the 3-frame dip to white
at the 7.88 s cut (shots 2/3). Rows 10 (sweep) and 11 (freeze) are baked as ONE clip, so the sweep lands on the
freeze frame with no colour or position jump. No colour work here: primary correction + look stay in Premiere.

Why bake (logged in project.md): Premiere Motion keyframes on frame-rate-interpreted clips, still-image default scaling
and frame holds are all unverified or broken through the MCP (premiere-mcp-reality.md); a bake makes framing exact
and leaves Premiere to assemble, grade, type and mix.

Usage: python tools/bake_shots.py analysis/edl_v1.json renders/bakes [--only 1,11] [--preview]
Writes renders/bakes/NN_<shoot>_<clip>.mov + bakes.json (timeline frames, source ranges, files).
"""
import json, sys, subprocess, math, argparse
from pathlib import Path
import numpy as np
from PIL import Image

FPS = 25
REEL = Path(__file__).resolve().parents[1]
DEC = "scale=in_color_matrix=bt709:in_range=tv:out_range=pc"   # sources: HEVC 8-bit, tv range, BT.709

def tl_frame(t):            # nearest frame, ties down (cut on or just before the beat)
    x = t * FPS; f = math.floor(x)
    return f if x - f <= 0.5 else f + 1

def ease(f): return 0.5 - 0.5 * math.cos(math.pi * f)

def crop_box(W, H, ex, ey, cw):
    cwp = cw * W; chp = cwp * 16 / 9
    l = min(max(ex * W - cwp * 0.5, 0), W - cwp); t = min(max(ey * H - chp * 0.40, 0), H - chp)
    return (l, t, l + cwp, t + chp)

def at(s, f):
    """crop params at shot fraction f (0..1)."""
    fe = ease(f)
    cw = s["cw"] + (s.get("cw_end", s["cw"]) - s["cw"]) * fe
    ex, ey = s["ex"], s["ey"] + (s.get("ey_end", s["ey"]) - s["ey"]) * fe
    if "track" in s:   # measured camera drift: follow linearly (not eased)
        tr = s["track"]
        for a, b in zip(tr, tr[1:]):
            if a[0] <= f <= b[0]:
                u = 0 if b[0] == a[0] else (f - a[0]) / (b[0] - a[0]); ex, ey = a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
    return ex, ey, cw

def frames(src, t0, n, rot, W, H):
    vf = DEC + (",hflip,vflip" if rot else "") + ",format=rgb24"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", src, "-frames:v", str(n), "-vf", vf,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    sz = W * H * 3
    for _ in range(n):
        b = p.stdout.read(sz)
        if len(b) < sz: break
        yield Image.frombuffer("RGB", (W, H), b, "raw", "RGB", 0, 1)
    p.stdout.close(); p.wait()

def encoder(path):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", str(FPS),
                             "-i", "-", "-vf", "scale=out_color_matrix=bt709:out_range=tv", "-c:v", "prores_ks", "-profile:v", "3",
                             "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                             "-color_range", "tv", str(path)], stdin=subprocess.PIPE)

def mix(im, colour, a):
    if a <= 0: return im
    return Image.blend(im, Image.new("RGB", im.size, colour), min(a, 1.0))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("edl"); ap.add_argument("out"); ap.add_argument("--only", default="")
    a = ap.parse_args(); edl = json.loads(Path(a.edl).read_text()); out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    rows = {f"{r['shoot']}:{r['clip_id'].split('_')[-1]}": r for r in json.loads((REEL / "analysis/survey/eyes_candidates.json").read_text())}
    shots = {s["n"]: s for s in edl["shots"]}
    only = {int(x) for x in a.only.split(",") if x}
    # timeline frames per row; the last picture frame is 549 (21.96 s), one black frame before the audio ends at 22.0 s
    for s in edl["shots"]:
        s["f_in"] = tl_frame(s["seq_in"]); s["f_out"] = 549 if s["n"] == 11 else tl_frame(s["seq_out"])
    jobs = [[shots[n]] for n in range(1, 10)] + [[shots[10], shots[11]]]
    log = []
    for job in jobs:
        n0 = job[0]["n"]
        if only and not ({s["n"] for s in job} & only): continue
        key = job[0]["key"]; r = rows[key]; src = str(REEL / "raw" / "b-roll" / Path(r["source"]).name)
        rot = "UPSIDE" in r["orientation"]; sfps = float(r["fps"])
        W, H = (2160, 3840) if "2160" in r["resolution_display"] or "3840" in r["resolution_display"] else (1080, 1920)
        name = f"{n0:02d}_{key.replace(':', '_')}" + ("_sweep_freeze" if len(job) == 2 else "")
        path = out / f"{name}.mov"; enc = encoder(path); total = 0; ent = {"rows": [s["n"] for s in job], "file": str(path.relative_to(REEL)), "src": src, "rot180": rot}
        for s in job:
            N = s["f_out"] - s["f_in"]
            if s.get("freeze"):
                im0 = next(frames(src, s["src_in"], 1, rot, W, H)); seq = (im0 for _ in range(N)); src_rng = [s["src_in"], s["src_in"]]
            else:
                seq = frames(src, s["src_in"], N, rot, W, H); src_rng = [s["src_in"], round(s["src_in"] + N / sfps, 3)]
            k = 0
            for im in seq:
                f = k / max(N - 1, 1); ex, ey, cw = at(s, f)
                fr = im.resize((1080, 1920), Image.LANCZOS, box=crop_box(W, H, ex, ey, cw))
                if s["n"] == 1 and k < 8: fr = mix(fr, (0, 0, 0), 1 - k / 8)                      # fade in from black 0-0.3 s
                if s["n"] == 2 and k == N - 1: fr = mix(fr, (255, 255, 255), 0.5)                # dip to white: 50 %
                if s["n"] == 3 and k == 0: fr = mix(fr, (255, 255, 255), 1.0)                    #   on the beat frame: 100 %
                if s["n"] == 3 and k == 1: fr = mix(fr, (255, 255, 255), 0.4)                    #   then 40 %
                enc.stdin.write(fr.tobytes()); k += 1
            if k != N: raise SystemExit(f"row {s['n']}: got {k} of {N} frames (source too short?)")
            total += N; ent.setdefault("parts", []).append({"n": s["n"], "frames": N, "tl_in": s["f_in"], "tl_out": s["f_out"], "src_real": src_rng})
        enc.stdin.close(); enc.wait(); ent["tl_in"] = job[0]["f_in"]; ent["tl_out"] = job[-1]["f_out"]; ent["frames"] = total
        log.append(ent); print(f"{name}: tl {ent['tl_in']}-{ent['tl_out']} ({total} fr) rot={rot}", flush=True)
    bj = out / "bakes.json"
    old = {e["file"]: e for e in json.loads(bj.read_text())} if bj.exists() else {}
    for e in log: old[e["file"]] = e
    bj.write_text(json.dumps(sorted(old.values(), key=lambda e: e["tl_in"]), indent=1))

if __name__ == "__main__":
    main()
