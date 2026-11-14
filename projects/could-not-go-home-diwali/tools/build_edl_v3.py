"""Build EDL v3 for could-not-go-home-diwali (reel-local), after the director's notes on v2d:
  - "the shot where a random couple is there, change"                        → N14 out
  - "where fire cracker is being burnt is too elegant"                        → F9 out
  - "man in the jewellery stall, the video glitches there"                    → the vendor shots are the plain depth bake (no preview
                                                                                stabiliser: it lost track for one frame at 9.96 s and snapped 43 px)
  - "look at the reference videos, the video there has some slow down / cinematic effect"
        → measured: the reference's "slow down" is a STEP-PRINT stutter (each image held 3 frames ≈ 8 images/s, shutter smear) on
          the crowd passing a still seller and on a panning rickshaw → scripts/step_print.py (--step 8) on 01 (auto, a bus streaking
          past the still driver) and 12 (the Diwali show at the same fest)
  - "I need more of my footage to be used; extend the reel timing" + answers: extend, audio later (guide looped as placeholder);
    keep only stock S1 (Maa's hands) and F8 (marigold hands)
Result: 30.76 s, 6 letter lines × 3 bars on audio/guide_loop_v3.wav (152 BPM, seamless loop: bars 1–11 + bars 5–11 + tail), 18 shots,
16 from the director's footage. Two renders: camera-true (edl_v3.json) and the reference look (edl_v3_look.json).
Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v3.py [--mix 0.6] [--only NAME,…]
"""
import argparse
import json
import sys
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[3]
REEL = Path(__file__).resolve().parents[1]
R = "projects/could-not-go-home-diwali"
sys.path.insert(0, str(REEL / "tools"))
import build_edl_v1 as v1   # noqa: E402  (letter lines, overlay files)
import build_edl_v2 as v2   # noqa: E402  (build_new, lut_clip, top_anchor)
import build_edl_v2b as v2b  # noqa: E402  (build_macro, macro_framing)

