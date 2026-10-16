# Project Log

| Field | Value |
|---|---|
| Reel name | my-reel |
| Status | proposal |
| Reel type | music-montage |
| Arch version | 0.3.0 |
| Pilot | yes |
| Current round | 2 |
| Premiere project | projects/my-reel/my-reel.prproj |
| Latest sequence | Reel_my-reel_v1 (9038708e-343c-4499-b53f-34eeb9914710) |
| Latest export | renders/exports/my-reel_v1_mix.mp4 (41.28 s, 1080×1920, 25 fps, H.264 10 Mbps, AAC 320k, −11.1 LUFS, peak −1.3 dBFS) |

## Approved decisions
- Hook: #1 blue reveal (C010) → gold hit (C077) on accent 2.23 s
- Target runtime: 41.27 s
- Grade / LUT: Gold & Shadow — gemini_warm_film_2383.cube 50 % on V3, grain 40 % on V4
- Caption style: kinetic beat words DUM · DUM · DURGA · MAA · SHAKTI (English), Anton/Bebas-style bold condensed, end card DURGA PUJA 2026 + @satyajitmall
- Music: Dum Durga 61.88 → 103.15 s

## Round 1 — Interview (2026-10-16)
- Reel type: **music-montage** (no speech; Dum Durga drives cuts).
- End feeling: goosebumps / pride.
- Audience: filmmaker / creator crowd (craft-forward: grade, cuts, motion).
- Length: 30–45 s.
- Reference: `references/ref1-filmmakerguy.mp4` (@the.filmmaker.guy, 21.6 s).
- Premiere: bridge connected (26.5.2). Project holds 17 Adobe sample clips + auto `Sequence 01` (1920×1080) — ask director before removing.

## Round 2 — Interview (2026-10-16)
- Music: Dum Durga **61.88 → 103.15 s** (41.27 s, natural outro).
- Look: **Gold & Shadow** (Warm Film LUT 50 %, deep blacks, sat −15, vignette, 16mm grain 40 %).
- Text: **kinetic beat words** on accents.
- Effects: **signature moments only**; no fake slow-mo.

### Reference → parameters
- ref1: 8 cuts, avg 2.41 s, median 1.6 s, first cut 7.1 s (thresholds 0.15 and 0.1 agree, per v0.2.4). Dark, beam-lit, gold serif text, cool grade.
- Ours: one shot per bar (1.765 s @136 BPM) ≈ ref median; accents cut harder; grade stays gold (footage is warm), blue only on C010/C011.

### Footage facts
- 77 clips, 1080×1920, Rec.709 8-bit HEVC. 65 × 25 fps, 12 × 24 fps (C001–C012) → **25 fps sequence**; 24 fps clips conformed with `speed_change` 104.17 %.
- No slow-mo headroom anywhere.
- Mostly 1–2 stops under (median exposure ≈ 0.23), warm, very saturated. Unusable dark: C001, C002, C025, C042, C049–C053.
- Recorded upside down (all clips carry the same −90° rotation tag, so these were shot inverted): C008, C018, C022, C023, C032; HQ overview sheets (v0.3.0) also flag C014, C015, C020; C016 found in rough cut (rotated). None of C014/C015/C020 is in the EDL.

## Round 1 — Proposal
Music time = reel time + 61.88 s. Grid: downbeats (every 4th beat) at reel 0, 1.79, 3.55, 5.32, 7.08, 8.85, 10.61, 12.38, 14.14, 15.91, 17.67, 19.44, 21.20, 22.97, 24.71, 26.47, 28.24, 30.00, 31.74, 33.53, 35.27; accents at 2.23, 4.44, 7.08, 9.73, 31.74; last beat 36.15; track ends 41.27.

### Hook options
1. **(Recommended) Blue reveal → gold hit.** C010 src 0.30 s, tilt-down from blue chandelier to Durga with slow push; hard cut on accent 64.11 (reel 2.23) to C077 src 7.60 gold Durga, snap zoom + "DUM" + bass drop. Cool→gold jump is the hook.
2. **Push-in → hit.** C003 src 0.60, camera zooms from wide hall into the white goddess (0–2.23); hard cut on 2.23 to C077.
3. **Text → roar.** C076 src 0.80 "SHAKTI STAMBHA" lettering tracking; cut on 2.23 to C072 Narasimha roar with impact shake.

