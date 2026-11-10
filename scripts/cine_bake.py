#!/usr/bin/env python3
"""Bake Apple Cinematic Video depth for a reel (v0.9.2), so previews, sheets, checks and Premiere see the blur.

Clips shot in Cinematic mode (Blackmagic Cam or the iPhone Camera app; ingest_report.py flags them "cinematic") store a
sharp picture plus a depth track. Only Apple apps draw the blur, so the bake goes first: everything downstream reads
the baked ProRes, never the camera file (CLAUDE.md §5, skill Phase 1).

  --check CLIP…        list which clips are Cinematic, with the recorded aperture
  --edl EDL            bake every Cinematic clip an EDL uses, over the span its shots use plus handles, then write
                         raw/baked/<camera stem>_f<F>_<start>-<end>.mov    (ProRes 422 HQ, rotation tag kept, with sound)
                         analysis/bake_map_<edl stem>.json                 camera → bake, start, dur, f-number
                         analysis/<edl stem>_baked.json                    the same EDL, clips → bakes, src_in shifted
                       Shots on non-Cinematic clips (stock, renders, stills) are left as they are. An existing bake of
                       the same span and f-number is reused (--force re-bakes).

The f-number defaults to the one recorded per frame (the shot as the director framed it). --fnumber overrides it for
every clip, --fnumber-for C062=2.8 for one clip (camera file stem or its clip number; f/2.8 for hands and tools moving
through the focal plane, which shimmer at f/2 once slow motion interpolates them: Diwali). Focus pulls (cine_bake
--rack) are never applied here: only when the director asks for one (effects-playbook §B).

Usage:
  ./.venv/bin/python scripts/cine_bake.py --check projects/<reel>/raw/Media
  ./.venv/bin/python scripts/cine_bake.py --edl projects/<reel>/analysis/edl_v1.json [--fnumber-for C062=2.8] [--handle 0.48]
Single clip: scripts/bin/cine_bake <in.mov> <out.mov> [--start S --dur D --fnumber F --audio]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from media_info import fps_of  # noqa: E402

STUDIO = Path(__file__).resolve().parent.parent
SRC = STUDIO / "scripts" / "cine_bake.swift"
BIN = STUDIO / "scripts" / "bin" / "cine_bake"
VIDEO = (".mov", ".mp4", ".m4v")
MERGE_GAP = 1.0     # seconds: two used spans of one clip closer than this share a bake


def ensure_binary() -> Path:
    """Build scripts/bin/cine_bake when it is missing or older than its source."""
    if BIN.exists() and BIN.stat().st_mtime >= SRC.stat().st_mtime:
        return BIN
    BIN.parent.mkdir(parents=True, exist_ok=True)
    print(f"building {BIN.relative_to(STUDIO)} …")
    r = subprocess.run(["swiftc", "-O", "-o", str(BIN), str(SRC)], capture_output=True, text=True)
    if r.returncode:
        sys.exit("swiftc failed (needs the Xcode Command Line Tools and macOS 14+):\n" + r.stderr[-2000:])
    return BIN


def cinematic_info(path: Path) -> dict | None:
    """{'aperture': 'f/2', 'dur': s} for an Apple Cinematic Video file, else None."""
    out = subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
                         capture_output=True, text=True).stdout
    try:
        d = json.loads(out or "{}")
    except ValueError:
        return None
    tags = d.get("format", {}).get("tags", {})
    has_dish = any(s.get("codec_tag_string") == "dish" for s in d.get("streams", []))
    if tags.get("com.apple.quicktime.cinematic-video-intent") != "1" and not has_dish:
        return None
    return {"aperture": tags.get("com.blackmagic-design.camera.aperture"), "depth_track": has_dish,
            "dur": float(d.get("format", {}).get("duration", 0) or 0)}


def resolve(clip: str) -> Path:
    p = Path(clip).expanduser()
    if p.is_absolute() or p.exists():
        return p
    return STUDIO / clip


def rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(STUDIO))
    except ValueError:
        return str(p)


def fnumber_for(path: Path, default: float | None, per_clip: dict[str, float]) -> float | None:
    for key, f in per_clip.items():
        if path.stem == key or path.stem.endswith("_" + key):
            return f
    return default


def label(f: float | None) -> str:
    return "frec" if f is None else f"f{f:g}".replace(".", "p")


def check(paths: list[Path]) -> None:
    files = [q for p in paths for q in (sorted(p.rglob("*")) if p.is_dir() else [p])
             if q.suffix.lower() in VIDEO and not q.name.startswith("._")
             and not any(part.lower() in ("proxy", "proxies") for part in q.parts)]   # app proxies carry no depth
    n = 0
    for f in files:
        info = cinematic_info(f)
        if info:
            n += 1
        print(f"{'cinematic' if info else '-        '}  {(info or {}).get('aperture') or '':6} {rel(f)}")
    print(f"{n} of {len(files)} clips are Cinematic Video" + (": bake them before previews, sheets and Premiere" if n else ""))


def bake_edl(edl_path: Path, default_f: float | None, per_clip: dict[str, float], handle: float, force: bool) -> None:
    edl = json.loads(edl_path.read_text())
    shots = edl if isinstance(edl, list) else edl.get("shots", [])
    reel_fps = float((edl.get("fps") if isinstance(edl, dict) else 0) or 0)
    reel = edl_path.resolve().parent.parent
    out_dir = reel / "raw" / "baked"
    spans: dict[Path, list[list[float]]] = {}
    cine: dict[Path, dict] = {}
    for s in shots:
        if not s.get("clip"):
            continue
        cam = resolve(s["clip"])
        if cam not in cine:
            cine[cam] = cinematic_info(cam) if cam.exists() else None
        if not cine[cam]:
            continue
        fps = reel_fps or fps_of(cam)
        rate = float(s.get("rate", 1.0))
        a = float(s.get("src_in", 0))
        b = a + (float(s["end"]) - float(s["start"])) * rate if rate > 0 else a + 1 / fps
        spans.setdefault(cam, []).append([a, b])
    if not spans:
        print("no Cinematic clips in this EDL: nothing to bake")
        return
    binary = ensure_binary()
    out_dir.mkdir(parents=True, exist_ok=True)
    bmap = []
    for cam, sp in spans.items():
        cam_fps = fps_of(cam)
        dur_all = cine[cam]["dur"]
        merged: list[list[float]] = []
        for a, b in sorted(sp):
            if merged and a - merged[-1][1] < MERGE_GAP:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        f = fnumber_for(cam, default_f, per_clip)
        for a, b in merged:
            start = max(0.0, round((a - handle) * cam_fps) / cam_fps)
            end = min(dur_all, round((b + handle) * cam_fps) / cam_fps)
            dst = out_dir / f"{cam.stem}_{label(f)}_{start:05.2f}-{end:05.2f}.mov"
            entry = {"camera": rel(cam), "baked": rel(dst), "start": round(start, 4), "dur": round(end - start, 4),
                     "fnumber": f if f is not None else "recorded", "aperture_recorded": cine[cam]["aperture"]}
            if dst.exists() and not force:
                print(f"reuse  {dst.name}")
            else:
                cmd = [str(binary), str(cam), str(dst), "--start", f"{start:.4f}", "--dur", f"{end - start:.4f}", "--audio"]
                if f is not None:
                    cmd += ["--fnumber", f"{f:g}"]
                r = subprocess.run(cmd, capture_output=True, text=True)
                if r.returncode or not dst.exists():
                    sys.exit(f"bake failed on {cam.name}: {(r.stderr or r.stdout)[-1500:]}")
                print(f"baked  {dst.name}  {start:.2f}+{end - start:.2f} s at {label(f)}")
            bmap.append(entry)

    def bake_for(cam: Path, t: float) -> dict | None:
        for e in bmap:
            if e["camera"] == rel(cam) and e["start"] - 1e-6 <= t <= e["start"] + e["dur"] + 1e-6:
                return e
        return None

    new = json.loads(edl_path.read_text())
    new_shots = new if isinstance(new, list) else new["shots"]
    moved = 0
    for s in new_shots:
        if not s.get("clip"):
            continue
        cam = resolve(s["clip"])
        if not cine.get(cam):
            continue
        e = bake_for(cam, float(s.get("src_in", 0)))
        if e is None:
            sys.exit(f"internal: no bake covers {s.get('name')} at {s.get('src_in')}")
        s["clip"] = e["baked"]
        s["src_in"] = round(float(s.get("src_in", 0)) - e["start"], 4)
        moved += 1
    if isinstance(new, dict):
        new["note"] = ((new.get("note") or "") + f" Cinematic depth baked by scripts/cine_bake.py from {edl_path.name} "
                       f"(map: bake_map_{edl_path.stem}.json).").strip()
    map_path = edl_path.parent / f"bake_map_{edl_path.stem}.json"
    out_edl = edl_path.parent / f"{edl_path.stem}_baked.json"
    map_path.write_text(json.dumps(bmap, indent=1))
    out_edl.write_text(json.dumps(new, indent=1, ensure_ascii=False))
    print(f"✓ {len(bmap)} bakes, {moved} shots moved to them")
    print(f"✓ {rel(map_path)}")
    print(f"✓ {rel(out_edl)}  ← preview, storyboard, pregate and the Premiere build read this one")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", nargs="+", type=Path, metavar="CLIP", help="clips or folders to test for Cinematic Video")
    g.add_argument("--edl", type=Path, help="analysis/edl_v<N>.json")
    ap.add_argument("--fnumber", type=float, help="f-number for every clip (default: the recorded one)")
    ap.add_argument("--fnumber-for", action="append", default=[], metavar="CLIP=F",
                    help="f-number for one clip, by camera file stem or clip number (repeatable)")
    ap.add_argument("--handle", type=float, default=0.48, help="seconds baked either side of the used span")
    ap.add_argument("--force", action="store_true", help="re-bake even when the bake file exists")
    a = ap.parse_args()
    if a.check:
        check(a.check)
        return
    per_clip = {}
    for item in a.fnumber_for:
        k, _, v = item.partition("=")
        try:
            per_clip[k.strip()] = float(v)
        except ValueError:
            sys.exit(f"--fnumber-for wants CLIP=F, got {item!r}")
    bake_edl(a.edl, a.fnumber, per_clip, a.handle, a.force)


if __name__ == "__main__":
    main()