FPS = 25
CUTS = [0.0, 1.56, 3.12, 4.68, 6.24, 7.84, 9.44, 11.04, 12.64, 14.24, 15.80, 17.40, 19.00, 20.60, 22.20, 23.80, 25.40, 26.96, 28.56]
RUNTIME = 30.76
LINE_OF = [i // 3 for i in range(18)]
F8 = "raw/stock/pexels-8811075/8811075-hd_1920_1080_25fps.mp4"
S1 = "raw/stock/pexels-38001819/16127033_1920_1080_50fps.mp4"

# (name, source, shows)
#   ("new", cid, cam_in, rate, stab, fnumber)          bake + half-size pre-render (v2.build_new)
#   ("macro", cid, cam_in, (u, v), scale)              bake + full-size pre-render, 1:1 crop on the hands (v2b)
#   ("full", path, src_in, (scale, x, y) | None)       a full-size file used directly (step-print render or the plain bake)
#   ("stock", path, src_in, native fps, exposure)      landscape stock, 4:3 middle, top-anchored push
SHOTS = [
    ("01_C049_auto_step", ("full", "renders/fx_v3/C049_step.mov", 0.0, None), "STEP-PRINT: the auto driver sits still while the bus and street streak past in steps"),
    ("02_C048_auto_turn", ("new", "C048", 2.72, 1.0, None, 2.0), "the driver turns his head toward the lit street (real time)"),
    ("03_F8_marigold", ("stock", F8, 4.0, 25, 0.0), "stock F8: hands laying marigold flowers"),
    ("04_C054_parotta", ("new", "C054", 0.80, 1.0, None, 2.8), "parotta maker lifting a parotta off the tawa (real time)"),
    ("05_C054_hands", ("macro", "C054", 2.30, (0.52, 0.76), 90.0), "cut-in: the parotta held up on his spatula, his hands at the tawa (calmest stretch of the clip)"),
    ("06_C056_juice", ("new", "C056", 0.20, 1.0, None, 2.0), "the juice-stall man in the festival light, working the counter"),
    ("07_S1_maa_roti", ("stock", S1, 2.4, 50, 1.0), "stock S1: a mother's hands shaping roti at night (50 %)"),
    ("08_C052_cook", ("new", "C052", 1.00, 1.0, None, 2.8), "the young cook plating food for strangers (real time)"),
    ("09_C053_serve", ("new", "C053", 1.55, 1.0, None, 2.8), "he hands the plate across to a customer (real time)"),
    ("10_C062_vendor", ("full", "raw/baked/v1c/07_C062_vendor.mov", 0.52, None), "jewellery vendor at his stall, looking into his phone"),
    ("11_C062_vendor_close", ("full", "raw/baked/v1c/08_C062_vendor_close.mov", 4.92 - 4.2, (46.0, 787, 830)), "closer: the vendor's face and phone"),
    ("12_C058_show_step", ("full", "renders/fx_v3/C058_step.mov", 0.0, None), "STEP-PRINT: the Diwali show at the same fest, the stage stepping while the crowd watches"),
    ("13_C050_paan", ("new", "C050", 0.40, 1.0, None, 2.8), "paan maker in white wrapping paan (real time)"),
    ("14_C051_paan_look", ("new", "C051", 0.20, 1.0, None, 2.0), "he looks away, still, lost in thought (real time: 70 % ghosted a frame)"),
    ("15_C059_icecream", ("new", "C059", 0.50, 1.0, None, 2.0), "the ice-cream counter server at work in his hairnet"),
    ("16_C063_foam", ("new", "C063", 0.90, 1.0, None, 2.8), "next morning: the young car-washer foaming a scooter (real time)"),
    ("17_C064_wash", ("new", "C064", 5.60, 1.0, None, 2.8), "he washes the scooter, facing us, just before he looks up (wide)"),
    ("18_C064_look", ("new", "C064", 7.20, 0.8, None, 2.0, (55.0, 0.42, 0.40)), "cut-in: his face as he looks up toward the camera (80 %; 51 % of the width)"),
]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mix", type=float, default=0.6); ap.add_argument("--only")
    a = ap.parse_args()
    look_dir = REEL / "renders" / "look_v3"; look_dir.mkdir(parents=True, exist_ok=True)
    shots, look_shots = [], []
    for i, (name, src, shows) in enumerate(SHOTS):
        st, en = CUTS[i], (CUTS[i + 1] if i + 1 < len(CUTS) else None)
        dur = round(en - st, 2)
        line = v1.LINES[LINE_OF[i]][0]
        todo = not a.only or name in a.only.split(",")
        kind = src[0]
        if kind == "new":
            _, cid, cin, rate, stab, fno = src[:6]
            closer = src[6] if len(src) > 6 else None
            if todo:
                clip, camname, bstart = v2.build_new(name, cid, cin, rate, stab, fno, dur)
            else:
                clip, camname, bstart = f"{R}/renders/fx_preview_v2/{name}.mov", cid, None
            scale, pos = v2.top_anchor(75.0, 1080, dur)
            if closer:                                   # a fixed closer frame (4K terms), the half-size pre-render doubles the Scale
                sc4, u, v = closer
                sc_k, pos = v2b.macro_framing(u, v, sc4, dur)
                scale = [[t, round(x * 2, 2)] for t, x in sc_k]
            spd = "real time" if rate >= 0.999 else f"{int(round(rate * 100))} % (AE Timewarp)"
            shot = {"clip": clip, "src_in": 0.0, "rate": 1, "rotation": -90, "scale": scale, "pos": pos, "ease": "ease",
                    "note": f"build: camera {camname} in {cin:.2f} s, {spd}, {'stabilise position-only (Warp)' if stab else 'no stabilisation'}, "
                            f"depth f/{fno:g} recorded focus; push +5 % top-anchored; preview = half-size pre-render (Scale ×2)"}
        elif kind == "macro":
            _, cid, cin, (u, v), sc = src
            clip, camname, bstart = v2b.build_macro(name, cid, cin, dur, todo, stab=None)
            scale, pos = v2b.macro_framing(u, v, sc, dur)
            shot = {"clip": clip, "src_in": 0.0, "rate": 1, "rotation": -90, "scale": scale, "pos": pos, "ease": "ease",
                    "note": f"build: camera {camname} in {cin:.2f} s, real time; 1:1 crop on the hands (Scale {sc:g}); no preview stabiliser (it snapped); Warp in the build; f/4"}
        elif kind == "full":
            _, path, sin, framing = src
            if framing:
                sc, x, y = framing
                scale, pos, ease = [[0, sc], [dur, round(sc * 1.05, 2)]], [x, y], "ease"
            else:
                scale, pos = v2.top_anchor(37.5, 2160, dur)
                ease = "linear" if "step" in name else "ease"
            note = ("STEP-PRINT render (scripts/step_print.py --step 8, shutter blur; the reference's 'slow down'); build: Posterize Time 8 "
                    "+ the render swapped in" if "step" in name else "the plain depth bake, no stabilisation (v2d's stabiliser glitched here); Warp in the build")
            shot = {"clip": f"{R}/{path}", "src_in": round(sin, 3), "rate": 1, "rotation": -90, "scale": scale, "pos": pos, "ease": ease, "note": note}
        else:
            _, path, sin, nfps, ev = src
            scale, pos = v2.top_anchor(75.0, 1080, dur)
            shot = {"clip": f"{R}/{path}", "src_in": sin, "rate": round(FPS / nfps, 5), "scale": scale, "pos": pos, "ease": "ease",
                    "note": f"STOCK (Pexels; raw/SOURCES.md): native {nfps} fps at 25{'' if nfps == FPS else ' (real slow motion)'}; push +5 %"}
            if ev:
                shot["grade"] = {"exposure": ev, "sat": 1.0}
        shot.update(name=name, start=st, end=en, line=line, shows=shows)
        shots.append(shot)
        lshot = dict(shot)
        lout = look_dir / f"{name}.mov"
        if todo or not lout.exists():
            off = v2.lut_clip(shot["clip"], shot["src_in"], shot["rate"], dur, lout, a.mix, True)
        else:
            off = shot["src_in"] - max(0.0, shot["src_in"] - 0.1)
        lshot["clip"] = str(lout.relative_to(STUDIO)); lshot["src_in"] = round(off, 3)
        look_shots.append(lshot)
        print(f"{name:24s} {st:5.2f}–{en:5.2f}  L{LINE_OF[i] + 1}")
    end = {"name": "19_end_card", "start": CUTS[-1], "end": RUNTIME, "line": "— tumhara beta (title on black)",
           "shows": "title 'Mera diya bhi jalaana', sign-off, handle"}
    ov = [{"file": f"{R}/renders/overlays/window_matte_4x3.png", "start": 0.0, "end": CUTS[-1]}]
    for n in range(6):
        a0, b0 = CUTS[3 * n], CUTS[3 * n + 3] if 3 * n + 3 < len(CUTS) else CUTS[-1]
        ov.append({"file": f"{R}/renders/overlays/line_{n + 1:02d}.png", "start": round(a0 + (0.20 if n == 0 else 0.12), 2), "end": round(b0 - 0.08, 2)})
    ov.append({"file": f"{R}/renders/overlays/end_card.png", "start": round(CUTS[-1] + 0.12, 2), "end": RUNTIME})
    audio = [{"file": f"{R}/audio/guide_loop_v3.wav", "start": 0.0, "in": 0.0, "gain_db": -0.5, "fade_in": 0, "fade_out": 0}]  # -0.5: the loop seams peaked at -0.9 dBTP
    base = ("v3: 30.76 s, 6 lines × 3 bars on the looped guide (placeholder audio, director: 'extend, audio later'); 18 shots, 16 own "
            "(stock only S1 Maa's hands, F8 marigold hands); step-print stutter (reference's slow-down) on 01 and 12; vendor shots "
            "unstabilised (v2d glitch).")
    for fn, sh, extra in (("edl_v3.json", shots, " Camera-true."), ("edl_v3_look.json", look_shots, f" LOOK PREVIEW: ref_match.cube at {a.mix:.0%}.")):
        (REEL / "analysis" / fn).write_text(json.dumps({"fps": FPS, "runtime": RUNTIME, "note": base + extra, "shots": sh + [end],
                                                        "overlays": ov, "audio": audio}, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v3.json and analysis/edl_v3_look.json")


if __name__ == "__main__":
    main()
