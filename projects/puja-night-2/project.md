# Project Log

| Field | Value |
|---|---|
| Reel name | puja-night-2 |
| Status | done (2026-10-19): v6d final, Instagram package approved, retro written (`retro.md`, `studio/retros/puja-night-2.md`), 8 CRs open for HQ |
| Reel type | music-montage |
| Arch version | 0.5.3 (v0.5.1 adopted at round 2; 0.5.3 for round 3: HQ relayed that the director wants motion graphics / text-behind / AI considered) |
| Pilot | yes |
| Current round | 6 |
| Premiere project | projects/puja-night-2/puja-night-2.prproj |
| Latest sequence | Reel_puja-night-2_v6d (d50965a2-8ca5-4a0d-9316-27bd64a52828); v6 abandoned; v1–v6c kept as rollbacks |
| Latest export | renders/exports/puja-night-2_v6d_mix.mp4 + _v6d_IG.mp4 (55.60 s) |

## Approved decisions
- Hook: **A** — C103 20.40 s, woodcut pandal outside, fade up + push 100→108, title 0.8–4.2, first cut 4.76 (approved 2026-10-18)
- Target runtime: 59.82 s (music section 3:31.88–4:31.70)
- Grade / LUT: Match Reference (Kodak 2393 built-in ~40 % base, look contrast, vignette, 12 % grain)
- Caption style: title `PUJA NIGHTS · 2026` + end card `@satyajitmall`; no location tags
- Music: *Shondhatara* (Coke Studio Bangla S2, Arnob × Sunidhi Nayak × Adit Rahman, 7:15). **Round 4: section D 1:45.60–2:41.20** (was A 3:31.88–4:31.70). Director's own copy (Music library) linked as a **cutting guide** at `music/shondhatara_GUIDE.mp3`, not in `assets/music/` (not a licensed sync copy). Plan: post with IG's library Shondhatara from the same start point.