### EDL (25 fps; 24 fps sources marked *, conformed at 104.17 %)
| # | reel in–out | clip | src in | src out | text / action | V1 move | V5 | transition out | SFX (A2) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.00–2.23 | C010* | 0.30 | 2.62 | tilt-down reveal | slow push 100→106 | — | cut | riser @1.23 |
| 2 | 2.23–4.44 | C077 | 7.60 | 9.81 | accent 1 | snap zoom 100→118 / 5 fr | DUM | flash (dip white 3 fr) | bass drop @2.23 |
| 3 | 4.44–7.08 | C003* | 4.10 | 6.85 | accent 2 | camera zoom (native) | DUM | cut | shutter @4.44, pop |
| 4 | 7.08–9.73 | C058 | 2.60 | 5.25 | accent 3 | impact shake 6 fr | DURGA | cut | swish @7.08, pop |
| 5 | 9.73–12.38 | C044 | 1.00 | 3.65 | accent 4 | slow push 100→105 | MAA | cut | pop |
| 6 | 12.38–14.14 | C006* | 1.00 | 2.83 | diya arcade | native dolly | — | cut | — |
| 7 | 14.14–15.91 | C029 | 0.20 | 1.97 | temple | native tilt | — | cut | — |
| 8 | 15.91–17.67 | C031 | 2.60 | 4.37 | lantern street | native | — | cut | — |
| 9 | 17.67–19.44 | C034 | 0.30 | 2.07 | bamboo figure | slow push | — | cut | — |
| 10 | 19.44–21.20 | C041 | 2.00 | 3.76 | wide pandal | — | — | whip out (5 fr) | whoosh @21.20 |
| 11 | 21.20–22.97 | C046 | 0.20 | 1.97 | yellow Tel wall | whip in (5 fr) | — | cut | — |
| 12 | 22.97–24.71 | C056 | 1.00 | 2.74 | gold lattice | native | — | cut | — |
| 13 | 24.71–26.47 | C068 | 1.00 | 2.76 | glowing panels track | native | — | cut | — |
| 14 | 26.47–28.24 | C064 | 4.30 | 6.07 | pillars | native | — | cut | — |
| 15 | 28.24–29.12 | C016 | 3.20 | 4.08 | flurry (2 beats) | — | — | cut | — |
| 16 | 29.12–30.00 | C074 | 9.00 | 9.88 | flurry (2 beats) | — | — | cut | — |
| 17 | 30.00–31.74 | C076 | 0.80 | 3.41 | SHAKTI STAMBHA text | ramp 200 %→100 % | — | flash (dip white 3 fr) | riser tail |
| 18 | 31.74–33.53 | C072 | 0.60 | 2.39 | accent 5, roar | impact shake | SHAKTI | cut | shutter + bass drop @31.74 |
| 19 | 33.53–36.15 | C076 | 16.00 | 18.62 | push into gold idols | native push | — | cut on last beat | — |
| 20 | 36.15–41.27 | C011* | 0.80 | 6.13 | outro hold | slow push 100→108 | DURGA PUJA 2026 + handle @37.0 | fade to black 0.5 s | — |

**Runtime: 41.27 s · 20 shots · avg 2.06 s · median 1.77 s.**

## Round 1 — Director notes (2026-10-16)
- Approved. Hook 1, words as proposed. Remove the Adobe sample media. Handle left blank → ask again before the end card.

