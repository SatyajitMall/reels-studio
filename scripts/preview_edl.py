#!/usr/bin/env python3
"""Offline preview of a cut, built from its EDL straight off the camera files: no Premiere, a few minutes per version.

Pace, picks, framing and slow-mo windows are settled on these previews, so Premiere gets one build at the end for the
grade and finishing (skill Phases 2–3; promoted from Pujo's preview_assemble.py, which built v6–v10 while Premiere was
busy with another reel). The colour is the camera's own, plus an optional approximate primary per shot. It is NOT the
Lumetri grade: the final grade is judged on the Premiere export (goddess approved a look on stills and rejected it on the
full reel). Every preview carries a small "offline preview" label in the top band unless --clean.

The EDL (analysis/edl_v<N>.json) is one JSON object. The same file is the shot map pregate.py, camera_fidelity.py,
render_diff.py and storyboard.py read, and the plan the Premiere build follows:

{"fps": 25,                                                 "runtime": 29.84 optional (default: the last shot's end)
 "shots": [
  {"name": "05_C051", "start": 8.40, "end": 10.20,          reel seconds; frames = round(t × fps)
   "clip": "projects/<reel>/raw/b-roll/A001_10212101_C051.mov",
   "src_in": 4.00,                                         camera seconds at the shot's first frame
   "rate": 0.553,                                          camera s per reel s: speed (0.5 = half), × interpreted/native
                                                           fps for a conformed clip; 0 = a freeze frame; default 1.
                                                           Slow-mo here repeats frames: the final uses AE Timewarp
                                                           (effects-playbook §C)
   "scale": 56,                                            Premiere Motion Scale %, or keys [[t, scale], …] (t = s from
                                                           the shot's start). Default: fill the 9:16 frame (50 on
                                                           vertical 4K)
   "pos": [540, 960],                                      Premiere Motion Position (sequence px), or keys [[t, x, y], …]
   "ease": "ease",                                         between keys: "ease" (Premiere ease in + out) or "linear"
   "rotation": 0,                                          degrees, as Premiere's Rotation (180 for an upside-down clip)
   "grade": {"exposure": 0.0, "sat": 1.0},                 approximate primary: stops, saturation × (camera-true = none)
   "dissolve": 0,                                          frames of cross dissolve centred on this shot's first cut
   "fade_in": 0, "fade_out": 0,                            frames from / to black (the picture only, not the overlays)
   "audio_db": null,                                       the clip's own sound at this gain (dialogue); null = muted
   "line": "and that's the whole point of Pujo.",          the VO / dialogue line this shot carries (Phase 2 line table)
   "shows": "Ma's face as the chandelier lands"},          what in the frame shows the line
  {"name": "end_card", "start": 27.30, "end": 29.84, "image": "projects/<reel>/renders/overlays/endcard.png"}
 ],
 "overlays": [{"file": "projects/<reel>/renders/overlays/subs/sub_01.png", "start": 0.30, "end": 2.20}],
 "audio": [{"file": "projects/<reel>/audio/vo.wav", "start": 0.0, "in": 0.0, "gain_db": 0.0, "fade_in": 0, "fade_out": 0.5}]}

A shot without "clip" is black, or "image" (a still, filled to the frame). Overlays are 1080×1920 PNGs or alpha .mov
renders (V5), drawn above everything. Audio: the listed tracks plus each shot's own sound where "audio_db" is set,
summed and limited at −1 dBFS, not loudness-normalised (pregate a preview with --profile ig-quiet). A plain shot map (a
JSON list) also works, with --fps. Paths are relative to the studio root.

Checks before rendering (exit 1): missing clips, a shot that runs past its clip's end, overlapping shots, unknown keys.
Reported per shot: the narrowest width shown (% of the widest 9:16 framing, at the largest Scale; ≥ 80 % is the default,
effects-playbook §B), and black edges at any key or at 9 points across the shot. A dissolve on the first shot or after a
gap is ignored, with a warning. Shot names must be unique.

--only 03_C042,07_C035 renders just those shots back to back (a grade sample of the hardest shots) and writes the
re-timed EDL next to the output, so camera_fidelity.py / pregate.py can run on the sample.

Usage (from the studio root):
  ./.venv/bin/python scripts/preview_edl.py projects/<reel>/analysis/edl_v3.json -o projects/<reel>/renders/previews/<reel>_p3.mp4
      [--only <names>] [--guides] [--clean] [--fps 25]
For a ≤ 29 MB copy to send: scripts/encode_master.py <preview> -o <…_phone.mp4> --phone
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from camera_fidelity import EXACT, probe   # noqa: E402  (exact YUV→RGB flags; display size after the rotation flag, fps, duration)
from encode_master import PICTURE, has_audio  # noqa: E402  (H.264 High, BT.709 TV range, tagged)

W, H = 1080, 1920
SAFE = {"top": 220, "bottom": 320, "right": 120}      # Instagram UI bands (CLAUDE.md §3)
LUMA = np.array([0.2126, 0.7152, 0.0722], np.float32)
SHOT_KEYS = {"name", "start", "end", "clip", "src_in", "rate", "scale", "pos", "ease", "rotation", "grade", "dissolve",
             "fade_in", "fade_out", "audio_db", "image", "line", "shows", "role", "note", "text"}
EDL_KEYS = {"fps", "runtime", "shots", "overlays", "audio", "note"}
OVERLAY_KEYS = {"file", "start", "end"}
AUDIO_KEYS = {"file", "start", "in", "dur", "gain_db", "fade_in", "fade_out"}
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


# ---------- the EDL ----------
def load_edl(path: Path, fps: float | None = None) -> dict:
    data = json.loads(path.read_text())
    edl = {"shots": data} if isinstance(data, list) else dict(data)
    edl["fps"] = float(fps or edl.get("fps") or 0)
    if not edl["fps"]:
        sys.exit(f"{path}: no fps (add \"fps\" to the EDL or pass --fps)")
    edl.setdefault("overlays", [])
    edl.setdefault("audio", [])
    unnamed = [i + 1 for i, s in enumerate(edl["shots"]) if not s.get("name")]
    if unnamed:
        sys.exit(f"{path}: shots {unnamed} have no \"name\" (every tool reading the EDL keys on it, e.g. \"05_C051\")")
    return edl


def frames(t: float, fps: float) -> int:
    return int(round(t * fps))


def fps_arg(fps: float) -> str:
    for exact, rational in ((29.97, "30000/1001"), (23.976, "24000/1001"), (59.94, "60000/1001")):
        if abs(fps - exact) < 0.01:
            return rational
    return f"{fps:g}"


def keyed(value, t: float, ease: str) -> list[float]:
    """A Premiere-style property: a constant ([540, 960] or 56) or keys [[t, v…], …], held before the first and after the last."""
    if not isinstance(value, list) or not value or not isinstance(value[0], list):
        return [float(v) for v in (value if isinstance(value, list) else [value])]
    keys = sorted(value, key=lambda k: k[0])
    if t <= keys[0][0]:
        return [float(v) for v in keys[0][1:]]
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(b[0] - a[0], 1e-9)
            if ease == "ease":
                u = u * u * (3 - 2 * u)
            return [float(x) + (float(y) - float(x)) * u for x, y in zip(a[1:], b[1:])]
    return [float(v) for v in keys[-1][1:]]


def key_values(value) -> list[list[float]]:
    if isinstance(value, list) and value and isinstance(value[0], list):
        return [[float(v) for v in k[1:]] for k in value]
    return [[float(v) for v in (value if isinstance(value, list) else [value])]]


def fill_scale(sw: int, sh: int) -> float:
    """The Scale (%) that just fills the 9:16 frame: the widest framing a clip allows."""
    return 100 * max(W / sw, H / sh)


class Framing:
    """One shot's Motion settings over time, in Premiere's terms: Scale (%), Position (sequence px), Rotation (deg)."""

    def __init__(self, shot: dict, sw: int, sh: int):
        self.sw, self.sh = sw, sh
        self.scale = shot.get("scale", fill_scale(sw, sh))
        self.pos = shot.get("pos", [W / 2, H / 2])
        self.ease = shot.get("ease", "ease")
        rot = shot.get("rotation", 0)
        self.rot = math.radians(float(rot)) if isinstance(rot, (int, float)) else 0.0   # check() reports anything else

    def at(self, t: float) -> tuple[float, float, float]:
        s = keyed(self.scale, t, self.ease)[0] / 100
        px, py = keyed(self.pos, t, self.ease)
        return s, px, py

    def min_scale(self) -> float:
        return min(v[0] for v in key_values(self.scale)) / 100

    def min_width_pct(self) -> float:
        """The narrowest width shown (at the largest Scale), % of the widest 9:16 framing."""
        return 100 * fill_scale(self.sw, self.sh) / max(v[0] for v in key_values(self.scale))

    def key_times(self) -> list[float]:
        return [float(k[0]) for v in (self.scale, self.pos) if isinstance(v, list) and v and isinstance(v[0], list) for k in v]

    def width_pct(self, t: float) -> float:
        return 100 * fill_scale(self.sw, self.sh) / 100 / self.at(t)[0]

    def affine(self, t: float, fx: float, fy: float) -> tuple[float, ...]:
        """Output pixel → prescaled source pixel (PIL's inverse affine)."""
        s, px, py = self.at(t)
        c, sn = math.cos(self.rot), math.sin(self.rot)
        return (fx * c / s, fx * sn / s, fx * (self.sw / 2 + (-c * px - sn * py) / s),
                -fy * sn / s, fy * c / s, fy * (self.sh / 2 + (sn * px - c * py) / s))

    def crop(self, fx: float, fy: float, pw: int, ph: int) -> tuple[int, int] | None:
        """For a static, unrotated shot whose prescale already gives the output scale: the integer crop origin, so the
        frame is copied, not resampled (a sub-pixel bicubic resample added about 1 point of crush on dark noise).
        None when the shot needs the transform (keys, rotation, enlargement, or black edges)."""
        if self.key_times() or self.rot:
            return None
        a, _, c, _, e, f = self.affine(0, fx, fy)
        if abs(a - 1) > 0.005 or abs(e - 1) > 0.005:
            return None
        x0, y0 = int(round(c)), int(round(f))
        return (x0, y0) if 0 <= x0 and 0 <= y0 and x0 + W <= pw and y0 + H <= ph else None

    def covers(self, t: float) -> bool:
        a, b, c, d, e, f = self.affine(t, 1.0, 1.0)
        for x, y in ((0, 0), (W, 0), (0, H), (W, H)):
            u, v = a * x + b * y + c, d * x + e * y + f
            if u < -0.5 or v < -0.5 or u > self.sw + 0.5 or v > self.sh + 0.5:
                return False
        return True


def prescale(fr: Framing) -> float:
    """Source reduction (ffmpeg, area) to the shot's smallest scale, so the per-frame transform only enlarges, by at
    most the push (no aliasing, and a static shot is close to a 1:1 copy)."""
    return min(1.0, fr.min_scale())


def grade_fn(grade: dict | None):
    """The approximate primary: exposure in stops (on a 2.2 gamma) and a saturation multiplier."""
    if not grade:
        return None
    ev, sat = float(grade.get("exposure", 0)), float(grade.get("sat", 1))
    x = np.arange(256, dtype=np.float32) / 255
    lut = (np.clip(x ** 2.2 * 2 ** ev, 0, 1) ** (1 / 2.2) * 255 + 0.5).astype(np.uint8)

    def apply(img: np.ndarray) -> np.ndarray:
        out = lut[img] if ev else img
        if sat != 1:
            f = out.astype(np.float32)
            y = (f @ LUMA)[..., None]
            out = np.clip(y + (f - y) * sat + 0.5, 0, 255).astype(np.uint8)
        return out
    return apply


# ---------- decoding ----------
class Reader:
    """Sequential frames of one shot from its camera file, at the reel's fps: nearest camera frame for each reel frame
    (Premiere without frame blending), upright (the rotation flag is applied), reduced by `f`. Holds the last frame
    when the file runs out."""

    def __init__(self, clip: Path, t0: float, rate: float, fps: float, n: int, size: tuple[int, int]):
        self.size, self.n, self.last, self.lead, self.held = size, n, None, 0, False
        if t0 < 0:                                          # a dissolve handle before the clip's first frame: hold it
            self.lead = min(n, int(math.ceil(-t0 * fps / rate))) if rate > 0 else 0
            t0 = 0.0
        w, h = size
        scale = f"scale={w}:{h}:flags=area+{EXACT},format=rgb24"
        if rate > 0:
            vf, count = f"setpts=(PTS-STARTPTS)/{rate},fps={fps_arg(fps)},{scale}", n - self.lead
        else:                                               # rate 0: a freeze frame, one camera frame held
            vf, count = scale, 1
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", str(clip), "-an", "-vf", vf,
                                   "-frames:v", str(count), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE)
        self.nbytes = w * h * 3

    def next(self) -> np.ndarray:
        if self.lead:                                       # camera frame 0, read once and shown through the handle
            self.lead -= 1
            if self.last is None:
                self.last, self.held = self._read(), True
            return self.last
        if self.held:                                       # ... and at the first frame after it, not consumed twice
            self.held = False
            return self.last
        fr = self._read()
        if fr is not None:
            self.last = fr
        return self.last if self.last is not None else np.zeros((self.size[1], self.size[0], 3), np.uint8)

    def _read(self) -> np.ndarray | None:
        buf = self.p.stdout.read(self.nbytes)
        if len(buf) < self.nbytes:
            return None
        return np.frombuffer(buf, np.uint8).reshape(self.size[1], self.size[0], 3)

    def close(self) -> None:
        self.p.stdout.close()
        self.p.wait()


