# Project Log

| Field | Value |
|---|---|
| Reel name | kolkata |
| Status | done (2026-11-08): v8c approved with its Instagram package; retro written |
| Reel type | hybrid (round 5: spoken guide intro + song; was music-montage) |
| Playbook | cinematic-montage (calmed to the reference's pace; overrides to be set in the brief) |
| Arch version | 0.9.0 |
| Pilot | yes |
| Current round | 8 |
| Premiere project | `projects/kolkata/premiere/kolkata.prproj` |
| Latest sequence | `Reel_kolkata_v8` (54a7d1e7-996f-40ca-8338-aa9783ece7c5) |
| Latest export | `renders/exports/kolkata_v8c_mix.mp4` · `renders/previews/kolkata_v8c_phone.mp4` |

## Now
<!-- Rewritten at the end of every round, in at most 30 lines. A new session reads this block and the latest round only (skill Phase 0). -->
- **Status: done (2026-11-08).** The director approved v8c and its Instagram package ("Approve, do retro"). Retro: `retro.md` = `studio/retros/kolkata.md`. Posting only when the director asks.
- **Sequence:** `Reel_kolkata_v8` (54a7d1e7-996f-40ca-8338-aa9783ece7c5), a duplicate of v7. Rollbacks: `Reel_kolkata_v7` (v7b), `Reel_kolkata_v6`.
- **Post this:** `renders/exports/kolkata_v8c_mix.mp4` (= `deliver/kolkata_v8c_POST.mp4`; baked song, −14 LUFS). Phone: `renders/previews/kolkata_v8c_phone.mp4`.
- **Cut:** 76.20 s, 26 shots, `analysis/edl_v8.json`.
- **Since v6_3:**
  1. look: Fuji Eterna 250D → 3510 at 30 % on V3 (preset);
  2. title (V5, 7.76–10.56): "Kolkata / the city of / CULTURE, HERITAGE AND SURPRISES" in Amita / Tiro Bangla Italic / Eczar (`tools/make_title_v7.py --style amita --y 425`, fonts in `assets/fonts/`, OFL);
  3. shot 9 "passion": Oct 15 C076 gold Durga in profile (AE Timewarp 88 %, Warp);
  4. shot 17 flower seller de-duplicated (45 fps, 0.56×); shot 18 Kumartuli = Pexels 33742628 clay face; tram interior Shadows +10 / Blacks +1.
- **Package (`deliver/`):** `PACKAGE.md` (hooks, alt text, settings, two risks), `caption.txt`, `kolkata_v8_cover.jpg` (C076 + title, Eterna 30 %). AI label off.
- **Accepted minors:** shot 9 ~27 % softer than camera (Pixel Motion, only at 2×); the title's caps line rests on the cartridge top (0–20 px); the flower seller's blown reds (source); the tram's darkest tones slightly flat (only at 3× gain).
- **Open for the director:** posting, on request only (iPhone Mirroring, stop before Share; the director taps it).
- **Next:** HQ applies the 12 kolkata CRs (`/studio-hq`). Reel work only if the director asks to post or change something.
- **CRs (12):** landscape-footage-9x16, premiere-soft-bloom, song-research, film-emulation-first-use, lyric-shot-skill, montage-line-table, preview-fx, footage-catalogue, look-preset-second-lumetri, cover-title-type, stock-intake, late-round-edits.
- **Tools (reel-local):** `swap_v7.py` (shot swaps on a built sequence), `make_title_v7.py`, `deliver_v8c.sh`, `build_v6.py`, `guide_edl_v6d.py`, `fx_prerender.py`.

## Friction log
<!-- Pilot reels: one line each time something is slow, fails, needs a guess, a manual step or a workaround. Format: `- [phase] what happened → workaround → CR filed? (CR id / no)` -->
- [Phase 0] Reference arrived as `Frames from North Kolkata - October 2025Shot on Fujifilm X-T3 Edited on DaVinci Resolve...Howrah.mp4` (spaces, `...`) → renamed in the reel folder to `references/ref_north_kolkata.mp4`; the original stays in `~/Downloads/` → no CR.
- [Phase 0] No studio tool says whether a reference's audio is speech, song or instrumental (sets reel type and the audio route) → ran `scripts/transcribe_local.py --model small` on the extracted audio in the scratchpad: it found sung Hindi/Urdu vocals, which identified the song. Took ~10 s → no CR (works; note for HQ if it recurs).
- [Phase 0] Profile says brand colours are "not set yet (ask once)". Asked; the director picked the reference's yellow + red **for this reel only**, so the brand colour is still unset → no CR (nothing new to record in the profile).
- [Phase 1] `analyze_footage.py` on 101 4K clips (14.5 min of footage) took ~20 min with `ingest_report.py --scan` running alongside → slow but fine; no CR.
- [Phase 1] Every clip is tagged rotation −90, whichever way the phone was held. 57 usable clips are landscape on their side; the overview can't show which way to turn them → both-rotation sheet in the scratchpad, picked by eye → `analysis/orientation.json` → **CR-20261104-kolkata-landscape-footage-9x16**.
- [Phase 1] The 80 %-of-width rule (CLAUDE.md §3) can't hold for landscape clips in 9:16 → framing sheet (full-bleed / 16:9 frame / 4:5 window); the director picked the 4:5 window → same CR.
- [Phase 1] `look_preview.py` squashes a portrait still into a landscape tile when the stills are mixed (C100) → ignored for this round → same CR (item 4).
- [Round 2] The director wanted more looks than the 3 offered → previewed all 8 film stocks, CineStill / mono / muted-red / bleach, the 5 starter LUTs, an ffmpeg "≈ match reference", and an effects sheet (grain, vignette, bloom, halation, light leak, stack) from a scratchpad ffmpeg script. SpeedLooks (`SL *.itx`, e.g. SL GOLD TOBACCO, SL CLEAN KODAK B SOFT) are encrypted and can't be previewed outside Premiere → no CR (known, §A3).
- [Phase 3] `verify_premiere_connection`: Premiere running, MCP Bridge not running (`bridge_unavailable`) → manual step for the director → no CR (known).
- [Phase 3] The director's new project was saved as `projects/pujo-ki-asolei-sobar/premiere/KOLKTA REEL.prproj` (another reel's folder) → `app.project.saveAs` to `projects/kolkata/premiere/kolkata.prproj`. The empty stray file stays in pujo's folder for the director to delete (a reel session doesn't touch other reels) → no CR.
- [Phase 3] `export_frame` (no `format`) returned `Illegal Parameter type`, and QE `exportFramePNG` returned false, until `renders/stills/` existed. After `mkdir` QE worked. Cause of the `export_frame` error unconfirmed (likely the missing folder) → no CR yet.
- [Phase 4] The director's adjustment layer was created in the selected `06_Music` bin; `rootItem` search missed it → recursive search, then moved → no CR.
- [Phase 4] Premiere 2026's Gaussian Blur is `AE.Impact_Blur_FX` with an **Amount** property, not "Blurriness" (the script failed with `null is not an object`) → property dump, then set Amount → CR (bloom route).
- [Phase 4] The playbook's soft-bloom route is After Effects `glow` per shot (13 round trips, ~50 min, plus swapping the renders back in and re-applying the primaries) → built in Premiere as a V2 highlight copy in Screen mode instead, tuned by render in two passes → **CR-20261105-kolkata-premiere-soft-bloom**.
- [Phase 3 v2] `setInPoint` on the WAV guide landed 1 frame early (74.68 for 74.72 s), found only by cross-correlating the export against the guide → re-placed → CR item for the reality doc? → no CR yet (one occurrence).
- [Round 3] No song-research step in the studio; two builds were spent on rejected songs → reel-local method + **CR-20261106-kolkata-song-research**.
- [Stock] `.env` has `PEXELS_API_KEY=` with an empty value, and the studio has no stock-search script → read the Pexels search and video pages in Chrome (search-page HTML for IDs, page data for size / fps / length / author, screenshots to check content). It took ~15 min for 10 queries and ~12 page checks. Pexels titles can be wrong ("Howrah Bridge" 27496938 is another bridge), so check by eye → no CR yet (a `stock_search.py` with a working key would cut this to minutes).
- [Round 2] The director picked the effects sheet's "film stack" as the look. The soft bloom has no Premiere-native route: After Effects `glow` per shot (after-effects.md) or an ffmpeg bake like the halation recipe → decide in the brief; no CR yet.
- [Round 3] iPhone Mirroring for IG Insights: first `request_access` was denied in the dialog; on retry (2026-11-07, iPhone connected) computer-use answered "Computer control is disabled in Settings" → asked the director to turn computer use on in the Claude app settings, or send screenshots → no CR (app setting, not studio).
- [Round 3] iPhone Mirroring can't take background input while the Mac is in a full-screen Space (`app_bring_to_current_space` refused; clicks ignored) → full-screen control. Typing drops characters after the first (`type`), so one key per letter. Scrolling needs scroll_amount 100. Insights → Content showed "No content available" for 1 year → per-reel views read from the profile grid → no CR (record in a future IG-data CR if HQ wants an insights tool).
- [Round 3 audition] The director's song copies are music-video rips; Mayabee is AAC inside a `.mp3` name, which `librosa`/libsndfile can't open (`song_fit.py` crashed after measuring the other two) → converted all three to 48 kHz WAV in `music/`. Rips may not start where IG's library version starts → IG cues given as song moments, not timecodes → CR-20261106 (add: convert to WAV on intake).
- [Round 3] `orientation.json` (Phase 1, picked by eye on both-rotation sheets) had 3 clips labelled portrait that display sideways (C017, C018, C025), and C109 marked unusable when it was only sideways. Found only on the director's note, by rendering every clip upright at its best moment → full-pool upright sheet `analysis/pool_v3/` → CR-20261104 (add: verify orientation on upright best-moment sheets, not mid-frames).
- [Round 3 audition] No studio tool cuts one shot pool to several songs → reel-local `tools/audition_edl.py` (beat-snapped, energy-paced, priority drops); first pass gave one bar per shot (mechanical) → song-wide energy, 2-bar quiet holds, arc bias, soft-end re-split → CR-20261106 item 3.
- [Round 4] Story note for the third time; v3b_M3 had passed the review gate. The line table (skill Phase 2.3) is VO-only, and the reviewer has no story check, so a list of places passed → line table + `tools/story_edl.py`, played-beat cuts → **CR-20261107-kolkata-montage-line-table**.
- [Round 5] The song's spoken intro is in English, then Bengali; Whisper with `--language bn` turned the English into garbage, so the guide's lines were found only by re-running chunks with `en` and `bn` (faster-whisper's own decoder also failed on a WAV path: PyAV `metadata_errors`; passed a numpy array instead) → no CR (note for HQ: `transcribe_local.py` has no mixed-language mode).
- [Round 5] Finding free stock for 9 reference shots took a subagent 23 min in Chrome (no Pexels API key, no stock-search script) → same gap as the round-2 stock line → no new CR.
- [Round 5] The director changed the song and the length mid-round (reference song → "Kolkata", 60–90 s), after the stock search had started → the line table was written once both were known; no rework.
- [Round 5b] The offline preview can't stabilise, its slow-mo on 25 fps repeats frames, ramps are a two-piece step, whips and leaks don't show; the director judged v5 without the planned effects ("no cinematic effect") → reel-local `tools/fx_prerender.py` (stabilise / interpolated slow-mo / eased ramp / whip / interpret) and `tools/make_leak.py` → **CR-20261107-kolkata-preview-fx**.
- [Round 5b] `scripts/shake_report.py` crashes on camera `.mov` files (`ValueError: could not convert string to float: '7319,'`, ffprobe fps with a trailing comma) → measured on the preview instead → same CR.
- [Round 5b] The steadiest replacements came from the Pujo pool (the city footage has few locked night or "surprise" shots), which took Pujo to 8 of 30 shots before anything was sent; the director: "too many pooja shots" → 4 of 28, with own non-Pujo shots for explorer and the final. The line table has no subject-mix check → no CR (reel-level; the round-4 story CR covers line-table checks).
- [Round 6] The round-5 note "Ami urjar mukheejee section cut out and use it as ami apanader guiide" asked to CUT the name; I read it as "use the guide intro" and kept the name for two rounds → name cut in v6; lesson: restate an ambiguous note as an action and confirm before building → no CR.
- [Round 6] No step asks what the sung lines mean; Whisper turbo `bn` garbled the sung verse, and an initial prompt made turbo hallucinate its words → large-v3 without a prompt, envelope for word boundaries → **CR-20261107-kolkata-lyric-shot-skill** (the director asked for this skill).
- [Round 6] The director asked for a new skill; a reel session can't write `.claude/skills/` → drafted in full inside the CR for HQ → same CR.
- [Round 6b] Free stock has no running Kolkata tram shown head-on (Pexels, Pixabay, Commons all searched; about 40 min). The one Pexels clip with a tram shows it side-on behind cars. A shot list for the director's next walk would have caught it at Phase 1 → no CR (footage gap, reel-level).
- [Round 6c] **No tram footage, but plenty of photos.** Free stock video had no running Kolkata tram head-on, while free stock photos had plenty (Unsplash: 200 "kolkata tram"). I spent $0.64 on an AI tram before the director asked for a photo. Lesson: search photos as well as video before proposing AI → reel-level lesson, no CR. Also: a still pre-framed in window coordinates needs `pos [540, 960]` (the EDL default 910 lifted it 50 px and showed a blur strip) → fixed in `guide_edl_v6c.py`.
- [Round 6d] **Finding a clip by what the director remembers** ("the bus depot video", "people dancing on the streets during bhashan") meant grepping five reels' notes and re-reading survey sheets (~35 min for three lookups). Nothing catalogues the shared Pujo / KOLKATA footage by content → CR-20261108-kolkata-footage-catalogue.
- [Round 6d] `shake_report.py` still crashes on the camera's rotation-tagged files (`'7319,'`), so 16 proxies were transcoded first. Phase correlation also counts a big moving subject as shake (the bus measured 13.9 px on a locked camera), so the background had to be judged by eye → same CR.

- [Round 6d build] `scripts/ae_roundtrip.py` can do a constant Timewarp or a frame-repeating `time_remap`, but not a ramp with Pixel Motion (no `frameBlendingType` on the remapped layer), so the dhakis 100 → 40 % ramp came from the reel-local `fx_prerender.py` (minterpolate) at 1080×1920 → CR-20261108-kolkata-footage-catalogue item 4.
- [Round 6d build] Track-item in-points landed 1 frame early on 2 of 26 video clips and on 1 audio clip (the v2/v3 WAV quirk, now also on video). The build reads back and fixes them; a generic "place, read back, correct" helper would save every build from rediscovering this → same CR, item 5.
- [Round 7] **`applyLumetriPreset` on a layer that already has a Lumetri inserts a second Lumetri *before* it.** My script set Creative Intensity on the last (old, look-less) Lumetri, so the first render had the look at 100 % (sat +0.15 vs +0.04 previewed). Only the render check caught it; the read-back said "30". Fixed by picking the Lumetri whose Look ≠ 0. Also confirmed: Creative Intensity mixes linearly (Premiere = preview within 0.003) → CR-20261108-kolkata-look-preset-second-lumetri.
- [Round 7] A full rebuild (`build_v6.py`) would have wiped the hand-made fixes (dissolve, in-points, Warp, title keys) and the new look, so two shot swaps needed a new reel-local `tools/swap_v7.py` (remove, place, read back, re-make edge dissolves). The read-back part is CR-20261108-kolkata-footage-catalogue item 5; the swap itself is reel-level for now.
- [Round 7] `shake_report.py` gave 30–44 px "jitter" on C168, a smooth pan across a bamboo grid: the repeating grid aliases the phase correlation. Judged by eye on a 0.17 s frame strip instead → same CR (item 3).
## Rounds 0–1 and Phase 1
Moved to `log/rounds.md` (2026-11-07).

## Rounds 2–3 and the Instagram package
Moved to `log/rounds.md` (2026-11-07).

## Round 4
Moved to `log/rounds.md` (2026-11-07).

## Round 5
Moved to `log/rounds.md` (2026-11-07). Song map and the v5 line table are there; line meanings now in `analysis/lyrics_meaning.md`.

## Round 5b — Director notes on the v5 preview (2026-11-07)
Moved to `log/rounds.md` (2026-11-08).

## Round 6 — Director notes on v5b (2026-11-07)
Round 6 (the lyric line table, the name cut) and Round 6b (the AI tram) moved to `log/rounds.md` (2026-11-08).

### Round 6c — the tram photo (2026-11-07)
Moved to `log/rounds.md` (2026-11-08).

### Round 6d — Director notes on v6c (2026-11-08)
**Notes, verbatim (voice, two messages):**
> "Okay, there are a couple of imperfections here. Uh, The inside of the tram, that video, uh, there is a problem where it goes out of focus. The one where I'm walking on the lanes and one said Ganga is visible. It has stabilization issues. There are a couple of footages like that. You can check using one of them. The same one while I'm working on the bridge, it is stabilization issue. You can check what we can use. Uh, And if you look at the city of surprises where you have used a cart hand pull cart, can you use the tram line video or the bus depot video that I have? Try if they fit in better. And while you are seeing the video, of the while you're seeing the standing tram that you use, which does not fit in, try if you can possibly take an image of a bus Kolkata bus that is moving, or the bus stop that I have captured in my part of the reels, right? City"
>
> "And in the city of surprises, maybe try and use the picture where people are dancing on the streets during bhashan."

**Read as, and measured:**
1. **Tram interior out of focus = shot 25, C030.**
   - Sharpness per 0.2 s (variance of the Laplacian, centre 60 %) holds at 1.0–1.17× the clip median from 0 to 4.8 s, then drops to 0.16× at 5.6 s and 0.03× after 8 s.
   - The shot used 2.0–6.12, so its last 1.3 s was soft. **Now 0.40–4.52**, sharp throughout.
2. **The walk with the Ganga on one side = shot 7, C089** (the river promenade, lamps against the sun). The preview never stabilised it.
   - Stabilised with smooth σ 30, zoom 1.06: the current window (6.4 s) measures **0.84 px** on the full frame, 1.03 px in the reel (v6c 1.65).
   - The 2.8 s window measured 2.16 px, so it was not used.
3. **The walk on the bridge = shot 6, C082** (the Howrah walkway POV).
   - In v6c (σ 20, camera 0.0–3.96) it measured 2.10 px in the reel, the highest of our own shots, with a 5.7 px lurch at camera 1–2 s.
   - **v6d: σ 40, zoom 1.08, camera 2.0–5.96** (past the lurch) → **1.23 px** in the reel framing, peak 2.75 (was 4.89).
   - C084, the other walkway POV, measured 1.54 px at σ 30 on the full frame, so C082 stays.
   - The C089 promenade measures 1.03 px in the reel (v6c 1.65).
   - Jitter measured on a full-frame pre-render reads about half the in-reel number, because the 4:5 window magnifies the frame about 2.2×. Compare in-reel against in-reel.
4. **"City of surprises" (shot 5, was the stock hand-pulled rickshaw):**
   - **The tram line** = C023, rails in the road at dusk, locked at 0.3 px.
   - **The bus depot** = C020/C021, the terminus at sunset under the trees, locked at 0.2 px.
   - **The bhashan street dancing:** searched Oct 21 C001–C057 (four goddess survey sheets plus new sheets):
     - C047 25–27 s has a woman dancing in the street beside the dhakis and Ma's truck. It is **7.6 px even with a locked stabilisation** (the truck drifts ~100 px), smeared, with a passer-by crossing in front, so it fails;
     - C025 looks like dancing at 2 fps, but it's men hauling Ma up the ghat steps on ropes;
     - the only clean dancing at the bhashan is **C035**, the women in lal-paar saris dancing on the ghat road, which was shot 9.
   - **v6d: C035 moves to "surprises" at real speed (src 0.4).** C023 and C020 are on the options sheet as alternatives.
   - The tram line and the depot are steady and in the right light, but neither reads as "surprise" at a glance.
5. **Shot 9 "… passion" accent** (C035 left it): **Oct21 C029, the big dhak at the ghat**.
   - Locked, sharp, 0.13 % ripple; slow push 50 → 54; hard cut on the accent after the dhakis' slow motion.
   - Copied to `raw/selects/Oct21_A001_10211946_C029.mov`.
   - **Tried and rejected:**
     - Oct19 C027 (a boy dancing to the dhak): 3.4–4.9 px and 2.15 % flicker;
     - C003 Maidan football: the players are too small to read.
6. **The standing tram (shot 21, the photo) → a moving Kolkata bus.**
   - Pexels "kolkata bus" gave **39654702** (Trishik Bose): a garlanded blue-and-yellow private bus driving straight at the camera, front end clear. Picked for v6d.
   - Interpreted 30 → 25 (0.833×, so 3.4 s of source fills the 4.08 s line), src 0.5, push 125 → 130, pos x 490 so the front stays clear of the IG buttons as it nears.
   - **Alternatives:**
     - the director's own bus stop C019: a blue bus boarding at sunset, but a man crosses close to the lens at 1.5–4.2 s, and the bus doesn't move;
     - Pexels 32665222 / 32665228: side-on buses, same shoot as the rickshaw.
   - Licences are in `raw/SOURCES.md` (Round 6d).

**v6d** (`tools/guide_edl_v6d.py` → `analysis/edl_v6d.json`, jobs `analysis/fx_jobs_v6d.json`):
- v6 with the six changes above; 76.20 s, 26 shots.
- **Pujo:** 4 of 26 (dancers, dhakis, dhak, Kumartuli).
- **No AI shot.**
- **Build recipe for the bus:** interpret 39654702 to 25 fps; Scale 125 → 130; Position 490, 910.
- **Options sheet:** `analysis/round6d_options.jpg`. Pool sheets: `analysis/round6d_bus_tram_pool.jpg`. Shake: `analysis/shake_v6c.json` (v6c per shot).

### Round 6d — Build `Reel_kolkata_v6` (2026-11-08)
Director: "Yes, build v6d".
- **Sequence:** `Reel_kolkata_v6` (5ae5d5b3-909f-456d-a451-d9b04afd7179), duplicated from `Reel_kolkata_v3b_M3`, which stays untouched as the rollback.
- **Build script:** `tools/build_v6.py` → `analysis/_es_build_v6.jsx`, run with `$.evalFile`. It does the following:
  - places the 26 shots on V1 frame for frame;
  - interprets 11 stock files to 25 fps first: 24, 23.976, 29.97, 30, 59.94 and 60;
  - applies the EDL's Rotation, Position and eased Scale keys;
  - clears V2 (v3's bloom copy, a look) and V4 (grain), and disables the V3 adjustment layer (camera-true);
  - puts the "Kolkata" title on V5 with the 0.4 s settle, the V6 window matte to the end, and V7 black fades (6 f in, 20 f out);
  - audio: A2 needle drop (−8 dB) and tram bell (−20 dB); A3 song from 7.25 s at −2.5 dB with a 1.5 s fade; A1 muted.
  - **Read-back:**
    - C082 / C089 and the tram bell landed 1 frame early. Fixed by setting the track item's in/out (C082 = 2.00 s, C089 = 6.40 s, bell = 8.40 s);
    - the needle-drop clip ran past its media (6.89 s) and was trimmed to 172 frames;
    - V1 gaps: 0.
- **Slow motion:** After Effects Timewarp (Pixel Motion) at camera size 2160×3840, `analysis/ae_jobs_v6.json` → `renders/ae/v6_*.mov`, for C111 70 %, C061 70 %, C018 60 %, C028 50 %, C033 75 %.
  - Every render passed `frame_match`, and no doubled limbs were seen.
  - The dhakis ramp uses the preview's stabilised ramp render (`renders/fx_preview/Oct21_C047_dhakis.mov`, 1080×1920, Scale 108, 8 % upscale). `ae_roundtrip.py`'s `time_remap` has no Pixel Motion frame blending, so a 100 → 40 % ramp would stutter (friction log).
- **Stabilisation:** Warp Stabilizer via `stabilize_clip` on C082 (smoothness 50, auto-scale 102 %), C089 (50, 104.1 %) and the C061 AE render (30, 101.5 %).
  - All three analysed by themselves (AnalysisStatusCounter 408), with no banner in the export.
  - **Jitter in the reel framing, master vs the v6d preview:** C082 0.81 vs 1.23 px (v6c 2.10); C089 0.56 vs 1.03 (v6c 1.65); C061 0.33 vs 3.8.
- **Colour (camera-true):** one Lumetri on six clips only, the v3-approved cast fixes (temperature / tint / exposure):
  - C035: tint +6;
  - C047: exposure +0.3;
  - C029: tint +5 (new, the same green-cast flag as C035);
  - C061: +10 / +5;
  - C018: tint +4;
  - C105: tint +4, exposure +0.35.
  - No look yet: the sheet `analysis/looks_v6/looks_sheet.png` shows camera-true next to F125→2393 (preset), Eterna→3510 (preset), Reala→2393 (preset) and 500T→2383 (dropdown), at 30 %.
- **Master:** `renders/masters/kolkata_v6_master.mov` (ProRes 422 10-bit, 76.20 s, export 15 s, audio max −5.3 dB). It matches the preview on all 26 shots (`analysis/v6_master_vs_preview.jpg`).
- **Deliverables** (`tools/deliver_v6.sh`):
  - `renders/exports/kolkata_v6_mix.mp4` (H.264 High, −14.0 LUFS, peak −1.4 dBFS): **the file to post**, since the name cut can't ride on Instagram's library audio;
  - `renders/previews/kolkata_v6_phone.mp4` (720p, 27.6 MB);
  - **pregate PASS** (`analysis/pregate_v6/`).

## Round 6d — Review gate (v6 build)
- **First run** (`analysis/review_v6.md`, Fable 5.1, full review): FAIL, with 2 majors and 4 minors. All five of the director's notes were verified as done in the build.
- **Answers:**

  | # | Finding | Answer |
  |---|---|---|
  | 1 | major: the ghat bathers (Pexels 4200197) strobe as passers-by cross the lens | **fixed.** The clip is a timelapse with crossings all through its 10 s. The only long clean span is camera frames 180–261 (82 f), so the Setu sunset holds 2 beats longer (the cut moves 33.48 → 34.48) and the bathers play that span. AE Timewarp to stretch the clean span was rejected: Pixel Motion ghosted the jumping people (`renders/ae/v6_bathers_clean_64.mov`, unused). |
  | 2 | major: the planned 10-frame dissolve into the verse was missing | **fixed.** QE Cross Dissolve 10 f, centred on 29.52 (frames 733–743). `build_v6.py` didn't read the EDL's `dissolve` key; noted for the next build. |
  | 3 | minor: the title appeared 7–10 frames late | **fixed.** Opacity 0 → 100 over 4 f from 7.76, scale 104 → 100 over 10 f, blur 12 → 0 over 8 f. The still's in-point is 3599.96 s, so the keys are relative to it. |
  | 4 | minor: the cricket shot is the softest (1080p at 125 %) | **intended.** It's the director's pick since v5b; it will be named at Checkpoint 2. |
  | 5 | minor: a bystander at the dancers' left edge | **fixed.** Camera 1.0–3.0 s (the arms up), Scale 56, x 600. |
  | 6 | minor: the tram bell is ~20 dB under the song | **fixed in part.** Re-cued (in 10.25 s), so the first strike lands at 68.90 on the tram cut, and raised to −14 dB, the top of the studio's SFX range. The director judges it by ear. |
  | — | note: possible micro-judder in the dhakis' 40 % section | to check on the phone (the preview's minterpolate ramp; the director approved the preview) |

- **v6b:** `renders/masters/kolkata_v6b_master.mov` → `renders/exports/kolkata_v6b_mix.mp4` (−14.0 LUFS, −1.3 dBFS) and `renders/previews/kolkata_v6b_phone.mp4` (27.6 MB). Pregate PASS (`analysis/pregate_v6b/`); the diff shows changes only at 7.8–8.16, 15.92–17.92, 29.36–29.68 and 30.84–37.76, plus the audio.
- **Second run** (`analysis/review_v6b.md`, focused): FAIL, 1 major and 3 minors. Answers:
  1. **The bathers still blink** (smaller crossings all through the source) → **fixed by replacement.** Pexels 36819326 (people on the ghat at sunset, the Setu behind; vertical 4K, interpreted 30 → 25, Scale 50).
     - Warp Stabilizer (smoothness 30, auto-scale 100.4 %, analysed by itself, no banner). Sky-band jitter 5.5 → 4.4 px, on a par with the director-approved stock shots (Victoria 4.5, Howrah blue hour 4.7).
     - The reel-local `fx_prerender.py` stabiliser was tried first and helped less (5.1 px): the moving crowd in the lower quadrants confuses its 4-quadrant tracker.
     - Changing Warp's smoothness after analysis didn't re-solve (the label and the numbers stayed the same).
  2. **The bystander at the dancers' left** → fixed: Scale 62.5, x 405.
  3. **The bell cuts in mid-ring** → fixed: the clip starts at the cut (68.84) on file 10.65 s; the strike at 10.68 lands at 68.87.
  4. **The tram tail under the Academy shot** → fixed: the clip ends at 73.28 with a 0.5 s fade.
- **v6_3** (renamed from "v6c", so it isn't confused with the v6c tram-photo preview): `renders/masters/kolkata_v6_3_master.mov` → `renders/exports/kolkata_v6_3_mix.mp4` (−14.0 LUFS, −1.4 dBFS) and `renders/previews/kolkata_v6_3_phone.mp4` (27.6 MB).
  - Pregate PASS (`analysis/pregate_v6_3/`); the diff vs v6b shows only 15.92–17.92 and 34.48–37.76, plus the audio.
  - Maps: `edl_v6d.json` (current), `edl_v6d_build1.json` (v6), `edl_v6d_build2.json` (v6b).
- **Third run** (`analysis/review_v6_3.md`, the final focused check of the last fixes): **PASS**, no defects.
  - Notes for the director: the warm sunset → grey dusk cricket at 37.76 (time passing); a half-cut onlooker at the dancers' left edge for the first 0.4 s (a normal crowd edge).
  - The stale bell row in `edl_v6d.json` is fixed (`guide_edl_v6d.py` `review_fixes`).

## Round 7 — Checkpoint 2 answers on v6_3 (2026-11-08)
Director, verbatim:
> "Add a film look" → (the look question) "Fuji Eterna → 3510"
> "0.27 to 0.28, we say Kolkata Passion Air Shohor. In that, we are showing a single dhaki shot that he's playing, and looking at the river bank. That does not match with Kolkata Passion Air Shohor. Can we try and use a different footage, like a footage of a very surreal Durgama, or something like that, that would add a lot of effect there, right? We have so many lovely pandals of where people passionately have built the statues or the concepts. Can we look at any of them to use it through the puja footage?"
> "हर এই cheer code 0.52 seconds. The picture that the footage that you've used is good. Can we not find actual Kumatuli footage that can be used there?"
> (Kumartuli question) "D: clay face"
> "ket the first dhaki be there, for the sexond shot try and detremine a shot that showacses passion from teh pandals"

What I did, 1:1:
1. **Look** → Fuji Eterna 250D → Fuji 3510 (built-in preset) at 30 % on the V3 adjustment layer of `Reel_kolkata_v7` (75dc6c7d-8a4b-41fc-8b12-25e279e82458, a duplicate of v6). The inherited Lumetri on that layer was neutralised (vignette −0.5 → 0, no look). Render check against `looks_v6/looks.json` (v6 vs v7 Premiere stills, same frames):

   | still | Δ luma prev / Premiere | Δ sat | Δ R−B |
   |---|---|---|---|
   | 12.5 | −0.0092 / −0.0089 | +0.040 / +0.038 | +0.027 / +0.027 |
   | 74.6 | −0.0087 / −0.0083 | +0.095 / +0.093 | +0.039 / +0.038 |

   Scripts: `analysis/_es_look_v7.jsx`, `_es_look_v7_fix.jsx` (the preset landed in a second Lumetri; friction log).
2. **0:27.5 "passion" (shot 9)** → the director kept the dhakis (shot 8) and left the pandal pick to me. Pool: 25 candidates from five reels' notes (`analysis/round7_pandal_candidates.md`, by a research agent), the top 8 on `analysis/round7_passion_pool.jpg`. Picked **Oct 17 C168**, the giant Durga face over lit diyas under violet light: eyes to camera, the craft of the pandal, and its 1.7 s on the face fills the 2.04 s slot exactly at 30 → 25 fps. Copied to `raw/selects/Oct17_A001_10180047_C168.mov`. Camera 1.4–3.1 s, Scale 56 → 60 (≥ 83 % of the width), x 540. Smooth pan, checked on a 0.17 s frame strip (shake_report is fooled by the bamboo grid). Not used: C175 (flying bronze Durga, never posted; the runner-up), C162 (in uski-aankhein's final).
3. **0:50 Kumartuli (shot 18)** → 7 free Pexels Kumartuli clips (`analysis/round7_kumartuli_pool.jpg`, `raw/SOURCES.md` "Round 7"); the director picked **D, Pexels 33742628**: hands shaping the eye of a raw clay goddess face. Camera 2.1–3.9 s (its steady window, 1.65 px), 29.92 → 25 fps, Scale 50 → 53.
- **Build:** `tools/swap_v7.py` → `analysis/edl_v7.json` + `_es_swap_v7.jsx`. Read-back: in-points exact (C168 42 f, D 63 f), the 10 f Cross Dissolve at 733–743 re-made, C168's camera sound removed from A1, V3 on. Stills `analysis/look_v7/v7_swaps.jpg`.
- **Master:** `renders/masters/kolkata_v7_master.mov` (ProRes 422, 76.20 s, exported in 20 s). Delivery `tools/deliver_v7.sh`.

## Round 7 — Review gate (v7 build)
- **First run** (`analysis/review_v7.md`, Fable 5.1, focused on the look across all 26 shots + the two new shots): FAIL, 1 major + 3 minors. The look "reads as natural film colour, not a filter" (skin hue ≤ 1°, blue hour stays blue); shot 18 passes; audio md5 identical to v6_3.
- **Answers:**

  | # | Finding | Answer |
  |---|---|---|
  | 1 | major: shot 9 too tight; the crown is clipped and the diyas are a sliver, unlike the pool tile the shot was picked from | **fixed.** Scale 50 → 53 (was 56 → 60), y 830 (was 910): the crown and the flame bed stay in the window for the whole glide; 94–100 % of the width. Checked on simulated frames (`analysis/round7_framing_d.jpg`) and an export still. |
  | 2 | minor: the Eterna toe deepens the tram interior (C030) | **fixed.** One Lumetri on the clip: Shadows +10, Blacks +1. Still at 70.9 s: luma 0.129 (= camera-true v6_3; look only 0.125), ≤ 16/255 54 % (v6_3 51 %, look only 56 %), p02 7 (v6_3 4). Blacks +3 and +12 floored the blacks (p02 10 / 18) and were rejected. |
  | 3 | minor: the flower seller's blown reds grow a little (7.0 → 7.8 % of the window) | **accepted.** The source is blown (noted since round 6); darkening the highlights can't bring texture back. |
  | 4 | minor: the flower seller repeats every 4th frame (pre-existing since round 6) | **fixed.** The Pexels "60 fps" file is 45 fps with every 4th frame doubled. `renders/fx_preview/stock_flower_seller_dedup45.mov`: camera 3.0–4.8 s, the 27 repeats dropped by measured index (consecutive diff < 1.0), 81 unique frames at 45 fps, ProRes 422 HQ; interpreted to 25 = 0.56× (was 0.42× with hitches). Min consecutive diff 7.4 (no repeats). `mpdecimate` didn't drop them (its block thresholds miss near-identical repeats with encoder noise). |

- **v7b:** `tools/swap_v7.py --base analysis/edl_v7.json` (shots 9 and 17; `edl_v7_build1.json` = the v7 map), `analysis/_es_c030_shadows_v7.jsx`. Master `renders/masters/kolkata_v7b_master.mov`; delivery `tools/deliver_v7b.sh`.
- **Second run** (`analysis/review_v7b.md`, the focused check of the three fixes): **PASS.** Shot 9 keeps the crown and the diya flames for the whole glide; the flower seller has no repeats and no wrongly dropped frames; the tram's mean luma equals v6_3 and the camera.
  - One minor left, **accepted:** the tram's darkest tones sit a little flat (floor at code 22 vs the camera's 19–20); the reviewer can't see it at 1×. Changing Blacks again would send the director an unreviewed fix (the gate's 2-loop cap). If wanted later: Blacks −2.
