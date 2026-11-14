"""Build EDL v2b for could-not-go-home-diwali (reel-local): v2 + the director's note "shots look a little too unrelated".

The v2 stock inserts came from other places, light and camera heights, so they read as random cutaways. v2b takes the
no-face shots from the same workers: 1:1 macro crops of their own hands from our 4K clips (same place, same light),
paired with their wide or face shot. One stock clip stays: S1, a mother's hands making roti, because L3 literally says
"your hands", cut hands-to-hands into our cook's hands. 7 of 12 shots show no face.

Two renders from one cut, as v2: camera-true (edl_v2b.json) and the reference look (edl_v2b_look.json, ref_match.cube).
Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v2b.py [--mix 0.6] [--only NAME,…]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[3]
REEL = Path(__file__).resolve().parents[1]
R = "projects/could-not-go-home-diwali"
sys.path.insert(0, str(REEL / "tools"))
import build_edl_v1 as v1  # noqa: E402
import build_edl_v2 as v2  # noqa: E402  (lut_clip, probe_wh, top_anchor)

FPS = 25
PUSH = 1.05
LINE_OF = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
WIN_C = (540, 910)

# ("reuse", edl file, shot name) | ("macro", cid, cam_in, (u, v) hands centre in the upright frame, scale in 4K terms) |
# ("stock", path, src_in, native fps)
SHOTS = [
    ("01_C047_auto", ("reuse", "edl_v1c.json", "01_C047_auto"), "auto driver from the back seat, the lit street drifting past (70 %)"),
    ("02_C048_auto_turn", ("reuse", "edl_v1c.json", "02_C048_auto_turn"), "the driver turns his head toward the lit street (real time)"),
    ("03_C054_parotta", ("reuse", "edl_v2.json", "03_C054_parotta"), "parotta maker lifting a parotta off the tawa (real time)"),
    ("04_C054_hands", ("macro", "C054", 4.00, (0.56, 0.78), 90.0), "macro: his hands at the tawa, turning parotta"),
    ("05_S1_maa_roti", ("stock", "raw/stock/pexels-38001819/16127033_1920_1080_50fps.mp4", 2.4, 50),
     "stock S1: a mother's hands shaping roti at night (50 fps → 50 % slow motion), the one image from home"),
    ("06_C052_hands", ("macro", "C052", 1.20, (0.52, 0.80), 90.0), "macro: the young cook's hands plating food for strangers (hands to hands)"),
    ("07_C062_vendor", ("reuse", "edl_v1c.json", "07_C062_vendor"), "jewellery vendor at his stall, looking into his phone"),
    ("08_C062_phone", ("macro", "C062", 4.92, (0.34, 0.76), 90.0), "macro: the phone in his hand"),
    ("09_C050_hands", ("macro", "C050", 0.40, (0.39, 0.75), 90.0), "macro: the paan maker's hands at work"),
    ("10_C051_paan_look", ("reuse", "edl_v1c.json", "10_C051_paan_look"), "he looks away, still, lost in thought (70 %)"),
    ("11_C064_hands", ("macro", "C064", 0.80, (0.55, 0.80), 90.0), "macro: the car-washer's soapy hands wringing the cloth"),
    ("12_C064_carwash_look", ("reuse", "edl_v1c.json", "12_C064_carwash_look"), "he looks up from the work toward the camera (80 %)"),
]


def macro_framing(u, v, sc, dur):
    """Scale/Position (4K terms, after Rotation −90 → 3840×2160 upright) that put (u, v) at the window centre, clamped so
    the image always covers the 4:3 window; a +5 % push on the same point."""
    def pos_for(s):
        w, h = 3840 * s / 100, 2160 * s / 100
        x = WIN_C[0] - (u - 0.5) * w
        y = WIN_C[1] - (v - 0.5) * h
        x = min(max(x, 1080 - w / 2), w / 2)
        y = min(max(y, 1315 - h / 2), 505 + h / 2)
        return round(x, 1), round(y, 1)
    s1 = round(sc * PUSH, 2)
    (x0, y0), (x1, y1) = pos_for(sc), pos_for(s1)
    return [[0, sc], [dur, s1]], [[0, x0, y0], [dur, x1, y1]]


def build_macro(name, cid, cin, dur, todo, stab="smooth"):
    cam = sorted((REEL / "raw" / "Media").glob(f"*_{cid}.mov"))[0]
    bstart = max(0.0, round((cin - 0.72) * FPS) / FPS)
    bdur = round((cin - bstart + dur + 1.0) * FPS) / FPS
    baked = REEL / "raw" / "baked" / "v2b" / f"{name}.mov"; baked.parent.mkdir(parents=True, exist_ok=True)
    out = REEL / "renders" / "fx_preview_v2b" / f"{name}.mov"; out.parent.mkdir(parents=True, exist_ok=True)
    if todo:
        r = subprocess.run([str(REEL / "tools" / "cine_bake"), str(cam), str(baked), "--start", f"{bstart:.2f}", "--dur", f"{bdur:.2f}",
                            "--fnumber", "4"], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"bake {name}: {r.stderr or r.stdout}")
        job = [{"id": name, "clip": str(baked.relative_to(STUDIO)), "src_in": round(cin - bstart, 3), "out_dur": dur, "stab": stab,
                "sigma": 15, "zoom": 1.04, "transl_only": True, "rate": 1.0, "half": False, "out": str(out.relative_to(STUDIO))}]
        jf = REEL / "analysis" / "fx_jobs_v2b.json"; jf.write_text(json.dumps(job, indent=1))
        subprocess.run([sys.executable, "-I", str(REEL / "tools" / "fx_prerender.py"), "--jobs", str(jf)], cwd=STUDIO, check=True)
    return str(out.relative_to(STUDIO)), cam.name, bstart


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mix", type=float, default=0.6); ap.add_argument("--only")
    a = ap.parse_args()
    shots, look_shots = [], []
    look_dir = REEL / "renders" / "look_v2b"; look_dir.mkdir(parents=True, exist_ok=True)
    cache = {}
    for i, (name, src, shows) in enumerate(SHOTS):
        st, en = v1.CUTS[i], v1.CUTS[i + 1]
        dur = round(en - st, 2)
        line = v1.LINES[LINE_OF[i]][0]
        todo = not a.only or name in a.only.split(",")
        if src[0] == "reuse":
            ed = cache.setdefault(src[1], {s["name"]: s for s in json.loads((REEL / "analysis" / src[1]).read_text())["shots"]})
            s0 = dict(ed[src[2]])
            shot = {k: s0[k] for k in ("clip", "src_in", "rate", "rotation", "scale", "pos", "ease", "note", "grade") if k in s0}
            shot.update(name=name, start=st, end=en, line=line, shows=shows)
        elif src[0] == "macro":
            _, cid, cin, (u, v), sc = src
            clip, camname, bstart = build_macro(name, cid, cin, dur, todo)
            scale, pos = macro_framing(u, v, sc, dur)
            shot = {"name": name, "start": st, "end": en, "clip": clip, "src_in": 0.0, "rate": 1, "rotation": -90, "scale": scale,
                    "pos": pos, "ease": "ease", "line": line, "shows": shows,
                    "note": (f"build: camera {camname} in {cin:.2f} s, real time; MACRO 1:1 crop of the 4K frame (Scale {sc:g}, "
                             f"{1080 / (3840 * sc / 100):.0%} of the width), centred on the hands at ({u}, {v}); stabilise position-only "
                             f"(Warp); depth f/4 recorded focus (bake start {bstart:.2f}); push +5 %; preview = full-size pre-render")}
        else:
            _, path, sin, nfps = src
            w, h = v2.probe_wh(f"{R}/{path}")
            sc0 = 100.0 * 810 / h
            scale, pos = v2.top_anchor(sc0, h, dur)
            shot = {"name": name, "start": st, "end": en, "clip": f"{R}/{path}", "src_in": sin, "rate": round(FPS / nfps, 5),
                    "scale": scale, "pos": pos, "ease": "ease", "line": line, "shows": shows, "grade": {"exposure": 1.0, "sat": 1.0},
                    "note": f"STOCK (Pexels, raw/SOURCES.md): {int(round(100 * FPS / nfps))} % (native {nfps} fps interpreted at 25); "
                            "primary exposure +1.0 stop (underexposed stock); push +5 %"}
        shots.append(shot)
        lshot = dict(shot)
        lout = look_dir / f"{name}.mov"
        if todo or not lout.exists():
            off = v2.lut_clip(shot["clip"], shot["src_in"], shot["rate"], dur, lout, a.mix, True)
        else:
            off = shot["src_in"] - max(0.0, shot["src_in"] - 0.1)
        lshot["clip"] = str(lout.relative_to(STUDIO)); lshot["src_in"] = round(off, 3)
        look_shots.append(lshot)
        print(f"{name:22s} {st:5.2f}–{en:5.2f} {line[:34]}")
    end = {"name": "13_end_card", "start": v1.CUTS[-1], "end": v1.RUNTIME, "line": "— tumhara beta (title on black)",
           "shows": "title 'Mera diya bhi jalaana', sign-off, handle"}
    prev = json.loads((REEL / "analysis" / "edl_v1.json").read_text())
    base = ("v2b = v2 + director note 'shots look a little too unrelated': the no-face shots are now 1:1 macro crops of the same "
            "workers' hands from our 4K clips (same place, same light); one stock clip stays (S1 Maa's hands, L3, cut hands to "
            "hands). 7 of 12 shots without a face. Cuts, letter, window, type unchanged.")
    for fn, sh, extra in (("edl_v2b.json", shots, " Camera-true."),
                          ("edl_v2b_look.json", look_shots, f" LOOK PREVIEW: ref_match.cube at {a.mix:.0%}.")):
        (REEL / "analysis" / fn).write_text(json.dumps({"fps": FPS, "runtime": v1.RUNTIME, "note": base + extra, "shots": sh + [end],
                                                        "overlays": prev["overlays"], "audio": prev["audio"]}, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v2b.json and analysis/edl_v2b_look.json")


if __name__ == "__main__":
    main()
