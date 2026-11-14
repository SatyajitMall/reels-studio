#!/usr/bin/env python3
"""Gentler voice match (director on v15, 2026-10-27: "too processed / synthetic").
v15 resynthesised every frame through a vocoder and warped timing and formants: that is where the synthetic texture came from.
Here the director's own waveform is kept and only nudged:
  place     take 6 phrases on their slots exactly as v14 (analysis/vo_place.json), no timing warp
  pitch     Praat PSOLA (overlap-add on the real waveform, formants untouched): a smaller shift toward the reference
            (--shift st) and an optional mild widening of the intonation (--range, log-F0 scale around the median)
  tone      auto matching EQ toward the reference at partial strength (--eq), gentle 1.6:1 compression, small-room tail,
            room tone; static loudness; mono; muxed on the v13 picture
Usage: vo_gentle.py --shift -3 --range 1.2 --eq 0.6 --tag v16a
v17 (director on v16a: hiccup in '18 saal ki umr mein', 'achanak se chup' and the last line rushed / unclear, nasal throughout):
  --merge2          line 2 as one phrase (no inserted pause before 'duniya'); 'duniya' still on the f165 cut
  --slow 8b:0.9,..  slow named phrases (WSOLA atempo < 1)      --t10b 33.465  start of the last phrase
  --light           lighter denoise / de-ess (consonants clearer)
  --formant 0.97    Praat 'Change gender' (PSOLA + formant shift) instead of the pitch-tier manipulation
  --eqmode smooth   a smooth corrective EQ (chest up, nasal 1 kHz down, presence, air) instead of the jagged auto-match
v18 (director on v17: still nasal, lacks the reference's calm deep sound): --shift -5 --formant 0.93 --range 1.1
  --eqmode smoothmatch --eq 0.85 (half-octave match: softer 3-5 kHz, dull top, warmer 450 Hz) --room dark
  vo_gentle.py --shift -3 --range 1.2 --merge2 --slow 8b:0.9,10b:0.93 --t10b 33.465 --light --formant 0.97 --eqmode smooth --tag v17
"""
import json, subprocess, sys, warnings
from pathlib import Path
import numpy as np
from scipy import signal
warnings.filterwarnings("ignore")
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "renders/_pylib"))
import parselmouth  # noqa: E402
from parselmouth.praat import call  # noqa: E402
def opt(k, d): return type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
SHIFT, RANGE, EQ, TAG = opt("--shift", -3.0), opt("--range", 1.2), opt("--eq", 0.6), opt("--tag", "v16a")
MERGE2, LIGHT, FORMANT, EQMODE, T10B = "--merge2" in sys.argv, "--light" in sys.argv, opt("--formant", 0.0), opt("--eqmode", "auto"), opt("--t10b", 0.0)
SLOW = {k: float(v) for k, v in (x.split(":") for x in opt("--slow", "").split(",") if x)}
A = REEL / "audio/vo_director"; PLACE = json.loads((REEL / "analysis/vo_place.json").read_text()); T0 = PLACE["reel_t0_in_take_s"]
VID = REEL / "renders/exports/pujo-ki-asolei-sobar_v13_IG.mp4"; SR, DUR = 48000, 35.8333

def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).astype(np.float64)
def ff(x, af):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
                       input=np.asarray(x, np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)
