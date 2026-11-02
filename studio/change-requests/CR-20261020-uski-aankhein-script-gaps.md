# CR-20261020-uski-aankhein-script-gaps

| Field | Value |
|---|---|
| From reel | `projects/uski-aankhein/` |
| Arch version | 0.6.0 |
| Type | script · skill |
| Severity | workaround |
| Status | partly done (v0.7.0, v0.8.0) |

## What happened
Phase 0–2 of a music-montage pilot where the soundtrack is the reference's own audio, the footage is a 5-shoot pool, and one stock clip is used as a blended layer.

1. **`teardown.py` needs `--ours`, but the skill doesn't pass it.** Skill Phase 1 says `teardown.py --ref <ref> -o …` ("measure the references"). The script errors without `--ours` (`usage: teardown.py [-h] --ref REF --ours OURS -o OUT`), so there's no reference-only mode.
2. **The beat analyser can't read a video file.** `gemini_audio_and_beat_analyzer.py --music references/Video-14732.mp4` fails with `soundfile.LibsndfileError: … Format not recognised`. That's the common case when the soundtrack is a reference reel's audio (puja-night-2, pujo-ki-asolei-sobar and this reel).
   - The beat grid also reports beats inside a near-silent stretch: "beats" every 0.6 s through 4.8–7.7 s, where RMS falls to −48 dB. The 4.18–19.02 s section got labelled one "intro".
