# Brief — written by the editor, approved by the director

**Status:** approved 2026-10-20 (v1, hook H1; reel `.cube` loaded by hand OK). **Round 1b amendments** (director notes on the previz): eye-match dissolves + bloom flash, eye-lock stabilisation, **G2 Gold & Shadow** grade instead of Match reference. See `project.md` "Round 1b". **Round 2 (v2, director approved storyboard B on 2026-10-21):**
- a bonedi-bari act between the hook and the faces;
- an **AI-generated esraj** opening (labelled) instead of the Pexels band;
- C074 / C076 / C084 dropped.

The §2 hook, the §4 pace table and the §5 clips below are updated for v2. Older lines stay for history, marked *(v1)*.

## 0. CURRENT PLAN: v10 (round 5 + review-gate fixes + the v10 quality pass; Premiere sequence `Reel_uski-aankhein_v10`). This section overrides everything below, including the v4/v5 plan after it.
- **Concept** (director: "Like the reference"): calm and intimate, the reference's structure. v7: **one idol per shot** (director, round 5b): the red clay Durga (under the singer), the white sholapith Durga, the giant clay face.
- **v10 quality pass** (director, on the v9c file on iPhone: "very poor quality": soft, plastic faces, blocky darks; picked "Real frames + wider"): A and B are a stack of 21 aligned real frames (no Real-ESRGAN, no strong denoise), framed wider so enlargement stays ≤ 1.42× (A eye pair 27 → 31 % of the width, B 26 → 31 %); C keeps its framing with the denoise only in the shadows; clarity 0.08. Delivery is encoded from a Premiere ProRes 422 master: H.264 High, CRF 15, ~14 Mb/s (`tools/encode_hq.sh`). This overrides the A/B eye spans and the AI notes below.
- **Shots** (`tools/bake_r10.py` → `renders/bakes_r10/V1_timeline_v10.mov`; v9c was `tools/bake_r9c.py`, on `tools/bake_r9b.py`; A/B/C from `bake_r5.py` / `bake_r7.py` with the v9 review fixes):

