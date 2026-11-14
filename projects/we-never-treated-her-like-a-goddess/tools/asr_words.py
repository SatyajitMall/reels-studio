"""Word-level transcript of a VO file with local faster-whisper (ElevenLabs key is rejected; CR external-vo-audio).
Usage: <venv-with-faster-whisper>/bin/python tools/asr_words.py <audio> <out.json> [model] [lang]"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

audio, out = sys.argv[1], sys.argv[2]
model_name = sys.argv[3] if len(sys.argv) > 3 else "small.en"
lang = sys.argv[4] if len(sys.argv) > 4 else "en"
model = WhisperModel(model_name, device="cpu", compute_type="int8")
# decode with ffmpeg: the PyAV in a fresh venv rejects faster-whisper's open() kwargs
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
segs, info = model.transcribe(np.frombuffer(pcm, np.float32), language=lang, word_timestamps=True, vad_filter=False, beam_size=5)
res = {"model": model_name, "language": info.language, "segments": []}
for s in segs:
    res["segments"].append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip(),
                            "words": [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for w in s.words]})
json.dump(res, open(out, "w"), indent=1)
for s in res["segments"]:
    print(f'{s["start"]:6.2f}–{s["end"]:6.2f}  {s["text"]}')
    print("        " + "  ".join(f'{w["w"]}@{w["s"]:.2f}' for w in s["words"]))
