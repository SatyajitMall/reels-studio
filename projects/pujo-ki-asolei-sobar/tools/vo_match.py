#!/usr/bin/env python3
"""Match the director's voiceover (take 6) to the reference voice in pitch, intonation, timing, timbre and effect
(director, 2026-10-27: "reverse engineer the audio to match the source audio in all aspects").
Measured gap (tools: librosa pyin / centroid; analysis in project.md): reference F0 median 140 Hz, range 9 st, voiced 80 %, darker
(centroid ~1060 Hz), mono, slight tail; take 6: 182 Hz, 5 st, 62 %, brighter (~1340 Hz), dry. Pace is the same.
Method (WORLD vocoder, renders/_pylib/pyworld):
  1 analyse   cleaned take (high-pass, FFT denoise, de-ess) -> F0 / spectral envelope / aperiodicity, 5 ms frames
  2 timing    per phrase (analysis/vo_place.json: which take phrase plays where), DTW on MFCCs against the same words in the
              reference -> a smoothed, monotone time map; frames are re-sampled along it (TIMING = strength, 0..1)
  3 pitch     the reference F0 contour on the aligned frames (octave errors rejected), blended in log-F0 with the take's F0
              shifted to the reference median (INTON = strength), the take's micro-jitter kept so it stays human
  4 timbre    spectral envelope warped on the frequency axis by K (searched: best fit of the take's envelope to the reference's)
  5 effect    auto matching EQ (1/3-octave LTAS ratio vs the reference's loud speech frames, clamped), compression to the
              reference's level swing, small-room tail to the reference's decay, room tone, mono; static loudness; mux on v13 picture
Usage: vo_match.py [--timing 1.0] [--inton 0.85] [--tag v15]
  -> audio/vo_director/vo_take06_matched_<tag>.wav, renders/exports/pujo-ki-asolei-sobar_<tag>_IG.mp4, analysis/vo_match_<tag>.json
"""
import json, subprocess, sys, warnings
from pathlib import Path
import numpy as np
from scipy import signal, ndimage
warnings.filterwarnings("ignore")
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "renders/_pylib"))
import pyworld as pw  # noqa: E402
import librosa  # noqa: E402
def opt(k, d): return type(d)(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
TIMING, INTON, TAG = opt("--timing", 1.0), opt("--inton", 0.85), opt("--tag", "v15")
A = REEL / "audio/vo_director"; PLACE = json.loads((REEL / "analysis/vo_place.json").read_text())
T0 = PLACE["reel_t0_in_take_s"]; VID = REEL / "renders/exports/pujo-ki-asolei-sobar_v13_IG.mp4"
SR, FP, DUR = 48000, 5.0, 35.8333; HOP = int(SR * FP / 1000)

def load(p, sr=SR):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).astype(np.float64)
def ff(x, af):
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
                       input=np.asarray(x, np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)
