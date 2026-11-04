#!/usr/bin/env python3
"""Word-level transcripts with local Whisper (faster-whisper): the studio's default transcriber since v0.9.

ElevenLabs Scribe returned 401 on three reels in a row (puja-night-2, Pujo, goddess), and each reel improvised a local
Whisper. This one is free, offline after the first model download, and writes the same JSON shape as the vendor's Scribe
helper, so `pack_transcripts.py` and `timeline_view.py` read it unchanged:

  <edit-dir>/transcripts/<stem>.json = {"language_code": "en", "text": "...", "source": "faster-whisper small",
      "words": [{"type": "word", "text": "Pujo", "start": 1.02, "end": 1.31, "speaker_id": null, "probability": 0.93},
                {"type": "spacing", "text": " ", "start": 1.31, "end": 1.40}, ...]}

Audio is decoded with ffmpeg (16 kHz mono): the PyAV that faster-whisper bundles rejects its own open() arguments.

Timing: Whisper's word starts can run early (about 0.3 s on the goddess VO). Use them to find the clause, then place the
cut on the waveform (`timeline_view.py`), 0 to 2 frames before the speech starts (CLAUDE.md §4b).

Models download once into ~/.cache/huggingface (small ≈ 0.5 GB, large-v3-turbo ≈ 1.6 GB). `small` suits English;
for Hindi or Bangla use --model large-v3-turbo and --language hi / bn.

Usage (from the studio root; scripts/transcribe_reel.sh wraps this for a reel's A-roll):
  ./.venv/bin/python scripts/transcribe_local.py projects/<reel>/audio/vo.wav --edit-dir projects/<reel> [--language en]
      [--model small] [--vad] [--force]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

SR = 16000


def pcm(path: Path) -> np.ndarray:
    """16 kHz mono float samples; empty when the file has no audio track."""
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True)
    return np.frombuffer(p.stdout, np.float32) if p.returncode == 0 else np.zeros(0, np.float32)


def cached(out: Path, model: str, language: str | None) -> str | None:
    """Why an existing transcript can be kept, or None to transcribe again (another model or language asked for)."""
    if not out.exists():
        return None
    try:
        data = json.loads(out.read_text())
    except ValueError:
        return None
    source = data.get("source")
    if source is None:
        return "cached (ElevenLabs Scribe; --force to replace it)"
    if source == f"faster-whisper {model}" and language in (None, data.get("language_code")):
        return "cached"
    return None


def scribe_shape(segments, language: str, model: str) -> dict:
    """faster-whisper segments → the Scribe word list (words plus the spacing between them)."""
    words: list[dict] = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if not text:
                continue
            start, end = round(w.start, 3), round(max(w.end, w.start), 3)
            if words and start > words[-1]["end"]:
                words.append({"type": "spacing", "text": " ", "start": words[-1]["end"], "end": start})
            words.append({"type": "word", "text": text, "start": start, "end": end, "speaker_id": None,
                          "probability": round(w.probability, 3)})
    text = " ".join(w["text"] for w in words if w["type"] == "word")
    return {"language_code": language, "text": text, "source": f"faster-whisper {model}", "words": words}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("media", type=Path, nargs="+", help="video or audio files")
    ap.add_argument("--edit-dir", type=Path, required=True, help="the reel folder; writes <edit-dir>/transcripts/<stem>.json")
    ap.add_argument("--model", default="small", help="faster-whisper model (small, medium, large-v3-turbo …)")
    ap.add_argument("--language", default=None, help="ISO code (en, hi, bn); omit to auto-detect")
    ap.add_argument("--vad", action="store_true", help="skip long non-speech stretches (fewer invented words in music beds)")
    ap.add_argument("--force", action="store_true", help="re-transcribe even if the JSON exists")
    a = ap.parse_args()

    out_dir = a.edit_dir / "transcripts"
    out_dir.mkdir(parents=True, exist_ok=True)
    todo = []
    for m in a.media:
        if not m.exists():
            sys.exit(f"not found: {m}")
        out = out_dir / f"{m.stem}.json"
        why = None if a.force else cached(out, a.model, a.language)
        if why:
            print(f"▸ {m.name}: {why} ({out})")
            continue
        todo.append((m, out))
    if not todo:
        return

    from faster_whisper import WhisperModel   # imported late: loading it takes a few seconds
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    for m, out in todo:
        t0 = time.time()
        audio = pcm(m)
        if audio.size == 0:
            print(f"✗ {m.name}: no audio track")
            continue
        segments, info = model.transcribe(audio, language=a.language, word_timestamps=True, vad_filter=a.vad,
                                          beam_size=5, condition_on_previous_text=False)
        data = scribe_shape(list(segments), info.language, a.model)
        out.write_text(json.dumps(data, indent=1, ensure_ascii=False))
        n = sum(1 for w in data["words"] if w["type"] == "word")
        print(f"✓ {m.name}: {n} words, {info.language}, {audio.size / SR:.1f} s audio in {time.time() - t0:.0f} s → {out}")


if __name__ == "__main__":
    main()
