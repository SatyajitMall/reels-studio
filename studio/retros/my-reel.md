# Retro — written by the editor at the end of the reel

| Field | Value |
|---|---|
| Reel | my-reel (Durga Puja night, first pilot) |
| Reel type | music-montage |
| Arch version | 0.2.5 for Round 1; 0.3.0 adopted at the start of Round 2 |
| Rounds to approval | 8 (v1 reopened with 7 notes → v2; shake → v3; crowd shot → v4; colour → v5; selects → v6; AE finishing → v7; upside-down clips, pan-in/out, transitions, visible AE looks → v8 final) |
| Final runtime | final v8 (v7 + rotated C023/C032, moves, transitions, rays/leaks/embers) · v3: 49.76 s · 21 shots · avg 2.61 s · median 2.2 s · slow open, first hit at 10.72 s (v1 was 41.28 s, avg 2.04 s) |

## What worked (keep doing)
- **Beat grid → EDL in reel time.** Converting `beats.json` to reel time (music start 61.88 s) and snapping every cut to a 25 fps frame produced an EDL that assembled in one `add_to_timeline_batch` call (21/21 placed, 0 gaps).
- **Two short interview rounds with concrete options.** Round 2 offered three timecoded music sections and three looks measured from the footage. The director picked the recommended option on 4 of 4 questions.
- **Analysing in the background.** The 77-clip analyser (~8 min) ran while Round 1 was being asked, so no time was lost.
- **Footage interpretation for frame-rate conform.** `set_override_frame_rate 25` on the 24 fps clips gave frame-for-frame playback, exact slot lengths and no gaps (CR filed).
- **Verifying by render, not by tool result.** Many tools returned `success` without doing the work, so every step was checked against an exported still (luma / saturation numbers plus a look by eye). This caught a black-and-white clip, a LUT that never loaded, misplaced transitions, a fade that didn't fade and a silent export.
- **ExtendScript → file → Bash.** Script results never come back, so scripts wrote `analysis/_es_out.txt` and I read it with Bash. This unblocked colour, blend modes, transitions and audio levels.
- **Asking the director for one manual click.** Asking for a single, numbered step (create an Adjustment Layer) was faster than fighting computer-use across macOS Spaces.

## Rounds 2–3: what the first cut got wrong
v1 was approved, then reopened. The director's notes are the most useful output of this pilot:
- **Too literal to the beat.** One shot per bar for 40 s felt mechanical. v2 added a tempo arc (slow open → up → down → outro) using the track's own sections; average shot 2.0 → 2.6 s.
- **Effects read as "jumps".** Impact shakes and a snap zoom on top of handheld footage looked like camera wobble. All removed; replaced by digital push/pull on static holds.
- **Kinetic words didn't mean anything** (DUM · DUM · DURGA · MAA · SHAKTI). Replaced by a title and an end card only.
- **No opening.** v2 used the 8.5 s beatless intro as a slow, titled opening before the first hit.
- **No slow motion / speed play.** v2 added Optical Flow slow-mo on 4 calm shots (25 fps footage) and 150–250 % speed-ups.
- **Grain too heavy** at 40 % → 12 %.
- **Handheld shake.** v3: frame-by-frame shake measurement and Warp Stabilizer on 13 shots (44–98 % less shake on 10).
- **Round 4: a filler shot read as random.** A 0.88 s crowd shot (C031) had been picked for "atmosphere" but didn't belong to the story (idols → craft). Every montage shot should belong to one of the brief's named groups; flag the odd one out at Checkpoint 1.
- **Round 5: the grade passed my checks but not the director's eye.** v1–v4 colour was checked only for mean luma per shot. Per-frame measurement found crushed blacks, a red-orange hue from the film look, magenta blues and shot-to-shot jumps. Colour QA needs hue, black/white levels and cast per shot, not just brightness.
- **Round 6: selects came from mid-frames, not from the footage.** v1's picks were made from one mid-frame per clip plus a few contact sheets. Scoring every second of all clips (sharpness, colour, contrast, shake, exposure) and reviewing the top unused moments found 5 clearly better shots (temple, spiral lattice, engraved ceiling, procession relief, diyas). Do this in Phase 1, before the EDL.
- **Round 7: After Effects finishing (studio v0.4.0).** Denoise −12…−29 % dark-area noise, one true eased speed ramp, Timewarp slow-mo, glow. Two Timewarp bugs (in-point offset; black tail when the source is pre-trimmed) found by checking frames, not trusting the render log; HQ fixed the first in v0.4.1. Glow brightens shots by 0.09–0.13 luma, so re-match exposure after every AE swap. Swapping clips in Premiere drops adjacent transitions.
- **Round 8: upside-down footage was thrown away.** 8 clips recorded inverted were rejected in Round 1 instead of rotated; one (C023) holds a top-6 % moment. Rotate, then score. Also: centred transitions on Warp-stabilised clips burn "New frames need analyzing" banners (align transitions to the non-Warp side); visible AE looks (light rays) built by reel script outside the round-trip — HQ asked for them to become proper ops instead.
- Lesson: for a `music-montage`, the brief should plan the energy arc and motion style, not just the beat grid, and handheld footage should be measured for shake before the cut, not after.