def still(path: Path) -> np.ndarray:
    """A still filled to 1080×1920 (centre crop)."""
    im = Image.open(path).convert("RGB")
    k = max(W / im.width, H / im.height)
    im = im.resize((max(W, round(im.width * k)), max(H, round(im.height * k))), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    return np.asarray(im.crop((x, y, x + W, y + H)))


def rgba_still(path: Path) -> np.ndarray:
    im = Image.open(path).convert("RGBA")
    if im.size != (W, H):
        print(f"  ! {path.name} is {im.size[0]}×{im.size[1]}, scaled to {W}×{H}")
        im = im.resize((W, H), Image.LANCZOS)
    return np.asarray(im, np.float32) / 255


class Overlay:
    """A V5 element: a PNG (still) or an alpha video, from its start time."""

    def __init__(self, item: dict, fps: float):
        self.path = Path(item["file"])
        self.f0, self.f1 = frames(item["start"], fps), frames(item["end"], fps)
        self.fps, self.p, self.img = fps, None, None
        self.is_still = self.path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")

    def at(self, f: int) -> np.ndarray | None:
        """The overlay at reel frame f (frames come in order): loaded on its first frame, released after its last."""
        if f >= self.f1:
            self.close()
        if not (self.f0 <= f < self.f1):
            return None
        if self.is_still:
            if self.img is None:
                self.img = rgba_still(self.path)
            return self.img
        if self.p is None:
            self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(self.path), "-an", "-vf",
                                       f"fps={fps_arg(self.fps)},scale={W}:{H}:flags=bicubic+{EXACT},format=rgba", "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                                      stdout=subprocess.PIPE)
        buf = self.p.stdout.read(W * H * 4)
        if len(buf) == W * H * 4:
            self.img = np.frombuffer(buf, np.uint8).reshape(H, W, 4).astype(np.float32) / 255
        return self.img                                      # past the video's end: its last frame

    def close(self) -> None:
        if self.p:
            self.p.kill()
            self.p.wait()
            self.p = None
        self.img = None


def over(base: np.ndarray, rgba: np.ndarray) -> np.ndarray:
    a = rgba[..., 3:4]
    return base * (1 - a) + rgba[..., :3] * 255 * a


def label_layer(text: str) -> np.ndarray:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, 26)
    x0, y0, x1, y1 = d.textbbox((24, 28), text, font=font)
    d.rectangle((x0 - 10, y0 - 8, x1 + 10, y1 + 8), fill=(0, 0, 0, 110))
    d.text((24, 28), text, fill=(200, 200, 200, 200), font=font)
    return np.asarray(im, np.float32) / 255


