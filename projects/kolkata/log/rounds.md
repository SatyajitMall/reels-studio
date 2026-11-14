# KOLKATA — rounds log (moved out of project.md on 2026-11-07, when it passed 4,000 words)

Rounds 0–1 and Phase 1, verbatim. The current state is in `project.md` (`## Now` and Rounds 2–3).

## Round 0 — Interview

### Round 1 answers (2026-11-04)
| # | Question | Answer |
|---|---|---|
| 1 | What is it? Anyone speaking? | "Go through the reference video I just added." After the teardown: **music montage like the reference, no VO** → `music-montage`, playbook `cinematic-montage` |
| 2 | Footage | `KOLKATA2026 /Media 1` (Oct 24–25) **and** `KOLKATA2026 /Media` (Oct 31) |
| 3 | End feeling | **Be inspired / nostalgic** |
| 4 | Length | **Whatever the story needs** (the guide audio caps it; see open question 2) |
| 5 | Branding | Handle @satyajitmall (profile). Type: **reference's marigold-yellow serif + red drop shadow**, this reel only |
| 6 | References | `references/ref_north_kolkata.mp4` (added by the director; copy of `~/Downloads/Frames from North Kolkata - October 2025…Howrah.mp4`) |
| 7 | Soundtrack | **Same song as the reference, added in Instagram at upload** → guide-copy route. IG audio page not checked yet (needs the reference's link) |
| – | Audience | **Bengalis, home and abroad** |

### Reference teardown: `ref_north_kolkata.mp4`
Measured with `teardown.py` and `analyze_footage.py --reference` (`analysis/teardown/TEARDOWN.md`, `analysis/references/`), watched at 1 fps (`analysis/references/watch/`).
- **File:** 1280×720 **landscape 16:9**, 24 fps, 35.08 s, AAC stereo 44.1 kHz. Caption credits a Fujifilm X-T3, edited in DaVinci Resolve. Our reel is 9:16, so its compositions are a feel reference, not framings to copy.
- **Pace:** 13 shots, 20.5 cuts/min, average 2.7 s, median 2.62 s, shortest 2.04 s, longest / first cut 3.88 s. No flashes, no 1–2 frame transitions: hard cuts, fade out at the end. Motion mean 9.97 (p90 14.2): mostly locked or slow handheld holds, the subject's own movement carries it.
- **Picture:** luma 0.297 (dark-ish), contrast 0.737, saturation 0.298, warm (R−B +0.076). Warm, soft film look; night shots kept dark.
- **Sound:** −14.1 LUFS, LRA 10.4 LU, true peak −0.7 dBTP. The song is **"Jaane Woh Kaise Log The" (*Pyaasa*, 1957)** (vocals identified by local Whisper; lyrics not reproduced here). Quiet start: the vocal enters at about 3.7 s.
- **Type:** "October 2025" small serif top-left; "Frames of" small over a huge "Calcutta" in marigold-yellow serif with a red offset drop shadow, over the record close-up (~3.9–6.5 s); a one-line quote with attribution at the bottom in small yellow serif. No other text.
- **Shots, in order:** (1) old man in a radio/record shop placing a vinyl, 0–3.9 s · (2) close-up hands on the turntable + title card · (3) Vidyasagar Setu at sunset, country boat · (4) two boys and a dog on the ghat, Howrah Bridge behind · (5) Howrah Bridge at dusk, lit ferry, silhouettes on the ghat · (6) Victoria Memorial, sun flaring through a tree · (7) painted lane with mirror / frame art · (8) smoky market lane, porter with a basket on his head · (9) flower market, roses and marigolds · (10) wall with hammer-and-sickle and Bengali writing, street beyond · (11) Howrah Bridge at night, a man in the river · (12) tram interior at night · (13) tram window on the night city, fade out.
- **What it means for us (to confirm in Round 2 / the brief):** median ~2.6 s per shot (the playbook's own rule: take the reference's median), so a calm arc rather than the festival reels' 1.6–1.8 s; hard cuts; probably no swishes (no fast motion to sell); a day → dusk → night arc; people at work and city landmarks one subject per shot; a title card over an early close-up.

## Phase 1 — Footage analysis (2026-11-04)
- **Linked** (not copied) 101 clips into `raw/b-roll/` (`raw/SOURCES.md`). Copy the shortlist into `raw/` once chosen (director profile).
- **Ingest** (`analysis/ingest.md`): Blackmagic Cam, HEVC 8-bit Rec.709, ~58 Mb/s. 97 clips at 25 fps → **sequence 25 fps**. C108 / C110 (24.917) and C109 (24.833, VFR) conform by interpretation. C036 claims 50 fps but averages 23.1 with 224 dropped frames: no slow-mo headroom anywhere. Flicker: none at risk. Jumps: C102 at 4.96 s, C028 at 10.92 / 11.44 s (keep the placed windows clear). Casts: the Oct 25 river group (3750 K, 31 clips) reads cool / green → warm + magenta in the primary. Nov 1 night (C038–C046) is mostly black (luma ≤ 0.05).
- **Guide audio**: `audio/guide_ref_stereo.wav`. Beat grid (`analysis/audio_summary.md`): 95.7 BPM, 1 bar = 2.508 s, beat until 28.86 s, accents 0.12 / 5.22 / 8.43 / 13.51 / 17.39 / 19.92 / 25.66 / 28.86. The reference's 12 cuts (3.88, 6.29, 8.96, 11.00, 13.75, 16.79, 19.17, 21.67, 24.38, 27.00, 29.42, 32.00) sit 1.1–1.3 s after the detector's downbeats every time. Either the detector's bar phase is off by half a bar or the editor cut on the sung phrases. The vocal lines start at ~3.7, ~14.0 and ~24.2 s (Whisper), matching cuts 1, 5 and 9. **Plan on the reference's cut times**; the director checks by ear.
- **Selects / motion**: `analysis/selects.md` (290 moments), `analysis/motion.json`.
- **What the pool holds** (upright, by eye):
  - **Oct 25, day → sunset:**
    - river: ferries at the jetty C059–C060, rowing boat C061, Vidyasagar Setu C064–C067, moored boats C068–C070;
    - Chandpal ghat steps C071–C074, riverside walk C075–C076, Chandpal ferry ghat sign C077–C078;
    - **Howrah Bridge walkway POV** C081–C085 (people walking: C083), river sunset through the railings C086–C089;
    - Eden Gardens floodlight tower at blue hour C090–C091, scooter POV rides C092–C095, Writers'-style red façade from the scooter C096–C098, **yellow Ambassador taxi** C100–C101;
    - **College Street bookstalls** C103–C106 (bookseller faces: C106), Dakshineswar temple from the river C108 / C110, **Indian Coffee House** interior C111–C114, **Uttam Kumar** film-strip mural C115–C117.
  - **Oct 31, dusk:** Maidan football C001–C007, Maidan roads C008 / C011, Eden floodlights C012–C013, a monument C014–C016 (180°), kids C017–C018, a bus with crowd at sunset C019–C021, **trams** (parked) C025–C027, **chai pot steaming** C028, a tram interior C029–C030, **Academy of Fine Arts at night**, crowd C032–C034.
  - **Nov 1:** **St Paul's Cathedral at dusk** C035–C037, night clips C038–C046 too dark.
- **Unusable:** C058 (laptop test), C024, C031, C080, C102, C009, C010, C038–C046. C109 is a 54 s ferry ride, mostly railing blur: check for a usable window.

## Round 0 — Interview, Round 2 answers (2026-11-04)
Shown: `analysis/framing/framing_sheet.jpg` and the look sheets: `analysis/looks/looks_sheet.png` (3 looks at 30 %), `film_a` / `film_b` / `film_c` (all film stocks at table intensity), `starter_luts_sheet.jpg`, `effects_sheet.jpg`. Stills: C065, C106, C006, C033, C100.

| # | Question | Answer |
|---|---|---|
| 1 | Framing of the landscape clips | **C: 4:5 window** (recommended) |
| 2 | Look (first round: camera-true / 500T→2395 / 250D→3510 / F125→2393) | "Find other LUTs and effects" → second round of sheets → **"film stack"**: camera colour + soft bloom / mist + vignette + grain 5 % |
| 3 | Effects on top | **Vignette, grain 5 %** (both already in the film stack). Grain stays off the night shots (§A4) |
| 4 | Pace | **Exactly the reference** (one shot per bar, ~13 shots) |
| 5 | Story order | **Day → dusk → night** (recommended) |
| 6 | Title | **"Calcutta"** |
| 7 | Stock for missing shots | Director, mid-round: "a few appropriate shots you might not find in the footage, find them from stock videos online, they should match the footage I recorded". Then: "whatever is missing, including the opening shot" |
| – | Captions | none (music-montage default: title card + end card) |

**Overrides this reel will carry in the brief:**
- 4:5 window instead of ≥ 80 % width (CR filed).
- One shot per bar for the whole reel, against the playbook's energy-arc rule: the director's explicit choice, matching the reference.
- **Stock as whole shots, including the opener**, against the profile's "stock as a layer or bridge, never for the subject". The director asked for it on this reel; each stock clip is labelled in the brief and picked by the director.
- Title type: a reference-style serif instead of the playbook's DIN Condensed cream.

## Round 1 — Proposal (2026-11-05)
Stock: the director said "use your strong picks" → 5 Pexels clips downloaded to `raw/stock/` (285 MB, `raw/SOURCES.md`). Brief: `brief.md` (draft v1). EDL: `analysis/edl_v1.json`. Storyboard: `analysis/storyboard_v1_p1.jpg` + `_p2.jpg`. Preview: `renders/previews/kolkata_p1.mp4` + `kolkata_p1_phone.mp4` (28.1 MB). Window matte and title made with the reel-local `tools/make_overlays.py`.

**Hook options**
1. **(Recommended, in v1)** Stock vinyl close-up (Pexels 6742732, src 2.0 s): the stylus riding the record, push 62.5 → 66 %, 6-frame fade in. The song's intro "plays" from it. Cut at 3.88 s (first sung line, ~3.7 s) to "Calcutta" over the chai steam (Oct31:C028).
2. Own footage only: open on the boatmen rowing (Oct25:C061, src 4.0 s, hold) with a slow push, "Calcutta" at 3.88 s over the chai. No stock in the first 6 s.
3. AI-generated Kolkata gramophone shop (an old shopkeeper lowering the needle), like the reference's opener. Veo draft ≈ $0.12, final ≈ $0.40, labelled AI-generated; only if the director wants that exact image.

**EDL v1** (34.96 s, 874 frames, 25 fps; all shots in the 4:5 window; hard cuts; no SFX; guide audio on A3)
| # | clip | in | out | text / action | V1 move | V2/V5 | transition out | SFX |
|---|---|---|---|---|---|---|---|---|
| 1 | Stock 6742732 vinyl | 2.00 | 6.05 (1.043×) | – | push 62.5→66, pos x −110 | matte | cut 3.88 | – |
| 2 | Oct31:C028 chai | 0.50 | 2.90 | **"Calcutta"** 3.88–6.28 | push 62.5→65, rot −90 | title + matte | cut 6.28 | – |
| 3 | Oct25:C061 boat | 4.00 | 6.68 | – | push 62.5→65, rot −90 | matte | cut 8.96 | – |
| 4 | Stock 40180894 Howrah, river | 5.00 | 6.02 (50 % slow-mo) | – | held, pos y 1000 | matte | cut 11.00 | – |
| 5 | Oct25:C106 bookseller | 0.50 | 3.26 | – | held, rot +90 | matte | cut 13.76 | – |
| 6 | Oct25:C111 Coffee House | 0.00 | 3.04 | (2nd sung line) | push 62.5→65, rot −90 | matte | cut 16.80 | – |
| 7 | Stock 39276190 flowers | 3.00 | 4.18 (50 %) | – | held | matte | cut 19.16 | – |
| 8 | Oct25:C100 taxi | 1.00 | 3.52 | – | held, pos y 860 | matte | cut 21.68 | – |
| 9 | Oct31:C007 Maidan | 1.50 | 4.22 | – | push 62.5→65, rot −90 | matte | cut 24.40 | – |
| 10 | Oct31:C030 tram | 1.00 | 3.60 | (3rd sung line) | push 62.5→65, rot −90 | matte | cut 27.00 | – |
| 11 | Stock 38386435 Victoria | 3.00 | 5.03 (0.833×) | – | held | matte | cut 29.44 | – |
| 12 | Stock 38584444 Howrah blue hour | 2.00 | 4.13 (0.833×) | – | held | matte (no grain from here) | cut 32.00 | – |
| 13 | Oct31:C033 Academy night | 0.50 | 3.46 | – | push 62.5→65, rot −90 | matte | fade to black 22 f | – |

**Runtime:** 34.96 s.

**Pregate (p1 phone copy, `--profile ig-quiet`):** verify_render PASS, frame_scan PASS (3 flags inside the fades). camera_fidelity FAILs on every shot because it ignores the window bars and the rotation (CR item 6). Checked by eye on `analysis/pregate_p1/fidelity/fidelity_sheet.jpg`: the render matches the rotated camera frames. Watched at 1 fps (`analysis/watch_p1/`): all 13 shots upright and in the window, the title readable, the cuts on the plan.

## Round 1 — Director notes (2026-11-05)
- **Approved** brief v1 + EDL v1 as previewed (`kolkata_p1_phone.mp4`): "Approve, build it". No changes. The opener stays the stock vinyl (hook option 1); no date line or quote.

## Round 1 — Changes made / Phase 3 rough cut (2026-11-05)
- Project `premiere/kolkata.prproj` (saved-as from the director's new project; the only project open). Scratch disks → `premiere/`.
- Bins `01_A-Roll` … `06_Music`; imported 8 own clips (`raw/selects/`), 5 stock, 2 overlays, grain, guide WAV (ExtendScript `importFiles`).
- Stock conformed by interpretation to 25 fps: vinyl 23.976 → 1.043×, Victoria / Howrah blue hour 30 → 0.833×, Howrah river / flowers 60 → **0.4167×** (every frame once). The preview used 0.5× for the 60 fps shots: a little slower in the build.
- `Reel_kolkata_v1`: 1080×1920, 25 fps (from C028, then `setSettings`), 6 video tracks (V1 shots · V2 spare · V3 adjustment layer · V4 grain · V5 title · V6 window matte) and 3 audio tracks (A1 camera sound muted · A3 guide). Built by `analysis/_es_build_v1.jsx`: frame-exact starts 0, 97, 157, 224, 275, 344, 420, 479, 542, 610, 675, 736, 800 → 874. Rotations, Scale (62.5 rotated / 50 vertical), Position and push keys read back as planned.
- Dip to Black (QE): 0–6 f and 852–874 f.
- Read-back: `get_timeline_gaps` shows only V5 0–3.88 s (the title starts at 3.88, as planned). 13 mid-shot stills from Premiere (`renders/stills/`) match the preview: upright, in the window, title on S2.
- Shot map: `analysis/map_v1.json` (in-points snapped to frames: 0.50 → 0.52, 1.50 → 1.52; clips → `raw/selects/`).

## Round 1 — Phase 4 colour (2026-11-05)
- **Adjustment layer** (director's manual step) on V3, 0–874. It landed in the `06_Music` bin (the bin that was selected), so I moved it to `03_Graphics`.
- **A1 primary** (`analysis/_es_colour_v1.jsx`, one Lumetri, by occurrence): only **C061** (3750 K under daylight) gets Temperature +10, Tint +5. Render check: R−B −0.155 → −0.126, G−M +0.034 → +0.024. Every other clip is camera-true: no Lumetri. C007's "green cast" is the grass, not a cast. C106 / C111 keep the recorded warm light.
- **Vignette** (V3 Lumetri: Amount −0.9, Midpoint 40, Feather 70). Render check: window edges 7–15 % darker, centre luma unchanged.
- **Grain** V4: `gemini_film_grain_16mm.mp4` interpreted 30 → 25, looped 6–736 f (off on S12–S13), Overlay (19), opacity 5 %. Barely measurable (hf detail +0.3 on S1 / S3), as intended at 5 %.
- **Soft bloom** (`analysis/_es_bloom_v1.jsx`), built **in Premiere instead of After Effects glow**: a copy of each V1 shot on V2 (same item, in-point, Motion and push keys) with one Lumetri isolating the highlights (Exposure −2, Contrast 100, Shadows −100, Blacks −100; C061's primary copied), Gaussian Blur Amount 20, Screen (22) at 30 %. The copies' linked audio on A2 is removed.
  - The first try (Exp −1, Contrast 60, blur 40, 40 %) added +0.04–0.05 luma and doubled p02: hazy, washed. Tuned to the approved effects-sheet mist tile (which measured luma +0.003–0.017, p98 +0.014–0.016): now luma +0.009–0.020, p98 +0.001–0.019, saturation −0.002…−0.03.
  - Stills: `renders/stills/v1_*` (camera framing, no colour) · `v1c_*` (primary + vignette + grain) · `v1e_*` (+ bloom, current).

## Round 1 — Phase 5–7 finishing + export (2026-11-05)
- **Title** (V5): focus-pull settle over the first 10 frames (opacity 0 → 100, Scale 104 → 100, Gaussian Blur Amount 30 → 0), keyed in source time. No HyperFrames: the PNG title + Premiere keys are the final.
- **Sound:** guide on A3 only; no SFX (brief); A1 camera sound muted.
- **Master:** `renders/masters/kolkata_v1_master.mov`. ProRes 422 10-bit 4:2:2, 34.96 s, `exportAsMediaDirect` with Match Source ProRes 422 (36 s to render). Audio present: max −0.8 dB.
- **Deliverables:**
  - `renders/exports/kolkata_v1_mix.mp4` (H.264 High, guide baked; audio loudnorm-limited to −1.4 dBTP, −12.9 LUFS, because the reference audio peaks at −0.7). **Archive only, never posted.**
  - `renders/exports/kolkata_v1_IG.mp4`: the same picture with silent audio, for upload. The director adds the song in Instagram with "Use audio" from 0:00. `verify_render --profile ig-quiet` FAILs "audio present: silent". That's intended here (no natural sound, and the IG audio is added in the app).
  - `renders/previews/kolkata_v1_phone.mp4` (28.0 MB, the review copy, with the limited mix audio).
- **verify_render:** mix PASS (bitrate WARN 9.8 Mb/s at CRF 16), phone PASS, IG see above.
- **Pregate** (`analysis/pregate_v1/`, `--no-fidelity`): verify PASS, frame_scan PASS (2 flags inside the fades), watch sheets written. The camera check was skipped: it can't handle the window or the rotation (CR-20261104 item 6).
- **Review gate:** `reel-reviewer` on Fable (editor Opus), full review, report → `analysis/review_v1.md`.

## Round 1 — Review gate
**v1** (`analysis/review_v1.md`, Fable, full review): **FAIL**, 4 majors + 6 minors. Answers:
| # | Finding | Answer |
|---|---|---|
| 1 | major: S7 flowers judder, every 4th frame a repeat | **fixed:** the Pexels file holds 45 real fps in a 60 fps container. Source de-duplicated (mpdecimate, 451 of 603 frames) → `renders/stock/flowers_dedup_25.mov`, every frame once (0.556×). v1b: 59 of 59 frames unique |
| 2 | major: S5 bookseller AE ramp +28 % | **fixed:** src 1.12 s (raw settles by 1.6 s, dips at 3.9 s). v1b range 4.4 % |
| 3 | major: S6 Coffee House AE ramp −24 % | **fixed:** clip too short to skip the drift → Lumetri exposure counter-keys (V1 + the V2 bloom copy), two passes. v1b range 5.1 % |
| 4 | major: S13 Academy AE ramp −22 % | **fixed:** src 3.4 s. v1b range 1.6 % |
| 5 | minor: vignette 28–32 % at the corners | **fixed:** Amount −0.9 → −0.5 (the profile's "natural, never processed") |
| 6 | minor: frame 0 grey, last frame 10 % | **fixed:** black PNG on V7 with opacity keys instead of Dip to Black. v1b frame 0 and the last frame are 10-bit black (64) |
| 7 | minor: title over the chai-wallah's chest, not the steam | **intended (ask at Checkpoint 2):** legible, face clear; the brief text was updated to "over the chai stall" |
| 8 | minor: red celosia clipped (source) | **intended (ask):** it's in the Pexels source |
| 9 | minor: masked pedestrian on Victoria | **fixed:** src 12.5 s (empty path, dome centred) |
| 10 | minor: tram near-black (camera-true) | **intended (ask):** matches the camera; offer a +10–15 shadow lift |

v1b: new master/exports `kolkata_v1b_*`, shot map `analysis/map_v1b.json`, script `analysis/_es_fix_v1b.jsx`. Pregate v1b PASS (diff: same structure, audio identical). `_mix` PASS. `_IG` FAILs "silent" by design. Focused review: `analysis/review_v1b.md` → **PASS**. All majors verified fixed; audio bit-identical to v1; the unchanged shots differ only by the vignette. New minors for the director:
- A: vignette at −0.5 is still present (corners 0.73–0.92 of the camera);
- B: S11 Victoria, a blown lamp globe cut by the left edge for the first ~1.2 s (fix: src ≈ 13.5 s).
Carried: #7 title placement, #8 red flowers, #10 dark tram.

## Round 2 — Director notes (2026-11-05, on v1b)
Verbatim: "what music are we planning to use? where is the frames matching the story line I see gaps - feel I have more usable footage - also do we do more creative research on which song to pick based on the footage we have, also can we use a couple of pooja footage the best quality one that is"
1. Unsure which music is planned (v1 = the reference's song, *Pyaasa* 1957, added in IG).
2. The frames don't follow a storyline; "gaps" between the shots and the story.
3. More usable footage exists than v1 uses.
4. Research the song choice from the footage we have.
5. Add a couple of the best-quality Pujo shots.
→ Treated as a **re-brief of music + story** (not a fix round): song research, story options, unused pool and Pujo shortlist are presented before any re-cut. v1b stays as the rollback.
- Shown: `analysis/pool_unused.jpg` (75 unused usable clips, upright) and `analysis/pujo_picks/picks_sheet.jpg` + `PICKS.md` (12 ranked Pujo shots, by a read-only subagent from the earlier reels' analyses).
- **Answers (2026-11-05):**
  - Song: "research more" → `analysis/song_research.md` (6 options; recommended Chandrabindoo "Amar Shohor").
  - Story: **day → dusk → night** (kept).
  - Pujo: **#2 Oct21:C035**, women in lal-paar saris dancing at a ghat (in the goddess final as shot 7).
  - Length: **45 s**.
  - **Song (2026-11-05): "Amar Shohor", Chandrabindoo** (sung by Anindya Chatterjee). It replaces the reference's song. Route: Instagram library audio added at upload, so the director must (1) confirm it's in IG's audio picker and (2) put an owned copy in `projects/kolkata/music/` as the cutting guide. One continuous ~45 s section; the IG start timecode goes in the brief.
- **v2 shot pool (draft, untimed; final order and count once the song's phrases are known, ~16–18 shots):**
  - Day, river: Oct25:C061 boatmen · stock Howrah from the river (40180894) · Oct25:C083 Howrah walkway, people · Oct25:C072 ghat steps · Oct25:C064 Vidyasagar Setu
  - Day, streets: Oct25:C097 red façade from the scooter · Oct25:C093 scooter POV · Oct25:C100 yellow taxi · Oct25:C106 bookseller · Oct25:C103 Book Exchange · Oct25:C111 Coffee House · stock flowers (de-duplicated) · Oct25:C115 Uttam Kumar mural
  - Dusk: Oct31:C007 Maidan football · Oct25:C090 Eden tower at blue hour · Oct31:C030 tram interior · Oct31:C026 old tram · stock Victoria at dusk · Nov1:C037 St Paul's · stock Howrah at blue hour
  - Night: **Oct21:C035 lal-paar saris dancing (Pujo)** · Oct31:C033 Academy at night (ending)
  - **IG library: confirmed** by the director (2026-11-05, "Done, it's there"). The guide copy is not in `music/` yet (the folder is empty, and none was found in Downloads, Desktop or Music).
  - Open: the vinyl opener came from the old-song idea. With "Amar Shohor", open on the river morning instead (proposal at Checkpoint 1b). The title "Calcutta" stays unless the director changes it.

## Round 2 — Proposal (2026-11-05)
- Song section **1:14.72 → 1:59.28** of "Amar Shohor" (44.56 s; IG start 1:14.7). Chosen from the energy curve and the vocal map (Whisper: the title line at 60.0 s, refrains at 103.0 / 106.1 / 109.1 / 112.2 s, again at 195–202 and 238–248 s). The alternative 3:11.6–3:56.2 starts in chorus 2.
- `analysis/edl_v2.json` (17 shots, bar downbeats), storyboard `analysis/storyboard_v2_p1/_p2.jpg`, preview `renders/previews/kolkata_p2_phone.mp4` (28.2 MB, camera colour, guide baked).
- Pregate p2 (`--profile ig-quiet`, `--no-fidelity`): frame scan PASS; verify FAILs true peak −0.7 dBTP (the guide song's own peak, not an issue in a preview; fixed by limiting the `_mix` as in v1b).
- Framing check: C115 → **C117** for the mural (C115's window showed only film strips; C117 at 3.4 s shows Uttam Kumar + the lettering, picture slid up to y 660).
- Clips added to `raw/selects/`: C064, C083, C096, C093, C117, C027, Oct21:C035.

## Round 2 — Changes made / Premiere build v2 (2026-11-05)
- Director: "Approve, build v2". `Reel_kolkata_v1` cloned → **`Reel_kolkata_v2`** (694e4a9a-2eb2-43da-80b0-c908c8ee9212); v1b stays untouched as the rollback.
- Imported C064, C083, C096, C093, C117, C027, Oct21:C035 and `audio/amar_shohor_guide.wav`; C083 / C096 (25.001 / 25.008 fps) interpreted to 25.
- `analysis/_es_build_v2.jsx`: 17 shots on V1, bloom copies on V2, A1 primaries (C061 temp +10 / tint +5; **C035 tint +6** for its green cast), C111 exposure keys. V3 / V6 extended to 1114 f; grain 6–885 f; title 77–154 f with the settle; black fades 0–7 / 1092–1114; song on A3. Read-back: V1 17, V2 17, A2 empty, all frame-exact.
- The song's in-point first read back 74.68 s (1 frame early, confirmed by cross-correlating the master against the guide) → re-placed; now **74.720 s**, verified the same way.
- Master `renders/masters/kolkata_v2_master.mov` (44.56 s, song peak 0.0 dB) → `renders/exports/kolkata_v2_mix.mp4` (limited: −1.4 dBTP, −12.4 LUFS, PASS), `kolkata_v2_IG.mp4` (silent, for upload), `renders/previews/kolkata_v2_phone.mp4` (28 MB). Shot map `analysis/map_v2.json`.
- Pregate v2 PASS (verify, frame scan; fidelity skipped, CR-20261104 item 6). Review gate: a fresh Fable reviewer, full review → `analysis/review_v2.md`.

## Round 2 — Review gate
**v2** (`analysis/review_v2.md`, a fresh Fable reviewer, full review): **FAIL**, 1 major. Picture side passes: a hand-rebuilt camera check puts every shot within ±0.006 luma of its camera file, all 17 cuts within ±0.5 frame of a downbeat, song offset 74.720 s. Answers:
| # | Finding | Answer |
|---|---|---|
| 1 | major: music stops dead under the 22-frame picture fade | **fixed:** A3 Level keys fade to silence over the last 22 frames (master RMS falls −13 → −71 dB) |
| 2 | minor: master audio at 0 dBFS (1,907 full-scale samples) | **fixed:** A3 −2.5 dB; master peak −2.5 dB |
| 3 | minor: flowers cooler than the source as seen (R−B −0.045) | **fixed:** the old dedup file had mixed tags (bt709 matrix, bt470bg primaries, smpte170m transfer), so Premiere decoded it as 601. Re-rendered `flowers_dedup_25_709.mov` with all tags BT.709; export R−B 0.535 vs source-as-seen 0.536 |
| 4 | minor: Coffee House dim (held at the camera's settled level) | **intended (ask at Checkpoint 2):** camera-true; offer a +0.3 EV lift to its opening level |
| 5 | minor: bookseller lunges out of frame in the last 8 frames | **fixed:** bookseller 1 bar at src 1.6 (19.96–21.52), taxi 3 bars (15.32–19.96) |
| – | note: party-poster faces top-right in the taxi shot | **ask** at Checkpoint 2 |

v2b: `_es_fix_v2b.jsx`, master/exports `kolkata_v2b_*`, map `analysis/map_v2b.json`. Pregate v2b PASS. `_mix` PASS (−1.4 dBTP, −12.4 LUFS). Focused review → `analysis/review_v2b.md`: **PASS**. All four fixes verified; outside the changed spans the largest frame difference is 0.81 (encoder noise). One new minor for the director: the taxi is now a 3-bar hold (4.64 s), so the energy dips a touch mid-chorus; offer to swap its third bar for a 1-bar street shot.

## Round 3 — Director notes (2026-11-06, on v2b)
Verbatim: "The song does not match the storyline and the footage. I want the footage to be better and accurate. I actually want to do more research on the songs and the types of songs that can be used. So there's how is the architecture for researching about songs? Can we think on the lines of those architecture, please, and build the architecture of researching songs as per the reference video provided, but it should not exactly follow the reference or copycat the reference, but use it as just as a reference."
1. "Amar Shohor" doesn't match the storyline or the footage.
2. The footage should be better and more accurate (shots that show what the song says).
3. Research songs and song *types* properly.
4. Build an architecture for song research based on the reference, using it only as a reference, never a copycat.
→ The studio has no song-research step (an architecture gap). Worked around in the reel: `research/SONG_RESEARCH_METHOD.md` (7 stages, story first) + **CR-20261106-kolkata-song-research** for HQ. v2b stays as the rollback.
- **Stage 3 answers (2026-11-06):** story **"a Bengali far from home"**, language **Bengali**, era **any**, matching **mood only**. Criteria + 6-beat spine: `research/criteria.md`.
- **Stage 5:** long-list research handed to a web-research subagent → `research/longlist.md` (18–25 verified candidates, a ranked top 8, no lyrics quoted).
- **Stage 6 tool:** `tools/song_fit.py` (BPM / half-time feel, shots per footage hold, best continuous section vs the target arc, vocal density by Whisper). Validated on the two known songs (`research/fit_test/`):
  - "Amar Shohor" 152 BPM = half-time 3.16 s bars, best window 73.2–119.3 s (≈ our 74.72 pick), **vocals 12.6 words / 10 s, longest gap 1.3 s**: dense singing, which explains why it felt busy against held shots;
  - the *Pyaasa* guide (35 s) is too short for a 45 s window.
- **Stage 5 result:** `research/longlist.md`: 22 verified songs, a ranked top 8, 14 set aside, with sources (no lyrics quoted). Top 8:
  1. "Agomonir Gaan" (Anupam Roy, 2019; dedicated to Bengalis abroad missing Pujo, the title means "calling someone home"; spot-checked: SVF);
  2. "Ghore Pherar Gaan" (Moheener Ghoraguli, *Khyapar Gaan* 1999, by Gautam Chattopadhyay; spot-checked: Wikipedia);
  3. "Purano Sei Diner Kotha" (Tagore 1885, Hemanta / Kishore / Srikanto recordings);
  4. "Coffee Houser Sei Addata" (Manna Dey 1983);
  5. "Ore Neel Doriya" (Abdul Jabbar, *Sareng Bou* 1978);
  6. "Abar Bochhor Koori Pore" (Rupankar, 2022);
  7. "O Nodi Re" (Hemanta, 1959);
  8. "Apur Paayer Chhaap" (Arijit Singh, *Apur Panchali* 2014).
  - IG-library availability is unknown for all of them: the director checks in the app.
- **Director on the top 8 (2026-11-06):** "find better" / "try other". What was missing: **a more cinematic sound**. Focus: **Bangla indie / acoustic**. → Second pass (subagent) → `research/longlist_2.md`: cinematic, sparse-vocal Bengali indie / acoustic songs of longing and home.
- **Second pass result (17 songs, top 6):**
  1. "Chiltey Roud / O Ki Ekbar Ashiya" (Arnob & Ripon Kumar Sarkar, Coke Studio Bangla S1, 2022; spot-checked; reviewers call its yearning romantic);
  2. "Nodir Kul" (Ripon / Arnob, CSB S2, 2023; river and water; the theme is uncertainty, not home);
  3. "Shantiniketan" (Anupam Roy, *Byatha Nei* 2026; homesickness for remembered places, spot-checked; the video is an unrequited love story);
  4. "Meghpeon" (Debayan Banerjee, *Grihapravesh* 2025);
  5. "Esho Amar Shohore" (Meghdol, 2018; the city is Dhaka; opens on a VO);
  6. "Boipoka" (Anupam Roy, *Chandrabindoo* 2025; the closest story, bright not swelling).
  - #1, #2 and another are Coke Studio Bangla, the same show as puja-night-2's "Shondhatara". None shows an IG Reels signal.
- **Director asked (2026-11-06) for Instagram statistics, analytics and trends.** The Instagram MCP failed to connect this session, and the installed Instagram plugin is a comment channel, not analytics. Offered: iPhone Mirroring (read Insights + the trending audio list, with the director's OK), screenshots, or an API set-up via an HQ CR.
- **Director suggested "Mayabee"** for the audition (likely the 2025 single composed by Srabon Habib, 3:16; to confirm). iPhone Mirroring blocked twice (denied, then computer control off in Settings); waiting on the director.
- **2026-11-07: IG data read** (iPhone Mirroring, full-screen control, read-only) → `research/ig_insights.md`; gate results appended to `research/longlist_2.md`. Mayabee is by **Blue Touch** (Dhaka), not the Srabon Habib release first found.
- **Director approved the audition of 3 (2026-11-07):** Shantiniketan, Chiltey Roud, Mayabee. Asked for owned copies in `projects/kolkata/music/`.
- **Audition built (2026-11-07):** `research/AUDITION.md`.
  - `song_fit.py` measured: Shantiniketan 103 BPM, Chiltey Roud 92 BPM, Mayabee 123 BPM (half-time); vocal density 2.6 / 6.5 / 7.8 words per 10 s in their best windows.
  - Sections were chosen from the full-song Whisper timing (hook repeats) and energy: a quiet open, a lift into the hook, and an end at a phrase end.
  - Three offline previews from one pool (14–17 shots, every cut on a beat). Checked: widths 77–100 % (the 4:5 window, as approved), no black or frozen stretch, phone copies at −14 LUFS.
  - Sent to the director.
- **Director's note on the audition (2026-11-07):** "skip Shantiniketan, use the Mayabee but different parts of the song, make iterations with footage tables; the opening should be strong; the reference had a strong and justified opening."
  - Read the reference's opening: a man at a record stall puts on a record, the song starts from it, and the title lands on the record close-up at 3.9 s. The music has a reason to start.
  - Our opening was a wide river with no person and no action.
  - Built four Mayabee iterations, each on a different part of the song with an opening chosen for that moment. Footage tables, storyboards and phone previews: `research/MAYABEE_ITERATIONS.md`.
  - Builder: added fixed openings, forced cuts on musical hits, title-on-hit and pace (`tools/audition_edl.py`).
  - New selects: C070 (boat close), C078 (Chandpal ferry ghat).
  - Mayabee is now the song. Its story-fit risk (a romance) is handled by reading the city as the "Mayabee": the enchantress you haven't seen in months.
- **Director's note (2026-11-07):** "make iterations then we will decide; the footage choice needs to be optimised, the best footage of the lot; they can be upside down or ill-oriented, please make sure they are fixed and used."
  - Reviewed all 101 clips upright at their best steady moment in the 4:5 window (`analysis/pool_v3/`).
  - Fixed orientation (`analysis/orientation.json` `fixes_2026_11_07`):
    - C017 / C018 / C025 sideways → −90;
    - C109 unusable → −90 (a red-gold pandal mirrored in a lake);
    - C010 → 180.
  - New ranked pool v3 (`tools/audition_edl.py --pool v3`). Every iteration keeps C109, C018 and C025, adds C105 (bookstall) and C089 (sunset lamps), and ends on the Academy.
  - M1–M4 rebuilt and re-rendered.
  - Checked by eye on mid-frame sheets: all upright, and the fixed clips read correctly. The "black edges" warnings are the known 4:5-window artefact (CR-20261104 item 5). No black or frozen stretches; −14.1 LUFS.
  - Sent to the director with `research/MAYABEE_ITERATIONS.md`.

## Round 3 — Changes made / Premiere build v3 (2026-11-07)
**Director:** "try m3 and m1 both". Both are built in Premiere; the director picks after the review gate.

**Sequences** (both duplicated from `Reel_kolkata_v2`, which stays as the rollback):
- `Reel_kolkata_v3_M1` (89340a17-dd5d-4877-be43-ab5dcb42f9bb)
- `Reel_kolkata_v3_M3` (117893c9-509a-4f27-957d-7b96b03964d2)

**Build:** generated from `analysis/edl_v3_{M1,M3}.json` by `tools/build_v3.py` → `analysis/_es_build_v3_{M1,M3}.jsx`, the v2b recipe generalised:
- V1 shots + V2 bloom copies; primaries only on flagged casts (the brief's round 3 list); C111 counter-keys;
- V3 vignette and V6 window trimmed to the end; V4 grain off on night shots;
- V5 title on the hit with a focus-pull settle; V7 fades;
- A3 Mayabee at −2.5 dB, fading to silence over the last 30 f; A1 muted.

**Read back:**
- M1: 13 + 13 clips, 0–1100 f, title 100–176, grain 6–925.
- M3: 15 + 15 clips, 0–1187 f, title 287–374, grain 161–1000.
- No errors in either. C109 conformed to 25 fps by interpretation.

**Fixes found on read-back / by eye:**
1. A3 `setInPoint` landed 1 frame early again (4.36 for 4.40, 163.36 for 163.40; v2 had the same) → re-placed asking for +1 frame (`_es_fix_v3_a3.jsx`); read back exact on both.
2. C109 had a dark blob (ferry roof) at the window's top edge → push 68 → 70 %, y 895 (`_es_fix_v3_c109.jsx`); checked at 3 times on the master, clean.

**Masters:** `renders/masters/kolkata_v3_{M1,M3}_master.mov` (ProRes 422; 44.00 / 47.48 s).

**Deliverables** (`tools/deliver_v3.sh`):
- `renders/exports/kolkata_v3_{M1,M3}_mix.mp4` (guide baked, −14 LUFS, archive / review);
- `_IG.mp4` (silent, for upload);
- `renders/previews/kolkata_v3_{M1,M3}_phone.mp4` (28 MB).

**Pregate:** M1 **PASS**, M3 **PASS** (`analysis/pregate_v3_{M1,M3}/`). verify_render passes. Frame scan: 2 flags each, all inside the designed fades. Fidelity skipped (CR-20261104 #6).

**Review gate:** two full reviews on Fable running.

## Round 3 — Review gate (v3 → v3b)
Reports saved unedited: `analysis/review_v3_M1.md` (FAIL: 7 major, 4 minor), `analysis/review_v3_M3.md` (FAIL: 4 major, 4 minor). Reviewer Fable 5.1; editor Opus.

**v3b fixes** (sequences `Reel_kolkata_v3b_M1` 53dc4473-d28d-4f90-aad1-33ec3df67603 and `Reel_kolkata_v3b_M3` 49d388ee-2aaf-4bdf-90fb-3f0561191b8d, duplicated from v3; EDLs `analysis/edl_v3b_{M1,M3}.json`; pool `--pool v3b` in `tools/audition_edl.py`):

| Report # | Severity | Answer |
|---|---|---|
| M1 #1 chai close half-face under the title | major | **fixed:** a real cut-in at 105 → 108 %, pos 580, 720. Pot and steam fill the window, no face. Src 11.7, after C028's dropped-frame jumps at 10.9 / 11.4 |
| M1 #2 jump cut 01 → 02 | major | **fixed** by #1: +62 % tighter, different subject (pot, not man) |
| M1 #3 the opening isn't an action that starts the music | major | **intended, disclosed:** C028 has no stirring anywhere. The brief now says what it shows (the chai-wallah sets out clay cups behind the steaming pot: the city waking). It's a mood open, and the song's first note now lands on frame 1 (#11, 3-frame fade-in). M3 is the action open (dhakis on the hit). The director picks between them |
| M1 #4 / M3 #2 C025 auto-exposure ramp | major | **fixed:** src 1.1 (past the ramp), shot ≤ 2.45 s |
| M1 #5 / M3 #3 C105 auto-exposure ramp | major | **fixed:** src 1.6, shot ≤ 3.0 s |
| M1 #6 loudest hit (24.0 s) missed | major | **fixed:** a forced cut on the hit (reel 24.03 with the new in-point), Coffee House → kids in red |
| M1 #7 Setu: lamp post, small bridge | major | **fixed (both cuts):** src 2.6 (after the pan clears the pole), 85 → 87 %, pos 740, 960 |
| M3 #1 cold open starts 0.96 s before the hit | major | **fixed:** song in 164.36 s (IG start ≈ 2:40.0); dhakis src 32.36; 3-frame fade-in, so the hit lands on frame 1 |
| M3 #4 / M1 #10 C111 too dark | major / minor | **fixed:** counter-keys now hold the camera's head level (0 → +0.72 over 2 s) instead of its darkest |
| M1 #8 pandal: reflection lost | minor | **fixed:** C109 from the ferry ride's later window (src 48.9 real s, 64 → 66 %, y 900): full reflection, clean top (no ferry roof) |
| M1 #9 chai wide: head cropped at the push's end | minor | **fixed:** position keyed with the push (y 910 → 937), so the top edge stays put |
| M1 #11 song attack clipped | minor | **fixed:** song in 4.32 s (the attack) |
| M3 #5 title on the snare pickup, not the band's downbeat | minor | **fixed:** the cut and the title move to the full-band downbeat (reel 11.24); the boat holds through the pause |
| M3 #6 / M1 beat timing: every cut 1–2 frames late | minor | **fixed:** detected beats nudged 0.05 s earlier (`--beat-lag 0.05`) |
| M3 #7 dhakis edge clutter | minor | **fixed in part:** 54 %, pos 570, 900 clears the half-face at the left. The passer-by in the last 5 frames is gone with the shorter shot (now 2.0 s) |
| M3 #8 taxi: man on the phone at the left | minor | **intended:** he's too close to the taxi to crop out without black edges, and a later in-point brings a second man in. Street life; the director can ask for a swap (C101) |
| M3 note: vignette darkens edges 10–12 % | note | **intended (approved look, v2b).** Offer the director a halved vignette if anything reads "processed" |
| M1 note: C061 is two men on a drifting boat, not rowing | brief text | **fixed** in the EDL and the brief |

### Second loop (v3b)
- **M3 v3b: PASS** (`analysis/review_v3b_M3.md`). Every v3 major resolved. Five minors go to the director:
  1. the taxi man on the phone;
  2. dhakis-shot clutter (a phone filming behind, a passer-by in the last 4 frames);
  3. the Setu lamp arm in the corner behind the title;
  4. five cuts on beats the band doesn't play (13.97, 29.99, 38.00, 20.51, 5.44): check by ear;
  5. a second Howrah (day stock), offered as a day → night callback or a swap for own footage.
  - Note: halve the vignette first if anything reads "processed".
- **M1 v3b: FAIL** (`analysis/review_v3b_M1.md`). Ten of eleven v3 findings resolved; the Setu was partly resolved. Two new majors:
  - **#1 hit at 40.05 missed** (a regression: lengthening the last shot moved the Academy cut to 39.00). **Fixed in v3c:** pandal 32.04–36.04, dancers 36.04–40.04 (the whole clip, src 0.0), Academy 40.04–44.04 on the hit.
  - **#2 Setu lamp arm and tree.** **Fixed in v3c:** 90 → 92 %, y 800 (the arm leaves the top), x keyed 740 → 900 with the camera's pan (the pylon stays in to the end). Checked on the camera file at 4 times, no black edges.
  - Minors:
    - **#3** band entry at 8.05 inside the boat hold: **intended.** The title shot can't hold 4 s: C028's steady stretch after the jumps ends at 14.9. The director's ear decides.
    - **#4** Setu → tram brightness jump: **fixed:** tram +0.6 (was +0.4). A swap isn't possible: the tram's clean stretch is ≤ 2.45 s.
    - **#5** C018 is an adult and a child in red: **fixed** in the EDL and the brief.
  - Tempo is ≈ 120 BPM (the reviewers' measure); the beat tracker read 123. The cuts follow the detected beats, so the grid holds.
- **v3c_M1:** `Reel_kolkata_v3c_M1` 27024db8-0266-45f9-bf88-06b26191169a, EDL `analysis/edl_v3c_M1.json`, `_es_build_v3c_M1.jsx` (build_v3 now keys x and y). Gate step 6: this is the focused check of the last fixes (the changed shots only).

### Focused check (v3c_M1): FAIL on one major, so it goes to the director (gate cap reached: two loops + the focused check)
`analysis/review_v3c_M1.md`. Resolved: the Academy on the hit, the lamp arm out, the pylon in, C018's description. Audio bit-identical to v3b; the rest of the picture untouched.
- **#1 tree crown at the Setu's left edge for ≈1.2 s (major): open, the director's call.** At src 2.6 the foliage sits next to the pylon's leg, so no crop keeps the pylon and drops the tree.
  - The reviewer wrote "the director named the tree": that's wrong. The tree came from the reviewer's own v3b finding and the editor's change list, not a director note.
  - Options for the director: accept (≈1.2 s of leaves at the edge), or swap the Setu for C065 (the same bridge, cleaner left edge; needs one more build and check).
- **#2 pylon grazes the edge in the last 0.4 s (minor):** goes with #1 (key x to 980, or moot with C065).
- **#3 Setu → tram drop unchanged in ratio (minor): intended.** Camera-true on both sides; the tram reads fine by eye.
- **#4 EDL text (minor): fixed** (Setu "shows" no longer mentions the title).
- Phone copies verified: `renders/previews/kolkata_v3c_M1_phone.mp4` (28.3 MB, −13.5 LUFS) and `kolkata_v3b_M3_phone.mp4` (28.0 MB, −13.8 LUFS): PASS.

## Instagram package
<!-- Filled in after final approval. -->

## Round 4 — Story note (2026-11-07)
**Note (verbatim):** "wait the footage still does not match the song or the story no story is coming out properly". The same note as round 2 ("the frames didn't follow a story"), now the third time story has failed.

**Why (editor's diagnosis of v3b_M3):**
1. **The order fights the story.** It opens on Pujo night (the arc's peak), then jumps back to morning river and runs to night again. Time goes backwards, then forwards.
2. **Nobody to follow.** 9 of 16 shots are empty places (Setu, ghat steps, Howrah ×2, tram, coffee-house hall, sunset lamps, pandal, Academy). "A Bengali far from home" lives only in the brief's story column; nothing on screen says someone is away, arriving or leaving.
3. **Shots were slotted by priority and energy, not by meaning.** `audition_edl.py` fills beat slots from the pool in beat-bucket order; the song's turns (breath, hook, chorus) carry no story turn except the title.
4. **The reference's thread** (`analysis/references/watch/sheet_01.jpg`): a person's action starts the music, one mood (warm, melancholy light), people in almost every frame.
5. **Process gap:** the skill's line table (Phase 2.3, `line | shot | what in the frame shows it`) is written for VO reels only, so this music montage never had one. Story beats were labels on time-of-day buckets.

**Footage that can carry a story** (seen on `analysis/pool_v3/sheet_*.jpg`, not yet in any cut): scooter POV with the speedometer in frame (C092–C094), red façade rushing past the scooter (C096–C098), people crossing the Howrah walkway (C081–C083), a man at the railing looking at the Setu (C067), the Chandpal ferry-ghat gate (C077/C078), Maidan football at pink dusk (C001–C007), the bus crowd in the sun (C019/C020), the Academy crowd at night (C034), an empty tram interior at dusk (C030), the Dashami ghat lights (Oct21 C039).

**Director's pick (AskUserQuestion, 2026-11-07):** story **"Home for Pujo"**: someone comes home and leaves again. Same song window as v3b_M3 (164.36 s, 47.5 s; IG start ≈ 2:40).

**Line table v4** (`tools/story_edl.py` → `analysis/edl_v4_story.json`; every cut on a played beat, onset ≥ 4× median):

| # | Reel time | Song moment | Story line | Shot | What in the frame shows it |
|---|---|---|---|---|---|
| 1 | 0.00–2.00 | the hit | the dhak calls you home | Oct21 C047 | dhakis drumming by the idol truck |
| 2 | 2.00–6.48 | band in full (4.0) | you arrive across Howrah | C083 (new) | people walking toward camera on the Howrah walkway |
| 3 | 6.48–11.24 | the breath | the river below | C061 | two men on a country boat on the Hooghly |
| 4 | 11.24–14.48 | the hook | home: "Calcutta" | C064 | the Setu, title |
| 5 | 14.48–17.00 | verse | the ride in | C094 (new) | scooter POV, speedometer in frame, heritage road |
| 6 | 17.00–19.00 | verse | the old city rushing past | C096 (new) | red façade and bougainvillea blurring past |
| 7 | 19.00–21.00 | verse | the old tram | C025 | blue-and-white tram |
| 8 | 21.00–24.00 | verse | the yellow taxi | C101 (new) | Ambassador on the tram lines, a man walking past |
| 9 | 24.00–27.00 | hook again | who you missed | C028 | the chai-wallah at his steaming pot |
| 10 | 27.00–29.00 | – | who you missed | C105 | the bookseller in his stall |
| 11 | 29.00–31.00 | – | who you missed | C111 | the Coffee House hall |
| 12 | 31.00–33.00 | chorus | evening | C003 (new) | boys playing football on the Maidan at dusk |
| 13 | 33.00–36.00 | chorus | Pujo | C109 | the pandal on the lake at sunset |
| 14 | 36.00–38.48 | chorus | Dashami night | Oct21 C039 (new) | the lit truss over the ghat, the immersion crowd |
| 15 | 38.48–42.04 | last phrase | the goodbye | Oct21 C035 | lal-paar dancers on Dashami |
| 16 | 42.04–47.50 | last phrase, ring-out | you leave | stock Howrah blue hour | the bridge at blue hour; fade to black (bookends the arrival across Howrah) |

Dropped from v3b_M3: ghat steps, Howrah day stock (the second Howrah), C100 taxi (→ C101, a person in frame), kids in red, sunset lamps, Academy night. 16 shots, 47.5 s.

## Round 5 — Director note on the v4 story preview (2026-11-07)
Verbatim: "Again the shots are nkt that great just use the stock musci as reffernce at stock offening as reffence use the same clip if needed and clour grade it ina differnt way, for my viieos you not doing teh cinametci effects that we did in othe project no slow motion no anything and footage selection is bad, whever you feel thw ctock teel stiory cannotbe replciated use free vdieo from online"
Read as ("stock" = the reference reel, `references/ref_north_kolkata.mp4`):
1. The shots aren't good enough; the footage selection is bad.
2. Use the reference's music (*Pyaasa*, "Jaane Woh Kaise Log The", guide `audio/guide_ref_stereo.wav`, 35.08 s) and the reference's opening (a man puts a record on; the song starts from it; title on the record close-up).
3. Follow the reference's story shot for shot; where the director's footage can't replicate a shot, use free-licence stock video from online.
4. "Use the same clip if needed and colour grade it in a different way": the reference creator's own shots can't be reused (their footage; a regrade doesn't change that). Read as: reuse one of our clips twice where needed, graded differently; and our grade differs from the reference's.
5. Cinematic effects like the other reels (my-reel, puja-night-2, uski-aankhein): slow motion, speed ramps, punch-ins, designed transitions, sound design. Round 1's "no swishes, no flashes" (taken from the reference) is lifted.
→ Re-brief, not a fix round. v4 story EDL and v3b_M3 stay as rollbacks. Stock search for the gaps handed to a subagent → `analysis/stock_round5.md`.
- **Director, mid-round (2026-11-07):** added `audio/Kolkata (কলকাতা) … Praktan Anupam Roy Shreya Ghoshal ….mp3` ("I have added an audio called Kolkata"), then: "Ami Urja Mukherjee section cut out and use it as ami apnader guide; make a story 60–90 seconds".
  - Read as: the song "Kolkata" (*Praktan*, 2016; Anupam Roy, Shreya Ghoshal) replaces Mayabee. Its spoken intro (a city guide, "Urja Mukherjee", introduces herself) becomes the reel's guide; the story runs 60–90 s.
  - Guide copy `music/kolkata.wav` (48 kHz, from the mp3). Analysis `research/kolkata_song/` (117.5 BPM, bar 2.04 s; Whisper large-v3-turbo).
  - **Song map (song s):** digital silence to 9.80 (the first note) · instrumental 9.80–17.8 · spoken guide (English, then Bengali) 17.86–38.0 · verse 1 ≈ 40–62 · chorus 61.96–82.8 · instrumental after. The spoken lines: Kolkata a city of culture (17.86), heritage (21.78), surprises (23.22); her name and "your guide" (25.20–28.8); "but I call myself an explorer" (29.54); in Bengali, some say Paris is the city of love (31.6), I say Kolkata is the city of passion (34.9). The chorus asks the city to walk and see, think it over, and whether it will come along (no lyrics quoted).
  - **Window:** song 7.25 → 86.00 s = **reel 78.76 s**; the first note lands at reel 2.55 as the record settles; IG start = the very start of the song (its first note).

## Round 5 — Line table "Your guide to Kolkata" (2026-11-07)
EDL `analysis/edl_v5_guide.json` from `tools/guide_edl.py`. Storyboard `analysis/storyboard_v5_guide_p1–p3.jpg`. Stock from `analysis/stock_round5.md` (subagent; every clip checked by eye on a full-length frame sheet).
| # | reel | song moment / line | shot | what the frame shows | effect |
|---|---|---|---|---|---|
| 1 | 0.00–5.68 | intro: the song starts from the record | stock Pexels 8090957 | hands lower a record onto a vintage player | fade in 6 f, push; needle-drop + crackle at 2.40 |
| 2 | 5.68–10.56 | intro, title on the bar (reel 7.75) | stock Pexels 6742732 | stylus in the groove | title **Kolkata** with the focus-pull settle |
| 3 | 10.56–14.48 | VO: a city of culture | own Oct25:C112 | Indian Coffee House hall | slow push |
| 4 | 14.48–15.92 | VO: heritage | stock Pexels 38386435 | Victoria Memorial at dusk | 0.83× |
| 5 | 15.92–17.92 | VO: surprises | own Oct25:C110 | a pandal-palace mirrored in a lake | whip in + whoosh |
| 6 | 17.92–22.24 | VO: her name, "your guide" | own Oct25:C082 | walking into the Howrah walkway truss | slow push |
| 7–8 | 22.24–24.32 | VO: "an explorer" | own Oct25:C094 | scooter POV | **speed ramp 250 % → 100 %** + whoosh |
| 9 | 24.32–27.60 | VO: some say Paris is the city of love | own Oct25:C089 | iron lamps on the river promenade, sun | slow push |
| 10 | 27.60–30.04 | VO: I say Kolkata is the city of passion | own Oct21:C047 | dhakis drumming | — |
| 11 | 30.04–32.08 | accent | own Oct21:C035 | Dashami dancers | **flash** 3 f + sub-hit |
| 12 | 32.08–36.04 | verse: the city in light | stock Pexels 3939524 | sun over the Vidyasagar Setu, a country boat | **dissolve** 10 f in, push |
| 13 | 36.04–40.32 | verse | stock Pexels 4200197 | bathers on the ghat, Howrah behind | 0.83× |
| 14 | 40.32–42.36 | verse | stock Pexels 5013993 | a boy batting on the ghat | — |
| 15 | 42.36–44.52 | verse | own Oct25:C061 | boatmen on the Hooghly | push |
| 16 | 44.52–46.60 | verse | stock Pexels 40180894 | under Howrah from the river | **slow-mo 0.42× (60 fps)** |
| 17 | 46.60–48.64 | verse | stock Pexels 35071306 | the flower market from above | slow-mo 0.42× |
| 18 | 48.64–50.72 | verse | stock Pexels 35067019 | a marigold porter under Howrah | slow-mo 0.42× |
| 19 | 50.72–52.76 | verse | stock Pexels 39276190 | a flower seller | slow-mo 0.42× |
| 20 | 52.76–54.88 | verse end | stock Pexels 40160762 | Kumartuli artisans painting Durga idols | push |
| 21 | 54.88–56.92 | chorus: walk and see | stock Pexels 2843864 | people walking past Bengali wall writing | 0.83× |
| 22 | 56.92–59.04 | chorus | own Oct31:C018 | an adult and a child in red walking | push |
| 23 | 59.04–61.04 | chorus: think it over | own Oct25:C105 | an old bookseller at his stall | push |
| 24 | 61.04–65.16 | chorus: walk | stock Pexels 2843866 | yellow taxis, a tram passing old houses | 0.83× |
| 25 | 65.16–67.28 | chorus | own Oct25:C097 | façades rushing past the scooter | step-print (build) |
| 26 | 67.28–69.36 | chorus: think it over | own Oct31:C028 | the chai pot steaming | push |
| 27 | 69.36–71.40 | chorus: dusk | stock Pexels 38584444 | Howrah at blue hour | 0.83× |
| 28 | 71.40–75.52 | chorus: will you come with me? | own Oct31:C030 | inside a tram at night | tram bell |
| 29 | 75.52–78.76 | outro | stock Pexels 34545518 | a diya on the river, Howrah lit | fade to black 20 f |
- 13 own shots, 16 stock (Pexels / Pixabay licences, `raw/SOURCES.md`). The reference's beats kept: the record opens the song, the river in golden light, the ghat with Howrah, the flower market, the colourful craft lane, the old streets with wall writing, the tram at night.
- Not in any free library: a Kolkata record shop (a home record player instead), a Kolkata tram at night outside (own interior C030 instead). An AI-generated record-shop opener is possible (motion-and-ai.md §3, ≈ $0.52) if the director wants it.
- The preview's whip and step-print are placeholders (hard cuts); they're built in Premiere.


## Round 5b — Director notes on the v5 preview (2026-11-07)
Verbatim: "the final shot I don't like, thefew of my shots need stabilzationa nd cnmeatic effect, the swooping shots don not make it good. The shots of city of surprises can be better, but we are on the right trakc please keep workinh"

Read as:
1. Replace the final shot (stock diya + Howrah, pexels-34545518: it also measured 12 px jitter).
2. Stabilise our handheld shots and give our own shots real effects (slow motion, ramps, designed transitions), not just cuts.
3. Drop the swooping shots.
4. A better picture for "and city of surprises".
5. Keep the story, song window and line timings (approved direction).

**Measured on the v5 preview** (`scripts/shake_report.py`, `analysis/shake_v5.json`; jitter RMS px at 1080 wide; locked shots read 0.3–1.2):

| Shot | jit_rms | pan px/s | Verdict |
|---|---|---|---|
| 25 C097 façade ride | 56.2 | 701 | the swoop: out |
| 08 / 07 C094 scooter POV | 32.4 / 20.1 | 32 / 240 | swooping and shaky: out |
| 24 stock tram street | 12.8 | 131 | stabilise |
| 29 stock diya (final) | 12.2 | 251 | out (note 1) |
| 03 C112 Coffee House | 9.8 | 215 | stabilise + slow |
| 15 C061 boatmen | 9.2 | 55 | stabilise (horizon rolls) + slow |
| 10 C047 dhakis | 8.3 | 38 | stabilise + ramp |
| 06 C082 walkway POV | 2.6 | 17 | stabilise (walking bob and roll) |

**Changes in v5b** (`analysis/edl_v5b.json` from `tools/guide_edl_v5b.py`; same song window 7.25 → 86.00, 78.76 s; 30 shots; the picks are in `analysis/round5b_picks/PICKS.md`, all measured with shake_report):

| Line | v5 | v5b | Effect |
|---|---|---|---|
| culture | C112 Coffee House | same | stabilised, 70 % slow motion |
| heritage | stock Victoria | same | whips out (3 frames) |
| surprises | C110 palace pandal on the lake | **Oct18:C187** giant LED petal arches nested over a packed street (0.74 px; 30 fps, interpreted) | whip in + whoosh, slow push |
| your guide | C082 walkway POV | same | stabilised, horizon levelled (shake halved) |
| explorer | C094 scooter ramp + ride (swooping) | **stock Pexels 35040390** a young woman in a saree on a Kolkata Metro platform, looking around as a train streaks past (0.3 px; 60 fps) | real slow motion (interpreted), slow push |
| city of love | C089 river lamps | same | light leak on the cut in |
| passion | C047 dhakis | same | stabilised; real speed, then an eased ramp into 40 % slow motion |
| … passion | C035 dancers | same | 65 % slow motion after the flash |
| verse start | stock Setu sunset | same | dissolve + light leak |
| on the river | C061 boatmen | same | stabilised, horizon levelled, 70 % slow motion |
| come walk and see | stock wall writing (a woman and a passer-by block the wall) | **stock Pexels 32665218** a hand-pulled rickshaw running toward us down the tram tracks, yellow taxis (0.2–0.9 px) | — |
| walk and see | C018 walk | same | 60 % slow motion |
| the old streets | stock tram street | same | stabilised |
| rushing past | C097 façade ride (swooping, 56 px) | **C101** yellow Ambassador taxi on the tram lines, a man walking past (static) | slow push |
| think it over | C028 chai | same | 50 % slow motion on the steam |
| outro | stock diya + Howrah (disliked; 12–22 px shake) | **C033** (own) the Academy of Fine Arts lit at night, people at the door (0.07 px): bookends "a city of culture" | 75 % slow motion, slow push, fade 20 f |

- **Mid-round note (2026-11-07), verbatim:** "too many pooja shots young are using". The first v5b draft (not sent) had 8 Pujo shots out of 30: the surprises triplet, the rajbari arch, the dhakis, the dancers, Kumartuli, and the Dashami ghat final. Now 4 of 28: one pandal shot for "surprises", the dhakis, the dancers, and Kumartuli (artisans at work). The triplet, the rajbari arch (explorer) and the Dashami ghat (final) went; explorer and final are now our own non-Pujo shots. Still Pujo and swappable on request: the dancers (alternative: C003 boys' football on the Maidan for "passion").
- **Second mid-round note (2026-11-07, on the first sent v5b), verbatim:** "that tram vidoe great find something better also the shot where a woman passes and muslim man is there I didn’t understand the validity of including it, also the pandal image I could find clue what that pandal ?"
  - Read as:
    1. the tram-rails explorer shot (C023) isn't great;
    2. the stock wall-writing shot shows only passers-by;
    3. the forge pandal (C088) is unreadable.
  - Changes:
    1. explorer → stock Pexels 35040390, a young woman in a saree on a Metro platform looking around, real slow motion. Own C067 was tried first: upright it's a family chatting on the promenade, not an explorer;
    2. "come walk and see" → the stock hand-pulled rickshaw on the tram tracks;
    3. surprises → the LED petal arches (C187), readable at a glance.
  - Pujo stays at 4 of 28.
  - The forge pandal is Oct 16 card clip C088, recorded 2026-10-15 20:27. The file has no GPS, so the pandal isn't named in any studio note. Its giant spanners are stamped "DROP FORGED". puja-night-2 used the same pandal.
- Own Pujo clips copied into `raw/selects/` for the picks (director profile: copies of what a reel uses): `Oct18_…C187` (used), and `Oct16_…C088`, `Oct15_…C044`, `Oct20_…C051` (picked, then dropped; kept as alternates).
- Preview pre-renders: `renders/fx_preview/*.mov` from `analysis/fx_jobs_v5b.json` (`tools/fx_prerender.py`). Leaks: `renders/overlays/leak_a|leak_b_{screen,alpha}.mov` (`tools/make_leak.py`).
- **The build** follows each shot's `note` in the EDL: camera in-point and rate; Warp Stabilizer (Smooth Motion) on the five stabilised shots; AE Timewarp for the own-footage slow motion and the dhakis ramp (time_remap op); the whip as a Directional Blur ramp + whoosh; the leaks on V4 in Screen.
- Considered and not used: an end title over the final (tested on the truss shot: gold on gold, unreadable).


## Round 6 — Director notes on v5b (2026-11-07)
Verbatim:
- "Ami ujar mukherjee why that part is there chop it / it should be ami apnader guide / out, also the coffe house image is mad I had mukltioel bother botages check that / teh frame for city of surporises is just bad doe snot match / The gitrl in the metro station why is that there / Try and uderstand teh lyric and dtermine the shots post it crreta ethat skill"
- "And also the trnsition sould an deffetc I don not like"

Note: the round-5 note "Ami urjar mukheejee section cut out and use it as ami apanader guiide" meant exactly this cut. I had read it as "use the guide intro".

**Changes made in v6** (`analysis/edl_v6.json` from `tools/guide_edl_v6.py`; 76.20 s, 26 shots; line meanings in `analysis/lyrics_meaning.md`):
1. **Name cut:**
   - `tools/song_edit_v6.py` removes song 25.72–28.273 s: exactly 5 beats, with a 30 ms centred crossfade. The new file is `music/kolkata_v6_edit.wav`.
   - The line now runs "Ami … apnader guide, but I call myself an explorer". Re-transcribed to confirm, and no click at the join.
   - **The edit can't exist in Instagram's library audio**, so this reel posts with its baked audio.
2. **Coffee House:** C112 (a pan with no subject) → **C111**, the locked wide hall with waiters in white (0.42 px), at 70 % slow motion. C113 and C114 are handheld (7–10 px).
3. **Surprises:** the LED arches → the **hand-pulled rickshaw on the tram tracks** (stock Pexels 32665218): daylight, matching Victoria and the walk around it, "the old city still running".
4. **The Metro girl is out.** "I am your guide, but I call myself an explorer" is now one stabilised walking POV (C082). No stranger stands in for the guide.
5. **Transitions:** whip, whoosh, flash, riser and both light leaks removed. Plain cuts, one 10-frame dissolve into the verse, fade in and out. Sound effects left: needle drop and tram bell only.
6. **Lyrics → shots:**
   - every line is summarised (meaning only) and given one shot, in `analysis/lyrics_meaning.md`;
   - the chorus line "walk and see" is now one 4.2 s walk (C018);
   - Pujo is down to 3 of 26 (dhakis, dancers, Kumartuli).
7. **The skill:** drafted as **CR-20261107-kolkata-lyric-shot-skill**, with the full SKILL.md. HQ owns `.claude/skills/`, so a reel session can't install it.

### Round 6b — Director note on v6 (2026-11-07)
Verbatim: "Seems nice. Just try and look for a better tram footage. The footage that you've used that has a car and a tram, it's not very clear. We can use a footage from the tram actually running on the line with a clear front end view. Check for that, maybe."

The shot in question is #21 `stock_tram_street` (Pexels 2843866, reel 58.52–62.60): the tram only slides past side-on behind a black SUV. The full 22.6 s clip has no head-on moment.

**Search for a running Kolkata tram, front-on (none found free):**
- **Pexels:** every "kolkata", "kolkata street", "calcutta" and "kolkata city" result (267 clips) checked by description and tags for tram, plus 175 tram clips checked for India/Kolkata. Only 2843866 has a Kolkata tram. The rest are Istanbul, Lisbon, Melbourne, Wrocław, Bucharest, Mexico City. Riaz Uddin's Kolkata series (32665218–32665230) checked by preview: taxis, buses, rickshaws, St Paul's, Science City, no tram.
- **Pixabay:** Kolkata results have no tram; its tram results are Melbourne, Prague, Hong Kong, Budapest.
- **Wikimedia Commons:** 1,183 Kolkata videos, none of a tram. Vimeo search needs a login. Getty and Adobe Stock have paid Kolkata tram clips.
- **Own footage:** only the retired trams parked under trees (Oct31 C025–C027: a clear front end, but not running) and the night interior (C030, already shot 25).
- **AI:** this reel has $0 of AI spend (caps: $2, 2 shots). A Veo tram would need the AI label on the post.

**Director's choice: (b) the AI-generated tram**, $0.12 draft approved (2026-11-07). The others offered: shoot it, the parked C027 + push-in, keep 2843866.

**Draft 1** (`renders/gen/tram_front_draft_20261107-233159.mp4`, $0.12 charged; prompt and negative in `analysis/gen_tram_front_prompt_v1.txt` / `_negative_v1.txt`):
- **Good:** the tram comes straight at the camera on grooved rails, with a white body, a blue band, a headlight, overhead wires and green-shuttered houses. No baked look.
- **Wrong:**
  - the board reads "ROUTE", with invented numbers;
  - the taxi is a New York checker cab, not an Ambassador;
  - the light is sunny, against C101's haze. Luma 0.489 vs 0.391; 15.9 % of the sky clipped vs 0.06 %; R−B 0.068 vs 0.097.
- **colour_report.py crashed on C101** (the same fps-parse bug as shake_report), so I measured C101 from a temporary copy. Filed in **CR-20261107-kolkata-film-emulation-first-use**, along with the skill's first-use report.

**v6b preview:**
- `tools/guide_edl_v6b.py` imports v6 and swaps shot 21 for the draft, conformed with `conform_clip.py --start 0.25 --match renders/gen/anchor_C101_1s.png` (3.60 s at 25 fps). The fx pre-render slows it to 0.85 to fill 4.08 s, preview only; the 8 s final needs no slow-down.
- Everything else is v6.

**Re-prompt ready** for draft 2 and the final (`analysis/gen_tram_front_prompt_v2.txt` / `_negative_v2.txt`):
- no taxi;
- a plain blank board;
- "hazy overcast afternoon, no direct sun";
- negative adds readable words / ROUTE / NY taxi / sunshine / blue sky.

Dry runs: draft 2 $0.12, final $0.40. Each needs the director's yes. Per shot: 3 drafts, 1 final.

**Director: "yes" to draft 2 + the final (≈ $0.52), 2026-11-07.**

**Draft 2** (`renders/gen/tram_front_draft_20261107-234435.mp4`, $0.12, seed 2611, prompt v2): all three fixes landed.
- the board is plain and unreadable;
- no taxi;
- overcast white-grey sky; blacks match C101 (p02 0.045 vs 0.046, crush 0.3 %).

Still off: brighter (luma 0.493 vs 0.391), the overcast sky clipped (16 %), paler (sat 0.117 vs 0.225) and neutral where C101 is warm (R−B 0.001 vs 0.097). That goes to the conform nudge and the Phase 4 primary + A2 match. No baked look, so the final keeps the same prompt + seed.

**AI final** (`renders/gen/tram_front_final_20261107-234604.mp4`, 1080×1920, 8 s, 24 fps; $0.40; same prompt v2 + seed as draft 2; conformed to `renders/gen/tram_front_final_conformed.mov`):
- clean, with a real approach;
- next to a real WBTC car, the tram looks generic and European;
- reel AI spend: **$0.64 of $2**.


### Round 6c — Director note while the final generated (2026-11-07)
Verbatim: "the tram shot in applicable use stock inage"

Read as: where a real stock **photo** fits, use it instead of the AI clip. The final was already sent to OpenRouter and couldn't be recalled, so it was kept as the alternative.

**Search:**
- Pexels photos: 2 real Kolkata tram fronts, 36464499 and 38193707 (the depot);
- Unsplash: 200 free "kolkata tram" photos.

The three best, compared as 4:5 crops (`analysis/tram_options.jpg`):
- **Unsplash pc_sZ1DLdGU (Subhashis Das): picked.**
  - A WBTC tram on the line, front end clear, route board "25 Esplanade–Gariahat", headlight on, daylight under trees.
  - Real and unmistakably Kolkata.
- Unsplash vyHy43ezE40 (Ujjwal Jajoo): tram 277 head-on, with the best haze match, but the rails barely show and it reads as parked.
- Pexels 36464499: the tram is small in the frame.

Licences are logged in `raw/SOURCES.md`.

**v6c** (`tools/guide_edl_v6c.py` → `analysis/edl_v6c.json`): v6 with shot 21 = the photo.
- The photo is a 4:5 crop of its full height, framed exactly in the window (y 235–1584), with a blurred copy under the matte: `renders/gen/stock_tram_subhashis_9x16.png`.
- It's pushed 1.00 → 1.06 over 4.2 s by `conform_clip.py`.
- **No AI shot in v6c, so no Instagram AI label is needed.**
