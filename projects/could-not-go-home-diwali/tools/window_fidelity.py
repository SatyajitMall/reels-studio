"""Camera check inside the 4:3 window (reel-local stand-in for camera_fidelity.py, which can't see windows or the
−90 rotation yet: CR-20261104-kolkata-landscape-footage-9x16 item 6, accepted for v0.11).

For each EDL shot it samples the render at the shot's middle, crops the window (y 505–1315), and rebuilds the same
framing from (a) the camera file and (b) the depth-baked file, using the EDL's Scale/Position/Rotation. Reports luma,
saturation, p02/p98, crush/clip and NCC for render vs camera and render vs baked, and writes a camera | baked | render
sheet. Thresholds follow effects-playbook §A0: luma ≥ camera − 0.02 (and ≤ +0.06), sat ×0.95–1.05, crush ≤ camera + 1 %.
The baked file carries the depth blur, so NCC vs camera is lower by design; NCC vs baked checks the framing (≥ 0.6).

Usage (studio root): .venv/bin/python -I projects/could-not-go-home-diwali/tools/window_fidelity.py <render> \
    --edl projects/could-not-go-home-diwali/analysis/edl_v1.json -o projects/could-not-go-home-diwali/analysis/winfid_p1
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

STUDIO = Path(__file__).resolve().parents[3]
WIN = (0, 505, 1080, 1315)
LUMA = np.array([0.2126, 0.7152, 0.0722])


def frame(path, t, upright=False):
    vf = "transpose=2" if upright else "null"
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", str(path), "-frames:v", "1", "-vf", vf,
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                            "-show_entries", "stream_side_data=rotation", "-of", "json", str(path)], capture_output=True, text=True)
    st = json.loads(probe.stdout)["streams"][0]
    w, h = st["width"], st["height"]
    rot = 0
    for sd in st.get("side_data_list", []):
        rot = int(sd.get("rotation", 0))
    dw, dh = (h, w) if abs(rot) == 90 else (w, h)          # ffmpeg autorotates by the tag
    if upright:
        dw, dh = dh, dw
    raw = subprocess.run(cmd, capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(dh, dw, 3)


def keyed(v, t):
    if isinstance(v, list) and v and isinstance(v[0], list):
        ks = sorted(v)
        if t <= ks[0][0]:
            return ks[0][1:]
        for a, b in zip(ks, ks[1:]):
            if t <= b[0]:
                u = (t - a[0]) / (b[0] - a[0]); u = u * u * (3 - 2 * u)
                return [x + (y - x) * u for x, y in zip(a[1:], b[1:])]
        return ks[-1][1:]
    return v if isinstance(v, list) else [v]


def framed(img, scale, pos):
    """The window as Premiere shows it: image (upright, W×H) scaled by scale % and centred at pos (sequence px)."""
    s = scale / 100.0
    ih, iw = img.shape[:2]
    x0 = (WIN[0] - pos[0]) / s + iw / 2; x1 = (WIN[2] - pos[0]) / s + iw / 2
    y0 = (WIN[1] - pos[1]) / s + ih / 2; y1 = (WIN[3] - pos[1]) / s + ih / 2
    crop = Image.fromarray(img).crop((int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))))
    return np.asarray(crop.resize((WIN[2] - WIN[0], WIN[3] - WIN[1]), Image.LANCZOS))


def stats(a):
    f = a.astype(np.float64) / 255
    l = f @ LUMA
    mx, mn = f.max(2), f.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return {"luma": float(l.mean()), "sat": float(sat.mean()), "p02": float(np.percentile(l, 2)), "p98": float(np.percentile(l, 98)),
            "crush": float((l < 0.02).mean() * 100), "clip": float((f.max(2) >= 0.999).mean() * 100)}


def ncc(a, b):
    x = (a.astype(np.float64) @ LUMA).ravel(); y = (b.astype(np.float64) @ LUMA).ravel()
    x -= x.mean(); y -= y.mean()
    return float((x * y).sum() / (np.sqrt((x * x).sum() * (y * y).sum()) + 1e-9))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("render"); ap.add_argument("--edl", required=True); ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--map", help="bake_map.json (default: next to the EDL)")
    a = ap.parse_args()
    edl = json.loads(Path(a.edl).read_text())
    bmap = json.loads(Path(a.map or Path(a.edl).with_name("bake_map.json")).read_text())
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    rows, tiles = [], []
    for s in edl["shots"]:
        if "clip" not in s:
            continue
        tm = (s["start"] + s["end"]) / 2
        r = frame(a.render, tm)[WIN[1]:WIN[3], WIN[0]:WIN[2]]
        lt = tm - s["start"]
        src_t = s["src_in"] + lt * s.get("rate", 1)
        sc = keyed(s.get("scale", 37.5), lt)[0]
        pos = keyed(s.get("pos", [540, 910]), lt)
        stem = Path(s["clip"]).stem
        if stem in bmap:                       # v1b/v1c: the clip is a pre-render; map back to the camera by the shot name
            b = bmap[stem]
            cam_t = b.get("cam_in", b["start"]) + lt * b.get("rate", 1)
        else:                                  # v1: the clip is the baked file itself
            b = bmap[stem.split("_")[0]]
            cam_t = b["start"] + src_t
        clip_img = frame(STUDIO / s["clip"], src_t, upright=True)
        cam_img = frame(STUDIO / b["camera"], cam_t, upright=True)
        bk = framed(clip_img, sc, pos)
        cam = framed(cam_img, sc * clip_img.shape[1] / cam_img.shape[1], pos)
        R, C, B = stats(r), stats(cam), stats(bk)
        n_c, n_b = ncc(r, cam), ncc(r, bk)
        f = []
        if R["luma"] < C["luma"] - 0.02: f.append(f"luma FAIL {R['luma']:.3f} < camera {C['luma']:.3f} − 0.02")
        elif R["luma"] > C["luma"] + 0.06: f.append(f"luma WARN {R['luma']:.3f} > camera + 0.06")
        rs = R["sat"] / max(C["sat"], 1e-6)
        if not 0.95 <= rs <= 1.05: f.append(f"sat {'FAIL' if not 0.9 <= rs <= 1.1 else 'WARN'} ×{rs:.2f}")
        if R["crush"] > C["crush"] + 1: f.append(f"crush FAIL {R['crush']:.1f} % vs camera {C['crush']:.1f} %")
        if R["clip"] > max(C["clip"] * 1.5, C["clip"] + 0.5): f.append(f"clip WARN {R['clip']:.1f} % vs {C['clip']:.1f} %")
        if n_b < 0.6: f.append(f"framing FAIL: NCC vs baked {n_b:.2f}")
        verdict = "FAIL" if any("FAIL" in x for x in f) else ("WARN" if f else "PASS")
        rows.append((s["name"], verdict, C, B, R, n_c, n_b, f))
        tiles.append((s["name"], cam, bk, r))
        print(f"{s['name']:24s} {verdict:4s} luma cam {C['luma']:.3f} baked {B['luma']:.3f} render {R['luma']:.3f} · sat ×{rs:.2f} · NCC cam {n_c:.2f} baked {n_b:.2f} {'; '.join(f)}")
    md = ["# Window fidelity (4:3 window, y 505–1315)", "",
          "| Shot | Verdict | Luma cam → baked → render | Sat cam → render | Crush % cam → render | Clip % cam → render | NCC vs cam / baked | Findings |",
          "|---|---|---|---|---|---|---|---|"]
    for n, v, C, B, R, nc, nb, f in rows:
        md.append(f"| {n} | {v} | {C['luma']:.3f} → {B['luma']:.3f} → {R['luma']:.3f} | {C['sat']:.3f} → {R['sat']:.3f} | {C['crush']:.1f} → {R['crush']:.1f} | "
                  f"{C['clip']:.2f} → {R['clip']:.2f} | {nc:.2f} / {nb:.2f} | {'; '.join(f) or '—'} |")
    verdict = "FAIL" if any(v == "FAIL" for _, v, *_ in rows) else "PASS"
    md.insert(1, f"**Verdict: {verdict}** · {len(rows)} shots. Sheet: `winfid_sheet.jpg` (camera | baked (depth) | render).")
    (out / "WINFID.md").write_text("\n".join(md) + "\n")
    tw = 360; th = int(810 * tw / 1080)
    S = Image.new("RGB", (3 * (tw + 6) + 6, len(tiles) * (th + 28) + 6), (20, 20, 20)); d = ImageDraw.Draw(S)
    fnt = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 18, index=1)
    for i, (n, c, b, r) in enumerate(tiles):
        y = 6 + i * (th + 28)
        d.text((6, y + 2), f"{n}: camera | baked | render", font=fnt, fill=(255, 210, 120))
        for j, im in enumerate((c, b, r)):
            S.paste(Image.fromarray(im).resize((tw, th)), (6 + j * (tw + 6), y + 24))
    S.save(out / "winfid_sheet.jpg", quality=85)
    print(f"{verdict} · {out / 'WINFID.md'}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
