# Brief — written by the editor, approved by the director

> Claude writes this file after the interview and footage analysis. The director only answers questions, shares references, and approves. Don't fill it in by hand; ask Claude to change anything.

**Status:** approved on 2026-10-16 (hook 1, words as proposed, English only; handle @satyajitmall; font Anton/Bebas-style)

## 1. The idea
- **Reel type:** `music-montage` (no speech; CLAUDE.md §4a + §4c)
- **One-line concept:** *Many faces, one Shakti.* Four goddesses hit on the track's four opening accents, then a beat-cut tour of the pandals' craft, a roar on the last accent, and a quiet blue goddess to close.
- **Story arc:**
  - setup: blue chandelier tilts down to reveal Durga (0–2.2 s);
  - turn: four idol faces slam in on the four accents with DUM · DUM · DURGA · MAA (2.2–12.4 s);
  - build: pandal craft tour, one shot per bar (12.4–31.7 s);
  - payoff: Narasimha roar on the last accent, push into gold idols, blue Durga hold + end title (31.7–41.3 s).
- **Goal:** goosebumps / pride.
- **Audience:** filmmaker / creator crowd, so the craft (grade, beat-sync, camera moves) has to be visible.
- **Target length:** 41.3 s (music 61.88 → 103.15 s of Dum Durga, natural outro).

## 2. Hook (0–3 s)
- **Moment:** C010 (blue-lit Durga), src 0.30 → 2.62 s: camera tilts down from the blue chandelier to her face. Hard cut on **accent 64.11 s (reel 2.23 s)** to C077 (gold Durga slaying Mahishasura), src 7.60 s.
- **Visual move:** slow push 100 → 106 % on C010; snap zoom 100 → 118 % over 5 frames on C077; cool → gold colour jump is the hit.
- **On-screen text:** "DUM" pops on the hit.
- **Sound:** riser from 1.23 s, sub-hit / bass drop on 2.23 s.

## 3. References → concrete parameters
| Reference | What we take from it | Measured |
|---|---|---|
| `ref1-filmmakerguy.mp4` (@the.filmmaker.guy, 21.6 s, 30 fps) | Dark, beam-lit, idol-led framing; detail inserts (face, hands) between wides; reverent pace; gold type on dark. **Not** taken: its 7 s opening hold (breaks our 3 s hook) and its cool blue grade (our footage is gold; blue kept only on C010/C011 as an accent). | 8 cuts, avg shot 2.41 s, median 1.6 s, shortest 0.57 s, first cut 7.1 s. Exposure 0.12, cool (−0.05), 25 % crushed shadows |

Our measured plan: 20 shots, avg 2.06 s, median 1.76 s (one bar at 136 BPM), shortest 0.88 s (2 beats).

## 4. Treatment
### Pace
- 136 BPM: beat 0.441 s, bar (4 beats) 1.765 s.
- Accents section (2.23–12.38 s): cut on every accent (64.11, 66.32, 68.96, 71.61 → reel 2.23, 4.44, 7.08, 9.73).
- Groove (12.38–31.74 s): one shot per bar, cut on every 4th beat; one 2-beat flurry at 28.24 s.
- Payoff: accent 93.62 (reel 31.74), last beat 98.03 (reel 36.15), outro hold to 41.27.
- Hard cuts by default; match the camera direction of adjacent shots where possible (tilt-down → tilt-down).

### Colour
- **Sequence:** 1080×1920, **25 fps** (65 of 77 clips are 25 fps). C003, C006, C010, C011 are 24 fps → `speed_change` 104.17 % to conform frame-for-frame (source span = slot × 1.0417).
- **Primary correction (per clip, V1, one `color_correct` each):** footage is 1–2 stops under (exposure 0.14–0.38), very saturated, warm. Direction:
  - brightness +15…+25 on C044, C041, C077, C076, C074 (exposure < 0.2); +5…+10 on the rest;
  - highlights −20…−30 on C046 (yellow wall 0.5) and C072, C056 (bright lamps);
  - saturation −10…−15 at clip level where the analyser says "very saturated" (all but C056);
  - temperature: leave C010/C011 blue; trim warm cast −5…−10 on C029, C058, C077 only where skin/idol faces go orange;
  - no log footage (all Rec.709 SDR, 8-bit), so no conversion LUT.
- **Shot matching:** idol run C077 → C003 → C058 → C044 within ±0.04 exposure; groove run matched to C029 as the anchor.
- **Creative look — "Gold & Shadow" (V3 adjustment layer):** `gemini_warm_film_2383.cube` at 50 %, contrast +15, saturation −15, shadows −10 (deep blacks, gold highlights), vignette −1.0. Blue shots will pick up a little warmth from the LUT; accepted so they still read as the cool accent.
- **Texture (V4):** `gemini_film_grain_16mm.mp4` looped end to end, Overlay, 40 % (also hides 8-bit noise from lifting shadows). No light leaks.

