#!/usr/bin/env python3
"""Round 9: build each timeline shot from its graded, deflickered render: speed segments (optical-flow slow motion via
ffmpeg minterpolate for speed < 1, straight frames at 1x), hidden cuts between segments, 5-frame handles where the source
allows (the 886 dissolve needs them), natural sound kept only under 1x segments (silence under slow motion).
Writes renders/final_shots/<NN>_<clip>_v9f.mov + .json (place_in = handle before the shot).  Shots that are plain 1x
windows of an existing render get only a json pointing at that render.
Usage: v9_build.py [shot n ...] [--edl v9] [--out v9f]"""
import json, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
def _opt(k, dflt): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else dflt
EDLV, OUTV = _opt("--edl", "v9"), _opt("--out", "v9f")
E = json.loads((REEL / f"analysis/edl_{EDLV}.json").read_text()); W, H, HD = 1080, 1920, 5
only = {a for a in sys.argv[1:] if a.isdigit()}
def frames_of(path, a, b):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"select='between(n,{a},{b})'", "-fps_mode", "passthrough",
                          "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint16).reshape(-1, H, W, 3)
MI_DEFAULT = "mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1"
def slow(path, r0, n_out, speed, nb=10**9, mi=MI_DEFAULT):
    """n_out frames starting at render frame r0, spaced `speed` render frames apart (optical flow)."""
    a = int(np.floor(r0)); b = min(int(np.ceil(r0 + n_out * speed)) + 2, nb - 1)
    with tempfile.TemporaryDirectory() as td:
        seg = Path(td) / "s.mov"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vf", f"select='between(n,{a},{b})',setpts=N/30/TB", "-fps_mode", "passthrough",
                        "-c:v", "prores_ks", "-profile:v", "3", "-an", str(seg)], check=True)
        fps = 30 / speed
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(seg), "-vf",
                              f"minterpolate=fps={fps:.5f}:{mi},setpts=N/30/TB",
                              "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
    F = np.frombuffer(raw, np.uint16).reshape(-1, H, W, 3)
    k0 = int(round((r0 - a) / speed))
    if len(F) > k0 + n_out and np.array_equal(F[k0], F[k0 + 1]): k0 += 1     # minterpolate repeats its first frame (gate v10 #7)
    return F[k0:k0 + n_out]
for s in E["shots"]:
    if only and s["n"] not in only: continue
    pat = f"*_{s['clip']}_{s['base']}.json"
    bj = json.loads(next(R.glob(pat)).read_text())
    def src_of(seg):
        """(json, path, file-frame rate, frame count) of the render a segment reads; seg["json"] picks another render (round 10)."""
        j = json.loads((R / seg["json"]).read_text()) if seg.get("json") else bj
        pth = R / j["file"]
        k = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(pth)], capture_output=True, text=True).stdout)
        return j, pth, (25 if j.get("conform") else 30), k
    def r_of(seg):
        j, _, fr, _ = src_of(seg)
        return round(j["place_in"] * 30) + seg["off"] if "off" in seg else (seg["t"] - j["src_start"]) * fr   # place_in is in file frames / 30
    segs = [dict(x) for x in s["segments"]]
    # handles: extend first / last segment by up to HD frames where the render has them
    pre = min(HD, int((r_of(segs[0])) // segs[0]["speed"]) - 1); pre = max(pre, 0)
    last = segs[-1]; n_last = last["tl"][1] - last["tl"][0]
    nb_last = src_of(last)[3]
    post = min(HD, int((nb_last - 3 - (r_of(last) + n_last * last["speed"])) // last["speed"])); post = max(post, 0)
    plain = len(segs) == 1 and segs[0]["speed"] == 1 and not segs[0].get("json")
    if plain:   # json only: a window of the existing render
        r0 = r_of(segs[0]); out = dict(bj, place_in=round(r0 / 30, 5), place_out=round((r0 + s["endF"] - s["startF"]) / 30, 5), v9=s)
        (R / f"{int(s['n']):02d}_{s['clip']}_{OUTV}.json").write_text(json.dumps(out, indent=1)); print(f"✓ {s['n']} {s['clip']} window of {bj['file']} @ {r0}", flush=True); continue
    pieces, audio_mask = [], []
    for i, g in enumerate(segs):
        n = g["tl"][1] - g["tl"][0]; r0 = r_of(g); _, base, _, nb = src_of(g)
        if i == 0: n += pre; r0 -= pre * g["speed"]
        if i == len(segs) - 1: n += post
        if g["speed"] == 1:
            F = frames_of(base, int(round(r0)), int(round(r0)) + n - 1); audio_mask += [(base, int(round(r0)) + k) for k in range(n)]
        else:
            F = slow(base, r0, n, g["speed"], nb, g.get("mi", MI_DEFAULT)); audio_mask += [None] * n
        assert len(F) == n, (s["n"], i, len(F), n)
        if g.get("zoom"):                                   # cut-in: crop about a centre, lanczos back to full frame (per channel, 16-bit)
            from PIL import Image
            z = g["zoom"]; cw, ch = int(W / z), int(H / z); cx, cy = g.get("center", [0.5, 0.5])
            x0 = int(min(max(cx * W - cw / 2, 0), W - cw)); y0 = int(min(max(cy * H - ch / 2, 0), H - ch))
            def up(c): return np.asarray(Image.fromarray(c.astype(np.float32), mode="F").resize((W, H), Image.LANCZOS))
            F = np.stack([np.stack([up(f[y0:y0 + ch, x0:x0 + cw, c]) for c in range(3)], -1) for f in F]).clip(0, 65535).astype(np.uint16)
        pieces.append(F)
    V = np.concatenate(pieces); N = len(V)
    name = f"{int(s['n']):02d}_{s['clip']}_{OUTV}"
    # audio: source samples under 1x frames, silence under slow motion
    spf = 48000 // 30; out_a = np.zeros((N * spf, 2), np.int16); AU = {}
    for k, m in enumerate(audio_mask):
        if m is None: continue
        bp, rf = m
        if bp not in AU:
            araw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(bp), "-vn", "-ac", "2", "-ar", "48000", "-f", "s16le", "-"], capture_output=True).stdout
            AU[bp] = np.frombuffer(araw, np.int16).reshape(-1, 2) if araw else np.zeros((0, 2), np.int16)
        A = AU[bp]
        if (rf + 1) * spf <= len(A):                          # render audio runs at the file's 30 fps (conformed clips were atempo'd)
            out_a[k * spf:(k + 1) * spf] = A[rf * spf:(rf + 1) * spf]
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "a.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "48000", "-ac", "2", "-i", "-", str(wav)], input=out_a.tobytes(), check=True)
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb48le", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-i", str(wav),
                                "-map", "0:v", "-map", "1:a", "-vf", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
                                "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                                "-colorspace", "bt709", "-c:a", "pcm_s16le", "-movflags", "+write_colr", str(R / f"{name}.mov")], stdin=subprocess.PIPE)
        enc.stdin.write(V.tobytes()); enc.stdin.close(); enc.wait()
    out = dict(bj, file=f"{name}.mov", src_start=None, conform=False, place_in=round(pre / 30, 5), place_out=round((pre + s["endF"] - s["startF"]) / 30, 5),
               frames=N, v9=s, handles=[pre, post])
    (R / f"{name}.json").write_text(json.dumps(out, indent=1)); print(f"✓ {name}: {N} frames (handles {pre}/{post}), segments {[(g['speed']) for g in segs]}", flush=True)