## Friction log
<!-- Pilot reels: one line each time something is slow, fails, needs a guess, a manual step or a workaround. Format: `- [phase] what happened → workaround → CR filed? (CR id / no)` -->
- [Phase 0] Director gave the music as a YouTube link to a commercial song. Studio has no flow for "song from a streaming link" (can't download: unlicensed, YouTube ToS) → asked director for an owned/licensed file or the IG-audio-at-upload route → CR-20261018-puja-night-2-commercial-music-ig
- [Phase 0] ElevenLabs Scribe returned **401 Invalid API key** (`.env` key is stale) and no local Whisper is installed → couldn't transcribe the reference to check for narration; used chroma cross-correlation vs the song + level diff instead (proved no VO) → CR-20261018-puja-night-2-script-bugs
- [Phase 1] ~18 of 62 clips are recorded upside down (phone/camera held inverted at night); `analyze_footage.py` doesn't flag orientation → listed by eye from overview sheets; will rotate 180° in Premiere → CR-20261018-puja-night-2-script-bugs (repeat of CR-20261016-my-reel-footage-overview → studio rule)
- [Phase 1] The beat analyser's "Candidate cuts" rank by energy only (all its 45/60 s picks are high-energy); a calm brief needed a manual pick from the per-bar table + rendered previews for the director's ear → wrote 3 preview MP3s with ffmpeg → CR-20261018-puja-night-2-script-bugs
- [Phase 1] Contact sheets show 6 frames per clip but I needed in/out-specific frames for ~28 shortlisted clips → wrote a throwaway strip-sheet script in the scratchpad (6 labelled frames per clip, 7 clips per sheet) → no CR (watch.py + selects cover it once a cut exists)
- [Phase 1] Premiere has `my-reel.prproj` open and the my-reel session is still active; the studio has no rule for two reel sessions sharing one Premiere → held all Premiere work until after Checkpoint 1 and asked the director → CR-20261018-puja-night-2-premiere-session-setup
- [Phase 3] `create_project` opened the new project *alongside* my-reel.prproj; `get_project_info` still reported my-reel's `Reel_my-reel_v10` as the active sequence → passed explicit sequence IDs everywhere and set `activeSequence` by script → CR-20261018-puja-night-2-premiere-session-setup
- [Phase 3] `add_to_timeline_batch` placed the MP3 at source 211.84 instead of 211.88 (1 frame early). `projectItem.setInPoint(ticks or seconds, 4)` was silently ignored for this audio-only item (it reads back 211.878 on a weird MP3 timebase); `setInPoint(211.88, 2)` (audio) worked → CR-20261018-puja-night-2-extendscript-notes
- [Phase 3] `export_frame` failed with `Illegal Parameter type` even without `format`, until the output path had a `.png` extension and `renders/stills/` existed (template has no `stills/` folder) → created folder, used `.png` → CR-20261018-puja-night-2-premiere-session-setup
- [Phase 3] ExtendScript object keys `in`/`out` are reserved words (ES3) → whole `evalScript` failed with a generic CEP error → renamed keys → CR-20261018-puja-night-2-extendscript-notes
- [Phase 4] Adjustment layer took 4 rounds: the director's File › New landed in the other open project (my-reel), then the menu item stayed disabled (Project panel not focused; Premiere on another Space, the director's Space is a full-screen app, so `app_bring_to_current_space` and background menu clicks failed) → editor used full-screen control + Finder (Dock) grant and made it in 3 clicks (~15 min total) → CR-20261018-puja-night-2-premiere-session-setup
- [Phase 4] ExtendScript `File.write` silently wrote 0 bytes when the JSON held Lumetri property names with non-ASCII characters → `f.encoding="UTF-8"` before `open` → CR-20261018-puja-night-2-extendscript-notes
- [Phase 4] 14 separate `export_frame` calls per check is slow → one ExtendScript loop with QE `exportFramePNG(timecode, path)` exports all 14 stills in one call → CR-20261018-puja-night-2-extendscript-notes
- [Phase 4] `color_correct` also writes its temp/tint into Lumetri's HSL Secondary block (idx 101/102) → zeroed by script → CR-20261018-puja-night-2-extendscript-notes
- [Phase 5] `shake_report.py` crashed on the source .mov files (`could not convert string to float: '1,'`, ffprobe trailing comma) → measured on 540×960 proxies of each shot's source range → CR-20261018-puja-night-2-script-bugs.
- [Phase 7b] Two gate loops were spent on soft footage I hadn't screened: the phone hunted focus in the dark (C081, C089, C139, C137, C078–C082 all have long out-of-focus stretches). `selects_score.py` ranks 1 s windows by relative sharpness and `frame_scan.py` flags dips relative to the shot median, so a shot that is soft for most of its length passes both; my own first check ran at half resolution and missed C139's 1.9 s soft head → full-res absolute per-frame Laplacian per candidate clip before the EDL → CR-20261018-puja-night-2-focus-qa.
- [Phase 7b] No trim-in-place recipe: every fix meant remove + re-place + re-apply Lumetri, scale, rotation, keys, Warp (re-analysis), transitions and A1 levels (~15 min per loop) → CR-20261018-puja-night-2-focus-qa (trim recipe request).
- [Phase 7b] After `speed_change`, trackItem `inPoint`/`outPoint` read back in speed-scaled time and `outPoint` didn't refresh after setting `end`; verified by render instead → CR-20261018-puja-night-2-extendscript-notes (follow-up).
- [Round 3] A baked clip placed on V1 (after trimming C095 with `trackItem.end`) rendered transparent — grey grain over black — in stills and export; same media on V2 fine; fresh re-place, H.264 relink and no-effects tests didn't fix it (~20 min) → V2 overlay over the untouched V1 shot → CR-20261018-puja-night-2-motion-ai.
- [Round 3] `text_behind.py` fixes the word to the screen; C095's hold drifts ~60 px/s → reel-local tracked variant `tools/text_behind_tracked.py` (matte-anchored, smoothed, fades) → CR-20261018-puja-night-2-motion-ai.
- [Round 3] Bridge reported "not running" right after an export; `verify_premiere_connection` showed it connected again a moment later → no CR (pilot saw the same).
- [Round 3] I added C087 to the reveal after checking its sharpness and steadiness but not its orientation; it was recorded upside down and the blind reviewer caught it as a blocker (the 2nd reel with many inverted clips) → CR-20261018-puja-night-2-script-bugs (orientation check) — add "orientation of every newly added clip" to the gate checklist.
- [Round 3] Freeze-frame over source blur: `razor_timeline_at_time` on V1/A1 + `speed_change 0.01` on the middle piece holds its first frame (scan reports it as "frozen") → CR-20261018-puja-night-2-extendscript-notes (recipe).
- [Round 4] The Premiere MCP bridge stopped sending a heartbeat at 11:41, during the 42-min blind review; when the director restarted it, Premiere had the **Auto-Save copy** (`Adobe Premiere Pro Auto-Save/…11-38-31.prproj`) open, not the main project. The main file was newer (11:41:52, after the v4b export) → opened the main project and closed the auto-save copy without saving (~10 min, one director round-trip) → CR-20261018-puja-night-2-premiere-session-setup (follow-up).
- [Round 4] v4b's static soft PNG mask + 12-frame dissolve left C088's phone screens visible for ~1.5 s (gate loop 2 major); the studio has no tracked-mask tool → reel-local `tools/phone_mask_tracked.py` (pan by phase correlation, screens by colour, hull or box per phone, ProRes 4444 alpha in reel space) → CR-20261018-puja-night-2-motion-ai (follow-up).
- [Round 4] Premiere composited a ProRes 4444 overlay pixel with file alpha 0.97 (ffmpeg `prores_ks`, yuva444p12le) at ≈ 0.87 effective (core p95 luma 31 vs ≈ 7 expected) → full-opacity cores (1.0) → CR-20261018-puja-night-2-extendscript-notes (follow-up).
- [Round 4] Trim without remove + re-place: `trackItem.start = t` trims the head (in/out read back stale), and **`trackItem.inPoint` / `outPoint` are writable** (verified by stills against the source); DOM `transition.remove(false,false)` removes a transition. That covers v4c's re-cut in 3 small scripts → CR-20261018-puja-night-2-extendscript-notes (follow-up; answers part of the focus-qa trim-recipe request).
- [Round 5] `add_track {position: "below"}` inserted the new audio track at **index 0**, shifting A1→A2, A2→A3, A3→A4 (the `_IG` export would have muted the SFX instead of the music) → deleted it and used `position: "above"` (new track at the end) → CR-20261018-puja-night-2-extendscript-notes (follow-up).
- [Round 5] A script that reframed two clips, imported a ProRes 4444 `.mov`, placed it with a trimmed in-point and exported 4 QE stills hung the bridge (45 s timeout, heartbeat alive, no result written, no save); Premiere sat in a full-screen Space the editor can't reach → director check → CR-20261018-puja-night-2-premiere-session-setup (follow-up).
- [Round 5] Round 5 needed many short moments, but the studio's selects only keep the top 3 per clip → reel-local `tools/shot_pool.py` (per-frame sharpness at 1080 × 1920, motion, luma for all 62 clips, ~4 min) found 17 unused clips with usable material → CR-20261018-puja-night-2-focus-qa (follow-up).
- [Round 5] No studio tool for a text-mask (footage inside letters) title → reel-local `tools/durga_intro.py` (fill / behind modes, beat-timed flips, renders from the graded export) → CR-20261018-puja-night-2-motion-ai (follow-up).
- [Round 5] **Orientation again (4th time):** C085 and C086 went into v5 upside-down; the blind reviewer caught both as blockers in loop 2 (loop 1 missed them). My EDL marked C087 `rot:180` but not its forge siblings, and the check sheet's abstract content (nuts, spikes) looked plausible both ways. Rotated in v5c → CR-20261018-puja-night-2-script-bugs (follow-up: orientation must be decided per clip from readable cues such as text and the ground, and logged in a table before placement).
- [Round 5] C097 scored high on the Laplacian (245–320) in a fast pan whose frames are heavy horizontal smear: streak texture fools the sharpness metric → rejected by eye → CR-20261018-puja-night-2-focus-qa (follow-up).
- [Round 6] **Warp Stabilizer analysis can't be started by script.** QE `addVideoEffect("Warp Stabilizer")` leaves every clip at "Click Analyze to begin" (banner in renders); setting Warp's unnamed boolean params 0/1 doesn't start it; effects can't be removed, so v6 (22 clips with un-analysed Warp) was abandoned and rebuilt as v6b. MCP `stabilize_clip` started analysis on only 7 of 25 clips (both nests, C090, C095, C096, C101, C129); 18 stayed at "Click Analyze to begin" after 6 min → director clicks Analyze → CR-20261018-puja-night-2-extendscript-notes (follow-up).
- [Round 6] Swapped-in clips placed by `overwriteClip` keep Premiere's default scale 100 % (a 2× zoom on 4K into 1080 × 1920); my swap script didn't set 50 % → caught as "over-zoom, soft" in QA → CR-20261018-puja-night-2-extendscript-notes (follow-up: placement helper must always set the base scale).
- [Round 6] Warp side-effects: smoothness 100 by script → "extreme cropping" error frame that doesn't clear when set back; Warp on a reframed clip (C096 62 %) introduced a 2-frame judder the source doesn't have; a dissolve across Warp clips shows the analysis banner (handles not analysed) → CR-20261018-puja-night-2-extendscript-notes (follow-up).
- [Round 6] The gate's loop-2 major on C087 (stuttering push) was in the **source**: CFR 25 fps, but the camera's own zoom steps unevenly (frame-diff cadence 0.16 vs ≤ 0.03 on smooth shots). My QA measured translation jitter only, which a zoom doesn't show → removed the shot; added a frame-difference cadence check (std / mean of frame differences) to my per-shot QA → CR-20261018-puja-night-2-focus-qa (follow-up: cadence per shot in `frame_scan.py` / `shake_report.py`).
- [Round 6] Nesting a speed-changed clip to Warp it (the studio recipe) renders at the 1080 × 1920 nest size, so any reframe of the nest above 100 % is an upscale: C132 at 128 % went soft (Laplacian 44 vs 140–1000 elsewhere) → un-nested; speed on the 4K clip itself, no Warp → CR-20261018-puja-night-2-extendscript-notes (follow-up: warn in the nest recipe; nest at 2160 × 3840 or don't reframe the nest).
- [Round 6] 150 % speed with frame sampling steps 1-2-1-2 source frames (cadence 0.24). The DOM TrackItem has no interpolation call and MCP `set_time_interpolation` only toggles QE `setFrameBlend`; **QE `trackItem.setTimeInterpolationType(2)` sets Optical Flow** (readback `timeInterpolationType` 2): cadence 0.24 → 0.11, jitter 2.9 → 0.6 px, no warping on people → CR-20261018-puja-night-2-extendscript-notes (follow-up).
- [Phase 0] Reference folder is spelled `Reffernce`; `link_footage.sh` skip pattern `*ref*rence*` doesn't match it, so a re-run of the b-roll link would pull the reference in as footage. Not hit this time (reference added after linking) → linked reference separately with role `references` → CR-20261018-puja-night-2-script-bugs

## Sources
- Footage: `Documents/Video /Puja 2026 Oct 16/Media` → `raw/b-roll/` (62 clips, C078–C139, Blackmagic, recorded 15 Oct 20:16 → 16 Oct 01:48). Proxies not linked.
- Reference: `Documents/Video /Puja 2026 Oct 16/Reffernce/Video-92015.mp4` → `references/` (720×1280, 30 fps, 45.2 s).
- Music request: https://www.youtube.com/watch?v=1_Hfi1EV0-k. Not downloaded by the editor. Director supplied the file (`~/Music/.../Coke Studio Bangla/Shondhatara….mp3`, identical to the copy in Downloads) → symlinked to `music/shondhatara_GUIDE.mp3`.

## Phase 0/1 findings
- **Interview round 1:** type `music-montage`; angle "cinematic montage using the narration of the video" (meaning being clarified); goal **calm / nostalgia**; length **what the song needs**; audience = filmmaker / creator crowd (carried over from my-reel).
- **Reference `Video-92015.mp4`:** "Exclusive First Look of Ek Pukur Bhalobasa, Telipukur Yuba Sangha" — a walkthrough of one pandal (round pond-art panel → dark corridor → mural walls + lit windows → artist painting → idol reveal at 35 s → murals). Warm, dark (18 % crushed), 7 cuts, avg shot 5.64 s, median 3.55 s, first cut 2.67 s. Title text sits on top for the whole reel.
- **Reference audio = Shondhatara 2:06.4 → 2:51.5, one uncut stretch, no voiceover** (chroma correlation 0.97–0.99 in every 4 s window, constant offset 126.39 s; level within ±1.7 dB of the song). Tempo ≈ 96 BPM (librosa, to be confirmed by the beat grid).
- **Footage (62 clips, 2160×3840, 25 fps, 8-bit, dark warm shoot, median exposure 0.264):** several pandals, not the reference's —
  forge / giant-wrench pandal (C085–C089), Rajasthani folk-doll pandal (C090–C095), gold chandelier dome + Durga (C096–C101), Bengali woodcut / almanac print pandal (C102–C115), bamboo-lotus pandal (C116–C124), iron-scaffold net pandal (C125–C129), red pandal (C130–C135), Durga close-ups (C136–C139), sculpted pastel Durga (C081–C084).
  **Upside down (fix with 180° rotation before use):** C112, C116, C117, C118, C120, C121, C122, C124, C127, C130, C131, C133, C134, C135, C136, C137, C138, C139 (to be confirmed per clip from contact sheets). C102 is near-black (skipped from selects).

<!-- The editor appends one section per round below: "## Round N — Proposal", "## Round N — Director notes", "## Round N — Changes made". -->

## Round 1 — Proposal (2026-10-18)
Interview round 2 answers: narration = **walkthrough story** (night journey across pandals); song section = **editor picks from beat map** → director picked **A, 3:31.88–4:31.70** by ear from 3 previews (`music/previews/`); look = **Match reference**; pace = **calm 3–5 s**.

### Hook options
| | Shot (src) | Lands on | Why / risk |
|---|---|---|---|
| **A (recommended)** | C103 20.40 s: woodcut pandal from outside, dancers + crowd, glowing roundel; fade up + push 100→108, title 0.8–4.2 | first cut on bar 3 (4.76) | Walkthrough logic (arrive → enter); motion in frame from frame 1. Calm, not a hard hook |
| B | C132 0.30 s: red arches, people walking in, camera tilts up | bar 3 (4.79) | Strongest *camera* motion in the first second ("step in with us"); loses the outside-arrival beat |
| C | C139 7.20 s: Durga face close, rotated, as a 2.5 s cold open, then cut back to C103 | bar 2 (2.53) | Strongest-looking frame up front for retention; breaks the calm arc and spends the reveal early |

### EDL (reel time; music = song 211.88 s + reel time; 25 fps, cuts quantised to the frame)
| # | clip | in | out | rec in–out | dur | text / action | V1 move | V2/V5 | transition out | SFX |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | C103 | 20.40 | 25.16 | 0.00–4.76 | 4.76 | ARRIVE: woodcut pandal outside, dancers, crowd | push 100→108 (hold) | title 0.8–4.2 | cut (bar 3) | — |
| 2 | C132 | 0.30 | 5.09 | 4.76–9.55 | 4.79 | ENTER: red arches, people walking in | handheld tilt kept | — | cut (bar 5) | — |
| 3 | C081 | 1.30 | 5.48 | 9.55–13.73 | 4.18 | GLIMPSE: Durga through wooden slats | push 100→106 (hold) | — | cut on pickup accent +3.2 | — |
| 4 | C090 | 0.30 | 3.45 | 13.73–16.88 | 3.15 | LIFT: crowd under fairy-light canopy | handheld | (📍 tag?) | cut (bar 8) | — |
| 5 | C093 | 0.30 | 2.83 | 16.88–19.41 | 2.53 | folk mural wall | push 100→104 if static | — | cut (bar 9) | — |
| 6 | C095 | 4.90 | 9.94 | 19.41–24.45 | 5.04 | tilt down to the lamp goddess | handheld tilt | — | Cross Dissolve 12 fr (bar 11) | — |
| 7 | C110 | 0.30 | 4.09 | 24.45–28.24 | 3.79 | woodcut Lakshmi on lotus | handheld pan R | (📍 tag?) | cut on accent +2.6 | — |
| 8 | C105 | 0.05 | 3.23 | 28.24–31.42 | 3.18 | woodcut Durga panel | handheld | — | cut (beat) | — |
| 9 | C100 | 0.02 | 3.18 | 31.42–34.58 | 3.16 | curtain pillar → chandelier | handheld tilt | (📍 tag?) | cut (bar 15) | — |
| 10 | C099 | 4.00 | 9.04 | 34.58–39.62 | 5.04 | dome, Durga far, crowd hands raised | push 100→104 if static | — | cut on the PEAK (bar 17) | (opt. soft swell) |
| 11 | C089 | 4.60 | 9.66 | 39.62–44.68 | 5.06 | REVEAL: optical zoom into Durga over crowd | native zoom only | (📍 tag?) | cut (bar 19) | — |
| 12 | C139 | 7.20 | 12.24 | 44.68–49.72 | 5.04 | Durga face, gold | **rotate 180°**, push 100→106 | — | Cross Dissolve 12 fr (bar 21) | — |
| 13 | C083 | 0.30 | 4.73 | 49.72–54.15 | 4.43 | SETTLE: pastel Durga whole (callback to #3) | handheld pan | — | Cross Dissolve 12 fr (beat) | — |
| 14 | C088 | 5.00 | 10.67 | 54.15–59.82 | 5.67 | last look: Durga far through the giant wrench | pull 106→100 (hold) | end card 56.06–58.6 | Dip to Black 1.2 s | — |

**Runtime 59.82 s.** 14 shots, avg 4.27 s, median 4.3 s, shortest 2.53 s. 3 dissolves + fade in/out.

## Round 1 — Review gate, loop 1 (`analysis/review_v1.md`): FAIL, 4 major / 4 minor
Fixes built on `Reel_puja-night-2_v1b` (duplicate of v1; v1 kept). Shot list `analysis/shots_v1b.json`, EDL `analysis/edl_v1b.json`.
1. **C105 Warp smear 30.28–30.40 (major) — fixed.** The source itself is motion-blurred at 2.08–2.16 s (Laplacian 223 vs ~2,500 around it), so neither Warp nor a slip could save the slot (only ~2 s clean). Replaced by **C107** (woodcut figures, pan along the same wall, sharp 0–3.6 s) at 28.24–31.40, Warp added. v1b scan: no flag; its shake reads 14 px but it's a 270–290 px/s pan (frames sharp, no banner).
2. **C081 focus hunt (major) — fixed.** Sharp only from source 4.40 to 5.64. Now C081 10.08–13.72 = source 2.00–5.64: 2.3 s soft glimpse through the slats, focus snap at reel ≈ 12.4 (beat 12.49), 1.2 s sharp hold, cut on the 13.72 accent. To give it room ARRIVE was re-timed on the grid: C103 0–5.36 (steady source 20.28–25.64 only; 19.16–20.36 is a jerky pan, 30.9 px), C132 5.36–10.08. **This changes the approved EDL timings in ARRIVE (same shots, same order) → tell the director at Checkpoint 2.**
3. **Title over the medallion performer (major) — fixed.** Title now 104 px at y 1486–1559 over the crowd silhouettes (safe zone ✓).
4. **C139 soft head (major) — fixed.** C089's reveal runs to 45.32 (beat; source 3.88–9.60, sharp throughout), C139 starts at its sharp source 7.84 (soft at 7.36–7.60). Dissolve handle kept (out 12.24 of 12.48). v1b scan: no flag.
5. **ARRIVE luma steps (minor) — partly fixed:** C132 +0.65 stop (was +0.45); the rest is intended ("walking in" from the lit exterior to the darker interior) → ask at Checkpoint 2.
6. **9.56 cut off the beat (minor) — fixed by the re-time:** cuts now at 5.36 (beat) and 10.08 (beat 10.10).
7. **Warmer and more saturated than the reference (minor) — partly fixed:** red trio C132/C095/C139 Basic Saturation 88 → 80, C139 temp +6 → +2, C095 +6 → +3; gold shots unchanged. How far toward the reference is the director's call → ask at Checkpoint 2.
8. **Dot spacing (minor) — fixed:** measured 19 px / 18 px either side on the new render.

## Round 1 — Review gate, loop 2 (`analysis/review_v1b.md`): FAIL, 0 blocker / 6 major / 5 minor
Gate limit reached (2 loops). Majors fixed on `Reel_puja-night-2_v1c` (duplicate of v1b) and verified by the editor with the reviewer's own method (per-frame Laplacian at full resolution on the export, `analysis/review_v1c/`), not by a third review.
1. **C081 focus hunt (major) — fixed.** Full-res per-frame: C081 is out of focus (6–9) until source 4.36 and sharp (70–83) from 4.40 to its end, only 1.24 s. Now C081 = 12.48–13.72 (source 4.40–5.64): a sharp glimpse from the 12.49 beat into the accent. The time went to **C130** (inside the red pandal, rotated, source 2.80–5.20, sharp, no dips) at 10.08–12.48. C078/C079/C080/C082/C137 checked as alternatives: all soft.
2. **C139 focus hunt (major) — fixed.** v1b's fix used a half-resolution sharpness check that missed it: at full res C139 is soft (~40) until source 9.52, then 195–320. C139 now 47.20–49.72 from 9.52. C089 is soft before source 2.80, so C089 runs from 2.80 to its last frame, slowed to 93.7 % (optical flow) to land the cut on the 47.20 bar. Per-frame: C139 min/median 0.78, no low frames; C089 two 2-frame source dips (≈43.8, 46.0).
3. **C090 tail smear (major) — fixed.** C090 now 13.72–16.24 (source 0.00–2.52), cut on the strongest hit; no low frames.
4. **C093 camera jerks (major) — fixed by replacement.** C093's two jerks can't both be avoided in its 3.24 s. **C092** (same folk pandal, static doll procession, sharp throughout) at 16.24–19.40; no low frames.
5. **C107 pan blur (major) — fixed.** C107 now ends at 30.76 (source 0.00–2.52), before the pan accelerates; no low frames.
6. **C100 bright, flat opening (major) — fixed.** C100 at 30.76–33.96 with contrast +30, shadows −10, an exposure ramp −0.5 → 0 over its first second. C099 then runs 33.96–39.60. Cut step C107 → C100 measured within the tolerance range after the ramp; the C100 hue (22°) stays as content (gold curtains under sodium light).
7. C099 handheld jerks (minor) — **not fixed:** 6 short frames remain (it is frame-rate-interpreted; Warp needs a nest). Ask the director at Checkpoint 2 whether to nest + Warp or trim it.
8. Title over a crowd head (minor) — **fixed:** title y 1423–1499, checked on a still at 4.0 s with the push at 107 %: clears the medallion performer and the heads.
9. Hue off the gold target on C103/C099/C100 (minor) — **intended / director's call:** warming + green on the primaries moved it < 1° (red decor and sodium light are the content); HSL secondary isn't scriptable here. Ask at Checkpoint 2.
10. C103 → C132 brightness step (minor) — **fixed:** C132 +0.85 stop (0.247 vs C103 0.296).
11. C090 composition (bald head) (minor) — **intended:** "crowd filming" is in the reference; ask at Checkpoint 2.
- Colour QA v1c (`analysis/colour_v1c.json`): montage median 0.263; crushed > 25 % only on C081 (27 %, dark slats framing the glimpse, after +1.0 stop / shadows +25), C089 (31 %, pure-black crowd silhouettes; reviewer accepted, reference 34–39 %) and C088 (fade); C103 clips 3.6 % (bulbs and spotlights). All intended.
- Scan v1c: only the designed fades. Exports: `_mix` peak −1.4 dB; `_IG` −23.9 dB (ambience only).

## Round 1 — Director notes (Checkpoint 1, 2026-10-18)
- "Approved: hook A, the 14-shot EDL, Match Reference look. Title: PUJA NIGHTS · 2026. No location tags."

## Round 1 — Build log
- **Phase 3 rough cut (2026-10-18):** new project `puja-night-2.prproj` (my-reel.prproj stays open alongside; Premiere's active sequence was still my-reel v10, so every call passes the sequence ID). 62 clips → `02_B-Roll`, guide MP3 → `06_Music` (ExtendScript `importFiles`). C099 (25.005 fps) and C103 (25.002) conformed to 25 by interpretation. `Reel_puja-night-2_v1` = 1080×1920 @ 25 fps (from C090, then `setSettings`), V1–V3 / A1–A3.
- EDL placed with `add_to_timeline_batch`, quantised to frames (`analysis/edl_v1.json`); readback: all 14 shots match rec + source in/out to the frame, 0 gaps. Runtime **59.80 s** (1495 frames; music section 211.88–271.68).
- Music landed at 211.84 (1 frame early) → re-placed with `projectItem.setInPoint(211.88, 2)` (audio media type) + `overwriteClip` → readback 211.88–271.68 ✓.
- All V1 clips Motion Scale 50 % (2160×3840 → 1080×1920); C139 Rotation 180°. Verified by stills at 2.0 / 42.0 / 47.0 s (`renders/stills/v1_rough_*.png`).
- A1: natural sound Level −24 dB (0.01122) on all 14; Constant Power 1-frame crossfade at all 13 cuts (QE, start-aligned; readback ✓). Saved.
- **Phase 4 colour (2026-10-18):**
  - Adjustment layer: director's first click landed in **my-reel.prproj** (both projects open); closed my-reel without saving (director's OK; file still 14:46). The next attempt didn't register (menu item disabled until the Project panel has focus; Premiere on another Space while the director's Space is a full-screen app). Editor did it with full-screen control: Dock → Premiere → click Project panel → File › New › Adjustment Layer (1080×1920, 25 fps) → placed on V3 0–59.8 (`isAdjustmentLayer` ✓). V4/V5 added.
  - **A1 primary** (one `color_correct` per clip → temp/tint; rest by script on the same Lumetri, idx 14 temp, 15 tint, 16 Basic sat, 19 exposure, 20 contrast, 21 highlights, 22 shadows, 43 Creative sat, 101/102 HSL-secondary temp/tint zeroed). Final per clip (temp, tint, exp, shadows, sat): C103 −6/−5/0/0/100 · C132 −3/−4/+0.45/0/88 · C081 −4/0/+0.55/+10/100 · C090 +6/−12/0/0/90 · C093 +6/−12/+0.15/0/90 · C095 +6/−12/0/0/88 · C110 −6/+4/0/0/100 · C105 −6/0/−0.25/0/100 · C100 +6/−12/0/0/88 (contrast +20) · C099 +6/−12/0/0/88 · C089 −6/0/+0.2/+15/100 · C139 +6/−12/0/0/88 · C083 −4/0/0/0/100 · C088 0/0/+0.35/+10/100. One Lumetri per clip (readback ✓).
  - First pass cooled the red-gold pandals −8…−10 → midtone hue dropped 5–7° (redder), as in the pilot → temperature moved to neutral/warm, tint toward green.
  - **A3 look** (V3): `applyLumetriPreset("Fuji F125 Kodak 2393 (by Adobe)")` → Look intensity 40, contrast +15, shadows −10, exposure +0.15, Basic sat 95, temp +4, tint −10, vignette −0.8.
  - **A4 texture**: `gemini_film_grain_16mm.mp4` conformed 30→25 fps (4.8 s loop), 13 copies on V4 0–59.8, Overlay (19), 12 %.
  - **Verified by render** (14 mid-shot stills, `renders/stills/a5_*`, sheet `analysis/stills_a5.jpg`): luma median 0.2745 (reference 0.264), range 0.187–0.310; crushed shadows 0.6–20.8 % (all < 25 %; reference 18 %); clipped ≤ 1.6 %. Gold-lit shots C110 34°, C105 31°, C089 32°, C088 37°, C083 43°, C081 42° ✓.
  - **Deliberate flags:** hue < 30° on C132 (red arch lights, 16°), C103 (pink-lit facade, 19°), C095 / C099 / C100 / C139 / C093 / C090 (red cloth and decor dominate the midtones, 20–29°; per-clip warm + green moved them < 1°, so it's content, not cast). C088 luma 0.187 (last shot, fades to black), C081 0.209 (dark slats framing the glimpse).
  - Saved.
- **Phase 5 motion / effects (2026-10-18):**
  - Shake on source ranges (px jit_rms, 1080 space): C105 10.1, C110 8.2 (pan 219 px/s), C100 7.9 (tilt), C132 7.3 (tilt walk), C093 5.8, C090 5.7, C099 5.4, C139 4.4, C081 3.8, C083 3.5, C095 2.9, C089 1.9, C103 1.1, C088 0.4. → **Warp Stabilizer (smoothness 50) on C105, C093, C090** (low pan, hard cuts both sides). Export re-measure: C090 5.7→1.0, C093 5.8→1.2, C105 10.1→5.9. No "Analyzing" banner in the export (checked frames).
  - Motion Scale keys (source time, linear): C103 50→54, C081 50→53, C099 50→52, C139 50→53, C088 53→50 (= 100→108/106/104/106, pull 106→100).
  - Transitions (QE, readback ✓): V1 Dip to Black 0–0.48; Cross Dissolve centred 24.20–24.68, 49.48–49.96, 53.92–54.40; Dip to Black 58.60–59.80. V4 grain Cross Dissolve 0–0.48 and 58.60–59.80.
  - V5: `renders/overlays/title.png` (`PUJA NIGHTS · 2026`, 112 px, lower third y 1379–1462, moved from the top because it collided with the pandal's Bengali banner) 0.80–4.20 with 12-fr dissolves; `endcard.png` (`@satyajitmall`, y 356–433, in the dark trees above Durga) 56.08–59.80, 12-fr in, out with the fade.
- **Phase 6 sound:** A3 music −2.5 dB clip level (master peaks 0 dBFS), Constant Power fade-in 0–0.48 and fade-out 58.6–59.8. A1 natural sound −24 dB. No SFX (calm, per brief).
- **Phase 7 export (2026-10-18):** `exportAsMediaDirect` with Premiere's "Match Source – H.264 High Bitrate" preset. `puja-night-2_v1_mix.mp4`: 1080×1920, 25 fps, 59.80 s, peak −1.4 dB, mean −15.7 dB (audio present, unlike the pilot). `puja-night-2_v1_IG.mp4`: same picture, A3 muted → peak −23.9 dB (ambience only). Music sync vs grid: −20 ms (MP3 decoder padding, < 1 frame).
  - `frame_scan.py`: 5 spans: black at 0.00–0.04 and 59.68–59.80 (fades, intended); blur dips C105 30.28–30.40 (0.31× median), C139 44.84–45.12 (0.49×), C088 59.56–59.72 (inside the fade).
- **Arch:** studio moved to **v0.5.1** during this round (patch: HyperFrames motion graphics, `text_behind.py`, `gen_video.py` AI video). Adopt at the start of round 2. AI video stays off (director profile: own footage only).

## Round 2 — Director notes (Checkpoint 2 on v1c, 2026-10-18)
Director's words (lightly cleaned):
1. "C099 jerks: stabilise it"
2. "Chandelier: push it toward gold"
3. "Red pandal shots: keep them, desaturate a little"
4. "C090: reframe" (the bald head / phone in the lower third)
5. "Shondhatara music is downloaded and kept locally… tell me what the rules in IG are to use it, how to add it; it's in the same folder as the videos (Oct 16)" → `Documents/Video /Puja 2026 Oct 16/Music/Shondhatara … [1_Hfi1EV0-k].mp3`, md5-identical to the guide already in the cut (no change to the music).

## Round 2 — Changes made (v2, `Reel_puja-night-2_v2`, duplicate of v1c)
1. **C099 stabilised:** Warp Stabilizer (smoothness 50) applied directly (25.005 → 25 interpretation didn't need a nest: no "Analyzing" banner in the export). Shake 5.53 → 2.44 px. Its 1–2-frame motion-blur frames (≈35.0, 35.44, 36.8, 36.96, 39.04) are in the source, so Warp can't sharpen them.
2. **Chandelier toward gold:** ASC CDL added to C099 and C100 (Red slope 0.96, Green 1.14, Blue 0.84; first try 0.98/1.08/0.90 reached only 26°/28°). Midtone hue C099 19.9° → 29.5°, C100 22.4° → 32.0° (gold band 30–45°).
3. **Red pandal shots desaturated a little:** Basic Saturation 80 → 72 on C132, C130, C095, C139 (mean saturation −7 %: C132 0.69 → 0.64, C095 0.70 → 0.65, C139 0.67 → 0.62).
4. **C090 reframed:** Motion Scale 50 → 66 % (still downscaling the 4K source), Position y 0.50 → 0.63: the bald head and phone are below frame; canopy, murals and doll procession stay. Sharpness unchanged (no low frames), shake 2.4 px.
5. **IG music:** the file in `Video /Puja 2026 Oct 16/Music/` is md5-identical to the guide in the cut; nothing to change. Rules and steps given to the director in chat (post `_IG`, add Shondhatara from IG's library at 3:31.9).
- Exports: `puja-night-2_v2_mix.mp4` peak −1.4 dB; `_v2_IG.mp4` −23.9 dB (ambience only). Scan: designed fades only.

## Round 2 — Review gate, loop 1 (`analysis/review_v2.md`): FAIL, 0 blocker / 3 major / 3 minor
Director notes 2–4 delivered; note 1 half-delivered. Majors are carried into the v3 proposal (HQ asked for v3 as the next version; build only after the director's yes):
1. **C089 optical-flow ghosting (major) — fix in v3:** C089 back to 100 % (no retime). The reveal becomes **C087** (Durga glowing through the giant wrenches, steady, source 4.24–6.16) 39.60–41.52 → **C089** 41.52–47.20 (source 4.24–9.92, 100 %) → C139 unchanged.
2. **C099 soft pulses (major) — fix in v3:** the source's blur bursts can't be stabilised away (Warp fixed only the geometry: 5.5 → 2.4 px). Chandelier block becomes C100 30.76–33.92 (ends 1 frame before its tail smear; also answers minor 5) → **C101** (static peacock dome + Durga, 2.92 s, slowed to 91 % on a shot with zero motion so no ghosting) 33.92–37.12 → C099 shortened to its calmest 2.48 s (source 6.56–9.04).
3. **Phone screen in C089 (major) — fix in v3:** C089 reframed (scale 68 %, position y 0.667) like C090: phones cropped below frame, Durga and Shiva whole (stills `graphics/proposal/reveal_fix_C087_C089crop.jpg`).
4. C090 last 4 frames (minor) — intended: the clip starts at source 0.00 so it can't slip earlier, and the 16.24 cut sits on the reel's strongest hit.
5. C100 tail (minor) — fixed by ending at 33.92 (above).
6. Title halo (minor) — fixed in v3: animated title with a stronger dark halo.

## Round 3 — Proposal (draft, 2026-10-18; build only after the director's yes)
Requested by HQ for the director: redo as the next version after the v2 gate, with the new studio features (arch 0.5.3, `motion-and-ai.md`). v1–v2 stay as rollbacks.
1. **Animated title + end card (HyperFrames → ProRes 4444 alpha on V5).** Replace the static PNGs with a `/motion-graphics` composition each, in `graphics/title/` and `graphics/endcard/`:
   - one motif: calm focus-pull settle (blur ≈ 12 px → 0, tracking wide → 8 px, opacity 0 → 1 over ≈ 1.0 s, ease-out), clean hold, 0.5 s fade-out;
   - DIN Condensed Bold (local font), cream `#F5E6C8`, dark soft halo (no gold glow), 1080×1920, 25 fps, transparent;
   - title `PUJA NIGHTS · 2026` 3.4 s (0.80–4.20), box y ≈ 1423–1499 (approved placement, re-checked on a C103 still);
   - end card `@satyajitmall` 3.72 s (56.08 → end), y ≈ 356–433 over the dark trees, fade timed to the picture's 58.6–59.8 dip.
   Mock: `graphics/proposal/title_focuspull_mock.png`.
2. **Text behind the subject — stills tested (local `remove-background`, ≈ 0.7 s/frame):**
   | Shot | Matte | Verdict |
   |---|---|---|
   | C095 lamp goddess (src 8.6 / 9.6) | clean, 20–21 % of frame, head and body solid on both frames | ✅ technically best; but the figure is a Rajasthani folk doll, not Durga |
   | C083 pastel Durga (src 0.3–4.7, 12 frames) | clean 0.3–2.0 (face solid 40–57 %); from 2.3 the camera moves in and her face goes semi-transparent (24–34 %) | ⚠️ only ≈ 1.6 s usable (reel ≈ 49.96–51.56, right after the dissolve) |
   | C089 forge Durga (wide) | mush (18 % semi-transparent) | ❌ |
   | C139 gold face close-up | almost nothing (0.4 %) | ❌ (as HQ predicted) |
   Composites: `graphics/proposal/textbehind_C095_MAA.png`, `textbehind_C083_MAA.png`. Recommendation in chat.
3. **AI-generated shots: none.** No gap the footage can't fill: the night journey is fully covered by the director's own clips, the runtime is fixed by the music (59.80 s), so any generated shot would replace real footage. Director profile: "only for shots the director's own footage can't provide". $0 spent, no dry run needed.

## Round 3 — Director decisions (2026-10-18)
- v3 fixes: **"Yes, as proposed"** (reveal C087 → C089 100 % reframed → C139; chandelier C100 → C101 → C099 short).
- Text behind the subject: **"MAA" behind the folk Durga on C095**.
- Title and end card: **animate both** (HyperFrames, stronger dark halo, same placement).
- AI-generated shots: none proposed (no gap), $0.

## Round 3 — Changes made (v3, `Reel_puja-night-2_v3`, duplicate of v2)
1. **Reveal rebuilt (review v2 #1, #3):** C087 39.60–41.52 (source 4.24–6.16, −0.2 stop, highlights −20) → C089 41.52–47.20 at **100 %** (source 4.24–9.92; Scale 68 %, Position y 0.667 → phones cropped; exposure 0, shadows +10) → C139 unchanged. No optical-flow retime anywhere.
2. **Chandelier rebuilt (review v2 #2, #5):** C100 ends 33.92 (before its tail smear) → C101 33.92–37.12 (static dome, 91.25 %, contrast +20, ASC CDL gold, −0.15 stop) → C099 37.12–39.60 (source 6.56–9.04, Warp, ASC CDL gold). Export: C099 2 soft frames (was 9 pulses).
3. **"MAA" behind the folk Durga (C095):** tracked bake (`tools/text_behind_tracked.py`, 420 px, dark halo, word top = subject top − 140 px, fade 0.08–0.58 / 1.80–2.28 s) → `renders/behind/C095_MAA_h264.mp4` on **V2** 21.92–24.20 over the untouched C095 on V1, same Lumetri values. Verified by stills (21.8 / 21.96 / 23.0 / 24.24) and export.
4. **Animated title + end card:** HyperFrames compositions `graphics/title/` and `graphics/endcard/` (from HQ's `durga-title-motion` skeleton; focus-pull settle, dark halo 0.85/0.70 + drop shadow, fade-out) → `renders/title-alpha.mov` (3.4 s) and `renders/endcard-alpha.mov` (3.72 s), ProRes 4444 alpha 25 fps, on V5 at 0.80 and 56.08. Alpha verified in Premiere.
5. AI-generated shots: none ($0).
- QA v3: scan = designed fades only; colour median 0.283; C089 +0.056 / 2.2 % clipped (lit idol filling the crop, intended); `_mix` −1.4 dB, `_IG` −23.9 dB.

## Round 3 — Review gate, loop 1 (`analysis/review_v3.md`): FAIL, 0 blocker / 2 major / 3 minor → v3b
1. **C089 phones still in frame (major) — fixed:** my v3 crop was computed from a frame where the phones sat higher; they reach y ≈ 1570 in the 68 % framing. Recomputed: phones clear below frame needs ≥ 81.8 % → **82 %, y 0.818** (top edge stays on the frame top). Stills at 42.0 / 44.0 / 46.6: no phones.
2. **C099 blur pulses + phones (major) — fixed by replacement:** per-frame source scan at 0.6× local median: C099's longest clean window is 1.56 s (16 bad frames in 6.56 s); **C096** (gold Durga with the lion, same pandal) has 0 bad frames in 3.72 s → C096 37.12–39.60 (source 0–2.48; +6/−12, sat 88, ASC CDL gold, −0.15 stop). Export: 0 low frames.
3. C101 3-frame knock (minor) — **not fixed:** all 2.92 s of C101 are used (no slack to slide); its longest clean window is 0.8 s. Logged.
4. C090 small phones bottom-left (minor) — **fixed:** 70 %, y 0.67 (top cut 58 px, no gap).
5. C089 focus breath 45.96–46.16 (minor) — **intended:** source AF in the hold; the 82 % crop makes it slightly more visible (also a 3-frame dip at 44.2).
- Judgement call for the director: the forge pandal at the peak (C087/C089) and again as the last look (C088), C087 and C088 being similar "Durga through the wrenches" frames.

## Round 3 — Review gate, loop 2 (`analysis/review_v3b.md`): FAIL, 1 blocker / 3 major / 5 minor → v3c
Gate limit reached (2 loops). Fixes built on `Reel_puja-night-2_v3c` and verified by the editor (stills + per-frame luma/sharpness on the export, `analysis/review_v3c/`); no third blind review.
1. **C087 upside down (blocker) — fixed:** Rotation 180°. Confirmed by eye: raw frame had the ceiling chevrons at the bottom and Durga's face inverted; rotated it matches C089. (Editor error: C087 entered in v3 after its sharpness was checked but not its orientation.)
2. **C096 bald head + phones (major) — fixed:** Scale 56 %, y 0.56 (bottom crowd strip out). Stills 38.4 / 39.4 clean.
3. **C100 → C101 brightness jump + pump (major) — fixed:** C101 exposure keyframes −0.8 → −0.15 over its first 1.0 s. Export luma across the cut 0.291 → 0.316 (+0.025), then flat 0.30–0.32 (was 0.29 → 0.40 → 0.31).
4. **C089 focus breath (major) — fixed:** razored V1/A1 at 45.92 and 46.20, middle piece speed 0.01 = hold of the sharp frame 45.92 for 7 frames (scan flags it as "frozen", intended; the zoom has finished there, drift ≤ 2 px/frame).
5. C089 tiny phone at bottom edge (minor) — fixed: 84 %, y 0.84.
6. C090 small phones (minor) — fixed: 75 %, y 0.75.
7. C101 knock (minor) — fixed the same way: hold of frame 35.76 for 4 frames (35.76–35.92).
8. C100 soft (minor) — intended/known: soft fabric shot the director has seen since v1c; no sharper take exists.
9. C088 phones at left + faint phone at C139's start (minor) — not changed: in the cut since v1 and seen by the director; ask at Checkpoint 2.
- v3c QA: scan = designed fades + the designed hold; exports `_mix` −1.4 dB, `_IG` −23.9 dB.

## Round 4 — Director notes (2026-10-19)
- Director asked why the cut doesn't use "the peaks in between 1:45 to 2:40". Editor rendered preview D (1:45.6–2:41.2, 55.6 s) and compared it with A by numbers (A: −5.6…0.0 dB, holds the song's loudest bars; D: −3.9…−1.5 dB, steady build then full). Director listened: **"Switch the music to D (1:45.6–2:41.2) and re-time the cut to it as round 4."**
- v3c itself not yet reviewed by the director (notes to follow).

## Round 4 — Plan (re-time to section D; all 17 shots kept, no new creative changes)
Music: Shondhatara **1:45.60–2:41.20** (105.60–161.20 s, 22 bars, 95.7 BPM). Grid (reel time): accents 0.00 (+2.9), **3.79 (+3.7)**, 8.85, 10.11 (+3.3), 17.70, 18.95; **lift at 20.23** (bar 51, −3.3 → −2.1 dB); full to the end; loudest bar 42.96 (−1.5 dB); section ends on bar 161.19. Runtime **55.60 s**. IG start point becomes **1:45.6**.
| # | clip | src | rec | dur |
|---|---|---|---|---|
| 1 | C103 | 20.28–24.08 | 0.00–3.80 | 3.80 |
| 2 | C132 | 0.28–4.08 | 3.80–7.60 | 3.80 |
| 3 | C130 | 2.80–5.32 | 7.60–10.12 | 2.52 |
| 4 | C081 | 4.40–5.64 | 10.12–11.36 | 1.24 |
| 5 | C090 | 0.00–2.52 | 11.36–13.88 | 2.52 |
| 6 | C092 | 0.12–3.28 | 13.88–17.04 | 3.16 |
| 7 | C095 | 4.88–9.96 | 17.04–22.12 | 5.08 |
| 8 | C110 | 0.28–3.44 | 22.12–25.28 | 3.16 |
| 9 | C107 | 0.00–2.52 | 25.28–27.80 | 2.52 |
| 10 | C100 | 0.00–3.16 | 27.80–30.96 | 3.16 |
| 11 | C101 | 0.00–2.92 | 30.96–34.12 | 3.16 |
| 12 | C096 | 0.00–3.16 | 34.12–37.28 | 3.16 |
| 13 | C087 | 4.24–7.40 | 37.28–40.44 | 3.16 |
| 14 | C089 | 4.24–9.28 | 40.44–45.48 | 5.04 |
| 15 | C139 | 9.52–12.04 | 45.48–48.00 | 2.52 |
| 16 | C083 | 0.28–2.80 | 48.00–50.52 | 2.52 |
| 17 | C088 | 5.00–10.08 | 50.52–55.60 | 5.08 |
- Title (HyperFrames) 0.20–3.60; "MAA" V2 overlay 19.56–21.84 (fades in on the lift); dissolves at 22.12, 48.00, 50.52; end card 51.88–55.60; fade 54.40–55.60. C101 at 92.4 % (2.92 s source over 3.16 s) with its exposure ramp; frame holds over the C101 knock and C089 focus breath re-placed at their new times.

## Round 4 — Changes made (v4, `Reel_puja-night-2_v4`, duplicate of v3c)
- V1/A1/V2/V5/A3 cleared and rebuilt on the D grid from `analysis/edl_v4.json`; V3 adjustment layer and V4 grain trimmed to 55.60. All per-clip values copied from the v3c clip of the same name by script (Lumetri temp/tint/sat/exposure/contrast/highlights/shadows, ASC CDL, scale/position/rotation; pushes and exposure ramps re-keyed at the new in-points).
- Music: A3 = Shondhatara 105.60–161.20 (`setInPoint(…, 2)`), −2.5 dB, 6-frame fade-in, 1.2 s fade-out. Sync vs the song −20 ms (MP3 decoder padding).
- C101 92.4 % (2.92 s source over 3.16 s); holds re-placed: C101 32.76–32.92 (knock), C089 44.84–45.12 (focus breath).
- "MAA" V2 19.56–21.84 (word fades in 19.64–20.14, onto the lift at 20.23). Title 0.20–3.60; end card 51.88–55.60.
- Exports: `_mix` 55.60 s, −1.4 dB; `_IG` −24.0 dB. Scan: designed fades + the designed C089 hold.

## Round 4 — Review gate, loop 1 (`analysis/review_v4.md`): FAIL, 0 blocker / 2 major / 5 minor → v4b
Re-time verified by the reviewer (all 16 cuts within 1 frame of a beat; "MAA" on the lift; reveal on the loudest bars; orientation, overlays, ending OK).
1. **C088 phone screens (major) — fixed:** soft dark mask (two feathered spots, 92 % / 85 %) on V2 50.52–55.60 with a 12-frame fade-in; cropping would cut Durga/Ganesh. Stills 51.5 / 54.0 clean.
2. **C096 heads rising at the tail (major) — fixed:** 62 % / y 0.60 (top cut 39 px). Stills 36.9 / 37.2 clean.
3. C089 hold resume jump (minor) — fixed: hold runs 44.84 → 45.48 (cut); frame diffs ≈ 0 to the cut.
4. C101 knock (minor) — fixed: hold runs 32.76 → 34.12 (cut).
5. C130 phone raised (minor) — fixed: `slip_edit` −0.4 s → source 2.40–4.92.
6. C103 tiny phones in the IG band (minor) — intended: tiny, inside the bottom UI band.
7. C139 silhouettes (minor) — intended: reference tolerates silhouettes.

## Round 4 — Review gate, loop 2 (`analysis/review_v4b.md`): FAIL, 0 blocker / 2 major / 5 minor → v4c
Gate limit reached (2 loops). The fixes below were verified by the editor (stills, per-frame metrics, frame scan); no third review. Verified by the reviewer: both holds read as still moments, all 17 cuts within 30 ms of a beat, "MAA" on the lift.
1. **C088 phone mask ramps in over ~1.5 s (major) — fixed:** tracked mask (`tools/phone_mask_tracked.py` → `renders/overlays/c088_phone_mask_tracked.mov`, V2 50.28–55.60, no transition; alpha ramps with the C083 → C088 dissolve). The phones are tracked through the camera pan and the hand moves. Phone A (in front of the crowd) gets its tracked box; B and C (next to Ganesh and the stage) get the convex hull of the glass, so no dark patch falls on the backdrop. Full opacity: Premiere rendered 0.97 as ≈ 0.87. Result: screen luma under the mask p95 100–168 (v4b) → 6–7 (v4c) from 50.52; the screens read as phones held up with the screen off. A fourth "phone" (D, a highlight at Ganesh's foot) was left alone.
2. **C130 phone raise from 9.5 s (major) — fixed:** the raise starts at source 4.30. C130 now runs **8.84–10.12** (on the 8.85 accent) at source **3.00–4.28**, ending 1 frame before the raise. C132 runs 3.80–8.84 at source 0.12–5.16 (the clip's last frame; per-frame sharpness ≥ 0.8 of its median, tail ≈ 1.0). A1 follows the picture, with a Constant Power crossfade at 8.84. Pacing: 3.80 / 5.04 / 1.28 / 1.24 s into the 10.11 downbeat (two quick glimpses on two accents).
3. C139 heads + a phone in the bottom band (minor) — not changed: the phone is a dark handset with a few UI dots at y ≈ 1780–1870, inside the 320 px IG bottom band (under the caption). Removing the heads needs ≥ 112 % with the frame shifted, which crops Durga's crown. → ask the director at Checkpoint 2.
4. C096 tail smear 36.9–37.28 (minor) — not changed: the source starts at 0, so there's no earlier frame to slip into, and the pan's motion blur carries into the reveal cut.
5. C100 soft (minor) — not changed (known since v1c; tilt motion blur).
6. **C101 repeated frames (minor) — fixed:** Frame Blending on the 92.4 % piece (QE `setTimeInterpolationType(1)`; no optical flow, which ghosted on C089). Smallest frame-to-frame change is now 2.5 (was ≈ 0 at 31.00 / 32.04 / 32.56).
7. **Music fade back-loaded (minor) — fixed:** A3 end transition is now an **Exponential Fade 54.56–55.60** with the picture. RMS per 0.2 s: v4b −17 −17 −22 −28 −36 dB, v4c −20 −26 −33 −44 −53 dB.
- Grain over the holds: the grain source changes every frame (mean frame diff 1.95), but at 12 % Overlay it's below what H.264 keeps on a held frame, so held frames encode identical. Left as is.

## Round 4 — Changes made (v4c, `Reel_puja-night-2_v4c`, duplicate of v4b)
- Scripts: `analysis/_es_v4c_open.jsx` (main project back from the auto-save copy), `_es_v4c_c130.jsx` + `_es_v4c_c130b.jsx` (C130 head trim + explicit in/out), `_es_v4c_c132.jsx`, `_es_v4c_fix2.jsx` (A1 crossfade, A3 fade, mask swap), `_es_v4c_c101.jsx`, `_es_v4c_refresh.jsx` (refresh mask media + stills), `_es_export_seq.jsx` (export by sequence ID).
- Exports: `_mix` 55.60 s, −1.4 dB peak / −16.3 dB mean; `_IG` −24.0 dB peak (ambience only), picture frame-aligned with `_mix`. Frame scan vs v4b: no new flags except C132's longer span (0.47 of median, designed walk) and one C100 blip (known soft).

## Round 4 — Checkpoint 2 (v4c, 2026-10-19)
- Director watched v4c on the phone with sound; notes not given yet ("Can I rewatch it").
- "What would make it more cinematic?" → **Slower, longer holds.** Next round: fewer, longer shots in the middle (fewer quick glimpses, more time on the deities), cuts on accents / every 4th beat, music section and 55.60 s unchanged. Plan goes to the director with the rewatch notes before any build.

## Round 5 — Director notes (after rewatching v4c, 2026-10-19)
Verbatim: "This video are coming out as slide slow instaed of cinematic cuts and music is darmatic but the shots and teh cuts do not make it dramtic as , also the natural depth in the video is missing post productio work is need. One intro screen willl will suggest would be TEH word durga teh recording fill the letter or the background of the liek teh marvel intro"
1. Reads as a slideshow, not cinematic cuts: the music is dramatic, the shots and cuts aren't.
2. Natural depth is missing: needs post-production work.
3. Intro: the word **DURGA** with the footage filling the letters (or the background), like the Marvel intro.
(Earlier answer to "more cinematic?" was "slower, longer holds"; the notes above ask for drama → read together as contrast: long holds only on hero moments, fast beat-cut bursts on the hits.)

## Round 5 — Proposal (draft, 2026-10-19; build only after the director's yes)
Music unchanged: D 1:45.60–2:41.20, **55.60 s**, IG start 1:45.6. Hit map (beat-level onset + low end): 2.54 → 3.14 → **3.79 (biggest)**; 8.85 / 9.45 / 10.11; 15.77, 17.70, 18.95; lift **20.23**; 25.27, 27.80; **40.43**; loudest bar 42.96. After 22.76 the song is full and dense.
Mocks: `renders/previews/durga_intro_mock.mp4` (with the song), `renders/previews/depth_mock.jpg`.

**Note 1, slideshow → dramatic cuts.** v4c = 17 shots, 1.24–5.08 s, avg 3.3 s, almost all hard cuts on the bar → reads as slides. v5:
- **Cut density follows the hits:** 0.6 s flashes on hits, 1.25 s two-beat cuts through the build and the full section, holds of 2.5–5 s only on 7 hero moments (the "slower, longer holds" answer lives there). **30 shots + the intro**, avg 1.7 s.
- **Cut on motion:** handheld moves carry across cuts in the same direction; C132 at 150 % so its whole tilt (arches → crowd) lands in 2.5 s; speed-up ramps into the lift (C126) and into the reveal (C087 whip), via After Effects time remap.
- **Impact on the hits:** riser into 3.79 + white flash + boom; whoosh-zoom into the lift 20.23; gold flash + sub hit on the 40.43 reveal; snap zooms on the beats over the static giant red feet (C135). SFX on A2 at −14…−18 dB (they stay in `_IG`).
- New material from a full-shoot sharpness scan (`tools/shot_pool.py`, all 62 clips): forge machinery C085/C086, iron-scaffold pandal C125/C126/C128/C129, red giant-feet pandal C133/C134/C135, woodcut print C106, folk C091/C093/C094, dome C098/C099, and **C112** (Durga in a blue-gold arch shrine; the camera pushes in to her face; sharp 3.5–12.7 s).

**Note 2, depth.** Mocked on three frames:
- **Subject matte** (standing figures, e.g. C095): background slightly defocused, −0.35 stop, cooler; subject +0.12 stop with local contrast.
- **Light pool** on dense idol tableaux where the matte fails (C096, C139, C112, C101, C089, C135): +0.35 stop on the face, −0.45 stop falloff to the edges, local contrast.
- Soft bloom on lamps. Baked from source and placed as V2 overlays over the original shots (the MAA method), same Lumetri.
- Global look: contrast +15 → +25, vignette −0.8 → −1.2, deeper blacks; grain unchanged.

**Note 3, intro.** `DURGA` in tall heavy condensed letters (Impact, closest to the profile's Anton; 980 × 640 px). Footage flips inside the letters on the beats (0 / 0.63 / 1.28 / 1.89 / 2.54, then every half beat). The camera pulls back out of the letters (0–2.54). `PUJA NIGHTS · 2026` fades in under it at 2.54. On 3.79 (the song's biggest hit) it smash-cuts into the reel with a white flash. Replaces the C103 hook and the old title card.

**EDL v5 (reel time; source in-points refined ±0.5 s at build for motion and phones)**
| # | rec | dur | clip | src in | what / move | out |
|---|---|---|---|---|---|---|
| 0 | 0.00–3.79 | 3.79 | DURGA card | C112, C106, C101, C091, C085, C134, C096, C139 inside the letters | pull back, flips accelerate, title under at 2.54 | flash + boom |
| 1 | 3.79–6.32 | 2.53 | C132 | 0.12 @150 % | red arches tilt → crowd walking in | cut |
| 2 | 6.32–7.60 | 1.28 | C094 | 1.0 | folk interior wide, crowd moving | cut |
| 3 | 7.60–8.85 | 1.25 | C103 | 4.0 | woodcut facade, push 100→106 | cut on hit |
| 4 | 8.85–9.45 | 0.60 | C085 | 0.5 | forge machinery flash | hit |
| 5 | 9.45–10.11 | 0.66 | C134 | 0.8 | giant red feet flash | hit |
| 6 | 10.11–12.64 | 2.53 | C093 | 0.3 | facade of lights, tilt (downbeat) | cut |
| 7 | 12.64–13.91 | 1.27 | C091 | 2.4 | folk dolls with lamps | cut |
| 8 | 13.91–15.17 | 1.26 | C092 | 0.12 | folk | cut |
| 9 | 15.17–15.77 | 0.60 | C106 | 0.6 | woodcut print, snap push | hit |
| 10 | 15.77–17.05 | 1.28 | C090 | 0.0 | folk interior | cut |
| 11 | 17.05–17.70 | 0.65 | C086 | 0.3 | red forge spikes | hit |
| 12 | 17.70–18.95 | 1.25 | C125 | 0.5 | iron scaffold, looking up | hit |
| 13 | 18.95–20.23 | 1.28 | C126 | 4.8 | dark scaffold, ramp 100→250 % into the lift | whoosh-zoom |
| 14 | 20.23–22.76 | 2.53 | C095 | 4.88 | folk Durga hero hold, **MAA** behind her, depth matte | cut |
| 15 | 22.76–24.01 | 1.25 | C110 | 0.8 | woodcut pan | cut |
| 16 | 24.01–25.27 | 1.26 | C107 | 0.0 | woodcut pan | cut on hit |
| 17 | 25.27–27.80 | 2.53 | C101 | 0.0 | chandelier dome, slow push, light pool | cut on hit |
| 18 | 27.80–29.05 | 1.25 | C096 | 0.0 | gold Durga + lion pan, light pool | cut |
| 19 | 29.05–30.33 | 1.28 | C099 | 1.0 | dome + Durga + crowd | cut |
| 20 | 30.33–32.86 | 2.53 | C098 | 7.6 | dome wide | cut |
| 21 | 32.86–35.37 | 2.51 | C135 | 2.0 | giant red feet, snap zooms on 33.46 / 34.11 / 34.74 | cut |
| 22 | 35.37–35.97 | 0.60 | C133 | 4.5 | red crowd | hit |
| 23 | 35.97–36.65 | 0.68 | C134 | 2.5 | red feet close | hit |
| 24 | 36.65–37.90 | 1.25 | C128 | 2.6 | Durga behind the scaffold mesh, crowd | cut |
| 25 | 37.90–39.15 | 1.25 | C129 | 0.5 | scaffold with plants, looking up | cut |
| 26 | 39.15–40.43 | 1.28 | C087 | 0.0 | forge approach, whip → speed-up into the reveal | gold flash |
| 27 | 40.43–45.49 | 5.06 | C089 | 4.24 | forge Durga zoom through the loudest bar, hold to the cut, light pool | cut |
| 28 | 45.49–48.02 | 2.53 | C139 | 9.6 | Durga face, push, light pool | cut |
| 29 | 48.02–50.53 | 2.51 | C088 | 5.0 | the crowd watching (tracked phone mask re-rendered) | cut |
| 30 | 50.53–55.60 | 5.07 | C112 | 7.6 | the camera pushes into Durga's face (ending), light pool, end card, fade | fade |

**What I can't do:** true slow motion (all footage is 25 fps; only speed-ups and holds); depth-of-field blur on the dense idol tableaux (the subject matte fails there, so depth comes from light); Marvel's 3D page-flip of the panels (flips are hard cuts inside the letters).
**Changes to approved items:** C103 hook and the `PUJA NIGHTS · 2026` title card → replaced by the DURGA intro (title kept under the word); last shot C088 → C112 Durga close-up; C100 (soft), C130, C081, C083 dropped.

## Round 5 — Director decisions (2026-10-19)
- Cut plan: **"Yes, build it"** (30 shots + DURGA intro, holds on the hero moments).
- Intro: **"Give me the first 4 second short in both formats, let me choose"** → render "inside the letters" and "behind the letters" previews.
- Depth: **"Cinematic warm grade is what I'm looking for"** → depth comes from the grade (warm highlights, rich contrast, deep shadows, vignette); per-shot matte / light-pool passes are not built unless asked.
- Ending: **"Yes, end on Durga"** (C112 push-in).
- Intro format (after both 4.6 s previews, `renders/previews/durga_intro_fill.mp4` / `_behind.mp4`): **"Inside the letters"** (`tools/durga_intro.py --mode fill`).

## Round 5 — Build log (v5, `Reel_puja-night-2_v5` 851c75ac-a594-4ae2-9911-237845a2022a, duplicate of v4c)
- **Cut:** 30 shots from `analysis/edl_v5.json` placed by script (`_es_v5_place.jsx`), frame-snapped ends closed (`_es_v5_close.jsx`); cuts at 3.80 / 6.32 / 7.60 / 8.84 / 9.44 / 10.12 / 12.64 / 13.92 / 15.16 / 15.76 / 17.04 / 17.72 / 18.96 / 20.24 / 22.76 / 24.00 / 25.28 / 27.80 / 29.04 / 30.32 / 32.88 / 35.36 / 35.96 / 36.64 / 37.92 / 39.16 / 40.44 / 45.48 / 48.04 / 50.52, all within 20 ms of a beat; 0 gaps; 55.60 s.
- **Per clip** (`_es_v5_look.jsx`): one Lumetri each added through QE `addVideoEffect` (no `color_correct`); reused clips copy their v4c values by clip code; new clips by group (forge −6/0 + shadows; folk +6/−12 sat 90; red −6/0 sat 72 +0.2; scaffold 0/0 +0.3…+0.6 shadows +10; dome +6/−12 sat 88 + gold CDL; woodcut −6/+4; C112 0/−4). Rotation 180 on C112/C133/C134/C135/C139/C087. Keys: pushes C103/C101/C139/C088/C112, snap on C106, three snap zooms on C135 (33.46/34.11/34.74), zoom punch on C126 into the lift.
- **Speed:** C132 150 %, C087 200 % (`speed_change`); C089 frame hold 44.84–45.48 (razor + 0.01).
- **MAA** on V2 20.24–22.76 with C095's Lumetri. **A1** −24 dB, 1-frame Constant Power at 30 cuts. **SFX:** A2 riser 2.80 (hit 3.81), snap swishes 15.08 / 33.40 / 34.08 / 34.68, whoosh 20.00, riser 39.44 (hit 40.45); A4 booms 3.80 / 40.44 (−15…−18 dB). **V1:** Dip to White 3.80–3.92 and 40.36–40.52, Dip to Black 54.40–55.60.
- **Grade (cinematic warm, V3):** look Lumetri temp +4 → +14, tint −10 → −20, sat 95 → 100, exposure +0.15 → +0.18, contrast +15 → +22, highlights 0 → −12, shadows −10 → −12, look intensity 40 → 50, vignette −0.8 → −1.4; **ASC CDL on the adjustment layer** R 1.02 / G 1.00 / B 0.84 (R 1.06 clipped C112's reds to 11 %). Stills (`renders/previews/grade_v4c_vs_v5.jpg`): hue +3…+8° warmer, clipping back to v4c levels.
- **Intro:** `tools/durga_intro.py --mode fill` sampled from the graded body export (flips: C101, C093, C096, C135, C085, C091, C089, C139) → `renders/overlays/durga_intro_v5.mp4` (95 frames) on V5 0–3.80.
- Exports (first pass): `puja-night-2_v5_mix.mp4` (55.60 s, −1.3 dB peak), `_v5_IG.mp4` (SFX + ambience, −11.4 dB peak).
- **Own QA, first pass:** raised lit phones in C098 / C099 crowds; C088's bottom-left phones back (v4c mask not carried over) → reframe C098 76 % / y 0.76, C099 83 % / y 0.83; C088 mask re-rendered for v5 (`renders/overlays/c088_phone_mask_v5.mov`, tool now takes `--t0/--cut/--end/--src-at-cut/--scale/--dissolve/-o`). Applying them (`_es_v5_fix1.jsx`) stalled Premiere's script engine (no reply, nothing saved) → waiting on the director.
- The stall was Premiere's **Import Files** progress dialog stuck on `c088_phone_mask_v5.mov` (director clicked Cancel; the reframes had already run). Retried the import alone (`_es_v5_import.jsx`): fine in seconds. Mask placed V2 48.04–50.52, in-point 0.24 (`_es_v5_mask.jsx`). C098 pushed further to 82 % / y 0.82 (76 % still showed a lit phone). Stills: C099 clean, C088 screens dark, C098 only head tops in the IG bottom band.
- Exports (second pass, 15:51): `_v5_mix` 55.60 s, −1.3 dB peak / −16.3 dB mean; `_v5_IG` −11.4 dB peak (SFX + ambience). Frame scan: designed flashes, hold and fade + per-shot blur dips on the fast / handheld flashes. Watch sheets `analysis/watch_v5/` (4 fps). Brief §0 written for the gate. Gate loop 1 running (reel-reviewer, fable).

## Round 5 — Review gate, loop 1 (`analysis/review_v5.md`): FAIL, 0 blocker / 6 major / 4 minor → v5b (`Reel_puja-night-2_v5b` 33968a2e-f2c3-4275-855e-d38e43133b01)
1. **C098 / C099 hot yellow block (major) — fixed by removal.** C099 exposure −0.4/−0.7 brought it to luma 0.32, but its per-frame sharpness stayed 120–360 against 600–1000 on the neighbours, so both dome shots are out: C096 27.80–30.32 (clean, 2.52 s), C135 30.32–35.36.
2. **C098 whip + jump cut + phone (major) — fixed** (C098 removed). C097 (gold detail, upside-down source, rotated) was tried as a replacement and rejected: heavy horizontal motion smear despite a high Laplacian score (streak texture fools the metric).
3. **C099 soft hold (major) — fixed** (removed; see 1).
4. **C103 phones (major) — fixed:** push 59→61 (118→122 %) top-anchored (pos y 0.59); the crowd band with the phones now sits below y 1600 (IG bottom band).
5. **C128 phones (major) — fixed:** 70 % (140 %) top-anchored; phones at y ≈ 1790–1860 (bottom band).
6. **C134 used twice with faces (major) — fixed:** first flash 75 % (150 %) top-anchored (feet only); second flash from C134's 12.0 s close-up of the feet (different moment, almost no people).
7. C091 SECURITY cap (minor) — fixed: source 2.0 and 108 % top-anchored (cap out of frame).
8. C133 bystander facing the lens (minor) — fixed: source 5.44 (backs only).
9. Intro subtitle small + dark fill (minor) — fixed: 86 px; C085 fill → C106 woodcut (bright).
10. C094 police-volunteer jacket (minor) — fixed: 108 % anchored left.
- Could-not-judge items: end-card font checked on the HyperFrames render: it **is** DIN Condensed Bold (cream); the export just softens it. IG balance: swishes and whoosh raised −18/−17 → −13 dB. C126 orientation confirmed upright.
- Also: C135's snaps now land on 31.58 / 32.86 / 33.46 / 34.11 / 34.74 with a swish on each.
- v5b exports 16:15: `_v5b_mix` 55.60 s −1.3 dB peak; `_v5b_IG` −11.4 dB. Frame scan: designed flash / hold / fade + short red-flash dips (C134 at 108–199 = smooth red surface, same as C135's 150–180, not blur). Watch sheets `analysis/watch_v5b/`. Gate loop 2 next.

## Round 5 — Review gate, loop 2 (`analysis/review_v5b.md`): FAIL, 2 blocker / 4 major / 7 minor → v5c (`Reel_puja-night-2_v5c` 953cc454-5735-4847-90cb-1c31fd4717a3)
Gate limit reached (2 loops). Fixes verified by the editor on the v5c export (numbers below); no third blind review.
1. **C085 upside-down (blocker) — fixed:** rotated 180° (stall signage now on the ground); source moved to 1.7–2.3 (tighter on the nuts; the stall banner sits mostly in the IG bottom band). My miss: the EDL had `rot:180` on C087 but not on its forge siblings.
2. **C086 upside-down (blocker) — fixed:** rotated 180° (wrench garland now at the top, as in the corrected C087).
3. **C135 crowd with phones + a face in the lens (major) — fixed:** top-anchored 128 % (pos y 0.64), snaps 128 → 136 → 144 → 152 → 160 → 168 %; the crowd sits below y 1600 for the whole hold (stills 33.4 / 34.6 / 35.2).
4. **C134 lit phone (major) + feet triple repeat (minor 12) — fixed:** the 35.96 flash is now a second C086 moment (red spikes, source 1.0–1.68, rotated), so the hits read feet → crowd → spikes → scaffold.
5. **C092 man looking into the lens (major) — fixed:** 114 % shifted right (pos x 0.431), the left 150 px are out.
6. **C112 red clipping on Durga (major) — fixed:** highlights −35, exposure −0.25, sat 85. R ≥ 250 at 54.0: whole frame 7.1 % → 0.6 %, warm skin 16.5 % → 1.0 %.
7. C132 dark phone in the last frames (minor) — not changed: a dark (unlit) phone for ≈8 frames at the end of the tilt; the source can't start earlier (0.12 → 0 only shifts 0.08 s).
8. C094 two small phones (minor) — fixed: 116 % anchored top-left (phones into the bottom band).
9. C091 SECURITY label at the band edge (minor) — fixed: 114 % top-anchored (label inside the band).
10. C101 focus breath on the cut (minor) — fixed: source starts 4 frames later (sharpness at the cut 520 / 396 / 261 → 717 / 859 / 611).
11. C087 guard facing the camera for 0.4 s at 200 % (minor) — not changed (moves into the band with the push).
13. DURGA "A" in IG's right 120 px (minor) — fixed: word 840 × 600 px (x 122–968; 8 px over only during the final push).
- v5c exports: `_v5c_mix` 55.60 s, −1.3 dB peak; `_v5c_IG` −11.4 dB (SFX + ambience). Frame scan: designed flashes / hold / fade + short motion dips on the hit flashes only.

## Round 6 — Director notes (after watching v5c, 2026-10-19)
Verbatim: "Some pan out and pan in done by the camera are jumy, the shots do not have cinematic statbility or depth, also review few more footages check what you have discarded what can be used. And after effect / motion graphic that you used between 0:19 to 0:21 are botched, maybe we do not need it. and think about better cinmetic transitions that match teh beat."
1. Camera push-ins / pull-outs are jumpy; shots lack cinematic stability and depth.
2. Review the discarded footage: what can be used.
3. The effect / motion graphic at 0:19–0:21 is botched; probably not needed.
4. Better cinematic transitions that match the beat.

## Round 6 — Proposal (draft, 2026-10-19; build only after the director's yes)
Mocks: `renders/previews/transitions_mock.mp4` (with the song), `renders/previews/discarded_review.jpg`, `renders/previews/depth_mock.jpg`.

**Note 1, jumpy camera moves / no stability or depth.** Shake on the v5c export (`analysis/shake_v5c.json`, jitter RMS px): C126 122 (the zoom punch), C086 second moment 91 (a 925 px/s whip in the footage), C086 31, C134 27, C110 19, C085 19, C091 17, C087 17, C129 15, C132 13; the rest 3–9. **No shot in v5 is stabilised** (studio default: Warp Stabilizer on handheld moving shots), my miss.
- Warp Stabilizer (Smooth Motion, 15–30 %) on every handheld moving shot; the speed-changed C132 and C087 nested first. Re-measure: target jitter < 5 px; any shot that stays jumpy is trimmed to its steadiest part or replaced.
- Camera push-ins / pull-outs (C089 zoom, C112 push): after Warp, check for zoom steps; if any remain, use the steadiest stretch with a smooth digital push instead.
- Depth: grade only so far (the director chose it in round 5). Offer again: per-shot depth pass on the hero shots (subject matte on standing figures, light pool on the tableaux); see `depth_mock.jpg`.

**Note 2, discarded footage.** Every unused clip re-scanned (relaxed criteria) and viewed upright (`discarded_review.jpg`). Usable:
- C083 pastel sculpted Durga (sharp; was in v1–v4);
- C116 + C124 bamboo-lotus pandal (a pandal the reel never shows: glowing lotus lamps, crowd interior);
- C108 / C109 woodcut arches with lamps and Bengali text;
- C127 scaffold Durga (darker).

Not usable (out of focus / near-black): C078–C082, C113–C123, C131, C136–C138; C097 (motion smear), C098 / C099 (soft, phones).
Placement:
- 9.44 flash C134 → C116 lotus lamps;
- 22.76 C110 → C109 woodcut arches;
- 35.96 flash (C086 whip footage) → C124 lotus interior;
- 48.04–50.52 C088 crowd → **C083 pastel Durga**, so the ending runs Durga face (C139) → pastel Durga (C083) → shrine push-in (C112).

**Note 3, the 0:19–0:21 effect.** That's the "MAA" text over the folk Durga plus the zoom punch out of C126. Both removed; the lift gets a proper zoom-through instead.

**Note 4, cinematic transitions on the beat** (`transitions_mock.mp4`):
- **zoom-through** on 3.80 (intro → reel) and on the 20.24 lift;
- **whip pans** where two pans meet on a beat (22.76, 24.00 and one more in the full section);
- **gold light leak** in place of both white flashes (3.80, 40.44);
- **soft film dissolve** into the ending (50.52);
- hard cuts everywhere else, so the transitions stay special.

Built from the graded render as short overlays on V5 at each cut (the intro method), so they match the mock exactly.
Runtime 55.60 s, music unchanged.

## Round 6 — Director decisions (2026-10-19)
- Stability: **"Yes"**: Warp Stabilizer on all handheld moving shots, swap / trim what stays jumpy, smooth the camera push-ins.
- Discarded footage: **"Yes, all"**: C116 lotus lamps (9.44), C109 woodcut arches (22.76), C124 lotus interior (35.96), C083 pastel Durga (48.04; ending = C139 → C083 → C112).
- Transitions: **"depends on the narration of the song and its meaning, or the beat of the music"** → editor places them by song structure: zoom-through at the section changes (3.80 intro → reel, 20.24 lift), whip pans where pans meet on beats in the full section, gold light leak on the climax reveal (40.44), soft dissolve into the outro / ending (50.52); hard cuts elsewhere.
- Depth / tone: **"Wherever necessary; all frames, all shots need to have cinematic tone and vibe to match the entire video"** → per-shot tone matching to one target (luma, warmth, saturation) on every shot + light-pool / depth where a shot reads flat.

## Round 6 — Build log (v6b, `Reel_puja-night-2_v6b` 4b732ab8-3ad5-48be-b401-0e80f5bfc50a; v6 95407ed0-… abandoned)
- Structure (`_es_v6b_struct.jsx`): MAA and the C088 mask off V2; C126 zoom punch flattened; V1 white flashes removed; C134@9.44 → C116 (0.48–1.16, rot 180), C110@22.76 → C109 (0.24–1.48), C086b@35.96 → C124 (0.8–1.48, rot 180), C088@48.04 → C083 (0.4–2.88, push 50→53).
- Stabilisation: C132 and C087 nested (`_es_v6b_nest.jsx`); Warp via MCP `stabilize_clip` on 25 clips; 18 needed the Analyze button (editor pressed it with screen control after the director's clicks didn't register). Status codes on Warp property 31: 201 = not analysed, 408 / 708 = analysed.
- Problems found and fixed on the way:
  - QE-added Warp never analyses (v6 abandoned);
  - Warp smoothness 100 by script → C091 "extreme cropping" error frame (setting it back doesn't re-stabilise) → C091 re-placed on its steady stretch (4.2–5.48) without Warp at 124 % (SECURITY cap out);
  - C096 judder introduced by Warp (source jitter 0.2) → re-placed without Warp;
  - C087 source jolt → steadier 1.4–2.68 at 100 %, no nest;
  - the four swapped-in clips had been placed at Premiere's default scale 100 % (2× zoom on 4K; my miss) → 50 %;
  - a Film Dissolve over Warp clips showed Warp's banner (no analysed handles) → baked warm dip instead.
- Tone match (`_es_v6b_tone.jsx`, from `colour_v6b.json`): exposure −0.9…+1.3 stop on outliers, forge / pastel warmed; result luma 0.22–0.26 on 25 / 29 shots.
- Transitions (`tools/beat_transitions.py` from the graded body with V6 hidden; V6 track): zoom 3.80 / 20.24, whip 22.76 / 24.00 / 27.80, leak 40.44, dip 50.52; whooshes A2 22.52 / 23.76 / 27.56 (−15 dB).
- Exports 18:08: `_v6b_mix` 55.60 s −1.3 dB; `_v6b_IG` −11.4 dB. QA: no Warp banners, black only in the end fade; velocity jitter < 0.6 px/frame on 26 / 28 shots (C091 1.18, C087 1.07).

## Round 6 — Review gate, loop 1 (`analysis/review_v6b.md`): FAIL, 0 blocker / 6 major / 6 minor → v6c (`Reel_puja-night-2_v6c` fa11c18f-661f-44aa-b456-9cce635587d6)
Verified by the reviewer: every other moving shot is smooth (stability note answered), no Warp banners / warping, all transitions clean and on their beats, tone consistent, audio to spec.
1. **C089 hold jumped ≈25 px (major) — fixed:** the live part is Warp-stabilised, the 0.01-speed hold piece wasn't. The hold is now the stabilised last moving frame (44.80) baked from the graded body, on V6 44.84–45.48. Frame diff into the hold 1.6, shift 0.
2. **C091 jitter 2.5 + soft opening (major) — fixed:** source 0.12–1.40 (its steadiest stretch), no Warp, 124 % top-anchored; jitter 0.22, sharp from the first frame (1356).
3. **C124 crowd phones (major) — fixed:** 138 % top-anchored (crowd into the IG band); +0.12 stop.
4. **C132 raised phone (major) — fixed:** nest 128 % top-anchored (crowd into the band); zoom-through at 3.80 re-baked.
5. **C109 motion smear (major) — fixed:** replaced by **C105** (woodcut Durga panel, source 0.24–1.48, jitter 0.34, sharpness 3140 vs C109's 200); both whips re-baked.
6. **C116 faces + soft first frame (major) — fixed:** in-point 2 frames later (first frame 539), 125 % top-anchored.
7. C089 focus breath on the loudest bar (minor) — not changed (a hold mid-zoom would stop the move on the loudest bar).
8–10. C093 / C094 single-frame stutters, C087 tremor (minor) — not changed (≈1–2 px; Warp re-analysis or source limits).
11. Tone (minor) — partly: C085 +0.12, C124 +0.12, C125 +0.05 stop; C101's exposure is a keyed ramp, left.
12. C133 crowd (minor) — 120 % top-anchored; it remains a crowd flash by design.
- v6c exports 18:37: `_v6c_mix` 55.60 s −1.3 dB; `_v6c_IG` −11.4 dB. No Warp banners; black only in the end fade.

## Round 6 — Review gate, loop 2 (`analysis/review_v6c.md`): FAIL, 0 blocker / 3 major / 6 minor → v6d (`Reel_puja-night-2_v6d` d50965a2-8ca5-4a0d-9316-27bd64a52828)
Gate limit reached (2 loops); every finding fixed or answered by the editor and verified by numbers and frames, no third blind review.
1. **C087 forward move stutters (major) — fixed by removal:** the stutter is in the source (CFR 25, but the zoom steps unevenly: cadence 0.16, jitter 0.97). C087 out; **C129** (scaffold, looking up; source cadence 0.02) re-placed fresh at 37.92–40.44 (source 0.48–3.00, no Warp). In v6d: jitter 0.8 px, cadence 0.12 (C087 was 2.3 / 0.15).
2. **C132 soft (major) — fixed:** the 1080 × 1920 nest at 128 % was an upscale. C132 placed fresh from the 4K source at 3.80 (source 0.12–3.90 at 150 %, 2.52 s), 128 % top-anchored, Lumetri from v5c (+0.2 stop), no Warp, **Optical Flow** interpolation (QE `setTimeInterpolationType(2)`). Sharpness 44 → 75 (1.7×); jitter 0.6 px, cadence 0.11 (frame sampling gave 2.9 / 0.24). Frames checked by eye: no flow warping on arches, mural or heads.
3. **C086 tone outlier (major) — fixed:** temp 50, tint +5, sat 140, highlights −15. Saturation 0.47 → 0.65, warmth (R−B) 0.19 → 0.34 (neighbours C090 0.82 / 0.43, C125 0.90 / 0.55; it stays the least saturated of the three because the teal mesh is in the content).
4. C085 (minor) — 115 % top-anchored (awning into the IG band), +0.25 stop. Mean luma 0.203 → 0.194: the bright awning left the frame, so the lift doesn't show in the number; left as a dark lantern flash.
5. C116 faces (minor) — 132 % top-anchored; heads below y 1620.
6. C091 phones (minor) — 130 % top-anchored.
7. C135 / C133 red (minor) — C135 saturation 64; C133 −0.25 stop (mean luma 0.298 → 0.280). The red hero hold stays red (approved).
8. C089 hold (minor) — accepted as a designed freeze on the 44.84 beat.
9. C125 / C126 dark scaffold (minor) — by design; ask the director at Checkpoint 2.
- Re-baked from the v6d body (V6 hidden): `d00_zoom_3.80` (into C132) and `d01_leak_40.44` (out of C129); swapped on V6.
- v6d exports: `_v6d_mix` 55.60 s, −1.3 dB peak / −16.3 dB mean; `_v6d_IG` −11.6 dB peak (music muted). Frame scan: only designed flags (transition blur, leak luma jump, C089 hold, end fade). No Warp banners. Timeline gaps: none.

## Round 6 — Checkpoint 2 (v6d, 2026-10-19)
- Director watched v6d full-screen on the phone with sound. Asked "What would make it more cinematic?": **"Nothing more, approved. Go to the Instagram package."**
- v6d is the final cut: `Reel_puja-night-2_v6d`, `renders/exports/puja-night-2_v6d_mix.mp4` (guide mix) + `_v6d_IG.mp4` (upload file; add IG library *Shondhatara* from 1:45.6). The three by-design calls (dark scaffold pair, C089 freeze on 44.84, red feet hold) stand with the approval.

## Instagram package
**Status:** approved 2026-10-19 (Checkpoint 3): hook 1, the caption as written, the 5 hashtags, cover 00:00:46:20 (Durga's face). Not published (the director posts).

**First-line hooks (≤ 125 chars)**
1. (Recommended, IG1 number-first → saves) "62 clips from one Puja night, 8:16 pm to 1:48 am, cut to 55 seconds on Shondhatara." (83)
2. (IG3 cold-open, nostalgia → comments) "Pandal to pandal until 1:48 am: red arches, woodcut walls, giant nuts and bolts, and then her face." (99)
3. (For the filmmaker crowd → saves) "Shot handheld at night on an iPhone 17. Every transition in this reel is built from its own frames, on the beat." (112)

**Caption (hook 1; 1079 chars, 0 em dashes)**
```
62 clips from one Puja night, 8:16 pm to 1:48 am, cut to 55 seconds on Shondhatara.

It opens on her name, the night flickering inside the letters, and zooms through on the song's biggest hit into the red arches.

Then pandal to pandal. Folk dolls, Bengali woodcut walls, a lotus pandal in bamboo, an iron scaffold, giant nuts and bolts, a pair of giant carved red feet above the crowd. On the song's peak a gold light leak opens on Durga, and the night ends on her face.

For the filmmakers, how it was made:
Shot handheld after dark on iPhone 17 with the Blackmagic Cam app, 4K 25 fps.
Handheld moves stabilised in Premiere; the opening tilt runs at 150 % with optical flow.
The zoom-throughs, whip pans and the light leak are built from the reel's own frames, each one on a beat.
Graded warm with a Kodak 2393 film-print look.

Save this if you're shooting a pandal this Puja. More cinematic Puja edits on @satyajitmall.

Music: Shondhatara, Coke Studio Bangla (Arnob, Sunidhi Nayak, Adit Rahman)

#durgapuja2026 #pandalhopping #shotoniphone17 #iphonecinematography #durgapuja
```

**Hashtags (5, sized):** #durgapuja2026 (niche) · #shotoniphone17 (niche) · #pandalhopping (mid) · #iphonecinematography (mid) · #durgapuja (broad label). Same set as my-reel, so the two Puja reels group together.

**Cover frame:** **00:00:46:20** (46.80 s, C139 Durga's face, the sharpest frame of the push; fills the 3:4 grid crop) → `renders/stills/cover/cover_A_C139_46.80.png`. Alt: 00:00:03:06 (3.24 s, DURGA title card with PUJA NIGHTS · 2026) → `cover_B_DURGA_03.22.png`. Preview: `renders/stills/cover/cover_AB_preview.jpg`.

**Media to attach:** `renders/exports/puja-night-2_v6d_IG.mp4` (55.60 s; natural sound + SFX, music muted), then add Instagram's library *Shondhatara* (Coke Studio Bangla) starting at **1:45.6** so the cuts land on the beats. `_v6d_mix.mp4` is the guide mix with the song (−13.9 LUFS, −1.3 dBTP) for checking sync; don't upload it (the song isn't licensed for sync). Both files pass `verify_render.py` (`analysis/verify_v6d_*`; only flag: the designed C089 hold).

Facts only from the footage metadata (62 clips, iPhone 17 + Blackmagic Cam, 15 Oct 20:16 → 16 Oct 01:48, 4K 25 fps) and the edit. No pandal names or locations (none confirmed; "no location tags" approved in round 1).

## Retro (2026-10-19)
- `retro.md` (copied to `studio/retros/puja-night-2.md`). 8 CRs for HQ: the six from 2026-10-18 (extendscript-notes, focus-qa, script-bugs, premiere-session-setup, commercial-music-ig, motion-ai; all with round 4–6 follow-ups) and two new: CR-20261019-puja-night-2-review-gate, CR-20261019-puja-night-2-beat-transitions.
