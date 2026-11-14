"""Build EDL v2c for could-not-go-home-diwali (reel-local): v2b + the director's note
"the micro and macro shots are somehow unrelated to the topic" → their pick "Their fest + Kolkata".

Inserts now carry the topic (missing home on Diwali) and come from the same night / the director's own home footage:
  L1 auto → C043 Kolkata at night (Victoria Memorial, 1 Nov, the director's home; lifted +2.3 stops)
  L2 parotta → C058 the Diwali stage show at the same fest (GPS: ~80 m from the stalls, 20:02): they celebrate, he works
  L3 S1 Maa's hands (stock) → the cook plating (wide; the hands macro read as off-topic)
  L4 vendor on his phone → N14 a couple in Diwali clothes waving into a phone (stock, Pexels 8811028): the call home
  L5 paan maker → his far-off look
  L6 C043 Kolkata again (deliberate callback: the promised home) → the car-washer looks up
Two renders again: camera-true (edl_v2c.json) and the reference look (edl_v2c_look.json).
Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v2c.py [--mix 0.6] [--only NAME,…]
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
import build_edl_v2 as v2  # noqa: E402

FPS = 25
LINE_OF = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
C043 = "raw/Media/A001_11011800_C043.mov"
CURVE = "0/0.01 0.02/0.14 0.06/0.40 0.15/0.66 0.4/0.90 1/1"

SHOTS = [
    ("01_C047_auto", ("reuse", "edl_v1c.json", "01_C047_auto"), "auto driver from the back seat, the lit street drifting past (70 %)"),
    ("02_C043_kolkata", ("camera", C043, 4.0, 0, 1.10), "home: Kolkata at night, Victoria Memorial's lit dome (the director's own clip, 1 Nov)"),
    ("03_C054_parotta", ("reuse", "edl_v2.json", "03_C054_parotta"), "parotta maker lifting a parotta off the tawa (real time)"),
    ("04_C058_diwali_show", ("new", "C058", 0.60, 1.0, "smooth", 2.0), "the Diwali stage show at the same fest: the crowd celebrates while he works"),
    ("05_S1_maa_roti", ("reuse", "edl_v2b.json", "05_S1_maa_roti"), "stock S1: a mother's hands shaping roti at night (50 %), the food from home"),
    ("06_C052_cook", ("reuse", "edl_v1c.json", "05_C052_cook_plating"), "the young cook plating food for strangers (real time)"),
    ("07_C062_vendor", ("reuse", "edl_v1c.json", "07_C062_vendor"), "jewellery vendor at his stall, looking into his phone"),
    ("08_N14_call_home", ("stock_vert", "raw/stock/pexels-8811028/8811028-hd_1080_1920_25fps.mp4", 2.8, 0.31),
     "stock N14: a couple in Diwali clothes waving and doing namaste into a phone: the call home"),
    ("09_C050_paan", ("reuse", "edl_v1c.json", "09_C050_paan"), "paan maker in white wrapping paan (real time)"),
    ("10_C051_paan_look", ("reuse", "edl_v1c.json", "10_C051_paan_look"), "he looks away, still, lost in thought (70 %)"),
    ("11_C043_kolkata_again", ("camera", C043, 11.0, 0, 1.12), "home again, a deliberate callback: Kolkata's lit dome, the promised next year"),
    ("12_C064_carwash_look", ("reuse", "edl_v1c.json", "12_C064_carwash_look"), "the car-washer looks up from the work toward the camera (80 %)"),
]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mix", type=float, default=0.6); ap.add_argument("--only")
    a = ap.parse_args()
    shots, look_shots, cache = [], [], {}
    look_dir = REEL / "renders" / "look_v2c"; look_dir.mkdir(parents=True, exist_ok=True)
    for i, (name, src, shows) in enumerate(SHOTS):
        st, en = v1.CUTS[i], v1.CUTS[i + 1]
        dur = round(en - st, 2)
        line = v1.LINES[LINE_OF[i]][0]
        todo = not a.only or name in a.only.split(",")
        kind = src[0]
        if kind == "reuse":
            ed = cache.setdefault(src[1], {s["name"]: s for s in json.loads((REEL / "analysis" / src[1]).read_text())["shots"]})
            s0 = ed[src[2]]
            shot = {k: s0[k] for k in ("clip", "src_in", "rate", "rotation", "scale", "pos", "ease", "note", "grade") if k in s0}
            shot.update(name=name, start=st, end=en, line=line, shows=shows)
        elif kind == "camera":                     # C043: near-black, not Cinematic. Lift by a curve (a plain gain left it dark
            _, path, sin, _stops, push = src       # in the preview's linear exposure, or blew the dome), light temporal denoise
            out = REEL / "renders" / "fx_preview_v2c" / f"{name}.mov"; out.parent.mkdir(parents=True, exist_ok=True)
            if todo or not out.exists():
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sin:.2f}", "-t", f"{dur + 0.2:.2f}", "-i", str(REEL / path),
                                "-vf", f"curves=all='{CURVE}',hqdn3d=2:1.5:6:4", "-an", "-c:v", "prores_ks", "-profile:v", "2",
                                "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                                str(out)], check=True)
            scale, pos = v2.top_anchor(37.5, 2160, dur, push)
            shot = {"name": name, "start": st, "end": en, "clip": str(out.relative_to(STUDIO)), "src_in": 0.0, "rate": 1, "rotation": -90,
                    "scale": scale, "pos": pos, "ease": "linear", "line": line, "shows": shows,
                    "note": f"build: camera {Path(path).name} in {sin:.2f} s, real time; linear push (an eased start read as a freeze); primary = RGB curve {CURVE} (shot near-black, "
                            f"luma 0.01) + light denoise (AE denoise in the build); push +{round((push - 1) * 100)} %; preview = curve pre-render"}
        elif kind == "new":
            _, cid, cin, rate, stab, fno = src
            if todo:
                clip, camname, bstart = v2.build_new(name, cid, cin, rate, stab, fno, dur)
            else:
                clip = f"{R}/renders/fx_preview_v2/{name}.mov"; camname = cid; bstart = max(0.0, round((cin - 0.72) * FPS) / FPS)
            scale, pos = v2.top_anchor(75.0, 1080, dur)
            shot = {"name": name, "start": st, "end": en, "clip": clip, "src_in": 0.0, "rate": 1, "rotation": -90, "scale": scale,
                    "pos": pos, "ease": "ease", "line": line, "shows": shows,
                    "note": (f"build: camera {camname} in {cin:.2f} s, real time, stabilise position-only (Warp), depth f/{fno:g} recorded "
                             f"focus (bake start {bstart:.2f}); push +5 % top-anchored; preview = half-size pre-render (Scale ×2)")}
        else:                                      # vertical stock: the window shows a 1080×810 band, centred at v
            _, path, sin, v = src
            sc0 = 100.0
            y = round(910 - (v - 0.5) * 1920, 1)
            shot = {"name": name, "start": st, "end": en, "clip": f"{R}/{path}", "src_in": sin, "rate": 1,
                    "scale": [[0, sc0], [dur, 105.0]], "pos": [[0, 540, y], [dur, 540, round(910 - (v - 0.5) * 1920 * 1.05, 1)]],
                    "ease": "ease", "line": line, "shows": shows,
                    "note": "STOCK (Pexels 8811028, Yan Krukau; raw/SOURCES.md): real time 25 fps; window on the upper band (faces + phone); push +5 %"}
        shots.append(shot)
        lshot = dict(shot)
        lout = look_dir / f"{name}.mov"
        if todo or not lout.exists():
            off = v2.lut_clip(shot["clip"], shot["src_in"], shot["rate"], dur, lout, a.mix, True)
        else:
            off = shot["src_in"] - max(0.0, shot["src_in"] - 0.1)
        lshot["clip"] = str(lout.relative_to(STUDIO)); lshot["src_in"] = round(off, 3)
        look_shots.append(lshot)
        print(f"{name:24s} {st:5.2f}–{en:5.2f} {line[:34]}")
    end = {"name": "13_end_card", "start": v1.CUTS[-1], "end": v1.RUNTIME, "line": "— tumhara beta (title on black)",
           "shows": "title 'Mera diya bhi jalaana', sign-off, handle"}
    prev = json.loads((REEL / "analysis" / "edl_v1.json").read_text())
    base = ("v2c = v2b + director note 'the micro and macro shots are somehow unrelated to the topic' → 'Their fest + Kolkata': inserts "
            "carry the topic: Kolkata at night (home, own C043) at L1 and L6, the Diwali show at the same fest (C058) at L2, Maa's "
            "hands (S1) at L3, a couple on a Diwali video call (N14) at L4. Cuts, letter, window, type unchanged.")
    for fn, sh, extra in (("edl_v2c.json", shots, " Camera-true."), ("edl_v2c_look.json", look_shots, f" LOOK PREVIEW: ref_match.cube at {a.mix:.0%}.")):
        (REEL / "analysis" / fn).write_text(json.dumps({"fps": FPS, "runtime": v1.RUNTIME, "note": base + extra, "shots": sh + [end],
                                                        "overlays": prev["overlays"], "audio": prev["audio"]}, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v2c.json and analysis/edl_v2c_look.json")


if __name__ == "__main__":
    main()
