# Earlier rounds (moved from project.md, 2026-11-10)

## Round 1 — Interview (2026-11-09)
| Question | Answer |
|---|---|
| Story spine | Letter to Maa / home |
| Speech | None: the lines appear as on-screen text |
| Audience + end action | Far from home this Diwali → send it to someone |
| Length | 30–45 s, **then capped at ≈ 20.7 s** by the audio route |
| Footage | dropped in `raw/Media/` (camera card layout) |
| References | `references/This Diwali, the city still buzzed — …mp4` (alias `ref_city_still_buzzed.mp4`), IG link https://www.instagram.com/p/DQDqyKGD5CK/ |
| Soundtrack | First "IG library song, same as the reference". The audio page says **Original audio by howwdeep.exe**; offered library "Telephones" (full length) vs the original audio (~21 s) vs another song → **director chose howwdeep's original audio** |
| Letter lines | Claude drafts, director edits |
| Language | Hindi + English |
| Title | Claude proposes 3 |
| Pilot | yes |
| Cinematic depth | Bake at f/2 as shot; "take your call shot by shot" |

### Reference: `ref_city_still_buzzed.mp4` by howwdeep.exe (Oct 21, 2025; 32.3K likes; paid partnership)
- Caption: "This Diwali, the city still buzzed — not with crackers, but with the sound of work… Another one who didn't go home this year." Subject: street workers on Diwali (security guard, rickshaw puller, seller on a stool, rangoli-tile maker, sweet-cart vendor on his phone, marigold garland hands, a man by candles, a flower seller).
- One line for the whole reel: **"Sorry maa, Diwali me nahi aa paunga"**, small white italic sans in quotes, upper left of the picture. Ends on black with a yellow handwritten signature.
- Frame: landscape footage in a **4:3 window** centred in 9:16 (720×542 of 720×1280), black above and below.
- Measured (`analysis/teardown/TEARDOWN.md`, 2 scene thresholds): 20.8 s, 24 fps, 16 cuts, median shot **1.17–1.33 s**, shortest 0.08 s, longest 3.17 s, first cut 2.62 s, one 1–2 frame flash. Muted teal-green film look, crushed blacks, marigold orange kept.
- Audio (`analysis/audio_summary.md`): −14.1 LUFS, **152 BPM** (bar 1.579 s; or 76 half-time), accents 0.07 / 2.69 / 5.48 / 8.24 / 10.24 / 13.03 / 16.6 s; low intro 0–6.25 s, full 6.25–9.45 s, mid to 18.2 s, beatless tail to 20.7 s. Whisper heard no usable lyric (instrumental-led section).
- Comments worth knowing for the caption: "Why do we pity them? They are not asking for pity, they are asking for respect." / "Some call it Diwali and some survival." The letter should honour, not pity.