def lufs(x):
    out = subprocess.run(["ffmpeg", "-v", "info", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"],
                         input=np.asarray(x, np.float32).tobytes(), capture_output=True).stderr.decode()
    return float(out.rsplit("I:", 1)[1].split("LUFS")[0])

# place (same as v14)
clean = ff(load(A / "take_06.wav"), "highpass=f=75:poles=2," + ("afftdn=nr=7:nf=-50:tn=1,deesser=i=0.18:m=0.5:f=0.5" if LIGHT else "afftdn=nr=12:nf=-50:tn=1,deesser=i=0.35:m=0.5:f=0.5"))
rt = lambda t: int((t + T0) * SR); PRE_PAD, POST_PAD, FADE = 0.04, 0.08, 0.012
vo = np.zeros(int((DUR + 1.5) * SR)); ph = [dict(p) for p in PLACE["phrases"]]
if MERGE2:                                                       # one take of line 2, 'duniya' on the f165 cut
    i2 = next(i for i, p in enumerate(ph) if p["phrase"] == "2a"); a2, b2 = ph[i2]["src_reel_s"][0], ph[i2 + 1]["src_reel_s"][1]
    ph[i2:i2 + 2] = [{"phrase": "2", "src_reel_s": [a2, b2], "target_s": 5.50 - (ph[i2 + 1]["src_reel_s"][0] - a2), "tempo": 1}]
for p in ph:
    for k, v in SLOW.items():
        if p["phrase"].split()[0] == k: p["tempo"] = v
    if T10B and p["phrase"].startswith("10b"): p["target_s"] = T10B
for i, p in enumerate(ph):
    a, b = p["src_reel_s"]; tgt, tempo = p["target_s"], p["tempo"]; a0, b0 = a - PRE_PAD, b + POST_PAD
    if i + 1 < len(ph) and ph[i + 1]["src_reel_s"][0] > a: b0 = min(b0, ph[i + 1]["src_reel_s"][0] - 0.01)
    seg = clean[rt(a0):rt(b0)].copy()
    if tempo != 1: seg = ff(seg, f"atempo={tempo}")
    n = int(FADE * SR); w = np.ones(len(seg)); w[:n] = np.linspace(0, 1, n); w[-n:] = np.linspace(1, 0, n)
    st = int((tgt - PRE_PAD / tempo) * SR); vo[st:st + len(seg)] += seg * w

# pitch: PSOLA on the real waveform
snd = parselmouth.Sound(vo, SR)
if FORMANT:                                                      # PSOLA + gentle formant lowering in one Praat pass
    f0med = call(snd.to_pitch(0.01, 75, 400), "Get quantile", 0, 0, 0.5, "Hertz")
    y = call(snd, "Change gender", 75, 400, FORMANT, f0med * 2 ** (SHIFT / 12), RANGE, 1.0).values[0].astype(np.float64)
else:
    man = call(snd, "To Manipulation", 0.01, 75, 400); pt = call(man, "Extract pitch tier")
    npts = call(pt, "Get number of points"); tv = np.array([[call(pt, "Get time from index", i), call(pt, "Get value at index", i)] for i in range(1, npts + 1)])
    med = np.median(np.log2(tv[:, 1])); newf = 2 ** (med + SHIFT / 12 + RANGE * (np.log2(tv[:, 1]) - med))
    pt2 = call("Create PitchTier", "matched", 0, snd.duration)
    for (t, _), f in zip(tv, newf): call(pt2, "Add point", t, f)
    call([pt2, man], "Replace pitch tier"); y = call(man, "Get resynthesis (overlap-add)").values[0].astype(np.float64)
ref = load(REEL / "audio/ref_audio_vo.wav")

# tone: partial auto matching EQ (1/3 octave), lows capped (the reference's lows carry its music bed)
def ltas(x):
    f, _, S = signal.stft(x, SR, nperseg=4096, noverlap=3072); P = np.abs(S) ** 2; e = P.sum(0); k = e > np.percentile(e, 70)
    return f, P[:, k].mean(1)
f, Pr = ltas(ref); _, Py = ltas(y)
cent = 31.5 * 2 ** (np.arange(0, 30) / 3); cent = cent[cent < 16000]; g = []
for c in cent:
    m = (f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6)); g.append(10 * np.log10(Pr[m].mean() / max(Py[m].mean(), 1e-20)) if m.any() else 0)
g = np.nan_to_num(np.array(g)); g -= np.median(g[(cent > 400) & (cent < 3000)]); g = np.clip(g * EQ, -5, 5); g[cent < 300] = np.minimum(g[cent < 300], 3); g[cent < 70] = np.minimum(g[cent < 70], 0)
if EQMODE == "smoothmatch":                                      # v18: match the reference's broad shape (1/2-octave smoothed), 150 Hz-12 kHz
    c6 = 150 * 2 ** (np.arange(0, 40) / 6); c6 = c6[c6 < 12500]; gm = []
    for c in c6:
        m = (f >= c / 2 ** (1 / 12)) & (f < c * 2 ** (1 / 12)); gm.append(10 * np.log10(Pr[m].mean() / max(Py[m].mean(), 1e-20)) if m.any() else 0)
    gm = np.convolve(np.pad(np.nan_to_num(np.array(gm)), 1, mode="edge"), np.ones(3) / 3, "valid")
    gm -= np.median(gm[(c6 > 500) & (c6 < 2500)]); gm = np.clip(gm * EQ, -6, 6)
    ent = [(60, 0.0), (100, 3.0), (130, 3.0)] + list(zip(c6, gm)) + [(16000, gm[-1] - 2)]
    y = ff(y / max(np.abs(y).max(), 1e-9) * 0.5, "firequalizer=gain_entry='" + ";".join(f"entry({c:.1f},{x:.2f})" for c, x in ent) + "':delay=0.05:accuracy=4")
    cent, g = np.array([e[0] for e in ent]), np.array([e[1] for e in ent])
