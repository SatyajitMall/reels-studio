# Brief — written by the editor, approved by the director

> Claude writes this file after the interview and footage analysis. The director only answers questions, shares references, and approves. Don't fill it in by hand; ask Claude to change anything.

**Status:** approved 2026-10-18 (Checkpoint 1: hook A, 14-shot EDL, Match Reference look, title `PUJA NIGHTS · 2026`, no location tags). **Round 5 (2026-10-19): treatment rewritten in §0 and approved by the director (dramatic cut, DURGA intro, cinematic warm grade, Durga ending).**

## 0a. Round 6 changes (current, v6d; on top of §0)
Director, round 6: camera push-ins / pull-outs jumpy, no cinematic stability or depth; review the discarded footage; the 0:19–0:21 effect is botched; better cinematic transitions on the beat. Decisions: stabilise everything; bring in the discarded clips; transitions placed by the song's structure; one cinematic tone on every shot.
- **Stability:** Warp Stabilizer (Smooth Motion) on every handheld moving shot, analysed; per-shot velocity jitter now < 0.6 px/frame (C091 1.2, C087 1.1; v5c worst was 3.7). Where Warp hurt (C096 judder, C091 crop error) or the source had a jolt (C087 first 1.2 s), the shot uses its steadiest source stretch without Warp. v6d: C087 is out (its forward move stuttered: the source itself steps unevenly); **C129** (scaffold, looking up) now holds 37.92–40.44 straight into the gold-leak reveal. C132 is no longer nested: 150 % speed on the 4K clip itself with **Optical Flow** time interpolation, 128 % top-anchored (no upscale; 1.7× sharper than v6c, even cadence).
- **New footage:** C116 lotus lamps (9.44, bamboo-lotus pandal, rotated, 125 % top-anchored), C105 woodcut Durga panel (22.76; v6c, replaced the smeared C109), C124 lotus interior (35.96, rotated), C083 pastel Durga (48.04–50.52, slow push) → the ending runs Durga face (C139) → pastel Durga (C083) → shrine push-in (C112).
- **Removed:** "MAA" text and the C126 zoom punch (0:19–0:21).
- **Transitions on the song's structure** (built from the graded render, V6): zoom-through at 3.80 (intro → reel) and 20.24 (the lift); whip pans at 22.76 and 24.00 (pans meeting on beats) and a downward whip at 27.80 (dome ceiling → gold Durga); gold light leak at 40.44 (the reveal; replaces the white flashes); soft dip through warm dark at 50.28–50.76 into the ending. Hard cuts elsewhere. Whooshes on the whips (A2).
- **Tone:** every shot matched to the montage (luma 0.22–0.26 on 25 of 29; dark scaffold C125/C126 a little lower by design); forge and pastel shots warmed (+10 temp, +8 sat); C089 / C128 highlights −20.
  v6d: C086 (red forge spikes) warmed to its neighbours (temp 50, tint +5, sat 140, highlights −15: saturation 0.47 → 0.65, warmth 0.19 → 0.34); C129 / C132 +0.2 stop; C133 −0.25 stop; C135 saturation 64; C085 115 % top-anchored (shop awning into the IG band) +0.25 stop; C116 132 %, C091 130 % top-anchored (faces and phones into the band).

