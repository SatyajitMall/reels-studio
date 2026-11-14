# Project Log

| Field | Value |
|---|---|
| Reel name | uski-aankhein |
| Status | done: v10b delivered (round 6 quality pass); the director is checking it on the phone |
| Reel type | music-montage |
| Playbook | cinematic-montage (override: stock B-roll allowed for the string player, see brief) |
| Arch version | 0.6.0 |
| Pilot | yes |
| Current round | 3 |
| Premiere project | `premiere/uski-aankhein.prproj` (own project, opened alongside pujo-ki-asolei-sobar.prproj, which I never touched) |
| Latest sequence | `Reel_uski-aankhein_v10b` (faef2705-81a1-43bc-9df1-063d0b79d584); v10, v9c, v9b, v9 and v1-v3 kept as rollbacks |
| Latest export | `renders/exports/uski-aankhein_v10b_mix_tp.mp4` (guide) + `uski-aankhein_v10b_IG.mp4` (upload, = `deliver/uski-aankhein_IG.mp4`), from ProRes masters `uski-aankhein_v10b_master_{mix,IG}.mov` |

## Interview — Round 1 (2026-10-20)
- **Name:** uski-aankhein ("her eyes"). Director's folder: `~/Documents/Video /Uski Ankehe/` (one reference clip).
- **Subject:** Durga's eyes.
- **Footage:** mix of all five shoots: `Puja 2026 Oct 15`, `Puja 2026 Oct 16`, `Pujo 2026 Oct 17 `, `Puja 2026 Oct 18 `, `Pujo 2026 Oct 19` (all under `~/Documents/Video `, note trailing spaces). **Not all 30 fps** (survey): Oct15 is 1080×1920 at 24 fps (C001–C012) or 25 fps; Oct16 25 fps; Oct17 C140–C145 25 fps, C152+ 30 fps; Oct18 30 fps; Oct19 30 fps except C021–C024 (24) and C004/C025 (29.3/29.0). Oct16/17/18/19 are 2160×3840 vertical; Oct15 is 1080×1920. Clip ids repeat (Oct15 and Oct19 both have C001–C032), so always name the shoot. Upside-down clips (same rotation metadata as upright ones): Oct15 C008, C023; Oct16 C084, C112, C120–C122, C127, C136–C139; Oct18 C191 (C192 to check).
- **Music:** the reference's own audio (`references/Video-14732.mp4`, 22.1 s). Cut to it; the director adds the IG library audio at upload (`_mix` guide + muted `_IG` export, as puja-night-2 / pujo-ki-asolei-sobar).
- **Stock B-roll:** find a free-licence clip of a bowed-string player (sarangi / esraj) like the reference's intro. Editor searches, director OKs each download.
- **Reel type:** music-montage (no speech) → playbook **cinematic-montage**.
- **Pilot:** yes.

