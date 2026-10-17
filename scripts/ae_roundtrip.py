#!/usr/bin/env python3
"""After Effects round-trip for finishing shots that Premiere can't do well.

For each shot in a jobs file it:
  1. builds a fresh AE project via scripts/ae_bridge.py (import source, 1080x1920 comp at the reel's
     fps, source in-point at comp 0, optional rotation/fill),
  2. applies the ops in order,
  3. saves projects/<reel>/renders/ae/<name>.aep and renders <name>.mov headlessly with aerender
     (default output module "High Quality" = ProRes 422; pass --om for another template),
  4. writes <name>_compare.png (source vs AE output, same moment) for checking by eye, and logs
     everything to projects/<reel>/analysis/ae_log.json.
The reel session then imports the .mov in Premiere and swaps it in for the original clip.

Jobs file (projects/<reel>/analysis/ae_jobs.json):
{
  "reel": "my-reel", "fps": 25, "width": 1080, "height": 1920,
  "shots": [
    {"name": "s01_C027", "source": "projects/my-reel/raw/b-roll/A001_10150436_C027.mov",
     "in_s": 2.0, "out_s": 4.5, "rotate": 0, "fill": true,
     "ops": [{"op": "denoise"},
             {"op": "timewarp", "speed": 50},
             {"op": "time_remap", "points": [[0, 0], [0.6, 1.5], [2.0, 2.0]], "ease": 75},
             {"op": "glow", "threshold": 70, "radius": 25, "intensity": 0.5},
             {"op": "grain", "intensity": 0.3}]}
  ]
}
Ops (built-in effects only; match names verified on AE 26.5 with `ae_bridge.py effects`):
  denoise     Remove Grain (VISINF Grain Removal), Viewing Mode = 4 (Final Output); "amount" (0.6),
              "passes" (2), "temporal": true adds temporal filtering. AE's defaults (1.0, 3 passes) cut
              noise 30 % on my-reel C027 but smeared texture
  timewarp    Timewarp (ADBE Timewarp), Pixel Motion, speed % (comp length = shot / speed)
  time_remap  speed ramp: points are [comp_s, source_s relative to in_s], Bezier keys with ease %
  stabilise   NOT SUPPORTED. Added by script, Warp Stabilizer never analyses: every rendered frame
              carried a "Click Analyze to begin." banner (tested 2026-10-17). Stabilise in Premiere
              (skill Phase 5), or have the director click Analyze in AE by hand.
  glow        Glow (ADBE Glo2) on highlights: threshold %, radius, intensity
  grain       Add Grain (VISINF Grain Implant) at a low intensity, after denoise if you want texture back

Usage:
  ./.venv/bin/python scripts/ae_roundtrip.py projects/<reel>/analysis/ae_jobs.json [--only NAME] [--om "High Quality"]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ae_bridge import run_jsx  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
AERENDER = "/Applications/Adobe After Effects 2026/aerender"

BUILD_JSX = r"""
var S = __SPEC__;
var proj = app.project;
// Safety: never discard the director's own AE work. Allowed: an empty untitled project, or a
// project this script made (saved under projects/<reel>/renders/ae/, or tagged with the marker folder).
var MARK = "__reels_studio_ae_roundtrip";
var ours = proj.file && proj.file.fsName.indexOf("/renders/ae/") >= 0;
for (var i = 1; i <= proj.numItems && !ours; i++) if (proj.item(i).name == MARK) ours = true;
if (!ours && (proj.numItems > 0 || proj.file)) {
    throw new Error("After Effects has another project open (" + (proj.file ? proj.file.fsName : "unsaved, " + proj.numItems + " items") +
                    "). Save and close it, or open a new empty project, then rerun.");
}
app.newProject();
proj = app.project;
proj.items.addFolder(MARK);
try {

var src = proj.importFile(new ImportOptions(new File(S.source)));
if (src.frameRate && Math.abs(src.frameRate - S.fps) > 0.01 && Math.abs(src.frameRate - S.fps) < 2) {
    src.mainSource.conformFrameRate = S.fps;   // e.g. 24 → 25: frame-for-frame, like Premiere's interpretation
}
var srcDur = S.out_s - S.in_s;
var compDur = srcDur;
var tw = null, tr = null;
for (var i = 0; i < S.ops.length; i++) {
    if (S.ops[i].op == "timewarp") tw = S.ops[i];
    if (S.ops[i].op == "time_remap") tr = S.ops[i];
}
if (tw) compDur = srcDur / (tw.speed / 100);
if (tr) compDur = tr.points[tr.points.length - 1][0];
var comp = proj.items.addComp(S.name, S.width, S.height, 1, compDur, S.fps);
var layer = comp.layers.add(src);
layer.startTime = -S.in_s;          // source in-point lands at comp 0
if (layer.outPoint < compDur) layer.outPoint = compDur;
if (S.rotate) layer.property("ADBE Transform Group").property("ADBE Rotate Z").setValue(S.rotate);
if (S.fill !== false) {
    var w = src.width, h = src.height, r = layer.sourceRectAtTime(0, false);
    var sc = Math.max(S.width / r.width, S.height / r.height) * 100;
    layer.property("ADBE Transform Group").property("ADBE Scale").setValue([sc, sc]);
}

// Source moment shown at the middle of the comp (for the before/after still).
var mid = compDur / 2, srcMid = S.in_s + mid;
if (tw) srcMid = S.in_s + mid * tw.speed / 100;
if (tr) { for (var k = 1; k < tr.points.length; k++) { var a = tr.points[k - 1], b = tr.points[k];
          if (mid <= b[0]) { srcMid = S.in_s + a[1] + (b[1] - a[1]) * (mid - a[0]) / (b[0] - a[0]); break; } } }
var report = {name: S.name, compDur: compDur, srcMid: srcMid, applied: [], warnings: [], params: {}};
function setByName(fx, name, value) {
    for (var k = 1; k <= fx.numProperties; k++) {
        var p = fx.property(k);
        if (p.name == name) { try { p.setValue(value); return true; } catch (e) { report.warnings.push(fx.name + "." + name + ": " + e); return false; } }
    }
    report.warnings.push(fx.name + ": no property '" + name + "'");
    return false;
}
function listProps(fx) {
    var out = [];
    for (var k = 1; k <= fx.numProperties; k++) {
        var p = fx.property(k);
        var v = null; try { v = p.value; } catch (e) {}
        out.push([p.name, (typeof v == "number" || typeof v == "boolean") ? v : null]);
    }
    return out;
}
var fxGroup = layer.property("ADBE Effect Parade");
for (var i = 0; i < S.ops.length; i++) {
    var op = S.ops[i], fx = null;
    if (op.op == "denoise") {
        fx = fxGroup.addProperty("VISINF Grain Removal");
        setByName(fx, "Viewing Mode", op.viewing_mode || 4);    // 1 Preview (a small box), 2 Noise Samples, 3 Blending Matte, 4 Final Output (verified by render)
        if (op.temporal) setByName(fx, "Enable", 1);              // Temporal Filtering: steadier result on video, slower
        setByName(fx, "Noise Reduction", op.amount !== undefined ? op.amount : 0.6);   // AE default 1.0 smeared detail on my-reel C027
        setByName(fx, "Passes", op.passes || 2);
    } else if (op.op == "timewarp") {
        fx = fxGroup.addProperty("ADBE Timewarp");
        setByName(fx, "Method", op.method || 3);               // 3 = Pixel Motion
        setByName(fx, "Speed", op.speed);
    } else if (op.op == "time_remap") {
        layer.timeRemapEnabled = true;
        var trp = layer.property("ADBE Time Remapping");
        // Add ours first, then drop AE's two default keys: removing every key hides the property
        // ("Can not set value at time … property is hidden").
        var want = {};
        for (var k = 0; k < op.points.length; k++) { trp.setValueAtTime(op.points[k][0], S.in_s + op.points[k][1]); want[op.points[k][0].toFixed(3)] = 1; }
        for (var k = trp.numKeys; k >= 1; k--) if (!want[trp.keyTime(k).toFixed(3)]) trp.removeKey(k);
        var ease = new KeyframeEase(0, op.ease || 75);
        for (var k = 1; k <= trp.numKeys; k++) {
            trp.setInterpolationTypeAtKey(k, KeyframeInterpolationType.BEZIER);
            trp.setTemporalEaseAtKey(k, [ease], [ease]);
        }
        layer.outPoint = compDur;
        report.applied.push("time_remap");
        continue;
    } else if (op.op == "stabilise") {
        throw new Error("stabilise isn't supported by script: Warp Stabilizer never analyses and renders a 'Click Analyze to begin.' banner. Stabilise in Premiere instead (skill Phase 5).");
    } else if (op.op == "glow") {
        fx = fxGroup.addProperty("ADBE Glo2");
        if (op.threshold !== undefined) setByName(fx, "Glow Threshold", op.threshold);
        if (op.radius !== undefined) setByName(fx, "Glow Radius", op.radius);
        if (op.intensity !== undefined) setByName(fx, "Glow Intensity", op.intensity);
    } else if (op.op == "grain") {
        fx = fxGroup.addProperty("VISINF Grain Implant");
        if (op.intensity !== undefined) setByName(fx, "Intensity", op.intensity);
    } else {
        report.warnings.push("unknown op " + op.op);
        continue;
    }
    report.applied.push(op.op);
    report.params[op.op] = listProps(fx);   // read back, so the log shows what AE actually holds
}
return report;
} catch (e) {
    proj.close(CloseOptions.DO_NOT_SAVE_CHANGES);   // don't leave a half-built project blocking the next run
    throw e;
}
"""

SAVE_JSX = r"""
var S = __SPEC__;
var comp = null;
for (var i = 1; i <= app.project.numItems; i++) if (app.project.item(i) instanceof CompItem && app.project.item(i).name == S.name) comp = app.project.item(i);
if (!comp) throw new Error("comp " + S.name + " not found");
app.project.save(new File(S.aep));
return {saved: S.aep};
"""


def jsx(template: str, spec: dict) -> str:
    return template.replace("__SPEC__", json.dumps(spec))


def compare_still(source: Path, src_mid: float, out_mov: Path, png: Path, comp_dur: float) -> None:
    """Source vs AE render at the same moment (middle of the shot, mapped through any retime), side by side."""
    mid = comp_dur / 2
    tmp_a, tmp_b = png.with_suffix(".a.png"), png.with_suffix(".b.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(src_mid), "-i", str(source), "-frames:v", "1",
                    "-vf", "scale=540:960:force_original_aspect_ratio=increase,crop=540:960", str(tmp_a)], check=False)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(mid), "-i", str(out_mov), "-frames:v", "1",
                    "-vf", "scale=540:960", str(tmp_b)], check=False)
    if tmp_a.exists() and tmp_b.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp_a), "-i", str(tmp_b), "-filter_complex", "hstack",
                        str(png)], check=False)
    for t in (tmp_a, tmp_b):
        t.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("jobs", type=Path)
    ap.add_argument("--only", help="run just this shot name")
    ap.add_argument("--om", default="High Quality", help="aerender output module template (default ProRes 422)")
    args = ap.parse_args()

    jobs = json.loads(args.jobs.read_text())
    reel = jobs["reel"]
    out_dir = ROOT / "projects" / reel / "renders" / "ae"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = ROOT / "projects" / reel / "analysis" / "ae_log.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else []

    for shot in jobs["shots"]:
        if args.only and shot["name"] != args.only:
            continue
        spec = {**shot, "fps": jobs.get("fps", 25), "width": jobs.get("width", 1080), "height": jobs.get("height", 1920),
                "source": str((ROOT / shot["source"]).resolve())}
        spec["aep"] = str(out_dir / f"{shot['name']}.aep")
        mov = out_dir / f"{shot['name']}.mov"
        print(f"▸ {shot['name']}: building in After Effects", flush=True)
        built = run_jsx(jsx(BUILD_JSX, spec), timeout_s=300)
        entry = {"name": shot["name"], "time": time.strftime("%Y-%m-%d %H:%M:%S"), "spec": shot, "build": built}
        if not built.get("ok"):
            print(f"✗ build failed: {built.get('error')}")
            log.append(entry)
            break
        rep = built["result"]
        for w in rep.get("warnings", []):
            print(f"  ! {w}")
        saved = run_jsx(jsx(SAVE_JSX, spec), timeout_s=120)
        if not saved.get("ok"):
            print(f"✗ save failed: {saved.get('error')}")
            entry["save"] = saved
            log.append(entry)
            break
        print(f"  rendering with aerender ({args.om})", flush=True)
        r = subprocess.run([AERENDER, "-project", spec["aep"], "-comp", shot["name"], "-OMtemplate", args.om,
                            "-output", str(mov)], capture_output=True, text=True)
        entry["aerender_rc"] = r.returncode
        entry["aerender_tail"] = (r.stdout + r.stderr)[-1500:]
        if r.returncode != 0 or not mov.exists():
            print(f"✗ aerender failed (rc {r.returncode}):\n{entry['aerender_tail']}")
            log.append(entry)
            break
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate:format=duration",
                                "-of", "json", str(mov)], capture_output=True, text=True).stdout
        entry["output"] = {"mov": str(mov.relative_to(ROOT)), "probe": json.loads(probe or "{}")}
        png = out_dir / f"{shot['name']}_compare.png"
        compare_still(Path(spec["source"]), rep["srcMid"], mov, png, rep["compDur"])
        entry["compare_png"] = str(png.relative_to(ROOT)) if png.exists() else None
        log.append(entry)
        print(f"✓ {mov.relative_to(ROOT)}  · compare: {entry['compare_png']}")

    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, indent=1))
    print(f"log: {log_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