## 0. Round 5 treatment (current, v5; supersedes §2 hook, §4 pace / effects / type / sound and §5 below)
Director, round 5: "slide show instead of cinematic cuts… music is dramatic but the shots and the cuts do not make it dramatic… natural depth missing… intro: the word DURGA, the recording fills the letters, like the Marvel intro". Decisions: dramatic cut plan approved; intro **inside the letters**; depth = **cinematic warm grade**; end on Durga (C112).
- **Music:** unchanged, D 1:45.60–2:41.20, 55.60 s, IG start 1:45.6. Hits: 2.54 → 3.14 → **3.79**; 8.85 / 9.45 / 10.11; 15.77, 17.70, 18.95; lift **20.23**; 25.27, 27.80; **40.43**; loudest bar 42.96.
- **Hook / intro (0–3.80):** `DURGA` (Impact, stretched 980 × 640 px, cream edge, dark red ground); footage flips inside the letters on every beat, then every half beat after 2.54; the camera pulls back out of the letters 0–2.54; `PUJA NIGHTS · 2026` under the word from 2.54; riser into 3.79, white flash + boom, smash cut into the reel. Built by `tools/durga_intro.py` from the graded render, on V5.
- **Pace:** 28 shots + intro (v5b), avg 1.8 s. 0.6 s flashes on hits; ≈1.25 s two-beat cuts through the build and the full section; holds of 2.5–5 s only on hero moments (C132 walk-in, C093, C095 + MAA, C101, C099, C135, C089 reveal, C139, C112 ending). Every cut within 20 ms of a beat.
- **Motion / energy:** cut on movement; C132 150 %, C087 200 % into the reveal; snap zooms on C135's beats and C106; zoom punch out of C126 into the lift; pushes on C103 / C101 / C139 / C088 / C112; C089 holds its last frame to the cut.
- **Transitions:** hard cuts; white flash 3.80 (into the reel) and 40.44 (the reveal); fade to black 54.40–55.60.
- **Look (cinematic warm):** V3 look Lumetri (Kodak 2393 preset, intensity 50, temp +14, tint −20, contrast +22, highlights −12, shadows −12, exposure +0.18, vignette −1.4) + ASC CDL on the adjustment layer R 1.02 / G 1.00 / B 0.84; per-clip primaries as before (red pandals sat 72, gold CDL on the dome shots). Grain 12 % Overlay.
- **Sound:** music A3 −2.5 dB (fades: 6 frames in, Exponential Fade 54.56–55.60); ambience A1 −24 dB; SFX A2/A4: riser 2.80 → hit 3.81, boom 3.80, snap swishes 15.08 / 33.40 / 34.08 / 34.68, whoosh into 20.24, riser → 40.45, boom 40.44 (−15…−18 dB). `_IG` export keeps SFX + ambience.
- **Phones / crowd:** C103 / C128 / C134 / C091 / C094 reframed top-anchored so phones, faces and labels fall out or into the IG bottom band; C088 tracked phone mask (`renders/overlays/c088_phone_mask_v5.mov`).
- **Type:** DURGA intro + `@satyajitmall` end card (51.88 → end, above the arch). "MAA" behind the folk Durga.