## Interview — Round 2 (2026-10-20, partial)
- **Words:** title USKI AANKHEIN + small English line "if her eyes were music" (the reference's idea, corrected English) + end card.
- **Frame:** full 9:16 (no letterbox).
- **Pace (7.9–22 s):** mixed: bar holds (2.4 s) building to 2-beat cuts (1.2 s), hero hold on the 19.6 s accent, ~8 shots.
- **Stock clip:** director watched 4 candidates and chose **Pexels 4221987** (bowed folk instrument, orange kurta, static tripod, daylight; 1280×720, 30 fps, 114 s). Downloaded to `raw/stock/pexels-4221987/` (39.5 MB). Strongest bowing: 9–17 s (hand-region motion scan). Caveat logged: 720p, so a 9:16 crop is soft; used as a blended layer, not a full-frame shot.
- **Look:** **A Match reference** (director, from `analysis/look_test/look_options.jpg`).
- **Effects:** signature only.

## Reference — `references/Video-14732.mp4` (measured)
- 960×720 (4:3, letterboxed), 30 fps, 22.13 s. Title "IF EYES IS A MUSIC" across the top for the whole clip.
- 2 shots: 0–7.93 s bowed-string player (sarangi-like) **double-exposed** over an eye close-up, warm/golden; 7.93–22.1 s one extreme close-up of a woman's eyes (bindi, kohl): blink ~13 s, side glances ~19–21 s.
- Teardown: 2.7 cuts/min, first cut 7.93 s, motion 4.54 (calm), luma 0.20, contrast 0.53, sat 0.335, warm R−B 0.147, −14.1 LUFS, −1.0 dBTP.
- Audio (beat grid `analysis/audio_summary.md` + RMS by hand): 0–4.2 s bowed-string intro (≈ −22 dB); swell 4.2–4.7 s; decay to near-silence 4.8–7.7 s (−48 dB at 7.0 s); rhythm enters 7.8 s; 99.4 BPM, bar 2.415 s; accents 4.18, 7.89, 11.8, 16.02, 19.6, 21.99; downbeats 9.1, 11.8, 14.23, 16.63, 19.02, 21.41. Audio ends abruptly at 22.0 s.

## Approved decisions
- Hook: **H1** (C163 + bowing double exposure + title, cut on 4.18 accent). Approved 2026-10-20
- Target runtime: 22.0 s (approved)
- Grade / LUT: **G2 Gold & Shadow** (round 1b, replaces look A after the previz). `grade/uski_aankhein_G2_gold_shadow_v1.cube`, director loads it by hand on V3
- Caption style: none; title USKI AANKHEIN + "if her eyes were music" + end card @satyajitmall
- Effects: signature only (director, Round 2)
- Sequence: 1080×1920, 25 fps (7 of 11 shots are 25 fps); 30 fps clips interpreted to 25 (0.83×)
- Music: reference audio (guide), IG audio at upload

## Friction log
<!-- Pilot reels: one line each time something is slow, fails, needs a guess, a manual step or a workaround. Format: `- [phase] what happened → workaround → CR filed? (CR id / no)` -->
- [0] Footage isn't in `~/Documents/videos`: it's `~/Documents/Video ` (trailing space), one folder per shoot day, some with clips under `Media/`. Folder names also carry trailing spaces (`Pujo 2026 Oct 17 `, `Puja 2026 Oct 18 `) → found by listing; always quote paths → CR-20261020-uski-aankhein-director-profile.
- [0] Director profile says "no outside stock footage"; this reel asks for stock B-roll → recorded as a per-reel override in the brief → CR-20261020-uski-aankhein-director-profile.
- [1] Skill Phase 1 shows `teardown.py --ref <ref> -o …`, but the script requires `--ours` → passed the reference as `--ours` too (identical columns, ref numbers usable) → CR-20261020-uski-aankhein-script-gaps.
- [1] `gemini_audio_and_beat_analyzer.py --music <ref>.mp4` fails: `soundfile` can't open .mp4 ("Format not recognised") → extracted `references/ref_audio.wav` with ffmpeg first → CR-20261020-uski-aankhein-script-gaps.
- [1] Footage pool is 5 shoots (262 clips); `link_footage.sh` links whole folders → reused the earlier reels' surveys (read-only) to shortlist, will link/copy only picks → see CR-20261019-pujo-ki-asolei-sobar-pool-survey (already filed).
- [1] Footage survey across 5 shoots took a background agent ~34 min (read ~17 overview sheets + ~90 contact sheets from earlier reels; 262 clips). Every earlier reel's survey had to be found by hand → pool-survey CR (already filed) covers a shared survey index.
- [1] `analyze_footage.py` / survey report one mid-frame; C168 "face centred at 2.1 s" was really a pan at ~0.3 frame-widths/s, and its face centre was at x 0.68 at 2.05 s, not 0.57 → found only by a 10 fps strip; the payoff became a sweep + freeze → CR-20261020-uski-aankhein-script-gaps.
- [1] No crop/reframe preview tool for 9:16 eye-line framing → wrote `tools/storyboard.py` (crop + crop-follow + freeze per EDL row) and a numpy eye tracker (no `cv2` in .venv) → CR-20261020-uski-aankhein-script-gaps.
- [1] Homebrew ffmpeg here has no `drawtext` filter (labelled contact sheet failed) → labels drawn with PIL instead → CR-20261020-uski-aankhein-script-gaps.
- [2] `conform_clip.py` always centre-crops to 9:16; the stock clip works only as a full-width landscape band (720p → 1080 wide = downscale, sharp) → plan: place it in Premiere as a scaled band, no conform crop → CR-20261020-uski-aankhein-script-gaps.
- [2] Reference grade measured with a reel-local per-band script (`analysis/ref_grade/ref_grade.json`), as pujo-ki-asolei-sobar did → covered by CR-20261020-pujo-ki-asolei-sobar-reference-grade-match.

- [3] Premiere Motion keyframes on frame-rate-interpreted clips, still scaling and frame holds are unverified or broken through the MCP. So I baked every V1 shot locally (`tools/bake_shots.py`: crop, push, crop-follow, freeze, 180°, conform, fade, dip). Premiere only assembles, grades, types and mixes. 55 s for 10 shots → CR-20261020-uski-aankhein-script-gaps.
- [4] Look auto-tune first forced the reference's shadow ratios and cooled the idols' shadows (B gain ×2.1); needed warm-only clamps. The first `.cube` also left pure black at 0 next to lifted 0.03 (blotchy crushed areas) → fixed in `tools/ref_look.py` → CR-20261020-uski-aankhein-script-gaps.
- [5] Title: reused pujo-ki-asolei-sobar's proven HyperFrames composition (`tracking-in` focus-pull) and changed text, size, y and fps, instead of the full `/motion-graphics` director/builder loop. Render took 18 s → CR-20261020-uski-aankhein-script-gaps (studio title template).

- [3] Premiere V3 look still needs 2 manual director steps (create Adjustment Layer; load the `.cube` in Lumetri → Creative → Look): `add_adjustment_layer` and `apply_lut` are broken (reality doc) → known; no new CR.

- [3] Premiere had 3 projects open (pujo, uski, puja-night-2). `app.project` (and everything QE does) follows whichever project's sequence was last in front, and it flipped to Pujo's between calls. Every uski script checks `app.project.path` and re-activates with `P.openSequence(seqID)` → CR-20261021-uski-aankhein-multi-project-premiere.
- [3] The director's manual `.cube` load went to the wrong place: no uski clip was selected, so it may have landed on a Pujo clip (~10 min lost, and a risk to another reel). Fixed with full-screen computer use (teach mode is not available in this session). Premiere was in its own full-screen Space, so the Dock click needed a Finder grant → CR-20261021-uski-aankhein-multi-project-premiere.

- [7] Review gate v1 found the eye-lock pinned the wrong point: hand-estimated eye positions were 30–200 px off, and the lock faithfully kept the error. ~45 min to measure pupils, re-track and re-bake. Lesson: measure the pupils on a gridded crop before tracking → CR-20261020-uski-aankhein-script-gaps (reframe tool should take measured eye points).
- [7] `verify_render.py --fix-loudness` writes no copy when only the true peak fails (loudness in range). An empty path made it write `_VERIFY.md` at the studio root, which I deleted. Fix: ffmpeg `alimiter` remux → CR-20261020-uski-aankhein-script-gaps.

- [7] `refreshMedia()` on the replaced stock-band overlay (same name, same 104 frames) rendered wrong in Premiere (luma 0.376 vs 0.242 with it disabled), while the V1 refresh the same way was fine. Workaround: import under a new file name and re-place → CR-20261021-uski-aankhein-multi-project-premiere (refresh caveat).
- [7] A stale entry in `bakes_v2.json` (old C120 bake still listed) would have composited two clips into one slot as a phantom dissolve. Caught before the export; `bake_v2.py` should replace by row, not by file name → CR-20261020-uski-aankhein-script-gaps.

- [2] Round 2, finding the reference's player: no stock search finds an esraj. Google Lens needed an image upload, which the browser tool can't do from a file, so I injected the crop through a JS `DataTransfer` on the Lens page. No exact match. ~40 min → AI shot (director-approved) → CR-20261020-uski-aankhein-script-gaps (item: reference source finder).
- [3] `bake_v2.py` hard-coded the last shot (`n == 11`, `range(1, 10)`), so adding rows silently broke the sweep/freeze pairing. Generalised to `last_n` in `tools/bake_v3.py`. Two more EDL-edit bugs cost re-bakes: a dict replaced in a lookup map didn't update the EDL list, and a `setdefault` chain left `ey` unset → CR-20261020-uski-aankhein-script-gaps.
- [7] `shake_report.py` can't tell a clamped lock from shake: C059 read 14 px RMS. Only a per-region motion check showed a smooth 160 px bob, caused by the lock crop hitting the source edge on every frame. The bake should warn when a lock clamps → CR-20261020-uski-aankhein-script-gaps.

- [7] Review v2 #1: moving C208 to a shorter slot left its measured `eye_ref` time outside the new source window. `track_eyes.py` silently clamped the reference frame, and the lock pinned a point 55 px off the pupils, which nothing caught before the gate. Fixed in the reel's tracker (track from the measured frame, then slice) → CR-20261020-uski-aankhein-script-gaps item 16.
- [7] Review v2 #2: the doorway shot put the shrine in the IG bottom zone (y 1657). No local check measures where the subject sits against the IG UI zones; only the reviewer caught it → CR-20261020-uski-aankhein-script-gaps item 17.

- [1/4] **The reference's transition style was invisible to the teardown.** `teardown.py` reported "2 shots, first cut 7.93" and nothing about how they change. The reference's only transitions are two 6-frame blinks (lids closing to a slit). I designed dissolves, then eye-match dissolves, then a ghost for three rounds, until the director said "look at the reference video to understand the transitions". Found in 10 min with per-frame luma and a strip → CR-20261020-uski-aankhein-script-gaps item 18.
- [4] **"One house" was three houses.** The Oct 20 folder's bonedi-bari night is three houses (A 20:29–20:32, B 21:25–21:28, C 21:42–21:51). The v2/v3 "bonedi act" mixed all three, which is part of "too many places". The survey had no place grouping; a fresh agent survey found it from idols, architecture and timecodes (~33 min) → CR item 19 (and the pool-survey CR).
- [4] **Look choice at 50 %:** `look_preview.py` at its default 50 % intensity made 7 film looks nearly indistinguishable at sheet size. I re-made the sheet at ~80 % with the current grade as a column and letters. The first G2 contrast variants used a pivot that lifted black to 0.07; switched to a black/white-anchored curve → CR item 20.
- [4] **Template tracker drift on a tripod shot:** C050's eye track walked 83 px while global motion was 8 px; a lock would have made a still frame wobble. Static shots now use a fixed crop → CR item 21 (tracker should check global motion first).
- [4] **G2b2 is a custom `.cube`:** it must be loaded into the V3 Lumetri by hand (or by computer use) again → known limitation; no new CR.

- [4-5] **Iterating on footage and framing without re-anchoring on the concept.** Each director note (more footage, one place, minimal idols, tighter, eyes as the subject) was executed literally. The sum drifted from the reference's calm two-shot idea, and image quality fell below the source's limits (2.4–3.4× crops). No studio rule caps enlargement or flags concept drift → CR-20261020-uski-aankhein-director-profile (add a "concept anchor" check per round) and script-gaps item 22 (enlargement cap per source resolution).

- [5] **Loading a custom .cube still needs the screen.** Premiere sat in its own full-screen Space, so background control couldn't click; the first full-screen approval timed out; the Dock click needed a Finder grant; the macOS Open panel (XPC) can't be clicked by computer use, so I picked the file with the keyboard. ~15 min → CR-20261021-uski-aankhein-multi-project-premiere (look loading) and CR item 25 (bake the look into V1, or use Premiere's built-in looks, to avoid the manual step).

- [7] **Double exposure veil:** a full-frame Screen of the AI player (white kurta) lifted shot A's blacks to p10 0.20 vs 0.07 on B/C, and its centred neck ran between her eyes. The v9 review caught both. Fix: place the layer like the reference (player left), ramp its weight off her face with a hole over the eyes, take the ghost's low-frequency veil back out (inverse Screen on its blur), then match black point and level to the other shots. ~40 min → CR-20261020-uski-aankhein-script-gaps item 27.
- [7] **Real-ESRGAN on small jewellery:** x4plus redraws a 20 px gold nath as blobs and gives silver filigree a waxy, invented texture. Fix: blend AI 55 % over the plain denoised enlargement, 20 % over jewellery. ~20 min → item 28.
- [7] **Regional flicker** after a global deflicker (one lamp beating at 30 fps; cheeks in anti-phase, ~1.2–1.6 %). Fix: a gain field, not one gain per frame. ~20 min → item 26.
- [8] **Cover:** the first cover was a frame grab with the title; the director said "Use a better cover". Four designed options (`tools/cover_r9.py`) → the director picked a designed eyes band. Pujo also ended on a designed cover → CR item 29 (designed cover by default).

- [9] **Approved file looked "very poor" on the iPhone.** Every check had been made on 2 fps sheets and Mac-size previews; nobody looked at 100 % crops the way a phone shows them. The AI upscale + strong denoise read as plastic, and Premiere's H.264 preset (Main, 9.5 Mb/s) blocked the darks. Fix: real-frame stacks, wider framing (≤ 1.42×), a ProRes master + x264 High encode. ~2 h → CR-20261020-uski-aankhein-script-gaps item 30.

<!-- The editor appends one section per round below: "## Round N — Proposal", "## Round N — Director notes", "## Round N — Changes made". -->

## Round 1 — Proposal (2026-10-20)
Plan files: `brief.md` v1 · `analysis/edl_v1.json` · storyboard `analysis/picks/storyboard_v1.jpg` (3 frames per shot through the planned 9:16 crop, cyan line = eye-line) · hook preview `analysis/look_test/hook_double_exposure_preview.jpg` · look options `analysis/look_test/look_options.jpg` (director chose A).

### Hook options
1. **H1 (recommended): bow over her eyes.** Oct17 C163 (red Durga in incense haze), source 0.00–3.48 s (30 fps clip interpreted to 25 fps: 4.18 s on screen). The bowing band from Pexels 4221987 (source 10.0–13.5 s) crosses her eyes; slow push; title fades in at 0.6 s. Cut on the string swell **accent 4.18 s**. *Why:* it's the reference's own move on our subject, motion from frame 1 (the bow), and it keeps the giant face for the payoff.
2. **H2: strongest image first.** Open on the C168 giant-face freeze (source 2.30 s) with the double exposure; the payoff becomes C139 with a push to the third eye. *Trade-off:* the best image goes up front for IG retention, but the ending loses its "the camera stops on her" moment.
3. **H3: born from black.** Gaussian blur reveal (60→0 over 1 s) on Oct18 C208's eyes as the strings start, with the double exposure; C163 moves to the breath. *Trade-off:* quietest and closest to the reference, but the weakest first second on a phone.

### EDL (25 fps sequence, 1080×1920; times in sequence seconds; source times are real seconds in the original clip)
| # | clip | in | out | text / action | V1 move | V2/V5 | transition out | SFX |
|---|---|---|---|---|---|---|---|---|
| 1 | Oct17 C163 (30 fps) src 0.00–3.48 | 0.00 | 4.18 | HOOK: red Durga in haze, eyes on the eye-line; bowing hand + instrument as a feathered band across her eyes (V2, Screen 55–70 %); title USKI AANKHEIN + "if her eyes were music" 0.6–3.8 s | slow push 3.3→3.7×, crop follows drift | V2 stock band (Screen 55–70 %, out 3.6–4.18) · V5 title 0.6–3.8 | cut (fade in 0–0.3 at head) |  |
| 2 | Oct18 C208 (30 fps) src 0.40–3.49 | 4.18 | 7.89 | THE BREATH: white sholapith Durga, pure eyes in the near-silence (no double exposure) | slow push 3.3→3.7× |  | dip to white 3 fr |  |
| 3 | Oct15 C074 (25 fps) src 9.60–10.81 | 7.89 | 9.10 | RHYTHM ENTERS: Shakti mask, huge staring eyes; 3-frame dip to white on the cut + sub-hit | as shot (slow tilt) |  | cut | sub-hit 7.89 (−16 dB) |
| 4 | Oct16 C139 (25 fps) src 9.60–12.30 | 9.10 | 11.80 | classic Kolkata Durga, big eyes, third eye (bar hold) | slow push 3.3→3.6× · ROT 180 |  | cut |  |
| 5 | Oct15 C076 (25 fps) src 17.60–20.03 | 11.80 | 14.23 | golden Durga, 3/4 profile, lowered gaze (bar hold) | as shot |  | cut |  |
| 6 | Oct17 C145 (25 fps) src 10.00–11.19 | 14.23 | 15.42 | gold Durga, eye-line lock run begins (2 beats) | hold |  | cut |  |
| 7 | Oct15 C025 (25 fps) src 5.00–6.21 | 15.42 | 16.63 | face slides past dark pillars (real lateral move) (2 beats) | as shot (lateral) |  | cut |  |
| 8 | Oct16 C112 (25 fps) src 11.40–12.58 | 16.63 | 17.81 | red-sari Durga (2 beats) | hold · ROT 180 |  | cut |  |
| 9 | Oct16 C083 (25 fps) src 3.30–4.51 | 17.81 | 19.02 | pastel Durga, third eye (2 beats) | as shot (push) |  | cut |  |
| 10 | Oct17 C168 (30 fps) src 1.82–2.30 | 19.02 | 19.60 | SWEEP: the camera pans across the giant face; face slides in from the right and lands centred (crop fixed at the landing spot) | crop fixed at landing spot |  | — (same clip continues) |  |
| 11 | Oct17 C168 (30 fps) src 2.30 (freeze) | 19.60 | 21.99 | PAYOFF: the pan stops dead on the accent (freeze frame at src 2.30 s), eyes fill the frame; slow push toward the third eye; sub-hit on 19.60; end card @satyajitmall 20.6-21.99; cut to black on 21.99 | FREEZE + push 2.2→2.6× to third eye | V5 end card 20.6–21.99 | cut to black 21.99 | sub-hit 19.60 (−16 dB) |

**Estimated runtime: 22.0 s** (21.99 s of picture + black to the end of the audio). 10 distinct idols, 11 EDL rows, median shot ≈ 1.2–2.4 s. Non-cut transitions: fade-in, one dip to white, the freeze, cut to black.

## Round 1 — Director notes (Checkpoint 1, 2026-10-20)
- "Approved: brief v1 with hook H1. Loading the .cube by hand is fine."
- Still open: which IG audio + start point at upload (asked; not answered yet).

## Round 1 — Rough-cut prep, local (2026-10-20, no Premiere yet)
- **Picks linked** into `raw/b-roll/` (10 symlinks, originals untouched; `raw/SOURCES.md`). `analysis/summary.md` per clip.
- **V1 baked** (`tools/bake_shots.py` → `renders/bakes/*.mov`, `bakes.json`). Each shot is ProRes 422 HQ 1080×1920 at 25 fps, exactly its timeline length, with:
  - frame-for-frame conform (30 fps sources play 0.83×);
  - 180° fix on C139 and C112;
  - eye-line crop, eased pushes, C163 crop-follow;
  - the C168 sweep + freeze as one clip;
  - the fade-in (0–0.32 s) and the 3-frame dip to white at 7.88 s.

  Cut frames at 25 fps: 0 / 104 / 197 / 227 / 295 / 356 / 385 / 416 / 445 / 475 / 490 / 549, then one black frame to 550 (22.00 s). All within ±1 frame of the beats.
- **V2 stock band** baked: `renders/stock/stock_band_v1.mov` (Pexels 4221987 real 10.00–13.47 s → 104 frames; 1566 px wide band on the eye line, feathered, desat/warm, fades in with the picture and out 3.60–4.16 s). Placed with Screen 65 %, with no keyframes needed.
- **V4 grain** baked at 25 fps (`renders/texture/grain_25fps_v1.mov`, 549 frames). It fades in from neutral grey, so Overlay stays neutral, and is placed at Overlay 12 %.
- **Look** `grade/uski_aankhein_reference_look_v1.cube`, from `tools/ref_look.py`:
  - tuned on one still per shot to the reference medians: luma 0.28, p02 0.067, p98 0.53, saturation 0.23, mid R/G 1.50, mid B/G 0.62;
  - per-clip primary targets (exposure stops, WB gains) are in `analysis/primary_targets_v1.json`;
  - before/after: `analysis/look_test/graded_v3/before_after.jpg`;
  - the director loads it by hand on the V3 adjustment layer.
- **Type:**
  - HyperFrames title `graphics/title/renders/title-alpha.mov` (3.2 s, 25 fps, ProRes 4444 alpha) and end card `graphics/endcard/renders/endcard-alpha.mov` (34 frames);
  - composite check: `analysis/type_check/type_check_v1.jpg`, inside the safe zone and below her face.
- **SFX:** `audio/sfx/` via `sfx_prep.py` (bass boom, transient at 0 s). Placed at 7.88 s and 19.60 s at −14 dB.
- **Previz (local, not the Premiere cut):** `renders/previz/uski-aankhein_v1_previz.mp4`, 22.00 s, 550 frames, LUT + Screen band + type + music + booms; audio peak −1.0 dB. Sheets: `analysis/watch_previz_v1/`.
- **Premiere scripts ready:** `tools/build_premiere_scripts.py` → `analysis/_es_import.jsx`, `_es_seq.jsx`, `_es_place.jsx`, `_es_readback.jsx`. They target `premiere/uski-aankhein.prproj` by path.

## Round 1b — Director notes on the local previz (2026-10-20)
Premiere: "Free, go ahead". On the previz: "jumps are odd the videos are ustable, the tranistions are not cinmetoc cinematic c olurs grading is not thete at all".
Read as:
1. **Jumps are odd.** Hard cuts between idols framed identically on the eye-line read as jump cuts.
2. **Unstable.** The 3.3× crops magnify handheld shake about 3×.
3. **Transitions not cinematic.** Plain hard cuts and a flat dip to white.
4. **Grading not there.** The reference-match LUT is flat and grey in motion: lifted blacks, no contrast, low saturation.

Fixing locally first (bakes + previz v2), then building in Premiere.

## Round 1b — Changes made (local; previz `renders/previz/uski-aankhein_v1b_previz.mp4`)
1. **"Jumps are odd"** → eye-match dissolves centred on the beats (`analysis/transitions_v2.json`): 12 frames at 4.16 s (hook → breath), 6 at 9.08, 8 at 11.80, 6 at 14.24, 4 at 15.40 / 16.64 / 17.80. The sweep at 19.00 stays a hard cut (its camera move is the transition).
2. **"Videos are unstable"** → eye-lock stabilisation. `tools/track_eyes.py` (FFT NCC, match 0.88–0.99) tracks her eyes in every source frame; `tools/bake_v2.py` moves the crop with them.
   - Jitter RMS on the holds (`analysis/shake_previz_v1b.json`):
     - C139 16.7 → 0.84 px
     - C112 15.3 → 0.22 px
     - C145 10.8 → 0.42 px
     - C076 12.2 → 2.9 px
     - C083 9.5 → 1.8 px
     - C208 5.4 → 0.22 px
     - C163 0.23 px
   - C074 and C025 were smooth tilts; both now eye-locked on later windows (C074 source 10.12 s at 1.8×; C025 source 5.30 s, eyes at 36 %). Frame-to-frame motion is 0 px except the edge frames.
   - The C168 sweep keeps its real pan.
3. **"Transitions not cinematic"** → the dissolves above + a 4-frame bloom flash (highlight glow + lift) on the 7.88 s rhythm drop, replacing the flat dip to white. Fade from black 0–0.32 s kept.
4. **"Grading not there"** → director picked **G2 Gold & Shadow** from 3 options (`analysis/look_test/grade_options_1b.jpg`).
   - Per-shot primary is baked: grey balance + exposure to one target, gains in `renders/bakes_v2/bakes_v2.json`.
   - Pre-look halation (0.22) is baked.
   - The look is `grade/uski_aankhein_G2_gold_shadow_v1.cube` (replaces the reference-match cube) on the V3 layer, plus a Lumetri vignette and grain at Overlay 12 %.
- **Brief overrides added:** dissolves (8) and the bloom exceed the playbook's 3–4 non-cut transitions per 30 s. The director asked for cinematic transitions; the eye-match dissolve is the concept. Primary correction is baked rather than done in Lumetri (it is still per clip, on the clip).
- V1 is now one file: `renders/bakes_v2/V1_timeline_v2.mov`, 550 frames, ProRes 422 HQ. Premiere assembles V1–V5 and A2/A3, grades V3, types and exports.

## Round 1 — Premiere build (2026-10-20, director: "Premiere is free")
- `create_project` → `premiere/uski-aankhein.prproj`, empty (no Adobe sample media).
- `_es_import.jsx`: 7 items in 01_A-Roll, 02_B-Roll, 03_Graphics, 04_Textures, 05_SFX, 06_Music.
- `_es_seq.jsx`: `Reel_uski-aankhein_v1`, 1080×1920 at 25 fps, from title-alpha.mov. `add_track` ×2 (above) → V1–V5, A1–A3.
- `_es_place.jsx`, read back:

  | Track | Clip | Frames | Settings |
  |---|---|---|---|
  | V1 | V1_timeline_v2 | 0–550 | |
  | V2 | stock band | 0–104 | Opacity 65, Screen (22) |
  | V4 | grain | 0–549 | Opacity 12, Overlay (19) |
  | V5 | title | 15–95 | |
  | V5 | end card | 515–549 | |
  | A2 | boom | 197–227, 490–520 | Level 0.0355 (−14 dB) |
  | A3 | ref_audio | 0–550 | 0.1778 (0 dB) |

  Sequence in/out 0–22 s. `get_timeline_gaps`: only V5's intended gaps. Saved.
- V3: the director created the Adjustment Layer (File → New). I placed it on V3 (0–549) and added one Lumetri via QE (`_es_adj.jsx`), with vignette Amount −1.0 / Midpoint 45 / Feather 70 (`_es_vignette.jsx`).
- **LUT, first try failed:** the director's first `.cube` load didn't land on the uski layer. Look = None; the render matched the ungraded V1 (luma 0.319 vs 0.313).
  - The director thinks it may have gone onto a Pujo clip. I messaged the Pujo session (reel-3) to check Creative > Look before its next export.
  - **Resolved:**
    - Pujo replied: a read-only scan of all 6 sequences (207 clips) found no Lumetri anywhere, and its final exports predate the load.
    - puja-night-2.prproj (also open) was last saved 2026-10-19 19:22 IST, with no auto-save since. On-disk is unaffected.
    - Director told to choose "Don't Save" if Premiere asks when closing puja-night-2.
  - Setting the Look by script fails: `Illegal Parameter type`.
- **LUT, second try:** with the director's OK, I loaded it through screen control (select the V3 clip → Effect Controls → Lumetri → Creative → Look → Browse → G2 cube). Render check vs previz: luma 0.309/0.268/0.277 vs 0.302/0.257/0.270, same deep blacks. Saved.
- **Exports** (`_es_export.jsx`, `exportAsMediaDirect` with Match Source H.264 High Bitrate): `_mix` and `_IG` (A3 music muted). Both 22.000 s, 1080×1920 at 25 fps, 9.7 Mb/s, BT.709 tags.
  - Mix: −14.1 LUFS, −1.0 dBTP.
  - IG: SFX only, −17.0 dBTP.
  - `verify_render.py`: everything passes except "black frames 0.00–0.12 s". That is the brief's planned fade from black (deliberate; reported at Checkpoint 2).
- **Teardown vs reference** (`analysis/teardown_v1/COMPARE.md`): ours is brighter (luma 0.276 vs 0.20), more contrast (0.685 vs 0.53), more saturated (0.586 vs 0.335), with more motion (14 vs 4.5). All deliberate: the G2 grade (round 1b), the pushes, dissolves and sweep. The scene detector counts 3 cuts because dissolves aren't detected (actual: 10 shots).

## Round 1 — Review gate
### Loop 1 (v1, `analysis/review_v1.md`): FAIL, 5 major + 3 minor. Answers:
1. **Eye-line not on one line (major)** → **fixed.** The lock had pinned my hand-planned template point, not the pupils. I measured the real pupil centres on the bake (`analysis/eyefix/eyeline_measure_v1.jpg`; C163 was at (343, 947)), set `eye_ref` per shot in `analysis/edl_v1c.json`, and re-tracked with the template centred on the pupils. Check: every shot within ±30 px of y 768, centred (`analysis/eyefix/eyeline_check_v1c.jpg`). The bow band now crosses her eyes.
2. **C076 lurch + smear (major)** → **fixed.** A per-frame sharpness scan found the clean stretches: 16.0–17.68 s and 18.48–20.08 s, smear 17.72–18.44 s. C076 now plays 16.04–17.68 s (eye-locked), then holds its last frame under the eased push. The frame scan's blur flags are gone.
3. **Dissolves don't morph (major)** → **fixed** by 1 + the swaps in 4. The dissolve mid-frames now overlap eye on eye (`analysis/watch_previz_v1c/dissolve_mids.jpg`).
4. **C025 dark slit (major)** → **fixed by replacement.** Oct16 C120 (golden statue face, 4K, unused) in the same slot. Oct18 C200 also replaces C083, whose face sat at the source's edge so its eyes couldn't be centred.
5. **C076 acid yellow (major)** → **fixed.** Primary wb 0.65, sat 0.9, −0.05 stop: mid B/G 0.26 → 0.43, hue 42°.
6. **Saturation see-saw (minor)** → **fixed.** C139 and C168 sat ×0.65; mid-sat range now 0.19–0.36 (was 0.56–0.86 on the reviewer's scale).
7. **Booms late (minor)** → **fixed.** Placed at 7.84 s and 19.56 s; audible onset (−45 dB) at 7.861 and 19.581, ≈20 ms before the cuts. Level −16 dB. The mix's true peak then hit −0.1 dBTP (boom on the music accent at 19.63 s), so the mix guide was peak-limited by remux: `uski-aankhein_v1b_mix_tp.mp4`, −1.9 dBTP, −14.1 LUFS. The IG file is unaffected (−19 dBTP).
8. **C208 / C112 luma +0.04 (minor)** → **fixed.** −0.12 stop each. All shots now within ±0.021 of the median luma (`analysis/watch_previz_v1c/`).
- Premiere: V1 media refreshed in place (same name and frame count; `refreshMedia()` → true; a still at 16 s matches the previz, mean diff 1.8 %), booms re-placed. Sequence still `Reel_uski-aankhein_v1` (a review loop inside round 1; the v1 exports are kept). Exports: `uski-aankhein_v1b_mix.mp4` / `_mix_tp.mp4` / `_IG.mp4`.

### Loop 2 (v1b, `analysis/review_v1b.md`): FAIL, 0 blockers, 3 majors + 4 minors. All fixed in v1c, **editor-verified** (the gate's 2-loop limit is reached; no third blind run):
1. **Freeze hop 78 px (major)** → **fixed.** The sweep's jitter compensation had a smoothing-edge kick in its last frames. It now tapers to 0 over the last 6 frames, and the freeze uses the sweep's last source frame (2.2867 s). On the export the pan runs −26…−44 px/frame, then 0: no skipped jump.
2. **C120 soft (major)** → **fixed by replacement.** Oct16 C084 (same pastel idol as the dropped C083, low angle, sharp 1.2–2.6 s), eye-locked through its camera pan. Eye sharpness 0.42 vs C120's 0.13 (same metric; the other shots 0.74–5.7); contrast 0.48 vs 0.38.
3. **C076 lime (major)** → **fixed.** R ×1.14, B ×1.04, −0.15 stop: hue 35°, R/G 1.41.
4. **C112 olive (minor)** → **fixed.** R ×1.12, sat 0.9: hue 36°, R/G 1.27.
5. **C145 chrome (minor)** → **fixed.** sat 0.85 (mid sat 0.27, in the pack).
6. **Sweep luma (minor)** → **fixed.** +0.15 stop easing to 0 at the freeze: sweep −0.028 vs median (within ±0.03).
7. **Hook band too wide (minor)** → **fixed.** `tools/stock_band.py` v2: only the instrument neck + bow (stock rows 0.28–0.62), a 300 px band on the eye-line, feather ±150 px, sleeve and cloth faded. In Premiere the refreshed band file rendered wrong (frame luma 0.376 vs 0.242 with V2 off). Re-imported it under a new name (`stock_band_v2.mov`); the still now matches the previz (diff 2 %).
- **v1c exports:** `uski-aankhein_v1c_mix_tp.mp4` (−14.1 LUFS, −1.9 dBTP; mix peak-limited by remux) and `uski-aankhein_v1c_IG.mp4` (music muted, −19 dBTP). Both pass `verify_render` except the planned fade-in black (0–0.12 s).
- All shots within ±0.028 of median luma, hues 29–40°. Frame scan (`analysis/review_v1c_editor_scan.json`) flags only the designed fade-in, bloom and end black.

## Round 2 — Director notes (Checkpoint 2 on v1c, 2026-10-21)
Quote: "chosse better footages. are these the fotages we want, do we onoly shows te face of ma nothing else it does make a story comepte or comepelluing. Check all teh fotages I added in teh new folder asweel. Also the character image in teh beinging is not stringa nd recognisable."
Read as:
1. **Better footage, and a story.** Ten idol faces in a row aren't a story. The cut needs more than Ma's face: people, ritual, the festival around her, so it builds and lands.
2. **New footage:** `~/Documents/Video /Pujo 2026 Oct 20/`, 34 clips C033–C066 (Navami night, 20:29–02:27). Check all of it.
3. **The opening character image is weak and not recognisable.** The hook's double exposure: the narrowed band shows only a neck and bow, so the musician (and C163 behind it) don't read.

### Round 2 — director's answers to the story options (2026-10-21)
- Story: "Less of single human more fottages of ma but teh stable foytgaes, yes use bondi bari fottages". So: few single-person shots, mostly **stable** footage of Ma, and use the Oct 20 bonedi-bari footage.
- Opening: "Also find teh accurate string player video from reffence sources fottage please. The isntrucment and musci need to match". So: identify the stock clip the reference itself used (the bowed instrument matching the audio) and use that.

### Round 2 — Finding the reference's string player (2026-10-21)
- **Instrument:** the reference's player holds an **esraj**: fretted neck, curved metal frets, small round body, played upright on the lap with a bow. It is not a sarangi, and Pexels 4221987 isn't a match. The soundtrack's intro is bowed esraj too, so the director's "instrument and music need to match" means an esraj.
- **Search:**
  - Pexels and Pixabay ("esraj", "dilruba", "Indian bowed string"): no esraj clip;
  - reverse image search (Google Lens on 4 crops of the reference's player, `analysis/ref_player/`): no exact match for the source clip. Lens only pointed at instrumental covers ("Chupke Se / Snehithane"), which are other people's performance videos with no licence.
- **Result:** no licensable footage of the reference's player exists. Offered the director an AI-generated esraj shot; their answer is under "director decisions" below.

### Round 2 — Proposal: storyboard B (`analysis/picks/storyboard_v2b_draft.jpg`)
Story: **music → her eye → the house that has worshipped her for generations → we walk in → Ma → the faithful → her many faces → the giant face stops on the accent.** Of the 12 shots, one has a person: a devotee in silhouette. The esraj shot shows only hands.

| # | seq (s) | clip | what | move | out |
|---|---|---|---|---|---|
| 1 | 0.00–2.40 | **AI esraj** (Veo 3.1 Lite, 24→25 fps) src 0.6 s | instrument, hands, bow, folded legs, **no face**; title 0.6–3.8 s | plain, full frame | dissolve 16 fr |
| 2 | 2.40–4.16 | Oct17 C163 | her eye. The esraj stays on as a Screen ghost that clears by 3.3 s | eye-lock | dissolve 12 fr on the swell accent |
| 3 | 4.16–6.04 | Oct20 C037 | bonedi bari: the old family photograph (generations of this puja) | slow push 0.70→0.62, locked | dissolve 10 fr |
| 4 | 6.04–7.88 | Oct20 C059 | the dark doorway, the shrine low under the lantern (the silence) | slow push, locked on the shrine | **bloom** on the drop 7.88 s + boom |
| 5 | 7.88–9.08 | Oct20 C050 | the bonedi Ma, face close, steady | eye-lock | dissolve 6 fr |
| 6 | 9.08–11.80 | Oct20 C056 | darshan: a devotee in silhouette before Ma in the thakurdalan | forward move kept, jitter removed | hard cut on the accent 11.80 |
| 7–11 | 11.80–19.02 | C139, C145, C208, C112, C200 | her many faces, eye-line locked (bar hold, then 2-beat run) | eye-lock | dissolves 6/4/4/4 fr, hard cut 19.02 |
| 12–13 | 19.02–21.99 | Oct17 C168 sweep + freeze | the giant face: the pan stops dead on the 19.60 accent, push to the third eye, end card | smooth → freeze | boom 19.60, cut to black 21.99 |

**Runtime 22.0 s** (550 frames at 25 fps). Dropped from v1c: C074 (Shakti mask), C076, C084 (the least stable). Dropped the V2 stock band (Pexels 4221987): the esraj double exposure is now baked into V1.

### Round 2 — director decisions (2026-10-21/22)
- Opening: "Do not use the face of the artist, use the instrument close up only and arm and legs may be". So: hands, arms, legs and instrument only.
- Storyboard B: "Yes, build it".
- AI esraj: "Yes, generate draft" ($0.12, 720p, 4 s), then "Yes, render final" ($0.40, 1080p, 8 s). **Total $0.52** of the $2 per-reel cap (month $0.64 of $10; `studio/ledger/ai-spend.jsonl`). The shot is labelled **AI-generated** in the brief, and the IG "AI info" label must be turned on at posting.

### Round 2 — Changes made (local; previz `renders/previz/uski-aankhein_v2_previz.mp4`)
1. **"Choose better footage / only Ma's face is not a story"** → story B: a bonedi-bari act (photo → doorway → bonedi Ma → darshan, 4.16–11.80 s) between the hook and the faces. The three least stable faces (C074, C076, C084) are gone.
2. **"Check all the footage in the new folder"** → surveyed all 34 Oct 20 clips (`analysis/survey_oct20/`). Picked the steadiest takes:
   - C037, C059, C056;
   - C050 instead of C045, which was motion-blurred.

   All are eye- or shrine-locked: C037 and C059 locked with a push, C050 locked, C056 keeps its forward move with the jitter removed.
3. **"Less of single human, stable footage of Ma"** → one devotee silhouette (C056). Every Ma shot is locked: shake 0.15–0.94 px RMS on the locked shots (`analysis/shake_previz_v2.json`). C037, C059 and C056 read higher only because of their designed pushes, moves and dissolve handles.
4. **"Character image not strong or recognisable" + "find the accurate string player"** → the reference's instrument is an esraj, and no licensable clip exists (search above). So the opening is an AI-generated esraj close-up (hands, bow, frets, folded legs, no face), full frame for 2.4 s, then a ghost over her eye.
5. **Editor fixes after the v2 previz check:**
   - C059 doorway: −1.0 → −0.5 stop. Luma was 0.08 against the 0.26 median; now about 0.16, a deliberate low-key night beat; the shrine stays unclipped.
   - C163: the esraj ghost was 0.55 Screen for the whole shot (luma +0.135 vs median). Now 0.45, clearing by 3.3 s, so the eye gets a clean beat before the photo.
   - C059 lock: shake_report showed 8.8 px RMS on the shot's core. Per-region phase correlation showed the whole frame bobbing about 160 px up, then back. The lock was clamped on every frame: the shrine sits at source ey 0.85–0.94, and cw 0.85 with v 0.78 needs a crop top below the source edge. A simulation of cw/v options picked cw 0.75 → 0.70, v 0.88. The shrine now moves 0 px from frame 3 to 43 (`analysis/watch_previz_v2/c059_v2fix.jpg`).
   - After the fixes, all shots are within ±0.021 of the 0.255 median luma, except C059 (0.130, deliberate low-key). Shake on the shot cores (`analysis/shake_previz_v2_core.json`): 0.37–2.6 px RMS. C056's 2.6 is its kept forward move.

### Round 2 — Premiere build (2026-10-22, director: "Free, go ahead")
- `analysis/_es_v2_build.jsx`, with the project-path guard. Pujo's v4 was in front before the run:
  - `Reel_uski-aankhein_v1` cloned → `Reel_uski-aankhein_v2`; v1 is untouched as the rollback;
  - imported `renders/bakes_v3/V1_timeline_v3.mov` (new name) into 01_A-Roll and placed it on V1, 0–550;
  - V2 cleared: the stock band is gone, the esraj ghost is baked.
- Read back: V3 adjustment layer (one Lumetri, G2 `.cube`, intensity 100, vignette −1 / 45 / 70), V4 grain, V5 title 15–95 and end card 515–549, A2 booms at 196 and 489, A3 music 0–550. Project saved 17:29.
- **Export check:** the Premiere export against the local previz has a median frame difference of 1.7 % (max 5.0 % on the bloom frame 197), luma within ±0.008.
- **Exports:**
  - `uski-aankhein_v2_mix.mp4`: true peak −0.1 dBTP (boom on the accent) → `alimiter` remux → `uski-aankhein_v2_mix_tp.mp4`, −14.1 LUFS / −1.9 dBTP;
  - `uski-aankhein_v2_IG.mp4`: music muted, −19 dBTP.

  `verify_render` passes both, except the designed fade-in black (0–0.08 s).
- Frame scan (`analysis/review_v2/scan.json`) flags only the fade-in, the bloom on the drop (7.96 s) and the end black. Teardown vs ref: `analysis/teardown_v2/COMPARE.md`.

## Round 2 — Review gate
### Loop 1 (v2, `analysis/review_v2.md`): FAIL, 3 major + 6 minor. Answers (fixes in v2b, `renders/exports/uski-aankhein_v2b_mix_tp.mp4`):
1. **C208 eyes 55 px below the eye-line (major)** → **fixed.**
   - *Cause:* C208's measured `eye_ref` time (1.933 s) lies outside its new 1.2 s window (0.33–1.50 s). `track_eyes.py` clamped the reference frame to the window's last frame, so the template was centred where the pupils would be 0.45 s later.
   - *Fix:* the tracker now tracks from the measured frame and slices the window (`tools/track_eyes.py`). The other rows' `eye_ref` times were already inside their windows.
   - *Check:* pupils on the 768 line at 15.6, 16.0 and 16.4 s (`analysis/review_v2/eyeline_v2b.jpg`).
2. **C059 shrine in the IG bottom zone (major)** → **fixed.**
   - *Why it can't just move up:* the source frames the idol cut off at its bottom edge (shrine at 0.74–1.0 of the frame height), so no crop can raise it with the doorway still in.
   - *New crop:* a medium shot of the shrine under the valance, lantern out (cw 0.46 → 0.42, 1.19× upscale), locked with the shrine at v 0.72. It plays 3.30–4.36 s, where the shrine is highest, then holds under the push for 19 frames; only 2 frames clamp.
   - *Check:* bright centroid y 1210 (was 1500 on my metric, 1657 on the reviewer's); 11 % of the bright pixels below 1600 (was 50 %); pure black 27 % (was 47 %).
3. **C163 flat and soft in the hook (major)** → **fixed.**
   - *Changes:* push capped at cw 0.40 → 0.36 (≤ 1.39× upscale, was 1.85×); black point 0.05; sat 0.72; mild unsharp.
   - *Check:* p10 0.080 → 0.054, Laplacian 9–12 → 13.6–17, mid sat 0.73 → 0.66.
4. **Title over the esraj body (minor)** → **intended:** a title card over the opening image, as in the reference, whose title sits across the picture. Director asked at Checkpoint 2.
5. **AI esraj body is a hybrid (minor)** → **intended; director asked at Checkpoint 2.**
   - *What's off:* the neck and frets read as esraj, but the body has sound-holes and pins; a real esraj has a parchment-covered body.
   - *Option:* re-generate for ~$0.40 final (+$0.12 draft), $1.04 total of the $2 cap. Not done without the director's OK.
6. **Repeated doorway framing (minor)** → **partly fixed by #2.** C059 no longer shows the doorway or lantern. The act now runs medium shrine → close Ma → wide darshan, a pull-back reveal of the devotee. The brief is updated to say so.
7. **C037 yellow wall, black corner (minor)** → **fixed:** sat 0.72 (mid sat 0.74 → 0.64), lift 0.02 (p10 0.009 → 0.022). The 1° keystone is not fixed: the bake has no rotate, and it's minor.
8. **Brief lists 7 dissolves (minor)** → **fixed:** brief §4 now lists the 8 dissolves, the bloom and the freeze. **Disagree** on one detail: 11.80 is a hard cut, not an 8-frame dissolve. Frame-to-frame difference there is one spike (0.244 at frame 294→295), with ≈0.03 on both sides.
9. **C200 / C112 / C050 soft (minor)** → **fixed (partly):**
   - C200: cw 0.25 → 0.30 (1.67× upscale, was 2×) + mild unsharp;
   - C112, C050: mild unsharp.
- **v2b checks:**
  - every shot within ±0.022 of the 0.254 median luma, except C059 (0.150, deliberate);
  - Premiere export vs previz: median diff 1.7 %;
  - `verify_render` passes, except the designed fade-in;
  - Premiere V1 swapped to `V1_timeline_v3b.mov` (imported under a new name) in `Reel_uski-aankhein_v2`, saved.

### Loop 2 (v2b, `analysis/review_v2b.md`): FAIL, 0 blockers, 2 majors + 6 minors. Fixed in v2c and **editor-verified** (the gate's 2-loop limit is reached; no third blind run):
1. **Run cuts land half a beat before the loud strokes (major, "ear check decides")** → **intended for now; the director decides by ear at Checkpoint 2.**
   - *Confirmed:* at 14.24 / 15.40 / 16.64 / 17.80 / 19.00 the treble percussion stroke lands 6–7.5 frames after the cut, and the bass pulse sits within ±2.5 frames of 4 of the 5 cuts.
   - *Why not changed:* the cuts follow the analyzer's beat grid, which has been the approved run timing since v1, and the director has never flagged it ("never re-cut approved sections unless asked").
   - *Ready if asked:* slide the four run cuts +7 frames (363 / 392 / 423 / 452).
2. **C037 junction box, bare wall (major)** → **fixed.**
   - *Change:* push 0.56 → 0.50 with the photo high in frame (v 0.42, u 0.44). The box is out; only the picture-light bar shows; all six men are in frame.
   - *Check:* `analysis/review_v2b/v2c_c037.jpg`.
3. **C037 late lock (minor)** → **fixed by 2.** The old framing clamped the first 14 frames (the camera pans ~120 px). Now: 0 px movement on the photo, measured; the only clamp (≤ 35 px) is in frames 0–6, under the first half of the incoming dissolve.
4. **C059 hop at the hold (minor)** → **fixed:** the hold starts at 4.28 s (was 4.36). The seam is now 2 + 6 px (was 12).
5. **C059 top 40 % black (minor)** → **intended:** the deliberate dark beat. The reviewer offered "accept".
6. **Title pops off (minor)** → **fixed.** The old render was still at 15 % opacity on its last frame, so the clip end cut it off. The new title (`graphics/title/renders/title-alpha-v2b.mov`) fades out with a 0.7 s `sine.inOut` blur-out, ending at 1 %.
7. **AI esraj not an accurate esraj (minor)** → **intended; director asked at Checkpoint 2.** The re-prompt option costs ~$0.52 (spend would be $1.04 of the $2 cap).
8. **9.08 dissolve reads as a double exposure (minor)** → **fixed:** hard cut on the 9.07 stroke. 7 dissolves now.
- *Brief notes:*
  - must-not wording aligned (the bonedi act is medium → close → wide);
  - transition list updated;
  - the SFX −18.4 dB frame-RMS is fine.
- **v2c (`renders/exports/uski-aankhein_v2c_mix_tp.mp4` + `_v2c_IG.mp4`):**
  - Premiere V1 → `V1_timeline_v3c.mov`, V5 title → `title-alpha-v2b.mov` (both imported under new names), saved;
  - export vs previz: median diff 1.8 %;
  - `verify_render` passes (designed fade-in excepted);
  - editor frame scan (`analysis/review_v2c_editor_scan.json`): only the 4 designed spans;
  - all shots within ±0.028 of the median luma, except C059 (0.148, deliberate).

## Round 3 — Director notes (Checkpoint 2 on v2c, 2026-10-23)
Answers to the Checkpoint 2 questions (multiple choice):
1. Run cuts 14.2–19.0 s: **"Shift onto strokes"**. The four cuts at 14.24 / 15.40 / 16.64 / 17.80 move 7 frames later (frames 363 / 392 / 423 / 452), onto the loud percussion strokes. The sweep cut stays at 19.00, so the freeze stays on 19.60.
2. AI esraj: **"Keep it"**. No re-generation; AI spend stays $0.52.
3. Title: **"Start with her eye"**. The title appears with the dissolve into her eye (≈ 2.1 s) and is gone by ≈ 4.1 s, never over the instrument.
4. IG audio: **"Same as reference"**, the same song at the same start point. That closes the brief's open question: the cut stays timed to the reference audio.
- No free-text notes on "what would make it more cinematic?".
- Sequence for this round: `Reel_uski-aankhein_v3` (duplicated from v2).

## Round 3 — Changes made (v3)
1. **"Shift onto strokes"** → done. The run cuts moved from 356 / 385 / 416 / 445 to **363 / 392 / 423 / 452** (`analysis/edl_v3.json`, `analysis/transitions_v4.json`, `tools/bake_v4.py` → `renders/bakes_v4/V1_timeline_v4.mov`).
   - Shot lengths: C139 2.72 s (source to 12.44 s of 12.48), then C145, C208, C112 slide unchanged, and C200 shortens to 0.94 s. The sweep cut stays at 19.00 and the freeze on 19.60.
   - Check: the treble strokes now land −1.3…+0.5 frames from each cut (were +6…+7.5). The eye-line holds, and C139's tail is locked (0 px).
2. **"Keep it"** (AI esraj) → unchanged; spend stays $0.52.
3. **"Start with her eye"** → title re-timed (`graphics/title/index.html`, v2b copy kept as `index_v2b.html`) and rendered as `title-alpha-v3.mov`: 52 frames at reel 2.08–4.16 s. Line 2 follows 0.25 s behind, both lines are fully on 2.72–3.52 s, then a 0.65 s blur-out. 0–2.08 s is the esraj alone.
4. **"Same as reference"** (IG audio) → recorded in the brief; the cut stays timed to the reference audio.
- **Premiere:**
  - `Reel_uski-aankhein_v2` cloned → `Reel_uski-aankhein_v3`;
  - V1 → `V1_timeline_v4.mov`, V5 title → `title-alpha-v3.mov` at 52–104;
  - look check: one Lumetri, LUT, vignette −1 / 45 / 70; saved.
- **Exports:** `uski-aankhein_v3_mix_tp.mp4` (−14.1 LUFS / −1.9 dBTP) + `uski-aankhein_v3_IG.mp4` (−19 dBTP).
  - export vs previz: median diff 1.8 %;
  - `verify_render` passes, except the designed fade-in.

## Round 3 — Review gate
### Loop 1 (v3, `analysis/review_v3.md`): FAIL, 1 major + 3 minor. Fixed in v3b (`renders/exports/uski-aankhein_v3b_mix_tp.mp4`):
1. **Title legible over the instrument at 2.20–2.48 (major)** → **fixed.**
   - esraj→eye cut 2.40 → 2.16 s, dissolve 16 → 12 frames (48–60);
   - the esraj Screen ghost on C163 now clears over 16 frames (gone by 2.80 s, was 3.3);
   - the title is re-timed and re-rendered (`title-alpha-v3b.mov`, 42 frames) at 2.40–4.08 s.

   *Check:* the title first shows at frame 62 at ~30 % over a faint ghost, and is legible from 66, with the ghost gone (`analysis/review_v3b/title_strip2.jpg`).
2. **Blurred title over the photo (minor)** → **fixed:** the photo dissolve is shortened to 8 frames (100–108), and the title's blur-out is < 5 % by frame 100 and gone by 101.
3. **C163 dim (minor)** → **fixed:** +0.15 stop (exp −0.05 → +0.10). Luma 0.235 → 0.271, median 0.255 on my metric.
4. **C056 lime glass panel (minor)** → **fixed:** green-dominant pixels pulled toward max(R, B) (keeping 40 % of the excess; new bake param `green`). Green pixels −60 %, their saturation 0.43 → 0.11.
- Brief bookkeeping: the must-have "silence with just her eyes" now matches storyboard B (the house holds the near-silence).
- **v3b checks:**
  - Premiere V1 → `V1_timeline_v4b.mov`, V5 title → `title-alpha-v3b.mov` at 60–102 (new names), saved;
  - export vs previz: median 1.8 %;
  - `verify_render` passes (designed fade-in excepted);
  - scan: 4 designed spans only;
  - all shots within ±0.022 of the median luma, except C059 (deliberate).

### Loop 2 (v3b, `analysis/review_v3b.md`): FAIL, 1 major + 2 minor → **superseded by round 4**.
- **Title over the fading esraj ghost at 2.44–2.70 (major):** round 4 replaces this opening with "her eye opens" out of a black blink, so the ghost goes.
- **C200, C145 soft (minors):** fed into the round-4 footage re-plan ("shots themselves weak").
- v3b was not shown to the director; their round-4 notes came in while this loop ran.

## Round 4 — Director notes (2026-10-23, while the v3b review gate ran)
Quote: "The footage is very rando teh first transition s not upto the mark and neithe is all other transition, the colurs grading is also not on point"
Read as:
1. **"Footage is very random":** the shots don't feel connected. The order and choice read as arbitrary; exactly why is asked below.
2. **"First transition not up to the mark":** esraj → her eye (12-frame dissolve + Screen ghost).
3. **"Neither is all other transition":** the 7 soft dissolves + bloom. Note: the montage playbook and the studio default are hard cuts, with transitions only as seasoning on big hits; the eye-match dissolves came from round 1b ("transitions not cinematic").
4. **"Colour grading not on point":** G2 Gold & Shadow (picked in round 1b) no longer satisfies.
Next: one multiple-choice round to pin each note down, then previews before re-cutting.

### Round 4 — director's answers (2026-10-23)
- **Footage ("very random"):** all four readings apply:
  - too many places (keep fewer, mostly the bonedi bari night);
  - no flow between shots;
  - the photo / shrine / darshan act doesn't fit;
  - shots themselves weak.

  → New storyboard (footage survey `analysis/survey_round4/`, running).
- **First transition:** "Her eye opens": esraj → black blink on the string swell → her eye opens out of the dark.
- **Transitions:** watched `renders/previz/transitions_r4.mp4` (blink / zoom-through / hard cut + flash), then: "look at the reffernec video to understand the transtions and vidoe fading effects".
  - **Reference measured** (`analysis/ref_r4/`). Its only transitions are two **blinks** on the accents (7.93 s and 16.02 s): straight top and bottom lids with a wide soft (faded) edge close to a slit on the eyes over ~3 frames, go black for 1–2 frames, and reopen on the next shot over ~3 frames. The slit content goes soft. The opening is one long double exposure (player over the eye). No dissolves.
  - Rebuilt as `renders/previz/transitions_ref_r4.mp4` (`tools/transition_lab.py --ref`: lids close 0.62 / 0.28 / 0.06, black 1 frame, open 0.22 / 0.60 / 0.90; feather 9 % of the frame height).
  - Director: **"Accents + hard cuts"**: blink on the big accents (her eye opens 4.16, the drop 7.88, 11.80, the payoff 19.60); clean hard cuts on the drum strokes in between; **no soft dissolves**.
- **Grade:** "gold and shadow but a little reduced contrast". G2 variants (`tools/g2_contrast.py`, curve T(x) = x − 4c(x − 0.40)x(1 − x) on the cube output, black and white anchored; a first pivot version lifted black to 0.07 and was discarded). Director: **G2b2, −17 %** (`grade/uski_aankhein_G2b2_gold_shadow_c18.cube`).
  - It replaces G2 in the V3 Lumetri Creative look, and the custom cube must be loaded by hand (or by computer use).
  - Film-look sheet `analysis/looks_r4/looks_sheet_r4.jpg` shown; the director stayed with Gold & Shadow.

### Round 4 — storyboard v4 built locally (2026-10-23), then new footage note
- **Storyboard v4 approved** with the alternative in slot 4. **Run set A** (house B only: Saraswati, the lion, Kartik) chosen after a wider search found no bigger close-ups of Ma (`analysis/survey_round4/run_options.md`, `run_picksheet.jpg`).
- **Built locally:**
  - `analysis/edl_v4.json`, `analysis/transitions_v5.json`, `tools/bake_v5.py` → `renders/bakes_v5/V1_timeline_v5.mov`. New in the bake:
    - reference blink cut type;
    - `fixed` mode with frame-blended speed;
    - lock `u` → `u_end`;
    - same-clip pairing only;
    - rebaked rows replace older manifest entries.
  - Previz `renders/previz/uski-aankhein_v4_previz.mp4` (G2b2, title 4.48–7.48 `title-alpha-v4.mov`).
- **Checks:**
  - Pupils measured on gridded full-res crops: every face shot on the 768 line within ±25 px, start to end. C050 isn't static: a slow zoom/creep moves her eyes ~85 source px, so it is eye-locked.
  - Glide smooth (8→14 px/frame, no jitter).
  - Luma within ±0.027 of the median.
  - Scan: only the designed blink frames.
- Premiere v4 build **not started**.
- **Director (2026-10-23):** "There are some many better sttaues and idols that can be used which are subtle an dminimalistic". Asked which: **clay / terracotta, white / sholapith, art statues / theme**; "search every day".
  - → Footage search `analysis/survey_round4b/` (running). The structure, blinks, G2b2 and title placement stay; the house-B footage is up for replacement.

### Round 4b — minimal idols (2026-10-23/24)
- **Search** (`analysis/survey_round4b/`): 296 unique clips on six days; three one-family sets:
  - A: Oct 17 clay theme pandal;
  - B: Oct 16 terracotta;
  - C: Oct 18 white sholapith.
- **Director:** "Oct 16, 17 and 18 all can be used". → **v4b mix** (`analysis/survey_round4b/storyboard_mix.jpg`):
  - the Oct 17 clay pandal is the backbone: C163 her eye opens, C162 glide on the drop, C154 stone mother with eyes held, C164 whip + freeze bookending the same red Durga;
  - the run adds the other days: Oct 16 C121 terracotta → Oct 18 C208 white sholapith → Oct 17 C162 giant clay face (three materials, eyes bigger each time).
- **Build files:** `analysis/edl_v4b.json`, `transitions_v5b.json`, `tools/bake_v5b.py` (adds `reverse` playback for the C164 whip) → `renders/bakes_v5b/`. Same blinks, cut frames, G2b2 and title as v4. House-B v4 kept as an alternative.

### Round 4c — opening (2026-10-24)
- **v4b preview checks:**
  - pupils on the 768 line within ~20 px in every face shot, start to end (gridded crops);
  - luma within ±0.027 of the median after fixes: C154 stone exp 0 (was +0.6: luma +0.13, cream instead of grey); C121 sat 0.75;
  - glide smooth (10→28 px/frame);
  - scan: only the blinks and the whip's motion blur.
- **Director on the v4b opening blink:** "I don not like the first trandisition whay is itn not like the dinger is fading into the idol cinetic".
  - → New end-aligned transition types `dexp` (Screen double exposure) and `xfade` (plain), in `tools/bake_v5b.py` and `track_eyes.py`. The 104 cut is now a 44-frame (1.76 s) fade from 2.40 to the 4.16 swell; C163 src_in 1.4667 so its head starts at source 0.0.
  - Comparison `renders/previz/opening_fade_options_r4c.mp4`. Director: **"A Double exposure"**.
  - Full preview `renders/previz/uski-aankhein_v4c_previz.mp4`.

### Round 4d — composition plan (2026-10-24/26)
- **Director:** "Whay are we not panning it more why are we not using more auucrate fottages, also why are we shouldwing extra landscape , whay are we not dterming a compostiona nd accuracy."
- **Answers to the clarifying round:**
  - "Both": a composition plan, and a designed move per shot;
  - too wide: "Stone statue (11.8 s)" and "All shots";
  - accuracy: "Eyes are the subject".
- **Composition board** (`tools/comp_board.py`, `analysis/comp_v5/plan.json` → `board.jpg`): start/end frame of every shot through the planned crop, graded.
  - Every shot is an eye close-up (eyes 34–68 % of the width, ≤ ~2.8× enlargement) with one move: push, orbit, tilt reveal, whip or freeze push.
  - The board found two survey errors: C200's eye span is ~165 px, not 280, and C154's is ~176, not 207. C200 moved to the tilt-reveal slot; C208 to the run.
  - Director: **"Yes, build it"**; 14.52 = **stone mother close-up** (C154 0.00–0.97; the 7.88 orbit uses 1.00–4.27, so no footage repeats).
- **v5 build:** `analysis/edl_v5.json`, `transitions_v6.json`, `tools/bake_v6.py` (adds `v_end`, the designed tilt) → `renders/bakes_v6/`, preview `renders/previz/uski-aankhein_v5_previz.mp4`.

## Round 5 — Director notes on the v5 preview (2026-10-27)
- Quote: "Very bad image quality very bads frames very off from the concept of the reel the transitions are also very bad". (Cube loading for later: "You do it on screen".)
- **Editor's read (honest):**
  - *Quality:* 2.4–3.4× crops of phone footage plus sharpening, chasing "tighter / eyes are the subject".
  - *Concept drift:* the stone mother bust and the giant clay face aren't Durga. Nine shots with hard cuts on every stroke is a busy montage; the reference is two calm shots (a long double exposure of the player over an eye, then one pair of eyes with a blink).
  - *Transitions:* blinks plus hard cuts read as choppy.
- **Process lesson:** four rounds of footage and framing changes without re-anchoring on the concept. Next: a short re-brief anchored on the reference before any more cutting.

### Round 5 — re-brief answers (2026-10-27)
- **Concept:** "Like the reference": calm and intimate. The singer is double-exposed over Durga's eyes for the opening ~8 s, then one Durga's eyes held long; 3–4 shots, slow.
- **Idols:** "Durga + art statues".
- **Quality vs tightness:** "Tight eyes first". Quality has to come from processing: denoise before enlarging, gentle sharpening, the sharpest frame for holds, smooth slow-motion for long holds.
- **Transitions:** "Exactly like the reference": the long opening double exposure, then blinks only, on the reference's accents (7.88 and 16.02).
- **Plan v6, three shots:**
  - 0–7.88: singer × hero's eyes (Screen double exposure) + title;
  - 7.88: blink, then the hero's eyes held (slow push);
  - 16.02: blink, then closer on her eyes, end card, black at 21.96.
- **Editor-side quality bugs found:** the preview encodes were tagged full-range (yuvj420p), which crushes or hardens on many phone players → new previews in tv range; grain overlay 12 % → 6 %.

### Round 5 — v6 build (2026-10-27)
- **Choices:**
  - hero: **red clay Durga** (Oct 17);
  - quality route: **install the AI upscaler**. Real-ESRGAN ncnn-vulkan official macOS release v0.2.5.0 (51.8 MB, universal binary) is installed in `tools/realesrgan/`. At 1:1 it recovers eye outlines, lashes and the veins in the eye whites that Lanczos smears (`analysis/round5/esrgan_compare.jpg`).
- **Build:** `tools/bake_r5.py` → `renders/bakes_r5/V1_timeline_r5.mov`. Three shots:
  - A: singer × her face, Screen 0.55 at gain 0.8 (at 0.70/1.0 the white kurta washed shot A to luma 0.41);
  - B: C163 live, 137 frames AI-upscaled, then motion-interpolated to 203 (minterpolate drops ~2 end frames, so it stretches +2 and trims);
  - C: C164 live 51 frames, then held, eyes 68 → 76 % so it is visibly closer than B's end.
- **Preview:** `renders/previz/uski-aankhein_v6_previz.mp4` via `tools/previz_r5.sh`: G2b2, grain 6 %, title over shot B 8.60 s, booms 7.84 / 15.96, tv range.
- **Checks:**
  - eyes on the 40 % line in every frame checked;
  - upscaler flicker low (frame-to-frame change 0.005 in B);
  - luma A 0.33 / B 0.23 / C 0.25;
  - scan: only the designed blinks, fade and end black. A near-frozen eased stop at 21.36–21.88 is fixed with a constant-speed final push.

### Round 5b — more than one idol (2026-10-27)
- **On the v6 preview:** "Changes first", then "We are only using one idol?".
- **Answers:** "One idol per shot"; idols: **Red clay Durga, White sholapith Durga, Giant clay face**.
- **v7** (`tools/bake_r7.py` → `renders/bakes_r7/V1_timeline_r7.mov`), same reference structure and cut frames:
  - A: singer × red clay Durga (reused from r5);
  - blink 7.88 → B: white sholapith (Oct18 C208 0.00–4.03, eye-locked, AI-upscaled, slowed ~1.68×), title over her;
  - blink 16.00 → C: giant clay face (Oct17 C162 5.77–7.14: the glide lands on her, eye-locked, then held under a constant push; native-resolution downscale, no AI needed).
- Tracks: `analysis/eye_tracks_r5b.json` (scores 0.94+).

### Round 5c — finishing (2026-10-27)
- **On v7:** "Th evideo looks nice but a lot of cinemtic colur correction shot stanilsationa nd vidoe nehancement need to be done, foptage is of low quality."
- **Diagnosis:** measured shake was small; the real problem was **texture shimmer**. v7 AI-upscaled every frame and interpolated slow motion in shot B, so detail was redrawn each frame (`analysis/review_v7/B_interp_strip.jpg`). C also had a 5 px jolt from a track kink.
- **v8 fixes:**
  - B = the white sholapith's sharpest frame, denoised, AI-enhanced once, with a smooth push and a 1 % drift (jitter 0.02 px, no shimmer);
  - C = live clay-face glide, denoised, live part ends before the kink, smoother path (0.24 px RMS).
- Colour variants (`tools/colour_variants.py`, `analysis/round5/colour_variants.jpg`).
- **Director:** "Rich and deep there are some light flickering issue deal with it".
- **v9:**
  - **Flicker:** C's live frames pulsed ~0.8 % on a 3-frame cycle (mains-powered lights vs 30 fps, also in the source). Per-frame gain to the 9-frame face-luma trend: 0.04 % now, the same as the stills.
  - **Look:** `grade/uski_aankhein_G2r_rich_deep.cube` = G2 + split-tone + soft mid contrast; clarity (local contrast) baked into V1.
  - Preview `renders/previz/uski-aankhein_v9_previz.mp4`; scan clean.

### Round 5 — Premiere v9 build (2026-10-28; director: "Yes, Premiere is free")
- **Build:** `analysis/_es_v9_build.jsx`, path-guarded (pujo's v13 was in front). Cloned v3 → `Reel_uski-aankhein_v9`:
  - V1 → `V1_timeline_v9.mov` (copy of `renders/bakes_r7/V1_timeline_r7.mov`);
  - V5 title `title-alpha-v2b.mov` at 215–295 (8.60 s); end card 515–549;
  - V4 grain opacity 12 → 6;
  - A2 second boom 489 → 399 (the 16.00 blink), −16 dB.
- **Look:** loaded on screen (director: "You do it on screen"; full-screen control approved on the second try).
  - The adjustment layer was selected by script (`setSelected`), since background clicks can't reach Premiere's full-screen Space.
  - Lumetri → Creative → Look → Browse… → `uski_aankhein_G2r_rich_deep.cube`, chosen with the keyboard: the macOS open panel is a separate XPC process that computer use can't click.
  - Look check: one Lumetri, look path 105 chars (G2r), intensity 100, vignette −1/45/70. Saved 01:27.
- **Exports:**
  - `uski-aankhein_v9_mix.mp4` → alimiter → `uski-aankhein_v9_mix_tp.mp4` (−14.1 LUFS / −1.9 dBTP);
  - `uski-aankhein_v9_IG.mp4` (−19 dBTP).

  Export vs v9 preview: median frame diff 1.8 %, luma within +0.011 per shot. `verify_render` passes except the designed black frames (fade-in, the two blink beats).

## Round 5 — Review gate
### Loop 1 (v9, `analysis/review_v9.md`): FAIL, 2 major + 3 minor. Fixed in v9b (`tools/bake_r9b.py` → `renders/bakes_r9b/V1_timeline_v9b.mov`):
1. **A: the esraj ghost veils the opening and sits down the centre of her face (major)** → **fixed.**
   - *Cause:* the AI player's white kurta fills its frame, so a full-frame Screen lifts everything (pre-look p10 0.197 vs 0.074 / 0.069 in B / C; mean 0.380 vs 0.305). The instrument neck was centred, so it ran between her eyes, and the fretting hand crossed her right eye at 3.5–5 s.
   - *Fix:* the reference's split:
     - the player layer moved 380 px left and 220 px up, so the neck, pegs and fretting hand sit left of her face and the bow reaches in at eye level;
     - Screen weight 0.78 on the left, ramping to 0.30 over her face, with a soft hole (−70 %) over her eyes; the moved layer's edges feathered 160 px;
     - the ghost's low-frequency veil taken back out (inverse Screen on its σ≈32 px blur, 75 %): its lines and forms stay, its haze goes;
     - one black point and one gain for the whole shot, so p10 and mean match B / C.
   - *Check:* `analysis/round5/r9b/testA_sheet.jpg`, `renders/bakes_r9b/testA_100.png`. Measured on the bake and the export below.
2. **B: the gold nath rendered as a smear (major)** → **fixed in part; the rest is the real jewellery.**
   - *Cause:* the nath is real (a gold stud and chain to the ear; `analysis/round5/r9b/b_nose_compare.jpg`: raw / plain / AI / 50-50). Real-ESRGAN redraws its 20 px links as blobs.
   - *Fix:* the AI still is blended with the plain denoised Lanczos enlargement: AI 55 % overall, 20 % over the nath (soft ellipse).
   - *Result (honest):* the crunchy AI edges go, but the nath still reads as a cluster of gold beads at the nostril, because that is what the source holds at this size (`analysis/round5/r9b/nath_v9_v9b.jpg`). Pulling its highlights down was tried and rejected: it turned the gold into a grey-green stain (`analysis/round5/r9b/nath_tone_test.jpg`). Left for loop 2 to judge as real jewellery.
3. **B: waxy AI texture on the shola crown and silver (minor)** → **fixed** by the same blend (AI 55 %).
4. **C: end card on the scaffolding (minor)** → **fixed:** V5 end card moved up 240 px (cap top 1468 → 1228), onto the clay of her chin. In Premiere: Motion position on the V5 clip, not a new render.
5. **C: the scaffold band pulls the eye (minor)** → **fixed:** a soft graduated darkening on the bottom of the frame (from 60 % of the height down to ×0.52 at the bottom edge), baked into C. The push is unchanged, so the live→hold handover stays continuous.
- **v9b preview checks** (`renders/previz/uski-aankhein_v9b_previz.mp4`):
  - per-shot luma after the look: A 0.246 / B 0.251 / C 0.247 (v9: A 0.328); p10 A 0.015 vs B 0.010 / C 0.006 (v9: A 0.091);
  - frames `analysis/round5/r9b/compare_v9_v9b.jpg` (top v9, bottom v9b): her eyes clear in A, the player on the left;
  - end card on the chin clay (`analysis/round5/r9b/endcard_v9b_crop.png`).
- **Premiere v9b** (director: "Yes, Premiere is free"; `analysis/_es_v9b_build.jsx`, path-guarded):
  - v9 cloned → `Reel_uski-aankhein_v9b`;
  - V1 → `V1_timeline_v9b.mov`;
  - V5 end card Motion position (0.5, 0.5) → (0.5, 0.375), i.e. up 240 px.

  The V3 look carried over with the clone: one Lumetri, G2r cube path (105 chars), intensity 100, vignette −1/45/70. No on-screen step was needed. Saved.
- **Exports:**
  - `uski-aankhein_v9b_mix.mp4` → alimiter → `_mix_tp.mp4`: −14.1 LUFS / −1.9 dBTP;
  - `uski-aankhein_v9b_IG.mp4`: −19.0 dBTP, SFX only;
  - `verify_render`: only the designed black frames flag.
- **Export vs the v9b preview:** median frame diff 1.86 % (max 2.21 %), shot luma +0.005…+0.009. Per-shot mean luma: A 0.256 / B 0.260 / C 0.253.
- **Frame scan** (`analysis/review_v9b/scan.json`): the 9 designed spans only (fade-in, two blinks, end black).
- **Notes from the reviewer, not defects:**
  - B is one still frame under an 8 s push. That is the v8 plan (per-frame AI shimmered) and the director will be told at Checkpoint 2.
  - Brief §0 said "only the red clay Durga". Fixed: three Durgas, one per shot.

### Loop 2 (v9b, `analysis/review_v9b.md`): **PASS**, 0 blockers, 0 majors, 4 minors. Three fixed in v9c (`tools/bake_r9c.py` → `renders/bakes_r9c/V1_timeline_v9c.mov`), **editor-verified** (the gate's 2-loop limit is reached; no third blind run):
1. **C: the cheeks still pulse in anti-phase, ~1.2 % (minor)** → **fixed.**
   - *Cause:* the v9 deflicker was one gain per frame, and one lamp beats against 30 fps. My measurement on the bake: 0.54 / 0.69 % rms, 1.14 / 1.20 % max on the left / right cheek.
   - *Fix:* a regional deflicker on the live frames: a 40 px block luma field, softened, matched to its own 9-frame moving average. The hold keeps the last live frame's field.
2. **C: bright panel in the bottom-right corner, 16–20 s (minor)** → **fixed:** an extra corner darkening (−45 % at the corner, fading out by 80 % of the height and 45 % of the width) on top of the bottom grad.
3. **B: the title's sub-line is soft on the gold chest ornament (minor)** → **fixed:** a soft dark plate (−28 % at its centre, ellipse 430 × 140 px around the two lines), baked into V1 and timed to the title (in 8.60–9.20, out 11.20–11.80).
4. **B: the nath reads as a gold blob (minor)** → **intended:** it is the real nose ring and chain, overexposed in the source. The AI share there is already 20 %; pulling its highlights turned it grey-green (`analysis/round5/r9b/nath_tone_test.jpg`). The reviewer offers "accept" as an option. The director sees it at Checkpoint 2.
- **v9c checks (editor-verified):**
  - Premiere (director: "Yes, Premiere is free"; `analysis/_es_v9c_build.jsx`): v9b cloned → `Reel_uski-aankhein_v9c`, V1 → `V1_timeline_v9c.mov`. End card (0.5, 0.375) and the V3 look (one Lumetri, G2r, 100, vignette −1/45/70) carried over. Saved.
  - Exports:
    - `uski-aankhein_v9c_mix_tp.mp4`: −14.1 LUFS / −1.9 dBTP;
    - `uski-aankhein_v9c_IG.mp4`: −19.0 dBTP, SFX only;
    - `verify_render`: only the designed black frames flag.
  - Export vs the v9c preview: median 1.81 % (max 2.16 %).
  - Frame scan (`analysis/review_v9c_editor_scan.json`): the 9 designed spans only.
  - Cheek flicker on the export, 16.12–17.40 s: v9b left / right max 0.94 / 1.61 % → v9c 0.19 / 0.37 %. Handover jump unchanged (0.0005).
  - Corner panel luma at 17.0 s: 0.149 → 0.081. Sub-line background at 10.0 s: 0.412 → 0.327. Face unchanged (0.519 → 0.521).
  - Frames: `analysis/round5/r9b/compare_v9b_v9c.jpg`, `title_v9b_v9c.jpg`.
- **Not changed:**
  - The craft note on A (the ghost's string lines cross her nose bridge): it reads as the instrument, and the reviewer says so too.
  - The "boom at 15.96 may be masked by the 16.02 accent": it lands inside the blink black, at the same level as the first boom (−16 dB). It is judged by ear at Checkpoint 2.

## Round 6 — Director notes on the delivered file (2026-10-28/29)
- "The render whe exported to iphone hass very porr quality" (the v9c `_IG` file, by AirDrop).
- What looks poor: all four of "Soft / blurry", "Plastic / painted faces", "Blocky or noisy darks", "Worse than on the Mac".
- **Diagnosis** (`analysis/ig/quality/`):
  - The file matched a lossless render of the same frames (`export_vs_lossless.png`), so the transfer was not the cause and the encode was not the main loss.
  - **Soft / plastic:** the eye close-ups enlarged night phone HEVC (4K, 60 Mb/s, in-camera NR) by 1.65× (A) and 1.9–2.5× (B). A strong single-frame denoise (nlmeans 1.6), Real-ESRGAN and clarity 0.18 then repainted the texture, which the phone shows at full sharpness.
  - **Blocky darks:** Premiere's "Match Source - H.264 High Bitrate" preset encodes Main profile at 9.5 Mb/s, with B-frames of ~23 KB.
- **Options shown** (`options_A/B/C.jpg`): NOW / REAL frames at the same framing / REAL + WIDER. Director: **"Real frames + wider"**.

## Round 6 — Changes made (v10)
1. **Soft / blurry + plastic faces:**
   - A and B are now a stack of 21 aligned real source frames (sub-pixel phase correlation, trimmed mean; `tools/stack_r9d.py`), with a fine unsharp at output size. No Real-ESRGAN and no nlmeans on them.
   - A and B are framed wider, so enlargement stays ≤ 1.42×:
     - A: eye pair 27 → 31 % of the width (was 36 → 42 %, 1.65×+);
     - B: 26 → 31 % (was 42 → 54 %, up to 2.5×).
   - C keeps its framing (a native downscale). The denoise now only works in the shadows, so the clay and straw keep their texture.
   - Clarity 0.18 → 0.08. `tools/bake_r10.py` → `renders/bakes_r10/V1_timeline_v10.mov`.
   - Ghost, blinks, title plate, deflicker and the C grad/corner are unchanged. Per-shot luma matches v9c within 0.003.
2. **Blocky / noisy darks:**
   - Premiere now exports a ProRes 422 master (`analysis/_es_export_v10.jsx`).
   - The delivery H.264 is encoded from it (`tools/encode_hq.sh`): High profile, CRF 15, tune film, aq-mode 3, light deblock, 2 s GOP, BT.709 tv range. That gives 13.8 Mb/s.
   - Against the master:

     | | PSNR Y | SSIM min | Shadows PSNR (A / C) |
     |---|---|---|---|
     | Premiere's H.264 preset (same v10 sequence) | 44.3 dB | 0.967 | 41.7 / 46.8 dB |
     | New encode | 46.4 dB | 0.989 | 44.2 / 47.7 dB |
3. **Worse than on the Mac:** covered by 1 and 2. The phone shows 1080×1920 at full sharpness, so I now judge quality on 100 % crops (`v9c_vs_v10_crops.png`).
- **Premiere** (director: "Yes, Premiere is free"; another reel's project was also open, and the path guard switched to uski first):
  - v9c cloned → `Reel_uski-aankhein_v10`; V1 → `V1_timeline_v10.mov`;
  - the look carried over: one Lumetri, G2r, 100, vignette −1/45/70. Saved.
- **Checks:**
  - `verify_render`: mix −14.1 LUFS / −1.9 dBTP; IG −18.9 dBTP; 13.8 Mb/s; only the designed black frames flag.
  - Frame scan: the 9 designed spans only.
  - Export vs the v10 preview: median 1.93 %.
  - Cheek flicker max 0.17 / 0.42 %.

## Round 6 — Review gate
### Loop 1 (v10, `analysis/review_v10.md`): FAIL, 1 major + 2 minor. Fixed in v10b (`tools/bake_r10b.py` → `renders/bakes_r10b/V1_timeline_v10b.mov`). **Editor-verified, no second blind run:** the director was waiting ("y taking so long?") and the change touches shot B only, plus the grain level.
1. **B softer than A at 100 % (major)** → **fixed.**
   - *Cause:* the 21-frame 1× stack lost ~35 % of a single frame's high-frequency energy (Laplacian var 0.00108 vs 0.00165). Sub-pixel cubic shifts at 1× and residual misalignment averaged the detail away.
   - *Fix:* shift-and-add (`tools/stack_r10b.py`): the 9 sharpest of 21 frames, each upsampled 2×, aligned at 2× and trimmed-mean averaged, so the push resamples only once. Framed a little wider: eye pair 24 → 28 % (1.10 → 1.29×).
   - *Check:* B face Laplacian var on the export 0.00074 / 0.00061 → 0.00106 / 0.00087 (12.5 / 15.5 s), +43 % (`analysis/ig/quality/B_fix_compare.jpg`).
2. **Title on bright gold (minor)** → **fixed:** the soft dark plate under the title −28 % → −36 %. Sub-line background luma 0.318 → 0.288.
3. **No moving grain (minor)** → **partly.**
   - V4 grain 6 → 9 %. Measured, though, the studio grain clip (`renders/texture/grain_25fps_v1.mov`) does move (frame diff 7/255) but is faint (std 6.2/255). At 6–12 % Overlay it changes the picture by ~0.3/255, so it has been invisible in every version.
   - Visible grain would need ~40–60 % Overlay. That is offered to the director as a follow-up, not done → CR item 31.
- **v10b checks:**
  - Premiere (director: "Yes, Premiere is free"): v10 cloned → `Reel_uski-aankhein_v10b`, V1 → `V1_timeline_v10b.mov`, grain 9. The look carried over (one Lumetri, G2r, 100, vignette −1/45/70). Saved.
  - Exports: ProRes masters → `tools/encode_hq.sh`. Mix: −14.1 LUFS / −1.9 dBTP, 14.6 Mb/s High. IG: −18.9 dBTP.
  - `verify_render` and the frame scan (`analysis/review_v10b_editor_scan.json`): only the designed spans flag.
  - Export vs the v10b preview: median 1.90 %.
- **Delivered:** `deliver/uski-aankhein_IG.mp4` = v10b `_IG`. UPLOAD.md updated.

- **Director, 2026-10-30:** "Keep v10b as is. I'll check it on the phone." Visible grain was not added (grain stays 9 %, effectively invisible; CR item 31).

## Instagram package
Director approved v9c on 2026-10-28 ("Approved. Go ahead with the Instagram package."). Kit: `deliver/` (`UPLOAD.md`, `caption.txt`, `cover.jpg`, `cover_grid_check.jpg`, `uski-aankhein_IG.mp4` = `renders/exports/uski-aankhein_v9c_IG.mp4`).
- **Hooks** (first line, all under 125 characters):
  1. "This Durga Puja, I only filmed her eyes." (40) **recommended**: the subject is in plain search words, and it promises what the reel does;
  2. "If her eyes were music, this is how they would sound." (53): the title's idea;
  3. "A red clay Durga, a white sholapith Durga, a giant clay face. I only looked at their eyes." (90): names all three idols.
- **Caption** (`deliver/caption.txt`, 640 characters):
  - hook 1;
  - the three idols and the two shoot dates (17 and 18 October);
  - the title line;
  - one send CTA: "Send this to the friend who always looks at her eyes first.";
  - the AI credit line.
- **AI credit line:** "Edited with AI: @claudeai cut, graded and finished it in Adobe Premiere Pro (@adobevideo) via MCP, and sharpened the close-ups with an AI upscaler, from my footage and direction. The esraj player in the opening is AI-generated; the idols are real and filmed by me." Handles are the verified ones from `instagram-strategy.md`; never @premierepro.
- **AI info label: ON.** The reel contains a generated shot (AI esraj, Veo 3.1 Lite; `motion-and-ai.md` §3).
- **Hashtags (5, on subject):** #durgapuja #durgapujo2026 #maadurga #durgaidol #pujodiaries
- **Humanizer audit** (`ig-humanizer --mode audit`): PASS with 2 warnings, both fixed:
  - the "A X. A Y. A Z." fragment triad became one sentence with concrete items;
  - added a dated fact with a referent (two nights, 17 and 18 October).

  0 em dashes, 0 emoji, 2 standalone fragments (the hook and the title line), no vocabulary markers.
- **Cover:**
  - The first proposal (reel 10.6 s, the white sholapith with the title) got the note "Use a better cover".
  - I designed four options (`tools/cover_r9.py`, `analysis/ig/cover_options_v2.jpg`). The director picked **A, eyes band** (`deliver/cover.jpg`): a black frame with a wide band of the red clay Durga's eyes (the AI still, v9b grade + the G2r look, eye pair at 62 % of the width), "USKI AANKHEIN" above and "if her eyes were music" below, in the reel's DIN Condensed, cream with a dark halo.
  - It echoes the reference's letterbox. Eyes and title stay inside the 3:4 grid crop.
- **Alt text:** in `deliver/UPLOAD.md`.
- **Location:** the director's pick (city or pandal). The pandal names aren't in the footage metadata.
- **Music:** the reference reel's song from its start, added in the app ("Same as reference", round 3).
- **Not suggested:** collab invite, Story share (director profile).
