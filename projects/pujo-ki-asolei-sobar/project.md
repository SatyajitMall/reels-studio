# Project Log

| Field | Value |
|---|---|
| Reel name | pujo-ki-asolei-sobar |
| Working title | "Pujo ki Asolei Sobar" (Is Pujo really for everyone?). On screen: **PUJO KI ASOLEI SOBAR?** (romanised Bangla only) |
| Status | **ready to share** on the director's phone (IG Share screen): v19 + Jaago 17 % / 3 s fade-out, cover A1, caption with the 'Durga Puja' keyword + AI credit line, original 5 hashtags. Not yet posted (an earlier log line misread the director's 'done, publish it' as already posted) |
| Reel type | hybrid (external VO + bed from the reference; was music-montage until the reference arrived) |
| Arch version | 0.5.3 |
| Pilot | yes |
| Current round | 14 (posting: cover, own VO) |
| Premiere project | `premiere/pujo-ki-asolei-sobar.prproj` (created 2026-10-19 19:32; puja-night-2.prproj is still open alongside, untouched) |
| Latest sequence | `Reel_pujo-ki-asolei-sobar_v13` (bfd7d6ba-ebfc-49c4-8e7f-4763d0fec0b0); all earlier versions kept |
| Latest export | **`renders/exports/pujo-ki-asolei-sobar_v19_IG.mp4`** (upload; copied to `deliver/`), 35.80 s, 1074 frames. v18 (director's own VO) kept as a fallback |

## Approved decisions
- Hook: aarti opening (C152) + title; IG first line = hook 1 (approved 2026-10-21). Earlier: Devi/aarti montage M1–M5 (C152 priest's aarti → C161 → C152 close → C208 → C190), title PUJO KI ASOLEI SOBAR? 0.3–2.1 s (v1d, approved 2026-10-19)
- Target runtime: 35.82 s (the full reference audio)
- Grade / LUT: **v3 warm cinematic look** matched to the director's Bangkok film reference (sepia dropped in round 3). Earlier: **v1g sepia film look, baked per shot** (per-shot neutral match → sepia toning, 22 % colour kept → halation, vignette, grain) + **depth-model lens bokeh** (approved 2026-10-20)
- Caption style: English subtitles, Clean; title in romanised Bangla only
- Music: the reference's audio (VO + bed), whole, from 0:00. A cutting guide only; the director adds the same audio from IG at upload

## Round 0 — Interview, round 1 (2026-10-19)
- **Angle:** "Contrast, then hope": who gets left out of Pujo, then moments where everyone shares in it.
- **Speech:** "No speech, music only" (superseded in round 2, see below).
- **Footage:** director's pool `~/Documents/Media/` (97 clips C140–C236, Blackmagic Cam on iPhone: HEVC 3840×2160 with a rotation flag → 2160×3840 vertical, 85 @ 30 fps, 12 @ 25 fps (C140–C151), shot 2026-10-16 → 19). The director wanted to **choose from it first**.
- **References / music:** none at first ("you decide").
- From `studio/director-profile.md` (not re-asked): @satyajitmall, bold condensed type (DIN Condensed Bold), English words by default, own-footage effects only, AI video policy.

## Round 0 — Picks (2026-10-19)
- Survey: `analysis/media_survey/` (analyser on all 97). Grouped pick sheets: `analysis/picks/A_spectacle.jpg`, `B_edges.jpg`, `C_turn_and_themes.jpg`.
- Director: **take all 41** of the proposed shortlist; **copy** them (not link) → `raw/b-roll/` (2.3 GB). The only on-theme pandal is the **Ram-naam pandal (C224 / C228 / C230)**; C153 / C154 / C179 / C182 are off-theme.
- Left out: tests (C146–C151 bedroom + camera settings, C178 black, C229 0.5 s), upside-down C191 / C192, the Vajpayee pandal C176 / C177, the cartoon pandal C202–C205, repeats.

## Round 0 — Interview, round 2 (2026-10-19)
- **Music → reference:** the director added `~/Downloads/Video-64834.mp4` → `references/ref_audio_vo.mp4`: "use the same audio as well as the voiceover". It's a Hindi VO ("two men inside every man": the 18-year-old dreamer vs the 28-year-old who keeps the house running…) over a soft bed, 35.82 s.
- **Confirmed:** the whole 35.8 s as the soundtrack (→ `hybrid`); **keep the women** in too; post with **IG's audio at upload** (`_mix` + `_IG` exports); **English subtitles**.
- **Words:** title in romanised Bangla only. **Look:** cool edges → warm turn. **Pace:** arc, ~35–45 s (the VO sets it at 35.8 s).

## Round 1 — Proposal (2026-10-19)
Full plan: `brief.md` v1. Storyboard: `analysis/picks/storyboard_v1.jpg`. EDL data: `analysis/edl_v1.json`. Subtitles: `analysis/subtitles_v1.json`. VO line timings: `analysis/vo_timing.json` (burned-in subtitle changes + speech-band pauses; they agree to within 0.1 s).

**Hook options**
1. **(Recommended) C186 3.50–7.10:** packed street under lit arches, slow push, title PUJO KI ASOLEI SOBAR? from 0.3 s, VO L1 from 0.21 s. It opens on "the Pujo everyone sees", so every working face after it answers the question, and the seller gets the last shot uncontested.
2. **C193 0.00–3.30:** the balloon seller gazing at his balloons, the arch glowing behind, as the hook. Man + festival in one frame, but it spends the payoff image; the ending would fall to C194 (only 2.8 s).
3. **C143 0.00–3.60:** phones raised at the golden idol. Strong "spectacle" read, but busy behind the title (chandelier highlights).

**EDL (reel time = audio time; 30 fps; all cuts inside VO pauses)**
| # | clip | in | out | text / action | V1 move | V2/V5 | transition out | SFX |
|---|---|---|---|---|---|---|---|---|
| 1 | C186 | 3.50 | 7.10 | L1 "every man has two men inside him": crowd under arches | slow push 100→106 | V5 title 0.3–3.3 + sub | cut 3.60 | soft hit at title |
| 2 | C210 | 1.50 | 5.60 | L2 "at 18, wanted to conquer the world": boy gazing at toys | handheld | sub | cut 7.70 | — |
| 3a | C221 | 0.00 | 1.80 | L3 "and one who, at 28…": marigold seller | hold | sub | cut 9.50 (pause 9.26–9.62) | — |
| 3b | C189 | 0.30 | 1.65 | L3 "…": girl selling light-up toys | hold | sub | cut 10.85 (pause 10.74–10.92) | — |
| 3c | C213 | 2.00 | 3.85 | L3 "…keep the house running": old shopkeeper | slow push | sub | cut 12.70 | — |
| 4 | C211 | 0.50 | 3.05 | L4 "the first one dreamed": boy among balloons | handheld | sub | cut 15.25 | — |
| 5 | C222 | 1.00 | 3.05 | L5 "the second does the maths": flute seller on phone | source pan | sub | cut 17.30 | — |
| 6 | C187 | 0.50 | 4.10 | L6 "one day I'll change everything": lit arches, crowd | handheld | sub | cut 20.90 | — |
| 7a | C223 | 0.20 | 2.40 | L7 "the second thinks every month": phuchka seller | handheld | sub | cut 23.10 (pause 22.98–23.10) | — |
| 7b | C217 | 0.30 | 2.10 | L7 "let this month work out": old woman resting | hold | sub | cut 24.90 | — |
| 8a | C143 | 1.00 | 2.50 | L8 "maybe that's why": phones at the golden idol | hold | sub | cut 26.40 (pause 26.26–26.54) | — |
| 8b | C215 | 0.00 | 2.65 | L8 "when a man suddenly goes quiet": man alone by a tree | punch-in + slow push | sub | **Cross Dissolve 10 f** at 29.05 (turn) | — |
| 9 | C228 | 0.30 | 3.15 | L9 "doesn't mean he's lost to the world": Ram-naam pandal | slow push | sub | cut 31.90 | — |
| 10 | C193 | 0.00 | 3.92 | L10 "standing in front of his own old dreams": seller gazing at balloons | slow push | sub + @satyajitmall 34.4–35.8 | end 35.82 | — |

**Estimated runtime: 35.82 s** (14 shots, avg 2.56 s).

## Round 1 — Director notes on the proposal (2026-10-19)
1. "I want shots of the goddess in between the shots."

## Round 1 — Revised proposal v1b (2026-10-19)
Note 1 → a **goddess insert in every VO pause**: a different pandal's Durga each time, 0.57–1.32 s, hard cuts, gold look. The people stay on the lines. Skipped pauses: 15.08–15.38 (0.3 s, kept as the dream → maths hard match) and 20.54–21.25 (shot 6 is already spectacle). 8a C143 is dropped (redundant with the inserts; 25 fps). The turn dissolve moves to 28.70 (lone man → G6 Durga). +3 clips copied from the pool for faces the picks lacked: C163 (red), C171 (orange), C199 (purple). Storyboard: `analysis/picks/storyboard_v1b.jpg`; data: `analysis/edl_v1b.json`; goddess windows measured in `analysis/goddess/` (holds + selects).

| # | clip | in | out | reel | text / action | V1 move | transition out |
|---|---|---|---|---|---|---|---|
| 1 | C186 | 3.50 | 6.74 | 0.00–3.24 | L1 crowd under arches + TITLE 0.3–3.0 | slow push | cut |
| G1 | C208 | 0.30 | 1.04 | 3.24–3.98 | white Durga | hold | cut |
| 2 | C210 | 1.50 | 4.76 | 3.98–7.24 | L2 boy gazing at toys | handheld | cut |
| G2 | C163 | 0.10 | 1.09 | 7.24–8.23 | red Durga | hold | cut |
| 3a | C221 | 0.00 | 1.27 | 8.23–9.50 | L3 marigold seller | hold | cut (pause) |
| 3b | C189 | 0.30 | 1.65 | 9.50–10.85 | L3 girl selling toys | hold | cut (pause) |
| 3c | C213 | 2.00 | 3.23 | 10.85–12.08 | L3 old shopkeeper | slow push | cut |
| G3 | C152 | 24.00 | 25.32 | 12.08–13.40 | yellow Durga, priest | hold | cut |
| 4 | C211 | 0.50 | 2.35 | 13.40–15.25 | L4 boy among balloons | handheld | cut (hard match) |
| 5 | C222 | 1.00 | 2.47 | 15.25–16.72 | L5 flute seller on phone | source pan | cut |
| G4 | C171 | 1.20 | 2.34 | 16.72–17.86 | orange Durga, tilt up | source tilt | cut |
| 6 | C187 | 0.50 | 3.54 | 17.86–20.90 | L6 lit arches, crowd | handheld | cut |
| 7a | C223 | 0.20 | 2.34 | 20.90–23.04 | L7 phuchka seller | handheld | cut (pause) |
| 7b | C217 | 0.30 | 1.80 | 23.04–24.54 | L7 old woman resting | hold | cut |
| G5 | C199 | 3.60 | 4.42 | 24.54–25.36 | purple Durga | punch-in 1.3× | cut |
| 8 | C215 | 0.00 | 3.34 | 25.36–28.70 | L8 man alone by a tree | punch-in + push | **Cross Dissolve 10 f** |
| G6 | C169 | 17.70 | 18.44 | 28.70–29.44 | gold-pandal Durga (TURN) | punch-in 1.3× | cut |
| 9 | C228 | 0.30 | 2.48 | 29.44–31.62 | L9 Ram-naam pandal | slow push | cut |
| G7 | C145 | 9.80 | 10.48 | 31.62–32.19 | golden Durga's face (25 fps → conform; orig. time) | hold | cut |
| 10 | C193 | 0.00 | 3.63 | 32.19–35.82 | L10 seller gazing up at balloons + @satyajitmall 34.4–35.8 | slow push | end |

**Runtime 35.82 s, 20 shots** (13 people avg 2.2 s, 7 goddess avg 0.9 s). All 19 cuts checked to sit in VO pauses.

## Round 1 — Director notes on v1b (2026-10-19)
1. "There are too many" (goddess inserts).
2. "Start with a montage of the Devi, with the shots where a priest is performing aarti in front of the Devi. Start from there."
3. "There are so many other shots of men that you have skipped."

## Round 1 — Revised proposal v1c (2026-10-19)
1. Goddess inserts after the opening: 7 → **2** (turn 28.70 C171, before the seller 31.62 C145).
2. Opens on a **Devi/aarti montage 0–8.23 s**: M1 C152 wide (the priest's aarti with incense, punched in 1.4×) → M2 C161 red Durga in aarti smoke → M3 C152 close (priest with the lamp, Devi's face) → M4 C208 white Durga → M5 C190 young priest beside the Devi, looking up (hands over to the men). Searched all 97 clips for aarti: C152 is the clear one; C158 / C160 / C161 / C164 (red Durga pandal) show aarti smoke, with C158's flame at ~8 s behind bamboo; C164's man in orange is on his phone. +2 clips copied (C161, C190).
3. **More men:** + C216 rickshaw puller, C212 young balloon seller with a boy, C201 father at the toy stall, C195 cotton-candy seller (plus C190 priests). Out: C186 / C187 crowd hooks, C211, C223, C189. Men are now 12 of the 14 people shots; women C221 and C217 stay.

Syllable-gap dips used for montage cuts (speech-band minima ≥ 9 dB deep): L1 0.45, 0.75, 1.71, **2.21**, 2.48; L2 4.32, 4.69, **5.03**, 5.24, **6.50**, 6.65.

| # | clip | in | out | reel | text / action | V1 move | transition out |
|---|---|---|---|---|---|---|---|
| M1 | C152 | 8.80 | 11.01 | 0.00–2.21 | L1 priest's aarti before the yellow Durga + TITLE 0.3–2.1 | punch-in 1.4× + push | cut (syllable gap) |
| M2 | C161 | 0.30 | 1.33 | 2.21–3.24 | red Durga in aarti smoke | hold | cut (pause) |
| M3 | C152 | 23.90 | 25.69 | 3.24–5.03 | L2 priest with the lamp, Devi's face | hold | cut (syllable gap) |
| M4 | C208 | 0.30 | 1.77 | 5.03–6.50 | white Durga | hold | cut (syllable gap) |
| M5 | C190 | 4.90 | 6.63 | 6.50–8.23 | young priest beside the Devi | handheld | cut (pause) |
| 3a | C216 | 0.00 | 1.27 | 8.23–9.50 | L3 rickshaw puller | hold | cut (pause) |
| 3b | C221 | 0.00 | 1.35 | 9.50–10.85 | L3 marigold seller | hold | cut (pause) |
| 3c | C213 | 2.00 | 4.55 | 10.85–13.40 | L3 old shopkeeper | slow push | cut (pause) |
| 4 | C210 | 1.50 | 3.35 | 13.40–15.25 | L4 boy gazing at toys | handheld | cut (pause, hard match) |
| 5 | C222 | 1.00 | 3.05 | 15.25–17.30 | L5 flute seller doing sums on his phone | source pan | cut (pause) |
| 6 | C212 | 0.20 | 3.80 | 17.30–20.90 | L6 young balloon seller + boy | handheld | cut (pause) |
| 7a | C201 | 0.30 | 2.44 | 20.90–23.04 | L7 father at the toy stall | hold | cut (pause) |
| 7b | C217 | 0.30 | 1.80 | 23.04–24.54 | L7 old woman resting | hold | cut (pause) |
| 8a | C195 | 0.20 | 2.20 | 24.54–26.54 | L8 cotton-candy seller in the crowd | handheld | cut (pause) |
| 8b | C215 | 0.00 | 2.16 | 26.54–28.70 | L8 man alone by a tree | punch-in + push | **Cross Dissolve 10 f** |
| G1 | C171 | 1.20 | 1.94 | 28.70–29.44 | orange Durga (TURN) | source tilt | cut |
| 9 | C228 | 0.30 | 2.48 | 29.44–31.62 | L9 Ram-naam pandal men | slow push | cut |
| G2 | C145 | 9.80 | 10.48 | 31.62–32.19 | golden Durga's face (25 fps → conform; orig. time) | hold | cut |
| 10 | C193 | 0.00 | 3.63 | 32.19–35.82 | L10 seller gazing up + @satyajitmall 34.4–35.8 | slow push | end |

**Runtime 35.82 s, 19 shots.** Storyboard: `analysis/picks/storyboard_v1c.jpg`; data: `analysis/edl_v1c.json`. The storyboard check caught a passer-by crossing C222 at 3.4 s → shot 5 ends at src 3.05.

## Round 1 — Director notes on v1c (2026-10-19)
1. "The colour grading should be the same across the videos."
2. "A natural depth in shots should be added."

## Round 1 — Revised proposal v1d (2026-10-19), cut unchanged from v1c
1. **One grade.** The edge/gold split is dropped. Every clip is primary-matched (A1) to one warm-neutral target (midtone R/G ≈ 1.06, B/G ≈ 0.90, luma 0.34–0.38); then a single V3 adjustment layer carries one look (Kodak 2393 preset ≈ 40 %, saturation −5) for the whole reel. Preview on 8 shots: warm/cool spread 0.65 → 0.24, luma spread 0.19 → 0.11.
2. **Natural depth.** (a) Tonal: a gentle S (shadows −10, blacks −5, highlights −15, contrast +8) + soft vignette (−0.8) on the V3 look, every shot. (b) Optical: a person matte (`hyperframes remove-background`) → mild background defocus (σ 5 px) + 0.15 stop falloff, baked to ProRes on 10 people shots before colour. Not on the idols, C195 or C228. Tested on stills: `analysis/look_test/before_after.jpg` (tool: `tools/look_preview.py`, an intent preview with the starter `.cube`; the Premiere look is the built-in preset and gets matched by render in Phase 4).

## Round 1 — Checkpoint 1 approved (2026-10-19)
Director: "Approved v1d. Kids' faces are fine, subtitles OK as drafted, keep the 2 goddess inserts. Start the rough cut. No other reel session is using Premiere right now."
- `brief.md` v1d is now binding.

## Round 1 — Rough-cut prep, outside Premiere (2026-10-19)
Premiere held puja-night-2.prproj (reel-2 working). The director chose "wait for reel-2 to finish". Done meanwhile:
- **Depth bakes** (`tools/depth_bake.py`, v2 recipe: σ 3 + distance ramp): 10 shots → `renders/depth/*_depth.mov` (2160×3840 ProRes 422 HQ, 30 fps, source audio). 0 frame_scan flags on all 10. Placement offsets in `renders/depth/bakes.json` (place_in = 0.5 s handle where the source allowed).
- **Title:** HyperFrames project `graphics/title/` (base copied from puja-night-2's verified title), PUJO KI / ASOLEI SOBAR?, 96 px, cap tops 236 / 340, 2.9 s @ 30 fps, ProRes 4444 alpha (`graphics/title/renders/title-alpha.mov`). Composite-checked on M1 (punch-in) and M2: line 2 sits over the gold frieze on M1, legible with the halo; recheck after the grade.
- **Subtitles:** 18 cards (`renders/overlays/subs/sub_01–18.png`, DIN Condensed 68 px, soft white #F8F4EC, dark halo, centre y 1475; all inside the safe zone). End card `renders/overlays/endcard_handle.png` (@satyajitmall, y 1290). Composite-checked on C213, C215, C193.
- **Premiere scripts, ready to run** (all target this reel's `.prproj` by path, never "active"): `analysis/_es_import.jsx`, `_es_items.jsx`, `_es_seq.jsx` (1080×1920 @ 30 from title-alpha.mov), `place_v1.json` (19 rows for `add_to_timeline_batch`; C145 times converted to interpreted fps), `_es_reframe.jsx` (scale 50; M1 70 @ 0.542 / 0.500; 8b 65 @ 0.350 / 0.447, from the matte), `_es_av.jsx` (VO on A3, subtitles V5, title + end card V6). Generator: `tools/build_premiere_scripts.py`.

## Round 1 — Rough cut (2026-10-19, Phase 3)
- Director: "go" (reel-2 done; its notes say puja-night-2 is final, and its .prproj was saved 19:22:59).
- Closing puja-night-2.prproj (no save) was **denied by the permission classifier** ("interfere with workloads"). → Left it open, untouched; created this reel's project alongside (`create_project`). It became the active project (verified via `app.projects` / `app.project.path`). Every script checks the project path.
- Import: 40 items (02_B-Roll 8 originals, 07_Depth 10 bakes, 03_Graphics 20, 04_Textures grain, 06_Music VO). C145 conformed 25 → 30 (`set_override_frame_rate`).
- Sequence from title-alpha.mov: 1080×1920 @ 30; QE `addTracks` → V6 / A3.
- V1 via `add_to_timeline_batch` (19 clips): source in/outs to the frame. **7 one-frame gaps** from rounding (cut times like 2.21 s = 66.3 f) → extended the earlier clip's `end` to the next start on V1 + A1. `outPoint` read back stale, so set explicitly (in + duration). Final readback: contiguous, rec length = source length on all 19; `get_timeline_gaps` reports 1 gap of 4e-12 s (float noise). End frame 1075 = 35.833 s.
- Reframe readback: scale 50 on all; M1 70 @ (0.5418, 0.4998); 8b 65 @ (0.35, 0.4468).
- A3: VO wav 0–35.71 (the reference's 0.105 s AAC priming isn't content; timings unchanged). V5: 18 subtitles (sub_01 0.20–1.60 … sub_18 –35.71). V6: title 0.27–3.17, end card 34.40–35.82. A1 nat sound: −24 dB on M1–M3 (aarti) and 6 / 8a (crowd), everything else silent.
- `save_project` ✓. Export `pujo-ki-asolei-sobar_v1_rough.mp4`: 1080×1920, 30 fps, 35.80 s; audio max −0.7 dB / mean −17.3 dB ✓. Overview `analysis/review_v1_rough/overview.jpg`, watch sheets `analysis/review_v1_rough/watch/`.
- Own look: plan followed; ungraded blue vs gold clash (Phase 4); 8a C195 subject tiny/dark (candidate swap: C194 seller close-up or C219 at review).

## Round 1 — Director notes on rough v1 (2026-10-19)
1. "Timing looks fair, but too many shots of the Durga unnecessarily. Go through the narration and try to fit in accordingly."

## Round 1 — Changes made → rough v1b (`Reel_pujo-ki-asolei-sobar_v1b`, duplicated from v1)
1. **Durga 7 → 3, every shot re-fitted to its VO line** (EDL `analysis/edl_v1e.json`, brief §5 v1e):
   - out: C161 red Durga, C208 white Durga, the C171 orange-Durga turn insert, and the weak C195;
   - kept: the aarti (A1 wide, A2 lamp close-up) and one goddess beat (C145 golden face → seller looks up, for L10 "his own old dreams");
   - L2 "at 18, wanted to conquer the world" → young balloon seller C212; L6 "one day I'll change everything" → young priest C190 (src 3.30, opening on him, not mid-pan); L8a → phuchka seller C223 (new depth bake, 0 flags); turn = Cross Dissolve 856–866 lone man → Ram-naam men.
2. Opening re-cut after checking v1b's first export: the title (0.27–3.17) had landed on the Devi's face in the close-up → A1 now holds 0–96 f (the whole title over the wide), A2 = 0.87 s lamp beat (src 24.60), C212 from f122.
- Readback: 16 clips on V1 / A1, contiguous, rec = source length, end f1075. Reframe ✓ (A1 70, 8b 65). V5 / V6 / A3 unchanged from v1. Exported `pujo-ki-asolei-sobar_v1b_rough.mp4`: 35.80 s, VO −0.8 dB peak, decodes clean.
- The MCP bridge dropped during the blocking `exportAsMediaDirect`; the export finished (No Error) and `verify_premiere_connection` reconnected. A1 aarti-close level was muted by a stale keep-list (fixed in `_es_export.jsx` for the next export).

## Round 1 — Director notes on rough v1b (2026-10-20)
1. "Still its cut and depiction is not accurate." Asked what: **"cuts off the words"** (pictures must change on the words, not in pauses or mid-line).
2. "Go through the folders of Videos, all folders marked Pujo, and then map the shot."
3. "The cinematic effect and colour grading as shown in the reference should come out."

## Round 1 — Revised plan v1f (2026-10-20)
1. **Cuts on the words.** Measured every sentence / clause onset in the VO to the frame (`analysis/word_onsets.json`: speech-band rise after each pause). v1b had cuts up to 28 frames early, sitting in the pauses (e.g. L8: f736 vs the word at f764). v1f: 13 shots, all 12 cuts exactly on onsets f124, 247, 288, 406, 460, 539, 638, 693, 764, 797, 886, 969. No cuts mid-word or mid-pause.
2. **All Pujo folders surveyed** (`~/Documents/Video /`): Oct 15 (78, pandal art, no working people; overviews built from my-reel's contacts → `analysis/survey_oct15/`), Oct 16 (63, idols / crowds; puja-night-2 overviews), Oct 17 + 18 (= the Media pool, 97, `analysis/media_survey/`), **Oct 19 (32, new, `analysis/survey_oct19/`)**. Oct 19 had what the narration needed. **One man per voice:** a young drummer (C004 / C005) is "the first man, 18", a tea seller (C032 / C031) is "the second man, 28". Plus: young stall seller gazing (C028) on "the first one dreamed", rickshaw puller on "and the one who", father at the toy stall / sums on a phone on "every month… let this month work out", the lone man on "goes quiet", the balloon seller on "his own old dreams". Durga: the aarti opening only (and behind the drummer). +5 clips copied.
3. **Reference grade measured** (`analysis/ref_grade/`, 11 frames): luma 0.25, p50 0.19, crushed ~10 %, sat 0.55, shadows R/G 1.02 B/G 0.53 (warm olive), mids 1.06 / 0.65 (amber), highlights 0.98 / 0.75; shallow focus, foreground framing, warm halation. New look `tools/ref_look.py` (per-clip normalise → low-key filmic curve + 3-way warm/olive balance + sat → halation + vignette). On our 13 frames: luma 0.248, sat 0.554, shadows 1.02 / 0.56, mids 1.06 / 0.65, highlights 0.97 / 0.75, i.e. within ~0.03 of the reference on every measure (`analysis/look_v1f/look_vs_ref.jpg`). LUT `grade/pujo_reference_look_v1.cube`.
- Storyboard `analysis/picks/storyboard_v1f.jpg`, EDL `analysis/edl_v1f.json`. Depth bakes for the 7 new / longer people shots (0 scan flags; C004 is VFR 29.28 → bakes now resample to an exact 30 grid).

## Round 1 — Director notes on v1f (2026-10-20)
1. "The shots are shot on an iPhone, so they don't have that natural depth of field: no bokeh at the back, no natural depth. You need to add that in post."
2. "The colour grading is off. I want very sepia, a filmy kind of vibe."
3. "Some have a blue hue, some a different tint, because they're shot under different lighting. Colour grade all of them accurately together."

## Round 1 — Changes → v1g (approved: "Yes, exactly this"; pipeline: "Bake into each shot")
1. **Lens bokeh from a depth model:** director approved a download of onnxruntime (PyPI, into `renders/_pylib`, reel-local) and Depth-Anything-V2-Small ONNX (Hugging Face, 99 MB, sha256 afb6a5c2…, `renders/models/`). Per frame: depth (CPU 0.35 s) → circle of confusion vs the focus plane → layered far-to-near disc blur with highlight boost (bokeh discs) → no bleed onto the subject (`tools/lens.py`). Edges checked at 100 %: no halos.
2. **Sepia film look** (`tools/sepia_look.py`) + halation / vignette / grain (`tools/preview_sepia_bokeh_lib.py`).
3. **Accurate together:** each shot's cast removed first (grey-world midtones + exposure to luma 0.36, constant per shot), then the identical look. Before/after: `analysis/look_v1g/before_after_v1g.jpg`.
- Full-frame renders: `tools/shot_render.py` → `renders/final_shots/*_v1g.mov` (ProRes 422 HQ 1080×1920 @ 30, source audio, 0.3 s handles, punch-ins baked). Shot 10 test: 48 frames, 0 scan flags.
- Brief rewritten to v1g (binding).

## Round 1 — v1c build (2026-10-20)
- 13 baked v1g shots (0 scan flags, except the C222 passer-by inside the tail handle) imported to bin `08_Final_v1g`; `Reel_pujo-ki-asolei-sobar_v1c` (0c7a2e62-…) duplicated from v1b (V5 / V6 / A3 kept), V1 / A1 rebuilt frame-exact; 100 % scale, push 100 → 105 on 1 / 4 / 11 / 12 / 13; Cross Dissolve 881–891. Exports `_v1c_mix` (−0.7 dB peak) and `_v1c_IG` (VO muted, ambience −26.7 dB peak).

## Round 1 — Review gate loop 1 (`analysis/review_v1c.md`): FAIL, 0 blocker / 6 major / 6 minor
1. **C193 face melts late (major) — fixed:** person matte (hyperframes remove-background per frame) protects the subject from blur, and focus = depth inside the matte. Face sharp to the last frame (`fix_compare`).
2. **C228 blown whites, veil, black top band, crushed blacks (major) — fixed:** highlight shoulder before the look (knee 0.72); halation 0.10 / vignette 0.12 on this shot; the vignette never goes below the film floor 0.03.
3. **C201 shirt blob + halo (major) — fixed:** shoulder + background fill rebuilt from out-of-focus pixels only (normalised convolution), so the subject no longer glows into the blur; near blur on the child 6 → 2 px.
4. **C028 face in the top UI (major) — fixed:** new moment 40.40–42.20 (he stands upright, gazing), face at y ≈ 360–540. ~0.4 s of the face sits near x 930–990 (right 120 px), clear of IG's icon column (y 1100+). Intended, to confirm at Checkpoint 2.
5. **C005 repeats shot 2, drummer idle (major) — fixed:** L6 is now C027 3.00–6.30, a young dhaki actually drumming, face lit up.
6. **C216 hair halo (major) — fixed** (same fill fix as 3).
7. C222 phone late (minor) — partly: in-point 0.90 → 1.03 (a passer-by enters at src 3.43, so the shot can't move later).
8. Subtitles over the priest (minor) — fixed: sub_01 / sub_02 re-set as 2-line cards right of the priest (x 637–913).
9. End card read as a 3rd subtitle (minor) — fixed: `@SATYAJITMALL` in the title style (DIN Condensed, cream, dark halo, tracked), lower-left over the dark coat (`endcard_handle_v2.png`).
10. C215 hand smear (minor) — fixed by the person matte.
11. Cut at f247 leads the word by 4 f (minor) — fixed: f251 (verified: VO jumps −31.6 → −11.2 dB at 8.37 s). My onset rule fired on breaths; re-measured all with a peak-relative rule (others 0–3 f, reviewer had them within ±1 f).
12. C032 shirt fringe (minor) — fixed (fill fix).
- Renderer v1h: `tools/shot_render.py --ver v1h` (EDL `analysis/edl_v1h.json`, focus `analysis/focus_v1h.json`).

## Round 1 — v1d build + review gate loop 2 (`analysis/review_v1d.md`): FAIL, 0 blocker / 6 major / 3 minor (gate limit reached: no 3rd blind loop; fixes verified by the editor)
- v1d: `Reel_pujo-ki-asolei-sobar_v1d` (6179d58f-…), 13 v1h shots, type swaps. A still overwritten on V5 took Premiere's default 5 s and wiped sub_02 / trimmed sub_03 → restored (set the item's in/out before `overwriteClip`); all 18 cards re-verified to ±0.02 s.
1. **C028 face soft, beads sharp (major) — fixed by replacement:** L4 is now the first man himself, C004 12.00–13.80, looking up and away, 1.6× on his face.
2. **C027 focus behind the hero (major) + 3. passer-by wipes (major) — fixed by replacement:** L6 is C005 0.50–3.80, the same drummer playing, 1.3× on hands, drum and face. Not a repeat of shot 2's wide.
   - Root cause of 1 and 2: focus came from the median depth of *all* people in the matte (background people included) → now a point on the hero, and only the hero's matte component is protected.
4. **Black floor differs between shots, shot 7 dark (major) — fixed:** the look's black is now 0.03 (was 0), clamped after vignette and grain; per-shot final luma gain to 0.27 (measured on 3 treated frames, limited 0.75–1.6).
5. **Three different 'first men' (major) — fixed:** one drummer for L2 / L4 / L6 (see 1–2).
6. **The Devi soft in the hook (major) — fixed:** shot 1 focus on the Devi (point), max blur 3 px, near 2 px, all people protected.
7. C028 no gaze (minor) — moot (replaced).
8. Cards 1–2 on the seated attendant's head (minor) — fixed: moved up to y 1230–1361.
9. C228 plumes smeared (minor) — far blur on 12 down to 8 px.
- Renders v1i: `tools/shot_render.py --ver v1i` (EDL `analysis/edl_v1i.json`, focus `analysis/focus_v1i.json`).

## Round 1 — v1e build + editor verification (gate limit reached after loop 2)
- 13 v1i shots → `Reel_pujo-ki-asolei-sobar_v1e`; readback frame-exact, 18 subtitles ±0.02 s, dissolve 881–891, pushes on 1 / 4 / 11 / 12 / 13.
- Per-shot luma over the placed frames: median 0.266, all within ±0.025 after C222 was re-rendered (its gain had been measured on handle frames with a passer-by → gain now measured only on placed frames). Black floor p1 0.025–0.064 on every shot (no true blacks). R−B +0.10…+0.14.
- First / mid / last frame of every shot checked from the export (`analysis/review_v1e/first_mid_last.jpg`): faces sharp, no halos, the Devi crisp, cards clear of the attendant.
- Found and fixed by the editor: a dropped-frame jump in C004 at 12.50 s inside shot 5 → shot 5 in 12.55 (placed window max frame diff 6.7 vs median 3.3).
- `frame_scan` on the final export: 0 flags in 1074 frames. `_mix` −0.7 dB peak; `_IG` −26.7 dB (nat sound only).

## Round 2 — Director notes on v1e (2026-10-20)
1. "The bokeh is not coming out OK. Maybe we render one without."
2. "Post-production work on correction, stability and clarity needs to improve."

## Round 2 — Changes (v2, `tools/shot_render_v2.py`; v1e kept as the with-bokeh version)
1. **No bokeh** (render flag; depth pass skipped).
2. **Stability:** own translation stabiliser. Phase correlation on quarter-res luma, camera path smoothed (gaussian σ 16 f) or locked on static holds (1, 3, 4, 8, 9, 11, 13); correction crop from a 10 % margin of the 4K-supersampled frame (no upscale). Measured on placed frames (`shake_report`): C031 6.33 → 3.71 px, C152 0.29 → 0.18. C222 doesn't improve (a fast ~450 px/s handheld swing, not shake) → **shot 9 replaced with C213** (old shopkeeper waiting, steady hold) for "let this month work out".
3. **Clarity:** hqdn3d denoise at 4K (temporal-heavy) → lanczos supersample → fine detail sharpen + local-contrast clarity on luma; grain 0.022 → 0.012. Sharpness (Laplacian var.): C222 +22 %, C031 +40 %, C152 ×4 (no blur).
4. **Correction:** white balance from near-neutral (lowest-chroma 30 %) pixels + per-shot tonal match (p02 / p50 / p98 → 0.035 / 0.30 / 0.86), all measured on the frames on screen; then the same sepia look, floor 0.03 and luma match 0.27.

## Round 2 — v2 renders + preview (2026-10-20)
- 13 v2 shots: luma within ±0.006 of the median (0.266), black floor 0.023–0.033, R−B +0.11…+0.16 (drummer's yellow shirt warmest).
- Camera shake on the static background (phase correlation, the same ROI the stabiliser uses), v1i → v2: shot 2 3.12 → 0.62 px (−80 %), 5 8.66 → 2.60 (−70 %), 6 4.82 → 2.25 (−53 %), 10 4.12 → 3.24 (−21 %), 7 2.56 → 2.46 (−4 %); holds locked (1, 3, 4, 8, 9, 11, 13 ≤ 0.4 px). `shake_report` over the whole frame reads higher on 5 / 7 / 10 because it counts the subjects' own motion (drum, hands); a background ROI (`stab_roi`) was added for those.
- Premiere was taken by reel-4 (`uski-aankhein.prproj` active) when I went to build v2. The project-path guard refused the import ("wrong project"); nothing touched their project. → Assembled an offline preview that mirrors the timeline (`tools/preview_assemble.py`): `renders/exports/pujo-ki-asolei-sobar_v2_preview.mp4` (1075 frames, 35.83 s, VO −0.7 dB, 0 scan flags). The Premiere build (`Reel_pujo-ki-asolei-sobar_v2`) waits until Premiere is free.

## Round 2 — Director: "for now finalise it" (2026-10-20)
- reel-4 idle → opened this reel's project alongside (reel-4's and puja-night-2's stay open, untouched); active project verified by path.
- `Reel_pujo-ki-asolei-sobar_v2` duplicated from v1e: V1 / A1 = 13 v2 shots, readback frame-exact, 18 subtitles ±0.02 s, dissolve 881–891, pushes 1 / 4 / 11 / 12 / 13, title + end card. Saved.
- **Final exports:** `pujo-ki-asolei-sobar_v2_mix.mp4` (guide VO, −0.7 dB peak) and **`pujo-ki-asolei-sobar_v2_IG.mp4`** (VO muted, ambience −26.7 dB: post with Instagram's audio from 0:00). 35.80 s, 1080×1920, 30 fps. `frame_scan` 0 flags. Matches the approved offline preview within encoding noise (mean diff 2–4 / 255).

## 2026-10-21 — Stray Look check (heads-up from reel-4 / uski-aankhein)
- The director loaded uski's G2 `.cube` in Premiere's Lumetri panel with no uski clip selected (~07:50 UTC); reel-4 warned it might have landed on a clip of ours.
- Read-only scan of all 6 of our sequences (207 video clips): only Opacity / Motion / Time Remapping, **no Lumetri**. `.prproj` last saved 2026-10-20 18:56 IST; the final v2 exports date from 18:56 IST on 10-20, before the incident → **delivered files unaffected**. A master-clip effect isn't scriptable to check → render-compare before any future export. Replied to reel-4 (puja-night-2.prproj is also open).

## Round 3 — Director notes on v2 (2026-10-21)
1. "The colour is too strong and the sepia does not come out well. We might try the cinematic colour grading that I have, the master class example." → the reference is `~/Downloads/We-Didnt-Expect-SnapYT.App.webm` (a Bangkok travel film, 3240×2160, 197 s; director picked it over the uski grade) → `references/ref_grade_bangkok.webm`.
2. "I have added more footage in new folders of Pujo, check those." → `~/Documents/Video /Pujo 2026 Oct 20/`: 66 clips; C001–C032 duplicate Oct 19, **C033–C066 are new** (Oct 20 evening → Oct 21 02:27). Surveying (`analysis/survey_oct20/`).

## Round 3 — Work in progress
- **Bangkok grade measured** (25 colour frames, B&W map shots skipped): luma 0.284, p02 0.031, p50 0.244, p98 0.747, saturation 0.346, crushed 4 %, mids R/G 1.00 B/G 0.86, highlights 0.91 / 0.87: a soft, low-saturation, slightly cool-highlight film look with full colour.
- `tools/cine_look.py`: tone curve + 3-way balance + saturation, fitted to those medians on our 13 corrected frames (Powell, bounded), then shadows tamed (the reference's shadow R/G 1.5 comes from its warm interiors) and saturation pinned to 0.346. Result: luma 0.298, p50 0.239, p98 0.746, sat 0.346, mids 1.01 / 0.89, highlights 0.93 / 0.90. A per-shot residual cast match after the look pulls the blue / green street-light shots warm-neutral.
- Proposal stills sent: `analysis/look_v3/proposal_v3.jpg`, `analysis/look_v3/cine_matched.jpg`. Grade approval pending; the director first pointed to the new footage.

## Round 3 — Director answers + v3 (2026-10-21)
- Grade: **"warmer"** (than the first cinematic proposal). Shots: **"you decide based on the narration; this is the skill I wanted you to develop."**
- **Narration-driven picks from Oct 20** (full reasoning table in brief §5): L3a "and the one who…" C216 → **C043** (a rickshaw puller revealed under the Pujo light column, ending on his face); L8b "when a man suddenly goes quiet" C215 → **C052** (an old man standing silent in a doorway). Considered and left out: C050 (a priest before the Devi: a 4th deity frame), C042 (no face). Both 25 fps, conformed in the renderer (every frame kept, played at 30; audio atempo 1.2, muted anyway).
- **v3 renderer** (`tools/shot_render_v3.py`): v2's stabilise / denoise / clarity / correction + warm cinematic look (mids 1.02 / 0.90, highlights 0.97 / 0.94) + per-shot warm cast match (target R/G 1.06, B/G 0.78) + per-shot saturation cap 0.34 (drummer shots were 0.46 → k 0.71). Shot stats: luma 0.270–0.277, saturation 0.22–0.35, black floor 0.016–0.033.
- `Reel_pujo-ki-asolei-sobar_v3` (17e6acf7-…) from v2: readback frame-exact, 18 subtitles ±0.02 s, dissolve 881–891; no effects on any clip (stray-Look check). Exports `_v3_mix` (−0.7 dB) and `_v3_IG` (−26.7 dB, VO muted), 35.80 s. `frame_scan` 0 flags; no repeated / stutter frames (conformed shots included); first / mid / last frames checked (`analysis/review_v3/first_mid_last.jpg`).
- Not run: a blind review gate on v3 (the round-1 loops are spent; editor-verified).

## Round 4 — Director note on v3 (2026-10-21): "Stabilisation issue"
- Measured (new subpixel similarity metric, `tools/shake2.py`, translation + roll + zoom per shot on the v3 export): holds steady (0.1–0.3 px), but residual shake on the handheld shots: 5 drummer close-up 2.3 px + 0.07° roll (1.6× punch-in amplifies it), 10 phuchka 2.1 px, 6 tea counter 1.5, 3 rickshaw reveal 1.4 px + 0.2 % zoom wobble, 7 drummer 1.1. The v2/v3 stabiliser was translation-only with 0.5 s smoothing, so roll / zoom shake and slow sway (8–13 px) remained.
- **Fix: `tools/stab2.py` + `tools/shot_render_v4.py`.**
  - Similarity stabiliser: a grid of 28 patches, subpixel phase correlation, RANSAC similarity fit (rejects the moving subject); synthetic test recovers roll within 0.04° and translation within 0.3 px.
  - **Tripod lock** on static scenes (1, 2, 4, 5, 6, 8, 9, 11, 12, 13) when the 15 % margin allows (else σ 45 smoothing); moving shots smoothed strongly (3: σ 24, 7 / 10: σ 40).
  - A **second pass** re-measures on the stabilised frames and corrects the residual. The output window is checked to stay inside the margin (no edges); 4K supersampling, so no upscale.
- Test shots, v3 → v4 (placed frames; jitter / slow sway): 5: 2.6 / 9.5 → 1.2 / 2.4 px · 10: 2.0 / 13.4 → 0.6 / 3.0 · 6: 1.5 / 9.7 → 0.3 / 1.7 · 3: 1.6 / 8.3 → 1.0 / 3.8.

## Round 4 — v4 built + exported (2026-10-21)
- All 13 shots re-rendered with `tools/shot_render_v4.py` (v3 look unchanged; similarity stabiliser, 2 passes). Locked: 1, 4, 5, 8, 9, 11, 12, 13; smoothed: 2 (σ 45, the lock didn't fit the margin), 3 (σ 24), 6 (σ 45), 7 / 10 (σ 40).
- `Reel_pujo-ki-asolei-sobar_v4` (0a87ace5-…) from v3: frame-exact, 18 subtitles, dissolve 881–891, no clip effects. Exports `_v4_mix` (−0.7 dB) / `_v4_IG` (−26.7 dB), 35.80 s; `frame_scan` 0 flags; no blank or smeared borders.
- **Residual shake on the export (v3 → v4):** 5: 2.34 → 0.47 px · 10: 2.11 → 0.51 · 6: 1.47 → 0.31 · 3: 1.44 → 0.80 · 7: 1.14 → 0.48 · 2: 0.60 → 0.24; every shot ≤ 0.8 px and ≤ 0.04° roll (`analysis/review_v4_shake2.json`).

## Round 5 — Director note on v4 (2026-10-22): "Colour corrections still not on point"
- Diagnosed instead of guessing (skin detector, YCbCr, on 5 frames per shot of the v4 export, against the reference):
  - **skin hue spread 23–40° across shots** (a pro target is about ±3°), skin saturation 0.29–0.51;
  - most shots at 33–40° = sallow / yellow-green skin, against the **reference skin at 27.7°**.
  - My cast match balanced near-neutral pixels, but skin is what the eye reads.
- **Fix: skin-anchored per-shot correction** (`tools/skin_match.py`): iterative channel gains (luminance-preserving) so each shot's skin lands on hue 28°, saturation ~0.45; neutrals weighted 15 % so whites don't swing; the skin mask is gated by a **person matte** (hyperframes remove-background on 5 sample frames) because warm objects (C213's jars) fooled the colour-only mask. Off for shot 1 (idol).
- Stills approved by the director ("Yes, apply it": `analysis/look_v5/skin_compare.jpg`). Renderer `tools/shot_render_v5.py` (= v4 + skin anchor); skin check `tools/skin_report.py`.

## Round 5 — v5 built + exported (2026-10-22)
- In-render skin solve (`shot_render_v5.py`, person-gated) still missed on shots whose clothes fall in the skin colour box (the drummer's yellow shirt): measured 24–40° on the renders. → **`tools/skin_post.py`**: post-pass on the rendered shots. Skin = person matte ∩ YCbCr box ∩ HSV skin window (hue 0–42°, sat 0.15–0.75), robust median; iterate luminance-preserving gains to hue 28° (±1°), then saturation 0.45; same constants on every frame → `*_v5b.mov` (shot 1 / idol left as v5).
- `Reel_pujo-ki-asolei-sobar_v5` (3de939c9-…): frame-exact, 18 subtitles, dissolve, no clip effects. Exports `_v5_mix` (−0.7 dB) / `_v5_IG` (−26.7 dB), 35.80 s; `frame_scan` 0 flags.
- **Measured on the export:** skin hue **26.6–30.0°** across all 12 people shots (v4: 23–40°), saturation 0.45–0.50; the look, the stabilisation (v4) and the cut are unchanged.

## Round 6 — Director note (2026-10-22): "One version in black and white. only the first durga in gold?"
Read as an **alternate**, not a replacement: v5 (colour) stays; a B&W version of the same cut, with colour kept only on the Durga's gold in shot 1.

## Round 6 — v5_bw built + exported (2026-10-22)
- `tools/bw_render.py` on the v5 / v5b shot renders (same cut, stabilisation and skin work):
  - **B&W:** red-leaning channel mix 0.40 / 0.50 / 0.10 (skin reads luminous), gentle S-curve; luma matched to the colour version (0.24–0.28 per shot).
  - **Shot 1 gold (`--isolate`):** soft key on the idol's gold, hue 40–80° (measured on the graded frame), sat > 0.08, value > 0.15; inside the idol band (y 230–1520, feathered); **minus a per-frame person matte** (hyperframes remove-background), so the priest and attendant go grey. Kept colour = true gold (1.0 / 0.78 / 0.36) at the B&W luminance, 25 % of the original texture colour. Coverage 25 % of the frame.
  - Renders `renders/final_shots/*_bw.mov` (BT.709 tagged) + json.
- **Text:** the title and the @handle endcard were cream-tinted (chroma ~45), which would break "only the Durga in gold". Neutral copies made: `renders/overlays/title-alpha_bw.mov`, `endcard_handle_v2_bw.png`. Subtitles were already neutral white.
- `Reel_pujo-ki-asolei-sobar_v5_bw` (bb70786f-…), duplicated from v5: V1/A1 replaced (bin `15_BW`), gaps closed, pushes, dissolve, 18 subtitles; title and endcard swapped with `replace_clip`. Readback identical to v5 (13 shots, end 1075, 0 problems; V6 timing, scale and opacity identical).
- Exports `_v5bw_mix` (−0.7 dB) / `_v5bw_IG` (−26.7 dB), 35.80 s; `frame_scan` 0 flags.
- **Measured on the export (2 fps):** shot 1 chroma mean 18.1 (28 % gold pixels); every other frame chroma ≤ 0.07, 0 pixels above 20, text included.
- Review gate: same cut and timing as v5, grade-only change, so numeric checks + stills only (no reviewer loop).

## Round 7 — Director note on v5_bw (2026-10-23): "Use the colour correction skills that I have added to this project, the first frame start as if the colour is fading out from everywhere"
Read as: the B&W version opens on shot 1 in full colour; the colour drains out of the whole frame, leaving only the Durga's gold. Skill = `.claude/skills/ffmpeg-color-grading-chromakey` (the colour skill in this project, HQ import v0.6.1).

## Round 7 — Changes (2026-10-23)
- **`tools/bw_fade.py`**, built from the skill's recipes: weighted `blend` (its "Blend original with LUT") animated per frame on the timestamp T (its "Animated Color Effects"), in RGB (`gbrp10le`, its studio fix), BT.709 tags + `write_colr` (its studio rule). A = shot 1 graded colour (`01_C152_v5.mov`), B = shot 1 B&W + gold (`01_C152_bw.mov`); weight = sine ease-in-out over **timeline 0.0 → 2.4 s** (title is up 0.27–3.17 s). → `renders/final_shots/01_C152_bwfade.mov`.
- Tested on stills first (skill rule): `analysis/look_bw/fade/strip.jpg` (timeline 0–3.5 s). The skill's own isolation filter `hsvhold` (hue 45, sim 0.25) was tried for the end state: it greyed the gold too (chroma 0.4), so the person-matted gold key (`bw_render.py --isolate`) stays as the end frame.
- Render check: timeline 0.00 s = v5 colour (mean diff 1.2/255, re-encode); 2.4 s onward = the B&W-gold shot (0.65/255); frame chroma 24.4 → 18.5 as the colour leaves everything but the gold.
- **Premiere not touched:** reel-4's `uski-aankhein.prproj` is the active project and its session is running, so switching projects could send its scripts into ours (CR-20261018-my-reel-premiere-shared-between-sessions). Review copy built offline with `tools/preview_assemble.py` (new flags `--shot1 bwfade --bw-text`) → `renders/previews/pujo-ki-asolei-sobar_v5bw2_preview.mp4`. Preview check: the same tool without the fade matches Premiere's `_v5bw_mix` export to 2.96/255 mean; with it, frames from 4.2 s on are identical to v5_bw, chroma 23.3 (0.25 s) → 18.5 (2.25 s); 35.83 s, −0.7 dB. Premiere build (`Reel_pujo-ki-asolei-sobar_v5_bw2`: duplicate v5_bw, `replace_clip` shot 1 with `01_C152_bwfade.mov`, export `_v5bw2_mix` / `_v5bw2_IG`) waits for Premiere.

## Round 8 — Director note (2026-10-23): "there is a light flickering effect in the footage, maybe because it was shot on 1/60 shutter speed and the electrical bandwidth of India is 50 Hz, fix that"
Diagnosis confirmed by measurement (`tools/flicker_scan.py` → `analysis/flicker/scan_v5b.json`): lamps pulse at 100 Hz; at 30 fps that aliases to **10 Hz**, a 3-frame brightness cycle, peak at 9.8–10.2 Hz in every 30 fps shot.
- **Global pumping:** shot 4 C032 3.1 % (p95 frame step 5.6 %), shot 6 C031 3.4 % (5.9 %), shot 9 1.2 %.
- **Rolling bands** (rolling shutter, phase shifting down the frame): shots 2, 5, 7, 10, with 1.5–2.8 % bands that average out globally.
- **Local bulbs:** one tile in shot 6 flickers 13 %.
- The 25 fps shots 3 C043 and 11 C052 are clean (100 Hz = 4 × 25).
- Applies to both versions, colour and B&W.

## Round 8 — Changes (2026-10-23)
- **`tools/deflicker.py`** on every 30 fps shot render (v5 / v5b → **`*_v6.mov`**; shots 3 and 11 pass through):
  - per-tile (32 × 12) log luma in linear light;
  - sliding lock-in on the 3-frame cycle (gaussian σ 5 frames, follows the phase drift of VFR clips);
  - Wiener shrink so motion barely counts;
  - 2 passes (shot 6: 4 passes, clamp 20 %), clamp 15 %;
  - smooth bicubic gain map in linear light. Brightness only: no ghosting.
  - Batch: `tools/render_all_v6.sh`.
- **Measured** (`analysis/flicker/compare_v5b_v6.json`):
  - global 10 Hz: shot 4 3.08 → 0.57 %, shot 6 3.37 → 0.90 %, shot 9 1.17 → 0.22 %, all others ≤ 0.27 %;
  - bands max ≤ 1.6 % (was 4.7 %);
  - p95 frame step: shot 4 5.57 → 1.29 %, shot 6 5.93 → 2.41 %.
- **Visual check** on consecutive frames, before vs after (`analysis/flicker/shot2_top_f20-22.jpg`, `shot6_f40-43.jpg`): the bright frame of each cycle is gone; moving arms and people show no smear.
- **B&W rebuilt** on v6: `bw_render.py --src v6 --out bw6` (shot 1 `--isolate`) and `bw_fade.py --a v6 --b bw6 --name bwfade6`. Batch: `tools/render_all_bw6.sh`.
- **Premiere is still held by reel-4** (`uski-aankhein.prproj`, now at its v3). Offline previews of both versions:
  - `renders/previews/pujo-ki-asolei-sobar_v6_preview.mp4` (colour);
  - `renders/previews/pujo-ki-asolei-sobar_v6bw_preview.mp4` (B&W, colour-fade opening).
- **Premiere plan, once free:**
  - `Reel_pujo-ki-asolei-sobar_v6` = duplicate v5, V1/A1 → v6 shots;
  - `_v6_bw` = duplicate v5_bw, V1/A1 → bw6 + bwfade6;
  - exports `_v6_mix` / `_v6_IG` / `_v6bw_mix` / `_v6bw_IG`.
- **CR filed:** CR-20261023-pujo-ki-asolei-sobar-mains-flicker.

## Round 9 — Director notes (2026-10-23): "Again we are choosing the same set of people a few many time, also at places I think we need to slow down the video to add more drama. Try matching the footage with the words being said. Go through all videos."
1. **Repeats:** v5/v6 shows the same drummer 3× (shots 2 C004, 5 C004, 7 C005) and the tea seller 2× (4 C032, 6 C031). That came from round 1's "one man per voice" reading. → each line gets its own man.
2. **Slow motion:** no clip in the pool can give true slow-mo. `tools/pool_index.py` → `analysis/pool_r9/index.json`: 741 files = 327 originals + 411 proxies, all 24 / 25 / 30 fps, 0 above 30. → slow-mo is **synthesised**:
   - optical flow (`minterpolate` mci/aobmc/bidir), applied after grade + deflicker;
   - tested at 0.6× on the hardest shot (troupe drumming): no tearing, slight smear that reads as motion blur;
   - the calm shots (dreamer, rickshaw) are clean (`analysis/pool_r9/slowmo/`).
3. **Words ↔ picture:** cuts on measured Hindi onsets. 'duniya jeetna' (conquer the world) has its envelope dip at 5.45–5.50 → cut f165; 'bas ghar' (keep the house running) 10.95 s → cut f328; the second man lands on 'Dusra…' (15.43 s).
4. **All videos:** 327 originals, contact-sheeted (`tools/pool_sheets.py` → `analysis/pool_r9/sheet_01–19.jpg`, 4 frames per clip) and read sheet by sheet.
   - Oct 15–16: pandal art, no people.
   - New people found: C222 (two men on one tarp), C216 (rickshaw puller looking at camera), C215 (man alone), C027 / C026 (dhaki boy + troupe), C190 (young priest), C212 (young balloon seller), C028, C009.
   - Detail strips: `analysis/pool_r9/cand_A–E.jpg`.

## Round 9 — Proposal (v9, awaiting approval): `analysis/edl_v9_proposed.json`, storyboard `analysis/pool_r9/storyboard_v9.jpg`
Runtime is unchanged, 35.83 s. **14 different men, none repeated.**

| # | Time | Line | Picture | |
|---|---|---|---|---|
| 1 | 0.00–4.13 | I think every man has two men inside him. | C152 priest's aarti | keep (approved hook, B&W fade) |
| 2 | 4.13–5.50 | One who, at 18, | C027 young dhaki boy drumming | new |
| 3 | 5.50–8.37 | wanted to conquer the world. | C026 dhaki troupe on the march | new, slow 0.6× |
| 4 | 8.37–10.93 | And one who, at 28, | C190 young priest turns to camera | new |
| 5 | 10.93–13.53 | just wants to keep the house running. | C032 tea seller pouring | keep (now once) |
| 6 | 13.53–17.97 | The first one dreamed. / The second does the maths. | C222, one shot: young man staring, arms crossed (slow 0.6×) → camera moves to the older man doing figures on his phone, landing on 'Dusra…' | new |
| 7 | 17.97–21.27 | The first said, 'One day I'll change everything.' | C212 young balloon seller | new, slow 0.7× |
| 8 | 21.27–23.10 | The second thinks every month, | C201 father at the toy stall | keep |
| 9 | 23.10–25.47 | 'Just let this month work out.' | C213 old shopkeeper | keep |
| 10 | 25.47–26.57 | Maybe that's why, | C215 man alone on a roadside wall | new |
| 11 | 26.57–29.53 | when a man suddenly goes quiet, | C052 old man in a doorway | keep, slow 0.6× |
| 12 | 29.53–32.30 | it doesn't mean he's lost to the world. | C216 rickshaw puller looks at us, traffic streams past | new, slow 0.65×, dissolve in |
| 13 | 32.30–35.83 | Sometimes he's just standing in front of his own old dreams. | C193 balloon seller gazing up | keep, slow 0.7× |

- **Dropped:** C004 / C005 drummer (×3), C031 (tea seller repeat), C043 rickshaw, C223 phuchka, C228 Ram-naam men.
- **Rhyme:** the young balloon seller (shot 7, "change everything") and the old balloon seller (shot 13, "old dreams").
- **Pipeline after approval:** copy the new clips into `raw/b-roll` (+ SOURCES.md), then for each new shot:
  - shot render (crop, denoise, stabilise; shot 6 keeps its camera move);
  - grade (cine look), skin anchor, deflicker;
  - slow-mo retime as the last step (deflicker needs the native 3-frame cycle);
  - B&W pass.
  - Premiere v9 / v9_bw when reel-4 frees Premiere.

## Round 9b — Director: "I don't like the 3rd shot" (2026-10-23)
- Offered 4 replacements for 'wanted to conquer the world' (`analysis/pool_r9/shot3_options.jpg`): C196 arch of light, C014 marching into the gate, stay on the dhaki boy, C140 night road. **Director chose: stay on the dhaki boy.**
- C027 has passers-by crossing the lens at 0.5, 1.3, 3.45–3.85, 4.2–4.4, 5.5–5.9 and 7.6–8.9 s (frame-difference scan + `analysis/pool_r9/c027_0-5s.jpg`, `c027_4-9s.jpg`). No clean 4.2 s stretch, so it plays as one shot with one cut hidden under a passer-by:
  - src 1.6–2.97 at 1× ("Ek jo 18 mein", 4.13–5.50);
  - slow 0.6× from 'duniya' over src 2.97–3.65, ending as a passer-by sweeps the lens;
  - cut under him to src 5.75, as another passer-by clears; slow 0.6× to 6.79 (→ 8.37).
- v9 is now **12 shots, 13 different men** (`analysis/edl_v9_proposed.json`, `analysis/pool_r9/storyboard_v9b.jpg`); every other shot is as proposed.

## Round 9 — v9 built (2026-10-23, approved "Approved v9 as revised. Render it, colour and B&W.")
- **New shots** through the v5 pipeline (`tools/render_all_v9.sh`):
  - render list `analysis/edl_v9r.json` + `focus_v9r.json`;
  - `shot_render_v5.py --ver v9 --edl v9r` (stabiliser: C190 and C212 fell back from lock to smooth for margin; C215 / C216 locked);
  - `skin_post.py` (skin hue 27.5–28.5°, sat 0.45);
  - `deflicker.py` → `*_v9c`.
- **Timeline shots:** `tools/v9_build.py` from `analysis/edl_v9.json` builds `*_v9f.mov`:
  - speed segments; slow motion by optical flow (`minterpolate` mci/aobmc), applied after grade + deflicker;
  - 5-frame handles for the 886 dissolve;
  - nat sound silent under slow motion.
  - Kept 1× shots are windows of their v6 renders (json only).
  - Speeds: 2 0.6× from 'duniya' (hidden cut at f203 under a passer-by), 5 0.67×, 6 0.68×, 10 0.6×, 11 0.55×, 12 0.7×.
- **Fixes found in my own QA:**
  - `frame_scan` flagged shot 5 at 17.63–17.9: a passer-by in a white shirt crosses the lens at C222 src 3.45 and the interpolation smeared him. → shot 5 source 0.42–3.39 at a uniform 0.67×. The camera now reaches the second man at f468 ('Dusra' 463).
  - Shot 6 → 0.68× and shot 11 → 0.55× to fit their renders; shot 11 keeps 5 dissolve frames.
- **B&W:** `bw_render.py --src v9f --out bw9` on shots 2–12; shot 1 = `01_C152_bwfade6` (colour → gold fade).
- **Previews** (Premiere still held by reel-4): `renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4` and `_v9bw_preview.mp4`, 35.83 s, −0.7 dB.
- **Measured:**
  - `frame_scan` 0 flags in 1075 frames;
  - flicker tile-max per shot ≤ 2.1 % (v5: up to 11.8 %);
  - B&W chroma after shot 1 ≤ 0.14.
- **brief.md → v9** (gate step 0); shot list `analysis/shots_v9.json`; review gate running.

## Round 9 — Review gate loop 1 (`analysis/review_v9.md`): FAIL, 1 blocker / 4 major / 3 minor
1. **Blocker, shot 2 (C027): smear from interpolated passers-by, hidden cut not hidden — fixed.**
   - No interpolated crossings now: 1× src 1.6–2.97 on "Ek jo 18 mein", then a **hard cut on 'duniya'** into slow-mo (0.54×) on a clean stretch of the same take (src 6.0–7.55; passers-by at 5.5–5.9 and 7.6+).
   - C027 re-rendered to 7.9 s for it.
   - It's a deliberate jump into slow-mo on the word; the director is asked at Checkpoint 2.
2. **Major, shot 2: the boy's face is crushed — fixed.** `tools/shot_trim.py`: luma toe lift (a 2.0, k 0.08; faces at 0.06 → ≈0.12, mids barely move), luma 0.265.
3. **Major, colour differs and skin is off — partly fixed, partly disputed.**
   - **Disputed:** person-gated skin on the v9 preview (the round 5 metric: person matte ∩ skin box ∩ HSV window, robust median, 5 frames per shot) puts every face at 26.4–30.4°, sat 0.43–0.48. The exception is shot 12, at 22.8° / 0.50 on its new slow-mo window, which is real.
   - **Fixed, shot 12:** mid_rgb trim [0.97, 1.04, 1.0].
   - **Kept as approved:** the higher saturation and red cast on shots 7 (C201, red balloons) and 10 (C052, orange wall) are scene colour, unchanged from v5 / v6, which the director approved after round 5.
   - **Fixed, new shots, now harmonised to the reel:**
     - 2 C027 and 3 C190: sat ×0.72 (0.63 → ~0.45);
     - 3: red cast down;
     - 9 C215: green tube light neutralised (mid R/G 0.90 → ~1.0).
4. **Major, shot 5 (C222): soft, dark, cold — fixed as far as the source allows.**
   - The source is soft: raw Laplacian variance 149 against ~1200 on other shots; our render 193, after interpolation 157.
   - Trim: shadow lift 1.2, warm [1.08, 1, 0.93], luma 0.26, luma sharpen 0.8.
   - Running the pan at 1× is impossible: the shot needs 4.4 s and the take has 3.0 s before a passer-by.
5. **Major, shot 6 (C212): weak in-point (the back of a boy's head) — fixed.** It starts at src 2.3, after the boy has cleared, at 0.5×.
6. **Minor, residual flicker on 2 / 3 / 4 / 9 — fixed.** Second deflicker pass, 3 iterations (`*_v9d`).
7. **Minor, the 886 dissolve double-exposes two heads — intended** (brief-approved turn). The director is asked at Checkpoint 2 whether to keep it or hard-cut.
8. **Minor, true peak −0.7 dBTP on the guide track — intended.** The guide only; the `_IG` export has VO muted and the `_mix` is for review.
- **Tool gap:** `frame_scan.py` gave 0 flags on a half-second full-frame optical-flow smear. → CR-20261021-pujo-ki-asolei-sobar-vfr-jump-qa (item: smear / ghost check).

## Round 9 — Review gate loop 2 (`analysis/review_v9_loop2.md`): FAIL, 0 blockers / 4 major / 4 minor (gate limit reached: fixes verified by the editor, no 3rd blind loop)
Loop-1 fixes confirmed by the reviewer: no smear on the shot 2 crossings, skin and B&W pass, cuts on onsets, nobody repeated.
1. **Major, shot 2 "camera jerk" at f165 — fixed.**
   - It is the deliberate cut on 'duniya' (src 2.97 → 6.0, not continuous). Near-identical framing made it read as a glitch.
   - Now a **cut-in**: the slow-mo part is punched in 1.12× on the boy, so it reads as a cut into slow motion.
2. **Major, shot 6: optical-flow swirl on the balloon turn — fixed.**
   - Tested `minterpolate` mci mb16 / mci mb8 + search 64 / blend on the turn (`analysis/review_v9/balloon_test.jpg`). The source frames themselves are motion-blurred there (fast hand at 1/60 s).
   - Now: mb 8 + search 64 for the shot, and **frame blend through the turn** (f584–606), which reads as motion blur instead of a swirl.
3. **Major, shot 2: drumstick ghosts in the slow-mo — reduced, rest intended.**
   - Finer motion vectors (mb 8, search 64; `analysis/review_v9/sticks_test.jpg`). All three methods double thin, fast sticks.
   - A slower factor would need more clean source than the take has (passers-by at 5.5–5.9 and 7.6+).
   - This is the limit of slow motion synthesised from 30 fps; flagged to the director.
4. **Major, shot 7 (C201): grade jump — fixed.** Trim, saturation ×0.72 and red cast down, skin protected.
5. **Minor, shot 10 orange backdrop — intended.** The approved v5 shot; the backdrop hue sits inside the skin band, so it can't be desaturated without greying the old man's face.
6. **Minor, residual flicker 3 / 4 / 8 / 9 (≤ 1.6 % quadrant) — intended.** At the visibility threshold after 2 passes; the director is asked to watch shot 4 on a phone.
7. **Minor, shot 5: picture lags 'Dusra' — fixed.** The pan eases in (0.9× → 0.8× → 0.49×) and settles on the second man near f472.
8. **Minor, true peak −0.7 dBTP on the guide — handled at the Premiere `_mix` export** (A3 −0.5 dB); `_IG` has VO muted.
- **Tool gap:** `frame_scan` has no translation-discontinuity test (missed the f165 jump). → added to CR-20261021-pujo-ki-asolei-sobar-vfr-jump-qa.

## Round 9 — Editor verification after loop 2 (2026-10-23)
- Shot 2: the cut-in on 'duniya' reads as a size change (f165 diff 31 = a cut; framing 1.12×).
- Shot 5's first ease (0.8 → 0.49×) made a visible speed step at f472 (3.8 → 2.0 px/frame). → six-step ease 0.9 / 0.85 / 0.75 / 0.65 / 0.55 / 0.51; the largest frame-to-frame speed change is now 0.74 px/frame.
- Shots 6 and 7 checked on the sheets: no swirl on the balloon turn; shot 7's toys and balloons are calmer, skin unchanged.
- **Final previews:** `renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4` and `_v9bw_preview.mp4`, 35.83 s, −0.7 dB. `frame_scan` 0 flags; skin 25.7–30.4° on all 12 shots; flicker tile-max ≤ 2.1 %; B&W chroma ≤ 0.14 after shot 1.
- **Premiere:** still held by reel-4 (`uski-aankhein.prproj`). The v9 / v9_bw sequences and the 4 exports wait for the director's go.

## Round 10 — Director notes on v9 (2026-10-23): "The coloured shots look better but a few sections are a little dark; the shot between 0:05–0:07 looks very dark, not clear; additionally the transition is weird from normal motion to fast (slow)."
1. **Shot 2 (0:05–0:07, dhaki boy, slow part) dark / unclear — fixed by re-picking the moment.**
   - The v9 slow part (C027 src 6.0–7.55) has the boy turned away and in shadow.
   - The same take at **src 19.9–22.8** shows him face-on, lit by the lamp, with no passers-by (C027 frame-diff scan + `analysis/review_v9/c027_9-23s.jpg`).
   - Rendered as `14_C027_*` (pipeline + skin + deflicker); trim with toe lift 3.0, luma 0.28. Face visible, luma 0.27–0.28 (v9: 0.26 with the face crushed; `analysis/review_v10_face.jpg`).
2. **"Transition weird from normal to slow" — fixed.**
   - The v9 jumped from 1× to 0.54× in one frame, on a 1.12× cut-in.
   - Now: a cut on 'duniya' to the face-on angle, then the speed **eases** over 15 frames (0.95 → 0.87 → 0.79 → 0.72 → 0.66), settling at 0.62×.
   - No punch-in. The builder gained per-segment source renders (`"json"` in the segment).
3. **"A few sections a little dark" — lifted.**
   - Toe lift + luma target 0.275 on 3 C190, 4 C032, 5 C222 (lift 1.6), 6 C212, 9 C215; shot 7 to 0.27.
   - Shots 1, 8, 10, 11, 12 were already 0.26–0.27.
- Output: `renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4` + `_v10bw_preview.mp4` (EDL still `analysis/edl_v9.json`, updated; same cut and timing).

## Round 10 — Review gate loop 1 (`analysis/review_v10.md`): FAIL, 0 blockers / 3 major / 6 minor
Director notes 1–3 confirmed by the reviewer: levels flat 0.29–0.30, the room lit, the speed change eased with no step. What remains is face exposure and grade consistency.
1. **Major, shot 2: the drummer's face still in shadow (0.17) — fixed.** `shot_trim.py` gained **`face_lift`**:
   - exposure raised only inside person matte × skin hues, local luma pulled toward 0.36, gain ≤ 2.2;
   - the background barely changes (`analysis/review_v10/face_lift_test.jpg`).
2. **Major, shot 6: ghosting on the balloon turn — fixed.** The turn (src 2.25–2.65, the hand-motion peak) now plays at **1×**, then eases 0.85 → 0.7 → 0.58 → 0.48 → 0.41×. No blend.
3. **Major, warm / cool alternation 7 → 8 → 9 → 10, saturation high on 2, 3, 7, 10 — fixed.**
   - Cause: my hue-only skin protection also shielded the orange and pink walls (they sit in the skin hue band), so the trims never reached them.
   - **New `protect: person`:** only skin inside a person matte is held to the anchor.
   - Shots 7 and 10 pulled toward the middle: mid R/B gains [0.83, 1, 1.12] and [0.86, 1, 1.1], sat ×0.66 / ×0.75.
   - Shots 8 and 9 warmed: [1.12, 1, 0.91] and [1.14, 0.98, 0.92].
   - Shots 2 and 3: sat ×0.65 with the person protected.
4. **Minor, shot 5: second man's face cut by the frame edge at 'Dusra' — fixed.** The pan front-loaded (0.95 → 0.9 → 0.78 → 0.62 → 0.5 → 0.35×), arriving about 7 frames earlier.
5. **Minor, shot 2: foreground heads at the right edge — fixed.** The face-on angle is scaled 1.08×, centred left.
6. **Minor, shot 2: drumstick doubling — intended.** The limit of 30 fps slow-mo; not visible at phone size.
7. **Minor, duplicated first frame of interpolated shots — fixed in `v9_build.py`.** The repeated first frame is dropped.
8. **Minor, black floor below 0.025 on 7 / 8 / 11 / 12 — fixed.** `floor: 0.025`.
9. **Minor, shot 12: backlit profile (face 0.13) — fixed.** `face_lift` with target 0.28, cap 1.5.
- Not judgeable from a preview: BT.709 tags. The Premiere export goes through `verify_render.py`.

## Round 10 — Review gate loop 2 (`analysis/review_v10_loop2.md`): FAIL, 0 blockers / 2 major / 4 minor (gate limit reached: fixes verified by the editor)
Loop-1 fixes confirmed: grade consistent (mid R/G 1.02–1.36, sat 0.32–0.50), shots 5 / 8–12 pass, cut on 'duniya' clean, no duplicate frames, B&W no defects.
1. **Major, shot 2b: the face-on slow-mo smeared ("painted" face) — fixed.**
   - Motion-compensated interpolation was warping a soft, low-light face. Now frame blend (`mi_mode=blend`); the source's own motion blur hides the step.
   - Face lift gentler (target 0.32, cap 1.8).
   - Verified on face crops (`analysis/review_v10/faces_after.jpg`): eyes and moustache read; the remaining softness is the camera original.
2. **Major, faces in the toe on 7 (father), 5a (young man), 2a — fixed.** `face_lift` on all three (targets 0.28 / 0.26 / 0.30). The father's face reads on the crop sheet.
3. **Minor, shot 6: the hand doubles at 0.39× (19.2–20.3) — intended.** The turn itself plays at 1×. What remains is the slow hold on a moving hand; the director is asked.
4. **Minor, shot 2 near-sepia (R/G 1.37) — fixed.** Cast pulled toward neutral (mid [0.9, 1, 1.08]), person protected.
5. **Minor, skin saturation spread — disputed.** The person-gated median puts every face at 0.42–0.49 (target 0.45). The reviewer sampled patches.
6. **Minor, true peak −0.7 dBTP on the guide — at export.** A3 −0.5 dB on the Premiere `_mix`.
- **Previews:** `renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4` and `_v10bw_preview.mp4`, 35.83 s; `frame_scan` 0 flags; no duplicate frames.

## Round 11 — Director note on v10 (2026-10-23): "In the coloured variant why does everything look so over-processed and not natural; the dhaki image isn't coming out great in slow-mo either"
**Why it looks processed:** each shot went through about a dozen stacked steps:
1. heavy temporal denoise (hqdn3d 1.5:1.2:6:4.5): waxy skin, smeared motion;
2. clarity 0.55 + local contrast 0.20 (+ a 0.8 sharpen on C222): crunchy halos, an HDR look;
3. per-shot auto-levels to one target (p02 / p50 / p98 → 0.035 / 0.30 / 0.86): every shot the same flat density;
4. near-full white balance (power 0.9) + forced cast match to one R/G B/G: every scene's light pushed to the same colour (the blue street at C216 turned orange);
5. the cine look at 100 %, skin anchor at 100 %, skin post-pass;
6. round 10's face lifts and shadow toe lifts: glowing faces, milky blacks.

The slow-mo is synthesised from soft, low-light 30 fps handheld footage, so it can't look like real high-speed slow motion.
**Proposal: natural mode** (`shot_render_v5.py --natural`):
- denoise hqdn3d 0.8:0.6:2:1.5;
- white balance half-way to neutral (power 0.45);
- half the auto-levels;
- clarity 0.12 detail / 0 local;
- look mixed at 60 %;
- cast match strength 0.35;
- saturation cap 0.40;
- skin anchor at half strength;
- halation 0.05, vignette 0.10, grain 0.006;
- no face or shadow lifts.

Deflicker and stabilisation stay.
- **Test on 4 shots** (C027 face-on, C032, C201, C216): `analysis/look_n1/compare.jpg` (camera original / v10 / natural).
- **Dhaki motion options:** `analysis/look_n1/dhaki_A_real_speed.mp4` (both angles at 1×, cut on 'duniya') vs `dhaki_B_slow_0.8x.mp4` (face-on at a gentle 0.8× frame blend). Both use natural-mode renders, no deflicker yet.

## Round 11 — Director answers (2026-10-23)
- **Look: "Natural, but warmer and matched".** New `--natural-matched` mode:
  - white balance power 0.6, auto-levels at 65 %, cast match 0.6, look at 75 %, skin anchor ^0.75, saturation cap 0.38;
  - denoise hqdn3d 0.8:0.6:2:1.5, clarity 0.12 / 0;
  - halation 0.06, vignette 0.12, grain 0.006;
  - no skin post-pass, no face or shadow lifts.

  All 13 source shots re-rendered (`*_m1`), deflickered (`*_m1d`); EDL `analysis/edl_v11.json`, built `*_v11f`.
- **Dhaki: "Slow where needed".** Shot 2 at 1× on "Ek jo 18 mein"; on 'duniya' a cut to his face-on angle, easing 0.95 → 0.9 → 0.85 into a gentle **0.8×** (frame blend, no motion warping).
- Slow motion stays where the shot is calm: 5 (the dreamer pan), 6 (young balloon seller; the source is too short for 1×), 10, 11, 12.
- B&W rebuilt from the new renders (`*_bw11`); shot 1 keeps the approved colour → gold fade.

## Round 11 — Review gate v11 loop 1 (`analysis/review_v11.md`): FAIL, 0 blockers / 4 major / 5 minor
The reviewer compared all 12 shots against their camera originals. Passes: 4, 7, 8, 9, 11, 12 (natural, detailed, warm-matched); B&W §4; cuts; 13 men.
1. **Major, shot 6 (C212): optical-flow warp on the balloon / hands — fixed by removing the slow-mo.**
   - The boy blocks the frame until src ≈ 2.3 (`analysis/review_v11/c212_0.4-4.jpg`). That leaves 1.75 s of clean seller for a 3.3 s line: any slow-mo means heavy interpolation.
   - Now **real speed from src 0.75**: "The first said," on the boy watching the balloons; the seller appears on "One day I'll change everything". C212 re-rendered.
2. **Major, shot 5: tail waxy at 0.35× — fixed.**
   - Ease 0.85 → 0.72 → 0.61× (slowest 0.61), starting at src 0.3.
   - Re-rendered with spatial-only denoise (hqdn3d 0.6:0.5:0:0).
   - Trade-off: the camera reaches the second man about 8 frames after 'Dusra' (minor).
3. **Major, shot 3: young priest's face 0.077 vs 0.20 on the original — fixed.** `face_lift` target 0.18 (the original's level), cap 2.
4. **Major, brightness normalised to 0.27 on every shot — fixed.**
   - Per-shot target = ½ original + ½ 0.28 (`analysis/review_v11/luma_targets.json`): hook 0.27 → 0.36, tea seller → 0.33, shot 6 → 0.35, doorway → 0.32, others 0.28–0.32.
   - Applied with a new `luma_gamma` op (a power curve, so highlights don't clip).
   - Shot 2 is exempt: the director asked for it brighter in round 10.
5. **Minor, shot 10: orange wall reads as a filter — fixed.** mid [0.92, 1, 1.05], sat ×0.85, person protected.
6. **Minor, shot 6: green neutrals — fixed.** mid [1.02, 0.96, 1.02], person protected.
7. **Minor, shot 2: the angle change reads as a jump cut with a blurred head at the edge — partly fixed.** The face-on angle starts at src 20.3, after the child clears. The cut itself is the director's pick.
8. **Minor, shot 2: faint stick ghost at 0.8× blend — intended** (the director chose "slow where needed").
9. **Minor, true peak — at the Premiere `_mix` export.**

## Round 11 — Review gate v11 loop 2 (`analysis/review_v11_loop2.md`): FAIL, 0 blockers / 4 major / 3 minor (gate limit reached: fixes verified by the editor)
Loop-1 fixes confirmed: brightness follows the originals, shot 6 at 1× clean, shot 5 lands on 'Dusra' (f464), no flicker, B&W passes.
1. **Major, shot 2 reads as a sepia filter — fixed.**
   - C027 re-rendered with per-shot natural overrides (`wb_k` 0.4, `cast_k` 0.25, `look_mix` 0.45), so the red stage light stays red.
   - The renderer gained focus-json overrides for the natural strengths.
2. **Major, dhaki slow-mo still ghosts / soft — fixed by playing it at real speed.**
   - Synthesised slow-mo on this take failed 4 blind reviews and the director's eye.
   - Now: 1× on both angles; on 'duniya' a cut to the face-on angle (src 19.95–22.82), crop 1.12× centred left, which also cuts the sliced face at the edge (minor 6).
   - Slow-mo stays on 5, 10, 11 and 12, where it is clean ("slow where needed").
3. **Major, shot 12 face grey-olive — fixed / verified.** `skin_post` on C193 (32°, sat 0.45); on the side-by-side with the original the face reads natural brown (`analysis/review_v11/vs_original_final.jpg`).
4. **Major, shot 3 skin over-red — fixed.** `skin_post` on C190 (29°, 0.44); balance trim softened to [0.95, 1, 1.03]; face at the original's level.
5. **Minor, shot 8 teal line — fixed.** `desat_hue` 175° ± 20, ×0.35.
6. **Minor, shot 2 framing — fixed** (see 2).
7. **Minor, brief out of date for shot 6 — fixed** (brief §4 Motion and §5).
- **Final v11:**
  - `renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4` + `_v11bw_preview.mp4`, 35.83 s;
  - `frame_scan` 0 flags, no duplicate frames;
  - luma 0.24–0.35, each shot halfway between its original and 0.28;
  - mid R/G 0.99–1.42 (2 and 3 keep their red light);
  - skin 22–37° (person-gated median).

## Round 11 — v11 approved + built in Premiere + exported (2026-10-24)
- Director: "v11 approved. Premiere is free now, build v11 and v11_bw and export all four files."
- Our project was made active with `open_project`; every script keeps the path guard. Bin `16_V11`: 24 shot files.
- **Sequences:**
  - `Reel_pujo-ki-asolei-sobar_v11` (f84bab33-41d9-4a24-880f-c4aeb7ba5098), from v5;
  - `Reel_pujo-ki-asolei-sobar_v11_bw` (41f0033a-45f4-4a40-82cb-832adf0dc8c2), from v5_bw, with the neutral title and end card.

  In both: V1 / A1 replaced by 12 shots (`analysis/place_v11_batch.json`, `place_v11bw_batch.json`), gaps closed, pushes 100 → 105 % on f0 / 328 / 797 / 886 / 969 (`_es_v1c_motion.jsx` now takes `$.global.PUSH`), Cross Dissolve f881–891.
- Premiere floors fractional source in-points: shots 4 and 6 landed one frame early (48 / 6), set to 49 / 7 by ticks to match the reviewed preview.
- **Readback:** 12 shots end at 1075, 0 problems; 18 subtitles on time; title / end card / VO intact; no stray effects.
- **Exports** (`_es_export.jsx` now takes `$.global.A3_DB`):
  - `renders/exports/pujo-ki-asolei-sobar_v11_mix.mp4` + `_v11bw_mix.mp4`: nat sound kept only on the aarti (f0) and the dhaki (f124) at −26 dB, VO −0.5 dB → −14.6 LUFS, true peak −1.2 dBTP;
  - `_v11_IG.mp4` + `_v11bw_IG.mp4`: VO muted, nat sound only.
- **Verified:**
  - `verify_render.py` PASS on all four (mix profile / ig-quiet), BT.709 tagged;
  - `frame_scan` 0 flags;
  - no duplicate frames;
  - exports vs reviewed previews: mean diff 2.3 / 255;
  - B&W chroma ≤ 0.08 after shot 1.

## Round 12 — Director note on v11 (2026-10-24): "I only have one complaint: the two successive shots of the drummer, can we replace the second shot with the boy selling the jewellery or some other shot?" + "no black and white needed"
- **Shot 2b ("wanted to conquer the world", f165–251) → C028, the young jewellery seller** (raw/b-roll, already copied in round 1).
  - First pick, src 23.0 (he looks out past his stall), dropped: he sits at the camera frame's right edge, so the stabilised window cut his face (`analysis/review_v11/c028_render.jpg`).
  - **Used: src 31.3–34.17**, calm (motion 4–5), face lit, centred, arranging his jewellery.
  - Same natural-matched pipeline: render `15_C028_m1`, deflicker, skin anchor (16.7° → 27°), brightness halfway to the original (0.32).
  - Built as `02_C027_v12f` (2a dhaki 1× + hard cut on 'duniya' to 2b); EDL `analysis/edl_v12.json`.
- **No B&W this round** (director). Colour only.
- Preview `renders/previews/pujo-ki-asolei-sobar_v12_preview.mp4`: `frame_scan` 0 flags, no duplicates; shot 2b mid R/G 1.28, skin 24°, luma 0.31.
- **Premiere:** `Reel_pujo-ki-asolei-sobar_v12` (0a6dfb19-eb71-4eb0-b406-68a5d2b70d14), duplicated from v11. Shot 2 on V1 / A1 replaced (bin `17_V12`). Readback: 12 shots end at 1075, 0 problems, dissolve and subtitles intact. Review gate running before export.

## Round 12 — Review gate (`analysis/review_v12.md`, `review_v12_loop2.md`) + export (2026-10-24)
- **Loop 1** (FAIL, 1 major / 3 minor):
  1. **2b too cool / green — fixed.** Cause: `skin_post` fixed his reddish skin (16.7°) with global gains that pulled red out of the whole frame. New `shot_trim` op **`skin_gain`** corrects skin inside the person matte only. 2b is now mid R/G 1.28, B/G 0.78 (= shot 4), skin 23°.
  2. **Head-down pose — intended** (calm, lit, his work). The standing moments drift out of frame or blur; the director is asked.
  3. **Subtitle cards — fixed.** Card 3 now 4.1333–5.50 (on the cut, was 2 frames early), card 4 from 5.50 (on the f165 cut). `subtitles_v1.json` + Premiere V5 updated.
  4. **Guide bed hard stop — fixed.** `_es_export.jsx` `$.global.A3_FADE` (0.4 s level ramp on A3); the tail now falls −18 → −85 dB.
- **Loop 2** (gate limit): the round-12 change is clean; 14 men; cuts and cards on onsets.
  - The one major, shot 7 (father) darkest in the reel, is carried over unchanged from v11, which the director approved ("I only have one complaint"). Not re-graded, flagged.
  - Other minors (3 / 2a saturation, 5 head crop during the tilt, 12 skin by patch metric, 9 / 12 cast, cards 1–2 over the asura, 6 bystander) are all v11 state, director-approved.
- **Premiere:** `Reel_pujo-ki-asolei-sobar_v12` (0a6dfb19-eb71-4eb0-b406-68a5d2b70d14), shot 2 = `02_C027_v12g`. Readback: 12 clips end at 1075, 0 problems, subtitles match.
- **Exports** (colour only, director: "no black and white needed"): `renders/exports/pujo-ki-asolei-sobar_v12_mix.mp4` (−14.6 LUFS, −1.2 dBTP) + `_v12_IG.mp4` (VO muted).
- **Verified:** `verify_render` PASS on both; `frame_scan` 0 flags; matches the reviewed preview (2.3 / 255); no duplicates.

## Final (2026-10-24)
- Director: "I like the final render, now how do I package it and upload it to Instagram."
- **Upload kit `deliver/`:**
  - `pujo-ki-asolei-sobar_IG.mp4` (= `_v12_IG`, VO muted);
  - `cover.jpg` (00:00:12:15 tea seller, survives the 4:5 / 3:4 grid crop, `cover_grid_check.jpg`);
  - `caption.txt` (approved caption; one line updated for v12: "A young dhaki drummer. A boy minding his jewellery stall.");
  - `UPLOAD.md` (highest-quality upload setting, "Use audio" from the reference reel so the VO starts at 0:00, volumes, cover, caption, credit).
- **Open:** the VO creator's handle for the credit line.
- **Retro written.** 10 CRs filed by this reel (+ updates to 3 other reels' CRs).

## Round 13 — Director note after watching on the phone (2026-10-24): "the video quality is not optimal, a lot of shots have the light flickering issue, and the colour grading seems too dark, the video comes out too dark"
- **Flicker, measured on the v12 export** (10 Hz lock-in per tile, `analysis/review_v12/flicker_export.json`): residual max 4.0–6.0 % on 2a (dhaki) / 2b (jewellery boy), 2.3–2.9 % on 4 (tea seller) / 9 (man on the wall), 1.6 % on 7. Sources flicker up to 13 % (C028); the round-8 settings (2 passes, clamp 15 %, 32×12 tiles) only cut it 2–5×.
  - Sweep on C028: 8 passes, clamp 35 %, 64×24 tiles, temporal σ 3 → residual 6.9 → 1.2 % max, p90 2.95 → 0.69 %. The correction map is no sharper (no edge artefacts); consecutive-frame crops checked (`analysis/review_v12/deflicker_tst6_check.jpg`, `deflicker_tst7_face.jpg`).
  - Re-run on every 30 fps shot (`tools/deflicker_v13.sh` → `*_m2d`; skin post-pass → `*_m2s` on C190 / C193). `deflicker.py` gained `--sig`.
- **Brightness:** options sheet (`analysis/review_v13/brightness_options.jpg`): current / A +½ stop / B +1 stop. **Director chose A.** Every shot's luma target × 1.25 by a power curve (highlights kept); trims `v13_*` → `*_m2e`. EDL `analysis/edl_v13.json`, build `*_v13f`, preview `renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4`.

## Round 13 — Review gate v13 loop 1 (`analysis/review_v13.md`; reviewer on Sonnet, Fable was out of credits): FAIL, 1 major / 5 minor
1. **Major, shot 9 (C215) flicker ≈ v12 level (0.84 % mean tile) — root cause found and fixed.**
   - A second pass, a Wiener floor, a frame-wide pass and a clip mask all left it unchanged.
   - Diagnosis: the corrected output is flat **in linear light** (model and output agree), but not **in display brightness**. Each tile mixes non-flickering ambient light with flickering lamp light, so a per-tile gain solved in linear light under-corrects the mid-tones the eye sees.
   - **Fix:** `deflicker.py --display` (estimate and correct in code values) + `--grid 160x90 --sps 1.0`.
   - C215: 0.76 → **0.14 %** mean tile, global 0.53 → 0.06. C032: 0.69 → 0.16 %.
   - The correction map is no sharper; consecutive-frame crops of the pouring hands are clean (`analysis/review_v13/deflicker_ty6_hands.jpg`).
   - Re-run on all 30 fps shots → `*_m4d`.
2. **Minor, residual on 4 / 3 — fixed** by the same change.
3. **Minor, blacks lifted on 1 / 6 (11's sky) — fixed.** New `black_target` op: after the brightness curve, the darkest 1 % is pinned at 0.03 on every shot.
4. **Minor, 7 still darkest — fixed.** Extra lift: 7 ×1.25 (+⅓ stop); 9, 3, 2a ×1.1.
5. **Minor, 2a orange vs 2b cool — fixed.** 2a mid [0.94, 1, 1.04], person protected.
6. **Minor, subtitle halo margin over bright backgrounds — intended.** Readable per the reviewer; the cards are approved.

## Round 13 — Review gate v13 loop 2 (`analysis/review_v13_loop2.md`): FAIL, 1 major / 5 minor (gate limit reached: fixes verified by the editor)
Both director notes confirmed: flicker gone or invisible (whole-frame swing < 0.5 % on every shot); every shot brighter with deeper blacks and no burnt whites.
1. **Major, shot 8 (C213): a thin teal band crawls down the dark cabinet — fixed.**
   - It's in the camera original (an LED's rolling-shutter beat), likely part of the director's "light flickering".
   - A temporal median (11 or 41 frames) couldn't remove it: the band stalls.
   - New `tools/band_remove.py --inpaint`: per frame and per 90 px column strip, rows where a teal stripe stands out of a 41-row running median are filled by vertical interpolation. Gone in every sampled frame; cabinet texture kept (`analysis/review_v13/band_remove_check.jpg`).
2. **Minor, shot 5 the darkest (4→5 −20 Y) — fixed.** Extra ×1.15.
3. **Minor, dim faces on 2a / 3 / 7 / 12 — fixed.** `face_lift` (2a 0.30 / cap 1.4, 3 0.26 / 1.6, 7 0.28 / 1.5, 12 0.26 / 1.4).
4. **Minor, subtitle contrast over bright garments (6, 10) — intended.** Legible; the cards are approved.
5. **Minor, red channel clipping on saturated reds (7 balloons ~4 %, 8, 3, 6) — fixed.** Highlight shoulder knee 0.8 on those shots.
6. **Minor, skin spread (2a / 3 orange, 12 cheek) — unchanged.** Same as the approved v12.
- Output: `*_m5e` / `09_C213_m5f`, build `*_v13h`, preview `renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4`.

## Round 13 — v13 exported (2026-10-24)
- Premiere `Reel_pujo-ki-asolei-sobar_v13` (bfd7d6ba-ebfc-49c4-8e7f-4763d0fec0b0): final media (`*_m5e`, `09_C213_m5f`, builds `*_v13h`; bin `20_V13c`). Readback: 12 clips end at 1075, 0 problems; pushes, dissolve and 18 subtitles intact.
- **Exports:** `renders/exports/pujo-ki-asolei-sobar_v13_mix.mp4` (−14.6 LUFS, −1.2 dBTP, bed fade) + `_v13_IG.mp4` (VO muted). `verify_render` PASS on both (30 fps, BT.709); `frame_scan` 0 flags; matches the preview (1.2 / 255); no duplicates.
- **Measured on the export:**
  - flicker ≤ 0.38 % mean tile on every shot (v12: up to 0.97 %; peaks were 4–6 %);
  - mean luma 0.408 (v12 0.31);
  - blacks at true black;
  - highlight clipping ≤ 0.5 % on 12 of 13 shots (shot 7's balloons ~1 %).
- **Set up for posting (2026-10-27), not yet shared.** Set up on the director's iPhone via iPhone Mirroring (IG photo access granted for the one video; Jaago 17 %, fade-out 3 s; cover A1; caption typed key by key without "?" and 🎙️, which mirroring can't send). Correction: it was NOT yet published; the Share screen was still open at 19:39. The caption was then edited in place: 'This Durga Puja, I filmed…' and the AI credit line.
- **v19 (2026-10-27): @abhii.jpgg gave the director permission to use his original audio.**
  - The director chose to split the voice from the song and add "Jaago" licensed from IG.
  - demucs htdemucs, two stems, in a temp venv (scratchpad, not the studio's). Stems in `audio/stems/htdemucs/ref_audio_vo/`. The vocal stem is silent in the pauses: 40.6 dB separation, no sung notes left.
  - `tools/vo_orig_build.py`: high-pass + gentle gap expander on the stem; v13 bed fade; over the v13 natural sound; static gain to −14 LUFS; muxed on the v13 IG picture (original subtitles = his words). Export `renders/exports/pujo-ki-asolei-sobar_v19_IG.mp4`.
  - Fixed one bug: `-shortest` dropped 4 end frames. Now `apad` + `-t 35.8`, so 1074 frames.
  - `verify_render` PASS: −14.3 LUFS, −2.5 dBTP, audio = video 35.800 s. Envelope correlation with the reference 0.755 at 0 ms lag.
  - Upload kit:
    - `deliver/pujo-ki-asolei-sobar_IG.mp4` = v19;
    - caption credit "🎙️ Voiceover: @abhii.jpgg (used with permission)";
    - `UPLOAD.md`: add Jaago at ≈15 % with a 3 s fade-out;
    - `dm_abhii.txt` removed; `vo_script.md` moved to `analysis/vo_hi/`.
- **v18 approved (2026-10-27).** Upload kit updated:
  - `deliver/pujo-ki-asolei-sobar_IG.mp4` = v18_IG;
  - `UPLOAD.md` rewritten: VO in the video; optional "Jaago" (Lifafa) from IG's library at 10–15 % under it; no trimming;
  - `caption.txt` credit is now "🎙️ Words: @abhii.jpgg · voiced by me";
  - `dm_abhii.txt` is now a courtesy note about using his words.

  The recorder server is stopped. Nothing is posted yet: the director posts from the phone.
- **v18 (2026-10-27): the director on v17: "still nasal, lacks the calm deep effect".**
  - Diagnosis (1/6-octave spectra vs the reference): v17 was +2.4 st above the reference's pitch and 3–5 kHz brighter (edgy / nasal). The reference is soft on top (−6 dB at 9–11 kHz vs v17) and warmer at 450 Hz.
  - v18: Praat "Change gender" −5 st, formants ×0.93, range ×1.1. Half-octave smoothed match EQ (`--eqmode smoothmatch --eq 0.85`, +3 dB proximity shelf below 130 Hz); darker, slightly larger room (`--room dark`). Placement and slowdowns as v17; subtitles patched as v17.
  - Measured vs the reference:

    | | v17 | v18 |
    |---|---|---|
    | Tone difference, 150 Hz–10 kHz, mean | 2.6 dB | 0.9 dB |
    | Tone difference, max | 13.8 dB | 3.4 dB |
    | Pitch offset | +2.4 st | +0.4 st |

  - `verify_render` PASS.
  - Limit: a laptop-mic take carries its own nasal resonance. A re-take on the iPhone mic, close and lower, would get closer than any processing.
- **v17 (2026-10-27): the director's notes on v16a (picked v16a).**
  1. **Hiccup in "18 saal ki umr mein":** v14–v16 split line 2 before 'duniya' and inserted 0.27 s. Now one unbroken phrase from 4.44 s, with 'duniya' still on the f165 cut.
  2. **"achanak se chup ho jaata hai" rushed / unclear:** phrase 8b slowed to 0.9×.
  3. **Last line rushed / unclear:** 10b slowed to 0.93× and starts 0.1 s earlier (ends 35.78).
  4. **Nasal throughout:** v16a's per-band auto EQ was jagged (±3 dB alternating), which coloured the voice. Replaced by a smooth EQ: +3 dB @170 Hz, −3.5 dB @1 kHz, −1 dB @1.9 kHz, +2 dB @3.8 kHz, +2 dB @9 kHz. Nasal-vs-chest went from −6.1 dB (v16a) to −8.9 dB (reference −8.1).
  5. **Clarity:** lighter denoise and de-ess. Pitch via Praat "Change gender" (−3 st, formants ×0.97, range ×1.2).
  6. **Subtitles to his words:** take 6 transcribed (`analysis/vo_take06_asr`). Cards re-worded:
     - card 10 "The first said," → "The first one says,";
     - cards 17–18 → "Sometimes he's just / lost in his own old dreams."

     Rendered with `tools/sub_card.py`, fitted to the old cards within ~5 px. Patched into the export by `tools/sub_patch.py`: clean background from the shot renders, feathered band only; handle and picture untouched (re-encode difference 2.2/255). Record in `analysis/subtitles_v17.json`.
  - **Premiere v13 still has the v1 wording.** Update V5 there before any new Premiere export.
  - Export `renders/exports/pujo-ki-asolei-sobar_v17_IG.mp4`. `verify_render` PASS (15.8 Mb/s, −14.3 LUFS, −2.4 dBTP).
- **v16a / v16b = gentler matches (2026-10-27).** The director found v15 "too processed / synthetic".
  - `tools/vo_gentle.py` keeps the real waveform: v14 placement (no timing warp), Praat PSOLA pitch (formants untouched), partial auto EQ, 1.6:1 compression, room tail.
  - v16a: −3 st, intonation range ×1.2, EQ 60 %. v16b: −2 st, range ×1.0, EQ 50 %. `verify_render` PASS on both (−14.3 LUFS).
  - The director also allowed an AI re-creation "if needed". The ElevenLabs key is still invalid (401). Boundary: AI may rebuild the director's own voice, but never clone @abhii.jpgg's voice without his consent.
- **v15 = take 6 matched to the reference voice (2026-10-27).** The director asked to match pitch, delivery and effect in every aspect. Built by `tools/vo_match.py` (WORLD vocoder in `renders/_pylib`).
  - Pitch −5.0 st, with the reference's F0 contour transferred per phrase (strength 0.85, capped at ±5 st).
  - Syllable timing DTW-warped to the reference (strength 1.0); formants −0.9 st (K 0.95, best envelope fit).
  - Auto 1/3-octave matching EQ (lows capped at +4 dB because of the reference's bed); 1.8:1 compression; small-room tail; room tone.
  - Measured against the reference:

    | | v14 | v15 |
    |---|---|---|
    | Mean pitch offset | +5.4 st | +0.2 st |
    | Median absolute pitch offset | 5.4 st | 0.8 st |
    | F0 contour correlation | 0.49 | 0.67 |
    | Centroid (reference 1062 Hz) | 1268 Hz | 1027 Hz |
    | DTW timing offset, median | 116 ms | 81 ms |

  - Plots: `analysis/vo_v15_pitch.png`, `analysis/vo_v15_spectro_line1.png`.
  - Export: `renders/exports/pujo-ki-asolei-sobar_v15_IG.mp4`. `verify_render` PASS (−14.3 LUFS, −2.5 dBTP).
  - Risk: vocoder texture; not checked by ear. Fallbacks: `--inton` / `--timing` lower, or v14.
- **v14 = director's VO, take 6 (2026-10-27).**
  - Recorded in `tools/vo_recorder` (Chrome, MacBook mic, headphones: guide bleed −45 dB). Built by `tools/vo_build.py` → `audio/vo_director/vo_take06_final.wav` + `renders/exports/pujo-ki-asolei-sobar_v14_IG.mp4` (v13 picture copied, new audio).
  - Placement: 17 phrases put on their slots, cut words on the cuts (duniya f165, sirf ghar f328, bas is mahine f693, jab koi mard f797); line 7a at 1.07×; internal pauses trimmed on lines 4 and 10. Details in `analysis/vo_place.json`; plot in `analysis/vo_v14_alignment.png`.
  - Polish: high-pass, FFT denoise, de-ess; EQ matched to the reference (within ±1 dB from 500 Hz to 8 kHz; the reference's 200–500 Hz and 8–12 kHz carry its music bed, so not chased fully); 2:1 compression (level swing 2.4 dB vs reference 3.1); small-room reverb at a low mix; room tone at −62 dB under the gaps.
  - Mix: over v13's natural sound, static gain. `verify_render` PASS: −14.3 LUFS, −2.9 dBTP, 30 fps, BT.709.
  - Awaiting the director's review. On upload, add "Jaago" (Lifafa) from IG's library low under the voice, or no music.
- **Director's own VO (2026-10-27).** The director will record the lines himself.
  - Record-along guide: `renders/guide/record_along_guide.mp4` (`tools/record_guide.py`). Teleprompter in Hinglish, slot bars with ticks on the cut words, the reference voice at −6 dB as a pace guide, a CLAP cue for sync.
  - Script: `deliver/vo_script.md` (Hinglish, from a local whisper-medium transcription `analysis/vo_hi/`, corrected by hand); line slots from the measured onsets and pauses.
  - Credit: the words are still @abhii.jpgg's, so credit "words: @abhii.jpgg".
- **Audio blocker found at posting (2026-10-27).**
  - The reference reel's Instagram audio is the song "Jaago" by Lifafa (IG library track, 0:42). @abhii.jpgg spoke his voiceover over it, so "Use audio" gives only the song, not the VO the cut and subtitles follow.
  - Director chose to **ask @abhii.jpgg for permission** first. DM draft: `deliver/dm_abhii.txt` (the director sends it).
  - If he agrees: separate his voice from the bed (demucs, in a reel-local venv), bake the VO into a new IG export, and add "Jaago" from IG's library underneath so the music stays licensed.
  - The caption credit then becomes the voiceover → @abhii.jpgg, with music attributed by IG.
  - Posting is on hold until he replies. Found by browsing on the director's iPhone via iPhone Mirroring; one mis-tap saved one of his posts to the director's Saved and was undone at once.
- **Cover redesigned (2026-10-27).** The director asked for a better cover than the bare frame.
  - Options A–D (`analysis/cover/cover_options.jpg`) → the director picked A (rickshaw puller) and asked to make it cinematic.
  - A1 / A2 (`cover_A_compare.jpg`) → **A1 approved**.
  - A1: real frame 41 of `11_C216_m5e`; background −1/6 stop; face key +0.2 stop; S-curve + roll-off; teal / warm split; halation on the lights only; −0.35 stop vignette; grain.
  - Measured: face luma 0.272 → 0.301, mean 0.392 → 0.340, clip 0.12 %.
  - Saved as `deliver/cover.jpg` (`tools/cover_design.py`, `tools/cover_cine.py`).
- **Reference reel (VO source):** https://www.instagram.com/reel/DasO3VRo5co/ by @abhii.jpgg (director, 2026-10-27). Credit filled in `deliver/caption.txt`.
- **Director approved v13 on 2026-10-26** and is uploading from `deliver/` (steps in `deliver/UPLOAD.md`).
- **Upload kit updated:** `deliver/pujo-ki-asolei-sobar_IG.mp4` = v13_IG; new `cover.jpg` (same frame, 00:00:12:15, brighter) + `cover_grid_check.jpg`.

## Friction log
<!-- Pilot reels: one line each time something is slow, fails, needs a guess, a manual step or a workaround. Format: `- [phase] what happened → workaround → CR filed? (CR id / no)` -->
- [0] The director's footage lives in a pool folder (`~/Documents/Media`, 97 clips over 4 shoot days) and they wanted to pick before anything entered the reel. No studio step covers "survey a pool → shortlist → bring in"; `analyze_footage.py` assumes `raw/`. → Ran the analyser on the pool into `analysis/media_survey/` (97 clips in ~7 min), built grouped pick sheets with a reel-local script (`tools/picksheet.py`), and copied only the picks. → CR-20261019-pujo-ki-asolei-sobar-pool-survey
- [0] The director asked to **copy** rather than link (studio default: link). `link_footage.sh` has no copy mode or clip-list mode. → Copied by hand with `cp -pn` plus a `SOURCES.md` line. → same CR
- [0] Reel type changed after Round 1: "no speech, music only" became "use the reference's audio + VO". The interview doesn't ask whether the soundtrack is an existing audio track with a VO (a common IG pattern), and no reel type or rule covers "external VO track as the soundtrack". → Treated it as `hybrid` with the VO as the timing source; the cut follows phrase pauses. → CR-20261019-pujo-ki-asolei-sobar-external-vo-audio
- [1] `transcribe.py`: `Scribe returned 401 … "Invalid API key"` (the ElevenLabs key in `.env` is set but rejected). `gemini_transcribe_fallback.py` needs a local Whisper (none installed: no `mlx_whisper` / `faster_whisper`). → Line timings from burned-in subtitle changes (yellow-text mask on the bottom band) + speech-band (300–3400 Hz) pauses, `tools/vo_timing.py`: 10 lines, both methods agree within 0.1 s. No word-level timings, so every cut sits in a pause. → same CR (+ tell the director the key is invalid)
- [1] `gemini_audio_and_beat_analyzer.py` on VO + bed reports 117.5 BPM and accents that follow the speech, not a music grid. → Ignored the grid; the VO lines drive the cut. → same CR
- [1] No storyboard tool for Checkpoint 1 (in/mid/out frames per EDL row). → `tools/storyboard.py` from `analysis/edl_v1.json`; it caught a bad source range on shot 10 before the director saw it (C193 10.6–14.5 lost the seller's face → 0.0–3.9). → CR-20261019-pujo-ki-asolei-sobar-pool-survey (tools section)

- [1] Brief said "all 30 fps", but C143/C145 are 25 fps (survey summary: C140–C151). Caught while re-planning v1b. → C143 dropped; C145 conformed by interpretation (CLAUDE.md §3). The per-clip fps column is easy to miss in a 41-row table. → no CR (note for retro: storyboard tool should print fps and flag non-sequence rates)

- [1] "Natural depth" has no recipe in the playbook (§A/§B cover grade, vignette, moves; nothing on subject/background separation). → Tonal depth on the look + a reel-local matte defocus bake (`tools/look_preview.py` for stills; `tools/depth_bake.py` to write in Phase 5, reusing `text_behind.py`'s matte step). → CR after the bake is verified in Phase 5

- [3] Depth bake v1 (σ 5, everything outside the person matte blurred) blurred the rickshaw he sat on and the bikes in front of him, which read as fake portrait mode. → v2: σ 3 + distance ramp (no blur below the subject's feet, rising toward the top of frame). Natural on C216 / C213 / C193, 0 scan flags. Blackmagic Cam fps 30.0066 forced to 30 in the bake. No depth-estimation model exists locally (`hyperframes` has only `remove-background`). → CR with the depth recipe
- [3] `hyperframes transcribe` (local word-level timestamps) exists. It would have replaced the dead ElevenLabs key in Phase 1. → add to CR-20261019-pujo-ki-asolei-sobar-external-vo-audio
- [3] At rough-cut start, Premiere had **puja-night-2.prproj** open (active `Reel_puja-night-2_v4c`) while the reel-2 session showed "working", although the director had said no session was using Premiere. → stopped before any Premiere mutation and asked the director; did the depth bakes meanwhile. → CR-20261018-my-reel-premiere-shared-between-sessions (already open; +1 occurrence)

- [3] Closing another reel's open project was denied by the permission classifier even with the director's go, and with that reel marked done. → Opened this reel's project alongside; scripts target it by path. Two open projects make the adjustment-layer click (Project panel focus) and active-project tools riskier. → CR-20261018-my-reel-premiere-shared-between-sessions (+1: the editor can't close another reel's project; the director or the owning session must)
- [3] `add_to_timeline_batch` with EDL times not on frame boundaries left 1-frame gaps (7 of 19 cuts). → Snap EDL times to frames before placing (closed by script this time). → CR: add "quantise the EDL to sequence frames" to skill Phase 3 (folded into CR-20261019-pujo-ki-asolei-sobar-pool-survey's tools section)

- [3] MCP bridge reported `bridge_unavailable` right after a blocking `exportAsMediaDirect` (export itself completed). → `verify_premiere_connection` once, then continued. → CR-20261018-puja-night-2-premiere-session-setup (bridge-drop follow-up, +1)

- [1] Three rounds lost because cuts were placed in VO pauses (the 'cut in the gap' rule from 4b's dead-air logic) while the director expects pictures to change ON the word. The skill has no rule for VO-driven montage cut placement. → measured onsets, cut on them. → CR-20261019-pujo-ki-asolei-sobar-external-vo-audio (+ rule: cut on sentence / clause onsets, never inside pauses)
- [1] The director's footage is spread over 6 'Puja/Pujo' folders (some with trailing spaces in the name). I only searched the one pool folder they named at first. → surveyed all; Oct 19 held the key shots. → CR-20261019-pujo-ki-asolei-sobar-pool-survey (+ search every shoot folder by name pattern before shortlisting)
- [1] The brief's look was planned from a profile default (Warm Film) instead of measuring the reference's grade. The director had to ask for the reference look explicitly. → `tools/ref_look.py` measures the reference and builds a matching LUT. → CR: make 'measure the reference grade' a Phase 1 step (new, below)

- [4] The studio has no depth tooling: iPhone footage needs synthetic shallow DOF for a 'cinematic' brief, and the person-matte defocus (v1d) read as a mild blur, not a lens. → local Depth-Anything-V2 + layered disc blur, baked per shot (~2 s/frame CPU). → CR-20261020-pujo-ki-asolei-sobar-lens-bokeh
- [4] The look is baked into the shot media at the director's request (exact match to the approved stills, no manual LUT load), not on a V3 adjustment layer as CLAUDE.md §2.5 / §3 say. → logged; same CR

- [7b] The review gate caught 6 majors that my own checks passed: halos from the bokeh fill, a melting face late in a shot (I only checked mid-frames), clipped whites, a face in the IG top zone, a repeated set-up. → per-frame person matte + fill fix; check first / mid / last frames of every baked shot, not just mid. → CR-20261020-pujo-ki-asolei-sobar-lens-bokeh (+ QA: check 3 frames per shot)

- [5] `overwriteClip` of a still image uses the default still duration (5 s) and silently overwrote 2 subtitle cards behind it, before `end` was set. → set the projectItem in/out to the wanted length first, then clear. → add to CR-20261018-puja-night-2-extendscript-notes (still-image overwrite)

- [R2] No stabiliser is scriptable here: Warp Stabilizer's Analyze can't be run by script (puja-night-2 CR) and this ffmpeg has no vidstab. → own phase-correlation stabiliser in the shot renderer, with the margin from 4K supersampling. → CR-20261020-pujo-ki-asolei-sobar-lens-bokeh (+ stabilise / denoise / clarity stages)
- [R2] The synthetic bokeh (depth model) was the director's request in round 1 but rejected in round 2 ('not coming out ok'). Monocular depth on night iPhone footage gives plausible but not convincing lens blur. → render without; keep it as an option. → same CR (record as a limit)

- [R2] Premiere switched to another reel's project (reel-4) mid-session without notice; my next import would have gone into their project without the path guard. → guard held; offline preview built. → CR-20261018-my-reel-premiere-shared-between-sessions (+1: a 3rd occurrence; a lock file is overdue)

- [R2] With 3 reels' projects open in one Premiere, a manual Lumetri Look load (director, for reel-4) could land in another reel's project. → read-only cross-check; clean here. → CR-20261018-my-reel-premiere-shared-between-sessions (+1: one project open at a time, or a lock)

- [R4] My first stabiliser was translation-only, and my own check (whole-frame `shake_report`, integer phase correlation) couldn't see roll, zoom wobble or slow sway; the director saw it. → similarity stabiliser + subpixel metric that reports translation / roll / zoom / sway per shot. → CR-20261020-pujo-ki-asolei-sobar-lens-bokeh (finishing section: use the similarity version; measure sway, not only jitter)

- [R5] 'Colour correction' was measured on neutrals and global stats only; skin-tone consistency (what viewers judge) wasn't measured until the director's 5th colour note. A colour-only skin mask also catches warm objects. → person-gated skin metric + skin-anchored correction. → CR: add a skin-tone consistency check (hue ±3° across shots) to colour QA (`colour_report.py`) and the playbook §A2 shot-match step

- [R6] `replace_clip` (preserveEffects) returned `success:false`, "motion scale not restored", while the replacement was correct: Motion, Opacity, timing and in/out all read back identical to the original clip. → verified by a property-by-property readback against v5. → CR-20261021-pujo-ki-asolei-sobar-premiere-ops (item 10)

- [R7] Premiere's active project switched to reel-4's (session running) between my rounds; a 5th time Premiere was held by another reel. → offline preview for review, Premiere build deferred. → CR-20261018-my-reel-premiere-shared-between-sessions (+1)

- [R8] Mains flicker (1/60 s shutter under 50 Hz lamps) reached round 8 before anyone measured it; the director saw it. No studio check looks for a periodic brightness cycle, and ffmpeg `deflicker` is global only (it misses rolling bands and single bulbs). → lock-in scan + per-tile deflicker in the reel. → CR-20261023-pujo-ki-asolei-sobar-mains-flicker

- [R9] Repeats and the slow-mo request: my round-1 rule "one man per voice" put the same drummer on screen 3 times; and slow motion was asked for on a pool that is 100 % 24–30 fps, which no analysis flagged up front. → full-pool index + contact sheets, one man per line, synthesised slow-mo labelled as such. → CR-20261021-pujo-ki-asolei-sobar-director-profile (add: "vary the people; never the same subject twice unless it's a deliberate callback"; "ask about slow-mo at the shoot: 60 fps for any shot you may want slowed")

- [R9] The blind reviewer caught a half-second optical-flow smear (passers-by interpolated in shot 2) that `frame_scan` passed with 0 flags, and that my own 2 fps look missed. → no interpolation across occluders; the gate earned its keep again. → CR-20261021-pujo-ki-asolei-sobar-vfr-jump-qa (smear check)

- [R10] Hue-based skin protection also protected orange / pink walls (they share the skin hue band), so two rounds of grade trims never reached them; two blind reviews flagged the warm / cool alternation. → protection gated by a person matte. → candidate for the colour phase in the playbook (CR-20261020-pujo-ki-asolei-sobar-reference-grade-match follow-up)

- [R11] Correction stacking: every round added a fix on top (denoise, clarity, auto-levels, forced cast, skin anchor ×2, face / toe lifts), each measured as an improvement on its own metric, until the director called the whole thing over-processed. No studio check compares a render against the camera original for "naturalness". → natural mode at partial strengths; original / current / proposed sheet before re-rendering. → CR: a `vs_original` sheet in the colour QA step, plus a cap on stacked corrections

- [R13] The director saw flicker on the phone that the export passed: my deflicker settings (from round 8) left 2–6 % on hard-flickering LED / bulb shots, and "no flicker" from frame_scan and the reviewer was relative to their thresholds, not to a phone screen. The grade also read too dark on a phone (mean luma 0.25–0.36). → stronger deflicker sweep-tuned per measured residual (target ≤ 1.5 % per tile), +½ stop. → CR-20261023-pujo-ki-asolei-sobar-mains-flicker (add: residual target per tile + phone check), CR-20261023-pujo-ki-asolei-sobar-correction-stacking (add: brightness target for phone viewing)

<!-- The editor appends one section per round below: "## Round N — Proposal", "## Round N — Director notes", "## Round N — Changes made". -->

## Instagram package
**Approved 2026-10-21** by the director: hook 1, the caption, these 5 hashtags, cover A (00:00:12:15). Drafted 2026-10-20 (ig-hook-extractor + ig-caption-writer + humanizer rules + hashtag recipe). **Not published**: the director posts. Upload `renders/exports/pujo-ki-asolei-sobar_v2_IG.mp4` and add the reference audio from Instagram's picker, starting at **0:00**.

**First-line hooks (< 125 characters)**
1. **(recommended, shares)** At 18 you want to conquer the world. At 28 you just want this month to work out. *(80 chars; IG3 relatable cold-open: the VO's idea for silent scrollers)*
2. Pujo ki asolei sobar? Is it everyone's, or only everyone who gets the night off? *(80 chars; IG2 reframing question, echoes the on-screen title)*
3. The drummer, the tea seller, the man with the balloons: they work every Pujo night so the rest of us can celebrate. *(115 chars; observational)*

**Caption** (hook 1; ~560 characters, 1 emoji, no em dashes)

> At 18 you want to conquer the world. At 28 you just want this month to work out.
>
> This Pujo I filmed the people who work through the nights.
>
> A young drummer playing in front of the Devi. A tea seller at his counter. A rickshaw puller waiting for a fare. An old shopkeeper behind his jars. A balloon seller standing still under the lights, looking up.
>
> Pujo belongs to all of us. Some of us get to celebrate it, and some of us keep it running.
>
> Pujo ki asolei sobar?
>
> Send this to someone who has been the second man for a while.
>
> 🎧 Audio: [credit the voiceover's creator here]

**Hashtags** (5, sized by judgment: post counts can't be read from here, so check them in the app's search before posting; put them at the end or in the first comment)
- niche: `#pujodiaries` · `#durgapujo2026`
- mid: `#streetportraits` · `#indianstreetphotography`
- broad: `#durgapuja`

**Cover frame:** **00:00:12:15** (12.50 s): the tea seller pouring, with no subtitle on the frame; face and kettle survive the 4:5 profile-grid crop (`renders/stills/cover/cover_options.jpg`). Alternatives: 00:00:07:15 (drummer before the Devi), 00:00:31:27 (Ram-naam men in lamplight).

**Open:** the voiceover creator's handle for the credit line (brief §7).
- Caption edit drafted with an AI-credit line (@claudeai, @adobevideo — both checked on Instagram 2026-10-27: Claude by Anthropic 2.3M; Adobe Video 751K, official; @premierepro is NOT Adobe's) and hashtags 3 Pujo + #claudeai #premierepro: deliver/caption_edit_ai_credit.txt.
- Research 2026-10-27 (hashtag cap, AI disclosure, ranking): hashtags classify the topic more than they add reach, so keep all 5 on Pujo / street photography. The AI credit goes in the caption text + @ tags only (a detailed 'how AI was used' disclosure). Suggested a separate behind-the-scenes reel for the AI audience. `caption_edit_ai_credit.txt` reverted to the original 5 hashtags.