## Friction (from the friction log, ranked by time lost)
| # | Phase | What happened | Workaround | Time lost |
|---|---|---|---|---|
| 1 | P4 colour | `color_correct` dropped brightness/highlights/shadows; saturation −8 → 0, and it zeroed the Creative saturation → clip went B&W. `set_effect_property` only hits the first of Lumetri's 3 "Saturation" props | `color_correct` for contrast/temp/tint only, then a script to set Exposure (stops), Highlights, Shadows, Basic Sat (0–200) and Creative Sat = 100 by occurrence | ~25 min |
| 2 | P4 look | `add_adjustment_layer` made a transparent 1920×1080 PNG; no scripting API for adjustment layers; `apply_lut` reported success but loaded nothing | Director created the Adjustment Layer by hand; used `applyLumetriPreset("Fuji F125 Kodak 2393 (by Adobe)")` instead of the 2383 `.cube` | ~20 min + 1 manual step |
| 3 | P5 transitions | `add_transition` / `add_transition_to_clip` landed one clip off; opacity-keyframe fade didn't render | Removed via `transitions[i].remove()`; re-added with QE `addTransition(tr, atStart, dur)` (true = start); Dip to Black for fades; also faded the V4 grain, which shows as grey over black | ~15 min |
| 4 | P7 export | `exportAsMediaDirect` gave correct picture but silent audio with 2 presets; no user `.epr` for `export_sequence` | Rebuilt the mix with ffmpeg from the EDL (music + 9 SFX at timeline times/levels, limiter) and muxed it onto Premiere's picture | ~10 min |
| 5 | P1 project | `import_folder` failed 77/77; `import_media` ignored `binName`; `delete_*` reported deleted but removed nothing | `app.project.importFiles(paths,true,bin,false)`; temp bin + `deleteBin()` | ~8 min |
| 6 | P4 texture | `set_blend_mode` → `Illegal Parameter type`; blend enum undocumented | Mapped the enum by test renders (alphabetical: Normal 18, Overlay 19, Screen 22, Soft Light 23) | ~8 min |
| 7 | P1 analysis | No cross-clip overview; "underexposed" on 70/77 night clips; upside-down clips not flagged; beat summary mislabelled, no energy map | PIL mosaics; 2 s RMS energy curve (both fixed in v0.3.0) | ~8 min |
| 8 | P6 sound | `set_clip_volume {volumeDb:-16}` → Level 0 (silent) | Level = 10^((dB−15)/20) set by script | ~3 min |
| 9 | P5 ramp | `slip_edit` ignores `offset` (needs `deltaSeconds`); razor with `audioTrackIndices:[]` still cut all audio | Used `deltaSeconds`; the music split was harmless | ~3 min |
| 11 | R3 stabilise | Warp + Speed can't share a clip (banner burned into render); Warp on a 24→25 fps interpreted clip stuck at "New frames need analyzing"; `nest_clips` isn't a real nest; script can't remove the broken effect | Delete + rebuild the clip, `createSubsequence` nest, Warp the nest; scan exports for banners | ~25 min |
| 12 | R2 slow-mo | `set_time_interpolation optical_flow` set Frame Blending | QE `setTimeInterpolationType(2)` | ~3 min |
| 10 | P5 type | Anton / Bebas not installed | DIN Condensed Bold (macOS system font) rendered to PNG with PIL; first end-card position sat on Durga's face → moved above the crown | ~5 min |

