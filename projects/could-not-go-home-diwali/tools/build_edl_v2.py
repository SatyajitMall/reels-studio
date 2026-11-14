"""Build EDL v2 for could-not-go-home-diwali (reel-local): v1c + the director's p1c note
"look at the reference … too far … add stock: micro / macro subjects, shots without the subject's face".

Each letter line pairs one of our workers with a no-face Pexels insert (director's "Recommended set"); 6 of 11 shots
show no face (the reference: 5 of 9). 50/60 fps stock is interpreted at 25 fps: real slow motion, no invented frames.
Two renders from one cut: camera-true (edl_v2.json) and the reference-match look (edl_v2_look.json: every clip passed
through analysis/look_ref/ref_match.cube at --mix, black bars and type untouched).

Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v2.py [--mix 0.6]
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

FPS = 25
WIN_TOP = 505
PUSH = 1.05
FX = f"{R}/renders/fx_preview_v1c"
LINE_OF = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

# (name, source, shows). source: ("fx", file in fx_preview_v1c) | ("new", cid, cam_in, rate, stab, fnumber) | ("stock", path, src_in, native fps, kind)
SHOTS = [
    ("01_C047_auto", ("fx", "01_C047_auto.mov"), "auto driver from the back seat, the lit street drifting past (70 %)"),
    ("02_S9_diyas", ("stock", "raw/stock/pexels-34579325/14652728_3840_2160_25fps.mp4", 2.0, 25, "land"),
     "stock S9: a row of lit diyas in the dark, the Diwali at home he isn't at"),
    ("03_C054_parotta", ("new", "C054", 0.80, 1.0, "smooth", 2.8), "parotta maker lifting a parotta off the tawa (real time)"),
    ("04_S24_market", ("stock", "raw/stock/pexels-34766750/14739228_1080_1920_60fps.mp4", 6.0, 60, "vert"),
     "stock S24: the night market from above, the busiest night (60 fps → 42 % slow motion)"),
    ("05_S1_maa_roti", ("stock", "raw/stock/pexels-38001819/16127033_1920_1080_50fps.mp4", 2.4, 50, "land"),
     "stock S1: a mother's hands shaping roti at night (50 fps → 50 % slow motion)"),
    ("06_C052_cook", ("fx", "05_C052_cook_plating.mov"), "the young cook's hands plating food for strangers (real time)"),
    ("07_C062_vendor", ("fx", "07_C062_vendor.mov"), "jewellery vendor at his stall, looking into his phone"),
    ("08_S14_aarti", ("stock", "raw/stock/pexels-34565062/14645124_1920_1080_25fps.mp4", 5.6, 25, "land"),
     "stock S14: a hand passing over the lit diyas, taking the aarti"),
    ("09_C050_paan", ("fx", "09_C050_paan.mov"), "paan maker in white wrapping paan (real time)"),
    ("10_C051_paan_look", ("fx", "10_C051_paan_look.mov"), "he looks away, still, lost in thought (70 %)"),
    ("11_S8_diya_ring", ("stock", "raw/stock/pexels-36424458/15444557_3840_2160_60fps.mp4", 1.5, 60, "land"),
     "stock S8: a ring of lit diyas on rangoli from above (real time; slow motion read as a freeze)"),
    ("12_C064_carwash_look", ("fx", "12_C064_carwash_look.mov"), "the car-washer looks up from the work toward the camera (80 %)"),
]


def probe_wh(path):
    p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0",
                        str(STUDIO / path)], capture_output=True, text=True)
    w, h = p.stdout.strip().splitlines()[0].split(",")[:2]
    return int(w), int(h)


def top_anchor(sc, img_h, dur, push=PUSH):
    s1 = round(sc * push, 3)
    return [[0, sc], [dur, s1]], [[0, 540, round(WIN_TOP + img_h * sc / 200, 1)], [dur, 540, round(WIN_TOP + img_h * s1 / 200, 1)]]


def build_new(name, cid, cin, rate, stab, fno, dur):
    """Bake + pre-render a camera window that v1c didn't have (same pipeline as build_edl_v1c)."""
    cam = sorted((REEL / "raw" / "Media").glob(f"*_{cid}.mov"))[0]
    need = dur * rate
    bstart = max(0.0, round((cin - 0.72) * FPS) / FPS)
    bdur = round((cin - bstart + need + 1.0) * FPS) / FPS
    bake_dir = REEL / "raw" / "baked" / "v2"; bake_dir.mkdir(parents=True, exist_ok=True)
    baked = bake_dir / f"{name}.mov"
    r = subprocess.run([str(REEL / "tools" / "cine_bake"), str(cam), str(baked), "--start", f"{bstart:.2f}", "--dur", f"{bdur:.2f}",
                        "--fnumber", f"{fno}"], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"bake {name}: {r.stderr or r.stdout}")
    out = REEL / "renders" / "fx_preview_v2" / f"{name}.mov"; out.parent.mkdir(parents=True, exist_ok=True)
    job = [{"id": name, "clip": str(baked.relative_to(STUDIO)), "src_in": round(cin - bstart, 3), "out_dur": dur, "stab": stab,
            "sigma": 15, "zoom": 1.04, "transl_only": True, "rate": rate, "out": str(out.relative_to(STUDIO))}]
    jf = REEL / "analysis" / "fx_jobs_v2.json"; jf.write_text(json.dumps(job, indent=1))
    subprocess.run([sys.executable, "-I", str(REEL / "tools" / "fx_prerender.py"), "--jobs", str(jf)], cwd=STUDIO, check=True)
    return str(out.relative_to(STUDIO)), cam.name, bstart