def guides_layer() -> np.ndarray:
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for box in ((0, 0, W, SAFE["top"]), (0, H - SAFE["bottom"], W, H), (W - SAFE["right"], SAFE["top"], W, H - SAFE["bottom"])):
        d.rectangle(box, fill=(255, 40, 40, 60))
    return np.asarray(im, np.float32) / 255


# ---------- checks ----------
def dissolves(edl: dict) -> list[int]:
    """Each shot's dissolve in frames; 0 on the first shot or after a gap (nothing to dissolve from)."""
    fps, shots = edl["fps"], edl["shots"]
    return [int(s.get("dissolve", 0)) if i and frames(s["start"], fps) == frames(shots[i - 1]["end"], fps) else 0
            for i, s in enumerate(shots)]


def check(edl: dict) -> tuple[list[str], list[str], dict]:
    """Errors (stop), warnings, and per-shot facts (camera size, fps, width shown)."""
    fps, errs, warns, facts = edl["fps"], [], [], {}
    for where, item, allowed in ([("EDL", edl, EDL_KEYS)] + [(f"overlay {o.get('file')}", o, OVERLAY_KEYS) for o in edl["overlays"]]
                                 + [(f"audio {t.get('file')}", t, AUDIO_KEYS) for t in edl["audio"]]):
        if set(item) - allowed:
            errs.append(f"{where}: unknown keys {sorted(set(item) - allowed)}")
    names = [s["name"] for s in edl["shots"]]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        errs.append(f"shot names must be unique: {', '.join(dupes)} (a clip used twice gets its own name, e.g. 05_C051b)")
    diss = dissolves(edl)
    prev_end, prev_name = 0, None
    for i, s in enumerate(edl["shots"]):
        n = s["name"]
        unknown = set(s) - SHOT_KEYS
        if unknown:
            errs.append(f"{n}: unknown keys {sorted(unknown)}")
        if s.get("ease", "ease") not in ("ease", "linear"):
            errs.append(f"{n}: ease must be \"ease\" or \"linear\"")
        if not isinstance(s.get("rotation", 0), (int, float)):
            errs.append(f"{n}: rotation must be a number (keys aren't supported)")
        if float(s.get("rate", 1.0)) < 0:
            errs.append(f"{n}: rate must be ≥ 0 (0 = a freeze frame; reverse a clip in Premiere)")
        if s.get("dissolve") and not diss[i]:
            warns.append(f"{n}: dissolve ignored ({'first shot' if i == 0 else 'it follows a gap'})")
        a, b = frames(s["start"], fps), frames(s["end"], fps)
        if b <= a:
            errs.append(f"{n}: ends before it starts")
        if a < prev_end:
            errs.append(f"{n}: starts at frame {a}, before {prev_name} ends (frame {prev_end}); use \"dissolve\" for overlap")
        elif a > prev_end:
            warns.append(f"{(a - prev_end) / fps:.2f} s of black before {n}")
        prev_end, prev_name = b, n
        if s.get("clip"):
            clip = Path(s["clip"])
            if not clip.exists():
                errs.append(f"{n}: no clip {clip}")
                continue
            info = probe(clip)
            rate = float(s.get("rate", 1.0))
            src_out = float(s.get("src_in", 0)) + (b - a) / fps * rate
            if src_out > info["duration"] + 1 / max(info["fps"], 1):
                errs.append(f"{n}: needs camera time up to {src_out:.2f} s, the clip ends at {info['duration']:.2f} s")
            fr = Framing(s, info["w"], info["h"])
            dur = (b - a) / fps
            width = fr.min_width_pct()
            gaps = [t for t in sorted(set(np.linspace(0, dur, 9).tolist() + fr.key_times())) if 0 <= t <= dur and not fr.covers(t)]
            if gaps:
                warns.append(f"{n}: the framing leaves black edges (at {gaps[0]:.2f} s into the shot)")
            if s.get("audio_db") is not None and abs(rate - 1) > 1e-6:
                warns.append(f"{n}: audio_db ignored on a retimed shot (rate {rate:g})")
            facts[n] = {"w": info["w"], "h": info["h"], "fps": info["fps"], "width_pct": width, "framing": fr}
        elif s.get("image") and not Path(s["image"]).exists():
            errs.append(f"{n}: no image {s['image']}")
    for o in edl["overlays"]:
        if not Path(o["file"]).exists():
            errs.append(f"overlay {o['file']} not found")
    for t in edl["audio"]:
        if not Path(t["file"]).exists():
            errs.append(f"audio {t['file']} not found")
    return errs, warns, facts


