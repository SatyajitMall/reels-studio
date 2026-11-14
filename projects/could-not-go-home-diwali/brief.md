# Brief — written by the editor, approved by the director

**Status:** draft for Checkpoint 1, **v1c** (2026-11-09), after the notes on p1 ("no slow motions no cinematic effect") and p1b ("distortion, in and out focus, framing") · EDL `analysis/edl_v1c.json` (built by `tools/build_edl_v1c.py`) · preview `renders/previews/could-not-go-home-diwali_p1c_phone.mp4`

## 1. The idea
- **Reel type:** `music-montage`: no speech; the letter appears as on-screen lines over the reference's original audio.
- **Playbook:** `cinematic-montage`. **Overrides:**
  - **Letter lines on screen** (6 Hinglish lines + small English lines) instead of "title + end card only". The director supplies the words' meaning (they chose letter A); the playbook allows words that mean something.
  - **Line table: one worker per line, 2 shots per line** (director profile: one shot / subject per line, never the same person twice).
  - **4:3 window** for landscape footage (the director's pick; not yet in effects-playbook §B: CR-20261109-…-round2-sheets).
  - **No swishes, risers or SFX at all.** Plain cuts (director profile); the IG audio carries the sound.
- **One-line concept:** a letter home from the people who kept the city running on Diwali night: "Maa, is baar ghar nahi aa paaunga."
- **Story arc:** the apology (auto driver) → why (the busiest night: parotta maker) → what's missed (Maa's food, over a cook feeding strangers) → how they'll be there (aarti on the phone) → reassurance (tell Papa I'm fine) → promise (next year: the car-washer looks up, the next morning) → sign-off "— tumhara beta".
- **Goal:** viewers far from home this Diwali feel seen, and **send it** to family or a friend who's also away. Respect, not pity.
- **Audience:** Indians living away from home (students, migrants, workers), and their families.
- **Target length:** **20.80 s**, capped by the audio (howwdeep.exe's original audio, 20.8 s).

## 2. Hook (0–3 s)
- **Moment:** `01_C047_auto`, camera C047 at 0.60 s: from the back seat of an auto, the driver's shoulders against a rain-wet, Diwali-lit street moving through the windscreen. It lands on the guide's first accent (0.07 s).
- **Visual move:** slow push 37.5 → 39.5 % (inside a steady hold, `motion.json` 0–8.2 s); the street moves from frame 1.
- **On-screen text:** L1 "Maa, is baar ghar nahi aa paaunga." / "Maa, I can't come home this time." from 0.20 s. At 1.56 s the driver turns his head into profile (`02_C048`).

## 3. References → concrete parameters
| Reference | What we take from it | Measured (`analysis/teardown/TEARDOWN.md`) |
|---|---|---|
| howwdeep.exe, "Sorry maa, Diwali me nahi aa paunga" (IG DQDqyKGD5CK) | the idea (workers on Diwali, a line to Maa), the 4:3 window, its audio (with the creator's OK), small italic type | 20.8 s · 16 cuts · median shot 1.17–1.33 s · first cut 2.62 s · muted teal film look · −14.1 LUFS |
| **Ours (deliberate differences)** | six letter lines instead of one, so **2 shots per line at 1.56–1.62 s** (calmer, to read); **camera-true** colour instead of the teal look; the director's depth (Apple Cinematic, f/2) | 12 shots + end card · median 1.58 s · first cut 1.56 s |

## 4. Treatment
### Pace
- Cuts on the guide's **bar downbeats** (152 BPM, bar 1.579 s; frame-snapped 0 / 1.56 / 3.12 / 4.68 / 6.24 / 7.84 / 9.44 / 11.04 / 12.64 / 14.24 / 15.80 / 17.40 / 19.00). Each line holds 2 bars (3.12–3.20 s); shot length 1.56–1.62 s.
- Energy: low intro (L1–L2) → full section 6.25–9.45 s carries **L3**, the hero line (Maa's food, over the cook) → mid (L4–L6) → the beatless tail holds the end card (19.00–20.80).
- Hard cuts only; a 3-frame black breath before the end-card text (19.00–19.12).

### Colour (camera-true, effects-playbook §A0)
- **Depth first:** every shot is the **Apple Cinematic bake at f/2** (`tools/cine_bake`, `raw/baked/`), the director's intended picture. Bake check: within ±0.003 luma of the camera inside the window; the deepest shadows sit ~1 code value lower (see exceptions).
- **Primary correction (A1), per clip, toward the camera file:**
  - C047 / C048 (auto, night, luma 0.23): lift exposure until the street lights start to burn (≤ 2 % at 255), no more.
  - C052 / C053 (stall, magenta-cool LED, G−M −0.07): pull a little magenta out of the skin with tint. The purple backdrop is real light and stays.
  - C050 / C051 / C054 / C062 (warm sodium/LED nights): balance only if skin turns orange; keep the camera's warmth.
  - C063 / C064 (daylight, Nov 9): none expected.
- **Shot matching (A2):** within each line's pair (01↔02, 03↔04, 05↔06, 07↔08, 09↔10, 11↔12), within the camera bands.
- **Creative look (V3): none.** Camera-true, the director's pick in Round 2.
- **Texture (V4): none** (night phone footage).
- **Camera-check exceptions:** `01_C047_auto` and `02_C048_auto_turn` (the auto interior): the bake puts the deepest shadows ~1 code value lower (p01 0.010 → 0.006; the share under 0.05 is unchanged, 26.4 → 26.9 %). Invisible; allowed. Checked with `tools/window_fidelity.py`, because `camera_fidelity.py` can't measure inside a window yet (CR-20261104 item 6).
- **Framing:** 4:3 window = Rotation −90, **Scale 37.5**, Position (540, 910): **75 % of the camera width**, 1080×810 between y 505 and 1315, with the matte on V5. Pushes to 39.5 on holds (71 %).
- **Framing exception:** `08_C062_vendor_close` (Scale 46 in 4K terms, Position 787,830): **61 % of the width**, the closer second beat of the vendor. The v1/v1b parotta close is gone (it cut his head). With the +5 % push, base shots end at ~71 % of the camera width (~68 % on the three stabilised shots). Each is the closer second beat of its worker (face and hands at the tawa; the vendor's face and phone). No upscaling: the 4K source still downsamples.

### Effects & transitions (v1c)
**Rule from the director's notes:** slow motion only where the interpolation stays clean; work and hands in real time; no focus pulls; framing never cuts a head.

| Shot | Reel | Camera window | Speed | Depth | Stabilise | Framing |
|---|---|---|---|---|---|---|
| 01 auto street | 0.00–1.56 | C047 0.60 + 1.10 s | **70 %** | f/2 recorded focus | – | 75 → 78.75, top-anchored |
| 02 driver turn | 1.56–3.12 | C048 2.72 + 1.56 s | real time | f/2 | – | top-anchored push |
| 03 parotta (one held shot for L2) | 3.12–6.24 | C054 0.32 + 3.12 s | real time (the lift at ~4.8 s) | f/2.8 | position only | top-anchored push |
| 05 cook plating | 6.24–7.84 | C052 1.00 + 1.60 s | real time | f/2.8 | – | top-anchored push |
| 06 hand-off | 7.84–9.44 | C053 1.20 + 1.60 s | real time | f/2.8 | – | top-anchored push |
| 07 vendor | 9.44–11.04 | C062 0.52 + 1.60 s | real time | f/2 | position only | centred push |
| 08 vendor close | 11.04–12.64 | C062 4.92 + 1.60 s | real time | f/2 | – | Scale 92 @ 787,830 |
| 09 paan | 12.64–14.24 | C050 0.40 + 1.60 s | real time | f/2.8 | – | top-anchored push |
| 10 paan look | 14.24–15.80 | C051 0.20 + 1.10 s | **70 %** | f/2 | position only | top-anchored push |
| 11 car-washer | 15.80–17.40 | C063 0.90 + 1.60 s | real time | f/2.8 | – | x 470 (toward him), top-anchored |
| 12 look-up | 17.40–19.00 | C064 7.10 + 1.28 s | **80 %** | f/2 recorded focus | – | top-anchored push |

- **Slow motion** (build: AE Timewarp, Pixel Motion): 01, 10, 12 only. Tested in the preview with minterpolate. 02, 07 and 08 at 80 % ghosted pedestrians and garbled the hanging jewellery, so they stay real time.
- **Depth:** the camera's recorded focus on every shot (steady: range ≤ 0.11 per shot). f/2 as shot; **f/2.8 on the hands shots** (03, 05, 06, 09, 11) so hands and tools don't swim through the blur. **No rack pulls** (rejected on p1b).
- **Stabilise** (build: Warp Stabilizer, *Position* method, no rotation/scale) only 03, 07 and 10.
- **Motion:** +5 % push on every shot, anchored on the window's top edge wherever a head is near the top.
- **Transitions:** none: hard cuts on the downbeats. The end card cuts in from black.
- **After Effects:** Timewarp on 01, 10 and 12.

### Type & graphics (V5)
- **Letter lines:** Baskerville Italic **54 px**, cream `#F5E6C8`, in the black band under the window (x 70, y ≈ 1363; inside the safe zone, clear of every face). English line in Baskerville Italic **34 px**, 80 % white, under it. From each line's first cut + 3 frames (+5 for L1) to its last cut − 2 frames; a 3-frame fade in and out in Premiere (PNGs: `renders/overlays/line_0N.png`).
- **End card (19.00–20.80):** black. **"Mera diya bhi jalaana"** in **Rozha One** 92 px, cream, soft gold glow; "light my diya too" Baskerville Italic 36 px; **"— tumhara beta"** Baskerville Italic 50 px; small **@satyajitmall** (Helvetica Neue Light 28 px) at y 1500 (`renders/overlays/end_card.png`).
- **Window matte** `renders/overlays/window_matte_4x3.png` on V5 under the text.
- **Cover (Phase 8):** a designed cover (a strong frame + the title in Rozha One), from C064's look-up or C051's far-off look, picked from a sheet.

### Sound
- **Guide:** `audio/guide_ref.wav` (howwdeep.exe original audio, stereo, 20.8 s, 152 BPM; `analysis/audio_summary.md`) on A3, full level in `_mix`, fade out over the last 0.2 s. **Muted in `_IG`**: the director adds it in Instagram with "Use audio" from 0:00.
- **A1 natural sound:** muted. **A2 SFX:** none.
- `_mix` −14 LUFS ± 2, true peak ≤ −1 dBTP (the preview measures −14.1 / −1.0).

## 5. Clips
All camera clips are Blackmagic Cam, iPhone 17 Main, 25 fps, HEVC 8-bit, Apple Cinematic (f/2), held landscape (tag −90 → Rotation −90). Baked copies in `raw/baked/` (`analysis/bake_map.json`).

| Clip | Role | Window used (camera s) | Notes from the analysis |
|---|---|---|---|
| C047 | hero / hook | 0.60–2.16 | hold 0–8.2 s; dark interior (luma 0.23), lit street |
| C048 | B | 2.40–3.96 | driver turns into profile ~3.0–3.5 s |
| C054 | B ×2 | 0.32–1.88, 3.92–5.48 | handheld, no hold; warm |
| C052 | hero (L3) | 1.00–2.60 | hold 1.0–5.0 s; magenta-cool stall light |
| C053 | B | 1.20–2.80 | handheld; serving a customer |
| C062 | B ×2 | 0.52–2.12, 4.92–6.52 | ends before the 6.7 s tilt-up |
| C050 | B | 0.40–2.00 | hold 0–3.3 s; VFR (24.967): check the placed window |
| C051 | B | 0.20–1.76 | ends before the 2.5 s whip |
| C063 | B | 1.00–2.60 | hold 0.8–3.7 s; daylight |
| C064 | closer | 6.72–8.32 | looks up toward the camera; ends before the 8.4 s move |

**Not used:** C043 (near black), C049 (third auto angle), C055 (shaky), C056 (juice man), C057/C058 (stage crowd), C059 (ice-cream server), C060/C061 (wheelchair man and the woman on the pavement: left out so the letter reads as respect, not pity; available on the director's call).

### Line table
| Line | Shots | What in the frame shows it |
|---|---|---|
| Maa, is baar ghar nahi aa paaunga. / Maa, I can't come home this time. | 01 C047, 02 C048 | the auto driver working Diwali night, driving others; he turns his head as if remembering |
| Yahan Diwali pe sabse zyada kaam hai. / Diwali is our busiest night here. | 03 C054, 04 C054 close | the parotta maker flipping at a busy stall, then his face over the tawa |
| Tumhare haath ka khaana yaad aata hai. / I miss food made by your hands. | 05 C052, 06 C053 | the young cook's own hands plating food for strangers, then handing it across |
| Phone pe aarti dikha dena. / Show me the aarti on the phone. | 07 C062, 08 C062 close | the vendor at his stall looking into his phone |
| Papa se kehna, main theek hoon. / Tell Papa I'm fine. | 09 C050, 10 C051 | the paan maker at work, then his still, far-off look |
| Agle saal, pakka. / Next year. Promise. | 11 C063, 12 C064 | the morning after, the car-washer still at work, then he looks up |
| — tumhara beta | 13 end card | title on black |

## 6. Must-haves / must-NOT-haves
- **Must:** every line on a different worker; text never over a face; cuts on the downbeats (±2 frames); the depth bake on every shot; the window steady at 4:3 for the whole reel.
- **Must not:**
  - pity framing;
  - transitions, whooshes, flashes, leaks or grain;
  - a creative look;
  - the same person in two lines;
  - any text in the IG bands.

## 7. Open questions
- None blocking. The cover frame is picked in Phase 8 from a sheet.

## 8. Changelog
- **v2 (Checkpoint 1):** a creative look is allowed now. The director picked the **reference look** (`analysis/look_ref/ref_match.cube`) at 60 % on the V3 adjustment layer. This replaces "must not: a creative look" in §6.
- **v2b–v2d:** the inserts come from the same workers (hands at work). Stock is used only for home (S1, Maa's hands) and for Diwali work (F8, marigold hands).
- **v3 (approved "Build, reference look"):**
  - 30.76 s, 6 letter lines × 3 bars, 18 shots, 16 of them the director's;
  - step-print (3-frame holds, the reference's "slow down") on 01 (the auto and the bus) and 12 (the Diwali show);
  - one slow-motion shot, 18 (80 %, AE Timewarp);
  - placeholder audio: howwdeep's guide looped. The final song is still open.
  - The shot list is `analysis/edl_v3.json`, and the line table in §5 is superseded by it.
- **v3b (build fixes for "jumps, misalignment, shake, frame rate"):**
  - Warp Stabilizer (Position/Scale/Rotation) on 02, 05, 10, 11, 14 and on the step-print sources;
  - 05, 06, 10 and 11 moved to clean stretches of their clips;
  - jump cuts broken by size changes: 08 becomes a hands close-up, 11 a true close-up, 02 a punch-in.
  - The recipe is `tools/build_premiere_v3.py`.
- **v3c (Checkpoint 2 notes, 2026-11-11):**
  - **01 (the auto) plays in real time**, stabilised: `STAB_v3c.mov` frames 8–46. The step-print on 01 is gone; the director called it glitchy. 12 keeps its step-print, from a steady source.
  - **Look = the roti shot's grade.** The director: "the hand making the roti is the most cinematic shot ... apply that throughout the reel", "50 % or less".
    - V3 carries `analysis/grade_v3c/roti_match.cube`: a per-channel match of all shots to 07 as rendered in v3b. Lumetri Intensity 45 is just under a 50 % mix (calibrated by render).
    - 07 itself keeps `ref_match.cube` at 40 on its own V3 segment.
    - Even across the frame: a depth-based subject lift was tried and rejected for its edge halo.
  - **Per-shot balance:** one Lumetri per V1 clip (Exposure −1.0 to +1.0 stops, `analysis/grade_v3c/balance.json`). Every shot starts from one mid-brightness, so the look sits evenly.
    - 01 and 02 stay darker: the auto interior, at the +1-stop clamp.
  - **Intent for the reviewer:** a matte, warm, low-contrast picture family matching 07; no shot should jump in brightness or colour against its neighbours. Camera-true is no longer the target, so the camera check is skipped (`--look`).

### v3f changelog (2026-11-11, director's v3c notes)
- **15:** C061, the man in the wheelchair (bake f/2, frames 34–73), replaces the ice-cream server under L5 "Papa se kehna, main theek hoon".
  - The director asked for him ("why are we not using it?") and kept him after seeing the reviewer's pity-risk note ("Keep wheelchair man").
  - This overrides the "Not used" line above for C060/C061.
- **Stabilising:** 01/02/10/11/14 re-solved over only the frames played. Crop 105–113 %. 01's shake 6.6 → 1.7 px.
- **Framing:**
  - 02 Scale 54→56.7;
  - 03 marigold at stock 7.60 s with the window at the stock's right edge;
  - 07 roti flat at Scale 75, slid right (the stock has no picture below; the director kept Maa's hands over free stock).
- **Order:** 17 wash, then 16 foam, then 18, so there's no same-angle cut.

### v4 changelog (2026-11-11, director's notes after the v3f picture lock)
- **Letter lines move onto the picture** (layout B, like the reference); the 4:3 window stays.
  - Baskerville Italic 44 px (cream) / 28 px (80 % white), with a soft shadow, two balanced lines at most.
  - Each line sits in the corner of the picture that is clear of faces and the working hands through all its shots: L1 bottom-right, L5 top-left, the rest bottom-left.
  - This replaces the "Letter lines … in the black band under the window" rule above.
- **Depth:**
  - 10/11 (vendor) at f/4: the f/2 blur flickered on the hanging jewellery strands.
  - 13 (paan maker) at f/1.0, for more separation from the busy background.

### v4d changelog (2026-11-11)
- **Type → the Kolkata reel's family** (the director's request).
  - Letter lines: Hinglish in Amita Bold, English in Eczar SemiBold caps; cream with a soft glow.
  - End card: Amita / Eczar caps / Tiro Bangla Italic.
  - This replaces Baskerville Italic.
- **Ending:** the car-wash trio cut to foam → his look up → **a boy looking at his sparkler** (Pexels 10142920, stock, credited), then the end card.

### v4f changelog (2026-11-11, director after approving v4e)
- **Last shot 19 (26.96–28.56):** the boy with the sparkler → **a man crouching to light a cracker at night**.
  - Source: Pexels **photo** 5882889 (Pragyan Bezbaruah, free licence, credited).
  - Director: "a middle-aged man bursting a cracker … would be really meaningful". No free video of one exists (Pexels and Pixabay video, Pexels and Unsplash photos searched), so he picked "A".
  - It plays as a still with a slow push. The 4:3 crop is rows 1620–3543; Scale 42.2 → 43.9 (×1.04), linear, held on his hands and the flame.
  - Under L6 "Agle saal, pakka." (bottom-left, unchanged), then the end card.
  - Stock is now 3 of 17 shots (03 marigold, 07 Maa's hands, 19 the man).

### v5 changelog (2026-11-11, director's picks after the story QC, `analysis/qc_v4g/QC_REPORT.md`)
- **15 → C059**, the ice-cream server on his break, texting home (own footage). This replaces the wheelchair man under L5. The director confirmed this reading after the review found he's on his phone in the whole clip, not serving.
- **06 → a third beat of the parotta maker** (C054, own footage), at a different size from 04. This replaces the juice man under L2.
- **12 stays** (the director kept the boy at the stage show).
- **19 → AI-generated**, the director's option C: "Animate photo with AI".

| AI shot | Why | Route | Prompt / negative | Cost | Label |
|---|---|---|---|---|---|
| **19_S31_man_cracker_AI (AI-generated)** | The director asked for a middle-aged man bursting a cracker. No free video exists (Pexels and Pixabay video, Pexels and Unsplash photos, 30+ queries). He picked Pexels photo 5882889 (Pragyan Bezbaruah), then chose to animate it, since a still reads as a photo (review_v4f minor, story QC). | Veo 3.1 Lite from the first frame `renders/gen/S31_first_frame_9x16.png` (the stock photo, 9:16; no raw footage sent). Draft 4 s 720p, then a final 8 s 1080p after the director approves the draft. | `renders/gen/S31_prompt.txt` / `S31_negative.txt` (film-emulation-prompts: camera and light only, no grade) | ≈ $0.12 draft + $0.40 final | **Instagram AI info label ON** (a realistic person, generated). The caption names the shot as AI-animated; the Pexels creator is still credited. |
- **v5 as built:**
  - **06** = `06_C054_parotta_close`: C054 bake frames 0–39 (before 04's 1.24 s), Scale 48 → 50.4, top-anchored, Exposure −0.3.
  - **15** = `15_C059_icecream`, as v3c had it (raw/baked/v2 in 13, Scale 37.5 → 39.375, Exposure −0.15).
  - **19** = `19_S31_man_cracker_AI` (**AI-generated**):
    - Veo 3.1 Lite final `renders/gen/S31_man_cracker_final_20261111-230951.mp4`, interpreted at 25 fps;
    - source frames 12–51: he lights the cone, it erupts about 12 frames in;
    - Scale 100.1 → 103, Position (540, 725); one Lumetri, Exposure 0;
    - cost $0.12 draft + $0.40 final.
- **v5b** (review_v5 fixes):
  - 19 Position y 725 → 785, so his crown clears the window top;
  - 19 Lumetri Saturation 85, Sharpen −30, so it sits with the matte real shots;
  - L5 sits top-right on 13, 14 and 15 (not top-left, as the v4 note says).

### v6 changelog (2026-11-12, director on v5b)
- **Text: Hinglish only.** The English translation line is gone from every letter line and from the end card. The director: "I just want the text to be ... Hindi written in English ... I don't want it to be translated in English and written across."
- **Font: Avenir Next Medium** (picked from `analysis/v5b_notes/font_options.jpg`), cream with the same soft glow and shadow.
  - End card: "Mera diya bhi jalaana" (Avenir Next Medium) / "— tumhara beta" (Avenir Next Italic) / @satyajitmall.
- **Frame: the whole 16:9 camera frame** ("I meant horizontal" → "Yes, 16:9 like this"). The window is 1080×608 at y 606–1214 (centre 910), replacing the 4:3 window (y 505–1315). This supersedes the 4:3 rule above.
  - Every shot: Scale × 0.75 and its offset from the window centre × 0.75, so the top-to-bottom framing stays and the width grows by 4/3. Clamped so the clip always fills the window.
  - 19 (AI, generated vertical) shows a 16:9 slice: head to knees, plus the fountain.
- **Corner per line, after a frame check:**

  | Line | Corner | Notes |
  |---|---|---|
  | L1 | bottom-right | |
  | L2 | top-left, 3 lines | |
  | L3 | bottom-right, 3 lines | 08 slid left (x 282) and 09 pushed 5 % and slid right, to keep hands clear |
  | L4 | bottom-left | lower |
  | L5 | top-right | |
  | L6 | bottom-left | 18 slid right (x 760) |

- **In-points:**
  - 03: stock at 5.80 s (was 7.60), a livelier stretch;
  - 19: AI source frame 22 (was 12), so it opens as the cone catches and isn't near-still.

### v7 changelog (2026-11-12, director on v6c)
The director asked: "What happened to the shots that you were supposed to replace according to the storyline?" (status sheet: `analysis/qc_v4g/qc_status_v6c.jpg`). Then: **"Replace both"**, and **"Yes, download it"** for the stock clip.
- **03 → C047, own footage** (3.12–4.68). Replaces the stock marigold hand.
  - The Diwali-lit street through the auto windscreen, from the back seat: the same ride and night as 01–02, and the brief's first hook.
  - Bake `raw/baked/C047_f2_00.12.mov`, frames 22–60 (a scooter rolls toward the auto).
  - Framed like 01: Scale 28.17 → 29.53. Exposure 0 (v7b; +0.6 in v7 made it the brightest of the ride, review_v7 minor 2), so it matches 01.
  - The V3 look runs at 28 over 01–03, the auto's segment.
- **12 → Pexels 34565049 (Priyanka Photo): a woman lighting a diya at home, the aarti he asks to see** (17.04–19.0). Replaces the boy at the stage show.
  - Source 12.96–14.92 s: the match at the wick, close, the camera still rising. The locked-off stretch after it fails the frozen check.
  - The whole 16:9 frame: Scale 56.34 → 59.06. Exposure +0.4, Saturation 80.
  - Real video, credited, no AI label. Home is stock and the city is the director's footage, as with Maa's hands (07).
- **L4 "Phone pe aarti dikha dena." moves top-left** (`v7_line_04.png`).
  - The new 12's bottom-left is bright yellow cards.
  - On 10, top-left clears the vendor's phone hand (review_v6 minor 3).
- **01 in-point 2 → 4** (STAB_v3d), for the hook's focus shift. The stabilised render ends at frame 42, so 2 frames is the most it can move.
- **Stock is now 3 of 17 shots:** 07 Maa's hands, 12 the home diya, and 19 the man with the cracker (AI-animated). The caption credits Priyanka Photo instead of Yan Krukau.

### v8 changelog (2026-11-12, director on v7b)
The director: "In that diya shot can we slow it down and fire cracker shot also, if it extends the clips that's ok, and in first auto shot can we not add motion blur outside the auto? making it more cinematic".
- **12, the diya at home: slow motion, 50 %**, After Effects Timewarp (Pixel Motion), the studio's slow-mo route for 25 fps footage.
  - Source 12.96–14.72 s → 3.52 s (88 frames, was 49): one bar longer.
  - The shot is a calm close-up at half speed, so it's a designed low-motion span (pregate `17.04-20.56:freeze`). The reviewer judges every frame.
- **19, the man and the cracker (AI): slow motion, 50 %**, Timewarp.
  - Before the retime, the 24 fps Veo final was conformed frame-for-frame to 25 fps, keeping its codes (`renders/ae_src/S31_final_conform25.mov`).
  - Source frames 22–61 → 3.2 s (80 frames, was 40): one bar longer.
  - A Frame Mix version was tried; the round-trip's time remap eased it into an S-curve, so it was dropped.
- **01, the auto: motion blur outside the auto only** (`tools/blur_01_v8.py`).
  - The openings were traced on the stabilised clip, and the driver's silhouette cut out with a margin.
  - Inside them: motion-interpolated blur with a 6-frame shutter, so the bus and lights streak along their real motion.
  - The driver, the pillars, the roof and the dashboard are untouched (within ProRes rounding).
- **Length 30.76 → 33.92 s.** Everything after 12 is one bar later, and everything after 19 two bars later, so every cut stays on a downbeat.
  - The guide (`audio/guide_loop_v8.wav`) has bar 4 inserted before the loop's bar 5 and bar 11 repeated before the tail.
  - The guide runs at −1.2 dB with the same end fade.
  - L4 runs longer over the slow 12, and L6 over the slow 19; the end card is at 31.72–33.92.
- **Unchanged:** grade, text, every other shot.

### v10 changelog (2026-11-12, director after approving v8b)
The director: 12 and 19 "look a little fake ... different from the rest of the footage ... the hand is not shaking, not moving, and the pan looks too good to be true. Don't need to change it, but optimise it so they blend."
- **12, the diya (Pexels stock), and 19, the man and the cracker (Veo AI):**
  - **Same picture, same timing, same slow motion, same Premiere keys and Lumetri.** Nothing is regenerated.
  - **The director's own handheld camera path** is added as a sub-pixel move inside a 2 % zoom. The path is measured from this reel's shots 13, 14, 16, 18 and 09, detrended, chained and scaled ×1.25.
  - **Grain matched to the director's clips:** 19 was about 3× cleaner than the real night shots.
  - Tools: `tools/blend_v10.py` and `tools/measure_blend_v10.py`.
- **§6 "must not: grain" still holds for the reel.** No grain overlay and no texture layer are added. This is the camera's own noise level, put back on the two clips that lacked it, so they match the rest. It is the same kind of fix as the per-clip colour match.
- v10b raised 19's grain after v10 under-shot it. v10c removed a 0.5 px softening on 19 that made skin waxier.
- **Unchanged:** grade, text, timing, every other shot, audio.
- **Approved: v10c** (director, 2026-11-12, "Approve v10c"). It replaces v8b as the upload file. Review gate on Fable 5.1: PASS 8.5/10.

### v10d changelog (2026-11-13, director after the upload)
- **01 without the synthetic motion blur.** The v8 blur (minterpolate + tmix inside a mask) read on the phone as haze, bled into the driver's head and broke the match with 02–03. 01 is back on the stabilised camera footage, with the same framing, timing and grade. Nothing else changed.
- The other v8 item, 12 and 19 at 50 % (Timewarp), stays.