- **v7b deliverables:** `renders/exports/kolkata_v7b_mix.mp4` (−14.0 LUFS, −1.4 dBTP; the file to post), `renders/previews/kolkata_v7b_phone.mp4` (27.6 MB), master `renders/masters/kolkata_v7b_master.mov`. Pregate PASS (`analysis/pregate_v7b/`).

## Instagram package (Phase 8, v7b, 2026-11-08)
Director: "Approved, start IG" (v7b). Package in `deliver/`: `PACKAGE.md` (hooks, settings, alt text, risks), `caption.txt`, `kolkata_v7b_cover.jpg`, `kolkata_v7b_POST.mp4` (= `renders/exports/kolkata_v7b_mix.mp4`).
- **Hooks:** (1, recommended) "Paris can keep love. To me, Kolkata is the city of passion." · (2) "A 76-second guide to Kolkata, from the Coffee House to a tram at night." · (3) "For everyone who left Kolkata for work and still calls it home."
- **CTA:** send it to the friend who moved to Bangalore and still calls Kolkata home (followers: Kolkata 31 %, Bangalore 22.8 %, `research/ig_insights.md`).
- **Hashtags (5, topical):** #kolkata #kolkatadiaries #cityofjoy #calcutta #durgapuja.
- **Credits:** the song (Anupam Roy, Shreya Ghoshal, *Praktan* 2016); the 11 Pexels creators by name (no @: handles unverified); the AI line (@claudeai, @adobevideo; Premiere Pro and After Effects).
- **AI info label: off** (no generated shot in the cut).
- **Cover:** custom, the C168 Durga frame (0:28.7) with the title PNG lowered into the diya band (`analysis/ig_v7b/`).
- **Flagged to the director:** the baked commercial song (mute/limit risk; the library version can't carry the name cut), and stock = 13 of 26 shots, 51 % of the runtime (originality ranking).
- Humanizer audit: reads human; first line 59 chars; 0 em dashes; 3 emoji (credits only, the director's habit).

## Round 8 — Title, cover and the "passion" Durga (2026-11-08, after the package)
Director, verbatim (after "Approve package"):
> "Not the thumnail please look for a bvetter thumbnail" · "use better cinematic fonts" · "KOLKATA / The cityof / Culture Heritage and Surprises / thsi whoculd obe on the vdieo and teh thumbnail" · "Do not we have any better durga puja frames to use?" (with a screenshot of shot 9, C168) · "Find differnt indo western fonst"
> Picks: font "Amita"; cover "I: gold Durga in profile"; shot 9 "Yes, swap it in".

What I did:
1. **Title** (`tools/make_title_v7.py --style amita`): "Kolkata / the city of / CULTURE, HERITAGE AND SURPRISES". Amita Bold (Google Fonts, OFL) for "Kolkata", Tiro Bangla Italic for "the city of", Eczar SemiBold caps for the last line; cream with a soft dark band so it reads on the bright record. Shown: 4 western styles (Didot, Bebas, Futura, Bodoni), then 6 Indo-western (Rozha One, Yatra One, Galada, Eczar, Amita, Teko; `analysis/ig_v7b/covers/round7_*options.jpg`). Fonts in `assets/fonts/` with their OFL licences.
   - On V5 of `Reel_kolkata_v8`: `renders/overlays/title_v8_amita.png` replaces `title_kolkata.png`, same 7.76–10.56 s and the same settle keys (opacity 0 → 100 over 0.16 s, scale 104 → 100 over 0.4 s, blur 12 → 0 over 0.32 s), read back identical (`analysis/_es_title_v8.jsx`).
2. **Durga pool:** every strong Durga / pandal frame in the Pujo footage (`analysis/round7_durga_pool.jpg`, 13 clips A–M).
3. **Shot 9 (27.48–29.52)** → **Oct 15 C076**, the sculpted gold Durga in profile (Shakti Stambha pandal), copied to `raw/selects/Oct15_A001_10150524_C076.mov`. Camera 18.26–20.30 s (its sharp stretch; the clip ends at 20.32), 1080p vertical at Scale 100, y 1000, 25 fps. Handheld sway (proxy jitter 2.7 → 12 px toward the end) → **Warp Stabilizer**, smoothness 50, analysed (auto-scale 103.3 %).
   - The 9 → 10 Cross Dissolve is now **5 frames ending on the cut** (733–738): C076 has no picture after its out-point, so Premiere won't centre a 10-frame one. Starting the shot 5 frames earlier would open the accent on motion-blurred frames.
4. **Cover:** `deliver/kolkata_v8_cover.jpg`: C076 at 19.4 s with the Eterna 3510 LUT at 30 % (the reel's look, by ffmpeg) and the Amita title lower down; full 9:16, so the 3:4 grid crop has no black band.
5. **Caption:** the Durga line now reads "a gold Durga sculpted in profile on 15 October"; alt text and `PACKAGE.md` updated.
- **Sequence:** `Reel_kolkata_v8` (v8b export) (54a7d1e7-996f-40ca-8338-aa9783ece7c5), a duplicate of v7. Map `analysis/edl_v8.json`. Master `renders/masters/kolkata_v8_master.mov`, delivery `tools/deliver_v8.sh`.
- **Pregate v8: FAIL** (`analysis/pregate_v8/`), blur dips:
  - **title shot, 5.76–7.40 and 7.80–8.00:** the frames before the title are unchanged from v7b (render_diff: changes only from 7.8 s). They now read "soft" only because the larger title raised the shot's sharpness median; 7.8–8.0 is the designed 0.32 s focus-pull. → marked designed (`--designed 5.68-8.1`).
  - **shot 9, 27.56–27.64:** the camera's own motion blur 2–3 frames after the cut (C076 18.34–18.42), plus 29.36–29.44 inside the dissolve. → **fixed:** C076's only sharp stretch is 18.48–20.30 (1.82 s), so After Effects Timewarp (Pixel Motion) plays it at 88 % to fill the 2.04 s slot (`analysis/ae_jobs_v8.json` → `renders/ae/v8_C076_gold_durga.mov`, 52 frames, no ghosting by eye, sharpness ≥ 0.74 × median until the dissolve). Warp Stabilizer again (smoothness 50, auto-scale 103.1 %). The dissolve is re-made: Cross Dissolve 733–739 (6 frames, ending a frame after the cut); `--designed 29.32-29.52`.
- **v8b:** master `renders/masters/kolkata_v8b_master.mov`, delivery `tools/deliver_v8b.sh` (prev = v8, map `edl_v8.json`; `edl_v8_build1.json` = the v8 map).
- **Review v8b** (`analysis/review_v8b.md`, Fable 5.1, focused on the title and shot 9 vs v7b): **PASS**, 2 minors. Answers:
  1. **The caps line sat on the cartridge's "MMC 20 E" label** → **fixed (v8c):** `title_v8b_amita.png`, the block raised ~95 px (top of "Kolkata" at y 426) and the caps line +15 % (Eczar 39 px); checked over 7.85 / 8.6 / 9.4 / 10.45 s, clear of the label throughout. Same keys (`analysis/_es_title_v8c.jsx`). The cover re-rendered with the same type.
  2. **Shot 9 is ~27 % softer than the camera** (88 % Pixel Motion), visible only at 2× → **accepted**, told to the director.
  - Bookkeeping fixed: `edl_v8.json` title overlay → `title_v8b_amita.png`; shot 9 carries `camera` / `camera_in` / `camera_rate`.
- **v8c:** master `renders/masters/kolkata_v8c_master.mov`, delivery `tools/deliver_v8c.sh` (prev v8b).
- **Review v8c** (`analysis/review_v8c.md`, the final focused check of the title fix): **PASS.** Minors, accepted (the gate's loop cap; told to the director):
  1. the caps line clears the label but rests on the cartridge's soft top edge (0–20 px) — shippable; if wanted, raise another ~25–30 px;
  2. the caps line is only +3 % (cap height 23 → 24 px), not +15 %: `make_title_v7.py` shrinks any line wider than 840 px, and Eczar 39 px with 5 px tracking was wider, so it fell back to ~36 px.
- **Deliverables (v8c):** `renders/exports/kolkata_v8c_mix.mp4` (−14.0 LUFS, −1.4 dBTP; post this), `renders/previews/kolkata_v8c_phone.mp4`, `deliver/kolkata_v8c_POST.mp4`, `deliver/kolkata_v8_cover.jpg`, `deliver/caption.txt`, `deliver/PACKAGE.md`.

## Phase 9 — Retro (2026-11-08)
Director: "Approve, do retro" (v8c and the package). `retro.md` written and copied to `studio/retros/kolkata.md`. New CRs from the retro: CR-20261108-kolkata-cover-title-type, CR-20261108-kolkata-stock-intake, CR-20261108-kolkata-late-round-edits (12 kolkata CRs in all). Status → done.

## Posting (2026-11-08)
- Director: "Set it up now". Files: `deliver/kolkata_v8c_POST.mp4`, `deliver/kolkata_v8_cover.jpg`, `deliver/caption.txt`.
- **AirDrop is the director's step:** the computer-use Finder grant refuses Share and AirDrop ("they pass the document or selection to other applications"). Finder's `deliver` window was left open with both files selected.
- **Audio:** the director asked whether the song should come from Instagram instead of being baked in. Options: baked only; baked + library song at volume 0; Instagram's song with a re-cut (name back, +2.6 s drift). → **Chosen: our baked mix, plus "Kolkata" from the IG library at volume 0** for the credit and the audio page; check the preview before Share.
- **Prepared in Instagram (iPhone Mirroring, 2026-11-08 18:10–18:29), stopped before Share:**
  - the video `kolkata_v8c_POST.mp4`; the director widened Photos access to the two files themselves (Manage → Select More Photos);
  - audio: "Kolkata" (Anupam Roy, Shreya Ghoshal) from the IG library attached, **music volume 0**, clip volume 100;
  - consent notice "Others can now download and share your reels": the director chose **Allow** (Continue);
  - cover: `kolkata_v8_cover.jpg` from the camera roll; the profile-grid crop shows the face and the whole title;
  - caption: typed key by key from `deliver/caption.txt`, checked screen by screen; emoji omitted (Mirroring can't type them). Symbols `: ( ) " # @` and capitals all came through (the reality doc says shifted symbols fail: not on this run);
  - location: "Kolkata - The City of Joy" (Kolkata, West Bengal); Location Services left off;
  - Add AI label **off**; Audience Everyone; Trial off; Upload at highest quality on; "Also share on…" shows the director's Facebook profile (left as Instagram had it).
  - **No alt-text field for reels** in this Instagram version (More options has only Translate reel).
  - Instagram's last step is an "About Reels" sheet whose button is Share; I opened it once by Next and cancelled.
