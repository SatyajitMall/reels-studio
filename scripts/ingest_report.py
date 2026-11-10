#!/usr/bin/env python3
"""Ingest check (skill Phase 1, before analyze_footage.py): what the camera actually recorded, and what that means
for the edit. Built for the director's Blackmagic Cam (iPhone) footage; works on any clips.

Per clip it reads
  file     codec, profile, bit depth, colour tags (Rec.709 / log / HDR), rotation, bitrate, frame rate and whether it's
           variable (average ≠ nominal), duration
  camera   the app's own metadata: software, lens, white balance (K / tint), shutter, ISO, sensor fps, slate note
  picture  3 stills (25/50/75 %): black and white points, saturation, colour cast (mid R−B warm/cool, G−M green/magenta)
and flags
  8-bit           grade gently: big pushes band and block on 8-bit HEVC
  log / HDR       colour tags say log or HDR, or the picture is flat and grey (a log clip needs a conversion first)
  LUT             whether a LUT was burned in is NOT recorded by Blackmagic Cam. It's read from the slate note only
                  if the director typed it there (shooting guide); otherwise "not recorded"
  flicker risk    shutter vs mains lighting (--mains 50 for India/Europe): exposure that isn't a whole number of lamp
                  pulses (1/100 s at 50 Hz) pulses; the frame rate decides how it shows (30 fps → 10 Hz, a 3-frame cycle;
                  25 fps → 0 Hz, no pulsing). Only matters under mains-powered light (LED, tube, bulbs)
  variable fps    frames may be missing; with --scan, the gaps and the picture jumps they cause are listed with times
  colour cast     strong warm / cool / green cast, usually a white balance set for another light
  cinematic       Apple Cinematic Video (Cinematic mode): the depth of field is a separate track only Apple apps
                  draw, so the picture here is sharp. Bake with scripts/cine_bake.py before anything else reads it
--scan decodes every frame (small) to MEASURE flicker (lock-in on the lamp alias, whole frame and 6 horizontal
bands, since rolling shutters band) and to find jumps (frame difference > 6× the clip's median). Slower: use it on the
reel's own clips, not a whole card.

Writes <out>/ingest.md (summary, match groups, per-clip table) and <out>/ingest.json.

Usage:
  ./.venv/bin/python scripts/ingest_report.py projects/<reel>/raw -o projects/<reel>/analysis --scan
  ./.venv/bin/python scripts/ingest_report.py "~/Documents/Video /Pujo 2026 Oct 20" -o /tmp/ingest      # a whole card, fast
"""
from __future__ import annotations

import argparse
import colorsys
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

VIDEO = (".mov", ".mp4", ".m4v", ".mxf", ".mkv")
GENERIC = {"media", "clips", "dcim", "footage", "video", "videos", "b-roll", "a-roll", "raw"}


def find_clips(paths: list[Path]) -> list[Path]:
    out = []
    for p in paths:
        if p.is_file():
            out.append(p)
            continue
        for dirpath, dirnames, files in os.walk(p, followlinks=True):
            dirnames[:] = [d for d in dirnames if d.lower() not in ("proxy", "proxies") and "ref" not in d.lower()]
            out += [Path(dirpath) / f for f in files if f.lower().endswith(VIDEO) and not f.startswith("._")]
    return sorted(set(out))


def frac(s: str | None) -> float:
    try:
        n, d = (s or "0/1").split("/")
        return float(n) / float(d) if float(d) else 0.0
    except ValueError:
        return 0.0


def shoot_night(stamp: str | None) -> str | None:
    """The shoot a clip belongs to, from the camera's local recording time. Clips before 06:00 count with the evening
    before, so a Pujo night that runs past midnight stays one shoot."""
    if not stamp:
        return None
    try:
        t = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (t - timedelta(hours=6)).date().isoformat()


