#!/usr/bin/env python3
"""Local voiceover recorder for the director (2026-10-27): plays the record-along guide and records the Mac / iPhone mic in the
browser, saving every take straight into the reel as 48 kHz WAV + a JSON with the sync offset.
  GET  /            index.html (recorder page)
  GET  /guide.mp4   renders/guide/record_along_guide.mp4
  GET  /takes/<f>   saved takes (for playback)
  POST /save        body = WAV bytes; headers X-Offset (s of audio before the guide started), X-Device, X-Guide-Voice
Takes land in audio/vo_director/take_NN.wav (+ .json). Reel time 0 = offset + 6.0 s (the guide's pre-roll).
Usage: server.py [port]   (default 8765), then open http://localhost:8765
"""
import json, sys, time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
REEL = Path(__file__).resolve().parents[2]; HERE = Path(__file__).resolve().parent
GUIDE = REEL / "renders/guide/record_along_guide.mp4"; TAKES = REEL / "audio/vo_director"; TAKES.mkdir(parents=True, exist_ok=True)
PRE = 6.0

class H(SimpleHTTPRequestHandler):
    def _file(self, p, ctype):
        if not p.is_file(): self.send_error(404); return
        data = p.read_bytes(); rng = self.headers.get("Range")
        if rng and rng.startswith("bytes="):                      # video seeking needs range requests
            a, _, b = rng[6:].partition("-"); a = int(a); b = int(b) if b else len(data) - 1
            self.send_response(206); self.send_header("Content-Range", f"bytes {a}-{b}/{len(data)}"); data = data[a:b + 1]
        else: self.send_response(200)
        self.send_header("Content-Type", ctype); self.send_header("Accept-Ranges", "bytes"); self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"): return self._file(HERE / "index.html", "text/html; charset=utf-8")
        if path == "/guide.mp4": return self._file(GUIDE, "video/mp4")
        if path == "/takes":
            body = json.dumps(sorted(p.name for p in TAKES.glob("take_*.wav"))).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); return self.wfile.write(body)
        if path.startswith("/takes/"): return self._file(TAKES / Path(path).name, "audio/wav")
        self.send_error(404)

    def do_POST(self):
        if self.path.split("?")[0] != "/save": return self.send_error(404)
        data = self.rfile.read(int(self.headers["Content-Length"]))
        n = 1 + max([int(p.stem.split("_")[1]) for p in TAKES.glob("take_*.wav")] or [0])
        wav = TAKES / f"take_{n:02d}.wav"; wav.write_bytes(data)
        off = float(self.headers.get("X-Offset", "0"))
        meta = {"file": wav.name, "saved": time.strftime("%Y-%m-%d %H:%M:%S"), "offset_s": off, "reel_t0_in_take_s": off + PRE,
                "device": self.headers.get("X-Device", ""), "guide_voice": self.headers.get("X-Guide-Voice", ""), "bytes": len(data)}
        wav.with_suffix(".json").write_text(json.dumps(meta, indent=1))
        body = json.dumps(meta).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)
        print(f"saved {wav.name}: {len(data) / 1e6:.1f} MB, offset {off:.3f} s", flush=True)

    def log_message(self, *a): pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"VO recorder on http://localhost:{port}  (takes -> {TAKES})", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