def lufs(x, sr=SR):
    out = subprocess.run(["ffmpeg", "-v", "info", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"],
                         input=np.asarray(x, np.float32).tobytes(), capture_output=True).stderr.decode()
    return float(out.rsplit("I:", 1)[1].split("LUFS")[0])

# 1 analyse
take = ff(load(A / "take_06.wav"), "highpass=f=75:poles=2,afftdn=nr=12:nf=-50:tn=1,deesser=i=0.35:m=0.5:f=0.5")
ref = load(REEL / "audio/ref_audio_vo.wav")
def world(x, lo, hi):
    f0, t = pw.harvest(x, SR, f0_floor=lo, f0_ceil=hi, frame_period=FP); f0 = pw.stonemask(x, f0, t, SR)
    return f0, pw.cheaptrick(x, f0, t, SR), pw.d4c(x, f0, t, SR)
f0_t, sp_t, ap_t = world(take, 90, 320)
f0_r, t_r = pw.harvest(ref, SR, f0_floor=70, f0_ceil=260, frame_period=FP); f0_r = pw.stonemask(ref, f0_r, t_r, SR)
vt, vr = f0_t[f0_t > 0], f0_r[f0_r > 0]
SHIFT = float(np.median(np.log2(vr)) - np.median(np.log2(vt)))          # octaves (negative = down)
# reference F0 cleanup: reject octave errors vs a 0.6 s running median, then fill short gaps
lr = np.where(f0_r > 0, np.log2(np.maximum(f0_r, 1)), np.nan)
med = ndimage.generic_filter(np.nan_to_num(lr, nan=np.nanmedian(lr)), np.median, size=121)
lr[np.abs(lr - med) > 0.45] = np.nan

# 4 timbre: frequency-warp factor K that best fits the take's mean envelope to the reference's (250-4000 Hz)
fax = np.linspace(0, SR / 2, sp_t.shape[1])
def mean_env(sp, f0):
    e = np.log(sp[f0 > 0] + 1e-12); en = e.sum(1); return e[en > np.percentile(en, 50)].mean(0)
er = mean_env(pw.cheaptrick(ref, f0_r, t_r, SR), f0_r); et = mean_env(sp_t, f0_t); band = (fax > 250) & (fax < 4000)
def warp(env, k): return np.interp(fax / k, fax, env)
ks = np.linspace(0.80, 1.06, 27); fit = [np.corrcoef(warp(et, k)[band], er[band])[0, 1] for k in ks]; K = float(ks[int(np.argmax(fit))])

# 2+3 timing and pitch, phrase by phrase, onto a reel-time frame grid
NF = int((DUR + 0.6) * 1000 / FP); f0_o = np.zeros(NF); sp_o = np.full((NF, sp_t.shape[1]), 1e-12); ap_o = np.ones((NF, sp_t.shape[1]))
mf = lambda x: librosa.feature.mfcc(y=x.astype(np.float32), sr=SR, n_mfcc=20, n_fft=1024, hop_length=HOP)[1:]
dips = json.loads((REEL / "analysis/vo_timing.json").read_text())["speech_dips"]
phr = PLACE["phrases"]; log = []
for i, p in enumerate(phr):
    a, b = p["src_reel_s"]; tgt = p["target_s"]; tempo = p["tempo"]
    nxt = phr[i + 1]["target_s"] if i + 1 < len(phr) else DUR
    # the same words in the reference: from the phrase's target to the reference's next pause (bounded by the next phrase)
    ref_end = min([d0 for d0, d1 in dips if d0 > tgt + 0.25] + [nxt - 0.03, DUR])
    ref_end = max(ref_end, tgt + 0.3)
    ia, ib = int((a + T0) * 1000 / FP), int((b + T0) * 1000 / FP); ja, jb = int(tgt * 1000 / FP), int(ref_end * 1000 / FP)
    lin = np.linspace(ia, ib - 1, jb - ja)
    if TIMING > 0:
        X = mf(take[ia * HOP:ib * HOP]); Y = mf(ref[ja * HOP:jb * HOP])
        n = min(X.shape[1], ib - ia); m = min(Y.shape[1], jb - ja)
        Xn = (X[:, :n] - X[:, :n].mean(1, keepdims=True)) / (X[:, :n].std(1, keepdims=True) + 1e-6)
        Yn = (Y[:, :m] - Y[:, :m].mean(1, keepdims=True)) / (Y[:, :m].std(1, keepdims=True) + 1e-6)
        _, wp = librosa.sequence.dtw(X=Xn, Y=Yn, metric="cosine", step_sizes_sigma=np.array([[1, 1], [1, 2], [2, 1]]), weights_add=np.array([0, 0, 0]))
        wp = wp[::-1]; jmap = np.full(jb - ja, np.nan)
        for ii, jj in wp:
            if jj < len(jmap): jmap[jj] = ii if np.isnan(jmap[jj]) else (jmap[jj] + ii) / 2
        idx = np.arange(len(jmap)); ok = ~np.isnan(jmap); jmap = np.interp(idx, idx[ok], jmap[ok]) + ia
        jmap = ndimage.uniform_filter1d(jmap, 15)                       # 75 ms smoothing
        sl = np.clip(np.diff(jmap, prepend=jmap[0]), 0.55, 1.8); jmap = ia + np.cumsum(sl) - sl[0]   # monotone, bounded speed
        jmap = jmap * (ib - 1 - ia) / max(jmap[-1] - ia, 1e-6) + ia * (1 - (ib - 1 - ia) / max(jmap[-1] - ia, 1e-6))
        src_idx = (1 - TIMING) * lin + TIMING * jmap
    else:
        src_idx = np.linspace(ia, ia + (b - a) / tempo * 1000 / FP * tempo - 1, int((b - a) / tempo * 1000 / FP)); jb = ja + len(src_idx)
    src_idx = np.clip(src_idx, 0, len(f0_t) - 1); i0 = np.floor(src_idx).astype(int); fr = (src_idx - i0)[:, None]; i1 = np.minimum(i0 + 1, len(f0_t) - 1)
    sp_seg = np.exp((1 - fr) * np.log(sp_t[i0] + 1e-12) + fr * np.log(sp_t[i1] + 1e-12)); ap_seg = (1 - fr) * ap_t[i0] + fr * ap_t[i1]
    f0_seg = np.where((f0_t[i0] > 0) & (f0_t[i1] > 0), np.exp((1 - fr[:, 0]) * np.log(np.maximum(f0_t[i0], 1)) + fr[:, 0] * np.log(np.maximum(f0_t[i1], 1))), 0)
    lt = np.where(f0_seg > 0, np.log2(np.maximum(f0_seg, 1)), np.nan)
    jit = lt - ndimage.uniform_filter1d(np.nan_to_num(lt, nan=np.nanmean(lt) if np.isfinite(np.nanmean(lt)) else 7), 9)
    base = lt + SHIFT
    rr = lr[ja:ja + len(lt)] if ja + len(lt) <= len(lr) else np.pad(lr[ja:], (0, ja + len(lt) - len(lr)), constant_values=np.nan)
    rs = ndimage.uniform_filter1d(np.nan_to_num(rr, nan=0), 7) / np.maximum(ndimage.uniform_filter1d((~np.isnan(rr)).astype(float), 7), 1e-6)
    rs[ndimage.uniform_filter1d((~np.isnan(rr)).astype(float), 7) < 0.5] = np.nan
    tgt_l = np.where(np.isnan(rs), base, (1 - INTON) * base + INTON * (rs + np.nan_to_num(jit, nan=0)))
    tgt_l = np.clip(tgt_l, base - 0.4, base + 0.4)                     # never more than ~5 st away from the shifted voice
    f0_new = np.where(f0_seg > 0, 2 ** tgt_l, 0)
    n = min(len(f0_new), NF - ja); f0_o[ja:ja + n] = f0_new[:n]; sp_o[ja:ja + n] = sp_seg[:n]; ap_o[ja:ja + n] = ap_seg[:n]
    log.append({"phrase": p["phrase"], "take_s": [round(a, 3), round(b, 3)], "ref_span_s": [round(tgt, 3), round(tgt + n * FP / 1000, 3)]})
sp_o = np.array([warp(np.log(s), K) for s in sp_o]); sp_o = np.exp(sp_o)
y = pw.synthesize(np.ascontiguousarray(f0_o), np.ascontiguousarray(sp_o), np.ascontiguousarray(ap_o), SR, FP)
gate = np.repeat((f0_o > 0) | (sp_o.sum(1) > 1e-6 * sp_o.shape[1] * 10), HOP)[:len(y)]
y = y[:len(gate)] * ndimage.uniform_filter1d(gate.astype(float), int(0.01 * SR))

# 5 effect: auto matching EQ toward the reference's loud speech frames (1/3 octave, +-6 dB, 80 %)
def ltas(x):
    f, _, S = signal.stft(x, SR, nperseg=4096, noverlap=3072); P = np.abs(S) ** 2; e = P.sum(0); k = e > np.percentile(e, 70)
    return f, P[:, k].mean(1)
f, Pr = ltas(ref); _, Py = ltas(y)
cent = 31.5 * 2 ** (np.arange(0, 30) / 3); cent = cent[cent < 16000]; gains = []
for c in cent:
    m = (f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6)); gains.append(10 * np.log10(Pr[m].mean() / max(Py[m].mean(), 1e-20)))
