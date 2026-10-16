#!/usr/bin/env python3
"""Gemini Word-Level Transcription Wrapper (ElevenLabs Scribe v2 + Free Local Whisper Fallback).

Solves two issues in `.vendor/video-use/helpers/transcribe.py`:
1. Uses ElevenLabs `scribe_v2` (falling back to `scribe_v1` if needed) when `ELEVENLABS_API_KEY`
   is configured in `.env`.
2. When `ELEVENLABS_API_KEY` is blank in `.env`, instead of crashing and losing word-level
   cutting, automatically falls back to local Whisper (`mlx_whisper`, `faster_whisper`, or
   `whisper` CLI/Python) and converts the output into the exact Scribe JSON schema
   (`{"text": ..., "words": [{"text": ..., "start": ..., "end": ..., "type": "word", "speaker_id": "speaker_0"}]}`)
   so `.vendor/video-use/helpers/pack_transcripts.py` produces `takes_packed.md` seamlessly.

Usage:
    ./.venv/bin/python scripts/gemini_transcribe_fallback.py <reel-name> [--language en]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
SCRIBE_URL = "https://api.elevenlabs.io/v1/speech-to-text"
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mxf", ".mkv"}


def get_elevenlabs_key() -> str:
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == "ELEVENLABS_API_KEY":
                    val = v.strip().strip('"').strip("'")
                    if val:
                        return val
    return os.environ.get("ELEVENLABS_API_KEY", "").strip()


def extract_wav(video: Path, wav_out: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
            str(wav_out),
        ],
        check=True,
    )


def transcribe_elevenlabs(wav_path: Path, api_key: str, language: str | None) -> dict:
    for model_id in ("scribe_v2", "scribe_v1"):
        data = {
            "model_id": model_id,
            "diarize": "true",
            "tag_audio_events": "true",
            "timestamps_granularity": "word",
        }
        if language:
            data["language_code"] = language
        with open(wav_path, "rb") as f:
            resp = requests.post(
                SCRIBE_URL,
                headers={"xi-api-key": api_key},
                files={"file": (wav_path.name, f, "audio/wav")},
                data=data,
                timeout=1800,
            )
        if resp.status_code == 200:
            return resp.json()
    raise RuntimeError(f"ElevenLabs Scribe failed ({resp.status_code}): {resp.text[:300]}")


def whisper_segments_to_scribe_json(segments: list[dict]) -> dict:
    words_out: list[dict] = []
    full_text_parts: list[str] = []
    prev_end: float | None = None

    for seg in segments:
        seg_text = (seg.get("text") or "").strip()
        if seg_text:
            full_text_parts.append(seg_text)
        seg_words = seg.get("words") or []
        if not seg_words and seg_text:
            # Interpolate word timestamps if backend returned segment-only timestamps
            tokens = seg_text.split()
            s_start = float(seg.get("start", 0.0))
            s_end = float(seg.get("end", s_start + 0.5))
            dur = max(s_end - s_start, 0.1) / max(len(tokens), 1)
            seg_words = [
                {"word": tok, "start": s_start + i * dur, "end": s_start + (i + 1) * dur}
                for i, tok in enumerate(tokens)
            ]
        for w in seg_words:
            w_text = (w.get("word") or w.get("text") or "").strip()
            if not w_text:
                continue
            w_start = round(float(w.get("start", 0.0)), 3)
            w_end = round(float(w.get("end", w_start + 0.1)), 3)
            if prev_end is not None and w_start > prev_end:
                words_out.append({
                    "text": " ",
                    "start": prev_end,
                    "end": w_start,
                    "type": "spacing",
                    "speaker_id": "speaker_0",
                })
            words_out.append({
                "text": w_text,
                "start": w_start,
                "end": w_end,
                "type": "word",
                "speaker_id": "speaker_0",
            })
            prev_end = w_end

    return {"text": " ".join(full_text_parts), "words": words_out}


def transcribe_local_whisper(wav_path: Path, language: str | None) -> dict:
    """Try mlx_whisper, then faster_whisper, then openai-whisper."""
    try:
        import mlx_whisper  # type: ignore
        res = mlx_whisper.transcribe(
            str(wav_path),
            path_or_hf_repo="mlx-community/whisper-base-mlx",
            word_timestamps=True,
            language=language,
        )
        return whisper_segments_to_scribe_json(res.get("segments", []))
    except ImportError:
        pass

    try:
        from faster_whisper import WhisperModel  # type: ignore
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments_gen, _ = model.transcribe(str(wav_path), word_timestamps=True, language=language)
        segs = [
            {
                "start": s.start,
                "end": s.end,
                "text": s.text,
                "words": [{"word": w.word, "start": w.start, "end": w.end} for w in (s.words or [])],
            }
            for s in segments_gen
        ]
        return whisper_segments_to_scribe_json(segs)
    except ImportError:
        pass

    sys.exit(
        "Neither ELEVENLABS_API_KEY (in .env) nor a local Whisper package (mlx-whisper / faster-whisper) "
        "is installed. Run: ./.venv/bin/pip install faster-whisper   (or add ELEVENLABS_API_KEY to .env)."
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("reel_name", help="Reel folder name under projects/")
    ap.add_argument("--language", default=None, help="Optional ISO language code (e.g. 'en')")
    args = ap.parse_args()

    reel_dir = ROOT / "projects" / args.reel_name
    aroll_dir = reel_dir / "raw" / "a-roll"
    transcripts_dir = reel_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)

    clips = sorted(f for f in aroll_dir.iterdir() if f.suffix.lower() in VIDEO_EXT) if aroll_dir.is_dir() else []
    if not clips:
        sys.exit(f"No video clips found in {aroll_dir}")

    api_key = get_elevenlabs_key()
    mode = "ElevenLabs Scribe v2" if api_key else "Local Whisper Fallback"
    print(f"▸ Transcription mode: {mode}")

    for clip in clips:
        out_json = transcripts_dir / f"{clip.stem}.json"
        if out_json.exists():
            print(f"  cached: {out_json.name}")
            continue
        print(f"  transcribing {clip.name}...")
        with tempfile.TemporaryDirectory() as tmp:
            wav_path = Path(tmp) / f"{clip.stem}.wav"
            extract_wav(clip, wav_path)
            payload = (
                transcribe_elevenlabs(wav_path, api_key, args.language)
                if api_key
                else transcribe_local_whisper(wav_path, args.language)
            )
        out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"  ✓ saved {out_json.name}")

    pack_script = ROOT / ".vendor" / "video-use" / "helpers" / "pack_transcripts.py"
    packed_out = transcripts_dir / "takes_packed.md"
    subprocess.run(
        [sys.executable, str(pack_script), "--edit-dir", str(reel_dir), "-o", str(packed_out)],
        check=True,
    )


if __name__ == "__main__":
    main()
