#!/usr/bin/env python3
"""Round 3 shot renderer (v2 pipeline; LOOK = warm cinematic look matched to the director's Bangkok film + per-shot warm cast match;
25 fps sources conformed: every frame kept, played at 30).
Round 2 notes: (director: "bokeh not ok, render without; correction, stability and clarity need to improve").

  4K source -> [punch-in crop] -> temporal+spatial denoise (hqdn3d, at 4K) -> lanczos down to 1188x2112 (10 % margin)
  -> STABILISE: phase-correlation translation per frame, camera path smoothed (gaussian), correction crop 1080x1920
     taken from the margin (no upscaling, no resolution loss)
  -> CORRECTION: white balance from near-neutral (low-chroma) pixels + per-shot tonal match (p02/p50/p98 -> targets),
     constants per shot measured on the frames that are on screen
  -> CLARITY: fine detail sharpen + local-contrast "clarity" on luminance
  -> optional lens bokeh (off by default) -> sepia film look -> halation, vignette, finer grain -> shared floor + luma match
  -> ProRes 422 HQ 1080x1920 @ 30 + source audio, 0.3 s handles.
Usage: shot_render_v2.py <n> [--ver v2] [--bokeh]
"""
import json, subprocess, sys, time, tempfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import sepia_look as sl  # noqa: E402  (luma helper)
import cine_look as cl  # noqa: E402
CP = json.loads((REEL / 'analysis' / 'cine_look_params.json').read_text())
from preview_sepia_bokeh_lib import optical  # noqa: E402

n = sys.argv[1]
VER = sys.argv[sys.argv.index("--ver") + 1] if "--ver" in sys.argv else "v5"
EDLV = sys.argv[sys.argv.index("--edl") + 1] if "--edl" in sys.argv else "v5"
BOKEH = "--bokeh" in sys.argv
NAT = "--natural" in sys.argv or "--natural-matched" in sys.argv   # round 11 (director: "over processed, not natural"): partial strengths, no clarity
NM = "--natural-matched" in sys.argv   # director's pick: "natural, but warmer and matched": stronger match + look than --natural
S_WB, S_LEV, S_CAST, S_LOOK, S_SKIN, S_SAT = (0.6, 0.65, 0.6, 0.75, 0.75, 0.38) if NM else (0.45, 0.5, 0.35, 0.6, 0.5, 0.40)
edl = json.loads((REEL / "analysis" / f"edl_{EDLV}.json").read_text()); s = next(x for x in edl["shots"] if x["n"] == n)
f = json.loads((REEL / "analysis" / f"focus_{EDLV}.json").read_text())[n]
if NAT:   # per-shot overrides of the natural strengths (gate v11: C027 read as a sepia filter)
    S_WB, S_CAST, S_LOOK = f.get("wb_k", S_WB), f.get("cast_k", S_CAST), f.get("look_mix", S_LOOK)
src = next((REEL / "raw" / "b-roll").glob(f"*_{s['clip']}.mov"))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
SF = float(s.get('src_fps', 30)); CONFORM = SF < 28
nfr = s['endF'] - s['startF']
handle = 0.3; t0 = max(0.0, s['in'] - handle); t1 = min(dur - 0.04, s['in'] + nfr / SF + handle)
out_dir = REEL / "renders" / "final_shots"; out_dir.mkdir(parents=True, exist_ok=True)
name = f"{int(n):02d}_{s['clip']}_{VER}"; mov = out_dir / f"{name}.mov"
W, H = 1080, 1920
MG = f.get("stab_margin", 1.10)                                     # 1.10 -> 54 / 96 px margin; shakier shots more
MW, MH = int(round(W * MG / 2)) * 2, int(round(H * MG / 2)) * 2; MW -= MW % 4; MH -= MH % 4
MX, MY = (MW - W) // 2, (MH - H) // 2
T = time.time()