gains = np.nan_to_num(np.array(gains), nan=0.0); gains -= np.median(gains[(cent > 400) & (cent < 3000)]); gains = np.clip(gains * 0.8, -6, 6)
gains[cent < 300] = np.minimum(gains[cent < 300], 4.0)        # the reference's lows also carry its music bed: don't chase it fully
gains[cent < 70] = np.minimum(gains[cent < 70], 0)
entries = ";".join(f"entry({c:.1f},{g:.2f})" for c, g in zip(cent, gains))
y = ff(y / max(np.abs(y).max(), 1e-9) * 0.5, f"firequalizer=gain_entry='{entries}':delay=0.05:accuracy=4")
y = ff(y, "acompressor=threshold=-24dB:ratio=1.8:attack=10:release=160:makeup=2dB:knee=6")
# small-room tail (reference decays ~5 dB slower over the first 50 ms than the dry take)
rng = np.random.default_rng(15); L = int(0.8 * SR); tt = np.arange(L) / SR
ir = rng.normal(0, 1, L) * np.exp(-6.9 * tt / 0.5); ir[:int(0.012 * SR)] = 0
ir = signal.lfilter(*signal.butter(2, 5000 / (SR / 2)), ir); ir /= np.sqrt((ir ** 2).sum())
wet = signal.fftconvolve(y, ir)[:len(y)]; wet = signal.lfilter(*signal.butter(2, 200 / (SR / 2), "high"), wet)
y = y + 0.22 * wet * np.sqrt((y ** 2).mean()) / max(np.sqrt((wet ** 2).mean()), 1e-12)
# room tone from the take's quiet pre-roll, -62 dB
rt_src = take[int(0.05 * SR):int(1.05 * SR)]; xf = int(0.2 * SR); tone = np.zeros(len(y)); pos = 0
w = np.ones(len(rt_src)); w[:xf] = np.linspace(0, 1, xf); w[-xf:] = np.linspace(1, 0, xf)
while pos < len(tone): s = (rt_src * w)[:len(tone) - pos]; tone[pos:pos + len(s)] += s; pos += len(rt_src) - xf
y = y + tone * (10 ** (-62 / 20) / max(np.sqrt((tone ** 2).mean()), 1e-12))
y = y[:int((DUR + 0.25) * SR)]; k = int(0.25 * SR); y[-k:] *= np.linspace(1, 0, k)
g = -16 - lufs(y); y = ff(y, f"volume={g:.2f}dB,alimiter=limit={10 ** (-2 / 20):.3f}:attack=3:release=60:level=disabled")
stem = A / f"vo_take06_matched_{TAG}.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s24le", str(stem)], input=np.asarray(y, np.float32).tobytes(), check=True)
nat = load(VID); m = min(len(nat), len(y)); vol = -14.0 - lufs(nat[:m] + y[:m]) - 0.3
out = REEL / f"renders/exports/pujo-ki-asolei-sobar_{TAG}_IG.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VID), "-i", str(stem), "-filter_complex",
                f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[n];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                f"[v][n]amix=inputs=2:normalize=0:duration=first,volume={vol:.2f}dB,alimiter=limit=0.84:attack=3:release=60:level=disabled,aresample=48000[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", str(out)], check=True)
(REEL / f"analysis/vo_match_{TAG}.json").write_text(json.dumps({"timing": TIMING, "inton": INTON, "pitch_shift_st": round(SHIFT * 12, 2),
    "formant_warp_K": K, "formant_shift_st": round(12 * np.log2(K), 2), "eq_gains_db": dict(zip([round(c) for c in cent], np.round(gains, 1).tolist())),
    "phrases": log}, indent=1))
print(f"pitch shift {SHIFT * 12:+.2f} st, formant warp K={K:.3f} ({12 * np.log2(K):+.2f} st), timing {TIMING}, intonation {INTON}")
print("✓", stem.name, "+", out.name)
