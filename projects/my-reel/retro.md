# Retro — written by the editor at the end of the reel

| Field | Value |
|---|---|
| Reel | my-reel (Durga Puja night, first pilot) |
| Reel type | music-montage |
| Arch version | 0.2.5 (HQ moved to 0.3.0 mid-reel; not adopted, no round followed) |
| Rounds to approval | 1 (brief, look, v1 cut and IG package all approved first time; 0 change notes) |
| Final runtime | 41.28 s · 20 shots · avg 2.04 s · median 1.76 s · first cut 2.24 s |

## What worked (keep doing)
- **Beat grid → EDL in reel time.** Converting `beats.json` to reel time (music start 61.88 s) and snapping every cut to a 25 fps frame produced an EDL that assembled in one `add_to_timeline_batch` call (21/21 placed, 0 gaps).
- **Two short interview rounds with concrete options.** Round 2 offered three timecoded music sections and three looks measured from the footage. The director picked the recommended option on 4 of 4 questions.
- **Analysing in the background.** The 77-clip analyser (~8 min) ran while Round 1 was being asked, so no time was lost.
- **Footage interpretation for frame-rate conform.** `set_override_frame_rate 25` on the 24 fps clips gave frame-for-frame playback, exact slot lengths and no gaps (CR filed).
- **Verifying by render, not by tool result.** Many tools returned `success` without doing the work, so every step was checked against an exported still (luma / saturation numbers plus a look by eye). This caught a black-and-white clip, a LUT that never loaded, misplaced transitions, a fade that didn't fade and a silent export.
- **ExtendScript → file → Bash.** Script results never come back, so scripts wrote `analysis/_es_out.txt` and I read it with Bash. This unblocked colour, blend modes, transitions and audio levels.
- **Asking the director for one manual click.** Asking for a single, numbered step (create an Adjustment Layer) was faster than fighting computer-use across macOS Spaces.

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
- Worked as documented: `verify_premiere_connection`, `list_sequences`, `add_to_timeline_batch`, `create_bin`, `duplicate_sequence`, `set_override_frame_rate`, `set_clip_rotation`, `remove_from_timeline`, `get_timeline_gaps`, `get_clip_properties`, `list_clip_effects`, `save_project`.
