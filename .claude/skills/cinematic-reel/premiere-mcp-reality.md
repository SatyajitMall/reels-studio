# Premiere MCP: what actually works

Verified by the `my-reel` pilot on **Premiere 26.5.2 + adobe-premiere-pro-mcp 1.2.9** (2026-10-16). When either version changes, re-test the ❌ rows and update this file. Bugs are drafted for upstream in `studio/upstream/premiere-mcp-issues.md`.

## Rule 1: verify by render, never by the tool's reply
Many tools return `success`, `deleted: true` or `accepted_unverified` without doing the work. After every colour, transition, opacity, blend or audio change:
1. **Export a still**: `export_frame` with **no `format` argument**.
2. **Check it**:
   - numerically: luma, saturation, and `ffmpeg -af volumedetect` for audio;
   - and by eye.

Structural edits are checked with `get_timeline_gaps` / `get_timeline_summary` (CLAUDE.md §2.4).

## Rule 2: read script results through a file
`execute_extendscript` and `evaluate_expression` always return `"undefined"`. Make the script write its result, then read the file with Bash:

```javascript
var f = new File("/Users/<you>/Documents/reels-studio/projects/<reel>/analysis/_es_out.txt");
f.open("w"); f.write(JSON.stringify(result)); f.close();
```

## Tool status