## Change the studio (each one becomes a CR)
| # | Change | File / section | CR id |
|---|---|---|---|
| 1 | Overview mosaics, night-aware exposure read, upside-down flag | `scripts/analyze_footage.py`, skill Phase 1 | CR-20261016-my-reel-footage-overview (**done v0.3.0**) |
| 2 | Bar label fix, energy/section map, candidate cuts per length | `scripts/gemini_audio_and_beat_analyzer.py` | CR-20261016-my-reel-beat-summary (**done v0.3.0**) |
| 3 | Conform outlier frame rates by interpretation, not `speed_change` | CLAUDE.md §3, skill Phase 3 | CR-20261016-my-reel-conform-by-interpretation |
| 4 | Known-broken import/delete/script-return tools + workaround snippets | CLAUDE.md §2 / premiere-pro-mcp skill, skill Phase 1 | CR-20261016-my-reel-mcp-import-delete |
| 5 | Lumetri units + recipe, adjustment layer as a manual/template item, built-in look fallback for LUTs, blend-mode enum | playbook §A1/§A3/§A4, skill Phase 4, `_template` | CR-20261016-my-reel-color-tools |
| 6 | QE transition snippet, volume formula, shipped `.epr`, post-export audio check, `mix_from_edl.py` fallback | playbook §D/§F, skill Phase 7, `assets/presets/`, `scripts/` | CR-20261016-my-reel-transitions-export |
| 8 | Montage craft defaults: plan a tempo arc from the energy table, measure pans/holds (`motion.json`) and shake before cutting, Warp handheld moving shots by default, no impact shakes on handheld, title + end card over beat words unless asked, grain ≤ 15 % | skill Phase 1–5, playbook §B/§C/§E, `scripts/` (motion + shake analysers) | CR-20261016-my-reel-montage-craft |
| 7 | Playbook notes from the pilot: fade V4 grain with the picture; speed-ramp recipe as this MCP behaves; PIL type recipe + system font fallback; keep end cards off the subject | playbook §A4/§C/§E, skill Phase 5 | CR-20261016-my-reel-playbook-pilot-notes |

## Director's notes pattern
- **Approves the recommended option when the options are concrete and measured.** 4/4 in Round 2; brief, look, cut and package all approved without changes. Default: always lead with a recommendation backed by numbers.
- **Wants plain "what do I do" steps for any manual action.** They asked twice ("What are the current issues…", "what do I do?"). Every manual step should go out as a short numbered list naming the panel/menu, with "come back and say done".
- **Branding came late and in fragments** (the handle only arrived after being asked twice; font confirmed separately). Ask for handle / font / colours in Round 1, not Round 2.
- **"Build every effect from the footage, no outside stock."** Likely a standing preference; record it as a default in the brief.
- Will check beat timing by ear themselves; offer that as a review step instead of asking.