def probe(p: Path) -> dict:
    d = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(p)],
                                  capture_output=True, text=True).stdout or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    t = d.get("format", {}).get("tags", {})
    rot = next((x.get("rotation") for x in v.get("side_data_list", []) if "rotation" in x), 0)
    cinematic = (t.get("com.apple.quicktime.cinematic-video-intent") == "1"
                 or any(s.get("codec_tag_string") == "dish" for s in d.get("streams", [])))   # disparity track
    bits = 10 if "10" in (v.get("pix_fmt") or "") or v.get("profile") in ("Main 10", "High 10") else 8
    note = " · ".join(x for x in (t.get("com.apple.proapps.logNote"), t.get("com.blackmagic-design.camera.projectName"),
                                  t.get("com.apple.quicktime.comment"), t.get("comment")) if x)
    real = p.resolve()                                                    # a reel links (or copies) clips from the card
    shoot = real.parent if real.parent.name.strip().lower() not in GENERIC else real.parent.parent
    recorded = t.get("com.blackmagic-design.camera.dateRecorded") or t.get("com.apple.quicktime.creationdate") or t.get("creation_time")
    return {"clip": p.name, "path": str(p), "folder": shoot.name.strip(), "night": shoot_night(recorded),
            "codec": v.get("codec_name"), "profile": v.get("profile"), "pix_fmt": v.get("pix_fmt"), "bits": bits,
            "transfer": v.get("color_transfer"), "primaries": v.get("color_primaries"),
            "w": v.get("width"), "h": v.get("height"), "rotation": rot,
            "fps": round(frac(v.get("r_frame_rate")), 3), "avg_fps": round(frac(v.get("avg_frame_rate")), 3),
            "mbps": round(int(d.get("format", {}).get("bit_rate", 0) or 0) / 1e6, 1),
            "dur": round(float(d.get("format", {}).get("duration", 0) or 0), 2),
            "software": t.get("com.apple.quicktime.software") or t.get("encoder"),
            "lens": t.get("com.blackmagic-design.camera.lensType") or t.get("com.apple.quicktime.model"),
            "wb_k": t.get("com.blackmagic-design.camera.whiteBalanceKelvin"),
            "wb_tint": t.get("com.blackmagic-design.camera.whiteBalanceTint"),
            "shutter": t.get("com.blackmagic-design.shutterSpeed"), "iso": t.get("com.blackmagic-design.camera.iso"),
            "sensor_fps": t.get("com.blackmagic-design.sensorFPS"),
            "cinematic": cinematic, "aperture": t.get("com.blackmagic-design.camera.aperture"),
            "recorded": recorded, "note": note}


def stills(r: dict) -> dict:
    acc = defaultdict(list)
    for f in (0.25, 0.5, 0.75):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{r['dur'] * f:.2f}", "-i", r["path"], "-frames:v", "1",
                              "-vf", "scale=192:108,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
        if len(raw) < 192 * 108 * 3:
            continue
        a = np.frombuffer(raw, np.uint8)[: 192 * 108 * 3].reshape(108, 192, 3).astype(np.float32) / 255
        R, G, B = a[..., 0], a[..., 1], a[..., 2]
        y = 0.2126 * R + 0.7152 * G + 0.0722 * B
        mx, mn = a.max(2), a.min(2)
        sat = np.where(mx > 0.05, (mx - mn) / np.maximum(mx, 1e-3), 0)
        mid = (y >= 0.15) & (y < 0.6)
        acc["luma"].append(float(y.mean()))
        acc["p02"].append(float(np.percentile(y, 2)))
        acc["p98"].append(float(np.percentile(y, 98)))
        acc["sat"].append(float(sat[y > 0.1].mean()) if (y > 0.1).any() else 0.0)
        if mid.sum() > 50:
            acc["rb"].append(float((R - B)[mid].mean()))
            acc["gm"].append(float((G - (R + B) / 2)[mid].mean()))
            acc["hue"].append(colorsys.rgb_to_hsv(R[mid].mean(), G[mid].mean(), B[mid].mean())[0] * 360)
    return {k: round(float(np.mean(v)), 3) for k, v in acc.items()}


def flicker_risk(shutter: str | None, fps: float, mains: float) -> dict:
    """Rate mains flicker from metadata. Lamps pulse at 2 × mains. An exposure of a whole number of pulses is safe;
    otherwise each frame catches a different part of the pulse, aliased to |2·mains − k·fps|."""
    if not shutter or "/" not in shutter or not fps:
        return {"risk": "unknown", "why": "no shutter in metadata"}
    expo = frac(shutter)
    pulse = 2 * mains
    cycles = expo * pulse
    resid = abs(cycles - round(cycles))
    k = round(pulse / fps)
    alias = min(abs(pulse - j * fps) for j in (max(k - 1, 1), k, k + 1))
    period = round(fps / alias, 1) if alias > 0.5 else None
    if resid < 0.05 and round(cycles) >= 1:
        return {"risk": "safe", "why": f"{shutter} s = {round(cycles)} lamp pulses", "alias_hz": alias, "period_frames": period}
    if alias <= 0.5:
        return {"risk": "static", "why": f"{fps:g} fps locks to the {pulse:g} Hz pulse: no pulsing, possible fixed bands",
                "alias_hz": alias, "period_frames": None}
    strength = resid / max(cycles, 0.5)
    level = "high" if strength >= 0.1 else "low"
    return {"risk": level, "why": f"{shutter} s at {fps:g} fps → {alias:g} Hz flicker ({period}-frame cycle)",
            "alias_hz": alias, "period_frames": period}