| Tool | Status | Use instead |
|---|---|---|
| `verify_premiere_connection`, `list_sequences`, `add_to_timeline_batch`, `create_bin`, `duplicate_sequence`, `set_override_frame_rate`, `set_clip_rotation`, `remove_from_timeline`, `get_timeline_gaps`, `get_clip_properties`, `list_clip_effects`, `save_project` | ✅ works as documented | — |
| `import_folder` | ❌ `targetBin.importFiles is not a function` | ExtendScript: `app.project.importFiles(paths, true, targetBin, false)` |
| `import_media` with `binName` | ⚠️ imports, but into the project root | Import with the snippet above, or move afterwards (`item.moveBin(bin)`) |
| `delete_multiple_project_items` | ❌ `deleteResults.filter is not a function` | Temp-bin delete (below) |
| `delete_project_item` (footage) | ❌ says `deleted: true`, item stays | Temp-bin delete (below) |
| `execute_extendscript`, `evaluate_expression` | ⚠️ run, but return `"undefined"` | Rule 2 |
| `export_frame` with `format:"png"`, or into a folder that doesn't exist | ❌ `Illegal Parameter type` (same error for both) | Omit `format`; create the folder first |
| `color_correct` | ⚠️ writes only Contrast, Temperature, Tint. Brightness/Highlights/Shadows are ignored. `saturation` lands as 0 **and** zeroes Creative Saturation, so the clip turns **black & white** | Lumetri recipe (below). Never pass `saturation` |
| `set_effect_property` | ⚠️ sets only the **first** property with that name. Lumetri has 3 × "Saturation", 2 × "Intensity", 2 × "Contrast" | Set by occurrence in ExtendScript |
| `add_adjustment_layer` | ❌ makes a transparent PNG, not an adjustment layer. No scripting API for adjustment layers exists | Director makes one by hand (below) |
| `apply_lut` | ❌ reports success, loads nothing (custom `.cube` can't be loaded by script) | A look with a built-in preset: `app.project.applyLumetriPreset("<preset name>")` on the selected clip (325 built-ins: `getAllLumetriPresetsList()`). Any other look: the director picks it in Creative → Look. **Never write the Lumetri `Look` slot**: it's a dropdown index, and later writes change the number, not the look (effects-playbook §A3) |
| `set_blend_mode` | ❌ `Illegal Parameter type` | Set `Opacity.properties[1]` with the enum below |
| `add_transition`, `add_transition_to_clip` | ❌ lands one cut off, returns `accepted_unverified` | QE snippet (below) |
| Opacity keyframes on a clip interpreted to another fps | ❌ didn't render (Motion keyframes did) | Dip to Black transition for fades |
| `set_clip_volume {volumeDb}` | ❌ writes linear 0 → silent | Level formula (below) |
| `slip_edit` | ⚠️ `offset` ignored | Use `deltaSeconds` |
| `razor_timeline_at_time` with `audioTrackIndices: []` | ⚠️ empty array = **all** audio tracks | List the tracks you mean |
| `speed_change` | ⚠️ keeps the timeline duration and changes the source span (2.0 = twice the source) | Speed-ramp recipe in playbook §C |
| A speed-changed clip's `inPoint` / `outPoint` (QE `setSpeed`) | ⚠️ read and write **source time ÷ speed**. Writing raw source seconds moved both in-points (goddess round 10) | Write source ÷ speed, then check source = DOM value × speed |
| Scale keyframes on a speed-changed clip | ❌ didn't run the full ramp (goddess v10: C051 still at 0.56 Scale partway through) | Slow-mo through After Effects (playbook §C), swapped in at 100 % speed, with the push keyed on that clip |
| Optical Flow (QE `setTimeInterpolationType(2)`) | ⚠️ falls back to frame blends on fast or crossing motion: a doubled arm and a sharp/soft pulse on a 25 fps night crowd (goddess v10) | After Effects Timewarp (`after-effects.md`) |
| `get_encoder_presets` | ⚠️ finds no factory presets | Built-in `.epr` paths (below) |
| `create_sequence` | ⚠️ needs an `.sqpreset` | `create_sequence_from_clips` on a clip with the target size and fps |
| `exportAsMediaDirect` / `export_sequence` | ⚠️ correct picture, **silent audio** in the pilot (cause unknown) | Always check audio after export. Fallback: `scripts/mix_from_edl.py` |
| `applyLumetriPreset` on a clip that **already has a Lumetri** | ⚠️ adds a second Lumetri and inserts it **before** the old one; the `Look` slot reads 1 after any preset (kolkata v7: intensity 30 landed on the old, look-less Lumetri, so the look rendered at 100 %) | Find the look's Lumetri by `Look` ≠ 0 or a non-empty look path (prop 32), never by position; or apply the preset to a layer with no Lumetri |
| QE `addTransition` where the clip has no media past its out-point (or before its in-point) | ⚠️ silently makes a shorter, one-sided transition: 5–6 of 10 frames, ending on the cut (kolkata C076) | Read back `transitions[j].start/end` and flag any shorter than asked |
| `setInPoint` + `overwriteClip` | ⚠️ landed 1 frame early on 2 of 26 video clips and on audio (kolkata v2, v3, v6) | In-point read-back (snippet below), on every placed clip |
| `stabilize_clip` (Warp Stabilizer) | ✅ applies and analyses by itself. `AnalysisStatusCounter` 104 = running, 408 = done; the property name carries the auto-scale ("Auto-scale (103.1%)"). Changing Smoothness after analysis doesn't re-solve | Wait for 408 before exporting; set Smoothness before analysis |
| Gaussian Blur (Premiere 2026, `AE.Impact_Blur_FX`) | ⚠️ the size property is **Amount**; scripts looking for "Blurriness" fail with `null is not an object` | Find properties by `displayName` "Amount" |
| Wonder Glow, Echo Glow, Edge Glow, VR Glow, Alpha Glow (new in 2026) | untested | Soft bloom: the V2 highlight-copy recipe (effects-playbook §A4) |
| `$.evalFile` on a missing or empty file | ⚠️ fails silently | Check the file exists and is non-empty before running it |

## Snippets

**Delete project items (temp bin):**
```javascript
var tmp = app.project.rootItem.createBin("_delete_me");
// for each item to delete: item.moveBin(tmp);
tmp.deleteBin();
```
Then confirm with `list_project_items`.

**Lumetri primary correction (per clip):**
1. One `color_correct` call with only `contrast`, `temperature` and `tint`. That creates the clip's single Lumetri.
2. Then use ExtendScript to set the rest by property **occurrence** inside that Lumetri, and write the values to the file per Rule 2:
   - Exposure is in **stops** (e.g. +0.5);
   - Highlights and Shadows;
   - Basic Saturation is **0–200** (100 = neutral);
   - set **Creative Saturation = 100**, or the clip may stay desaturated.

**Blend mode** (`clip.components["Opacity"].properties[1].setValue(n, true)`), alphabetical enum:

| Mode | n |
|---|---|
| Color | 0 |
| Color Burn | 1 |
| Color Dodge | 2 |
| Darken | 3 |
| Darker Color | 4 |
| Difference | 5 |
| Dissolve | 6 |
| Exclusion | 7 |
| Lighter Color | 12 |
| Multiply | 17 |
| **Normal** | **18** |
| **Overlay** | **19** |
| Pin Light | 20 |
| Saturation | 21 |
| **Screen** | **22** |
| **Soft Light** | **23** |

Verified by render: 6, 12, 18, 19, 23. The rest is inferred from alphabetical order.

**Transition at a cut (QE):**
```javascript
app.enableQE();
var tr = qe.project.getVideoTransitionByName("Cross Dissolve");  // or "Dip to Black", "Dip to White"
qe.project.getActiveSequence().getVideoTrackAt(t).getItemAt(k).addTransition(tr, true, "00;00;00;08"); // true = clip START, false = END
```
Check the result with `seq.videoTracks[t].transitions[j].start/end`. Remove a wrong one with `transitions[j].remove(true, true)`.
A transition shorter than asked means the clip had no handle on that side (see the table); say so rather than re-adding it.

**In-point read-back (every placed clip):** `setInPoint` + `overwriteClip` can land a frame early, and nothing reports it. Work in frames (`TPF` = ticks per frame = 254016000000 / fps):
```javascript
function T(fr) { var t = new Time(); t.ticks = String(Math.round(fr * TPF)); return t; }
function F(t) { return Math.round(t.ticks / TPF); }
item.setInPoint(T(src), 4); item.setOutPoint(T(src + dur), 4);
track.overwriteClip(item, T(f0)); item.clearInPoint(4); item.clearOutPoint(4);
var c = /* the track item now starting at frame f0 */;
if (F(c.inPoint) != src) { c.inPoint = T(src); c.start = T(f0); }
if (F(c.end) != f0 + dur) c.end = T(f0 + dur);
```
Verified on kolkata v6–v8 (`projects/kolkata/tools/swap_v7.py`).

**Audio level:**
- Premiere's clip Level is linear, with `0.17783` = 0 dB.
- `Level = 10^((dB − 15) / 20)`, so −16 dB → 0.0282.

**Export presets** (built in, since `get_encoder_presets` finds none):
- **The master (default since v0.8):** `/Applications/Adobe Premiere Pro 2026/Adobe Premiere Pro 2026.app/Contents/Settings/IngestPresets/Transcode/Match Source - Apple ProRes 422.epr` with `exportAsMediaDirect` (10-bit 4:2:2; used on uski and goddess). Then `scripts/encode_master.py` makes the H.264 deliverables and the phone copy.
- The H.264 presets below gave 9.2–9.5 Mb/s Main profile, which looked blocky on the iPhone. Use them only for a quick internal check:
- `/Applications/Adobe Premiere Pro 2026/Adobe Premiere Pro 2026.app/Contents/Settings/IngestPresets/Transcode/Match Source - H.264 High Bitrate.epr`
- `/Applications/Adobe Media Encoder 2026/Adobe Media Encoder 2026.app/Contents/MediaIO/systempresets/4E49434B_48323634/00 - Match Source - High bitrate.epr`

**After every export:**
```bash
ffmpeg -i renders/exports/<file>.mp4 -af volumedetect -vn -f null - 2>&1 | grep max_volume
```
- `max_volume` must be above −20 dB.
- If it isn't, the export is silent. Rebuild the audio with `scripts/mix_from_edl.py` and say so in the round notes.

**Adjustment layer (the one manual step).** Send the director exactly this:
1. In Premiere's Project panel: File → New → Adjustment Layer → OK (it uses the sequence settings).
2. Come back and say "done".

Then place it on V3 across the reel with `add_to_timeline`, and load the look by its route in the film table (effects-playbook §A3):
- a **preset** look by `applyLumetriPreset`;
- a **dropdown** look: the director picks it, in the same message as the adjustment layer when possible ("then on V3: Lumetri → Creative → Look → <name>").

Premiere 2026 has **no Leave Color** effect, and the Lumetri Hue vs Sat curve and tint wheels can't be set by script. Both are UI steps.