## Tool reality check
- `color_correct`: only contrast / temperature / tint are written; saturation clamps to 0 and the Creative saturation is zeroed (B&W). Lumetri Exposure is in stops; Basic Saturation 0–200 (100 = neutral).
- `set_effect_property`: first property matching the name only (Lumetri has 3 "Saturation", 2 "Intensity", 2 "Contrast").
- `add_adjustment_layer`: transparent PNG, not an adjustment layer. No ExtendScript API for one.
- `apply_lut`: reports success, loads nothing. `app.project.applyLumetriPreset(name)` works on selected clips (325 built-in presets via `getAllLumetriPresetsList()`), and adds its own Lumetri.
- `set_blend_mode`: `Illegal Parameter type`. Blend Mode = `Opacity.properties[1]`, alphabetical enum 0–27.
- `add_transition` / `add_transition_to_clip`: off-by-one placement, `accepted_unverified`. QE `addTransition(tr, true)` = clip START.
- `set_clip_volume`: `volumeDb` writes a linear 0 (silent). Level = 10^((dB−15)/20).
- `slip_edit`: param is `deltaSeconds`.
- `razor_timeline_at_time`: `audioTrackIndices: []` means all audio tracks.
- `speed_change` 2.0: keeps the timeline duration and doubles the source span (good for ramps, the opposite of the playbook's assumption).
- `import_folder`: broken (`targetBin.importFiles is not a function`). `import_media`: ignores `binName`.
- `delete_multiple_project_items`: crashes; `delete_project_item` on footage: false success.
- `execute_extendscript` / `evaluate_expression`: always return `"undefined"`.
- `export_frame`: fails with `format:"png"`, works without it.
- `exportAsMediaDirect`: silent audio in this project (cause unknown; the director to check whether the timeline plays sound).
- `get_encoder_presets`: finds no factory presets. Built-in ones live under `…/Adobe Premiere Pro 2026.app/Contents/Settings/IngestPresets/Transcode/` and `…/Adobe Media Encoder 2026.app/Contents/MediaIO/systempresets/4E49434B_48323634/`.
- `create_sequence` needs an `.sqpreset`; `create_sequence_from_clips` on a clip with the target size and fps works.
- `stabilize_clip` (Warp): works on 100 % clips; burns a banner on speed-changed clips; failed on a 24→25 fps interpreted clip until nested. `createSubsequence(false)` (with in/out + V1-only targeting) is the working nest.
- `set_time_interpolation`: optical_flow → Frame Blending; use QE `setTimeInterpolationType(2)`.
- Worked as documented: `verify_premiere_connection`, `list_sequences`, `add_to_timeline_batch`, `create_bin`, `duplicate_sequence`, `set_override_frame_rate`, `set_clip_rotation`, `remove_from_timeline`, `get_timeline_gaps`, `get_clip_properties`, `list_clip_effects`, `save_project`.

## Round 9 addendum (v9, 2026-10-17)
- **Taste fail on an approved version.** The director approved v8, then called its AE looks (leaks, rays, embers, Light Leaks transitions) "cringe and less production grade". Lesson: on handheld night footage, cinema grade means restraint. Judge every added look by eye at 100 % and in motion, never by luma alone. → CR-20261017-my-reel-qa-visual-review.
- **QA was metric-only.** A C073 smear had been in every version since v6: Warp hid the shake, and selects scored mean sharpness, never the worst frame. Now every export gets a scan (repeats, luma jumps, blur dips, beats; `analysis/qa_scan.py`) plus a written per-shot report, before the director sees it.
- **The QA itself needed QA.** The v8 report blamed C055's softness on the leak; the v9 rescan proved it was the 120 % push. Re-scan after every fix and correct the earlier report in writing.
- **`replace_clip` is destructive** (overwrites neighbours, adds audio, drops transitions and Motion keys). Swap by script. → follow-up in CR-20261016-my-reel-mcp-import-delete.
- **Final: v9** (`renders/exports/my-reel_v9_mix.mp4`), approved 2026-10-17 after 9 rounds.
- **Review gate on v9 (after approval):** FAIL with 4 majors my own written QA had passed (C058 phone, C011/C032 smear, C055 focus). Even with written reasoning, an editor misses its own defects. Run the blind gate before every hand-off.

## Round 10 addendum (v10, approved final 2026-10-18)
- **The gate works, and loops are needed.** The blind review failed v10 twice (3 majors, then 2) before it passed. Each loop caught real defects, including two I introduced myself:
  - easing C023's zoom uncovered a phone;
  - cropping C032 enlarged its blur.

  Re-check the neighbouring problem every time you change a frame.
- **Metrics have blind spots:**
  - Laplacian sharpness misses one-directional motion smear: C011 rated 1.12 while visibly streaked. → CR-20261017-my-reel-directional-blur-scan.
  - frame_scan skips blur that straddles a cut.
- **Some clips have no good window.** C011 (smeared wherever Durga is in frame) and C032 (fast pan + crowd) had to be replaced, not trimmed. Score candidates on worst frame, directional blur *and* people at the frame edge before choosing.
- **Upside-down clips:** check the script on signage/engravings to confirm the rotation (C016's Bengali reads upright only when rotated).
- **Final: v10** (`renders/exports/my-reel_v10_mix.mp4`), 10 rounds.