| # | clip | reel | what / move |
|---|---|---|---|
| 0 | DURGA intro | 0.00–3.80 | footage inside the letters (C101, C093, C096, C135, C106, C091, C089, C139), pull-back, flips accelerate, word 840 × 600 px (clear of IG's right column), `PUJA NIGHTS · 2026` (86 px) under at 2.54; white flash + boom on 3.80 |
| 1 | C132 | 3.80–6.32 | red arches tilt → crowd walking in, 150 % |
| 2 | C094 | 6.32–7.60 | folk pandal interior, crowd moving; 116 % anchored top-left |
| 3 | C103 | 7.60–8.84 | woodcut facade, push 118→122 % top-anchored (crowd phones below the IG band) |
| 4 | C085 | 8.84–9.44 | forge machinery flash (hit), rotated 180°, source 1.7 |
| 5 | C134 | 9.44–10.12 | giant red feet flash (hit), 150 % top-anchored (no faces) |
| 6 | C093 | 10.12–12.64 | facade of lights, tilt (downbeat) |
| 7 | C091 | 12.64–13.92 | folk dolls with lamps, source 2.0, 114 % top-anchored |
| 8 | C092 | 13.92–15.16 | folk, 114 % shifted right (no lens-looker at the left edge) |
| 9 | C106 | 15.16–15.76 | woodcut print, snap push (hit) |
| 10 | C090 | 15.76–17.04 | folk interior, reframed 75 % |
| 11 | C086 | 17.04–17.72 | red forge spikes (hit), rotated 180° |
| 12 | C125 | 17.72–18.96 | iron scaffold, looking up (accent) |
| 13 | C126 | 18.96–20.24 | dark scaffold, zoom punch into the lift |
| 14 | C095 | 20.24–22.76 | folk Durga hero hold, **MAA** behind her head |
| 15 | C110 | 22.76–24.00 | woodcut pan |
| 16 | C107 | 24.00–25.28 | woodcut pan |
| 17 | C101 | 25.28–27.80 | chandelier dome, slow push, exposure settle (source from 0.16) |
| 18 | C096 | 27.80–30.32 | gold Durga with lion, 62 % (v5b: C098 / C099 dropped, whip + soft) |
| 19 | C135 | 30.32–35.36 | giant red feet, top-anchored 128 %, five snap zooms 31.58 / 32.86 / 33.46 / 34.11 / 34.74 (128 → 168 %), swishes |
| 20 | C133 | 35.36–35.96 | red crowd backs (hit), source 5.44 |
| 21 | C086 | 35.96–36.64 | red forge spikes, second moment (source 1.0, rotated) |
| 22 | C128 | 36.64–37.92 | Durga behind the scaffold mesh, 140 % top-anchored (phones below the IG band) |
| 23 | C129 | 37.92–39.16 | scaffold with plants, looking up |
| 24 | C087 | 39.16–40.44 | forge approach, 200 % into the reveal |
| 25 | C089 | 40.44–45.48 | forge Durga zoom through the loudest bar; holds 44.84 → cut; white flash in |
| 26 | C139 | 45.48–48.04 | Durga face, push |
| 27 | C088 | 48.04–50.52 | crowd + forge Durga, tracked phone mask |
| 28 | C112 | 50.52–55.60 | camera pushes into Durga's face (highlights −35, −0.25 stop, sat 85 against red clipping); end card 51.88; fade to black 54.40–55.60 |

## 1. The idea
- **Reel type:** `music-montage` (no speech; CLAUDE.md §4a + §4c).
- **One-line concept:** *One night, pandal to pandal.* A calm walkthrough through the Puja night: arrive outside, step in, glimpse the goddess, wander the crowds and the craft, then she's revealed on the song's peak, and the night settles as we look at her from afar.
- **Story arc (walkthrough, from the reference):** ARRIVE → ENTER → GLIMPSE → WANDER (crowds, folk art, woodcut panels, chandeliers) → REVEAL (Durga on the peak) → SETTLE (callback to the glimpsed goddess, then a distant last look).
- **Goal:** calm / nostalgia.
- **Audience:** filmmaker / creator crowd (from my-reel), so the craft has to be visible but quiet.
- **Runtime:** **55.60 s** (round 4, music D; was 59.80 s on A). Director chose "what the song needs".

## 2. Hook (0–3 s)
- **Shot:** C103 (src 20.28 s): the woodcut-print pandal at night from outside: glowing round panel, dancers on the steps, crowd in silhouette.
- **Visual move:** fade up from black (12 fr) into a slow push 100 → 108 % (on the measured static hold, source 20.28–25.64), with real motion in frame (dancers, crowd). First cut at **5.36 s** on a beat (v1b; was 4.76 in the approved plan, see changelog).
- **On-screen text:** title fades in at 0.8 s, out by 4.2 s (wording: open question 1).
- **Deliberately a calm open, not a 3-second hard hook** (goal is calm / nostalgia; the song's first lift is at 14.35 s). Alternatives in `project.md` Round 1.

## 3. References → concrete parameters
| Reference | What we take from it | Measured |
|---|---|---|
| `Video-92015.mp4` (45.2 s, 720×1280, 30 fps) "Exclusive First Look of Ek Pukur Bhalobasa, Telipukur Yuba Sangha" | Walkthrough structure (entrance → passage → murals → people → idol reveal → murals), warm dark grade with deep blacks, handheld moves kept, text pinned at the top | 7 cuts, avg shot 5.64 s, median 3.55 s, shortest 1.3 s, first cut 2.67 s. Exposure 0.264, contrast 0.008–0.777, warm +0.10, 18 % crushed shadows. **Audio = Shondhatara 2:06.4–2:51.5, uncut, no voiceover** |

Ours: 14 shots, avg 4.27 s, median 4.3 s, shortest 2.53 s, first cut 4.76 s.

## 4. Treatment

### Music (A3)
- **Track:** *Shondhatara* (Coke Studio Bangla S2, Arnob × Sunidhi Nayak × Adit Rahman). Director's own copy, linked as a **cutting guide** (`music/shondhatara_GUIDE.mp3`).
- **Section (round 4, director's choice D):** **1:45.60 → 2:41.20** (105.60–161.20 s), one continuous stretch, no music edits (Instagram's picker takes one unbroken stretch). Round 1–3 used A 3:31.88–4:31.70.
- **Grid (D):** 95.7 BPM, 22 bars. Accents at 0.00 (+2.9), **3.79 (+3.7, strongest)**, 8.85, 10.11, 17.70, 18.95; **lift at 20.23** (−3.3 → −2.1 dB); full to the end; loudest bar 42.96 (−1.5 dB); ends on the 55.59 bar.
- **Energy arc (reel time, music D):**
  - **ARRIVE / ENTER, build** (0–11.36, −3.9…−3.1 dB with strong accents): C103 + title opens on the 0.00 accent, cut on the strongest hit 3.79; C132 walk-in (3.80–8.84), C130 inside the red pandal on the 8.85 accent (v4c), C081 sharp glimpse on the 10.11 downbeat.
  - **BUILD** (11.36–20.23): folk pandal C090, C092 on the build's accents; C095's tilt to the folk Durga.
  - **LIFT** at 20.23 (−2.1 dB, full from here): "MAA" fades in behind her head on the lift; then woodcut C110, C107; chandelier C100, C101, C096.
  - **REVEAL** (37.28–48.00): C087 Durga through the wrenches → C089 optical zoom riding through the loudest bar (42.96) → C139 her face.
  - **SETTLE** (48.00–55.60): C083 callback, C088 last look with the end card; fade to black with the music over the last 1.2 s (D has no quiet outro, so the fade carries the ending).
- **Delivery:** two exports per version: `_mix` (guide music) and `_IG` (no music, ambience only) for posting with IG's library Shondhatara started at **1:45.6** (round 4).

### Pace
- Calm 3–5 s (director's pick; reference median 3.55 s). Hard cuts on bars and pickup accents; never one shot per bar for the whole reel (see arc).

### Motion style
- **Handheld moves kept** (they're the "walking through" feel): C132 tilt-up walk-in, C090, C095 tilt-down reveal, C110 pan, C107 pan, C100 tilt, C083 pan.
- **Digital push/pull only on measured holds** (`motion.json`): C103 push 100→108, C081 push 100→106, C139 push 100→106, C088 pull 106→100. C093 and C099 are near-static (mean speed 1.9 / 2.9) but not flagged as holds: push 100→104 only if they read static by eye.
- **C089 keeps its own optical zoom** into Durga (no digital move on top).
- **No slow-mo** as an effect (25 fps footage). Only C089 runs at 93.7 % with optical flow, imperceptibly, to reach the bar.
- **Stabilise** only where `shake_report.py` measures real jitter with little pan: **Warp Stabilizer (smoothness 50) on C090 and C107** (C105 and C093, Warped in v1, are out of the cut), all with hard cuts on both sides. C099 (5.4 px) left as is: it is frame-rate-interpreted (needs nesting first); push 100→104 kept subtle. C093 gets no push (Warp instead).
- **Sequence:** 1080×1920 @ **25 fps** (all 62 clips are 25 fps; 3 read 25.002–25.013, same rate). Sources are 2160×3840, scaled to 50 %, leaving 2× headroom for pushes.
- **Orientation:** C139 is recorded upside down → rotate 180°. (~18 other clips are upside down too; none are in this cut.)

### Colour
- **A1 primary (per clip, one Lumetri each):** the shoot is warm (+0.14 to +0.60) and very saturated, with exposure 0.17–0.34.
  - v2: red pandal shots C132 / C130 / C095 / C139 at Basic Saturation **72** (director: "desaturate a little"); chandelier C099 / C100 pushed to gold with ASC CDL (midtone hue 20–22° → 30–32°).
  - v1b: the red trio C132 / C095 / C139 at Basic Saturation 80 (C139 temp +2, C095 +3) after review v1 found them hot vs the reference; C132 +0.65 stop.
  - Pull the hottest pandals toward the reference's warmth (target +0.20…+0.35, gold kept): C090, C093, C095, C099, C100, C132, C139: temp −15…−20, Basic Saturation 85–90. C095, C099, C103, C132 and C139 also need tint toward green (−5) for their magenta cast.
  - Lift the dark ones: C081 (0.167) +0.4 stops, shadows +10; C132 (0.204) +0.3 stops; C088 (0.216) / C089 (0.228, 24 % crushed) +0.2 stops, shadows +10…+15.
  - C100 reads flat: contrast +20. C110 has a green tint: tint +5. (C105, −0.15 stop in v1, is out of the cut.)
- **A2 shot match:** adjacent shots within ±0.04 exposure and ±0.03 warmth, especially the folk trio (C090/C093/C095), the woodcut pair (C110/C107) and the peak pair (C089 → C139, which changes pandal and colour: gold-red).
- **A3 creative look: Match Reference** on the V3 adjustment layer: built-in `Fuji F125 Kodak 2393 (by Adobe)` at 40 %, contrast +15, shadows −10, exposure +0.15, saturation 95, temp +4, tint −10 (against the preset's red push), vignette −0.8. Measured on 14 stills: luma median 0.27 (reference 0.264), crushed 0.6–21 %. Check gold hue 30–45° with `colour_report.py --gold`; red pandals (C132, C139) are watched for the warm look pushing red.
- **A4 texture:** fine 16 mm grain, Overlay, **12 %**, faded with the picture at both fades. No light leaks or burns (calm).

### Effects & transitions
- **Hard cuts** everywhere except:
  - 0.00: fade from black (Dip to Black, 12 fr);
  - 24.45: Cross Dissolve 12 fr (folk pandal → woodcut pandal);
  - 49.72: Cross Dissolve 12 fr (gold Durga → pastel Durga, into the settle);
  - 54.15: Cross Dissolve 12 fr (into the last shot);
  - 58.62–59.82: Dip to Black 1.2 s.
- That's 3 dissolves + 2 fades in 60 s. Every dissolve has source handles (checked against clip lengths).
- **Signature moments:** the lift landing on the 13.73 pickup accent; the reveal C089 zoom on the peak at 39.62; the C081 → C083 callback (glimpsed through slats at 9.55, seen whole at 49.72).
- **After Effects:** none planned (the director called decorative AE looks "cringe" in my-reel). Optional: denoise on the darkest shots (C081, C088, C089) if noise shows in v1.

### Type & graphics
- **Title + end card only** (music-montage default). DIN Condensed Bold, cream `#F5E6C8`, dark soft halo instead of the gold glow (calm). **Title low, between the medallion and the crowd** (104 px, box y 1423–1499, centred, even spacing around the dot), because at the top it collided with the pandal's Bengali name banner and at y 1379–1462 it cut across the performer in the bottom medallion (review v1).
- **Title:** `PUJA NIGHTS · 2026`, 112 px, shot 1, 0.8–4.2 s, 12-frame dissolve in and out.
- **No location tags** (director, Checkpoint 1).
- **End card:** `@satyajitmall`, 84 px at y ≈ 400 (in the dark trees above Durga, checked on an exported still), 56.08 s → end, dissolving in over 12 frames and out with the picture's fade (58.6–59.8).

### Sound
- **A3 music:** guide section at −2.5 dB clip level (the master peaks at 0 dBFS) → mix peaks −1.4 dB; no ducking; 6-frame fade-in under the fade from black; fade-out = **Exponential Fade 54.56–55.60** with the picture (v4c; was a 1.2 s Constant Power that held level through the last hit and dropped in the final 0.3 s).
- **A1 natural sound:** crowd murmur from the clips at about −24 dB for presence (also stays in the `_IG` export under the IG song).
- **A2 SFX:** none planned (calm). Option: one soft low swell into the reveal at 39.62.

## 5. Clips (the cut, in order — as built v4 on music D, 17 shots, 55.60 s)
| # | Clip | In → out (reel) | Role | Pandal | Notes |
|---|---|---|---|---|---|
| 1 | C103 | 0.00–3.80 | hook, ARRIVE | woodcut print | push 100→108; animated title over it |
| 2 | C132 | 3.80–8.84 | ENTER | red arches | +0.85 stop, sat 72; source 0.12–5.16 (v4c: runs to the clip's last frame so C130 can start on the 8.85 accent) |
| 3 | C130 | 8.84–10.12 | inside | red pandal | rotated 180°; sat 72; source 3.00–4.28 (v4c: ends before the plaid-shirt man lifts his phone at source 4.30; v4b's 0.4 s slip wasn't enough) |
| 4 | C081 | 10.12–11.36 | GLIMPSE | pastel Durga | sharp tail only |
| 5 | C090 | 11.36–13.88 | lift: canopy + murals | Rajasthani folk | Warp; reframed **75 % / y 0.75** (v3c) |
| 6 | C092 | 13.88–17.04 | doll procession | Rajasthani folk | |
| 7 | C095 | 17.04–22.12 | folk Durga with lamps | Rajasthani folk | sat 72; **"MAA" behind her head 19.56–21.84** (tracked bake on V2; fades in 19.64–20.14, onto the song's lift at 20.23; out 21.36–21.84) |
| 8 | C110 | 22.12–25.28 | woodcut Lakshmi | woodcut print | dissolve in |
| 9 | C107 | 25.28–27.80 | woodcut figures | woodcut print | Warp |
| 10 | C100 | 27.80–30.96 | curtain pillar → chandelier | gold chandelier | ASC CDL gold; exposure ramp; ends before its tail smear |
| 11 | C101 | 30.96–34.12 | peacock dome + Durga | gold chandelier | static; 91.25 %; exposure ramp −0.8 → −0.15 over its first second (source auto-exposure settle); frame 35.76 held 4 frames over a knock; ASC CDL gold; v4: 92.4 %, hold 32.76 → 34.12; v4c: **Frame Blending** on the 92.4 % piece (frame sampling repeated single frames at 31.00 / 32.04 / 32.56) |
| 12 | C096 | 34.12–37.28 | gold Durga with the lion | gold chandelier | replaces C099 (v3b); reframed **62 % / y 0.60** (v4b) so no heads rise into the bottom during the pan; ASC CDL gold; −0.15 stop |
| 13 | C087 | 37.28–40.44 | REVEAL on the peak: Durga through the giant wrenches | forge | **rotated 180°** (recorded upside down); −0.2 stop, highlights −20 |
| 14 | C089 | 40.44–45.48 | optical zoom into Durga, hold | forge | 100 % (no retime); reframed **84 % / y 0.84** (v3c) so every phone is below frame; frame 45.92 held 7 frames over a source focus breath |
| 15 | C139 | 45.48–48.00 | Durga face | red-gold | rotated 180°; from its focus snap; sat 72 |
| 16 | C083 | 48.00–50.52 | callback: pastel Durga whole | pastel Durga | dissolve in |
| 17 | C088 | 50.52–55.60 | last look, end card | forge | pull 106→100; animated end card; fade out; **tracked phone mask** (V2 50.28–55.60, `renders/overlays/c088_phone_mask_tracked.mov`, ProRes 4444 alpha from `tools/phone_mask_tracked.py`): the three lit screens are black from C088's first frame (ramping with the 50.28–50.76 dissolve), so they read as phones held up with the screen off; no crop, deities untouched (v4c; v4b's static soft PNG ramped in over ~1.5 s and missed the screens' drift) |

## 5b. v3 additions (approved by the director 2026-10-18)
- **Type & graphics:** title and end card become HyperFrames motion graphics (ProRes 4444 alpha on V5): one calm focus-pull settle (blur ≈ 12 px → 0, tracking wide → 8 px, opacity 0 → 1 over ≈ 1.0 s, ease-out), clean hold, fade-out; DIN Condensed Bold, cream `#F5E6C8`, **stronger dark soft halo** (no gold glow), 25 fps. Title `PUJA NIGHTS · 2026` 0.80–4.20 at y ≈ 1423–1499; end card `@satyajitmall` 56.08 → end at y ≈ 356–433, fading with the picture.
- **Text behind the subject (one moment, director's pick):** **"MAA" behind the folk Durga on C095** (she holds a trishul), on its steady hold after the tilt (≈ 21.9–24.2), baked with `scripts/text_behind.py` on V1 before colour. Alternative: C083 pastel Durga, only ≈ 1.6 s of clean matte. C089 and C139 fail the matte test.
- **AI-generated shots:** none. No gap the director's own footage can't fill; $0.
- **Gate fixes from review v2:** reveal = C087 → C089 (100 %, reframed to drop the phones) → C139; chandelier = C100 → C101 (static, 91 %) → C099 (calmest 2.48 s).

## 6. Must-haves / must-NOT-haves
- Must: one continuous music stretch (IG sync); cuts on the grid; calm pacing; reference-matched warm dark grade with gold intact.
- Must not: impact shakes or snap zooms on handheld footage; decorative AE looks; invented filler words on screen; outside stock footage.

## 7. Open questions
1. ~~Title~~ → `PUJA NIGHTS · 2026`. ~~Location tags~~ → none.
3. **IG audio:** check that Shondhatara is in your Instagram music library and that you can start it at 3:31.9. If IG's version differs, I re-sync the cut to it.
4. **Premiere:** `my-reel.prproj` is open and the my-reel session is still active. This reel needs its own project (`projects/puja-night-2/puja-night-2.prproj`); I'll ask before switching.

## Changelog
- 2026-10-18 v1 approved at Checkpoint 1 (hook A, 14-shot EDL, Match Reference, title `PUJA NIGHTS · 2026`, no tags).
- 2026-10-18 v1 build: title moved from top to lower third (collision with the pandal banner); end card runs to the end and fades with the picture; Warp on C105/C093/C090 (measured shake), no push on C093; music −2.5 dB with fades; look values as measured. Runtime 59.80 s (frame-quantised from 59.82).
- 2026-10-18 v1b (review gate loop 1 fixes, before the director has seen anything): C105 → **C107** (source motion-blur jerk on C105); ARRIVE re-timed on the grid: C103 0–5.36, C132 5.36–10.08, C081 10.08–13.72 (its sharp tail + focus snap on the beat); reveal re-timed: C089 39.60–45.32, C139 45.32–49.72 (skips C139's soft first frames); title lowered to y 1486–1559 at 104 px; saturation 80 on C132/C095/C139, C132 +0.65 stop; Warp on C107. Runtime unchanged 59.80 s.
- 2026-10-18 v1c (review gate loop 2 fixes, still before the director has seen anything): **15 shots** (was 14). ARRIVE: C130 added (inside the red pandal) and C081 cut to its 1.24 s sharp tail (C081 is out of focus until source 4.40). Lift: C090 ends on the 16.24 hit, C092 replaces C093. Chandelier: C107 ends at 30.76, C100 30.76–33.96 with an exposure ramp, C099 33.96–39.60. Reveal: C089 from its focus snap, slowed 6 % to the 47.20 bar; C139 from its focus snap (source was soft until 9.52, not 7.68 as first measured at half resolution). Title y 1423–1499. Runtime 59.80 s.
- 2026-10-18 **v2** (round 2, director notes on v1c): C099 stabilised (Warp; shake 5.5 → 2.4 px; its 1–2-frame source motion blurs remain); chandelier C099/C100 pushed toward gold with ASC CDL (hue 20–22° → 30–32°); red pandal shots C132/C130/C095/C139 saturation 80 → 72; C090 reframed (scale 66 %, y 0.63) so the bald head and phone are out of frame. Cut, timings and music unchanged (59.80 s, 15 shots).
- 2026-10-18 **v3** (round 3; HQ relayed the director's wish for the new studio features; director approved the plan): animated HyperFrames title + end card (ProRes 4444 alpha on V5, stronger dark halo); "MAA" behind the folk Durga on C095 (tracked bake, V2 overlay); review-v2 fixes: reveal = C087 → C089 (100 %, reframed) → C139; chandelier = C100 → C101 → C099 (2.48 s). AI-generated shots: none. 17 shots, 59.80 s.
- 2026-10-18 **v3b** (review v3 fixes): C099 → **C096** (gold Durga with the lion, chandelier pandal; clean throughout); C089 reframe 68 % → 82 % / y 0.818 (phones fully out); C090 reframe 66 % → 70 % / y 0.67. C101's 3-frame source knock at 35.8 stays (all 2.92 s of the clip are in use).
- 2026-10-18 **v3c** (review v3b fixes): C087 rotated 180°; C096 56 % / y 0.56; C089 84 % / y 0.84 + 7-frame hold at 45.92; C090 75 % / y 0.75; C101 exposure ramp + 4-frame hold at 35.76.
- 2026-10-19 **v4** (round 4): music switched to **D 1:45.60–2:41.20** (director); all 17 shots re-timed onto D's grid (no shot dropped): C103 0–3.80 cut on the strongest accent; "MAA" fades in on the lift (20.23); C089's zoom rides through the loudest bar (42.96); dissolves 22.12 / 48.00 / 50.52; end card 51.88; runtime 55.60 s. Every grade, crop, rotation, hold and overlay carried over from v3c.
- 2026-10-19 **v4b** (review v4 fixes): C088 bottom-left phone screens darkened with a soft local mask (no crop, deities untouched); C096 62 % / y 0.60; C101 and C089 holds now run through to their cuts (no resume jump); C130 slipped 0.4 s earlier (source 2.40–4.92).
- 2026-10-19 **v4c** (review v4b fixes; gate limit reached, verified by the editor): C130 starts on the 8.85 accent (8.84–10.12, source 3.00–4.28) and ends before the phone raise; C132 extended to 8.84 (source 0.12–5.16); C088 phone screens covered by a tracked mask from the shot's first frame; C101's 92.4 % piece uses frame blending (no repeated frames); music ends on an Exponential Fade 54.56–55.60 with the picture. C139's dark phone in the IG bottom band, C096's tail smear and C100's softness left as they are (see project.md). Runtime 55.60 s.
- 2026-10-19 **v5** (round 5, director notes on v4c): DURGA Marvel-style intro (footage inside the letters) replaces the C103 hook + title card; 30-shot dramatic cut on the hit map (flashes, two-beat cuts, hero holds), new footage (forge, scaffold, giant red feet, C112 shrine), speed-ups, snap zooms, white flashes, SFX; cinematic warm grade (V3 Lumetri + ASC CDL); ending on the C112 Durga push-in. C100, C130, C081, C083 out. Runtime 55.60 s.
- 2026-10-19 **v5b** (review v5 fixes): C098 (whip + phone) and C099 (soft hold) dropped; C096 27.80–30.32; C135 extended to 30.32–35.36 with five snap zooms; reframes on C103 / C128 / C134 / C091 / C094; C134's second flash from its 12.0 s close-up; C133 from 5.44; intro subtitle 86 px and the dark forge fill swapped for the woodcut; swishes and whoosh −13 dB. 28 shots + intro, 55.60 s.
- 2026-10-19 **v5c** (review v5b fixes; gate limit reached, verified by the editor): C085 and C086 rotated 180° (were upside-down); C135 top-anchored 128 % with snaps to 168 % (crowd and phones into the IG band); the 35.96 flash is a second C086 moment (was C134 with a lit phone); C092 cropped right; C112 highlights −35 / −0.25 stop / sat 85 (red clipping 7.1 % → 0.6 %); C094 116 %, C091 114 %; C101 from source 0.16; DURGA word 840 × 600 px. 28 shots + intro, 55.60 s.
- 2026-10-19 **v6b** (round 6): all moving shots stabilised (Warp, analysed); C096/C091/C087 on steadier source stretches; C116, C109, C124, C083 in; MAA + zoom punch out; beat transitions (zoom-through ×2, whip ×3, gold leak, warm dip); per-shot tone match. 55.60 s.
- 2026-10-19 **v6c** (review v6b fixes): C089 hold = stabilised last frame; C091 steadier stretch; C109 → C105; C124 / C132 / C116 / C133 reframed top-anchored (phones and faces into the IG band); tone nudges. 55.60 s.
- 2026-10-19 **v6d** (review v6c fixes; gate limit reached, verified by the editor): C087 out, C129 extended to 40.44; C132 un-nested, 150 % with Optical Flow; C086 warmed; C085 / C116 / C091 reframed, C129 / C132 / C133 / C135 tone. Zoom-through 3.80 and gold leak 40.44 re-baked. 55.60 s, 27 shots + intro.