# 1) decode: crop -> denoise at 4K -> supersample down to the margin frame
dn = f.get("denoise", "hqdn3d=0.8:0.6:2:1.5" if NAT else "hqdn3d=1.5:1.2:6:4.5")
vf = (f"crop={f['crop']}," if f.get("crop") else "") + f"{dn},scale={MW}:{MH}:flags=lanczos" + ("" if CONFORM else ",fps=30")
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(src), "-an", "-vf", vf,
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, MH, MW, 3); N = len(frames)
print(f"▸ {name}: src {t0:.2f}-{t1:.2f}, {N} frames, decode {time.time() - T:.0f}s", flush=True)
pa = int(round((s['in'] - t0) * (SF if CONFORM else 30))); pb = min(N - 1, pa + nfr - 1)

# 2) stabilise (v4): similarity (translation + roll + zoom) from a grid of patches, RANSAC; lock static scenes when the
#    margin allows, else strong smoothing; corrections must keep the output window inside the margin frame.
import stab2  # noqa: E402
def gray_small(fr):
    g = fr.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
    return g.reshape(MH // 4, 4, MW // 4, 4).mean(axis=(1, 3))
smalls = [gray_small(fr) for fr in frames]
Ts = stab2.estimate(smalls, ps=40)
cx, cy = MW / 2, MH / 2
def fits(corr):
    xs = np.array([MX, MX + W - 1, MX, MX + W - 1]); ys = np.array([MY, MY, MY + H - 1, MY + H - 1])
    for C in corr[max(0, pa - 2):pb + 3]:
        xi = C[0, 0] * xs + C[0, 1] * ys + C[0, 2]; yi = C[1, 0] * xs + C[1, 1] * ys + C[1, 2]
        if xi.min() < 0 or yi.min() < 0 or xi.max() > MW - 1 or yi.max() > MH - 1: return False
    return True
mode = "lock" if f.get("stab_lock") else "smooth"
sig = float(f.get("stab_sigma", 30))
if mode == "lock":
    corr, path, smooth = stab2.plan(Ts, 4.0, cx, cy, lock=(pa, pb))
    if not fits(corr): mode = "smooth"; sig = max(sig, 45)
while mode == "smooth":
    corr, path, smooth = stab2.plan(Ts, 4.0, cx, cy, sigma=sig)
    if fits(corr) or sig < 4: break
    sig *= 0.7
# second pass: residual motion measured on the stabilised (small) frames, corrected again (lock / smooth as above)
S4 = np.diag([4.0, 4.0, 1.0]); S4i = np.linalg.inv(S4); Toff = np.array([[1, 0, MX], [0, 1, MY], [0, 0, 1.0]]); Toffi = np.linalg.inv(Toff)
def small_warp(g, C):
    Cs = S4i @ C @ S4; return stab2.warp(g[..., None], Cs, (H // 4, W // 4), (MY // 4, MX // 4))[..., 0]
st_smalls = [small_warp(smalls[i], corr[i]) for i in range(N)]
Ts2 = stab2.estimate(st_smalls, ps=36)
if mode == "lock": c2, p2, s2 = stab2.plan(Ts2, 4.0, W / 2, H / 2, lock=(pa, pb))
else: c2, p2, s2 = stab2.plan(Ts2, 4.0, W / 2, H / 2, sigma=sig)
corr_ref = [C @ Toff @ C2 @ Toffi for C, C2 in zip(corr, c2)]
if fits(corr_ref):
    r2 = (p2 - s2)[pa:pb + 1]; print(f"  pass 2: removed {np.sqrt((r2[:, :2] ** 2).sum(1).mean()):.2f}px + {np.degrees(np.sqrt((r2[:, 2] ** 2).mean())):.3f}deg", flush=True)
    corr = corr_ref
else: print("  pass 2: skipped (margin)", flush=True)
hf = path[pa:pb + 1] - smooth[pa:pb + 1]
raw_jit = float(np.sqrt((hf[:, :2] ** 2).sum(1).mean()))
print(f"  stabilise v4: mode {mode}{'' if mode == 'lock' else f' sigma {sig:.1f}'}, removed {raw_jit:.2f}px + {np.degrees(np.sqrt((hf[:, 2] ** 2).mean())):.3f}deg roll", flush=True)
def stab(fr, i):
    return stab2.warp(fr.astype(np.float32) / 255, corr[i], (H, W), (MY, MX))

# 3) correction constants from on-screen frames
def wb_gains(x):
    y = sl.luma(x); mx = x.max(-1); mn = x.min(-1); ch = (mx - mn) / np.maximum(mx, 1e-4)
    m = (y > 0.12) & (y < 0.85)
    if m.sum() < 1000: m = y > 0.03
    cut = np.percentile(ch[m], 30); m = m & (ch <= cut)                 # near-neutral pixels only (walls, cloth, skin shadows)
    R, G, B = (np.median(x[..., c][m]) for c in range(3))
    pw = S_WB if NAT else 0.9                                              # natural: half-way to neutral, the scene's light stays
    return np.array([(G / max(R, 1e-4)) ** pw, 1.0, (G / max(B, 1e-4)) ** pw])
samp = [stab(frames[i], i) for i in np.linspace(pa, pb, 6).astype(int)]
wb = np.median([wb_gains(x) for x in samp], axis=0)
ys = np.concatenate([sl.luma(np.clip(x * wb, 0, 1)).ravel()[::7] for x in samp])
p02, p50, p98 = np.percentile(ys, [2, 50, 98])
TIN = np.array([0.0, p02, p50, p98, 1.0]); TOUT = np.array([0.0, 0.035, 0.30, 0.86, 0.97])
if NAT: TOUT = S_LEV * TOUT + (1 - S_LEV) * TIN                          # natural: partial auto-levels
TIN = np.maximum.accumulate(TIN + np.arange(5) * 1e-4)
def correct(x):
    x = np.clip(x * wb, 0, 1.2); y = np.clip(sl.luma(x), 1e-5, None)
    y2 = np.interp(y, TIN, TOUT); return np.clip(x * (y2 / y)[..., None], 0, 1)
print(f"  correction: wb {np.round(wb, 3)}, tonal p02/p50/p98 {p02:.3f}/{p50:.3f}/{p98:.3f}", flush=True)

# 4) clarity on luminance
CL = f.get("clarity", (0.12, 0.0) if NAT else (0.55, 0.20))
def clarity(x):
    y = sl.luma(x)
    det = y - ndimage.gaussian_filter(y, 1.1); loc = y - ndimage.gaussian_filter(y, 22)
    y2 = np.clip(y + CL[0] * det + CL[1] * loc, 0, 1)
    return np.clip(x * (y2 / np.maximum(y, 1e-4))[..., None], 0, 1)

TARGET, FLOOR = 0.28, 0.025
lensmod = None
if BOKEH:
    import lens as lensmod  # noqa: E402
TR, TB, KR = CP.get('cast_target', [1.05, 0.80]) + [S_CAST if NAT else 0.8]
def cast_gains(x):
    y = sl.luma(x); mx = x.max(-1); mn = x.min(-1); ch = (mx - mn) / np.maximum(mx, 1e-4)
    m = (y > 0.18) & (y < 0.7) & (ch < 0.35)
    if m.sum() < 500: m = (y > 0.15) & (y < 0.8)
    R, G, B = (x[..., c][m].mean() for c in range(3))
    return np.array([(TR * G / R) ** KR, 1.0, (TB * G / B) ** KR])
_s = [cl.look(clarity(correct(stab(frames[i], i))), CP) for i in np.linspace(pa, pb, 5).astype(int)]
CG = np.median([cast_gains(x[::4, ::4]) for x in _s], axis=0)
def satm(x):
    mx = x.max(-1); mn = x.min(-1); return float(((mx - mn) / np.maximum(mx, 1e-6)).mean())
SATMAX = S_SAT if NAT else CP.get('sat_cap', 0.34)
_sm = np.mean([satm(np.clip(x * CG, 0, 1)[::4, ::4]) for x in _s])
SK = min(1.0, SATMAX / max(_sm, 1e-3)) ** 1.15                    # per-shot chroma cap (director: colour too strong)
print(f'  cast gains {np.round(CG, 3)}  sat {_sm:.3f} -> k {SK:.3f}', flush=True)
import skin_match  # noqa: E402
def _pre(i):
    x = np.clip(cl.look(clarity(correct(stab(frames[i], i))), CP) * CG, 0, 1)
    if SK < 0.999: yy = sl.luma(x)[..., None]; x = np.clip(yy + (x - yy) * SK, 0, 1)
    return x
if f.get('skin', True):
    _sk = [_pre(i)[::2, ::2] for i in np.linspace(pa, pb, 5).astype(int)]
    with tempfile.TemporaryDirectory(prefix='skin_') as _td: _pp = skin_match.people_alphas(_sk, _td)
    print(f'  person mattes: {sum(a is not None for a in _pp)}/5, coverage {np.mean([a.mean() for a in _pp if a is not None]) if any(a is not None for a in _pp) else 0:.2f}', flush=True)
    SKG, SKK = skin_match.solve_iter(_sk, people=_pp)
else: SKG, SKK = np.ones(3), 1.0
print(f'  skin anchor: gains {np.round(SKG, 3)} sat k {SKK:.2f}', flush=True)
LOOKMIX = S_LOOK if NAT else 1.0
def treat(i, gain=1.0):
    x = clarity(correct(stab(frames[i], i)))
    x = np.clip((LOOKMIX * cl.look(x, CP) + (1 - LOOKMIX) * x) * CG, 0, 1)
    if SK < 0.999: yy = sl.luma(x)[..., None]; x = np.clip(yy + (x - yy) * SK, 0, 1)
    x = skin_match.apply_full(x, SKG ** S_SKIN, SKK ** S_SKIN) if NAT else skin_match.apply_full(x, SKG, SKK)
    o = optical(x, seed=i, hal=(0.06 if NM else 0.05) if NAT else f.get("hal", 0.10), vig=(0.12 if NM else 0.10) if NAT else f.get("vig", 0.18), grain=0.006 if NAT else f.get("grain", 0.010))
    o = FLOOR + (o - FLOOR) * gain
    return np.clip(o, FLOOR - 0.005, 1)
mids = [treat(i) for i in np.linspace(pa, pb, 5).astype(int)]
gain = float(np.clip((TARGET - FLOOR) / max(np.mean([sl.luma(m).mean() for m in mids]) - FLOOR, 1e-3), 0.75, 1.6))
print(f"  luma gain {gain:.3f}", flush=True)

enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(out_dir / f"{name}_v.mov")], stdin=subprocess.PIPE)
for i in range(N):
    enc.stdin.write((treat(i, gain) * 255 + 0.5).clip(0, 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out_dir / f"{name}_v.mov"), "-ss", f"{t0:.3f}", "-t", f"{N / (SF if CONFORM else 30):.3f}", "-i", str(src),
                "-map", "0:v", "-map", "1:a?", "-c:v", "copy", "-c:a", "pcm_s16le"] + (["-af", f"atempo={30 / SF:.4f}"] if CONFORM else []) + ["-shortest", str(mov)], check=True)
(out_dir / f"{name}_v.mov").unlink()
rec = {"n": n, "clip": s["clip"], "file": mov.name, "src_start": round(t0, 4), "frames": N, "place_in": round(pa / 30, 4),
       "place_out": round((pa + nfr) / 30, 4), "conform": CONFORM, "sat_k": round(SK, 3), "skin_gains": [round(float(v), 4) for v in SKG], "skin_sat_k": round(float(SKK), 3), "cast_gains": [round(float(v), 4) for v in CG], "wb": [round(float(v), 4) for v in wb],
       "tonal_in": [round(float(v), 4) for v in (p02, p50, p98)], "raw_jitter_px": round(raw_jit, 2), "stab_mode": mode, "stab_sigma": round(sig, 1), "luma_gain": round(gain, 3),
       "bokeh": BOKEH, "secs": round(time.time() - T)}
(out_dir / f"{name}.json").write_text(json.dumps(rec, indent=1)); print(f"✓ {name} {N} frames in {rec['secs']}s", flush=True)