def scan(r: dict) -> dict:
    """Every frame at 64×36 grey: lock-in flicker amplitude at the alias period, and frame-difference jumps.
    Frame times come from the packets, so gaps (dropped frames on variable-rate clips) are found too."""
    W, H = 64, 36
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", r["path"], "-fps_mode", "passthrough", "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (W * H)
    if n < 10:
        return {}
    fr = np.frombuffer(raw, np.uint8)[: n * W * H].reshape(n, H, W).astype(np.float32) / 255
    pts = sorted(float(x.split(",")[0]) for x in subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time", "-of", "csv=p=0", r["path"]],
        capture_output=True, text=True).stdout.split() if x.split(",")[0] not in ("", "N/A"))
    pts = pts[:n] if len(pts) >= n else list(np.arange(n) / (r["fps"] or 25))
    out: dict = {}
    # Gaps: a frame interval longer than 1.5 nominal frames
    nominal = 1 / (r["fps"] or 25)
    gaps = [(round(pts[i], 2), round((pts[i] - pts[i - 1]) / nominal - 1)) for i in range(1, len(pts)) if pts[i] - pts[i - 1] > 1.5 * nominal]
    out["dropped"] = sum(g[1] for g in gaps)
    # Jumps: an isolated spike, a frame difference > 6× the clip median and > 3× both neighbours.
    # (A fast pan is high on every frame, so it doesn't count; a snap to a new framing does.)
    d = np.abs(np.diff(fr, axis=0)).mean((1, 2)) * 255
    med = float(np.median(d)) or 0.1
    nb = np.maximum(np.r_[d[1:2], d[:-1]], np.r_[d[1:], d[-2:-1]])
    jumps = [round(pts[i + 1], 2) for i in np.where((d > 6 * med) & (d > 8) & (d > 3 * nb))[0]]
    out["jumps"] = jumps[:12]
    out["gap_times"] = [g[0] for g in gaps[:12]]
    # Flicker: lock-in on the alias period, in 2 s blocks (phase drifts on variable-rate clips), whole frame + 6 bands
    P = r.get("flicker", {}).get("period_frames")
    if P and 2 <= P <= 30:
        series = [fr.mean((1, 2))] + [fr[:, b * H // 6:(b + 1) * H // 6].mean((1, 2)) for b in range(6)]
        blk = int(max(4 * P, 2 * (r["fps"] or 25)))
        amps = []
        for s in series:
            k = np.ones(int(round(P))) / int(round(P))
            trend = np.convolve(s, k, mode="same")
            det = (s - trend) / np.maximum(trend, 1e-3)
            a_blocks = []
            for i in range(0, len(det) - blk + 1, blk):
                seg = det[i:i + blk]
                ph = np.exp(-2j * np.pi * np.arange(len(seg)) / P)
                a_blocks.append(2 * abs((seg * ph).sum()) / len(seg))
            amps.append(float(np.median(a_blocks)) * 100 if a_blocks else 0.0)
        out["flicker_global_pct"] = round(amps[0], 2)
        out["flicker_band_pct"] = round(max(amps[1:]), 2)
    return out


def flags(r: dict) -> list[str]:
    f = []
    if r.get("cinematic"):
        f.append("cinematic")
    if r["bits"] == 8:
        f.append("8-bit")
    # Log looks flat AND lifted: grey blacks, mid-grey average, little colour. Dark shots are flat too, so they need the lift.
    flat_log = (r.get("p02", 0) >= 0.06 and r.get("p98", 1) - r.get("p02", 0) < 0.55 and r.get("sat", 1) < 0.3
                and 0.2 <= r.get("luma", 0) <= 0.6)
    if r["transfer"] in ("arib-std-b67", "smpte2084") or flat_log:
        f.append("log/HDR?")
    if r.get("luma", 1) < 0.05:
        f.append("very dark")
    if r["fps"] and r["avg_fps"] and abs(r["avg_fps"] - r["fps"]) / r["fps"] > 0.001:
        f.append("VFR")
    fl = r["flicker"]["risk"]
    if fl == "high":
        f.append("flicker risk")
    m = r.get("measured", {})
    if max(m.get("flicker_global_pct", 0), m.get("flicker_band_pct", 0)) >= 1.0:
        f.append(f"FLICKER {max(m['flicker_global_pct'], m['flicker_band_pct']):.1f}%")
    if m.get("jumps"):
        f.append(f"jumps {len(m['jumps'])}")
    rb, gm = r.get("rb", 0), r.get("gm", 0)
    if rb > 0.30:
        f.append("warm cast")
    elif rb < -0.02:
        f.append("cool cast")
    if gm > 0.03:
        f.append("green cast")
    if r["mbps"] and (r["w"] or 0) * (r["h"] or 0) >= 3840 * 2160 and r["mbps"] < 20:
        f.append("low bitrate")
    return f


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+", type=Path, help="folders (searched recursively, links followed) or clips")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--mains", type=float, default=50.0, help="mains frequency where it was shot (India 50, USA 60)")
    ap.add_argument("--scan", action="store_true", help="decode every frame: measure flicker, find dropped frames and jumps")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    clips = find_clips([Path(os.path.expanduser(str(p))) for p in a.paths])
    if not clips:
        sys.exit("No clips found")
    a.out.mkdir(parents=True, exist_ok=True)

    def one(p: Path) -> dict:
        r = probe(p)
        r.update(stills(r))
        r["flicker"] = flicker_risk(r["shutter"], r["fps"], a.mains)
        if a.scan:
            r["measured"] = scan(r)
        r["flags"] = flags(r)
        return r

    with ThreadPoolExecutor(a.workers) as ex:
        rows = list(ex.map(one, clips))

    # Summary
    n = len(rows)
    fps_c = Counter(r["fps"] for r in rows)
    seq_fps = fps_c.most_common(1)[0][0]
    flag_c = Counter(x.split(" ")[0] if x.startswith(("FLICKER", "jumps")) else x for r in rows for x in r["flags"])
    fl_c = Counter(r["flicker"]["risk"] for r in rows)
    combos = Counter((r["fps"], r["shutter"]) for r in rows if r["flicker"]["risk"] == "high")
    md = [f"# Ingest report ({n} clips)", "",
          f"- **Sources:** {', '.join(f'{k} ({v})' for k, v in Counter(r['software'] for r in rows).most_common(3))}",
          f"- **Codec:** {', '.join(f'{k} ({v})' for k, v in Counter(f'{r['codec']} {r['profile']} {r['bits']}-bit' for r in rows).most_common(3))}; "
          f"colour tags {', '.join(f'{k} ({v})' for k, v in Counter(r['transfer'] for r in rows).most_common(3))}; "
          f"{np.median([r['mbps'] for r in rows]):.0f} Mb/s median",
          f"- **Frame rates:** {', '.join(f'{k:g} ({v})' for k, v in fps_c.most_common())}. Sequence: **{seq_fps:g} fps** (most clips); "
          "conform the others by interpretation before placing them (CLAUDE.md §3).",
          f"- **Burned-in LUT:** not recorded by the camera app. "
          + (f"Slate notes found on {sum(1 for r in rows if r['note'])} clips (column Note)." if any(r["note"] for r in rows)
             else "No slate notes either: **ask the director** which clips carry a LUT, and look for an already-graded look on the stills."),
          "", "## Flags", "",
          "| Flag | Clips | What to do |", "|---|---|---|"]
    advice = {
        "cinematic": "Cinematic mode: the depth of field the director saw on the phone is a separate track that only Apple apps draw; "
                     "Premiere, ffmpeg and our scripts see it sharp. Bake first (scripts/cine_bake.py --edl, at the recorded "
                     "f-number) and point previews, sheets, checks and Premiere at the bakes (CLAUDE.md §5)",
        "8-bit": "Grade gently: primary pushes ≤ about ½ stop and modest saturation; strong looks band. Our own renders stay 10-bit ProRes",
        "log/HDR?": "Check the stills: a flat, grey clip needs a log → Rec.709 conversion before anything else (CLAUDE.md §2.5 exception)",
        "VFR": "Variable frame rate: check placed windows for jumps (run with --scan); avoid the listed gap times",
        "flicker risk": f"Shutter vs {a.mains:g} Hz lamps: expect pulsing on lamp-lit shots. Measure with --scan; deflicker before shot matching (CR mains-flicker)",
        "FLICKER": "Measured ≥ 1 % flicker: deflicker this clip before colour, or don't use it",
        "jumps": "Picture jumps inside the clip (dropped frames or a jolt): keep the placed window clear of the listed times",
        "warm cast": "White balance set cooler than the light (e.g. 5600 K under warm pandal lamps): cool it in the primary, per match group",
        "cool cast": "Cool cast (daylight/LED under a warm white balance): warm it in the primary",
        "green cast": "Green cast, usual under LED or tube light: add magenta (tint) in the primary",
        "low bitrate": "Low bitrate for 4K: expect blocking in dark areas; keep grades light",
        "very dark": "Mean brightness under 0.05 on the stills: probably unusable, or only for a black-out moment. Lifting it in 8-bit shows noise and blocks",
    }
    for k, v in flag_c.most_common():
        md.append(f"| {k} | {v} | {advice.get(k, '')} |")
    md += ["", f"Flicker from metadata ({a.mains:g} Hz mains): " + ", ".join(f"{k} {v}" for k, v in fl_c.most_common())
           + (". Most common risky settings: " + ", ".join(f"{f:g} fps at {s}" for (f, s), _ in combos.most_common(3)) if combos else "")
           + ". It only shows under mains-powered light, so outdoor daylight shots at risky settings are fine.", ""]
    # Match groups: same folder (shoot) and white balance
    groups = defaultdict(list)
    for r in rows:
        groups[(r["night"] or r["folder"], r["wb_k"])].append(r)
    md += ["## Match groups (same shoot night, same white balance)", "",
           "Start each group from one primary correction, then match shots within it (playbook §A1–A2).", "",
           "| Shoot night | WB | Clips | Mid R−B | G−M | Sat | Luma | Read |", "|---|---|---|---|---|---|---|---|"]
    for (folder, wb), g in sorted(groups.items(), key=lambda x: (x[0][0], str(x[0][1]))):
        rb = np.median([r.get("rb", 0) for r in g])
        gm = np.median([r.get("gm", 0) for r in g])
        read = "warm: cool it" if rb > 0.30 else "cool: warm it" if rb < -0.02 else "near neutral"
        if gm > 0.03:
            read += "; green: add magenta"
        md.append(f"| {folder} | {wb or '–'} K | {len(g)} | {rb:+.2f} | {gm:+.3f} | {np.median([r.get('sat', 0) for r in g]):.2f} | "
                  f"{np.median([r.get('luma', 0) for r in g]):.2f} | {read} |")
    md += ["", "## Clips", "",
           "| Clip | Shoot night | fps (avg) | Shutter | WB | ISO | Lens | Mb/s | Flicker | Measured | Note | Flags |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["night"] or r["folder"], r["clip"])):
        m = r.get("measured", {})
        meas = (f"{m.get('flicker_global_pct', '–')} / {m.get('flicker_band_pct', '–')} %" if "flicker_global_pct" in m else "")
        if m.get("jumps"):
            meas += f" · jumps at {', '.join(f'{t:g}' for t in m['jumps'][:4])} s"
        if m.get("dropped"):
            meas += f" · {m['dropped']} dropped"
        md.append(f"| {Path(r['clip']).stem} | {r['night'] or r['folder']} | {r['fps']:g} ({r['avg_fps']:g}) | {r['shutter'] or '–'} | {r['wb_k'] or '–'} | "
                  f"{r['iso'] or '–'} | {(r['lens'] or '–').replace('iPhone 17 ', '')}{' ' + r['aperture'] if r.get('aperture') else ''} | {r['mbps']:g} | {r['flicker']['risk']} | {meas} | "
                  f"{r['note'] or ''} | {', '.join(r['flags'])} |")
    (a.out / "ingest.md").write_text("\n".join(md) + "\n")
    (a.out / "ingest.json").write_text(json.dumps(rows, indent=1, default=str))
    print("\n".join(md[:md.index("## Match groups (same shoot night, same white balance)")]))
    print(f"✓ {a.out / 'ingest.md'}")


if __name__ == "__main__":
    main()