### Footage (`analysis/ingest.md`, `analysis/summary.md`, `analysis/selects.md`, `analysis/motion.json`)
- 19 clips, 172.9 s, Blackmagic Cam 3.5, iPhone 17 Main, HEVC 8-bit Rec.709, all **25 fps** → **sequence 25 fps**, no conforming. Flicker: safe on all. Shot in Bengaluru (GPS in metadata).
- **18 clips are Apple Cinematic Video** (f/2 recorded; C043 isn't, f/1.6): depth blur not in the picture → bake (`tools/cine_bake`, `analysis/cinematic/depth_sheet.jpg`).
- **Orientation** (`analysis/orientation.json`, checked at 25/50/75 % of every clip): 18 clips held landscape, tagged −90 → Premiere Rotation −90 (ffmpeg transpose=2). C060 already upright (tag 0). No +90 / 180.
- Casts: C052/C053 cool-magenta (stall lights). C050 VFR (24.967 avg): check placed windows. Night clips 0.20–0.40 luma; C047–C049 (auto interior) darkest of the usable ones.

| Clip | What | Best moments (selects + eye) | Note |
|---|---|---|---|
| C043 | Nov 1: distant lit palace dome at night, near black | — | luma 0.01; not usable except as a black-out |
| C047 / C048 / C049 | Auto driver from the back seat; Diwali-lit street through the windscreen | C048 1.5–3.5 s, C047 0–1 / 3–4 s | dark interior scores low, strong meaning ("the one who drives everyone home") |
| C050 / C051 | Paan stall: older man in white making paan, young helper; C051 he looks off, still | C050 0.5–2.5 s (steady), C051 0–2 s | C050 ends in a whip; C051 ends on the floor |
| C052 / C053 | Young cook plating at a veg-food stall, purple light; C053 serving | C053 5.5–8.5 s (top score), C052 0.5–3.5 s | magenta/cool cast |
| C054 | Parotta/dosa maker, hairnet, orange shirt, at the tawa | 0.5–3 s, 5–6 s | steady, warm |
| C055 | Egg trays, very shaky | — | unusable (shake 15–50) |
| C056 | Juice stall man in magenta light, near-portrait | 0–3 s | ends in a light-streak whip (maybe a transition) |
| C057 / C058 | Diwali stage show crowd; boy in a Barcelona jersey seen from behind | C057 0–3 s, C058 0–3.5 s | the celebration others are at: contrast or the "watcher" |
| C059 | Ice-cream counter server in hairnet, pink shop | 0.5–3.5 s | ends on the floor |
| C060 / C061 | Food street ("Rifle Shooting" sign): man in a wheelchair with an ID lanyard, a woman sitting on the pavement | C060 0–2 s, C061 5.5–6.5 s | C061 2.5–4.5 s is a pan |
| C062 | Jewellery street vendor on his phone by a red car | 4–7 s | "on the phone home" line |
| C063 / C064 | Nov 9 daytime: young car-washer foaming a scooter; C064 looks up and smiles | C063 1–4.5 s, C064 0.5–5 s | the morning after, still working: a candidate last shot |

## Round 2 — Interview (2026-11-09)
Sheets sent (phone size): `analysis/framing/framing_sheet.jpg`, `analysis/looks/looks_sheet.png` (depth-baked stills, 30 %), `analysis/type/titles_sheet.jpg`, `analysis/type/lines_sheet.jpg`, `analysis/letter_drafts.md`.

| Question | Options offered | Answer |
|---|---|---|
| Creator's OK for the audio | — | **Yes, director has howwdeep.exe's OK** |
| Letter | A Sorry, Maa · B Mera diya · C Kam shabd | **A** (recommended) |
| Title | Diwali, door se · Mera diya bhi jalaana · Is baar nahi, Maa | **Mera diya bhi jalaana** (from draft B; it isn't a line in letter A, so it works as the title) |
| Framing | R 4:3 (75 %) · C 4:5 (45 %) · B 16:9 (100 %) · A full-bleed (32 %) | **R 4:3 window** (recommended) |
| Look | camera-true · muted except red · 500T→2383 · 500T→2395 (all 30 %) | **Camera-true** (recommended) |
| Title font | Rozha One · Amita Bold · Baskerville Italic · Snell Roundhand (8 on the sheet) | **Rozha One** (recommended) |
| Letter-line type | reference italic · Baskerville Italic · handwritten · Eczar | **Baskerville Italic, cream** (recommended) |
| Pace | 2 shots per line · reference ~1.2 s · 1 shot per line | **2 shots per line**, 1 bar (1.58 s) each (recommended) |
| End card | title + sign-off · handwritten signature · title only | **Title + "— tumhara beta" + small @satyajitmall** (recommended) |

Measured for the brief:
- Looks at 30 % on 4 stills (`analysis/looks/looks.json`): `muted_red` sat −10…−27 %, 500T→2383 +0.005–0.014 luma, 500T→2395 lifts blacks (crush 6.5 → 0 % on the auto). Not used: camera-true chosen.
- Bake pipeline check (C064, same frame, passthrough vs ffmpeg decode of the camera file): +0.007–0.009 luma uniform (≈ 2 code values), no range shift. `cine_bake --start t` begins one frame early (2.48 s for 2.5 s).

## Proposal (Checkpoint 1, v1) — 2026-11-09
Brief: `brief.md` · EDL: `analysis/edl_v1.json` (built by `tools/build_edl_v1.py`) · storyboard `analysis/storyboard_v1_p1.jpg`, `_p2.jpg` · preview `renders/previews/could-not-go-home-diwali_p1.mp4` + `_p1_phone.mp4` (27.4 MB).

**Hook options**
1. **(Recommended)** `01_C047_auto` (C047 0.60 s): the auto driver from the back seat, a Diwali-lit street moving through the windscreen. On the first accent (0.07 s), slow push, L1 from 0.20 s. Opens on work, in motion, with the apology.
2. `07_C062_vendor` first (C062 0.52 s): the vendor on his phone + "Maa,". Opens on the call home, but spends the strongest line-object (the phone) at the start.
3. `12_C064` (C064 7.5 s) as a cold open: the car-washer looks up, then back to the night. Strong face, but breaks the night → morning order and gives away the promise.

**EDL v1** (cuts on the bar downbeats, 25 fps)
| # | Shot | Reel | Camera in | Line | V1 move | V5 | Out | SFX |
|---|---|---|---|---|---|---|---|---|
| 1 | 01_C047_auto | 0.00–1.56 | C047 0.60 | L1 Maa, is baar ghar nahi aa paaunga. | push 37.5→39.5 | matte + L1 | cut | – |
| 2 | 02_C048_auto_turn | 1.56–3.12 | C048 2.40 | L1 | base 37.5 (stabilise) | L1 | cut | – |
| 3 | 03_C054_parotta | 3.12–4.68 | C054 0.32 | L2 Yahan Diwali pe sabse zyada kaam hai. | base (stabilise) | L2 | cut | – |
| 4 | 04_C054_parotta_close | 4.68–6.24 | C054 3.92 | L2 | Scale 46 @ 752,1000 (stabilise) | L2 | cut | – |
| 5 | 05_C052_cook_plating | 6.24–7.84 | C052 1.00 | L3 Tumhare haath ka khaana yaad aata hai. | push | L3 | cut | – |
| 6 | 06_C053_cook_serving | 7.84–9.44 | C053 1.20 | L3 | base (stabilise) | L3 | cut | – |
| 7 | 07_C062_vendor | 9.44–11.04 | C062 0.52 | L4 Phone pe aarti dikha dena. | base (stabilise) | L4 | cut | – |
| 8 | 08_C062_vendor_close | 11.04–12.64 | C062 4.92 | L4 | Scale 46 @ 787,830 (stabilise) | L4 | cut | – |
| 9 | 09_C050_paan | 12.64–14.24 | C050 0.40 | L5 Papa se kehna, main theek hoon. | push | L5 | cut | – |
| 10 | 10_C051_paan_look | 14.24–15.80 | C051 0.20 | L5 | base (stabilise) | L5 | cut | – |
| 11 | 11_C063_carwash | 15.80–17.40 | C063 1.00 | L6 Agle saal, pakka. | push | L6 | cut | – |
| 12 | 12_C064_carwash_look | 17.40–19.00 | C064 6.72 | L6 | base (stabilise) | L6 | cut to black | – |
| 13 | 13_end_card | 19.00–20.80 | – | — tumhara beta | – | title, sign-off, @satyajitmall | end | – |

**Runtime 20.80 s** (520 frames), 12 shots + end card, median shot 1.58 s.

**Checks on the preview:**
- `pregate` (`analysis/pregate_p1/`, `--profile ig-quiet --designed 19.0-20.8`): verify PASS, frame scan PASS (2 flags inside the end card). camera_fidelity FAILs every shot because it can't see the window or the rotation (CR-20261104 item 6).
- Reel-local `tools/window_fidelity.py` instead (`analysis/winfid_p1/WINFID.md`): 11/12 PASS, within ±0.003 luma of the camera, NCC 0.95–0.99 vs camera (the gap is the depth blur), 1.00 vs the bake. 01_C047 flags crush 9.9 → 15.9 % (the bake's deepest shadows ~1 code value lower; < 0.05 share unchanged): allowed in the brief.
- Phone copy: 27.4 MB, −14.1 LUFS, −1.0 dBTP.

## Checkpoint 1 — Director notes on p1 (2026-11-09)
> "no slow motions no cinmeatic effect"

Read as: the cut plays in real time as plain handheld clips; the director wants slow motion and the camera-led "cinematic" of the profile (steady visible moves, drama from holds and slow motion, natural picture), **not** looks, leaks or transitions (profile: plain cuts, never processed).

## Checkpoint 1 — Changes for v1b (`analysis/edl_v1b.json`, `tools/build_edl_v1b.py`)
1. **Slow motion on every shot** (preview: minterpolate; build: AE Timewarp Pixel Motion): 01 auto street 60 %, 02 driver turn 65 %, 04 parotta close 70 %, 05 cook's hands 50 %, 06 the hand-off 60 %, 07 vendor 80 %, 08 vendor close 75 %, 09 paan 70 %, 10 paan look 60 %, 11 foam 50 %, 12 look-up 60 %.
2. **One speed ramp:** 03 parotta, real time → 40 % as the parotta lifts (camera C054 from 1.00 s; lift ~1.8–2.1 s).
3. **Rack focus from the director's own depth data** (`cine_bake --rack`, f/1.4 on these three only, so the pull reads on a phone): 02 street → driver as he turns; 07 festival lights → vendor; 12 scooter → his face as he looks up.
4. **Stabilised** every shot (preview: fx_prerender tracker, zoom 1.06; build: Warp Stabilizer), and a **visible +10 % push** on every shot (eased).
5. Unchanged: letter, cut times on the downbeats, 4:3 window, camera-true colour, plain cuts, end card.
- Not done, and why: no looks, leaks, whips or flashes (director profile: plain cuts; "over processed"). Offered if the director wants more.

**v1b results:**
- Pregate PASS (`analysis/pregate_p1b/`, `--no-fidelity`; the window check stands in).
- Colour through the pre-render: unchanged (sat ±5 %, no matrix shift).
- Rack test: 12's first pull used a fixed face rect, but he moves as he looks up, so it focused on the wall. Fixed by ending the pull on the camera's recorded focus (`--rack` rect width 0).
- Stabilisation: turned off on 01 and 12, where the tracker followed in-frame motion (jitter rose 2.0 → 3.4 and 2.3 → 4.4 px).

## Checkpoint 1 — Director notes on p1b (2026-11-09)
> "There is lot of distortion and in and out focus in this and framing issue fix it"

What the frames showed (`analysis/v1c_diag/`):
- **Distortion:** minterpolate slow motion warps moving hands and objects. 06: the plate melts between frames. 03: the parotta edge doubles and the spatula ghosts at 40 %. 05, 11: fingers and arms smear. The tracker's roll/zoom corrections add wobble.
- **In-and-out focus:** my three rack pulls (02, 07, 12) at f/1.4, plus hands and the spatula moving through the f/2 focal plane. The camera's recorded focus itself is steady (range ≤ 0.11, frame step ≤ 0.008 on every used window).
- **Framing** (`analysis/v1c_diag/framing_p1b.jpg`): 04's face leaves the top of the window by the shot's end (centred +10 % push × stabiliser zoom 1.06); 03, 05 and 10 lose the top of the head; in 11 the scooter mirror covers the car-washer at the frame's edge.

## Checkpoint 1 — Changes for v1c (`analysis/edl_v1c.json`, `tools/build_edl_v1c.py`)
1. **Distortion:**
   - Slow motion only on calm human beats: 01 street 70 %, 02 driver turn 80 %, 07 / 08 vendor 80 %, 10 paan look 70 %, 12 look-up 75 %.
   - Every hands / work shot back to **real time** (03, 04, 05, 06, 09, 11). The parotta ramp is gone; the lift plays in real time.
   - Stabilise only the three shakiest shots (04, 07, 10), **position only** (no roll/zoom), zoom margin 1.04.
2. **In-and-out focus:**
   - **No rack pulls.** Every shot uses the camera's own recorded focus.
   - f/2 as shot, **f/2.8 on the hands shots** (03, 04, 05, 06, 09, 11), so hands don't swim in and out of the blur (per-shot call, as the director allowed).
3. **Framing:**
   - Push **+5 %** (was +10 %), **anchored on the window's top edge** on head-at-top shots, so heads stay in.
   - 04 reframed (Scale 90 @ x 760, top-anchored).
   - 11 moved to C063 2.0 s, shifted left (x 360) so he sits centre-right and the mirror no longer covers him.
- Unchanged: letter, cut times, 4:3 window, camera-true colour, plain cuts, end card.

**v1c as sent:**
- **Framing check, round 1** (`analysis/v1c_check/framing_p1c.jpg`): 04's close still cut his head, because he leans to the camera's own top edge after 3.9 s; a hands-only close read as a headless torso. 11 at C063 2.0 s hid his face behind the mirror.
- **Final:** L2 is one held shot (C054 0.32–3.44 s, head in frame throughout); 11 back to C063 0.9 s, shifted to x 470. **11 shots + end card.**
- **Slow-motion check:** 02, 07 and 08 at 80 % ghosted pedestrians and garbled the jewellery, so they're real time. Slow motion stays on 01, 10 and 12 only, checked clean frame by frame.
- **Checks:** pregate PASS. Window check: within 0.005 luma of the camera on every shot; 01 and 02 crush +3–4 % from the bake (allowed). Phone copy 27.7 MB, 10.4 Mb/s, −1.0 dBTP.

## Checkpoint 1 — Director notes on p1c (2026-11-09)
> "look at the reference, we are a little too far away from the reference; also look at stock footage we can add, so micro or macro subjects or some shots without the subject's face"

**Reference vs p1c** (`analysis/teardown_p1c/COMPARE.md`, `analysis/ref_shots/`):
- **Pace is not the gap.** teardown counts 43 cuts/min on the reference, but most of those "cuts" are its in-camera motion: a still seller with the crowd streaking past (4.8–7.8 s) and a panning rickshaw puller (13.1–14.1 s). Real shots: 9 in 20.3 s (1.0–3.2 s each). Ours: 11 (1.56–3.12 s).
- **The real gaps:**
  1. **No-face shots:** 5 of the reference's 9 (canopy, top-down rangoli maker, **macro marigold hands**, head down by candles, **hands bagging flowers**); ours 0 of 11.
  2. **Diwali objects up close:** marigolds, candles, rangoli, decorations. Ours: food stalls.
  3. **Motion inside the shot:** crowd blur around a still worker, a speed-blurred pan.
  4. **Text:** one small italic white line in quotes inside the picture, top-left; ours six lines under it.
  5. **Look:** graded film (teal-green shadows, deep blacks, marigold orange kept; teardown saturation 0.151 vs our 0.116); ours camera-true.
- **Stock:** 25 Pexels candidates on a board (`analysis/stock/stock_candidates.md`, `stock_board_1/2.jpg`); a recommended no-face insert per line. Nothing downloaded.

## Checkpoint 1 — Changes for v2 (`analysis/edl_v2.json` camera-true, `analysis/edl_v2_look.json` reference look; `tools/build_edl_v2.py`)
Director's answers (p1c round):
- **Stock:** "Recommended set" (download approved). S9 34579325, S24 34766750, S1 38001819, S14 34565062, S8 36424458 → `raw/stock/pexels-*/`, logged in `raw/SOURCES.md` (~70 MB).
- **Closer to the reference:** "Reference-like film look" only. Text and the rest stay.

What changed:
1. **Each line = our worker + a no-face insert:**
   - L1: auto (70 %) + S9 diyas in a row;
   - L2: parotta lift + S24 night market (60 fps → 42 % real slow motion);
   - L3: S1 Maa's hands making roti (50 fps → 50 %, +1.0 stop: the stock is underexposed) + our cook;
   - L4: vendor on his phone + S14 a hand taking aarti over the diyas;
   - L5: paan maker + his look (70 %);
   - L6: S8 ring of diyas (real time, +12 % push) + the car-washer looking up (80 %).
   - **6 of 11 shots without a face** (reference 5 of 9). Dropped from v1c: driver turn (02), cook hand-off (06), vendor close (08), car-washer foam (11).
2. **Reference look**, measured (`analysis/look_ref/STATS.md`): the reference is warmer in mids and shadows, has green-tinted highlights (G−M +0.063 vs our −0.003), rolled-off whites (p98 0.83 vs 0.89), slightly lifted blacks (p02 0.027 vs 0.013) and more saturated mids (0.40 vs 0.32). It is not teal in the shadows.
   - `tools/ref_match_lut.py` builds `analysis/look_ref/ref_match.cube` by per-channel quantile matching plus a saturation trim. At 100 % it lands on the reference (luma 0.318/0.317, sat 0.391/0.386, highs G−M 0.059/0.063).
   - Preview at **60 %**. Build: V3 adjustment layer, the .cube loaded by hand (Lumetri → Creative → Look → Browse), Creative Intensity 60 %.
3. **Pregate:** first run FAILED "frozen" on S9 and S8 (still lifes at low motion) → S8 real time, both pushed +12 % → PASS on both versions.
4. **Unchanged:** cut times on the downbeats, the letter, the 4:3 window, type, end card, plain cuts.

## Checkpoint 1 — Director notes on v2 (2026-11-09)
> "shots look a little too unrelated"

Read: the Pexels inserts come from other places, light and camera heights (a top-down diya ring on a blue floor, a top-down market in another city, a studio row of diyas), so they read as random cutaways next to our eye-level, street-lit workers. The look question (camera-true vs reference look) wasn't answered, so v2b goes out in both again.

## Checkpoint 1 — Changes for v2b (`analysis/edl_v2b.json`, `edl_v2b_look.json`; `tools/build_edl_v2b.py`)
1. **No-face shots from the same workers:** 1:1 macro crops of their own hands from our 4K clips (Scale 90 in 4K terms, ~31 % of the width, no upscaling), same place, same light. Rendered full size, stabilised position-only, f/4 so the hands stay sharp.
   - L2: parotta lift → his hands at the tawa (C054 4.0 s).
   - L3: S1 Maa's hands (the one stock clip kept: the line says "your hands") → the cook's hands plating (C052 1.2 s): hands to hands.
   - L4: vendor → the phone in his hand (C062 4.92 s).
   - L5: the paan maker's hands (C050 0.4 s) → his far-off look.
   - L6: the car-washer's soapy hands (C064 0.8 s) → he looks up.
   - L1: auto → the driver's head turn (back from v1c).
2. **Dropped stock:** S9 (diya row), S24 (market from above), S14 (aarti), S8 (diya ring). Files stay in `raw/stock/` in case they come back.
3. 7 of 12 shots without a face. Cuts, letter, window, type, end card unchanged. Both colour versions again.

**v2b as sent:**
- Pregate PASS on both versions.
- Macro frames checked (`analysis/v2b_check/v2b_frames.jpg`): hands in every crop. 09 also shows the paan maker's lowered face.
- Jitter by phase correlation is dominated by moving hands on the macros (05 18 px, 11 9 px, 04 7 px), so camera shake can't be read there. Warp in the build, then `shake_report` on a background region.

## Checkpoint 1 — Director notes on v2b (2026-11-09)
> "the micro and macro shots are somehow unrelated to the topic"

Read: the hand macros were on-style (same place, same light) but about work, not about missing home on Diwali. Two misses in a row (off-style stock, then off-topic macros), so I showed options before building:
- **Own Diwali footage** (`analysis/topic/own_diwali_board.jpg`):
  - **C043 is Kolkata** (GPS 22.54 N 88.34 E, 1 Nov 18:00): Victoria Memorial lit at night, recoverable at +2.5 stops, the director's home in their own footage.
  - **C056–C058 are the Diwali stage show at the same fest** as the stalls (C050–C058 within ~80 m, 19:28–20:02).
- **Topic stock** (`analysis/stock/stock_board_topic.jpg`, N1–N16): A home's Diwali, B Diwali around them, C the call home.
- **Director's pick: "Their fest + Kolkata"** (recommended).

## Checkpoint 1 — Changes for v2c (`analysis/edl_v2c.json`, `edl_v2c_look.json`; `tools/build_edl_v2c.py`)
1. **Inserts:**
   - L1: auto → C043 Kolkata at night (+2.3 stops).
   - L2: parotta → C058 the Diwali show at the same fest.
   - L3: S1 Maa's hands → the cook plating (wide, not the macro).
   - L4: vendor on his phone → N14 a couple in Diwali clothes waving into a phone (Pexels 8811028, Yan Krukau, 13 MB, downloaded as part of the pick).
   - L5: paan maker → his look.
   - L6: C043 Kolkata again (deliberate callback: home next year) → the car-washer looks up.
2. **Dropped:** every hands macro (they read as off-topic), S9, S24, S14, S8.
3. Cuts, letter, window, type, end card unchanged; both colour versions again.

**v2c as sent:**
- Pregate first FAILED both Kolkata shots ("black", "frozen"). The preview's exposure is in linear light, so +2.3 stops barely lifted a clip whose median is pure black, and an eased push read as a freeze.
- Fixed: a pre-rendered RGB curve (`0/0.01 0.02/0.14 0.06/0.40 0.15/0.66 0.4/0.90 1/1`, clip ≤ 0.04 %), light temporal denoise, and a linear +10/12 % push. PASS on both versions. Frames checked (`analysis/v2c_check/v2c_frames.jpg`).
- Build note: C043 needs a Lumetri RGB curve (UI) or a curve preset, plus AE denoise. 8-bit noise is visible at full size.

## Checkpoint 1 — Director notes on v2c (2026-11-10)
> "why are random shots of Victoria used, they serve no purpose; can we not use close-up shots of handling or selling flowers and fire crackers?"

- Kolkata (C043) out. Board `analysis/stock/stock_board_flowers_crackers.jpg` (F1–F12).
- No free site has a firecracker stall or seller (Pexels: fireworks in the sky only; Pixabay: generic shops). The closest is hands with sparklers. An AI cracker stall was offered (~$0.52, labelled); not chosen.
- **Director's picks:** L1 **F8** (Pexels 8811075, Yan Krukau: hands laying marigolds), L6 **F9** (Pexels 6618563, Mariam Antadze: hands holding burning sparklers). Both downloaded (9 + 14 MB), logged in `raw/SOURCES.md`.

## Checkpoint 1 — Changes for v2d (`analysis/edl_v2d.json`, `edl_v2d_look.json`; `tools/build_edl_v2d.py`)
1. 02 = F8 marigold hands (real time, top-anchored push).
2. 11 = F9 sparkler hands (4K 30 fps at 25 → 83 %, real frames; window band at v 0.55).
3. Everything else = v2c. Pregate PASS on both versions; frames checked (`analysis/v2d/new_inserts.jpg`).

## Checkpoint 1 — Director notes on v2d (2026-11-10)
> "the shot where a random couple is there, change; and where fire cracker is being burnt is too elegant; and man in the jewellery stall, the video glitches there; and look at the reference videos, the video there has some slow down, has a cinematic effect"
> (mid-turn) "I need more of my footage to be used; if you want to extend the reel timing go ahead"
Answers: **extend, audio later** (guide looped as placeholder); stock kept: **S1 Maa's hands, F8 marigold hands** only.

Findings:
- **Vendor glitch:** a one-frame jump at 9.96 s (43 px, frame diff 35 vs ~5). The camera file is clean (no drops, no jumps), so it was the preview stabiliser losing track and snapping.
- **The reference's "slow down"** is not slow motion. It is a **step-print stutter**: in the crowd shot (4.8–7.8 s) and the rickshaw pan (13.1–14.1 s), each new image is held 3 frames (≈ 8 images/s at 24 fps) with shutter smear, while the seller stays still. Per-frame diffs `52.6 0.0 1.1 28.4 0.1 0.1 …`. 63–65 % of frames in those shots are near-duplicates; 0 % elsewhere.