### Effects & transitions (signature moments only)
| Reel time | Move (playbook) | Where |
|---|---|---|
| 0.00–2.23 | Slow push 100→106 % | C010 |
| 2.23 | Snap zoom 100→118 % in 5 fr | C077 entry |
| 4.44 | Flash cut, Dip to White 3 fr | C077 → C003 |
| 7.08 | Impact shake ±12 px, 6 fr decay | C058 entry |
| 21.20 | Whip / zoom blur, 5 fr each side | C041 → C046 |
| 30.00–31.74 | Speed ramp: 200 % → 100 % | C076 (Shakti Stambha text) |
| 31.74 | Flash cut + impact shake | → C072 Narasimha roar |
| 36.15–41.27 | Slow push 100→108 %, fade to black last 0.5 s | C011 |
Non-cut transitions: 4 in 41 s (flash ×2, whip, fade). No fake slow-mo (all footage ≤ 25 fps).

### Type & graphics (kinetic beat words, V5)
- Words on accents: **DUM** (2.23) · **DUM** (4.44) · **DURGA** (7.08) · **MAA** (9.73) · **SHAKTI** (31.74). Each holds to the next cut or ~1.5 s.
- End card 37.0–41.27: "DURGA PUJA 2026" + @satyajitmall.
- Style: bold condensed sans (Anton / Bebas Neue), warm white #F5E6C8 with a soft gold glow, centred at y ≈ 700 px (inside safe zone), pop-in scale 120→100 % in 3 frames. Built with `/hyperframes` → alpha `.mov` in `renders/overlays/`, or `add_text_overlay` if it renders clean.

### Sound
- **A3 music:** `inhaleexhalestudio-dum-durga-530246.mp3`, 61.88 → 103.15 s, full level, peaks −1…−3 dB, no ducking, natural outro ends the reel.
- **A1:** clip natural sound muted.
- **A2 SFX (−14…−18 dB):** riser 1.23 s (hit at 2.23) · bass drop 2.23 · camera shutter 4.44 · snap swish 7.08 · whoosh 21.20 · shutter + bass drop 31.74 · text-pop click on each word (−18 dB).

## 5. Clips
| Clip | Role | Notes from the analysis |
|---|---|---|
| C010 | hook | blue Durga, tilt-down reveal 0.3–3.0 s, 24 fps, exp 0.21, cool/magenta (keep) |
| C077 | hero (accent 1) | gold Durga + Mahishasura, revealed 3.7–9.6 s, exp 0.175 |
| C003 | hero (accent 2) | white ten-armed goddess, zoom-in 0.6–5.3 s, 24 fps, exp 0.22 |
| C058 | hero (accent 3) | orange Durga, exp 0.32, phone-holders enter frame after ~5 s |
| C044 | hero (accent 4) | red Durga + lion tableau, exp 0.14 (needs lift) |
| C006 | groove | diya-lined arcade, 24 fps, exp 0.24 |
| C029 | groove / match anchor | temple facade, exp 0.31 |
| C031 | groove | lantern street, people walking in, exp 0.27 |
| C034 | groove | bamboo umbrella figure vs night sky, exp 0.24 |
| C041 | groove | colourful wide pandal, exp 0.145 |
| C046 | groove (whip in) | yellow "Tel" wall, exp 0.5 — pull highlights |
| C056 | groove | gold lattice panels, exp 0.38 |
| C068 | groove | glowing panels tracking shot, exp 0.32 |
| C064 | groove | Kaalrekha pillars, dusk, exp 0.33 |
| C016 | flurry | engraved gold disc, exp 0.28 (check orientation in rough cut) |
| C074 | flurry | Khambeshwari face carving, exp 0.22 |
| C076 | ramp + payoff | "SHAKTI STAMBHA" text 0–4 s, push into gold idols 16–19 s, exp 0.21 |
| C072 | payoff (accent 5) | Narasimha roar, exp 0.38 |
| C011 | outro | blue Durga hold, 24 fps |
Rejected: C001, C002, C025, C042, C049–C053 (exposure ≤ 0.06, unrecoverable); C008, C018, C022, C023, C032 (recorded upside down; usable with 180° rotate if wanted).

## 6. Must-haves / must-NOT-haves
- Must: every cut on the beat grid; hook hit at 2.23 s; music's real outro ends the reel.
- Must not: fake slow-mo; creative LUT on clips; cut off the grid except the outro hold.

## 7. Open questions
- ~~Handle~~ resolved: @satyajitmall, Anton/Bebas-style. All moves built from own footage (no outside stock).
- Kinetic words OK as DUM · DUM · DURGA · MAA · SHAKTI? Bengali script instead of / alongside English?
- OK to remove the 17 Adobe sample clips + auto `Sequence 01` from the project?