3. **The survey can't see camera pans.** The survey said Oct17 C168 had its "face centred ~2.1 s". A 10 fps strip showed it's a pan at about 0.3 frame-widths per second, with the face centre at x 0.68 at 2.05 s. The payoff plan (a hold) had to become a sweep + freeze. Mid-frames and 3-frame contact sheets can't show this.
4. **No 9:16 reframe preview.** Eye-line-locked framing (every idol's eyes on the same screen line) needs per-shot crop centre, crop size, crop-follow over time and freeze. No studio tool previews a crop from a 4K vertical source.
5. **`conform_clip.py` only centre-crops to 9:16.** The stock clip (1280×720 landscape) only works as a full-width band across the eyes (Screen blend): 1280 → 1080 wide is a downscale, so it stays sharp. A 9:16 crop of 720p is a 2.67× upscale and loses the bow. There's no crop-offset or "band / keep landscape" option.
6. **No `drawtext` in this Mac's ffmpeg** (`No such filter: 'drawtext'`), so labelled contact sheets with timecodes fail. **No `cv2` in `.venv`**, so face/eye tracking was done with a slow numpy matcher.

7. **Reframe/motion in Premiere is the riskiest step for this kind of reel.** Eye-line-locked crops, pushes, crop-follow and a freeze on clips that need frame-rate interpretation all run into reality-doc gaps: opacity keyframes don't render on interpreted clips, Motion keyframes are in media time, freeze/hold isn't scriptable, and stills scale by default.
8. **Reference-look tuning:** forcing per-band colour ratios from a reference with different content (a warm skin close-up vs orange idols) pushed shadows to B ×2.1. My first `.cube` also mapped pure black to 0 while near-black went to 0.03.
9. **Titles:** every reel rebuilds the same focus-pull title through the full `/motion-graphics` loop; pujo-ki-asolei-sobar's composition was reused here by copying it.

10. **`verify_render.py --fix-loudness` only acts when loudness fails.** A mix at −14.1 LUFS with a −0.1 dBTP true peak (an SFX on a music accent) got no fixed copy. Called with an empty path, it also wrote `_VERIFY.md` / `_render-sheet.png` into the current directory (the studio root).
11. **Eye-lock needs measured eye points.** Review gate v1 found the eyes 30–200 px off the planned line because the tracker template was centred on hand-estimated positions. Re-pinning on measured pupils fixed it.

12. **Bake manifests keyed by file name:** replacing the clip in an EDL row left the old bake's entry in `bakes_v2.json`, and the compositor would have blended both into one slot. Key the manifest by EDL row.
13. **No tool finds a reference's source footage** (round 2). The director asked for "the accurate string player" from the reference. Pexels and Pixabay have no esraj, and Google Lens needs an image upload that the browser tool can't do from a file. I injected the crop through a JS `DataTransfer`. No exact match came back; it ended as an AI-generated shot.
14. **Hard-coded last shot in the bake:** `n == 11` and `range(1, 10)` in `bake_v2.py`. Adding EDL rows silently broke the sweep/freeze pairing. Fixed with `last_n` in `tools/bake_v3.py`.
15. **A clamped lock looks like shake.** On C059 the lock crop hit the source edge on every frame (the shrine sits at source ey 0.85–0.94), so the camera's 160 px tilt bob came straight through. `shake_report.py` showed only "14 px RMS"; a per-region motion check found the cause. The bake should report clamped frames per shot.
16. **An eye reference outside the shot window is clamped silently.** In round 2, C208 moved to a shorter slot, and its measured `eye_ref` time (1.933 s) fell outside the new window (0.33–1.50 s). The tracker used the window's last frame with the pupils' coordinates from 0.45 s later, and the lock pinned the wrong point (55 px off).
17. **No subject-vs-IG-UI check.** The C059 shrine (the only lit subject) sat at y ≈ 1657, under Instagram's caption and handle area. `frame_scan.py` checks text safe zones only by eye; nothing measures where the brightest or salient subject sits per shot.
18. **Teardown misses transition types.** `teardown.py` counts cuts but doesn't classify how shots change (hard / dissolve / dip to black / blink-slit / whip / double exposure). The reference's whole transition language (two blinks) went unnoticed for three rounds.
19. **Survey has no place grouping.** Clips from different houses or pandals in one shoot folder looked like "one place". Group by timecode gaps plus visual similarity (idol, architecture), and label each clip's place.
20. **Look previews at 50 % are too subtle to choose from.** Show the current grade as a column, use a strong intensity (~80 %), and letter the columns. Contrast variants must keep black anchored.
21. **Tracker on static shots.** Check global motion first; when the camera is still (< ~10 px over the shot), use a fixed crop instead of a template track, which can drift.
22. **No enlargement cap.** Chasing "tighter" pushed crops of phone 4K to 2.4–3.4× with unsharp, and the director called the result "very bad image quality". The reframe tools should report the enlargement per shot and warn above ~1.5× (or route to an AI upscaler).
23. **No AI upscaler in the studio.** Installed in the reel folder with the director's OK on 2026-10-27: Real-ESRGAN ncnn-vulkan, official macOS release v0.2.5.0 (`realesrgan-ncnn-vulkan-20220424-macos.zip`, 51.8 MB, universal binary). Path `projects/uski-aankhein/tools/realesrgan/`; binary sha256 c1c35d92…b7cc. x4plus on a 534×950 crop takes ~7.6 s/frame on this Mac and recovers eye outlines and lashes that Lanczos smears (`analysis/round5/esrgan_compare.jpg`).
24. **Preview encodes tagged full range.** `previz*.sh` converts to gbrp with out_range=pc and encodes `format=yuv420p` without a range conversion, so the files come out yuvj420p (full range). Phone players can crush or harden them, which may have fed the "bad image quality" note. Fix: `scale=out_range=tv` before the final format, plus `-color_range tv`.
25. **A custom look still needs a manual or on-screen load.** Each custom `.cube` change costs a director click or a full-screen takeover. Premiere in full-screen Space blocks background control, and the macOS Open panel is an XPC process computer use can't click (keyboard works). Options for HQ: bake custom looks into the V1 render, or keep a library of looks installed into Premiere's Creative LUT folder (selectable by index via script?), or document the keyboard path.
26. **Deflicker must be regional, not one gain per frame.** On the pandal's clay face a single lamp beats against 30 fps, so the two cheeks pulse in anti-phase. A per-frame global gain hid the frame-mean flicker (0.83 % → 0.04 %) but left ~1.2–1.6 % on each cheek, which the v9b review caught. Fix that worked: a low-res luma gain field (40 px blocks, softened) matched to its 9-frame moving average, applied per frame (`projects/uski-aankhein/tools/bake_r9c.py`; cheeks → 0.19 / 0.37 %). Suggest: `ingest_report.py`'s flicker measure reports per-region too, and a shared `deflicker.py` uses the gain field.
27. **No double-exposure recipe.** A Screen blend of a bright layer (a white kurta) over a darker face veils the whole shot (p10 0.20 vs 0.07) and puts the layer's centre on the subject's face. The v9 review flagged it as major. Recipe that passed the v9b review (`projects/uski-aankhein/tools/bake_r9b.py` `shot_A`):
    - place the layer off the subject, as the reference does;
    - weight it with a ramp plus a soft hole over the eyes;
    - feather the moved layer's edges;
    - remove its low-frequency veil (inverse Screen of a σ≈32 px blur, 75 %);
    - restore black point and level to the neighbouring shots.

    Suggest: effects-playbook entry + a shared helper.
28. **AI upscaler defaults.** Real-ESRGAN x4plus alone draws small jewellery as blobs and gives filigree a waxy, invented texture. Blend it with the plain denoised Lanczos enlargement (AI ≈ 55 %), and lower the AI share (≈ 20 %) over small specular jewellery. Use one AI still under a push for static subjects; per-frame AI shimmers (v7). Suggest: a shared `ai_upscale.py` with `--mix` and a mask option, documented in `motion-and-ai.md`.
29. **Designed cover by default.** Two reels in a row (pujo-ki-asolei-sobar, uski-aankhein) ended with a designed cover after a frame grab was rejected. Suggest: Phase 8 renders 3–4 designed covers in the reel's title type and grade, with a 3:4 grid-crop check, as one sheet (`projects/uski-aankhein/tools/cover_r9.py` is a working example).
30. **Delivery quality is judged on a phone, not on a Mac.** The approved v9c `_IG` file looked "very poor" on the director's iPhone: soft, plastic faces, blocky darks. Causes:
    - **Encode:** Premiere's "Match Source - H.264 High Bitrate" preset gives Main profile at 9.5 Mb/s.
    - **Picture:** AI upscale + strong single-frame denoise on 1.65–2.5× enlargements of night phone footage.

    Proposals:
    - **(a) Delivery path:** Premiere exports a ProRes 422 master ("Match Source - Apple ProRes 422.epr" works via `exportAsMediaDirect`), and the H.264 is encoded from it with x264 High, CRF 15, tune film, aq-mode 3 (`projects/uski-aankhein/tools/encode_hq.sh`: PSNR 44.3 → 46.4 dB vs the master, worst-frame SSIM 0.967 → 0.989, shadows +2.5 dB). `verify_render.py` should flag Main profile and < 12 Mb/s for 1080×1920.
    - **(b) Phone-scale check:** the review gate and the editor QA look at 100 % crops of faces and darks. `watch.py` could add a 100 % crop sheet per shot.
    - **(c) Real-frame stacks before AI for static subjects:** 21 aligned frames, trimmed mean (`projects/uski-aankhein/tools/stack_r9d.py`).
    - **(d)** Make item 22's enlargement cap (~1.4× for night phone footage) a hard rule.
31. **The studio grain is invisible at the playbook's levels.** `renders/texture/grain_25fps_v1.mov` (uski; its source in `assets/overlays/`) moves (frame diff 7/255) but its amplitude is low (std 6.2/255). Overlay at 6–12 % opacity changes a mid-dark picture by ~0.3/255, so "grain 6 %" has been a no-op in this reel, and probably in others using the same clip. The v10 reviewer caught it ("no moving grain visible"). Suggest: a grain asset normalised to a known amplitude (e.g. std ≈ 20/255) and a playbook level stated as visible amplitude, not opacity; add a frame-diff check to `frame_scan.py` for held/still shots.

## Workaround used in the reel
- (1) Passed the reference as both `--ref` and `--ours`; the ref column is the measurement.
- (2) `ffmpeg -i ref.mp4 -vn -ac 2 -ar 48000 -c:a pcm_s16le references/ref_audio.wav`, then ran the analyser on the wav. Checked the silence by a 0.1 s RMS printout (logged in `project.md`).
- (3) 10 fps full-frame strips of candidate clips, plus a numpy template tracker.
- (4) `projects/uski-aankhein/tools/storyboard.py`. It reads the EDL json (eye centre `ex/ey` as a fraction of the upright source, crop width `cw`, optional `cw_end`/`ey_end` push, `track` [[frac, ex, ey]…] crop-follow, `freeze`) and renders in / mid / out frames through the crop with the eye-line drawn. It caught 4 wrong eye positions and the C168 pan before the director saw the plan.
- (5) Plan: place the stock in Premiere as a scaled band (Scale ≈ 145 %, Position on the eye line), Screen blend by script. No conform crop.
- (6) PIL for labels.
- (7) `projects/uski-aankhein/tools/bake_shots.py`: bakes each EDL row (or the sweep + freeze pair) to ProRes 422 HQ 1080×1920 at the reel fps. It does an explicit BT.709 tv→pc decode, frame-for-frame conform, 180° fix, crop with eased push / crop-follow / freeze from the EDL fields, and baked fades and dips. 10 shots in 55 s. A local previz (`ffmpeg` concat + Screen band + `lut3d` + type + music) then checks timing before Premiere.
- (8) `projects/uski-aankhein/tools/ref_look.py`: band gains clamped to warm-only (R ≥ 1, B ≤ 1), chroma fades to neutral near black.
- (9) Copied `graphics/title` from pujo-ki-asolei-sobar and changed text, y, size and fps.

## Proposed change
- `teardown.py`: make `--ours` optional (reference-only report), or fix the skill's Phase 1 command.
- `gemini_audio_and_beat_analyzer.py`:
  - decode any media through ffmpeg to a temp wav when `soundfile` can't open it;
  - drop beats where RMS is more than 25 dB below the track median, and report those stretches as "silence" sections.
- Survey (`analyze_footage.py` or the pool-survey tool from CR-20261019-pujo-ki-asolei-sobar-pool-survey): add per-clip **camera motion over time** (global shift per 0.25 s: static / pan direction and speed / tilt), so "hold" vs "pan" is known before the EDL.
- Promote `projects/uski-aankhein/tools/storyboard.py` with the pool-survey CR's storyboard, keeping the crop / crop-follow / freeze fields. Add a `scripts/reframe_plan.py` that turns those EDL fields into Premiere Motion keyframes (Scale, Position) so the plan and the timeline match.
- `conform_clip.py`: add `--crop x,y,w,h` (source pixels) and `--band` (fit width, keep the landscape aspect, pad to 1080×1920 with alpha or black) for stock used as a blended layer.
- New `scripts/bake_shots.py` (from this reel's tool) as the default V1 path for crop-heavy reels, plus `scripts/previz.py` (bakes + overlays + LUT + audio → a timing preview before Premiere). Skill Phase 3 then becomes "bake, previz, assemble".
- `ref_look`/`build_look_lut` (see CR-20261020-pujo-ki-asolei-sobar-reference-grade-match): clamp band gains to the look's direction, and fade chroma to neutral at black.
- `assets/graphics/title-focus-pull/`: a studio HyperFrames title template (text, y, size and fps as parameters), so reels don't copy each other's folders.
- `verify_render.py`: make `--fix-loudness` also handle a true-peak-only FAIL (limiter to −1 dBTP), and refuse an empty or missing path instead of writing into cwd.
- Reframe/eye-lock tooling: take the eye point as a measured input (a gridded pupil-picking sheet), and add a post-bake check that measures the eye line per shot.
- (13) `scripts/ref_source_find.py`: frame crops of the reference + reverse image search (Lens/TinEye/Bing) + stock-site queries, with a report of candidates and licences.
- (14) Promote `bake_v3.py` with no hard-coded shot numbers; the sweep/freeze pair comes from the EDL (`pair_with`).
- (18) `teardown.py`: per cut, classify the transition from per-frame luma / difference / band-mask shape (dip, blink-slit, dissolve, hard, flash) and save a full-rate strip around each one; list them in COMPARE.md.
- (19) Pool survey: a `place` field per clip (timecode clustering + idol/architecture similarity), and pick sheets grouped by place.
- (20) `look_preview.py`: `--with-cube current.cube` column, default intensity 0.8 for choice sheets, lettered columns; a `contrast` op that keeps 0 and 1 fixed.
- (21) `track_eyes`: skip tracking when global motion over the window is below a threshold; report drift vs global motion.
- (22) Reframe/bake: log the enlargement per shot; warn above 1.5×; offer the AI-upscale path.
- (23) HQ: adopt Real-ESRGAN into `setup.sh` (pinned release + checksum) and a `scripts/upscale.py` wrapper (crop → x4plus → target size, batch per shot), mentioned in the reality doc and the effects playbook.
- (24) Every previz/export helper: tv-range output, tagged `-color_range tv`; `verify_render.py` should flag yuvj420p / pc range.
- (16) Tracker or reframe tool: when an eye reference lies outside the window, extend tracking to the measured frame and slice (as in this reel's `tools/track_eyes.py`), or fail loudly.
- (17) `frame_scan.py`: per shot, the salient/bright centroid and the fraction of lit pixels inside the IG bottom 320 px / right 120 px zones, flagged when the subject sits there.
- (15) The bake (or the reframe tool) logs per shot how many frames a lock or follow crop was clamped, and by how many px. More than 10 % clamped → warn, and suggest a cw/v that fits (simulation as in this reel's round 2).
- `setup.sh`: install an ffmpeg with `drawtext` (freetype) and add `opencv-python-headless` to `.venv`.

## HQ decision (v0.8.0, 2026-11-01)
- **(a) Delivery path: done.** Premiere exports a ProRes 422 master and `scripts/encode_master.py` encodes from it. `verify_render.py` fails Main profile, < 12 Mb/s and yuvj420p. On goddess v10b, `aq-mode 3` gained nothing over CRF 16 at the same cap (PSNR 42.7 vs 43.0 dB), so it isn't in the default.
- **(1) `teardown.py --ours`: done** in v0.7.0.
- Everything else stays open.
