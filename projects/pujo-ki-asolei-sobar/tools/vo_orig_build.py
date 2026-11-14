#!/usr/bin/env python3
"""v19: the reference creator's own voice (permission given to the director, 2026-10-27) without the song under it.
The reference audio (audio/ref_audio_vo.wav = @abhii.jpgg's VO over "Jaago", Lifafa) is split with demucs (htdemucs,
two stems); only the vocal stem is baked into the v13 picture (original subtitles, which are his words), over the v13 natural
sound. "Jaago" is then added from Instagram's library at upload, so the music stays licensed.
Usage: vo_orig_build.py <vocals.wav>  -> audio/vo_abhii_vocals_clean.wav, renders/exports/pujo-ki-asolei-sobar_v19_IG.mp4
"""
import subprocess, sys
from pathlib import Path
import numpy as np
REEL = Path(__file__).resolve().parents[1]; SR, DUR = 48000, 35.8333
VID = REEL / "renders/exports/pujo-ki-asolei-sobar_v13_IG.mp4"; OUT = REEL / "renders/exports/pujo-ki-asolei-sobar_v19_IG.mp4"
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).astype(np.float64)
def ff(x, af):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
                                        input=np.asarray(x, np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32).astype(np.float64)
def lufs(x):
    out = subprocess.run(["ffmpeg", "-v", "info", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"],
                         input=np.asarray(x, np.float32).tobytes(), capture_output=True).stderr.decode()
    return float(out.rsplit("I:", 1)[1].split("LUFS")[0])

v = load(sys.argv[1])
# light clean-up of separation residue: high-pass, gentle expander on the gaps (bed leakage), no tone change to his voice
v = ff(v, "highpass=f=70:poles=2,agate=threshold=0.008:ratio=3:attack=5:release=180:range=0.25")
v = v[:int((DUR + 0.1) * SR)]; k = int(0.4 * SR); v[-k:] *= np.linspace(1, 0, k)   # the v13 bed fade (A3_FADE 0.4)
v = ff(v, f"volume={-16 - lufs(v):.2f}dB,alimiter=limit={10 ** (-2 / 20):.3f}:attack=3:release=60:level=disabled")
stem = REEL / "audio/vo_abhii_vocals_clean.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s24le", str(stem)], input=np.asarray(v, np.float32).tobytes(), check=True)
nat = load(VID); m = min(len(nat), len(v)); vol = -14.0 - lufs(nat[:m] + v[:m]) - 0.3
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VID), "-i", str(stem), "-filter_complex",
                f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo[n];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                f"[v][n]amix=inputs=2:normalize=0:duration=first,volume={vol:.2f}dB,alimiter=limit=0.84:attack=3:release=60:level=disabled,aresample=48000,apad[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-t", "35.8", str(OUT)], check=True)
print("✓", stem.name, "+", OUT.name)