## Round 1 — Rough cut (2026-10-16)
- Sample media removed (17 clips + `Sequence 01`). Bins: 02_B-Roll (77), 04_Textures, 05_SFX (6), 06_Music, 03_Graphics. No 01_A-Roll (no A-roll).
- `Reel_my-reel_v1`: 1080×1920, 25 fps (created from C077), 20 clips on V1 per EDL, music on A3 (src 61.84–103.12), no linked clip audio (A1 empty = nat sound muted). Duration 41.28 s, 0 gaps (`get_timeline_gaps`).
- 24 fps conform done by **interpretation** (`set_override_frame_rate` 25 on C003, C006, C010, C011) instead of `speed_change`; source in-points scaled ×0.96. Plays frame-for-frame, no gaps.
- Music in-point quantised by Premiere to 61.84 (−40 ms, 1 frame) → every cut sits ≤ 1 frame before its beat; acceptable, re-check by ear.
- C016 recorded upside down → Motion rotation 180°.
- Stills at 1.6 / 3 / 28.6 / 38 s checked: content matches EDL. C011 (outro) has Durga left of centre → reframe in Phase 5.
- Not yet: speed ramp (#17), moves, colour, text, SFX. Saved.

## Round 1 — Director notes 2 (2026-10-16)
- Handle: **@satyajitmall** (branding, remember).
- Go ahead with colour.
- Director will check beat timing by ear at review.
- Font: bold condensed (Anton / Bebas style) confirmed.
- All pans / zooms / effects must be built from the existing footage (no outside stock).

## Round 1 — Colour (2026-10-16, in progress)
- Backup: `Reel_my-reel_v1_roughcut_backup` (697b61e3…).
- **A1 primary:** one Lumetri per V1 clip (20). Values (Exposure stops / Contrast / Highlights / Shadows / Basic Sat / Temp / Tint):
  C010 0.6/10/−10/10/92/0/−5 · C077 0.9/12/−10/10/88/−5 · C003 0.6/12/−10/5/88/−5 · C058 −0.3/10/−15/5/88/−8 · C044 2.2/10/−5/20/90 · C006 0.5/10/−15/5/88 · C029 0.3/10/−15/5/88/−8 · C031 0.4/10/−15/5/88 · C034 0.5/10/−10/5/92 · C041 2.0/10/−10/20/92 · C046 −1.2/5/−30/0/80/−10 · C056 0.05/10/−20/0/90 · C068 0.3/10/−20/5/88 · C064 0.3/10/−15/5/90 · C016 0.4/10/−15/5/88 · C074 0.6/12/−10/10/90 · C076 0.6/12/−10/10/88 · C072 −0.5/10/−25/0/88 · C076b −0.4/12/−10/10/88 · C011 0.6/10/−10/10/92/0/−5. Creative-section Saturation reset to 100 on all.
- **A2 match:** frame-mean luma now 0.25–0.36 across the reel (idol run 0.26–0.35); blue clips C010/C011 0.25/0.26.
- **A4 texture:** V4 = 9 × `gemini_film_grain_16mm.mp4` (interpreted 25 fps, 4.8 s loops, last trimmed to 41.28), Overlay (enum 19), 40 %.
- **A3 look: done.** Director created the Adjustment Layer (manual step). Placed on V3 0–41.28 (clip 000f42e9).
  - `apply_lut` with `gemini_warm_film_2383.cube` reported success but changed nothing (Input LUT/Look stay empty) → left an inert default Lumetri on the layer (can't be removed by script).
  - Used Premiere's built-in **"Fuji F125 Kodak 2393 (by Adobe)"** film-print look instead (`app.project.applyLumetriPreset` on the selected layer) — same Kodak print-film family as the brief's 2383 LUT. On that Lumetri: Look intensity 50, Contrast +15, Saturation 85, Shadows −10, Vignette −1.0.
  - Result: mean luma 0.16–0.29, p02 ≈ 0 (deep blacks), gold richer, blue clips shift teal-violet. Before/after: `renders/stills/look_before_after.jpg`.
- Extra unused project items: a 2nd "Adjustment Layer" (000f42e7, from my menu attempt) and the bogus PNG (000f42db). Left in place (can't delete footage items by script); harmless.
- Tracks: V5 (idx 4) added for type. Saved.

- HQ note 2026-10-16: studio now v0.3.0 (CR footage-overview + beat-summary applied). Minor bump → adopt at start of next round; CRs conform-by-interpretation and mcp-import-delete await director decision, keep workarounds.

## Round 1 — Director notes 3 (2026-10-16)
- Look approved (Kodak 2393 preset substitute OK). Go ahead with motion, speed ramp, kinetic words, end card, SFX.

## Round 1 — Motion, effects, type, SFX (2026-10-16)
- **V1 moves (keyframed by script):** C010 push 100→106 · C077 snap zoom 100→118 in 5 fr then drift to 121 · C058 + C072 impact shake ±12 px decaying over 6 fr (scale 103 to hide edges) · C044 push 100→105 · C034 push 100→104 · C011 outro push 115→138 with pan x 0.575→0.34 so Durga lands centred under the end card (the take pans: Durga enters ~1.8 s into the outro, a reveal).
- **Speed ramp #17:** razored C076 at 30.88; first half `speed_change` 2.0 (src 0.76–2.52 in 0.88 s), second half slipped +0.88 (src 2.52–3.40 at 1×). 0 gaps. Note: razor also cut A3 music at 30.88 (continuous, no audible effect).
- **Transitions:** Dip to White 3 fr at 4.32–4.44 and 31.64–31.76 · Whip 5 fr at 21.0–21.2 · Dip to Black 12 fr at 40.8–41.28 on V1 + V4 grain (+ end card). Verified by transition list and renders (flash luma 0.96, last frame 0.02).
- **V5 type:** PNGs from PIL in DIN Condensed Bold (macOS system font; Anton/Bebas style), cream #F5E6C8 with gold glow + soft shadow, `renders/overlays/`. DUM 2.24–4.32 · DUM 4.44–6.60 · DURGA 7.08–9.40 · MAA 9.72–11.40 · SHAKTI 31.76–33.40, each pop-in scale 120→100 over 3 fr. End card "DURGA PUJA 2026 / @satyajitmall" 37.0–41.28 at y 340/452 (above Durga's crown), cross-dissolve in 10 fr, dip to black out. All inside safe zone (x ≤ 929, y ≥ 265).
- **SFX:** A2 riser 1.24 (hit at 2.24) −16 · shutter 4.36 −16 · swish 7.04 −16 · pop 9.72 −18 · whoosh 20.92 −16 · shutter 31.68 −16 · pop 37.0 −18; A4 (new SFX2 track) bass drop 2.24 and 31.76 −14. Music A3 0 dB (section peak −2.1 dB).
- **Export:** Premiere `exportAsMediaDirect` (preset "Match Source - H.264 High Bitrate") → picture correct but **audio silent** (−91 dB), also with AME "00 - Match Source - High bitrate". All tracks unmuted, levels correct by script. → Workaround: same mix rebuilt with ffmpeg (music 61.84–103.12 + 9 SFX at their timeline times/levels, limiter −1 dB) muxed onto Premiere's picture → `my-reel_v1_mix.mp4`. Premiere-only file kept as `my-reel_v1_premiere_noaudio.mp4`.
- **QA:** analyser on export: 31 detected cuts (incl. flashes/type), avg 2.04 s, median 1.76 s, first cut 2.24 s; contact sheet `analysis/export_v1/`. Watch-outs: C074 shows signage text at top ("…temple at Aska… her worship"); C011 opens on pillar before Durga pans in.

## Round 1 — Director notes 4 (2026-10-16)
- **v1 approved** (`my-reel_v1_mix.mp4`). Go ahead with the Instagram package.

## Wrap-up (2026-10-16)
- Package approved (hook 1). Retro: `retro.md` → copied to `studio/retros/my-reel.md`. 7 CRs total (2 done v0.3.0, 5 open incl. new CR-20261016-my-reel-playbook-pilot-notes).

## Round 2 — Director notes (2026-10-16, on v1)
1. v1 "fair", but too much jump / shake → remove impact shakes, soften snap zoom.
2. Too much grain texture → much lighter.
3. No slow motion / speed play → add slow-mo and speed ramps for a cinematic feel.
4. Where a clip pans left/right then holds ~2 s: use the hold section and do a digital pan-in / pan-out (push or pull) on it.
5. Overlay text "very bad, does not make sense" → replace DUM · DUM · DURGA · MAA · SHAKTI.
6. No basic opening → build a proper opening.
7. Wants cinematic tempo through the video, with ups and downs (not one shot per bar throughout).

### Round 2 — Interview answers
- Text: **title + end card only** (no words during the montage).
- Opening: **slow build on the track's intro** (2–3 long wides, slow pushes, title fades in, then the first hit). Reel ~45–50 s.
- Slow-mo: **yes, Optical Flow 50–60 % on 4–5 calm shots**, plus fast→slow ramps into hits; check every frame for warping.
- Arch: adopting v0.3.0 (minor) at the start of Round 2.

## Friction log
<!-- Pilot reels: one line each time something is slow, fails, needs a guess, a manual step or a workaround. Format: `- [phase] what happened → workaround → CR filed? (CR id / no)` -->
- [P1] `analyze_footage.py` on 77 clips took ~8 min; ran in background while Round 1 was asked → fine, no CR.
- [P1] 77 per-clip `contact.png` files, no cross-clip overview; choosing heroes needed a mosaic → built mid-frame + contact mosaics in scratchpad with PIL (ffmpeg here has no `drawtext`) → CR-20261016-my-reel-footage-overview.
- [P1] Analyser "Read" column grades night footage against a talking-head norm (0.40–0.50), so 70/77 clips say "underexposed"; doesn't flag clips shot upside down (C008, C018, C022, C023, C032 found by eye) → CR-20261016-my-reel-footage-overview.
- [P1] `audio_summary.md` labels every-4th-beat times as "4-Bar Downbeats" (they're 1 bar apart, 1.765 s); no beats before 12.49 s or after 98.03 s and no energy/section map; empty dialogue table printed for music-montage → computed a 2 s RMS energy curve myself to find intro/lift/breakdown/outro → CR-20261016-my-reel-beat-summary.
- [P1] `delete_multiple_project_items` → `deleteResults.filter is not a function`; `delete_project_item` returned `deleted:true, method:deleteBin` for 17 footage items but removed nothing → moved them into a temp bin with `execute_extendscript` and `deleteBin()` on it → CR-20261016-my-reel-mcp-import-delete.
- [P1] `import_folder` → `ReferenceError: targetBin.importFiles is not a function` (77/77); `import_media` ignores `binName` (landed in root) → `app.project.importFiles(paths,true,bin,false)` via `execute_extendscript`, then `moveBin` → CR-20261016-my-reel-mcp-import-delete.
- [P1] `execute_extendscript` / `evaluate_expression` return `"undefined"` for any script result → verify with `list_project_items` instead → same CR.
- [P3] No 1080×1920 25 fps `.sqpreset` for `create_sequence` → `create_sequence_from_clips` on a 25 fps 9:16 clip, then lifted the clip → no CR (works).
- [P3] Conform rule says `speed_change`; that shortens clips after placement and opens gaps → used footage interpretation 25 fps instead (cleaner, exact) → CR-20261016-my-reel-conform-by-interpretation.
- [P3] `export_frame` with `format:"png"` → `Illegal Parameter type`; works without `format` → noted in mcp CR.
- [P4] `color_correct` only writes contrast/temperature/tint. `brightness`, `highlights`, `shadows` are dropped; `saturation:-8` was clamped to 0 **and** it zeroes the Creative-section Saturation → clip went black & white → set Exposure/Highlights/Shadows/Saturation by script on the same Lumetri (2nd "Saturation" = Creative → 100) → CR-20261016-my-reel-color-tools.
- [P4] `set_effect_property` picks the first property with a given name; Lumetri has 3 "Saturation"s → for duplicates, use `execute_extendscript` with occurrence index → same CR.
- [P4] `add_adjustment_layer` makes a transparent 1920×1080 PNG, 5 s, in /tmp — not an adjustment layer; a grade on it affects nothing → removed. ExtendScript has no adjustment-layer API; `app_menu` File > New > Adjustment Layer didn't open a usable dialog (Premiere on another Space) → asked director for 1 manual click → same CR.
- [P4] `set_blend_mode` → `Illegal Parameter type`. Blend Mode enum is alphabetical (Normal 18, Overlay 19, Soft Light 23, Screen 22) — mapped by test renders → set by script → same CR.
- [P4] `apply_lut` → success but no LUT loaded on the Lumetri (frame unchanged) → `applyLumetriPreset` with Adobe's Kodak 2393 look; a custom .cube can't be loaded by script → same CR.
- [P4] Script return values never come back → scripts write `analysis/_es_out.txt` via `File` and I read it → same CR.
- [P5] `add_transition(clip1,clip2)` and `add_transition_to_clip(clip, end)` place the transition one clip late/early (off-by-one in QE item index) and report `accepted_unverified` → removed via `track.transitions[i].remove()`, re-added with QE `item.addTransition(tr, atStart:bool, "00;00;00;12")` (2nd arg true = START, false = END) → CR-20261016-my-reel-transitions-export.
- [P5] Opacity keyframes on a 25-fps-interpreted 24 fps clip (C011) didn't render (fade stayed flat) → used Dip to Black transitions instead → same CR.
- [P5] `slip_edit` needs `deltaSeconds` (not `offset`; wrong key silently does nothing) → same CR.
- [P6] `set_clip_volume {volumeDb:-16}` set Level to 0 (= −∞, silent). Premiere Level is linear, 0.17783 = 0 dB, dB = 20·log10(v)+15 → set by script → same CR.
- [P7] No user .epr presets; `export_sequence` needs one → `exportAsMediaDirect` with Premiere's built-in Match Source H.264 preset. Export audio silent (2 presets) though timeline audio state is correct → ffmpeg remix + mux. **Director: please check whether the timeline plays sound in Premiere.** → same CR.
- [P0] Round 1 asked 4 of 5 questions in one AskUserQuestion (tool max 4); reference already supplied, so skipped Q5. Sample-media removal question deferred to Checkpoint 1 → no CR.

<!-- The editor appends one section per round below: "## Round N — Proposal", "## Round N — Director notes", "## Round N — Changes made". -->

## Instagram package
<!-- Filled in after final approval. -->
**Status:** approved 2026-10-16 with hook 1. Not published (director posts).

**First-line hooks (≤ 125 chars)**
1. (Recommended, IG1 Number-First → saves/follows) "77 clips from one Durga Puja night. 41 seconds. Every cut lands on the beat of Dum Durga." (89)
2. "Four goddesses, four drum hits. One night of Durga Puja 2026, shot on an iPhone 17." (83)
3. "Shot on an iPhone 17 after dark, graded like Kodak film: Durga Puja 2026 in 41 seconds." (87)

**Caption (hook 1; 791 chars, 0 em dashes)**
```
77 clips from one Durga Puja night. 41 seconds. Every cut lands on the beat of Dum Durga.

Four idols open it, one on each drum hit: DUM, DUM, DURGA, MAA.

Then the craft. Diya-lined arcades, a temple facade lit gold, bamboo figures against the night sky, the oil-market installation, the Kaalrekha pillars and the Shakti Stambha.

For the filmmakers, how it was made:
Shot after dark on iPhone 17 with the Blackmagic Cam app, 25 fps.
Cut to a 136 BPM grid, one shot per bar, hard cuts on the accents.
Graded warm with a Kodak 2393 film-print look, 16mm grain on top.

Save this if you're shooting a pandal this Puja. More cinematic Puja edits on @satyajitmall.

Music: Dum Durga by InhaleExhaleStudio (Pixabay)

#durgapuja2026 #pandalhopping #shotoniphone17 #iphonecinematography #durgapuja
```

**Hashtags (5, sized):** #durgapuja2026 (niche/mid, seasonal) · #pandalhopping (mid) · #shotoniphone17 (niche) · #iphonecinematography (mid) · #durgapuja (broad label). Post at end of caption or as first comment.

**Cover frame:** 00:00:03:00 (gold Durga C077 with "DUM", inside the 4:5 grid crop). Alt: 00:00:39:00 (blue Durga + end card).

**Media to attach:** `renders/exports/my-reel_v1_mix.mp4`.

Notes: no city/pandal names used (not confirmed by director); facts only from the footage, signage and the edit. Music credit included (Pixabay licence). Skills applied: ig-caption-writer (IG1), hashtag recipe from hashtag-strategy.md, humanizer rules (no AI-vocab clusters, no em dashes, no bait CTA); voice profile not filled.
