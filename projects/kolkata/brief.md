# Brief — written by the editor, approved by the director

## ROUND 8 (2026-11-08): the title card, the "passion" Durga, the cover
- **Title (video and cover):** "Kolkata / the city of / CULTURE, HERITAGE AND SURPRISES" (the director's words), Indo-western type picked by the director: **Amita** for "Kolkata", Tiro Bangla Italic, Eczar caps; cream, soft shadow. Same place and timing as the old title (7.76–10.56 s, over the record).
- **0:27.5 "… passion" (shot 9):** the director asked for a better Durga Puja frame → **Oct 15 C076**, a sculpted gold Durga in profile (Warp Stabilizer). The dissolve into the verse is 5 frames, ending on the cut.
- **Cover:** the same gold Durga with the title (the director's pick).

## ROUND 7 (2026-11-08): Fuji Eterna look at 30 %, a pandal Durga for "passion", real Kumartuli
Director's Checkpoint 2 answers on v6_3:
- **Look:** "Add a film look" → picked **Fuji Eterna 250D → Fuji 3510 at 30 %** from `analysis/looks_v6/looks_sheet.png` (the most saturated and warm of the four; the colours pop on saris, balloons, the blue bookstall). It's on the V3 adjustment layer (built-in preset, by script), with no extra moves, exactly as previewed. Verified by render: Premiere matches the 30 % preview within 0.003 on luma, saturation and warmth (CR-20261108-kolkata-look-preset-second-lumetri). This replaces "camera-true" for this reel; per-clip correction is unchanged.
- **0:27.5 "… passion" (shot 9):** "a single dhaki … looking at the river bank. That does not match" and "let the first dhaki be there, for the second shot … a shot that showcases passion from the pandals" → **Oct 17 C168**: a giant Durga face rising from a bed of lit diyas under violet light in a bamboo grid, the camera gliding past her eyes (camera 1.4–3.1 s, 30 → 25 fps by interpretation, Scale 56 → 60). Picked from the director's own Pujo pandal shots (`analysis/round7_passion_pool.jpg`, `analysis/round7_pandal_candidates.md`). Shot 8 (the dhakis) stays.
- **0:50 Kumartuli (shot 18):** "The footage you've used is good. Can we not find actual Kumartuli footage?" → the director picked **Pexels 33742628** (Niladri Saha, free): an artisan shaping the eye of an unbaked clay goddess face (camera 2.1–3.9 s, 29.92 → 25 fps, Scale 50 → 53). The director's own footage has no Kumartuli. Pool: `analysis/round7_kumartuli_pool.jpg`, licences in `raw/SOURCES.md` "Round 7".
- **Build:** `Reel_kolkata_v7` (duplicate of v6, shots 9 and 18 swapped by `tools/swap_v7.py`; everything else is v6_3). Shot map `analysis/edl_v7.json`.
- **Review gate v7 changes (v7b):** shot 9 framed wider and raised (Scale 50 → 53, y 830) so the crown and the diya flames stay in; the tram interior (C030) gets Shadows +10, Blacks +1 so the look doesn't sink its night detail; the flower seller's stock repeats every 4th frame, so it now plays a de-duplicated 45 fps copy (0.56×, smooth). Accepted: its blown red cockscombs (in the source).

## ROUND 6D (2026-11-08): steadier walks, a sharp tram interior, the bhashan dancers, a moving bus
v6d changes five shots of v6c. Everything else is v6c. Options sheet: `analysis/round6d_options.jpg`.
- **0:16 "city of surprises":** the stock hand-pulled rickshaw is replaced by our own **Dashami dancers** (Oct21 C035): women in lal-paar saris dancing on the ghat road at the bhashan, smoke and balloons under the banyan, at real speed.
  - **Tried and rejected:** the street dance inside C047 (25–27 s), 7.6 px jitter even when locked, with blur and a passer-by crossing.
  - **Alternatives:** the tram line (C023) and the bus depot (C020), both steady.
- **0:27 "… passion" accent:** C035 moved to "surprises", so this is now **the big dhak at the ghat** (Oct21 C029) with a slow push, cut on the accent. Pujo is still 4 of 26 shots: dancers, dhakis, dhak, Kumartuli.
- **0:18 walk into the Howrah walkway (C082):** stronger stabilisation (smooth σ 40, zoom 1.08), and the camera window moved to 2.0 s, past a lurch. It measures 1.23 px in the reel against 2.10 in v6c. The build uses Warp Stabilizer.
- **0:22 river promenade walk (C089):** now stabilised (σ 30, level horizon), 1.03 px in the reel against 1.65. It was unstabilised.
- **0:58 "walk and see, the old streets":** the standing-tram photo is replaced by **a moving Kolkata bus**. Pexels 39654702 (Trishik Bose, free) shows a garlanded private bus driving straight at the camera, front end clear. It's interpreted 30 → 25 fps (0.833×) with a slow push 125 → 130.
- **1:09 inside the tram at night (C030):** the camera lost focus at 4.8–6.6 s. The shot now uses 0.40–4.52 s, sharp throughout.
- **Review-gate changes in the build (2026-11-08):**
  - **0:29.5:** the planned 10-frame dissolve into the verse.
  - **0:34.5 "light everywhere":** the Setu sunset holds 2 beats longer, then **people on the ghat at sunset with the Setu behind** (Pexels 36819326, Souhityo Das, Warp-stabilised). This replaces the morning ghat bathers, a timelapse with passers-by blinking across the lens.
  - **The dancers:** cropped tighter (Scale 62.5, x 405) to lose a bystander.
  - **The title:** visible from 7.8 s.
  - **The tram bell:** starts on the tram cut with a strike, at −14 dB, and ends at 73.3 s.
- **Still no AI shot**, so the reel needs no Instagram AI label.
- **The build (approved 2026-11-08, "Yes, build v6d"): `Reel_kolkata_v6`.**
  - Camera-true colour: only the approved cast fixes. No look, grain or bloom yet; the director picks a look later, on stills.
  - Slow motion: After Effects Timewarp at camera size. Stabilisation: Warp Stabilizer on the walkway, the promenade and the boatmen.
  - The 4:5 window, the "Kolkata" title settle, a 6-frame fade-in and a 20-frame fade to black.
  - Audio: the edited song, the needle drop, the tram bell.
  - The `_mix` is the posted file.

## ROUND 6C (2026-11-07): the tram is a real stock photo
- **Shot 21 = a real photo** of a WBTC tram on the line, front end clear: Unsplash pc_sZ1DLdGU by Subhashis Das, Unsplash License. It's a 4:5 crop with a slow push-in (Scale 100 → 106 over 4.08 s).
- **Your note:** "the tram shot in applicable use stock image".
- **The AI tram from round 6B** (final $0.40, drafts $0.24) stays only as an alternative. With the photo, the reel has **no AI shot**, so it needs no Instagram AI label.

## ROUND 6B (2026-11-07): one AI-generated tram shot
- **Shot 21 (chorus "walk and see", reel 58.52–62.60, 4.08 s): AI-generated.** It shows a Kolkata tram running on the line toward the camera, with a clear front end. It replaces stock 2843866, where the tram passes side-on behind an SUV.
- **Why AI:** no free stock has a running Kolkata tram front-on. I searched:
  - Pexels: all 267 Kolkata clips, plus 175 tram clips;
  - Pixabay;
  - Wikimedia Commons.

  Your footage has only the retired trams parked under trees (C025–C027).
- **Your decision (2026-11-07):** you chose the AI tram over shooting it, the parked C027 or keeping the stock. The $0.12 draft is approved. The final (≈ $0.40) waits until you've seen the draft.
- **Rules:**
  - it isn't proof; it sets the scene between real shots (C105 bookseller before, C101 taxi on the tram lines after);
  - one AI shot in the reel;
  - the light matches C101 (soft overcast daylight);
  - no first frame, so no real people are animated;
  - turn on **Instagram's AI info label** at posting.
- **Prompt (light block per film-emulation-prompts):** An old Kolkata tram drives straight toward the camera along rails set into an old city street in Kolkata, India, and slows as it comes close, its front end filling the middle of the frame. The tram is a single old car with a flat front: white lower body, a blue band around the windows, a cream-yellow panel above the windscreen with a route number board, one round headlight low in the centre, and a single trolley pole on the roof touching the overhead wire. Two steel rails run in grooves down the middle of the grey asphalt; overhead tram wires hang from iron poles; old three-storey buildings with green wooden shutters and small balconies, and large green trees, line both sides; a yellow Ambassador taxi is parked at the left kerb. The street is quiet, no people near the camera. Filmed on a phone held vertically, 26 mm lens, 4K, 9:16, locked off, low beside the rails, no camera move. Soft daylight under light cloud, a hazy pale sky, soft shadows. Natural colour and white balance for that light, normal contrast, dark shadows that keep detail, bright lights that keep detail, clean image, no text.
- **Negative:** people close to the camera, faces, crowd, modern low-floor tram, articulated tram, European tram, double-decker, bus, colour grade, teal and orange, film grain, noise, halation, glow, lens flare, letterbox, black bars, vignette, faded blacks, oversaturated, text, watermark, logos

## ROUND 6 (2026-11-07): lyric-led, the guide's name cut, no transition effects
- **Why:** on v5b the director asked to cut the guide's name ("ami … apnader guide"), replace the Coffee House and "surprises" frames, drop the Metro girl and the transition sound and effects, and choose shots from what the lyrics mean.
- **Song:** `music/kolkata_v6_edit.wav`. The name is cut (song 25.72–28.273 s, 5 beats, 30 ms crossfade); the window runs from song 7.25 to 86.00, so the reel is **76.20 s**. Instagram's library audio can't carry the cut: post with the baked audio.
- **Story by line:** `analysis/lyrics_meaning.md` (meanings only, never lyrics). One shot per line; "I am your guide, but I call myself an explorer" is one walking POV; "walk and see" is one walk.
- **Effects:** slow motion and stabilisation on our own shots, the dhakis ramp, slow pushes, real slow motion on the 60 fps stock. **No transition effects or transition SFX** (director); one dissolve into the verse; fades. SFX: needle drop, tram bell.
- **Subjects:** Pujo 3 of 26 (dhakis, dancers, Kumartuli). No unexplained people.
- **EDL:** `analysis/edl_v6.json` from `tools/guide_edl_v6.py`.

## ROUND 5B (2026-11-07): stabilise, effects on our own shots, no swooping shots
- **Why:** the director on preview v5: "the final shot I don't like; a few of my shots need stabilisation and cinematic effect; the swooping shots don't make it good; the shots of 'city of surprises' can be better; we are on the right track". Story, song window and line timings stay as round 5.
- **Out:** the scooter POV (explorer) and the façade ride (both swooping, 20–56 px jitter); the diya final.
- **In:** "surprises" is the giant LED petal arches over a packed street, whipped in; "explorer" is a young woman in a saree on a Kolkata Metro platform looking around as a train streaks past, in real slow motion (free stock, Pexels 35040390); "come walk and see" is a hand-pulled rickshaw running down the tram tracks (free stock, Pexels 32665218); the taxi on the tram lines replaces the façade ride; the final is our Academy of Fine Arts at night (bookends "a city of culture"), slowed and faded.
- **Fewer Pujo shots** (director, mid-round: "too many pooja shots"): 4 of 28 (LED arches, dhakis, dancers, Kumartuli). The story is the city; Pujo is one of its faces.
- **Effects on our own footage** (25 fps, so slow motion is interpolated: AE Timewarp in the build, `minterpolate` in the preview):
  - stabilised: Coffee House, walkway, dhakis, boatmen, tram street;
  - slow motion: Coffee House 70 %, dancers 65 %, boatmen 70 %, walk 60 %, chai 50 %, final 75 %;
  - speed ramp: the dhakis go from real speed into 40 % on "passion", into the flash;
  - whip pan Victoria → surprises; light leaks into "city of love" and the verse; pushes on the holds.
- **Dropped from round 5:** the explorer speed ramp (its shot is gone) and the step-print (the façade ride is gone).
- **EDL:** `analysis/edl_v5b.json` from `tools/guide_edl_v5b.py`; table in `project.md` Round 5b.

## ROUND 5 RE-BRIEF (2026-11-07): "Your guide to Kolkata", supersedes rounds 3–4 for song, story, shots and effects
- **Why:** the director on the v4 story preview: the shots aren't good enough and the selection is bad; follow the reference's opening and story; use free stock where our footage can't replicate it; and add the cinematic effects the other reels had (slow motion and the rest). Then they added the song **"Kolkata"** (*Praktan*, 2016; Anupam Roy, Shreya Ghoshal) and asked to use its spoken guide intro ("Urja Mukherjee … your guide") and make a 60–90 s story.
- **Reel type:** `hybrid`. The guide's spoken intro is cut like a VO (§4b: cut on clause onsets, the picture shows the line); the sung part like a montage (§4c: cuts on bar downbeats the band plays).
- **Song:** `music/kolkata.wav` from 7.25 s (its first note at 9.80 s lands at reel 2.55, as the record settles) to 86.00 s = **78.76 s**. One continuous stretch of the song, so it can be added in Instagram from the song's start. **Open:** does Instagram's "Kolkata" (*Praktan*) include the spoken intro? If not, the guide's voice exists only in the baked `_mix`.
- **Story:** the reference's arc, told by the guide. The record starts the song → title → the guide's city: culture (Coffee House), heritage (Victoria), surprises (a pandal-palace on a lake), "your guide" (into the Howrah walkway), "an explorer" (the scooter ride), city of love (the river lamps), city of passion (dhakis, dancers) → verse: the city in light (Setu sunset, the ghat under Howrah, the river, the flower market, Kumartuli) → chorus, "come walk and see, think it over": the old streets, wall writing, a bookseller, chai, a tram → will you come with me (a tram at night) → Howrah lit at night, fade.
- **Footage:** 13 own shots + 16 free stock (Pexels / Pixabay; `raw/SOURCES.md`, `analysis/stock_round5.md`). The director asked for stock "wherever the reference's story can't be replicated" (overrides the profile's "stock only as a layer or bridge" for this reel). Own footage kept where it is the strongest frame for its line.
- **Effects (overrides round 1's "no swishes / no flashes", which came from the reference):**
  - real slow motion on four 60 fps stock shots (0.42×) and a gentle 0.83× on the 30 fps stock;
  - a 250 % → 100 % speed ramp on "explorer" with a whoosh;
  - a whip (zoom-blur) into "surprises" with a whoosh;
  - a 3-frame flash with a sub-hit on the accent between the dhakis and the dancers;
  - a 10-frame dissolve from the guide's voice into the verse;
  - a step-print on the façade ride (traffic passing close);
  - slow pushes on the holds; fade in 6 f, fade to black 20 f;
  - sound: needle drop and crackle at the start, a Kolkata tram bell on the tram, −14 to −20 dB.
- **Kept from earlier rounds:** the 4:5 window, the marigold title (now **"Kolkata"**, the song's and the guide's word), primaries on flagged casts. **Grade: open.** The director asked for a different grade; the preview is camera colour, and look options come with the build.
- **EDL:** `analysis/edl_v5_guide.json` from `tools/guide_edl.py`; line table in `project.md` Round 5.

## ROUND 4 RE-BRIEF (2026-11-07): story first (superseded by round 5)
- **Why:** the director on v3b_M3: "the footage still does not match the song or the story, no story is coming out properly". The story was a column label; the shots were slotted by priority and energy, nine of 16 were empty places, and M3 ran Pujo night → morning → night.
- **Story (director's pick): "Home for Pujo".** Someone comes home and leaves again: the dhak calls → arriving across the Howrah walkway → the river → "Calcutta" → the ride in (scooter POV) → the people you missed → evening → Pujo → Dashami, the goodbye → leaving at Howrah, blue hour. Howrah bookends the reel (arrive / leave).
- **Song:** unchanged, the v3b_M3 window (Mayabee from 164.36 s, 47.5 s, IG start ≈ 2:40).
- **Rule for this reel:** a line table first (`project.md` Round 4), one story line per shot, each shot chosen for what its frame shows; every cut on a beat the band plays (onset ≥ 4× median), never on the tracker's unplayed downbeats. Treatment (window, look, title, audio) unchanged from round 3.
- **EDL:** `analysis/edl_v4_story.json` from `tools/story_edl.py`.

## ROUND 3 RE-BRIEF (2026-11-07): superseded by round 4 for shot order
- **Why:** the director rejected "Amar Shohor" ("does not match the storyline and the footage"). A song-research round followed (`research/SONG_RESEARCH_METHOD.md`, `research/AUDITION.md`). Then:
  - "skip Shantiniketan, use the Mayabee but different parts of the song … the opening should be strong; the reference had a strong and justified opening";
  - "the footage choice needs to be optimised … best footage of the lot; upside down or ill-oriented clips fixed and used";
  - **"try m3 and m1 both"**: two cuts are built and the director picks one.
- **Story:** "a Bengali far from home", the city remembered: river morning → the roads → where we gathered → evening play → Pujo → night, the ache. Mood-only matching (pictures follow the feeling, not each lyric). Mayabee ("enchantress") is sung to someone not seen in months; here the city is that someone.
- **Song:** **"Mayabee", Blue Touch** (Dhaka). In Instagram's audio library (18K reels; checked in the app 2026-11-07). Guide copy: `music/mayabee.wav` (from the director's `audio/` copy; the music-video audio, which has 4.4 s of silence before the first note). ≈ 120 BPM by the reviewers' measure (the beat tracker reads 123), played as half-time; the cuts follow the detected beats.
- **Two cuts (same pool, same treatment; the opening and the song part differ):**

  | | Song part (guide copy) | IG start | Runtime · shots | Opening (why the music starts) | Title "Calcutta" |
  |---|---|---|---|---|---|
  | **v3c_M1** "From the first note" | 4.32 → 48.36 s (the first note's attack on frame 1) | **0:00** | 44.04 s · 13 | **A mood open, not an action:** a roadside chai stall, the chai-wallah setting out clay cups behind a big steaming pot, the city waking. C028 has no stirring or pouring. The song's first note on frame 1 (3-frame fade-in) | Rising in the steam on a real cut-in to the pot (105 %), on the first strong beat (4.02 s) |
  | **v3b_M3** "The second half" | 164.36 → 211.86 s (the hit on frame 1) | ≈ 2:40.0 | 47.52 s · 16 | **An action open:** Pujo, the dhakis drumming on the song's hit at frame 1, then the lal-paar dancers; then two men on a drifting boat through the song's breath | On the Setu, on the band's full downbeat after the breath (11.24 s) |

  Shot lists and song moments: `research/MAYABEE_ITERATIONS.md` (v3 plan); the built v3b EDLs `analysis/edl_v3b_M1.json` and `edl_v3b_M3.json` are authoritative. Every big hit carries a cut; detected beats are nudged 0.05 s earlier.
- **Footage (pool v3, `analysis/pool_v3/`):** the best of all 101 clips, ranked by eye upright in the 4:5 window.
  - **Orientation fixes, used:** C109 (pandal mirrored in a lake; was "unusable", only sideways), C018 (an adult and a child in red), C025 (old tram).
  - **New:** C105 (bookstall seller), C089 (sun through the riverside lamps); M3 also has C072 (ghat steps) and Oct21:C047 (dhakis).
  - **Kept:** C061 (two men on a drifting country boat), C064, C100, C028, C111, Oct21:C035, C033, and the stock blue-hour Howrah (M3).
- **Pace:** every cut on a beat of the song (bar downbeats preferred, `tools/audition_edl.py`). Shot length follows the song's energy: quiet ≈ 4–5 s, full ≈ 2.5–3 s, a slower open and a longer last shot. Hard cuts only; no transitions.
- **Treatment (unchanged from v2b):**
  - Look "film stack": camera colour, plus soft bloom (V2 highlight copy, Screen 30 %), vignette (V3), grain 5 % Overlay (V4; **off on night shots**: M1's Pujo and Academy; M3's Pujo cold open, blue hour and Academy).
  - 4:5 window (V6). Fade in 3 f (v3b; the opening hit lands on frame 1); fade out 20 f. Title: marigold Big Caslon, red shadow, 0.4 s focus-pull settle (V5).
  - **Primaries (camera-true):** casts fixed only where analysis flagged them:
    - C061 temp +10 / tint +5, C072 +8 / +5;
    - C018 tint +4, Oct21:C035 tint +6;
    - C025 tint +5 / exposure +0.4 (M3 v3b; +0.6 in M1 v3c, against the bright Setu before it), C105 tint +4 / +0.35, Oct21:C047 exposure +0.3;
    - C111 exposure counter-keys (auto-exposure ramp).
  - **Framing (v3b):**
    - C109 comes from the ferry ride's later window (src 48.9 s, 64 → 66 %, y 900): the full reflection, a clean top.
    - C028's close is a cut-in at 105 → 108 % (pos 580, 720), pot and steam only; its width is about 27 % of the camera's, on purpose.
    - C028 wide: position keyed with the push so the head isn't cropped.
    - C064 starts at src 2.6. M3 (v3b) uses 85 → 87 % at pos 740, 960. M1 (v3c) uses 90 → 92 % at y 800, with x keyed 740 → 900 with the camera's pan: the lamp arm out, the pylon in.
    - Oct21:C047 is at 54 % (pos 570, 900).
    - C025 starts at src 1.1 and C105 at 1.6, both past the camera's auto-exposure ramp.
    - C033 starts at src 2.9.
  - C111's counter-keys hold the camera's head level.
- **Audio:** song on A3 at −2.5 dB, fading to silence over the last 1.2 s; camera sound muted.
  - `_mix` (guide baked, loudnorm −14 LUFS): archive and review only.
  - `_IG` (silent): for upload, with Mayabee added in Instagram from the IG start above.
- **Must-not:** no swishes or whooshes, no text other than the title, no grain on night shots, no clip upside down or sideways.

## ROUND 2 RE-BRIEF (2026-11-05): superseded by round 3 where they differ
- **Why:** the director's notes on v1b: the music didn't fit the footage, the frames didn't follow a story, there's more usable footage, research the song, add a couple of the best Pujo shots.
- **Song:** **"Amar Shohor", Chandrabindoo** (`analysis/song_research.md`, recommended and picked). Instagram library audio, confirmed in IG by the director. Guide copy: `audio/Amar Shawhor.mp3` (director's) → `audio/amar_shohor_guide.wav`.
- **Section:** **1:14.72 → 1:59.28** of the track (44.56 s): the end of verse 1 into chorus 1, with the four title refrains (~1:43–1:52), ending at a clean section end. **IG picker start: 1:14.7** (check by ear that IG's version lines up).
- **Grid:** 152 BPM, 1.58 s bars (`analysis/song_v2/audio_summary.md`). Every cut is on a bar downbeat:
  - verse: 2-bar shots (day on the river);
  - chorus: 1-bar shots on the streets, then 2-bar holds at dusk and night.
- **Story:** day → dusk → night (director's choice), ~45 s (director's choice).
- **Pujo:** **Oct21:C035**, women in lal-paar saris dancing at a ghat on Dashami (also in the goddess final). It's the only Pujo shot, placed in the night block before the ending.
- **Title "Calcutta"** now sits in the open sky over Vidyasagar Setu (shot 2), not over a person (review v1 #7).
- **Opener:** the stock vinyl is dropped (it belonged to the old-song idea). The reel opens on the river.
- **Keeps from v1:** the 4:5 window, the film-stack look (camera colour + soft bloom + vignette −0.5 + grain 5 %, none at night), hard cuts, no swishes, the black-PNG fades, the review-v1 fixes (de-duplicated flowers, AE-ramp in-points, C111 exposure keys).
- **Runtime 44.56 s**, 17 shots, average 2.62 s (verse 3.1 s, chorus 1.5–3.1 s).
- **Stock (Pexels, director-picked):** Howrah from the river, flowers, Victoria (src 13.5 s, past the edge lamp), Howrah at blue hour.
- **Approved at Checkpoint 1b** on 2026-11-05 ("Approve, build v2"). The Premiere build `Reel_kolkata_v2` (a clone of v1b):
  - A1 primaries only on C061 (temp +10, tint +5) and Oct21:C035 (tint +6, green cast); every other clip camera-true;
  - C111 exposure counter-keys;
  - bloom copies on V2 (Screen 30 %); vignette −0.5 on V3;
  - grain 5 % from 0.24 s to 35.40 s (off on blue hour + night: shots 15–17);
  - title 3.08–6.16 s (focus-pull settle);
  - black-PNG fades (6 f in, 22 f out);
  - song from 74.72 s (verified by cross-correlation);
  - `_mix` limited to −1.4 dBTP; `_IG` silent for upload (IG start 1:14.7).

| # | Time (s) | Clip | src (s) | rate | Shows |
|---|---|---|---|---|---|
| 1 | 0.00–3.08 | A001_10251448_C061 | 4.0 | 1 | two boatmen rowing a country boat on the Hooghly |
| 2 | 3.08–6.16 | A001_10251452_C064 | 1.0 | 1 | Vidyasagar Setu over the river, open sky; "Calcutta" in the sky |
| 3 | 6.16–9.20 | 17164810_2160_3840_60fps | 5.0 | 0.4167 | Howrah Bridge from the river |
| 4 | 9.20–12.32 | A001_10251529_C083 | 11.0 | 1 | people walking the Howrah Bridge walkway |
| 5 | 12.32–13.84 | A001_10251623_C096 | 3.0 | 1 | red heritage facade rushing past from the scooter |
| 6 | 13.84–15.32 | A001_10251619_C093 | 1.0 | 1 | scooter POV down an open road |
| 7 | 15.32–18.44 | A001_10251635_C100 | 1.0 | 1 | yellow Ambassador on tram lines |
| 8 | 18.44–21.52 | A001_10251641_C106 | 1.12 | 1 | College Street bookseller |
| 9 | 21.52–24.60 | A001_10251657_C111 | 0.0 | 1 | Indian Coffee House hall (exposure counter-keyed in Premiere) |
| 10 | 24.60–26.16 | flowers_dedup_25 | 5.4 | 1 | Mallick Ghat flower seller |
| 11 | 26.16–27.72 | A001_10251753_C117 | 3.4 | 1 | Uttam Kumar on the film-strip mural, "UTTAM KUMAR" lettering |
| 12 | 27.72–29.24 | A001_10311639_C027 | 1.5 | 1 | an old Kolkata tram under the trees (1st refrain) |
| 13 | 29.24–32.28 | A001_10311604_C007 | 1.52 | 1 | boys playing football on the Maidan, pink sky (2nd refrain) |
| 14 | 32.28–35.40 | 16301337_2160_3840_30fps | 13.5 | 0.8333 | Victoria Memorial at dusk (3rd refrain) |
| 15 | 35.40–38.44 | 16387667_2160_3840_30fps | 2.0 | 0.8333 | Howrah Bridge at blue hour (4th refrain) |
| 16 | 38.44–41.56 | Oct21_A001_10211954_C035 | 0.2 | 1 | women in lal-paar saris dancing at a ghat on Dashami |
| 17 | 41.56–44.56 | A001_10311733_C033 | 3.4 | 1 | Academy of Fine Arts lit at night; fade to black |

---

> Claude writes this file after the interview and footage analysis. The director only answers questions, shares references, and approves. Don't fill it in by hand; ask Claude to change anything.

**Status:** approved at Checkpoint 1 on 2026-11-05 ("Approve, build it"); updated for the v1 Premiere build (changelog at the end)

## 1. The idea
- **Reel type:** `music-montage` (no speech; the song drives the timing, CLAUDE.md §4c)
- **Playbook:** `cinematic-montage`. **Overrides** (each the director's choice in Round 2):
  1. **One shot per bar for the whole reel** (13 shots, ~2.5 s each), on the reference's own cut times. The playbook says "never one shot per bar" (my-reel v1 read as mechanical). Here the director asked for "exactly the reference". The variation comes from the subjects and the day → dusk → night light, not the cut rate.
  2. **4:5 window** (1080×1350 centred at y = 910, black outside) for every shot, instead of full-bleed 9:16 with ≥ 80 % of the camera width. 57 of 84 usable clips were shot landscape; the window keeps 45 % of their width (CR-20261104-kolkata-landscape-footage-9x16).
  3. **Title type:** a marigold-yellow serif with a red offset shadow (from the reference), instead of the playbook's DIN Condensed in cream.
  4. **Stock as whole shots, including the opener** (5 of 13 shots, Pexels), instead of the profile's "stock as a layer or bridge only": the director asked for it on this reel.
  5. **No swishes / whooshes**: nothing moves fast enough to sell one, and the reference has none.
- **One-line concept:** a love letter to Kolkata, from the needle dropping on a record to the city lit at night, cut line by line to an old Hindi film song.
- **Story arc:** the record starts → morning on the river → the Howrah Bridge → books, coffee, flowers, taxi → dusk on the Maidan and the tram → landmarks at dusk and blue hour → the city at night, fade out.
- **Goal:** the viewer feels **nostalgia** and is inspired; Bengalis at home and abroad send it to someone who misses the city.
- **Audience:** Bengalis, home and abroad.
- **Target length:** **34.96 s** (874 frames at 25 fps). Set by the guide audio (34.97 s). A longer Instagram audio could allow more.

## 2. Hook (0–3 s)
- **Moment:** the stylus riding a spinning record (Pexels 6742732), with a slow push in. The song's crackly intro plays from it. The vocal enters at ~3.7 s, and the title lands on the first cut at 3.88 s.
- **Visual move:** push 62.5 → 66 % across the shot, fade in from black over 6 frames.
- **On-screen text:** none in 0–3.88 s; **"Calcutta"** from 3.88 s.
- The reference opens slow, and the playbook allows a slow open when the brief says so. Something moves from frame 1 (the spinning record + the push).

## 3. References → concrete parameters
| Reference | What we take from it | Measured (`analysis/teardown/TEARDOWN.md`) |
|---|---|---|
| `references/ref_north_kolkata.mp4` ("Frames of Calcutta", Fujifilm X-T3, DaVinci) | Pace and cut points, hard cuts, one title card, day → night, people at work + landmarks, fade out | 35.08 s, 13 shots, 20.5 cuts/min, avg 2.7 s, median 2.62 s, first cut 3.88 s, no flashes; luma 0.297, contrast 0.737, sat 0.298, warm R−B +0.076; −14.1 LUFS |

What we don't copy: its title wording ("Frames of Calcutta"), its title-over-a-record composition, its quote. Our title sits over a different shot (chai steam).

## 4. Treatment
### Pace
- 13 shots on the reference's cut times, snapped to 25 fps frames: 0.00 · 3.88 · 6.28 · 8.96 · 11.00 · 13.76 · 16.80 · 19.16 · 21.68 · 24.40 · 27.00 · 29.44 · 32.00 → 34.96. Shots run 2.04–3.88 s, median 2.60 s (reference 2.62).
- Hard cuts throughout; a 22-frame fade to black at the end. The three sung line onsets (~3.7, ~14.0, ~24.2 s) fall on cuts 1, 5 and 9 → the title, the Coffee House, the tram.
- The beat detector's downbeats sit 1.1–1.3 s before every reference cut (likely a half-bar phase error on a rubato song). We follow the reference's cuts, and **the director checks them by ear** on the preview.

### Camera and motion
- Slow digital pushes (+4–6 %, eased) only on steady holds (`analysis/motion.json`): S1, S2, S3, S6, S9, S10, S13.
- S5 (bookseller), S8 (taxi) and the stock shots carry their own movement, held as shot.
- **Slow motion only on 60 fps stock**, interpreted to 25 fps (0.42×, every frame once): S4 Howrah Bridge, S7 flowers. Our camera clips have no slow-mo headroom (all 25 fps).
- Conforms by interpretation: the 30 fps stock (S11, S12) plays at 0.833×, the 23.976 vinyl (S1) at 1.043×.
- **Stabilise** in Premiere only if the export shows shake: C061 and C111 are near-holds, C007 has a hold from 0.8 s.

### Colour
- **Primary correction (per clip):** camera-true, effects-playbook §A0.
  - C061 (river, 3750 K): cool + green cast → warm the temperature + add magenta.
  - C007 (Maidan, 5080 K): green cast → add magenta.
  - C106 / C111 (6050 K, warm light): keep the warmth the camera recorded.
  - Night C033: lift only until burn.
  - Stock: `conform_clip.py --match` against the neighbouring own shot. Retag the flowers clip (SD tags) and the Victoria clip (full range) to BT.709 TV range.
- **Shot matching:** adjacent shots within each light group: day S3–S8, dusk S9–S11, blue hour / night S12–S13.
- **Creative look: "film stack"** (the director's pick from `analysis/looks/effects_sheet.jpg`). No film-stock LUT:
  - **soft bloom / mist:** highlights glow softly. Built in Premiere: a highlight-only, blurred copy of each shot on V2 in Screen mode at 30 % (CR-20261105-kolkata-premiere-soft-bloom), tuned to the effects-sheet tile: luma +0.01–0.02, p98 +0.01–0.02;
  - **vignette:** Lumetri vignette on a V3 adjustment layer (one manual click to create it), tuned to darken the window's edges, not the bars;
  - **grain 5 %:** V4, Overlay, `assets/overlays/gemini_film_grain_16mm.mp4` looped. **Off on S12–S13** (blue hour / night phone footage, §A4).
- **Camera-check exceptions:** `camera_fidelity.py` can't yet handle rotation or the window (CR item 6). Until HQ fixes it, the camera check is judged by eye on its sheet, plus verify_render + frame_scan. The bloom lifts highlights by design: run with `--look`.
- **Framing exceptions:** every landscape clip shows 45 % of the camera width (4:5 window, override 2). In the vinyl (S1) the picture sits at the right edge so the stylus is in frame.

### Effects & transitions
- Hard cuts only; fade in (6 frames) at 0.00, fade to black (22 frames) at the end. No flashes, no light leaks, no whips, no shakes, no text-behind-subject.

### Type & graphics
- **Title "Calcutta"** 3.88–6.28 s: marigold-yellow (#F4B81C) Big Caslon serif with a red (#C41626) offset shadow and a soft dark halo, in the window's upper part over the chai stall, inside the safe zone. Animated in Premiere with a focus-pull settle over the first 10 frames (opacity 0 → 100, Scale 104 → 100, blur 30 → 0); it leaves on the cut at 6.28 s.
- No captions, no end card (the reference has none). The 4:5 window matte sits above the title on V5.

### Sound
- **Music:** "Jaane Woh Kaise Log The" (*Pyaasa*, 1957), the reference reel's audio. Cut to the stereo guide `audio/guide_ref_stereo.wav`. Deliverables: `_mix` (guide baked, archive only) and `_IG` (guide muted); the director adds the audio in Instagram with "Use audio" from 0:00 (CLAUDE.md §4c).
- Beat grid: `analysis/audio_summary.md` (95.7 BPM, 2.508 s bars).
- **SFX:** none planned. Natural sound muted (A1). Optional: a soft vinyl crackle under S1 at −20 dB, if the guide's own crackle isn't enough.

## 5. Clips
| # | Time | Clip | Role | Notes from the analysis |
|---|---|---|---|---|
| 1 | 0.00–3.88 | **Stock** Pexels 6742732 (Matthias Groeneveld) | opener | record player close-up, 3840×2160 23.976 → 25 (1.043×), src 2.0 s; picture at the right edge for the stylus |
| 2 | 3.88–6.28 | Oct31:C028 | title card | chai pot steaming at a stall, rotate −90, hold 0–7.1 s, src 0.5 s; jumps at 10.92 / 11.44 s are outside the window |
| 3 | 6.28–8.96 | Oct25:C061 | day, river | two boatmen rowing, rotate −90, hold 2.4–11.3 s, src 4.0 s; cool / green cast |
| 4 | 8.96–11.00 | **Stock** Pexels 40180894 (Ritesh Jha) | day, landmark | under Howrah Bridge from the river, 60 fps at 50 %, src 5.0 s |
| 5 | 11.00–13.76 | Oct25:C106 | day, people | College Street bookseller, rotate +90, hold 0–3.5 s, src 0.5 s |
| 6 | 13.76–16.80 | Oct25:C111 | day, institution | Indian Coffee House hall, rotate −90, hold 0–3.0 s (3.04 s used: the last 0.04 s is past the hold) |
| 7 | 16.80–19.16 | **Stock** Pexels 39276190 (Arijit Dey) | day, market | Mallick Ghat flower seller, 60 fps at 50 %, src 3.0 s; retag BT.709; highlights already blown in the source |
| 8 | 19.16–21.68 | Oct25:C100 | afternoon, icon | yellow Ambassador on tram lines, vertical, hold 0–5.9 s, src 1.0 s |
| 9 | 21.68–24.40 | Oct31:C007 | dusk, people | Maidan football, pink sky, rotate −90, hold 0.8–6.0 s, src 1.5 s |
| 10 | 24.40–27.00 | Oct31:C030 | dusk, icon | inside a tram, rotate −90, hold 0–7.3 s, src 1.0 s |
| 11 | 27.00–29.44 | **Stock** Pexels 38386435 (Soham Kundu) | dusk, landmark | Victoria Memorial at dusk, 30 → 25 (0.833×), src 3.0 s; full range → TV range |
| 12 | 29.44–32.00 | **Stock** Pexels 38584444 (Souhityo Das) | blue hour, landmark | Howrah Bridge above the traffic, 30 → 25 (0.833×), src 2.0 s |
| 13 | 32.00–34.96 | Oct31:C033 | night, ending | Academy of Fine Arts lit, crowd, rotate −90, hold 0–8.3 s, src 0.5 s, fade out |

Not used, still in the pool: Vidyasagar Setu (C064–C067), ghat steps (C071–C074), Howrah walkway POV (C081–C085), river sunset through railings (C086–C089), scooter rides (C092–C098), Dakshineswar (C108 / C110), Uttam Kumar mural (C115–C117), parked trams (C025–C027), St Paul's at dusk (C035 / C037), Eden floodlights (C012–C013, C090–C091).

Stock credits for the caption: Pexels: Matthias Groeneveld, Ritesh Jha, Arijit Dey, Soham Kundu, Souhityo Das.

## 6. Must-haves / must-NOT-haves
- Must: the reference's pace and cut points; day → dusk → night; the 4:5 window throughout; "Calcutta" title; the film-stack look.
- Must not: swishes; flashes or light leaks; grain on the night shots; the reference's own title wording or quote; the same person twice; synthetic bokeh or heavy processing (director profile).

## 7. Open questions
1. **The reference reel's Instagram link**, to check the audio page (library song or "Original audio", the creator; their OK if it's original audio). Required before posting, and best before the Premiere build.
2. Is the Instagram audio longer than 35 s? If yes, the reel could run longer (more shots from the unused pool).
3. A date line or a quote under the title? The director to supply one, or none (current plan: none).
4. The opener: the stock vinyl close-up is in v1. The alternatives are an AI-generated Kolkata gramophone shop (≈ $0.12 draft) or our own shot.

## Changelog
- 2026-11-05 · v1 Premiere build:
  - the 60 fps stock is interpreted to 25 fps (0.42× instead of the preview's 0.5×);
  - the soft bloom is built in Premiere (V2 copy, Screen 30 %) instead of After Effects glow;
  - the title animation is done in Premiere (focus-pull settle) instead of HyperFrames;
  - grain covers 0.24–29.44 s.
- 2026-11-07 · v3c_M1 (review v3b_M1): Academy cut back on the 40.04 hit (dancers the whole clip); Setu 90 %, y 800, x keyed with the pan; tram +0.6; C018 described as an adult and a child.
- 2026-11-07 · v3b (review gate v3): M1 opening described honestly as a mood open; song in-points on the attack (4.32 / 164.36 s); forced cut on M1's loudest hit; M3 title on the band downbeat; reframes and src_in moves per `project.md` Round 3 — Review gate.
- 2026-11-07 · Round 3 re-brief: song "Mayabee" (Blue Touch); two cuts v3_M1 (from the first note, chai opening) and v3_M3 (second half, Pujo cold open); pool v3 with orientation fixes (C109, C018, C025); casts fixed per clip; C109 reframed. Supersedes the round 2 song, shot table and pace.
- 2026-11-07 · round 4: story-first re-brief "Home for Pujo" (line table, played-beat cuts), on the director's story note.
