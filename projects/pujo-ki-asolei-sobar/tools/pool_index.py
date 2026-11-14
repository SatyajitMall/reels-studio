#!/usr/bin/env python3
"""Index every video in the director's Puja/Pujo folders: path, folder, name, duration, size, fps (r and avg),
frame count, codec.  Round 9 (director: "go through all videos"): find people not used yet and slow-mo headroom
(true slow motion needs capture fps >= 2x the 30 fps timeline).
Usage: pool_index.py -> analysis/pool_r9/index.json"""
import json, subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = (Path.home() / "Documents/Video ")
REEL = Path(__file__).resolve().parents[1]
files = sorted(p for d in ROOT.iterdir() if d.is_dir() and d.name.lower().startswith(("puja", "pujo")) and "sobar" not in d.name.lower()
               for p in d.rglob("*") if p.suffix.lower() in (".mov", ".mp4") and not p.name.startswith("._"))
def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=codec_name,width,height,r_frame_rate,avg_frame_rate,nb_frames:stream_side_data=rotation:format=duration,size:format_tags=creation_time,com.apple.quicktime.model",
                        "-of", "json", str(p)], capture_output=True, text=True)
    try: j = json.loads(r.stdout)
    except Exception: return {"path": str(p), "err": r.stderr[:200]}
    s = (j.get("streams") or [{}])[0]; f = j.get("format", {})
    fr = lambda x: (lambda a, b: round(a / b, 3) if b else 0)(*map(float, x.split("/"))) if x and "/" in x else 0
    return {"path": str(p), "folder": p.parent.name.strip(), "name": p.name, "dur": round(float(f.get("duration", 0)), 2), "mb": round(int(f.get("size", 0)) / 1e6, 1),
            "w": s.get("width"), "h": s.get("height"), "codec": s.get("codec_name"), "fps_r": fr(s.get("r_frame_rate")), "fps_avg": fr(s.get("avg_frame_rate")),
            "frames": int(s.get("nb_frames", 0) or 0), "rot": next((sd.get("rotation") for sd in s.get("side_data_list", []) if "rotation" in sd), 0),
            "created": f.get("tags", {}).get("creation_time"), "model": f.get("tags", {}).get("com.apple.quicktime.model")}
with ThreadPoolExecutor(8) as ex: rows = list(ex.map(probe, files))
(REEL / "analysis/pool_r9/index.json").write_text(json.dumps(rows, indent=1))
from collections import Counter
print("files", len(rows))
print("by folder", Counter(r.get("folder") for r in rows))
print("fps", Counter(round(r.get("fps_r", 0)) for r in rows))
print("codec", Counter(r.get("codec") for r in rows)); print("res", Counter((r.get("w"), r.get("h")) for r in rows))
print("name prefixes", Counter(r["name"][:4] for r in rows).most_common(8))
hi = [r for r in rows if r.get("fps_avg", 0) >= 48]
print("high-fps clips:", len(hi)); [print("  ", r["folder"], r["name"], r["fps_r"], r["fps_avg"], r["dur"], r["w"], r["h"]) for r in hi[:60]]
