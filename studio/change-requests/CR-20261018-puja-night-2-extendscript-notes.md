# CR-20261018-puja-night-2-extendscript-notes

| Field | Value |
|---|---|
| From reel | `projects/puja-night-2/` |
| Arch version | 0.5.0 |
| Type | skill (premiere-mcp-reality.md) |
| Severity | workaround |
| Status | open |

## What happened
Verified on Premiere 26.5.2 + MCP 1.2.9 during the puja-night-2 v1 build. Each cost a failed run or a silent mistake.
1. **Music placed 1 frame early.** `add_to_timeline_batch` with `sourceInPoint: 211.88` on an MP3 placed it at 211.84. `projectItem.setInPoint(<ticks or seconds>, 4)` was silently ignored for this audio-only item (`getInPoint()` stayed at 211.878 on the MP3's odd timebase; Premiere reports its fps as 2.75e-08). `setInPoint(211.88, 2)` (2 = audio) worked; then `track.overwriteClip(item, 0)` → readback 211.88–271.68.
2. **`File.write` wrote 0 bytes** when the JSON contained Lumetri property names with non-ASCII characters. Fix: `f.encoding = "UTF-8"` before `f.open("w")`.
3. **`in` / `out` as object keys** (`{in: …}`) are reserved words in ExtendScript (ES3); the whole `evalScript` fails with a generic "ExtendScript execution failed via CEP evalScript()".
4. **`color_correct` also writes its temperature/tint into Lumetri's HSL Secondary block** (property indices 101/102), not only Basic (14/15).
5. **Lumetri property index map** (one Lumetri Color, Premiere 26.5.2): 14 Temperature · 15 Tint · 16 Basic Saturation · 19 Exposure · 20 Contrast · 21 Highlights · 22 Shadows · 23 Whites · 24 Blacks · 34/35 Look · 38 Look Intensity · 40 Faded Film · 42 Vibrance · 43 Creative Saturation · 101/102 HSL-secondary Temperature/Tint · 110 Vignette Amount · 111 Midpoint · 112 Roundness · 113 Feather.
6. **Stills in one call:** 14 separate `export_frame` calls per colour check were slow. One ExtendScript loop with `qe.project.getActiveSequence().exportFramePNG("00;00;SS;FF", path)` exported all 14 in ~3 s.
7. **Scale keyframes on a trackItem take source (media) time:** `t.seconds = clip.inPoint.seconds + offset`, not sequence time.
8. **Running long scripts:** `execute_extendscript` with `$.evalFile(new File("<path>.jsx"))` keeps tool calls short and leaves the script in the reel's `analysis/` for reuse; `$.global.X = …` before `evalFile` passes parameters.

## Workaround used in the reel
All of the above, in `projects/puja-night-2/analysis/_es_*.jsx` (import, sequence, readback, music, Lumetri, look, grain, push, transitions, type, export, stills).

## Proposed change
Add items 1–8 to `.claude/skills/cinematic-reel/premiere-mcp-reality.md` (tool table + snippets), and add "read back the music clip's source in/out after placement" to skill Phase 3 step 4.

## Follow-up (same day, v1c)
9. **After `speed_change`**, a trackItem's `inPoint`/`outPoint` read back in speed-scaled time (source 2.80 at 93.68 % → `inPoint` 2.989), and `outPoint` did not refresh after setting `trackItem.end` (stayed at the pre-extension value although the clip now ends later). Verify such clips by render, not readback. `speed_change` keeps the timeline length; extending `end` afterwards then uses more source, up to the media end (C089: source 2.80 → 9.92).
10. **Optical flow** on a speed-changed clip: QE `item.setTimeInterpolationType(2)` returned without error (render looked clean at 93.7 %).
11. **Lumetri keyframes** work on property 19 (Exposure): `setTimeVarying(true)`, `addKey`, `setValueAtKey` in source time (used for a −0.5 → 0 exposure ramp on C100's bright head).
12. **Frame hold without a freeze-frame API:** `razor_timeline_at_time` (pass `videoTrackIndices:[0]`, `audioTrackIndices:[0]` so the music isn't cut) at both ends, then `speed_change {speed: 0.01}` on the middle piece holds its first frame for the piece's length (used to cover 4–7-frame source blur/focus breaths on static holds). `frame_scan.py` reports it as "frozen" (intended).
13. **Lumetri exposure keyframes on a speed-changed clip** (C101 at 91.25 %): keys at `inPoint` and `inPoint + 1.0` produced the intended ramp over ≈ 1 s of reel time (verified by per-frame luma on the export).

## Follow-up (round 4, v4c): trim in place and transition edits without remove + re-place
Verified on Premiere 26.5.2 by exported stills matched to source frames (NCC ≥ 0.98):
14. **`trackItem.inPoint` / `trackItem.outPoint` are writable.** Setting both on a placed clip changes the source range in place, keeping all effects, rotation and Lumetri (C130 → 3.00–4.28; C132 → 0.12–5.16 after `end` was extended). Order for an extension: `inPoint` → `end` → `outPoint`.
15. **`trackItem.start = t` trims the head** (the clip keeps its end), but `inPoint`/`outPoint` then **read back stale** (unchanged numbers). Set them explicitly afterwards and verify by still.
16. **Transitions can be removed:** DOM `track.transitions[k].remove(false,false)` removed a stale A1 crossfade and the A3 end fade (readback shows them gone). Add a new one with QE `item.addTransition(qe.project.getAudioTransitionByName("Exponential Fade"), false, "00;00;01;01")`. Exponential Fade gives an even dB slope; a Constant Power fade-out holds level to the last ~0.3 s.
17. **Frame Blending on a speed-changed clip:** QE `item.setTimeInterpolationType(1)` removed the repeated single frames of a 92.4 % retime (min frame diff ≈ 0 → 2.5). Optical flow (2) ghosted on C089.
18. **Overlay media changed on disk:** `projectItem.refreshMedia()` picks up a re-rendered `.mov` with the same frame count. Run it only after the render has finished (a refresh issued in parallel with the render kept the old frames).
19. **ProRes 4444 alpha from ffmpeg** (`prores_ks -profile:v 4444`, yuva444p12le) composites with less opacity than the file says: alpha 0.97 rendered as ≈ 0.87. Alpha 1.0 rendered as full. Use full-opacity cores for masks.

**Proposed addition to the reality doc:** a "trim in place" recipe (14–16) for review-loop fixes. This replaces the remove + re-place + re-apply cycle that cost ~15 min per loop (CR-20261018-puja-night-2-focus-qa).

## Follow-up (round 5, v5): building a 30-shot cut by script
20. **Lumetri without `color_correct`:** QE `qeItem.addVideoEffect(qe.project.getVideoEffectByName("Lumetri Color"))` adds exactly one Lumetri per clip (also "ASC CDL"); set values through the DOM afterwards. 30 clips in one call, with no `color_correct` side effects (HSL-secondary temp/tint still zeroed by habit).
21. **`add_track {position: "below"}` inserts at index 0** and shifts every audio track (A1 → A2 …). The `_IG` export, which mutes `audioTracks[2]`, would then have muted the SFX instead of the music. Use `position: "above"` (appends), then read the track list back.
22. **Frame-snapped placement:** `overwriteClip` at non-frame times snaps the start, and the end comes out one frame short of the next clip. Close gaps by setting each clip's `end` to the next clip's `start`, then read back.
23. **JSON is available** in Premiere's ExtendScript (`JSON.parse` of a UTF-8 file worked), so an EDL can be placed from a JSON file directly.

## Follow-up (round 6): Warp Stabilizer analysis
24. **QE `addVideoEffect("Warp Stabilizer")` never starts analysis.** Renders show "Click Analyze to begin". Setting Warp's unnamed boolean properties (index 0 / 1) doesn't start it, and the effect can't be removed by script, so the sequence had to be rebuilt.
25. **MCP `stabilize_clip` started analysis on only 7 of 25 clips in one pass** (both nests, plus C090, C095, C096, C101, C129). The other 18 stayed at "Click Analyze to begin" for 6+ minutes; no pattern found (all 4K 25p, some rotated, some keyed). Calling it again would stack a second Warp.
- **Proposed:**
  1. A reality-doc line: Warp needs the Analyze button for most clips when added by script, so plan a director click pass or full-screen control.
  2. Detect the banner before export: a blue band ≥ 60 % of the row width, B > R + 40.
  3. Upstream: ask the MCP server for a `warp_analyze` that presses the button (`studio/upstream/premiere-mcp-issues.md`).
26. **Placement default scale:** `track.overwriteClip(item, t)` places 4K clips at scale 100 % in a 1080 × 1920 sequence (2× zoom). Every placement helper must set the reel's base scale (50 % here) right after placing, then read it back.
27. **Warp side effects, verified on 26.5.2:**
    - smoothness set by script (100) can trigger the "To avoid extreme cropping set Framing to Stabilize Only…" error frame, which stays after setting it back;
    - Warp on a clip that is also reframed by Motion (62 %) produced a 2-frame vertical judder (velocity jitter 3.7 px/frame vs 0.2 in the source);
    - a dissolve over Warp clips renders the analysis banner during the transition (handles aren't analysed).
    - **Rule:** measure source jitter first and Warp only what needs it; never script smoothness above the default; no dissolves over Warp clips (bake the transition or use a dip).
28. **Nest-then-Warp makes reframes soft.** The skill's recipe for speed-changed clips (nest, then Warp the nest) renders the nest at the sequence size (1080 × 1920). Any reframe of the nest above 100 % is then an upscale: C132's nest at 128 % measured Laplacian 44 against 140–1000 on every other shot, and the blind reviewer flagged it as soft.
    - **Rule:** don't reframe a nest above 100 %. Reframe the 4K clip inside the nest, or skip Warp on a speed-changed clip whose source is steady enough (measure first).
29. **Optical Flow by script: QE `trackItem.setTimeInterpolationType(2)`** (verified on 26.5.2, readback `timeInterpolationType` = 2; 0 = frame sampling, 1 = frame blending presumably). The DOM TrackItem has no interpolation call, and MCP `set_time_interpolation` only calls QE `setFrameBlend(bool)` whatever mode is passed.
    - At 150 % speed, frame sampling steps 1-2-1-2 source frames (frame-difference cadence 0.24, velocity jitter 2.9 px). Optical Flow: cadence 0.11, jitter 0.6, no visible warping on people or lights.
    - Proposed: a reality-doc line, and an upstream note so `set_time_interpolation` calls `setTimeInterpolationType` with the requested mode.