# ---------- audio ----------
def build_audio(edl: dict, total: float, wav: Path) -> None:
    fps, inputs, chains, labels = edl["fps"], [], [], []
    for s in edl["shots"]:
        if s.get("clip") and s.get("audio_db") is not None and abs(float(s.get("rate", 1)) - 1) < 1e-6 and has_audio(Path(s["clip"])):
            a, b = frames(s["start"], fps), frames(s["end"], fps)
            dur, ms = (b - a) / fps, int(round(a / fps * 1000))
            k = len(labels)
            inputs += ["-i", s["clip"]]
            chains.append(f"[{k}:a]atrim=start={float(s.get('src_in', 0)):.4f}:duration={dur:.4f},asetpts=PTS-STARTPTS,"
                          f"aformat=sample_rates=48000:channel_layouts=stereo,volume={float(s['audio_db'])}dB,"
                          f"afade=t=in:d=0.01,afade=t=out:st={max(dur - 0.01, 0):.4f}:d=0.01,adelay={ms}|{ms}[a{k}]")
            labels.append(f"[a{k}]")
    for t in edl["audio"]:
        k = len(labels)
        start, src = float(t.get("start", 0)), float(t.get("in", 0))
        dur = float(t.get("dur", total - start))
        ms = int(round(start * 1000))
        chain = (f"[{k}:a]atrim=start={src:.4f}:duration={dur:.4f},asetpts=PTS-STARTPTS,"
                 f"aformat=sample_rates=48000:channel_layouts=stereo,volume={float(t.get('gain_db', 0))}dB")
        if float(t.get("fade_in", 0)) > 0:
            chain += f",afade=t=in:d={float(t['fade_in'])}"
        if float(t.get("fade_out", 0)) > 0:
            chain += f",afade=t=out:st={max(dur - float(t['fade_out']), 0):.4f}:d={float(t['fade_out'])}"
        inputs += ["-i", t["file"]]
        chains.append(chain + f",adelay={ms}|{ms}[a{k}]")
        labels.append(f"[a{k}]")
    if not labels:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{total:.4f}",
                        "-c:a", "pcm_s16le", str(wav)], check=True)
        return
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,apad,atrim=duration={total:.4f},"
                  f"alimiter=limit=0.891:level=false[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[out]",
                    "-c:a", "pcm_s16le", "-ar", "48000", str(wav)], check=True)


