# Brief — written by the editor, approved by the director

> Claude writes this file after the interview and footage analysis. The director only answers questions, shares references, and approves. Don't fill it in by hand; ask Claude to change anything.

**Status:** v9 (2026-10-23, round 9, approved): re-cut with **one different man per line, nobody repeated** (12 shots, 13 men), cuts on the Hindi words, synthesised slow motion at the emotional lines, mains flicker removed; two versions: colour and B&W (the B&W opens in colour and drains to the Durga's gold). Earlier: v3 warm cinematic look (round 3), v4 stabilisation, v5 skin-anchored colour.

## 1. The idea
- **Reel type:** `hybrid`. Soundtrack = the reference reel's audio (Hindi VO over a soft bed), whole, 0–35.83 s. No speech in our footage.
- **Concept:** *Pujo ki asolei sobar?* (Is Pujo really for everyone?). It opens on a priest's aarti before the Devi, then follows the men who work through Pujo while the VO says "there are two men inside every man": the 18-year-old who wanted to conquer the world, and the 28-year-old who just wants to keep the house running.
- **One man per line (v9):** the VO's "first" and "second" man are archetypes, so every line gets its own face; nobody appears twice (director, round 9: "we are choosing the same set of people a few many times"). Two men share one shot on purpose: shot 5, the dreamer and the man doing the maths side by side on one tarp. Rhyme: a young balloon seller says "one day I'll change everything"; the old balloon seller ends the reel "in front of his own old dreams".
- **Arc:** worship (L1) → the two men (L2–L7) → silence (L8) → "not lost to the world" (L9, dissolve) → the old dream (L10).
- **Length:** 35.83 s (1075 frames @ 30).

## 2. Hook (0–4.13 s)
- C152 src 8.80–12.93, 1.4× punch-in on the priest's aarti before the yellow Durga (baked), slow push. Title **PUJO KI ASOLEI SOBAR?** (romanised, DIN Condensed Bold, cream, soft halo) 0.27–3.17 s over the pandal ceiling, clear of the Devi's face.

## 3. References → concrete parameters
| Reference | What we take | Measured |
|---|---|---|
| `references/ref_audio_vo.mp4` (35.8 s VO reel, flower market) | Its audio whole; one shot per VO line; observational portraits of working men; shallow focus | 11 cuts, avg 2.98 s. Ours: 13 shots, avg 2.76 s |
| Director (v1g) | "very sepia, filmy"; real lens depth (bokeh), since iPhone footage has none; all shots graded accurately together despite mixed lighting | — |

## 4. Treatment
### Cutting (v9)
- **Every cut lands on the first word of a sentence or clause**, measured to the frame (`analysis/word_onsets.json` + envelope): f124, 251 ('Aur ek jo'), 328 ('bas ghar…'), 406, 539, 638, 693, 764, 797, 886, 969. Inside shot 5 the camera's move lands on the second man at f464 ('Dusra…' 463).
- Hard cuts, plus one Cross Dissolve of 10 frames centred on f886 (old man → rickshaw puller, L9). Shot 2 hides one cut under a passer-by crossing the lens (f203), so it plays as one shot.

### Colour (v11: natural, but warmer and matched; built on the v3 warm cinematic look)
- **Reference:** `references/ref_grade_bangkok.webm` (the director's "master class" example). Measured on 25 colour frames: luma 0.28, p50 0.24, p98 0.75, saturation 0.35, mids R/G 1.00 B/G 0.86.
- **Per shot:** stabilise → denoise → white balance from near-neutral pixels + tonal match (p02 / p50 / p98) → clarity.
- **One look** (`tools/cine_look.py`, params `analysis/cine_look_params.json`): soft filmic tone curve fitted to the reference, 3-way balance warmed at the director's request ("warmer"), saturation 0.72.
- **Per-shot warm cast match** (midtone R/G 1.06, B/G 0.78), so blue street light, green tube light and orange sodium all land on the same warm skin; a per-shot saturation cap of 0.34 (the drummer's yellow shirt was 0.47).
- Halation 0.10, vignette 0.18, grain 0.010; black floor 0.025; luma matched to 0.28.
- **v11 (round 11: "over-processed, not natural" → "natural, but warmer and matched"):** every correction at partial strength (`shot_render_v5.py --natural-matched`):
  - white balance 60 % of the way to neutral;
  - auto-levels 65 %;
  - cast match 0.6;
  - the look above mixed at 75 %;
  - skin anchor ^0.75;
  - light denoise, no clarity / local contrast;
  - no face or shadow lifts.

  Each scene keeps some of its own light.
- No synthetic bokeh (rejected in round 2). Sepia rejected in round 3 ("too strong, doesn't come out well").
- Renderer: `tools/shot_render_v5.py` (v4 similarity stabiliser, 2 passes; the look above; skin anchor) + `tools/skin_post.py` (skin hue 28°, sat 0.45 on every face) + **`tools/deflicker.py`** (round 8: removes the 10 Hz mains flicker from the 1/60 s shutter under 50 Hz lamps; per-tile, brightness only). 25 fps sources conformed.
- **B&W version:** `tools/bw_render.py` (red-leaning mix 0.40 / 0.50 / 0.10, gentle S-curve, luma matched); shot 1 keeps the Durga's gold (person-matted gold key) and opens in full colour, draining to B&W + gold over 0–2.4 s (`tools/bw_fade.py`). Title, subtitles and end card neutral white.

### Motion
- Slow push 100 → 105 % on 1, 4, 10, 11, 12 (Premiere scale keyframes). Handheld shots keep their own movement.
- **Slow motion (v9, director: "slow down at places to add more drama"):** synthesised by optical flow (ffmpeg `minterpolate`, after grade + deflicker); no clip in the 327-clip pool is above 30 fps. 5 (pan easing 0.85 → 0.61×), 10 (0.6×), 11 (0.55×), 12 (0.7×). The dhaki (2) and the young balloon seller (6) play at real speed: synthesised slow-mo on those takes smeared (round 11, "slow where needed"). Natural sound is silent under slow motion.

### Type & graphics
- Title as §2. English subtitles: 18 cards, Clean (soft white, dark halo), lower third above y = 1600 (`analysis/subtitles_v1.json`, approved). Cards 1–2 sit to the right of the priest (x 637–913, y 1230–1361). End card `@SATYAJITMALL` in the title style, lower left over the seller's dark coat, 34.40–35.82.

### Sound
- A3: reference VO + bed, from 0:00, peak ≈ −0.8 dB: a **cutting guide**; IG audio is added at upload. A1: nat sound muted except the aarti (1) and the dhaki drums (2, normal-speed part) at −26 dB. Exports: `_mix` (review) and `_IG` (VO muted).

## 5. Clips (v12, 13 shots, 14 men, frame-exact @ 30; `analysis/edl_v9.json`)
| # | Clip | Src | Frames | VO line | Why this shot (narration → picture) |
|---|---|---|---|---|---|
| 1 | C152 | 8.80–12.93 | 0–124 | L1 "every man has two men inside him" | the priest's aarti before the Devi + title (approved hook) |
| 2a | C027 | 1.60–2.97, 1× | 124–165 | L2 "one who at 18," | a young dhaki boy drumming |
| 2b | C028 | 31.30–34.17, 1× | 165–251 | L2 "wanted to conquer the world" | on 'duniya' a cut to a young jewellery seller at his stall, face lit (round 12: replaces the 2nd dhaki angle) |
| 3 | C190 | 4.33–6.90 | 251–328 | L3 "and one who, at 28," | a young priest at work turns to look at us |
| 4 | C032 | 4.53–7.13 | 328–406 | L3 "just wants to keep the house running" | the tea seller pouring |
| 5 | C222 | 0.30–3.39 easing 0.85 → 0.61× | 406–539 | L4 "the first one dreamed" / L5 "the second does the maths" | two men on one tarp: a young man, arms crossed, staring into space; the camera moves to the older man working figures on his phone |
| 6 | C212 | 0.67–3.97, 1× | 539–638 | L6 "the first said, one day I'll change everything" | a young balloon seller, balloon in hand, looking ahead |
| 7 | C201 | 0.30–2.13 | 638–693 | L7 "the second thinks every month" | a father at the toy stall, his child reaching |
| 8 | C213 | 2.00–4.37 | 693–764 | L7 "just let this month work out" | an old shopkeeper waiting for customers |
| 9 | C215 | 0.60–1.70 | 764–797 | L8 "maybe that's why" | a man alone on a roadside wall, head bowed |
| 10 | C052 (25 fps) | 1.00–3.12 at 0.6× | 797–886 | L8 "when a man suddenly goes quiet" | an old man standing silent in a doorway |
| 11 | C216 | 0.11–1.63 at 0.55× | 886–969 | L9 "it doesn't mean he's lost to the world" | a rickshaw puller in his seat looks straight at us while traffic streams past; dissolve in |
| 12 | C193 | 0.40–2.87 at 0.7× | 969–1075 | L10 "sometimes he's just standing in front of his own old dreams" | the balloon seller gazing up at his balloons + @SATYAJITMALL |

All 327 original clips in the director's Puja/Pujo folders were contact-sheeted for round 9 (`analysis/pool_r9/`).

## 6. Must-haves / must-NOT-haves
- **Must:** pictures change on the words; the picture matches the line literally. A different man on every line. The aarti opening. One grade identical across shots, skin on one tone. No flicker. Slow motion only at the emotional lines; dignity (no pity cues). Two versions (colour, B&W + gold), each with `_mix` and `_IG` exports.
- **Must not:** the same person twice; Durga shots without a narrative reason; cuts in VO pauses; creative looks that differ shot to shot; text outside the safe zone; shipping the reference audio as our own.

## 7. Open questions
- Who made the reference audio (for the caption credit)?

## Changelog
- v1 (2026-10-19): first draft from Round 1 + Round 2 + reference VO.
- v1b (2026-10-19): director note "goddess shots in between" → 7 goddess inserts in the VO pauses; 8a C143 dropped; +3 clips copied (C163, C171, C199). 20 shots.
- v1c (2026-10-19): director notes "too many" / "start with a montage of the Devi with a priest performing aarti" / "many other shots of men you skipped":
  - opens on a 5-shot Devi/aarti montage (C152 wide + close, C161, C208, C190 young priest), replacing the crowd hook;
  - goddess inserts cut from 7 to 2 (turn C171, before the seller C145);
  - more men: + C216 rickshaw puller, C212 young balloon seller, C201 father at the toy stall, C195 cotton-candy seller; − C186 / C187 crowds, C211, C223, C189;
  - +2 clips copied (C161, C190). 19 shots, 35.82 s.
- v1d (2026-10-19): director notes "colour grading should be the same across the videos" and "a natural depth in shots should be added" → one look (Kodak 2393 ≈ 40 %, a single V3 layer) with every clip primary-matched to one warm-neutral target (the edge/gold split is dropped); natural depth = tonal S-curve + soft vignette on all shots, plus a matte-based mild background defocus baked on 10 people shots. Preview stills in `analysis/look_test/`.
- v1e (2026-10-19, after the rough cut): "too many shots of the Durga unnecessarily, go through the narration and fit accordingly" → every shot re-matched to its line; Durga 7 → 3 (C161, C208, C171 out); L2 = young balloon seller C212, L6 = young priest C190, L8a = phuchka seller C223 (depth-baked; C195 out); turn = dissolve lone man → Ram-naam men; opening A1 to 3.20 s so the title never sits on the Devi's face. 16 shots, 35.83 s.
- v1f (2026-10-20): "cut and depiction not accurate" / "cuts on the words" / "go through all Pujo folders" → cuts on measured onsets; Oct 19 footage; one man per voice. 13 shots.
- v1g (2026-10-20): "iPhone has no natural depth of field, add bokeh in post" / "very sepia filmy vibe" / "grade all accurately together" → per-shot neutral match + sepia film look + depth-model lens bokeh, all baked per shot (director chose baking over a LUT on an adjustment layer).
- v1i (2026-10-20, review gate loops 1–2): cut f247 → f251; one drummer for every 'first man' line (L4 C004 12.0 face 1.6×, L6 C005 0.5 1.3×); shared black floor 0.03 + per-shot luma match 0.27; hero-only focus/protect; the Devi sharp in the hook; cards 1–2 beside the priest; end card in the title style.
- v2 (2026-10-20, round 2): "bokeh not ok, render without" / "correction, stability and clarity need to improve" → no bokeh; own stabiliser (phase correlation, 4K margin); hqdn3d + supersample + detail / clarity; white balance from near-neutral pixels + per-shot tonal match; shot 9 C222 → C213 (C222's swing can't be stabilised). Director: "for now finalise it".
- v3 (2026-10-21, round 3): warm cinematic look matched to the Bangkok reference (sepia dropped); per-shot cast match + saturation cap; L3a → C043, L8b → C052 from the new Oct 20 footage, chosen by narration.
- v4 (2026-10-21, round 4): "stabilisation issue" → similarity stabiliser (translation + roll + zoom), 2 passes.
- v5 (2026-10-22, round 5): "colour corrections still not on point" → skin-anchored correction (hue 28°, sat 0.45 on every face).
- v5_bw (2026-10-22, round 6): B&W alternate, only the first Durga in gold. Round 7: opens in colour and drains to gold (ffmpeg colour skill).
- v6 (2026-10-23, round 8): mains flicker (1/60 s under 50 Hz) removed per tile, both versions.
- v9 (2026-10-23, round 9): "same set of people a few many times" / "slow down at places for drama" / "match the footage with the words" / "go through all videos" → 327 clips surveyed; one man per line (13 men, no repeats); cuts on the Hindi words; synthesised slow-mo on 6 shots. Round 9b: shot 3 (dhaki troupe) rejected → the dhaki boy carries all of L2, slow-mo from 'duniya'.
- v10 (2026-10-23, round 10): "a few sections a little dark" / "0:05–0:07 very dark, not clear" / "transition weird from normal motion to slow" → shot 2's slow part re-picked (C027 face-on, src 20.0) with eased speed; toe lift + luma 0.275 on shots 3–6, 9.
- v11 (2026-10-23, round 11): "over-processed, not natural" / "dhaki not great in slow-mo" → director chose "natural, but warmer and matched" + "slow where needed": all shots re-rendered at partial correction strengths, no clarity, no face lifts; dhaki gentle 0.8× only from 'duniya'.
- v12 (2026-10-24, round 12): "the two successive shots of the drummer: replace the second with the boy selling jewellery" → 2b = C028 jewellery seller (src 31.3); "no black and white needed" → colour only.
