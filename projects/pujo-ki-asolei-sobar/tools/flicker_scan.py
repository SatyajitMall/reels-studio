#!/usr/bin/env python3
"""Mains-flicker scan (director, 2026-10-23: 1/60 s shutter under India's 50 Hz mains -> 100 Hz light flicker).
At 30 fps, 100 Hz aliases to |100 - 3*30| = 10 Hz (a 3-frame cycle); with a rolling shutter it can also show as horizontal
bands that roll.  Per shot: global log-luma spectrum (peak frequency, 10 Hz amplitude in %), plus per-row-band 10 Hz
amplitude and phase spread (banding = phase changes with y).
Usage: flicker_scan.py <suffix> [<suffix for shot 1>]   e.g. v5b v5   -> analysis/flicker/scan_<suffix>.json
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
SUF = sys.argv[1]; SUF1 = sys.argv[2] if len(sys.argv) > 2 else SUF
def frames(p, w=135, h=240):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
def amp10(x):
    """10 Hz (period-3) amplitude of a series, in % of its level, after removing a slow trend (lock-in on 10 Hz)."""
    L = np.log(np.maximum(x, 1)); n = len(L); t = np.arange(n)
    tr = np.convolve(np.pad(L, 4, mode="edge"), np.ones(9) / 9, "valid")
    r = L - tr; c = np.cos(2 * np.pi * t / 3); s = np.sin(2 * np.pi * t / 3)
    a, b = 2 * (r * c).mean(), 2 * (r * s).mean()
    return 100 * np.hypot(a, b), np.arctan2(b, a), r
out = {}
edl = json.loads((REEL / "analysis/edl_v5.json").read_text())
for s in edl["shots"]:
    suf = SUF1 if s["n"] == "1" else SUF
    js = R / f"{int(s['n']):02d}_{s['clip']}_{suf}.json"
    if not js.exists(): continue
    r = json.loads(js.read_text()); a0 = round(r["place_in"] * 30); nf = s["endF"] - s["startF"]
    F = frames(R / r["file"])[a0:a0 + nf]
    g = F.reshape(len(F), -1).mean(1); A, ph, res = amp10(g)
    spec = np.abs(np.fft.rfft(res * np.hanning(len(res)))); fr = np.fft.rfftfreq(len(res), 1 / 30); pk = fr[1:][np.argmax(spec[1:])]
    bands = [amp10(F[:, y:y + 20].reshape(len(F), -1).mean(1))[:2] for y in range(0, 240, 20)]
    ba = [round(b[0], 2) for b in bands]; bp = np.unwrap([b[1] for b in bands])
    out[s["n"]] = {"clip": s["clip"], "file": r["file"], "amp10_pct": round(A, 2), "peak_hz": round(float(pk), 2),
                   "band_amp_pct": ba, "band_phase_span_deg": round(float(np.degrees(bp.max() - bp.min())), 1),
                   "frame_jump_p95_pct": round(float(np.percentile(np.abs(np.diff(np.log(g))) * 100, 95)), 2)}
    o = out[s["n"]]; print(f"{s['n']:>2} {s['clip']} 10Hz {o['amp10_pct']:5.2f}%  peak {o['peak_hz']:5.2f} Hz  bands max {max(ba):5.2f}% phase span {o['band_phase_span_deg']:6.1f}°  p95 step {o['frame_jump_p95_pct']:.2f}%", flush=True)
(REEL / f"analysis/flicker/scan_{SUF}.json").write_text(json.dumps(out, indent=1))