# ---------- the render ----------
def relay(edl: dict, names: list[str]) -> dict:
    """--only: the named shots back to back from 0, without transitions, overlays or tracks."""
    by = {s["name"]: s for s in edl["shots"]}
    missing = [n for n in names if n not in by]
    if missing:
        sys.exit(f"--only: no shot named {', '.join(missing)} (names: {', '.join(by)})")
    t, shots = 0.0, []
    for n in names:
        s = dict(by[n])
        dur = (frames(s["end"], edl["fps"]) - frames(s["start"], edl["fps"])) / edl["fps"]
        s.update(start=round(t, 4), end=round(t + dur, 4))
        for k in ("dissolve", "fade_in", "fade_out"):
            s.pop(k, None)
        shots.append(s)
        t += dur
    return {**edl, "shots": shots, "overlays": [], "audio": [], "runtime": None}


def render(edl: dict, facts: dict, out: Path, label: str | None, guides: bool) -> None:
    fps, shots = edl["fps"], edl["shots"]
    total_f = frames(edl.get("runtime") or shots[-1]["end"], fps)
    total = total_f / fps
    span = [(frames(s["start"], fps), frames(s["end"], fps)) for s in shots]
    diss = dissolves(edl)
    need = []                                   # reel frames each shot must deliver, with dissolve handles
    for i, (a, b) in enumerate(span):
        pre = diss[i] // 2 if i else 0
        post = diss[i + 1] - diss[i + 1] // 2 if i + 1 < len(shots) else 0
        need.append((a - pre, b + post))

    overlays = [Overlay(o, fps) for o in edl["overlays"]]
    top = []
    if guides:
        top.append(guides_layer())
    if label:
        top.append(label_layer(label))
    stills = {i: still(Path(s["image"])) for i, s in enumerate(shots) if not s.get("clip") and s.get("image")}
    grades = [grade_fn(s.get("grade")) for s in shots]
    readers: dict[int, Reader] = {}
    sizes: dict[int, tuple] = {}

    tmp = tempfile.TemporaryDirectory(prefix="preview_edl_")
    wav = Path(tmp.name) / "mix.wav"
    build_audio(edl, total, wav)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", fps_arg(fps), "-i", "-", "-i", str(wav), "-map", "0:v", "-map", "1:a", *PICTURE,
                            "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-c:a", "aac", "-b:a", "256k",
                            "-t", f"{total:.4f}", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)

    def picture(i: int, f: int) -> np.ndarray:
        """Shot i's frame at reel frame f (its reader must be positioned at f)."""
        s = shots[i]
        if s.get("clip"):
            fact = facts[s["name"]]
            if i not in readers:
                fr = fact["framing"]
                k = prescale(fr)
                pw, ph = max(2, 2 * round(fact["w"] * k / 2)), max(2, 2 * round(fact["h"] * k / 2))
                rate = float(s.get("rate", 1.0))
                lo = max(need[i][0], 0)                       # the loop starts at reel frame 0
                t0 = float(s.get("src_in", 0)) + (lo - span[i][0]) / fps * rate
                readers[i] = Reader(Path(s["clip"]), t0, rate, fps, need[i][1] - lo, (pw, ph))
                sizes[i] = (pw / fact["w"], ph / fact["h"])
            src = readers[i].next()
            if grades[i]:
                src = grades[i](src)
            fx, fy = sizes[i]
            box = fact["framing"].crop(fx, fy, src.shape[1], src.shape[0])
            if box:
                arr = src[box[1]:box[1] + H, box[0]:box[0] + W].astype(np.float32)
            else:
                img = Image.fromarray(src).transform((W, H), Image.AFFINE, fact["framing"].affine((f - span[i][0]) / fps, fx, fy),
                                                     resample=Image.BICUBIC, fillcolor=(0, 0, 0))
                arr = np.asarray(img, np.float32)
        elif i in stills:
            arr = stills[i].astype(np.float32)
        else:
            arr = np.zeros((H, W, 3), np.float32)
        a, b = span[i]
        fin, fout = int(s.get("fade_in", 0)), int(s.get("fade_out", 0))
        if fin and a <= f < a + fin:
            arr = arr * ((f - a + 0.5) / fin)
        if fout and b - fout <= f < b:
            arr = arr * ((b - f - 0.5) / fout)
        return arr

    t_start = time.time()
    for f in range(total_f):
        active = [i for i, (a, b) in enumerate(need) if a <= f < b]
        frames_now = {i: picture(i, f) for i in active}       # every active reader advances one frame
        cur = [i for i in active if span[i][0] <= f < span[i][1]]
        img = frames_now[cur[0]] if cur else np.zeros((H, W, 3), np.float32)
        for i in active:                                      # dissolves: shot i fading in over shot i-1
            if i == 0 or not diss[i] or (i - 1) not in frames_now:
                continue
            c0 = span[i][0] - diss[i] // 2
            if c0 <= f < c0 + diss[i]:
                w = (f - c0 + 0.5) / diss[i]
                img = frames_now[i - 1] * (1 - w) + frames_now[i] * w
        for o in overlays:
            rgba = o.at(f)
            if rgba is not None:
                img = over(img, rgba)
        for layer in top:
            img = over(img, layer)
        enc.stdin.write(np.clip(img + 0.5, 0, 255).astype(np.uint8).tobytes())
        for i in [i for i in readers if need[i][1] <= f + 1]:
            readers.pop(i).close()
        if f and f % (int(fps) * 5) == 0:
            print(f"  {f / fps:5.1f} / {total:.1f} s", flush=True)
    enc.stdin.close()
    enc.wait()
    for r in readers.values():
        r.close()
    for o in overlays:
        o.close()
    tmp.cleanup()
    if enc.returncode:
        sys.exit("✗ the encoder failed")
    print(f"✓ {out}  ({total:.2f} s, {total_f} frames, rendered in {time.time() - t_start:.0f} s)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("edl", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--fps", type=float, help="for a plain shot map without \"fps\"")
    ap.add_argument("--only", help="comma-separated shot names: render just these, back to back")
    ap.add_argument("--guides", action="store_true", help="draw the Instagram UI bands (top 220, bottom 320, right 120 px)")
    ap.add_argument("--clean", action="store_true", help="no \"offline preview\" label")
    a = ap.parse_args()

    edl = load_edl(a.edl, a.fps)
    if a.only:
        edl = relay(edl, [n.strip() for n in a.only.split(",") if n.strip()])
    errs, warns, facts = check(edl)
    for s in edl["shots"]:
        n = s["name"]
        if n in facts:
            fa = facts[n]
            rate = float(s.get("rate", 1.0))
            flag = "" if fa["width_pct"] >= 80 else ("  < 80 % (name it in the brief)" if fa["width_pct"] >= 70 else "  < 70 %")
            print(f"  {n:14s} {s['start']:6.2f}–{s['end']:6.2f}  width {fa['width_pct']:3.0f} %{flag}"
                  + (f"  rate {rate:g}" if abs(rate - 1) > 1e-6 else "") + f"  ({fa['fps']:g} fps camera)")
        else:
            print(f"  {n:14s} {s['start']:6.2f}–{s['end']:6.2f}  {'still' if s.get('image') else 'black'}")
    for w in warns:
        print(f"  ! {w}")
    if errs:
        for e in errs:
            print(f"  ✗ {e}")
        sys.exit(1)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    if a.only:
        side = a.out.with_name(a.out.stem + "_edl.json")
        side.write_text(json.dumps({k: v for k, v in edl.items()}, indent=1))
        print(f"  re-timed EDL → {side}")
    label = None if a.clean else f"offline preview · colour approximate · {a.edl.stem}"
    render(edl, facts, a.out, label, a.guides)


if __name__ == "__main__":
    main()
