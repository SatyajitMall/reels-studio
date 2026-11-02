# CR-20261028-we-never-treated-her-like-a-goddess-pilot-notes

| Field | Value |
|---|---|
| From reel | `projects/we-never-treated-her-like-a-goddess/` |
| Arch version | 0.7.1 |
| Type | script · skill · rule |
| Severity | workaround |
| Status | partly done (v0.7.3, v0.8.0) |

First story-montage pilot (external English VO from a reference reel, 409 clips across 8 shoot folders). Phase 0–1 findings; more will be appended as the reel goes on.

## What happened
1. **Transcription, again.** `.vendor/video-use/helpers/transcribe.py` → `Scribe returned 401: … "Invalid API key"` (same as CR-20261019-pujo-ki-asolei-sobar-external-vo-audio). No local Whisper in `.venv`. A fresh `uv` venv with `faster-whisper` failed inside PyAV: `TypeError: open() got an unexpected keyword argument 'metadata_errors'`.
2. **`scripts/link_footage.sh` reference skip misses a spelling.** The pattern `*ref*rence*` skips `Reference`, `Refference`, `References`, but not the Oct 16 folder `Reffernce`. Its reference reel `Video-92015.mp4` was linked into `raw/b-roll/` and analysed as footage.
3. **Ambiguous clip labels.** Overview sheets and most tables label clips by number only (`C033`). The director's cards restart numbering: Oct 15 and 16 share one `Media/` folder (C001–C139), Oct 19, 20 and 21 each restart at C001, and Oct 20's folder also holds Oct 19's clips. `C033` names three different shots.
4. **Missed footage folders.** I listed `~/Documents/Video /` once at the start, linked the 6 folders it showed, and later told the director "none of the shoots has visarjan or a farewell". `Pujo 2026 Oct 21` (Dashami, 57 clips) and `KOLKATA2026` (56 clips) were in the root by then (folder dates 01:54, probably still copying at my first listing). The director corrected it ("Highly incorrect, Oct 21 is Dashami").
5. **Second reel in a row whose soundtrack is another reel's VO.** Round 1 still has no question for it; asked separately, and asked the IG "Use audio" rights question at Phase 1 as the sibling retro advised. Director: "decide later".
6. **`selects_score.py` / `motion_holds.py` key output by clip number** (`C029`), so clips from Oct 19, 20 and 21 overwrite each other in `selects.json` / `motion.json`.
7. **Storyboard + pick sheets again earned their keep** (as in CR-20261019-…-pool-survey): the storyboard caught 3 bad picks before the director saw them.
9. **Cross-project active sequence (Premiere).** After `create_project` with 3 other reels' projects open, `app.project` was the new project but `app.project.activeSequence` (and `verify_premiere_connection().activeSequence`) was still Uski's `Reel_uski-aankhein_v9c`. Tools that act on the active sequence would have edited another reel. Workaround: scripts target the project by path; open our own sequence and re-verify before any sequence tool. Proposed: the verify step refuses mutations when `activeSequence` doesn't belong to `project` (extends CR-20261018-my-reel-premiere-shared-between-sessions).
10. **Bridge dropped during export:** `execute_extendscript` returned `bridge_unavailable` while `exportAsMediaDirect` ran; the file was written and one `verify_premiere_connection` brought the bridge back. The script's result file was lost; the export was checked against a Premiere still. Proposed: run exports through a wrapper that writes the result file before calling the encoder, and polls for the output.
11. **Storyboard / pick sheets should overlay the IG safe zone** (top 220, bottom 320, right 120 px) on 9:16 tiles: shot #8 passed Checkpoint 1 with its subject under the caption zone and was only caught at the rough-cut still check.
8. **`muted_red` greys gold idols.** At the playbook's tolerance (12, or 25 for saffron), a gold Durga turns silver-grey (sheet `analysis/looks_r2/`). At `--red-tolerance 45`, gold and red stay and blues/greens still mute: sat 0.54 → 0.50 (vs 0.39 at 25). The director picked the 45 version.
12. **Kodak 5218 film looks aren't scriptable presets.** `getAllLumetriPresetsList()` (Premiere 26.5.2, 325 names) has the Fuji-negative looks (`Fuji F125 Kodak 2393`, `Fuji Eterna 250D Fuji 3510`, `Fuji Reala 500D Kodak 2393` …) but **not** `Kodak 5218 Kodak 2383`, `Kodak 5218 Kodak 2395` or `Kodak 5205 Fuji 3510`. The effects-playbook film table lists those three (and `muted_red`, `cinestill`) as `applyLumetriPreset` names. They're Creative → Look dropdown entries, not presets.
13. **`colour_report.py` hue depends on exposure.** The midtone sample (luma 0.15–0.85) changes when a shot is brightened, so mean hue moves without a colour change (C181: 28.6° → 22.6° with R−B 0.31 → 0.26 from a +0.5-stop lift and Basic Sat 85).
14. **Look and Leave Color can't be built by script on Premiere 2026.** Lumetri's `Look` property (idx 34/35) is a dropdown index, not in file order (7 = "Blue Intense"). The first write loaded that look, but later writes changed only the number and the panel kept the first look. QE's effect list (138 names) has none of the After-Effects-ported effects (Leave Color, Change Color, Channel Mixer…), so `muted_red`'s Leave Color can't be added by script; only `Color Pass` (full grey, RGB similarity, no amount) is there. A 3rd manual step for the director: pick the Look, drag Leave Color on; everything else is set by script.
15. **Manual adjustment layer missed on the first try** with 4 projects open: it landed nowhere the DOM could see, then appeared in our panel on the second try. One project open at a time would avoid it (CR-20261018-my-reel-premiere-shared-between-sessions).
16. **Leave Color is gone from Premiere 2026** (not just unscriptable): the Effects panel has no Leave Color anywhere (Color Correction holds ASC CDL, Brightness & Contrast, Lumetri Color, Tint, Video Limiter; Legacy has none). `muted_red` in the film table and story-montage playbook names an effect that doesn't exist. Built natively instead: Lumetri **Hue vs Sat** on the V3 layer, 100 % within ±45° of red, ramp to 46 % by −65° / +62°, all other hues 46 %. Checked against the `look_preview.py` muted_red tile: cool shot sat 0.31 → 0.16 (preview) vs 0.26 → 0.16 (ours); cast change matches. The curve (Lumetri idx 58) and the Creative tint wheels are binary blobs, so this is a UI step (computer use or the director).
17. **Pillow can't shape Bangla.** The studio `.venv` Pillow has no raqm (`features.check('raqm')` → False), so Bangla vowel signs render in the wrong place (আসছে comes out with ে after ছ). `render_type_cards.py` and any PIL card renderer will misspell Bangla / Devanagari, which the story-montage playbook asks for (thank-you card in the local language, native-language words). Workaround here: HTML card rendered by headless Chrome with a transparent background (`--default-background-color=00000000`, 1080×1920, scale 1).
18. **Mono VO plays 3 dB low.** The external VO was extracted mono (`-ac 1`) in Phase 1. Premiere pans a mono clip on a stereo track at −3 dB per channel, so the export measured −17.4 LUFS against the reference's −14.4, and nothing flagged it until the Phase 6 measurement. Fixed by re-extracting stereo (`-ac 2`, identical timing) and swapping it on A3 at −0.8 dB (−15.2 LUFS, −1.6 dBTP).
19. **ES3 reserved word as an object key** (`{in: …}`) fails the whole `$.evalFile` with only the generic "ExtendScript execution failed via CEP evalScript()", and the result file isn't written. A one-line ping script showed the bridge was fine.
20. **`verify_render.py` reads an end card on black as black frames.** Small text on black (0.86 % of the frame lit) is under blackdetect's 98 % threshold, so a designed end card FAILs "black frames" unless `--fade-end` is raised to the card's length (here 2.4).
21. **`teardown.py` pacing on our export:** 3 "flashes" at 0.04, 2.36 and 20.24 s were gold filigree moving under camera pushes (frame diff 27–32 per frame, no glitch frame); "first cut 0.04 s" is one of them; "longest shot 4.12 s" includes the end card; one real cut (21.64 s, similar luma) went undetected. The comparison flags were all artefacts.
22. **Setting `TrackItem.end` doesn't move the source out-point.** Rolling a cut forward by script (`A.end = later`) left the clip 2.08 s long on the timeline with only 1.76 s of source (`outPoint` unchanged, speed 1). It needed `A.outPoint` set too. The MCP `roll_edit` does exactly `A.end = …` and nothing else, so it has the same gap. `B.start` + `B.inPoint` on the following clip worked.
23. **Whisper word onsets can be 0.3 s early after a pause.** "feels" (L7) was placed at 25.74 s; the speech band shows silence 25.51–26.02 and the onset at 26.05. The cut and the subtitle card were planned on the Whisper time, so they landed 8 frames before the word. The director's rule is 0 to −2 frames. The review gate caught it; my own QA didn't, because it checked cuts against the same Whisper times. Several other cuts sit 3–4 frames early for the same reason.
24. **"Real camera push" in the Phase 1 motion read was an in-camera zoom in bursts** (C145: steps at 2.60, 3.20, 3.60, 4.04 s, static 4.32–6.24, a 30 % burst at 6.28–6.56). The hook window ended inside the burst and the eyes shot (#14) inside a tilt that accelerates from 11.20 s. Both read as a lurch into the cut. Fixed by slipping both windows to end before the move. `motion_holds.py` / the cut plan don't report where a camera move starts inside a chosen window.
25. **Shots didn't show their lines, and nothing in the pipeline caught it.** The director's first look at v1: "in a lot of places the footage does not match the transcript, or the essence of the transcript". Examples: "we dress her" over an already-dressed idol, "we cry" over a boy seen from behind, a rickshaw-puller close-up for "the city we are familiar with", while the pool held many Boron shots of women touching Ma's face, better Bhashan and many Kolkata shots. The Phase 2 picks came from a shortlist (`selects.md`, pick sheets by theme), not a line-by-line search of all 409 clips. Two blind review-gate passes checked craft and brief compliance and passed every one of these shots: the reviewer's checklist has no "does this shot show its line?" item.
26. **Framing and grade judged "off" by the director on v2.** v2 placed every 4K clip at fit (Scale 50): wide records, phones and clutter at the edges, subjects small, against a reference that frames close on faces, hands and Ma. The primary grade was tuned to numbers (sat ≤ 0.55, R−B, luma) and turned the orange pandals pink-magenta. Fixed in v3 by a per-shot crop plan (magnification 1.2–1.8×, centre on the subject, subtitle band kept off faces; previewed with ffmpeg crops before Premiere) and a grade judged by eye on a one-frame-per-shot stills sheet. A second in-camera zoom burst (C094 2.28 s, +1 for item 24) was caught by the director at 0:04.
27. **`frame_scan.py` misses smear inside a reframed shot.** It measures sharpness on the whole frame, so handheld smear magnified by a 1.5–1.8× crop (C045 at 4.24–4.80, C002 at 21.0–21.64, C007's focus drift) passed the scan and was found by the reviewer's own per-frame pass. This reel's `tools/best_window.py` scores every frame *inside the crop actually shown* (Laplacian variance + frame difference) and ranks windows by their worst frame; it picked the steadier windows for C002 and C007.

28. **`shake_report.py` reads a stabilised shot as still shaky.** C045 after Warp: whole-frame jit 12.6 → 10.0 px (Smooth Motion) and 10.0 again with No Motion, which suggested Warp had barely helped. Measured inside the crop actually shown (sub-pixel phase correlation, residual after a quadratic path), the wobble was 8.1 → 0.9 px RMS. The whole-frame number is dominated by things that aren't camera shake: the V5 subtitle swapping mid-shot, people moving at the frame edge, and the push.
29. **Warp can't fix the motion blur that shake leaves.** After stabilising C045, 11 frames (2.96–3.40) stayed at 0.4–0.5× the shot's median sharpness: a soft pulse on a now-steady image. Fixed by moving the cut onto the next word onset (3.00, before "the") so those frames drop out; the director had said only "it's shaky".
30. **"Quality" complaints from people the sample was shared with.** The file passes every check (9.2 Mb/s, no upscaled shot, blockiness below the reference). The visible limits were the source (8-bit night iPhone footage at 1/50 handheld), 1.2–1.8× crops, the 10 % grain, and likely the messaging app's re-encode. The studio has no guidance on how to share review copies, or on what Instagram does to grain.
31. **Night settings drifted from the shooting guide, and the ingest check didn't flag it.** The director suspected the Blackmagic Cam source (`projects/we-never-treated-her-like-a-goddess/analysis/quality_r5/SOURCE.md`), and the files themselves are sound: no defect, full 4K in Premiere, no proxies. But of the 18 shots:
    - 7 were shot at 1/33 or 1/25 s, against the guide's 1/50;
    - 12 were at ISO 200–500 at night;
    - 2 were at 1/60;
    - all were 8-bit HEVC.

    The phone's noise reduction smears fine detail, and the 1:1 crops (Motion scale 100 on vertical 4K) show it at full size. `ingest_report.py` flags 8-bit and flicker, but not "shutter slower than 1/fps×2" (motion blur) or night ISO. Phase 3 has no rule against 1:1 crops on soft night clips.
32. **Keyframed properties read back as their un-keyed default.** `property.getValue()` on a keyframed Motion Scale returned 100 for five clips whose keys were 80–93.6. That made me report five "1:1 crops" to the director, and item 31's list named the wrong five. `getValueAtKey(getKeys()[i])` gives the real values.
33. **No high-bitrate H.264 export route.** "Match Source - H.264 High Bitrate" gives 9.2 Mb/s at 1080×1920. No script-loadable preset goes higher, and custom `.epr` files can't be authored by script.
    - Workaround in this reel: a Premiere "Match Source - Apple ProRes 422" master (10-bit 4:2:2), then `ffmpeg libx264 -preset slow -tune grain -crf 16 -maxrate 20M -bufsize 40M -profile:v high -g 50`, BT.709 tags and AAC 320k.
    - Result: 18.9 Mb/s, `verify_render.py` PASS. Encode time is 13 s for 30 s.
34. **Baked look in Premiere: the old V3 grade must go fully, not just Look Intensity 0** (v6, HQ's `shot_look.py --full` bakes).
    - With the Look at 0 and the vignette off, the round-1 Hue vs Sat curve (reds/golds 100 %, other hues 46 %) was still active.
    - It desaturated #1 C010, the green night-foliage shot, from 0.39 to 0.24 and warmed its shadows and mids by R +0.03. C035, C002 and C100 lost 7–11 % saturation as well.
    - Found by exporting a Premiere still with V3–V5 muted: V1 alone matched the bake within 0.009.
    - Fixed by turning every V3 Lumetri section switch off except Creative, which holds the Sharpen.
35. **Premiere and ffmpeg disagree by one frame on a 24.94 fps clip interpreted at 25 fps** (C056, avg 10500/421, r 299/12; timestamps at a 0.04 s step with 0.042 s jumps).
    - ffmpeg's frame index puts the in point (2.20 s × 25 = frame 55) one frame later than Premiere shows. The offset is constant through the shot (NCC at 4 points).
    - The 25 fps and 30 fps clips agree.
    - Compensated at placement. A bake whose in point isn't on a frame boundary (C029, 4.70 s at 25 fps) also needs `floor`, not `round`.
36. **The director approved the halfway baked look from stills, then rejected it on the full reel** (same day). This matters for HQ's plan to make the baked look and the quality fixes studio defaults.
    - On v6b: "EVERYTHING DOES NOT LOOKS OVER PROCESSED INSTEAD OF LOOKING HD".
      - Measured cause: the Premiere Sharpen 20 + grain 4 % roughly doubled high-frequency energy vs the bake alone.
      - Removed in v6c.
    - On v6c: "the colours are all over the place, the things hardly look natural".
      - Cause by eye: the look muted gold to olive-grey (C143 sat 0.61 → 0.39) and turned the LED street olive.
      - The per-shot auto WB/cast drifted on foliage (#1) and LED light (#15). Fixing those took manual overrides.
    - **Chose:** the earlier per-clip warm-gold Premiere grade (v5e), with **no sharpen and no grain** (v7).
    - **For HQ:**
      - Preview a look on the **whole reel in motion** (or every shot's still) before calling it approved; four stills didn't predict the other 14 shots.
      - Don't default to added sharpening or grain on night iPhone footage.
      - The bake's auto WB needs a guard where the frame is dominated by foliage or coloured light.
    - Tools left in the reel: `tools/bake_tune.py` (per-shot overrides), `tools/colour_ab.py` (3-way colour sheet with spread numbers), `tools/process_ab.py` (processing A/B).
37. **Absolute brightness targets (round 9: luma ~0.40, no 2-s window under 0.30) burnt night shots** (round 9d, director on v9c: "0:22 is burnt, 0:10 … weird not natural colour palette").
    - To hit 0.30 on a pandal interior that the camera recorded at 0.17, the grade needed +3 EV: colour channels hit 255 on 2–7 % of five shots, and lifted night skies and water read as muddy khaki.
    - v9d/v9e grade against the camera instead: no channel at 255 beyond lamps (≤ 2 %), saturation within ±5 % of the camera at the same framing, night shots allowed under 0.30 (C017 0.21, reel mean 0.37).
    - Lumetri's Saturation slider is steep on dark, low-chroma shots: on C020, 96 → 105 moved HSV saturation 0.43 → 0.52 (+21 %). Tune it on stills, a few points at a time.
    - **For HQ:** write grade targets relative to the camera file (luma ratio, saturation and clip vs source), with an absolute floor only as a warning; add an any-channel-255 check to `verify_render.py` or the gate.
38. **Speed-changed clips: the DOM's in/out are in source time ÷ speed** (round 10, Premiere 26.5.2).
    - After QE `setSpeed(0.5532, ticks, false, false, false)` on C051 (src 4.00–5.04), `inPoint`/`outPoint` read 7.2308 / 9.1108. Writing `inPoint = 4.00` (raw source seconds) moved the source in to 2.21.
    - Fix: read source = DOM × `getSpeed()`, write DOM = source ÷ speed; Motion keys use the same DOM time.
    - QE `setSpeed` with a longer duration extends into an empty gap; on C035 it stopped at 91 of 98 frames, so set `end` after it and re-check.
    - **Motion keys on a speed-changed clip don't follow either:** Scale keys set at the DOM in/out (56→60, 62→56) rendered as a partial ramp (C051 still 56 at mid-shot; C035 62→58.5). Pre-rendered slow motion at 100 % avoids it (v10b).
    - **For HQ:** add both to `premiere-mcp-reality.md` (speed row), plus the slow-motion recipe used here: remove the neighbour without ripple, `move()` the clip, `setSpeed` with the target duration, `setTimeInterpolationType(2)`, re-key Motion.
39. **Premiere Optical Flow on 25 fps night crowds fails review; AE Timewarp at 4K passes the same checks better** (round 10).
    - Premiere OF: blend fall-back frames (77–91 % blend-like) with doubled arms and hands, plus a sharp/soft pulse on every synthesised frame (alternation 0.20–0.33 vs 0.05–0.08 real).
    - Compared on the same windows: ffmpeg `minterpolate` (mci/aobmc/bidir) 0.095 / 0.16; AE Timewarp Pixel Motion 0.087 / 0.108, the fewest bad frames. Both remove the double images at 1:1.
    - **Rotation:** this camera writes 3840×2160 with a −90° display-matrix flag. I fed AE pre-rotated 4K ProRes trims with ½-s handles; `frame_match` and an NCC timing check passed. `ae_roundtrip.py` hasn't been tested on rotation-flagged sources.
    - `ae_roundtrip.py` can't set Timewarp's Vector Detail; the reviewer asked for 100. Default was used.
    - **For HQ:** make AE Timewarp (4K comp, the jobs file's `width`/`height`) the default slow-motion route for 25 fps footage in effects-playbook §C, with Premiere OF only for calm shots. Add a `vector_detail` option and auto-rotation handling to `ae_roundtrip.py`. Consider `tools/r10_slowmo_metrics.py` (alternation + blend share) as a slow-mo check, noting that blend share runs high on any slow motion.
    - The reviewer measured why: a correct half-step in-between reads 64 % blend share at 2 px of motion. Its proposed slow-mo bar: no frame > ~70 %, mean within 20 points of real; half-res alternation within 0.03 of real; the fastest element single at 2× (`analysis/review_v10b.md`, `analysis/review_v10b/tools/synthetic.py`).
40. **External VO, 3rd reel: this time the reference's IG audio was "Original audio"** (@whoisnovonil), so "Use audio" carries the voice. The `_IG` upload file is the picture with only our natural sound (A3 muted on a duplicate sequence). Supports CR-20261019's "check the audio page at Phase 1": here the director answered it at export.

## Workaround used in the reel
- `projects/<reel>/tools/asr_words.py`: faster-whisper `medium.en` with word timestamps, audio decoded by ffmpeg to a float array (sidesteps PyAV). 30 s VO in ~2 min including the model download; wording checked against the reference's burned-in subtitles.
- Removed the mislinked reference symlink by hand and noted it in `raw/SOURCES.md`.
- `projects/<reel>/tools/cand_table.py`: ingest facts keyed `night:Cnnn` (night from the real path); `tools/picksheet.py`: pick sheets keyed by full file stem.
- Re-listed the root, linked both folders, analysed the 113 new clips into `analysis/new/` and `analysis/ingest_new/` (separate output dirs, so the first 15 overview sheets aren't overwritten).

## Proposed change
- **effects-playbook film table:** mark the `Kodak 5218 …` / `Kodak 5205 …` looks as "Look dropdown only, not a preset", and give the scriptable route once a reel verifies one (setting the Look slot by script, or a one-click manual step).
- **reality doc + film table + story-montage playbook:** `muted_red` = Look picked from the dropdown + **Hue vs Sat curve** (keep ±45° of red, others 46 %), both by UI (director or computer use); then intensity 35 / vignette by script. Leave Color doesn't exist in Premiere 2026. Say so in the Round 2 look options.
- **`render_type_cards.py`:** install Pillow with raqm (`brew install libraqm` + rebuild Pillow) and fail on complex scripts when it's missing, or render local-script cards through headless Chrome / HyperFrames.
- **`colour_report.py`:** report hue on a fixed sample (e.g. pixels whose source luma is in range), or flag gold hue only when R−B / G−M moved too.
- **Setup:** install `faster-whisper` in `.venv` and make `scripts/gemini_transcribe_fallback.py` (or `transcribe_reel.sh --file`) use it, decoding with ffmpeg as above. Add a `setup.sh` check that calls Scribe once and says plainly when the key is rejected.
- **`scripts/link_footage.sh`:** skip any directory whose name matches `ref*` case-insensitively (or a list: `ref*`, `*reference*`, `*refference*`, `*reffernce*`), and print what it skipped.
- **`scripts/analyze_footage.py` / `ingest_report.py` / `selects_score.py` / `motion_holds.py`:** key and label clips by full stem or with the shoot date and number (`10-20 C033`, from the `A001_MMDD…` stem) on overview sheets and in tables.
- **Skill Phase 1:** "List the footage root again right before saying a shot type doesn't exist" (and the `find_footage.sh` already proposed in CR-20261019-…-pool-survey).
- **Skill Phase 0, Round 1, Q1:** add "Is the soundtrack an existing audio (song, or a reel's audio with a VO)?" (+1 occurrence for CR-20261019-…-external-vo-audio).
- **story-montage playbook, Colour:** on festival footage with gold idols, start `muted_red` at tolerance ~45 (keeps gold, mutes blue/green), and say so in the look table.
- **Skill Phase 1 (external VO):** extract the reference audio in stereo (`ffmpeg -i ref.mp4 -vn -ac 2 -c:a pcm_s16le`), never `-ac 1`; Phase 6 measures the timeline's loudness against the reference before setting levels.
- **reality doc:** "ES3: reserved words (`in`, `class`, `default`, …) can't be bare object keys; a syntax error fails `$.evalFile` with the generic CEP message. Ping with a one-line script before suspecting the bridge."
- **`verify_render.py`:** an `--end-card <s>` option (or detect lit pixels in "black" runs: a run with text above, say, 0.3 % of the frame is a card, not black); the skill's Phase 7 command passes it when the brief has an end card.
- **`teardown.py`:** stop pacing at `--end-card` / the last fade to black, and only count a flash when the frame after differs from both neighbours (A→B→A), not on sustained high-detail motion.
- **reality doc + MCP fix list:** to roll a cut by script, set `B.start`, `B.inPoint` (later clip) then `A.end` **and** `A.outPoint`; read back that timeline length equals out − in for both. Flag `roll_edit` as ⚠️ (doesn't move the out-point).
- **Cut planning (talking-head / external VO):** after Whisper, refine every planned cut onset with a speech-band envelope (300–3400 Hz, 5 ms hop: first frame > floor + 12 dB after the pause) and plan cuts on that; `pack_transcripts.py` or a small `onsets.py` could write it next to the word times.
- **`motion_holds.py` / Phase 2 EDL:** for every chosen source window, print per-frame global motion (scale + shift) and flag any move that starts or accelerates in the last 0.5 s before the out-point.
- **Skill Phase 2 (VO / talking-head over B-roll):** for every line, search the whole pool for the shot that *shows* it (literal first, then essence), and put 2–3 candidates per line on a storyboard sheet with the line under each frame for Checkpoint 1. Not a themed shortlist.
- **`reel-reviewer` checklist, Edit:** "For each line of VO or caption, does the shot on screen show what the line says (literally, or its essence)? A shot that only shares the topic is a major." (A reviewer miss the director caught → review-gate.md Learning.)
- **Skill Phase 3 / playbook (vertical 4K footage):** a "framing pass" after the rough cut: for each shot choose magnification and centre on the subject (faces, hands, the idol's face), keep the caption band clear of faces, crop edge clutter (phones, cut-off heads); preview as ffmpeg crops on a sheet before setting Motion. Default is not fit-to-frame.
- **Grade QA:** colour_report numbers are a check, not the target; every grade pass ends with a one-frame-per-shot stills sheet judged by eye against the reference frames.
- **Motion scan tool:** a `scripts/zoom_scan.py` (per-frame global scale + shift by phase correlation, flags steps > 1.5 % or > 3 px) run on every source window at selection and on the export; this reel's scratch version found every burst the director and the gate caught.
- **`frame_scan.py`:** accept the Motion crop per shot (scale / position from the sequence, or a crops JSON) and measure sharpness / frame change inside it; add a window finder like `tools/best_window.py` to Phase 3 / 5 for every reframed shot.

- **`shake_report.py`:** accept the Motion crop per shot (as proposed for `frame_scan.py`, item 27), mask the V5 caption band, and report wobble as the residual after a smooth (e.g. quadratic) path *inside the crop*. Skill Phase 5: judge Warp by that number, not by the whole-frame one.
- **Skill Phase 5 (stabilise):** after Warp, run a per-frame sharpness pass inside the crop. Blur from the original shake survives stabilisation; drop those frames (slip, or move a cut onto the nearest word onset or beat) or flag them to the director. Warp by script works on this Premiere version: QE `addVideoEffect`; analysis starts by itself; Framing = 0 (Stabilize Only) keeps the approved crop when the crop margin covers the correction.
- **Review copies (skill Phase 7 / Checkpoint 2):** tell the director to share review copies as a file or Drive link (WhatsApp "Document" or HD), not as an app-compressed video. Before the IG export, propose grain ≤ 5 % (or none) on night footage, and a higher-bitrate master (~16–20 Mb/s) for Instagram's re-encode; mention IG's "Upload at highest quality" setting.
- **`ingest_report.py` + shooting guide (item 31):**
  - Flag `shutter slower than 1/(2×fps)` as motion-blur risk.
  - Flag ISO ≥ 200 on night clips as "noise reduction smear: avoid 1:1 crops".
  - Print a per-night settings summary the director can check against the guide after each shoot.
  - Skill Phase 3 framing pass: keep night clips at Motion scale ≤ ~75 on vertical 4K (≥ 1.3 source px per output px) unless the director asks for closer.
- **Reality doc (item 32):** "Read keyframed properties with `isTimeVarying()` → `getKeys()` / `getValueAtKey()`; `getValue()` returns the un-keyed default (e.g. Scale 100)."
- **Skill Phase 7 export (item 33):** make the ProRes master → x264 encode a studio script (e.g. `scripts/encode_master.py`, with the settings above) and the default for every `_mix` / `_IG` export. Keep Premiere's H.264 preset for quick previews only.
- **Baked-look route (items 34, 35), when HQ promotes `shot_look.py`:**
  - The Phase 4 "swap to bakes" step should make V3 sharpen-only: all Lumetri section switches off except Creative.
  - Check every placed bake against an ffmpeg reframe of the bake: NCC alignment at −1/0/+1, plus a Premiere still with the upper tracks muted.
  - Compute `--in` as `floor(in × fps)`.
  - Measure the frame offset of any non-25/30 fps clip at placement.

## HQ decision
**Items 8, 12, 14, 16 accepted, v0.7.3 (2026-10-29), with the director's go-ahead.**
- **12, 14 (looks):** HQ checked Premiere's own `Resources/LocalizedPresets/en_US/Effect Presets/Lumetri Presets.prfpset`. It agrees with this reel's live check: only the five Fuji-negative looks are presets. The film table now gives each look's route (**preset** by script, or **dropdown** by the director), with the preset spelling. The skill, the reality doc and CLAUDE.md now say never to write the `Look` slot by script.
- **16, 8 (`muted_red`):** Leave Color is replaced by the Lumetri Hue vs Sat recipe this reel verified, which is a UI step, with the reel's render check recorded. Tolerance 45 is the start point on footage with gold idols (effects-playbook §A3, story-montage Colour, `look_preview.py --red-tolerance` help).
- **Intensity:** the CLAUDE.md V3 row defers to each look's §A3 value (`muted_red` 35 %).
- **Still open:** items 1–7, 9–11, 13, 15 and 17. The reel is still in progress, so more items may be added.

## HQ decision (v0.8.0, 2026-11-01)
**Items 26, 30, 33, 36, 37, 38 and 39 (except its `vector_detail` option) accepted, v0.8.0, with the director's go-ahead on Batch A of the v0.8 plan (`studio/plans/v0.8-plan.md`).**
- **36, 37 (grade):** camera-true is the default grade (effects-playbook §A0). Each shot is judged against its own camera file at the same framing by the new `scripts/camera_fidelity.py`; the round-9 absolute targets are reported, never aimed at. A baked look is not a default.
- **26 (framing):** ≥ 80 % of the camera width, Scale ≤ 62.5 on vertical 4K (effects-playbook §B, SKILL Phase 3).
- **30, 33 (delivery):** a ProRes 422 master, then `scripts/encode_master.py` (H.264 High, CRF 16, ≤ 20 Mb/s, and a ≤ 29 MB phone copy). `verify_render.py` now fails Main profile, < 12 Mb/s and yuvj420p.
- **38, 39 (slow motion):** reality-doc rows for the speed-changed in/out points, the Scale keys and Optical Flow. After Effects Timewarp at camera size is the slow-mo default; `ae_roundtrip.py` feeds AE an upright trim of rotated phone clips.
- **34 (partly):** SKILL Phase 4 says to disable an inherited V3 layer and its Hue vs Sat curve when there's no look.
- **Still open:** 1–7, 9–11, 13, 15, 17–25, 27–29, 31, 32, 35 and 40, most of them planned in Batches B and C; and from 39, a `vector_detail` setting for the AE `timewarp` op (backlog).