| # | Time (s) | Shot | Move |
|---|---|---|---|
| A | 0–7.88 | the singer (AI esraj, labelled) as a Screen double exposure over her face (Oct17 C163, its sharpest frame). v9b: **the player sits on the left, her eyes stay clear** (the reference's split): the ghost layer moved left/up, strongest on the left and fading over her face, a soft hole over her eyes; its haze taken back out so blacks match B and C | slow push (eyes 36 → 42 % of width); fade from black |
| B | 7.88–16.00 | **the white sholapith Durga** (Oct18 C208): her sharpest frame, denoised and AI-enhanced once (v8: per-frame AI + slow motion shimmered); v9b: AI 55 % over the plain enlargement (20 % on the gold nath) so detail reads photographic; **title over her 8.60–11.80** | smooth push (eyes 42 → 54 %) with a 1 % lateral drift |
| C | 16.00–21.96 | **the giant clay face** (Oct17 C162 5.77–6.94 live: the glide lands on her, eye-locked, denoised, **deflickered**), then held on the last live frame; v9b: the scaffold band at the bottom darkened (soft grad); end card 20.6–21.96, on the chin (y ≈ 1245); black on 21.96 | push continues to the last frame (60 → ~70 %) |

- **Transitions** (director: "Exactly like the reference"): the opening double exposure, then the reference's **blink** on 7.88 (the drop) and 16.00 (the 16.02 accent); nothing else.
- **Quality** (director: "Tight eyes first" + "Install AI upscaler"):
  - every close-up crop is AI-upscaled with Real-ESRGAN x4plus at source resolution (`tools/realesrgan/`), then scaled to 1080×1920;
  - no unsharp;
  - grain 6 %;
  - standard-range (tv) encodes.
- **Look:** **Rich & deep** (director, round 5c): `grade/uski_aankhein_G2r_rich_deep.cube` (G2 Gold & Shadow + split-tone: gold highlights, slightly cool deep shadows; soft mid contrast) on V3, loaded by computer use ("You do it on screen"); local clarity baked into V1. Light flicker removed (per-frame deflicker on the clay face's live frames).
- **Sound:** reference audio; booms at 7.84 and 15.96 (the two blinks), −16 dB.
- **Idols allowed:** Durga + art statues (director); this version uses three Durgas, one per shot: red clay (A), white sholapith (B), giant clay face (C).

## (superseded) v4 (round 4, director-approved 2026-10-23); history.
- **Story:** the esraj plays → on the string swell, a blink, and **her eye opens** → the house (one bonedi house, "house B" of the Oct 20 night: chandelier, cast-iron arcade, her ekchala) → her eyes held still while the house slides past → the run on the drum strokes → a sweep lands on her face → blink → her eyes, frozen, slow push → black.
- *(v4, superseded by v4b)* **One place:** every shot except the AI esraj is from house B (Oct 20 C048/C049/C050, 21:25–21:28). The photo, shrine, darshan and the other pandals' faces are gone (director: "too many places", "no flow", "middle act doesn't fit", "shots weak").
- **Shots, v5** (round 4d, the director-approved composition board `analysis/comp_v5/board.jpg`). Eyes are the subject of every shot, framed tight, with one designed move each (EDL `analysis/edl_v5.json`, bake `tools/bake_v6.py`):

| # | Time (s) | Clip | Shot (eyes as % of frame width) | Move | In |
|---|---|---|---|---|---|
| 1 | 0–4.16 | AI esraj | instrument, hands, bow | — | fade from black |
| 2 | 4.16–7.88 | Oct17 C163 | red clay Durga, eyes 40 → 52 %; title over her | slow push | singer fades into her (double exposure 2.40–4.16) |
| 3 | 7.88–11.80 | Oct17 C154 1.00–4.27 | stone mother, face only, eyes 40 → 46 % | the real camera orbit, eyes locked | **blink** on the drop + boom |
| 4 | 11.80–14.52 | Oct18 C200 3.90–6.17 | crown and third eye, then her eyes (34 → 36 %) | tilt reveal (eyes rise from 62 % to the 40 % line) | **blink** |
| 5 | 14.52–15.68 | Oct17 C154 0.00–0.97 | stone mother eye close-up (44 → 46 %) | slight push | hard cut on the stroke |
| 6 | 15.68–16.92 | Oct18 C208 2.90–3.93 | white sholapith (46 → 52 %) | push | hard cut on the stroke |
| 7 | 16.92–18.08 | Oct17 C162 6.17–7.14 | giant clay face (60 → 68 %) | push | hard cut on the stroke |
| 8 | 18.08–19.60 | Oct17 C164 2.82→1.55 reversed | lands on her eyes (45 %) | whip | hard cut on the stroke |
| 9 | 19.60–21.96 | Oct17 C164 @1.55 | her eyes, frozen (45 → 56 %); end card | slow push | **blink** + boom |

- **Transitions:** the reference's blink, measured frame for frame on Video-14732 (7.93 and 16.02 s).
  - Straight top and bottom lids with a wide soft edge close to a slit on the eye-line over 3 frames, black on the beat frame, then the next shot opens over 3 frames.
  - Blinks on the accents 7.88, 11.80, 19.60; the opening (4.16) is the singer fading into the idol (v4c); **hard cuts on the drum strokes** in between; **no dissolves, no bloom** (director, round 4).
- **Look:** **G2b2**, Gold & Shadow at −17 % contrast with black and white anchored (`grade/uski_aankhein_G2b2_gold_shadow_c18.cube`) on the V3 adjustment layer, vignette as before. Director: "gold and shadow but a little reduced contrast".
- **Type:** title USKI AANKHEIN / *if her eyes were music* 4.48–7.48 s over her (slot 2), blur-out before the drop; end card unchanged.
- **Sound:** reference audio (the IG upload uses the same song at the same start point), booms at 7.84 and 19.56 s at −16 dB.
- **Must-haves:**
  - her eyes on the 40 % eye-line in every face shot;
  - the double-exposure fade ending exactly on the 4.16 swell; blinks exactly on 7.88 / 11.80 / 19.60;
  - hard cuts on the strokes;
  - one house;
  - the AI shot labelled (IG AI info at posting).
- **Must-nots:** dissolves, ghosts or double exposures over the title; ornate gold-heavy idols; idols outside Oct 16–18; phones.

## 1. The idea
- **Reel type:** music-montage (no speech; the reference's own audio is the soundtrack).
- **Playbook:** cinematic-montage. **Overrides** (each with its reason):
  1. *(v1)* **One stock clip allowed** (director profile says "no outside stock footage"): the director asked for a bowed-string player like the reference's intro and chose Pexels 4221987. It is used only as a blended layer in the hook, never as a shot of its own. **v2: dropped.** It isn't the reference's instrument and didn't read (director: "not strong and recognisable").
  1a. **v2: one AI-GENERATED shot, labelled.** The opening esraj (0–2.4 s, then a Screen ghost over her eye until about 3.3 s).
     - *Why:* the reference's player holds an esraj and the soundtrack is esraj. The director's shoots have no esraj. Pexels, Pixabay and a reverse image search found no licensable clip.
     - *Director's terms:* "instrument close up only and arm and legs, no face".
     - *Model:* Veo 3.1 Lite via OpenRouter (`scripts/gen_video.py`). Draft $0.12 (720p, 4 s), final $0.40 (1080p, 8 s, 24 fps conformed to 25 frame-for-frame). Total **$0.52** of the $2 cap, both runs approved by the director.
     - *Prompt:* in `renders/gen/esraj_open_final_20261022-102213.json`.
     - *Label:* "AI-generated (Veo 3.1; SynthID watermark)". **Turn on Instagram's AI info label at posting.**
  2. **Look = G2 Gold & Shadow** (round 1b). The director first picked Match reference (A), then saw it in motion and said "cinematic colours grading is not there at all"; G2 was picked from three cinematic options. Its contrast, saturation and luma are deliberately above the reference's measured grade.
  3. **Slow open instead of a hard 3 s hook**: the music is a quiet bowed-string intro and the reference opens slowly. Motion from frame 1 comes from the bow in the double exposure, a slow push and a crop that follows the camera's drift.
  4. **Runtime 22.0 s**, under the 30–45 s default: the soundtrack is 22.0 s and ends on a hard accent.
  5. **Words: title + one English line + end card** (playbook: title + end card only). The English line is the title's meaning, not a beat word.
  6. **One freeze frame** (effects playbook §C) for the payoff. An idol doesn't move, so the freeze reads as the camera stopping on her eyes.
  7. **Eye-match dissolves** (v2: 8 dissolves + bloom + freeze, listed in §4 Effects & transitions; round 1b, director: "jumps are odd", "transitions are not cinematic"): 7 dissolves of 4–12 frames centred on the beats, plus a 4-frame bloom flash on the rhythm drop. This is more than the playbook's 3–4 non-cut transitions per 30 s and its "hard cut by default". The eyes sit on the same line in every shot, so a dissolve morphs one goddess's eyes into the next; that is the concept.
  8. **V1 is baked outside Premiere** (v2: `tools/bake_v3.py` + `analysis/edl_v2.json` → `renders/bakes_v3/V1_timeline_v3.mov`; v1: `tools/bake_v2.py` → `renders/bakes_v2/V1_timeline_v2.mov`). In v2 the esraj ghost over C163 is baked into V1 too, so there is no V2 track. Every shot's 9:16 crop, push, eye-lock stabilisation, 25 fps conform, 180° fix, per-clip primary correction (grey balance + exposure to one target), pre-look halation, the dissolves, the bloom and the fade-in are all in that file. Primary correction is still per clip and on the clip. The creative look stays on the V3 adjustment layer in Premiere.
- **One-line concept:** *If her eyes were music.* Durga's eyes, from ten pandals across five nights, cut to a bowed-string melody. Every shot puts her eyes on the same line of the screen, so the goddess changes while her gaze stays.
- *(v1)* **Story arc:** the music is born over her eyes (bow over the eye) → silence, just her eyes → the rhythm enters and her eyes multiply (pandal after pandal, faster) → the camera finds the giant face and stops dead: the third eye.
- **v2 story arc (storyboard B):** the esraj plays (hands, bow, no face) → its ghost dissolves into her eye → an old bonedi-bari family photograph: generations of this puja → silence: inside the house, the shrine glowing under the red valance (v2b: the doorway crop put the shrine behind the IG UI) → the drop blooms into the bonedi Ma's face → a devotee's darshan in the thakurdalan → the rhythm: her many faces, eyes on one line, faster → the giant face stops dead on the accent.
- **Goal:** viewers feel held by her gaze, then save and share. *(Assumed from the concept; change at Checkpoint 1 if wrong.)*
- **Audience:** @satyajitmall followers and Durga Puja / Kolkata audiences, Bengali and Hindi speakers. *(Assumed.)*
- **Target length:** 22.0 s (fixed by the music).

## 2. Hook (0–4.16 s)
**v2 (storyboard B):**
- **0–2.16 s: the esraj** (v3b; was 0–2.40) (AI-generated, labelled). Close-up of the instrument, the bowing hand in a white chikan sleeve, the fingers on the frets, folded legs, no face. Full frame, with its own slow push. Fade from black over the first 0.32 s.
- **2.40–4.16 s: her eye.** A 16-frame dissolve into Oct17 **C163** (eye-locked on the eye-line). The esraj stays on as a Screen ghost (45 %), clearing by 2.80 s (v3b; was 3.3 s), so her eye gets a clean beat. Dissolve to the photograph on the swell accent at **4.16 s**.
- **On-screen text:** **USKI AANKHEIN** + *if her eyes were music*, **2.40–4.08 s** (v3b, director: "start with her eye"). It rises once the instrument has dissolved into her eye: the cut moved to 2.16 s (12 frames), and the esraj ghost is gone by 2.80 s. It has blurred out by the photo dissolve (4.00–4.32 s, 8 frames; < 5 % opacity from 4.00). It is never over the instrument or the photo. 0–2.16 s is the esraj alone.

*(v1 hook, kept for history:)*
- **Moment:** Oct17 **C163**, red Durga in incense haze, eyes on the eye-line, source 0.00–3.48 s (30 fps clip interpreted to 25 fps: 4.18 s on screen). Cut on the string swell accent at **4.18 s**.
- **Visual move:** the Pexels instrument neck + bow as a narrow feathered band (≈300 px) across her eyes (V2 `stock_band_v2.mov`, Screen 65 %, fading out 3.60–4.16 s). Slow push 3.3× → 3.7×, eyes locked on the eye-line (tracked). Fade from black over the first 0.32 s (frames 0–2 read as black: deliberate).
- **On-screen text:** **USKI AANKHEIN** with *if her eyes were music* under it, 0.6–3.8 s, focus-pull settle, below the face.
- Preview (rough, not the final grade): `analysis/look_test/hook_double_exposure_preview.jpg`.

## 3. References → concrete parameters
| Reference | What we take from it | Measured (`analysis/teardown/`, `analysis/ref_grade/ref_grade.json`, `analysis/audio_summary.md`) |
|---|---|---|
| `references/Video-14732.mp4` ("IF EYES IS A MUSIC", 960×720 letterboxed, 22.13 s) | The idea (eyes = music), the bow-over-eye double exposure, the slow intimate pace, the soundtrack, the grade | 2 shots: first cut 7.93 s, shots 7.93 / 14.19 s, motion 4.54 (calm), 0 flashes. Grade (picture area): luma 0.28–0.30, p02 0.065 (lifted blacks), p98 0.50–0.57 (no whites), saturation 0.23, mids R/G 1.41–1.60, B/G 0.60–0.63 (warm amber), shadows R/G 1.41–1.60, B/G 0.84–0.86. Audio −14.1 LUFS, −1.0 dBTP, 99.4 BPM |

**Where we deliberately differ:** the reference holds one live face for 14 s, and a living eye blinks and glances. Idol eyes don't, so we cut (director chose "Mixed" pace). We go full 9:16 with no letterbox (director's choice).

## 4. Treatment
### Pace
- **Sequence:** 1080×1920 at **25 fps** (7 of the 11 shots are 25 fps). The 30 fps clips (C163, C208, C168 and the stock) are conformed by interpretation and play at 0.83×. That's calm and fits; source ranges are scaled (CLAUDE.md §3).
- **Energy arc** (the music, measured):

**v2 energy arc:**

| Section | Time | Music | Shots | Shot length |
|---|---|---|---|---|
| Birth | 0–4.16 | bowed-string intro → swell accent | esraj (AI) → her eye (ghost) | 2.40 / 1.76 s |
| The house (silence) | 4.16–7.88 | decay to near-silence | bonedi photo → the shrine (medium) | 1.88 / 1.84 s |
| Rhythm enters | 7.88–11.80 | the drop (bloom + boom), 99.4 BPM | bonedi Ma → darshan | 1.20 / 2.72 s |
| Her faces | 11.80–19.02 | rhythm, rising | C139 bar hold, then C145 / C208 / C112 / C200 2-beat run, each cut on a loud stroke (14.52 / 15.68 / 16.92 / 18.08) | 2.72, then 1.16 / 1.24 / 1.16 / 0.94 s |
| Payoff | 19.02–21.99 | louder; final accent 21.99 | C168 sweep 0.58 s + freeze 2.39 s | |
| Out | 21.99–22.0 | music ends abruptly | cut to black | |

v3 cut frames at 25 fps: 60 / 104 / 151 / 197 (bloom) / 227 / 295 / **363 / 392 / 423 / 452** (run cuts on the percussion strokes, director round 3) / 475 / 490 (freeze); picture ends at 549, audio at 550 (22.00 s). 12 shots (13 EDL rows).

*(v1 energy arc:)*

| Section | Time | Music | Shots | Shot length |
|---|---|---|---|---|
| Birth | 0–4.18 | bowed-string intro (≈ −22 dB) | 1 (hook, double exposure) | 4.18 s |
| Breath | 4.18–7.89 | swell, then decay to near-silence (−48 dB at 7.0 s) | 1 (pure eyes) | 3.71 s |
| Rhythm enters / build | 7.89–14.23 | rhythm at 99.4 BPM | 3 | 1.21 / 2.70 / 2.43 s (bar holds) |
| Full | 14.23–19.02 | rhythm, rising | 4 | 1.2 s each (2 beats) |
| Payoff | 19.02–21.99 | louder; final accent 21.99 | 1 shot: sweep 0.58 s + freeze 2.39 s | |
| Out | 21.99–22.0 | music ends abruptly | cut to black | |

- 10 shots (11 EDL rows), median shot ≈ 1.2–2.4 s. Every cut is centred on a measured beat (±1 frame at 25 fps). Cut frames at 25 fps: 104 / 197 / 227 / 295 / 356 / 385 / 416 / 445 / 475 / 490 (freeze); the picture ends at frame 549 (one black frame), audio at 550 (22.00 s). Transitions: see Effects & transitions.

### Colour
- **Primary correction (per clip, baked into V1, round 1b):** partial grey balance (wb 0.5) + exposure to luma 0.30 (≤ +1 stop), from each shot's middle frame. Gains are in `renders/bakes_v2/bakes_v2.json`. Then a warm halation glow on the highlights (0.22). Per-clip intent:
  - C163: heavy red/orange haze; pull saturation and red.
  - C208: cold flat white light; warm it toward neutral, lower highlights.
  - C074: near-monochrome dark mask; lift mids a little.
  - C139: strong orange; trim saturation.
  - C076: yellow sodium; trim yellow, recover highlights.
  - C145: busy gold.
  - C025: dark with black pillars; keep blacks, lift the face.
  - C112: bright; lower exposure.
  - C083: pastel, flat, bright; lower exposure, add contrast.
  - C168: purple/blue light on orange skin; tame magenta.
  - Stock: daylight green-grey; desaturate, warm.
- **Shot matching:** all shots to one luma ±0.03 before the look. Faces' midtones matched across cuts, since the eyes sit on the same spot and any jump shows.
- **Creative look (V3 adjustment layer): G2 Gold & Shadow** (`grade/uski_aankhein_G2_gold_shadow_v1.cube`, `tools/grade_options.py`), loaded in Lumetri → Creative → Look at Intensity 100.
  - The look: a filmic S-curve (contrast 1.55, blacks to 0, highlights to 0.97), a warm gold split (mids R ×1.15 / B ×0.72), saturation 1.0.
  - On the same Lumetri, a vignette: Amount −1.0, Midpoint 45, Feather 70.
  - The match-reference look (`grade/uski_aankhein_reference_look_v1.cube`) is retired.
- **Texture (V4):** film grain at Overlay 12 %, baked at 25 fps (`renders/texture/grain_25fps_v1.mov`). It fades in from neutral grey with the picture. No light leaks.

### Effects & transitions (signature only)
**v2 (current):**
1. **Opening (0–2.40 s):** the AI esraj, full frame, fading up from black over 0.32 s.
2. **Esraj → her eye (2.40 s):** 16-frame dissolve. The esraj stays on as a 45 % Screen ghost over C163, clearing by ~3.3 s (baked into V1).
3. **Dissolves** (`analysis/transitions_v3.json`, 7 in total):
   - 2.16 s (12 frames; v3b, was 2.40 / 16), 4.16 (8; v3b, was 12), 6.04 (10);
   - v3: 14.52 (6), 15.68, 16.92 and 18.08 (4 each), on the strokes; v2 had them at 14.24 / 15.40 / 16.64 / 17.80.

   **Hard cuts** at 9.08 (face → room on the stroke; v2c, review loop 2), 11.80 (the accent into the faces) and 19.00 (into the sweep). **Bloom flash + boom** on the drop at 7.88 s (frames 196–199).
4. **Locks:**
   - eye-lock on every face shot: pupils at y ≈ 768, ±30 px;
   - shrine-lock on C059, which plays 3.30–4.28 s and then holds under the push;
   - C037 locked with a push;
   - C056 keeps its forward move with the jitter removed.
5. **Sweep → freeze → cut to black:** as v1 (items 5–6 below).
- Non-cut transitions: the fade from black, 7 dissolves, the bloom flash and the freeze (override 7). Title out: 0.7 s blur-out (v2c). The bonedi act runs medium shrine → close Ma → wide darshan (a pull-back reveal).

*(v1:)*
1. **Double exposure (0–4.18 s):** bowing band across the eyes, Screen, fading out 3.6–4.18 s.
2. **The breath (4.18–7.89 s):** C208 alone in near-silence, slow push. No effect: the silence is the effect.
3. **Rhythm entry (7.88 s):** a hard cut into C074 (the mask's huge eyes) with a 4-frame **bloom flash**: a warm highlight glow + lift on frames 196–199, peaking on the beat frame 197. Plus the bass boom.
4. **Eye-line lock + stabilisation (all shots but the sweep):** her eyes are tracked in every source frame (`tools/track_eyes.py`) and pinned at y ≈ 768 px (40 % down), centred.
   - No exceptions since the review-gate fixes: every shot's pupils sit within ±30 px of y 768, centred.
   - Handheld jitter on the holds is ≤ 3 px RMS (`analysis/shake_previz_v1b.json`).
4b. **Eye-match dissolves** at 4.16 s (12 frames), 9.08 (6), 11.80 (8), 14.24 (6), 15.40 / 16.64 / 17.80 (4 each). Hard cuts at 7.88 (bloom) and 19.00 (into the sweep).
5. **Sweep → freeze (19.02–21.99 s):** C168's real camera pan slides the giant face in; on the 19.60 accent it stops dead (freeze at source 2.30 s), then a slow push (2.2× → 2.6×) drifts up toward the third eye + sub-hit.
6. **Out:** cut to black on the final accent at 21.99 s.
- Non-cut transitions: the fade from black, 7 dissolves and the bloom flash (override 7).
- Motion: slow eased pushes on C163, C208, C139 and the C168 freeze. No shakes and no snap zooms. The eye-locked shots are steady; only the C168 sweep keeps its real camera pan.
- No After Effects (denoise only if the frame scan flags noise on C025 / C074).

### Type & graphics
- **Title:** USKI AANKHEIN, DIN Condensed Bold, cream `#F5E6C8` with a dark halo (calm reel), ~120 px. Under it, *if her eyes were music* at ~48 px. Focus-pull settle (HyperFrames, ProRes 4444 alpha on V5), 0.6–3.8 s, centred at about y 1400–1560, below the face and inside the safe zone.
- **End card:** @satyajitmall, small, 20.6–21.99 s, at about y 1500, over the chin and neck of the frozen face, clear of the eyes.
- No captions and no beat words.

### Sound
- **A3 music:** the reference's audio (`references/ref_audio.wav`, 22.0 s, 99.4 BPM), full level. It's already −14.1 LUFS / −1.0 dBTP, so no ducking.
- **A1:** clip natural sound muted.
- **A2 SFX** (prepped with `sfx_prep.py`): `gemini_bass_drop_boom` placed at 7.84 s and 19.56 s, so the audible onset lands ≈20 ms before the 7.88 / 19.60 cuts. −16 dB.
  - No whooshes. Per the playbook they go only on real fast motion, and the C168 sweep is moderate (≈0.3 frame-widths per second). If the sweep reads fast in the cut, a soft whoosh at −13 dB is the only candidate.
- **Exports:**
  - `_mix`: guide with the reference audio, −14 LUFS ± 2;
  - `_IG`: no music, SFX only, `--profile ig-quiet`. The director adds the IG audio at upload.

## 5. Clips
**v2 clips** (EDL `analysis/edl_v2.json`, transitions `analysis/transitions_v3.json`):

| # | Clip | fps | Role | Notes |
|---|---|---|---|---|
| 1 | **AI esraj** `renders/gen/esraj_open_final_20261022-102213.mp4` | 24 → 25 | opening | **AI-GENERATED** (Veo 3.1 Lite, $0.40 final + $0.12 draft). Source 0.6–3.0 s, full frame, wb off. Label it at posting |
| 2 | Oct17 C163 | 30 | her eye + esraj ghost | eye-locked, push cw 0.40 → 0.36 (≤ 1.4× upscale), black point 0.05, sat 0.72, mild sharpen, −0.05 stop; ghost 45 % Screen, clearing by 3.3 s |
| 3 | Oct20 C037 | 25 | bonedi photograph | old family photo on the bonedi-bari wall, 4K; push 0.56 → 0.50 with the photo high in frame (v 0.42), so the junction box above is out and only the picture-light bar shows; locked from frame 1; sat 0.72, lift 0.02 |
| 4 | Oct20 C059 | 25 | the shrine (inside the house) | medium shot of the shrine under the red valance, the central Durga's face at y ≈ 1185 (above the IG bottom zone). The source frames the idol cut off at its bottom edge, so the doorway crop put the shrine behind the IG UI. Shrine-locked, cw 0.46 → 0.42, v 0.72; plays 3.30–4.28 s, then holds under the push; −0.5 stop. Deliberate low-key beat (luma 0.15 vs 0.25 median) |
| 5 | Oct20 C050 | 25 | bonedi Ma, face close | steady, eye-locked; replaces C045 (motion-blurred) |
| 6 | Oct20 C056 | 25 | darshan | a devotee in silhouette before Ma in the thakurdalan; forward move kept, jitter removed |
| 7–11 | C139, C145, C208, C112, C200 | | her faces | as v1c (see below); C200 cw 0.30 (was 0.25); mild sharpen on C112 / C200 / C050 |
| 12–13 | Oct17 C168 | 30 | sweep + freeze payoff | as v1c |

Dropped in v2: C074, C076, C084 (least stable), Pexels 4221987 (wrong instrument). Shots 3–5 show one house and one Ma (wide → close); that's deliberate, not a repeat.

*(v1c clips:)* All idol clips are vertical (2160×3840 or 1080×1920). Ids repeat across shoots, so each is named with its shoot. EDL: `analysis/edl_v1c.json` (v1 + round 1b + review-gate fixes). Survey: `analysis/survey/eyes_candidates.md`.

| # | Clip | fps | Role | Notes from the analysis |
|---|---|---|---|---|
| 1 | Oct17 C163 | 30 | hook | 4K static, then a slow drift right after 2.3 s (eye-locked). Unused in any final cut |
| 2 | Oct18 C208 | 30 | the breath | sharpest face in the pool, static; used in pujo-ki-asolei-sobar's hook |
| 3 | Oct15 C074 | 25 | rhythm entry | Khambeshwari mask (a form of Shakti) with huge eyes, 1080p; source from 10.12 s at 1.8×, eye-locked (tilt cancelled). Unused |
| 4 | Oct16 C139 | 25 | bar hold | classic Kolkata face; **upside down → rotate 180°**; soft before 9.52 s (we start at 9.60); puja-night-2's hero |
| 5 | Oct15 C076 | 25 | bar hold | golden profile, lowered gaze, 1080p; plays 16.04–17.68 s, then holds the last frame under the push (the 17.72–18.44 s camera lurch is cut out); used in my-reel |
| 6 | Oct17 C145 | 25 | 2-beat | gold Durga; a pujo-ki-asolei-sobar insert |
| 7 | Oct16 C084 | 25 | 2-beat | pastel Durga, low angle, 4K, **upside down → rotated 180°**, source 1.04–2.44 s (sharp), eye-locked through the camera pan; replaces C025 (review v1: too dark, pillarboxed) and then C120 (review v1b: focus miss). The pastel idol of the dropped C083, so no repeat. Unused in any reel |
| 8 | Oct16 C112 | 25 | 2-beat | red-sari Durga; **upside down → rotate 180°**; used in puja-night-2 |
| 9 | Oct18 C200 | 30 | 2-beat | dark-skinned Durga under a red halo, purple pandal light, 4K at 4×, eye-locked; replaces C083 (review v1: face at the source edge, eyes could not be centred). Unused |
| 10–11 | Oct17 C168 | 30 | sweep + freeze payoff | giant face, kohl eyes, third eye, purple light, diyas. Unused |
| — | Pexels 4221987 | 30 | V2 layer in the hook | bowed folk instrument, 1280×720 daylight; source 10.0–13.5 s (strongest bowing). Pexels License |

Reuse: 5 of the 10 idols appeared in earlier reels (C084's idol was in puja-night-2 via C083/C081). Unused shots: C168, C163, C074, C084 and C200.

## 6. Must-haves / must-NOT-haves
- **Must:**
  - her eyes on the same line in every face shot (v2: shots 2, 5, 7–13);
  - v2: the esraj (hands, bow, no face), then its ghost over her eye;
  - v2+: the near-silence holds the house (the photograph, then the shrine), not her eyes alone;
  - the stop-dead freeze on the giant face;
  - every cut on a measured beat;
  - title and end card clear of the eyes and face.
- **Must not:**
  - the same idol twice (v2 exception: the bonedi act shows one Ma three times: the shrine medium, her face close, then the wide darshan);
  - phones or raised screens in frame (C058 dropped for one);
  - whooshes under the title;
  - light-leak transitions or stacked decorative looks;
  - more than one AI-generated shot. v2 has exactly one, the esraj, labelled in-brief and with IG's AI info label at posting.

## 7. Open questions
- ~~IG audio at upload~~ answered (round 3): the same song at the same start point as the reference, so the cut stays timed to the reference audio. *(Original question:)* which Instagram track (and start point) matches the reference's audio? The cut is timed to the reference's 22 s: bowed intro, near-silence 4.8–7.7 s, rhythm from 7.89 s. If the IG track starts elsewhere, the cuts won't line up.
- ~~Grade LUT~~ answered: the `.cube` is loaded by hand (done 2026-10-21).

## 8. Changelog
- 2026-10-20 v1: approved at Checkpoint 1 (hook H1, Match-reference look, hard cuts + dip to white).
- 2026-10-20/21 round 1b, from the director's notes on the local previz ("jumps are odd, the videos are unstable, the transitions are not cinematic, cinematic colours grading is not there at all"):
  - eye-match dissolves + bloom flash replace hard cuts and the dip to white;
  - eye-lock stabilisation;
  - **G2 Gold & Shadow** look replaces Match reference;
  - V1 baked outside Premiere with the per-clip primary;
  - SFX −14 dB;
  - C074 / C025 source windows moved for the lock.
- 2026-10-21 review gate v1 (FAIL, 5 major) fixes:
  - eye-lock re-pinned on the measured pupils (C163 was 190 px low);
  - C120 replaces C025, C200 replaces C083;
  - C076 plays its sharp stretch, then holds;
  - per-shot colour trims (C076 de-yellowed, C139/C168 saturation −35 %, C120 warmed, exposure trims);
  - booms placed 1–2 frames earlier, −16 dB;
  - mix guide peak-limited (−1.9 dBTP).
- 2026-10-21 review gate v1b (FAIL, 3 major) fixes, editor-verified:
  - freeze lands on the sweep's last frame (no hop);
  - C084 replaces the soft C120;
  - C076 / C112 red push, C145 sat −15 %;
  - sweep +0.15 stop easing out;
  - hook band narrowed to the instrument neck + bow on the eye-line (`tools/stock_band.py` v2 → `renders/stock/stock_band_v2.mov`).
- 2026-10-21/22 **round 2 (v2, storyboard B)**, from the director's Checkpoint 2 notes on v1c ("only Ma's face is not a story", "check the new folder", "string player not strong or recognisable", "less single human, stable Ma, use bonedi bari", "find the accurate string player", "no face, instrument + arms + legs"):
  - bonedi-bari act C037 → C059 → C050 → C056;
  - AI-generated esraj opening (labelled, $0.52 total, director-approved) replaces the Pexels band;
  - C074 / C076 / C084 dropped;
  - V2 track removed (the ghost is baked into V1).
- 2026-10-22 v2 previz checks (editor):
  - C059 lock re-framed (cw 0.75 → 0.70, v 0.88): the old crop clamped and passed the camera's tilt bob;
  - C059 −1.0 → −0.5 stop;
  - C163 esraj ghost 55 % → 45 %, clearing by 3.3 s.
- 2026-10-22 review gate round 2 (two loops, both FAIL; v2c editor-verified):
  - C208 re-pinned (tracker window bug);
  - C059 → medium shrine crop out of the IG zone;
  - C163 sharper and less hazy;
  - C037 junction box out;
  - title blur-out;
  - 9.08 hard cut;
  - softness trims.
- 2026-10-23 **round 3 (v3)**, from the director's Checkpoint 2 answers:
  - run cuts +7 frames onto the percussion strokes;
  - title moved to 2.08–4.16 s (over her eye only);
  - AI esraj kept as is;
  - IG audio = same song and start as the reference.
- 2026-10-23 review gate v3, loop 1 (FAIL: the title rose over the instrument) fixes:
  - esraj→eye cut 2.40 → 2.16 s (12 frames);
  - title 2.32–4.00 s;
  - photo dissolve 8 frames;
  - C163 +0.15 stop;
  - C056 green pulled toward neutral (lime glass panel).
- 2026-10-23 **round 4 (v4)**: new one-house storyboard (house B), reference blinks on accents + hard cuts on strokes, G2b2 grade, title over her eye in the silence. See §0.
- 2026-10-27 **round 5 (v6)**:
  - re-brief to the reference's structure: the singer double-exposed over the red clay Durga, a blink on 7.88, her eyes held, a blink on 16.00, then closer;
  - Real-ESRGAN AI upscaling for tight eyes;
  - title moved over her eyes in shot B;
  - grain 6 %; tv-range previews.
- 2026-10-28 **v9b** (review gate v9, FAIL 2 major + 3 minor): A's ghost moved to the left with her eyes clear and its haze removed (blacks match B/C); B's AI share 55 % (nath 20 %); C's scaffold band darkened; end card up onto the chin; stale idol line fixed.
- 2026-10-28 **v9c** (review gate v9b PASS, 4 minors): C regional deflicker + corner darkening; a soft dark plate under the title; the nath accepted as the real jewellery.
- 2026-10-29 **v10** (director on iPhone: "very poor quality"): real-frame stacks instead of AI, A/B framed wider (≤ 1.42×), C texture kept, clarity 0.08; HQ encode from a ProRes master.