def lut_clip(src, src_in, rate, dur, out, mix, rotate):
    """Render the used stretch of a clip through the reference-match LUT (preview of the V3 look), ProRes, same geometry."""
    lut = REEL / "analysis" / "look_ref" / "ref_match.cube"
    t0 = max(0.0, src_in - 0.1)
    need = dur * rate + 0.4
    vf = (f"scale=in_color_matrix=bt709:out_color_matrix=bt709,format=gbrp16le,split[a][b];"
          f"[b]lut3d=file='{lut}':interp=tetrahedral[l];[a][l]blend=all_mode=normal:all_opacity={mix},"
          f"scale=in_color_matrix=bt709:out_color_matrix=bt709:out_range=tv,format=yuv422p10le")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-t", f"{need:.3f}", "-i", str(STUDIO / src)]
    cmd += ["-vf", vf, "-c:v", "prores_ks", "-profile:v", "2", "-an", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", str(out)]
    subprocess.run(cmd, check=True)
    return src_in - t0


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mix", type=float, default=0.6)
    a = ap.parse_args()
    shots, look_shots = [], []
    look_dir = REEL / "renders" / "look_v2"; look_dir.mkdir(parents=True, exist_ok=True)
    for i, (name, src, shows) in enumerate(SHOTS):
        st, en = v1.CUTS[i], v1.CUTS[i + 1]
        dur = round(en - st, 2)
        line = v1.LINES[LINE_OF[i]][0]
        if src[0] in ("fx", "new"):
            if src[0] == "fx":
                clip = f"{FX}/{src[1]}"
                v1c = {s["clip"]: s for s in json.loads((REEL / "analysis" / "edl_v1c.json").read_text())["shots"] if "clip" in s}
                s0 = v1c[clip]
                note = s0["note"]
                scale, pos = s0["scale"], s0["pos"]
            else:
                _, cid, cin, rate, stab, fno = src
                clip, camname, bstart = build_new(name, cid, cin, rate, stab, fno, dur)
                scale, pos = top_anchor(75.0, 1080, dur)
                note = (f"build: camera {camname} in {cin:.2f} s, real time, stabilise position-only (Warp), depth f/{fno:g} "
                        f"recorded focus (bake start {bstart:.2f}); push +5 % top-anchored; preview = half-size pre-render (Scale ×2)")
            shot = {"name": name, "start": st, "end": en, "clip": clip, "src_in": 0.0, "rate": 1, "rotation": -90,
                    "scale": scale, "pos": pos, "ease": "ease", "line": line, "shows": shows, "note": note}
            rate_eff, rotate = 1.0, True
        else:
            _, path, sin, nfps, kind = src
            still = name in ("02_S9_diyas", "11_S8_diya_ring")    # still lifes: real time + a stronger push (pregate: "frozen")
            rate_eff = 1.0 if still else round(FPS / nfps, 5)     # else every native frame once at 25 fps
            w, h = probe_wh(f"{R}/{path}")
            if kind == "vert":                                    # 1080×1920: window shows its middle 810 rows
                sc0 = 100.0 * 1080 / w
                scale = [[0, sc0], [dur, round(sc0 * PUSH, 3)]]
                pos = [540, 910]
            else:                                                 # landscape: 4:3 middle of the frame fills the window
                sc0 = 100.0 * 810 / h
                scale, pos = top_anchor(sc0, h, dur, 1.12 if still else PUSH)
            slow = "real time" if (nfps == FPS or still) else f"{int(round(100 * FPS / nfps))} % (native {nfps} fps interpreted at 25: real frames)"
            shot = {"name": name, "start": st, "end": en, "clip": f"{R}/{path}", "src_in": sin, "rate": rate_eff,
                    "scale": scale, "pos": pos, "ease": "ease", "line": line, "shows": shows,
                    "note": f"STOCK (Pexels, raw/SOURCES.md): {slow}; build: set_override_frame_rate 25 on import; push +{12 if still else 5} %"}
            if name == "05_S1_maa_roti":
                shot["grade"] = {"exposure": 1.0, "sat": 1.0}
                shot["note"] += "; primary: exposure +1.0 stop (the stock is underexposed)"
            rotate = False
        shots.append(shot)
        # look version
        lshot = dict(shot)
        lout = look_dir / f"{name}.mov"
        off = lut_clip(shot["clip"], shot["src_in"], shot["rate"], dur, lout, a.mix, rotate)
        lshot["clip"] = str(lout.relative_to(STUDIO)); lshot["src_in"] = round(off, 3)
        if shot.get("rotation"):
            # ffmpeg autorotates on decode for the fx files? fx files carry no tag; keep the EDL rotation as is
            pass
        look_shots.append(lshot)
        print(f"{name:22s} {st:5.2f}–{en:5.2f} {line[:34]}")
    end = {"name": "13_end_card", "start": v1.CUTS[-1], "end": v1.RUNTIME, "line": "— tumhara beta (title on black)",
           "shows": "title 'Mera diya bhi jalaana', sign-off, handle"}
    prev = json.loads((REEL / "analysis" / "edl_v1.json").read_text())
    base_note = ("v2 = v1c + director note on p1c ('too far from the reference; add macro / no-face stock'): each line pairs one of "
                 "our workers with a no-face Pexels insert (S9, S24, S1, S14, S8); 6 of 11 shots without a face. 50/60 fps stock "
                 "interpreted at 25 (real slow motion). Cuts, letter, window, type unchanged.")
    for fn, sh, extra in (("edl_v2.json", shots, " Camera-true."),
                          ("edl_v2_look.json", look_shots, f" LOOK PREVIEW: every clip through analysis/look_ref/ref_match.cube at {a.mix:.0%} "
                                                            "(build: V3 adjustment layer, the .cube loaded by hand, Creative Intensity to match).")):
        doc = {"fps": FPS, "runtime": v1.RUNTIME, "note": base_note + extra, "shots": sh + [end], "overlays": prev["overlays"],
               "audio": prev["audio"]}
        (REEL / "analysis" / fn).write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v2.json and analysis/edl_v2_look.json")


if __name__ == "__main__":
    main()