elif EQMODE == "smooth":                                           # broad moves only: a jagged per-band match colours the voice (nasal / hollow)
    y = ff(y / max(np.abs(y).max(), 1e-9) * 0.5, "equalizer=f=170:t=q:w=0.8:g=3,equalizer=f=1000:t=q:w=1.1:g=-3.5,equalizer=f=1900:t=q:w=1.5:g=-1,"
                                                   "equalizer=f=3800:t=q:w=1.2:g=2,equalizer=f=9000:t=q:w=1.0:g=2")
    g = np.zeros_like(cent)
else:
    y = ff(y / max(np.abs(y).max(), 1e-9) * 0.5, "firequalizer=gain_entry='" + ";".join(f"entry({c:.1f},{x:.2f})" for c, x in zip(cent, g)) + "':delay=0.05:accuracy=4")
y = ff(y, "acompressor=threshold=-24dB:ratio=1.6:attack=10:release=160:makeup=1.5dB:knee=6")
rng = np.random.default_rng(16); L = int(0.8 * SR); tt = np.arange(L) / SR
ir = rng.normal(0, 1, L) * np.exp(-6.9 * tt / 0.5); ir[:int(0.012 * SR)] = 0
ir = signal.lfilter(*signal.butter(2, (3500 if opt("--room", "") == "dark" else 5000) / (SR / 2)), ir); ir /= np.sqrt((ir ** 2).sum())
wet = signal.fftconvolve(y, ir)[:len(y)]; wet = signal.lfilter(*signal.butter(2, 200 / (SR / 2), "high"), wet)
y = y + (0.24 if opt("--room", "") == "dark" else 0.18) * wet * np.sqrt((y ** 2).mean()) / max(np.sqrt((wet ** 2).mean()), 1e-12)
rs = clean[int(0.05 * SR):int(1.05 * SR)]; xf = int(0.2 * SR); tone = np.zeros(len(y)); pos = 0
w = np.ones(len(rs)); w[:xf] = np.linspace(0, 1, xf); w[-xf:] = np.linspace(1, 0, xf)
while pos < len(tone): s = (rs * w)[:len(tone) - pos]; tone[pos:pos + len(s)] += s; pos += len(rs) - xf
y = y + tone * (10 ** (-62 / 20) / max(np.sqrt((tone ** 2).mean()), 1e-12))
y = y[:int((DUR + 0.25) * SR)]; k = int(0.25 * SR); y[-k:] *= np.linspace(1, 0, k)
y = ff(y, f"volume={-16 - lufs(y):.2f}dB,alimiter=limit={10 ** (-2 / 20):.3f}:attack=3:release=60:level=disabled")
stem = A / f"vo_take06_{TAG}.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s24le", str(stem)], input=np.asarray(y, np.float32).tobytes(), check=True)
nat = load(VID); m = min(len(nat), len(y)); vol = -14.0 - lufs(nat[:m] + y[:m]) - 0.3
out = REEL / f"renders/exports/pujo-ki-asolei-sobar_{TAG}_IG.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VID), "-i", str(stem), "-filter_complex",
                f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[n];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                f"[v][n]amix=inputs=2:normalize=0:duration=first,volume={vol:.2f}dB,alimiter=limit=0.84:attack=3:release=60:level=disabled,aresample=48000[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
(REEL / f"analysis/vo_gentle_{TAG}.json").write_text(json.dumps({"shift_st": SHIFT, "range": RANGE, "eq_strength": EQ, "eqmode": EQMODE, "formant": FORMANT,
    "merge2": MERGE2, "slow": SLOW, "t10b": T10B, "light_clean": LIGHT, "phrases": ph,
    "eq_gains_db": dict(zip([round(c) for c in cent], np.round(g, 1).tolist()))}, indent=1))
print(f"✓ {TAG}: PSOLA shift {SHIFT:+.1f} st, range x{RANGE}, EQ {EQ:.0%} -> {stem.name}, {out.name}")
