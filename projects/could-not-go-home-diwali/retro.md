# Retro — written by the editor at the end of the reel

| Field | Value |
|---|---|
| Reel | could-not-go-home-diwali ("Maa, is baar ghar nahi aa paaunga": a letter home from the people who worked on Diwali night in Bengaluru), pilot |
| Reel type | music-montage with letter lines on screen (Hinglish only from v6; Hinglish + English before), playbook cinematic-montage with overrides (a picture window, 4:3 then 16:9; one worker per line) |
| Arch version | 0.9.1 at start; the studio moved to v0.10.2 during the build (the gate rule from this reel's CR) and was at v0.10.3 at approval |
| Rounds to approval | 2026-11-09 → 11-11. Checkpoint 1: p1 → p1b → p1c → v1b → v1c → v2 → v2b → v2c → v2d → v3 (approved "Build, reference look"). Checkpoint 2 in Premiere: v3b → v3c → v3d/e/f (picture lock v3f) → v4 → v4b → v4c → v4d → v4e (approved) → v4f (last shot swapped after approval, gate FAIL on its grade) → v4g (gate PASS) → story QC → v5 (FAIL: crown, 15) → v5b (PASS) → v6 (Hinglish only, Avenir, 16:9; FAIL) → v6b (PASS) → v6c (PASS) → the director asked what happened to the story-QC replacements → v7 (03 → C047, 12 → a diya lit at home; PASS 7.5) → v7b (03's exposure; PASS) → v8 (slow motion on 12 and 19, motion blur outside the auto on 01, 33.92 s on the beat grid; PASS 8) → v8b (19's face from Veo's own frames; PASS 8.5) → v9 zoom-blur experiment (rejected: "does not look natural at all") → **v8b and the package approved 2026-11-12** → after approval: the cover redesigned (4 options in the feed's style) and 12 + 19 blended into the director's footage, v10 → v10b → v10c (PASS 8.5) → **v10c approved 2026-11-12**; cover: B1 (the car washer) → "not festive enough" → C2 (the reel's own cracker photo, Didot white + gold) → a Pexels board of 8 → **D5 (a young man with a sparkler, Pexels 19467413) approved 2026-11-12** → set up in Instagram via iPhone Mirroring, music "Maa" (the director asked for an Indian song picked for reach), scheduled Fri 13 Nov 19:00 IST → after the upload the director rejected 01's synthetic blur on the phone → v10d (01 on the real footage; review FAIL on a false "line-start blur", then PASS on re-check) → **v10d approved 2026-11-13** → **posted** (the director, 2026-11-14; which file went out wasn't stated). 32 review-gate runs: 13 FAIL, 18 PASS, 1 discarded (ran on the editor's model) (+ 1 blind story QC) |
| Final runtime | 33.92 s: 17 shots + end card, 14 the director's (Apple Cinematic, depth baked), 3 Pexels stock (Maa's hands; a diya lit at home, 50 % slow motion; the last shot, a photo animated with AI, 50 % slow motion; both carry the director's own handheld path and grain from v10c), 25 fps, 1080×1920 with the picture in a 16:9 window (the whole camera frame; 4:3 until v5b); roti-match look at Lumetri Intensity 45. Audio: Instagram library song at upload, "Maa" (Taare Zameen Par, Shankar Mahadevan), picked at posting instead of the planned "Telephones" (Vacations); the cut is on the reference's 152 BPM guide, not on "Maa". AI spend for the reel: $0.52 (one AI-animated shot, label ON) |

## What worked (keep doing)
- **Baking Apple Cinematic depth** (`tools/cine_bake`, now `scripts/cine_bake.py`). The director's f/2 look only exists in Apple's framework; with it, every shot carries the depth he shot, per shot f-number when needed (f/4 on the jewellery strands that flickered, f/1.0 on the paan maker).
- **Asking with two boards before building an insert** (own topic footage + topic stock). Two insert rounds missed by guessing; boards landed it in one message each time (marigold hands, Maa's hands, the last shot ×2).
- **Warp Stabilizer solved over only the frames played** (± 2 handles). Crops fell from up to 120 % to 105–113 % and every shot got as steady or steadier (01: 6.6 → 1.7 px). The director's "don't crop too much" was this.
- **Text on the picture in the director's other reel's type** (Kolkata: Amita / Eczar caps / Tiro Bangla). The reel's look stopped reading as "a caption bar under a video"; one generator (`tools/make_type_v4d.py`) with per-line corner and width overrides fixed every overlap the reviewer found.
- **The review gate on a different model** (Fable vs this Opus editor) caught:
  - the vendor shot running into the camera tilt;
  - a jump cut;
  - the end card in Instagram's band;
  - lines on the tongs, the cook's board and a head;
  - 03's defocus, and 15's cut-off head.
- **Cloning the sequence for every version** (v3b … v4f): every round had a rollback, and single-shot changes never touched the approved rest (render_diff proved it each time).
- **Extending on the beat grid:** each slowed shot grew by exactly one bar, and the guide got one matching bar on a downbeat (bar 4 inserted, bar 11 repeated). Every later cut stayed within ±1 frame of a bar line, and the end card still lands on the music's tail.
- **AE Timewarp for slow motion, with the reviewer checking the in-betweens at 2×.** It caught what Timewarp does to sparks crossing a face. The fix (the head region from Veo's own frames, frame-mixed; Timewarp elsewhere) passed at 8.5/10.
- **Showing a reference-driven effect on the real footage before building a round** (v9): the zoom blur cost one preview, not a review loop.
- **Blending inserts by measurement, not by eye** (v10): the real shots' camera wander, fine shake and grain were measured in the window first, then the stock and AI shots were given the director's own handheld path and grain to land inside that range. Same picture, same timing; one render per fix, and the numbers told us when 19's grain under-shot.
- **Judging a cover in the feed** (v10): a mock grid of the five earlier covers next to each option made the miss of the first cover obvious and the redesign one round.
- **The bad-footage ladder held:** the last shot came from a free photo with a push, not an AI shot. Stock photos were searched before AI was offered.
- **Disproving a reviewer finding by track-mute renders** (v10d): the gate's "focus-in blur at every line start" was gone with V5 (text) muted, and flat with the type masked. The reviewer re-measured and withdrew it; no picture change was made for a false finding.
- **Posting through iPhone Mirroring and stopping before Schedule** (2026-11-12): music, cover, caption, location, AI label, quality and the schedule were all set on the phone; the director kept the last tap.

## Friction (from the friction log, ranked by time lost)
| # | Phase | What happened | Workaround | Time lost |
|---|---|---|---|---|
| 1 | Checkpoint 1 (p1 → v2d) | Nine preview rounds: slow motion on hands, rack pulls nobody asked for, a step-print misread as slow motion for three rounds, inserts from the wrong world (stock from elsewhere, then the wrong topic), "home" read as Kolkata | Boards before building; step-print as the reference's slow-down; no unasked effects | ~6 h |
| 2 | Checkpoint 2 (v3b) | A step-print on a handheld shot jumped 11 times; I marked it designed and four review loops passed it; the director's first words were "glitchy" | Removed the step-print on 01, stabilised; the gate rule (v0.10.2) | ~2 h |
| 3 | Phase 3 | Warp Stabilizer by script: half the clips never analysed, Method changes kept the old solve, No Motion past max scale renders black | One clip at a time, settings before analysis, wait for status 408 | ~1 h |
| 4 | v3c → v3d | Every Warp solved over a longer range than played → 111–120 % crops; found only after "don't crop too much" | Re-solve over the used frames | ~25 min + a round |
| 5 | Rounds 2, v3d, v4c, v4f | No stock search tool (no Pexels key): every search in Chrome via `__NEXT_DATA__`, boards built in the page | Chrome; boards as screenshots | ~1.5 h |
| 6 | Phase 1 / Round 2 | Cinematic depth invisible to ffmpeg and Premiere | `cine_bake.swift` | ~40 min (then 10 s per bake) |
| 7 | v3c | Loading a custom `.cube` needs the Look menu: the build stopped on a locked Mac and a timed-out screen-control prompt | The director unlocked; full-screen control | ~30 min |
| 8 | v4 → v4e | Text on the picture: five overlaps across four loops (head, tongs, board, hand, IG band) | Per-line corner/width/offset overrides | ~1 h |
| 9 | Round 1 | Length asked before the audio route was checked; "IG library song" turned out to be 20.8 s "Original audio" | Routes offered; final audio from the library | ~20 min + a re-plan |
| 10 | Phase 8 (v4f) | No free video of "a middle-aged man with a cracker"; `conform_clip --push` can't push inside a window; no photo span type; no cover tool; PNG grabs of Cinematic clips sideways | Premiere push on a crop, `freeze` span, `tools/make_cover_v4f.py` | ~1 h |
| 11 | v3c | `frame_scan` measured the whole frame, so a caption fade read as a blur dip in a sharp shot | Typed around it | ~10 min |
| 12 | v6c → v7 | After the story QC, 2 of the 5 misfits stayed in (03 not ticked, 12 "keep"), and none of my checkpoint messages since said those shots still didn't carry their lines. The director had to ask "what happened to the shots you were supposed to replace?" | A status sheet, then both replaced in v7 | a round (~1.5 h) |
| 13 | v8 | Slow motion and partial-frame blur have no complete studio route: no slow-mo span type, time_remap's ease, ffmpeg's colour-tag squeeze, an audio level lost on a clip swap, no masked blur op | Typed `freeze`, Timewarp, untagged conform, re-keyed gain, `tools/blur_01_v8.py` | ~70 min |
| 14 | v8 → v9 | A synthetic zoom blur after a reference image: radial streaks on a slow auto with a defocused street read as fake | Kept v8b's real-motion blur; a shooting note for next time | ~40 min |
| 15 | v7, v8b, v10d | render_diff missed changes (spans a frame short; a face-only change and v10d's 01 swap reported as "no picture change") | Measured by hand and told the reviewer | ~15 min |
| 16 | v10 | After approval the director found the stock diya and the AI cracker shot "a little fake": no route measures or matches an insert's camera feel and grain; then a grain amount solved on the source missed after Lumetri Sharpen −30 (0.20 instead of 0.48) | `tools/measure_blend_v10.py` + `tools/blend_v10.py`; a second render for 19 | ~60 min |
| 17 | v10 | The approved cover was rejected twice: first designed as a reel frame in the reel's type, not the feed's pattern; then the feed-style B1 (a daytime car wash) wasn't festive. No cover tool, no feed check, and no "does it say the occasion?" check | Read the five earlier covers by hand; `tools/cover_v10.py` / `_v10b` / `_v10c` with feed mocks; a Pexels board | ~60 min |
| 18 | v10 | The review gate ran on the editor's own model (the agent file pins no `model:`); the reviewer flagged it itself | Re-ran on Fable | ~15 min |
| 20 | after the upload (v10d) | 01's synthetic motion blur (v8: minterpolate + tmix in a traced mask) passed two gates and the director's approval, then read on the phone as "weird and blurry, not straight-line", haloed into the driver's face and no longer matched 02–03 | Removed it (v10d, 01 on the real stabilised footage) | ~40 min + a re-upload on the day |
| 21 | v10d | The review gate's first pass FAILED on a "focus-in blur" at every line start: its whole-window Laplacian sharpness read the text fading in | A dump, a source check and track-mute renders; the reviewer re-measured → PASS | ~35 min |
| 22 | posting | Instagram can't replace a scheduled reel's video; re-opening iPhone Mirroring asked for the Mac login (the director's), Finder access for AirDrop was declined; the music was changed at posting, so the cut isn't timed to the song that went out. The reel posted before the swap | The director handled it | ~20 min |
| 19 | v10 | ExtendScript failed with a bare "CEP evalScript() failed" from an object key named `new` (ES3 reserved); `node --check` passes it | Renamed the key | ~10 min |

## Change the studio (each one becomes a CR)
| # | Change | File / section | CR id |
|---|---|---|---|
| 1 | Check the audio's Instagram page (length, library vs original) before asking the length | SKILL.md Phase 0/1 | CR-20261109-could-not-go-home-diwali-audio-route-first |
| 2 | Bake Apple Cinematic depth; flag `cinematic` at ingest | ingest + `cine_bake.py` | CR-20261109-could-not-go-home-diwali-cinematic-depth (done v0.9.2) |
| 3 | Round 2 sheets: framing (incl. the 4:3 window) and type options | effects-playbook §B, a sheet tool | CR-20261109-could-not-go-home-diwali-round2-sheets |
| 4 | A designed span can't hide a jump; the gate reads every step-print strip | review-gate.md, pregate | CR-20261110-could-not-go-home-diwali-gate-missed-glitch (done v0.10.2) |
| 5 | Lumetri Creative Intensity isn't a linear mix: calibrate by render | effects-playbook §A3 | CR-20261110-could-not-go-home-diwali-look-intensity |
| 6 | Warp Stabilizer by script: the working recipe | premiere-mcp-reality.md | CR-20261110-could-not-go-home-diwali-warp-by-script |
| 7 | Solve Warp over only the frames played | premiere-mcp-reality.md, build scripts | CR-20261111-could-not-go-home-diwali-warp-used-range |
| 8 | frame_scan inside the window | frame_scan.py | CR-20261111-could-not-go-home-diwali-scan-window |
| 9 | `ig-quiet` shouldn't FAIL a deliberately silent upload | verify_render.py | CR-20261111-could-not-go-home-diwali-ig-silent |
| 10 | render_diff must catch text-only changes; strip stamps one frame early | render_diff.py, pregate strips | CR-20261111-could-not-go-home-diwali-render-diff-text |
| 11 | Photo shot in a windowed reel, a `photo` span type, and a cover tool | conform_clip.py, pregate.py, a new make_cover.py | CR-20261111-could-not-go-home-diwali-photo-shot-and-cover |
| 12 | Checkpoint 1 lessons: teardown motion bursts and step-print sections, frame_scan one-frame snaps, a per-shot time/move plan in the brief, the insert and motif rule, GPS at ingest | teardown.py, frame_scan.py, brief template, cinematic-montage, ingest_report.py | CR-20261111-could-not-go-home-diwali-checkpoint1-lessons |
| 13 | First use of film-emulation-prompts (image-to-video from a stock photo) | film-emulation-prompts, gen_video.py, motion-and-ai.md | CR-20261111-could-not-go-home-diwali-film-emulation-first-use |
| 14 | Slow-mo span type, time_remap linear ease, a masked region-blur op, ffmpeg colour tags, keeping audio levels on a swap | pregate.py, ae_roundtrip.py, a new region_motion_blur.py, the ffmpeg skill, reality doc | CR-20261112-could-not-go-home-diwali-v8-slowmo-and-blur |
| 15 | A blend tool for stock and AI inserts (the reel's handheld path + grain, solved after the grade), a pregate check of insert grain/shake against the real shots, the ES3 reserved-word note, and the reviewer's `model:` pinned | a new `scripts/blend_insert.py`, motion-and-ai.md §3, pregate.py, reality doc, `.claude/agents/reel-reviewer.md`, review-gate.md | CR-20261112-could-not-go-home-diwali-stock-ai-blend |
| 8+ | Measure sharpness with the type masked out (the gate's false "line-start blur", v10d) | frame_scan.py, the reviewer's measuring | more evidence in CR-20261111-could-not-go-home-diwali-scan-window |
| 14+ | No synthetic motion blur from minterpolate/tmix: it makes haze and halos; judge any partial-frame effect against its neighbours at phone size | ae_roundtrip / region blur op, review-gate.md | more evidence in CR-20261112-could-not-go-home-diwali-v8-slowmo-and-blur |
| 16 | Posting after a schedule: Instagram can't swap a scheduled reel's video; the director watches the IG preview on the phone before tapping Schedule; music changed at posting gets a beat check; Mirroring and AirDrop need the director at the Mac | ig-posting-reality.md, cinematic-reel Phase 8 | CR-20261114-could-not-go-home-diwali-posting-after-schedule |
| 11+ | The cover tool reads the feed (earlier reels' `deliver/cover.jpg`), offers its type families and always renders a feed mock | the proposed make_cover.py | more evidence in CR-20261111-could-not-go-home-diwali-photo-shot-and-cover |

## Director's notes pattern
What the director asked for in more than one round. These are likely candidates for new defaults.
- **"Don't crop too much / the background should be there"** (v3c, v3d): keep the frame wide; stabilise over the used range; push ≤ 5 %.
- **"Glitchy / jumping"** (v3b, v3c, v3f): any step-print, jitter or stabiliser float is noticed on first watch.
- **"Like the reference"** for text placement (v3f) and **"like Kolkata"** for the type (v4c): the director's own earlier reels are the type reference.
- **Own people, own topic** for inserts (v2b–v2d), stock only for a different world (home, Maa's hands), and then **a person who means something** for the last shot (boy → "a middle-aged man bursting a cracker").
- **No effects the director didn't ask for** (p1, p1b): slow motion, rack pulls. But when the director does ask (v8: slow motion, motion blur), go all the way, then show it.
- **Story integrity is tracked to closure:** "What happened to the shots that you were supposed to replace?" Every QC finding the director didn't pick stays listed in each checkpoint message until it's replaced or explicitly kept.
- **Language and type are the director's voice:** "Hinglish only, no translation", then a font picked from a sheet (Avenir Next).
- **"Is it not a 16:9 … I meant horizontal":** show the whole camera frame. The 4:3 window had read as "1:1".
- **Stock and AI inserts must look shot by the same hand** (v10): "the hand is not shaking … the pan looks too good to be true". A clean, steady insert next to handheld night footage reads as fake, even when its colour matches.
- **The cover belongs to the feed, not the reel** (v10): "fit in my Instagram feed based on the previous post". The earlier covers set the subject, the title position and the type. **And it must say the occasion at a glance** ("does not look festive enough"): a flame or a sparkler, not just a strong face. The director picked a stock photo over their own frames for it, and the white + gold Didot over the DIN caps.
- **Effects are judged on the phone, against their neighbours** (after the upload): a blur that passed two gates and an approval was rejected on the phone because it didn't match the next auto shots and smeared the face. A synthetic effect has to read as camera-made at phone size, next to the shots around it.
- **Music is picked for reach at posting** (2026-11-12): "something Indian", "based on analytics and probability of a hit". Settle the song before the cut is timed, or time the cut to the song that will go out.
- **Reference images for an effect mean a look, not a technique:** show it on the real footage first. A post effect that the footage can't support ("does not look natural at all") gets dropped.

## Tool reality check
Premiere MCP tools that failed, behaved unexpectedly or needed a different name than the docs say.
- `execute_extendscript` returns `"undefined"`; every result went through `analysis/es/_es_*.txt` (reality doc Rule 2). `$.sleep` over ~20 s timed the bridge out once.
- QE `addVideoEffect("Lumetri Color")` + property indices (19 Exposure, 15 Tint) worked every time; `color_correct` was never used.
- Warp Stabilizer: property 31 = status (408 done), 3 = Result, 4 = Smoothness, 5 = Method, 11 = max scale; changing Method after analysis keeps the old solve.
- `sequence.clone()` names the copy "<name> Copy"; renaming it and opening it first is needed before QE reaches it.
- `exportAsMediaDirect` with the Match Source ProRes 422 preset: reliable, ~1–2 min per 31 s.
- A still image on V1 takes in/out and Scale/Position keys like a clip (v4f).
- `TrackItem.move(Time)` exists on 26.5 and moves a clip by an offset, keeping its in-point (v8). Every move was read back.
- A long `exportAsMediaDirect` inside `execute_extendscript` can outlast the bridge ("MCP Bridge is not running"); the script still finished. Check its `_es_*.txt` before re-running (v8b).
- AE Timewarp (Pixel Motion, 50 %) synthesises **every** output frame, not just the in-betweens: even frames differ from the nearest source frame by ~10/255 (v8b).
- ffmpeg 7: output colour tags on an untagged source convert its levels (4–253 → 14–241). Tag the input or nothing (v8).
- ExtendScript is ES3: an unquoted object key that is a reserved word (`new`, `class`, `default`, `delete`, `in`) makes `$.evalFile` fail with only "ExtendScript execution failed via CEP evalScript()", no line and no output file (v10).
- Swapping a clip's media by remove + place + re-key + a fresh QE Lumetri, with the old values copied by property index and read back, kept keys and grade exact on both swaps (v10).
