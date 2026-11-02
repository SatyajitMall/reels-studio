# After Effects finishing (skill Phase 5b, optional)

Use After Effects for what Premiere can't do well: **denoise, true speed-ramp curves, Timewarp slow-mo, glow / halation**. Everything else stays in Premiere, including **stabilisation**: Warp Stabilizer can't be run by script in AE (below).

Verified on **After Effects 26.5 (26.5x89)**, 2026-10-17. Re-verify after an AE update.

## Setup (one time per machine)
1. After Effects is running, with an **empty untitled project** or no project open. The round-trip never touches another project: it refuses to run if one is open.
2. macOS Automation permission. The first call shows "… wants to control Adobe After Effects 2026": the director clicks **Allow**.
3. Check: `./.venv/bin/python scripts/ae_bridge.py verify` → `ok: true`, AE version.

## The bridge
- `scripts/ae_bridge.py` runs ExtendScript in AE and returns JSON.
- **AppleScript replies are useless:** `DoScript` always answers "0", or "1" when AE refuses. Results come back through a JSON file.
- **Never use `DoScriptFile`:** on 26.5 it didn't run, and it left a dialog that blocked every later script.
- **Long scripts block AE.** AE shows an "Executing Script…" window and refuses all other scripts until it ends. Never enumerate `app.effects` (it took 5+ minutes); check specific names with `ae_bridge.py effects <matchName>…`.
- **"Unable to obtain dynamiclink server"** appeared once in the director's AE during a render, while Premiere was also open (Premiere runs the Dynamic Link manager). Clicking OK was harmless, and the render finished.
- **If every call returns "1",** AE is busy or a dialog is open. Ask the director to look at AE and close or cancel it. Don't retry in a loop.

## The round-trip
1. **Write the jobs file.** Put `projects/<reel>/analysis/ae_jobs.json` together from the EDL, one entry per shot: source clip, source in/out, ops. The format is in `scripts/ae_roundtrip.py`.
2. **Run it:** `./.venv/bin/python scripts/ae_roundtrip.py projects/<reel>/analysis/ae_jobs.json [--only <shot>]`. This renders `projects/<reel>/renders/ae/<shot>.mov` (ProRes 422, at the job's size and the sequence fps) plus `<shot>_compare.png`, and logs everything to `analysis/ae_log.json`.
   - **Slow motion: render at the camera's size** (`"width": 2160, "height": 3840` for the director's vertical 4K), so Premiere's framing and pushes carry over when the render is swapped in at 100 % speed (goddess round 10).
   - **Rotated phone clips:** the camera files are stored landscape with a −90° flag, which After Effects ignores. Since v0.8 the script detects the flag and feeds AE an upright ProRes HQ trim (in − 0.5 s … out + 0.5 s, in `renders/ae_src/`, named by its in/out). Leave the job's `rotate` at 0 for these clips: the trim is already upright.
   - `width` / `height` / `fps` are set once, at the top of the jobs file, for every shot in it. Use a separate jobs file for shots at another size.
   - Each shot takes about **4 minutes**: aerender starts its own copy of AE.
   - Run batches in the background.
3. **Check every shot before using it:**
   - read `frame_match` in `ae_log.json` (and the console). It confirms that output frame 0 is the source at the in-point. On a mismatch, don't use the render: report it to HQ;
   - look at `_compare.png`;
   - for denoise, compare a 1:1 crop of a dark area;
   - for stabilise, run `scripts/shake_report.py` on the source vs the output;
   - for colour, run `scripts/colour_report.py`. The output's luma should stay within ±0.02 of the source.
4. **Swap the clip in Premiere:**
   - import the `.mov` with the reality-doc import snippet;
   - replace the original shot at the same timeline position;
   - check with `get_timeline_gaps`.

   AE renders the comp starting at the shot's in-point, so place the `.mov` from its start. No need to pre-trim sources: point `source` at the original clip and set `in_s` / `out_s`.

## Ops: what they do and what we learned
| Op | Effect | Defaults and verified notes |
|---|---|---|
| `denoise` | Remove Grain (`VISINF Grain Removal`) | Measured on 7 my-reel v7 shots: −12…−29 % dark-area noise. **Viewing Mode must be 4 (Final Output)**: 3 renders a black matte, 1 shows only a preview box. AE's default strength (1.0, 3 passes) cut noise 30 % on C027 but smeared texture. The studio default (0.6, 2 passes, `"temporal": true`) cut noise 19 % and kept texture. It's a modest denoiser: **Neat Video** (paid plugin) is far stronger if the director buys it. |
| `timewarp` | Timewarp (`ADBE Timewarp`), Method 3 = Pixel Motion | **The studio's slow-mo route for ≤ 30 fps footage (v0.8).** Counts from the shot's in-point since v0.4.1. v0.4.0 retimed from the start of the file, which the pilot caught on C076. Verified: C076 in 15.96 s at 60 % → 3.52 s, frame 0 = in-point; a pre-trimmed source gives the same result with no black tail. Goddess v10b, a 25 fps night crowd at 64 % and Ma at 55 %, both at 4K: passed review where Premiere Optical Flow doubled an arm. Check the fastest-moving element at 2× on in-between frames: single, never doubled. Measured bar: no frame more than ~70 % blend-like, half-resolution sharp/soft alternation within 0.03 of real footage. Still check fast or crossing motion for warping. |
| `time_remap` | layer time remapping, Bezier keys with ease | Verified on C077: one clip, smooth ease, replacing Premiere's two-clip fake. `points` are `[comp_s, source_s]`. Output can run 1 frame long (2.52 s for 2.5), so trim in Premiere. Never delete all of AE's default keys first: that hides the property ("Can not set value at time"). |
| `stabilise` | — | **Not supported; the script refuses it.** Added by script, Warp Stabilizer never analyses: every frame rendered with a blue "Click Analyze to begin." banner. Its jitter numbers even looked better, because the tracker locked onto the fixed banner. Stabilise in Premiere (skill Phase 5), or have the director click **Analyze** in AE by hand. |
| `glow` | Glow (`ADBE Glo2`; `ADBE GloH` doesn't exist on 26.5) | Halation on diyas and lamps. Defaults are threshold 80 %, radius 25, intensity 0.25: the pilot found 70 % / 0.5 clipped 21–54 % of pixels on ungraded night shots. Glow shots still needed exposure trims of +0.09…+0.13 luma in Premiere afterwards, so check them with `colour_report.py` against their neighbours. |
| `grain` | Add Grain (`VISINF Grain Implant`) | Bring back a little texture after denoise, if wanted |

## Optional paid plugins (the director decides)
- **Neat Video:** denoise.
- **Twixtor:** slow-mo.
- **RSMB:** motion blur on speed-ups.
- **Deep Glow:** glow.

None is installed today. If the director buys one, HQ adds it as an op.
