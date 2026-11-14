# Retro — written by the editor at the end of the reel

| Field | Value |
|---|---|
| Reel | kolkata ("Kolkata, the city of culture, heritage and surprises"), pilot |
| Reel type | hybrid (the song's spoken guide intro cut like a VO, then the sung part as a montage), playbook cinematic-montage |
| Arch version | 0.9.0 throughout |
| Rounds to approval | 2026-11-04 → 11-08. Round 0/1 brief → 2 looks → 3 song re-brief → 4 story → 5 re-brief ("Kolkata", the guide) → 5b → 6 (lyrics, name cut) → 6b/6c (tram) → 6d (v6c notes) → 7 (look, Durga, Kumartuli; cut approved on v7b) → 8 (title, cover, Durga; package approved on v8c). 16 review-gate runs: 9 FAIL, 7 PASS (v1b, v2b, v3b_M3, v6_3, v7b, v8b, v8c) |
| Final runtime | 76.20 s, 26 shots (13 own, 13 free stock = 51 % of the runtime), 25 fps, 1080×1920 inside a 4:5 window; Fuji Eterna 250D → 3510 at 30 %; −14.0 LUFS. AI spend $0.64 (an AI tram, not used) |

## What worked (keep doing)
- **Offline previews before Premiere** (`preview_edl.py`, plus the reel-local `fx_prerender.py` for stabilising, slow motion and ramps). The director judged rounds 5–6d on phone previews; Premiere was built only for v1–v3 and once the cut was settled (v6 → v8c).
- **Shots chosen by what each line means** (`analysis/lyrics_meaning.md`, round 6). Story failed three rounds when shots were picked by place and energy; it held once every line had one shot that shows it.
- **Candidate sheets through the reel's own frame** for every replacement: bus, tram, Kumartuli, Durga, covers. The director picked from sheets in one message each time (rounds 6d, 7, 8).
- **The review gate on a different model** caught what I missed:
  - the ghat "bathers" clip was a timelapse with people strobing past;
  - the planned dissolve was missing;
  - the Durga framing cut the diyas;
  - the look sank the tram interior's night detail;
  - the flower seller repeated every 4th frame;
  - the title sat on the cartridge's printed label.
- **Verifying by render, not by the tool's reply.** The look went in at 100 % while the read-back said 30 %; only the stills against `looks.json` showed it. Once fixed, Premiere matched `look_preview.py` within 0.003. Previewing looks on stills is trustworthy.
- **After Effects Timewarp for slow motion and Warp in Premiere for shake.** It filled a 2.04 s slot from a 1.82 s sharp stretch (C076) without blur frames, and brought the walkway shake from 2.10 to 0.81 px.
- **A research subagent for footage inventory.** 25 Durga and pandal candidates from five reels' notes in 10 min, each checked on a sheet.
- **Duplicate before every change** (v6 → v7 → v8). Every round has a rollback sequence.

## Friction (from the friction log, ranked by time lost)
| # | Phase | What happened | Workaround | Time lost |
|---|---|---|---|---|
| 1 | Rounds 2–4 | Story failed three times ("the frames didn't follow a story"). The line table was VO-only, and the gate had no story check | Line table by lyric meaning, `tools/story_edl.py` | ~5 h (2 builds + reviews) |
| 2 | Round 3 | No song-research step; two builds on songs that were then rejected | Reel-local research method, `tools/song_fit.py`, `audition_edl.py` | ~3 h |
| 3 | Rounds 2, 5, 6b–7 | No stock search tool (empty Pexels key); every search in Chrome, 15–40 min | Chrome, `__NEXT_DATA__`, candidate sheets | ~2.5 h |
| 4 | Round 8 | Cover and title after the package was approved: the director's own title and Indo-western type, a new Durga; no font library, no cover step | `tools/make_title_v7.py`, OFL fonts in `assets/fonts/`, full-frame covers | ~2 h (incl. 2 review runs) |
| 5 | Phase 1 / Round 3 | Landscape phone clips all tagged −90°; 4 orientation mistakes found later; the 80 %-width rule can't hold | Both-rotation sheets, then an upright best-moment sheet; the 4:5 window | ~1.5 h |
| 6 | Round 5b | The preview couldn't show stabilisation, slow motion, ramps or whips; v5 was judged "no cinematic effect" | `tools/fx_prerender.py`, `make_leak.py` | ~1.5 h |
| 7 | Rounds 7–8 | Single-shot and title changes on a built sequence: a rebuild would wipe the hand fixes and the look | `tools/swap_v7.py`, `_es_title_v8.jsx` | ~1.5 h |
| 8 | Rounds 5–6 | I misread "cut out [the name] and use it as 'ami apnader guide'" as "use the guide intro"; the name stayed two rounds | Name cut in v6; restate ambiguous notes as actions | ~1 h |
| 9 | Rounds 6d, 7 | Clips asked for by memory ("the bus depot video", "dancing during bhashan", "better Durga frames") had no catalogue | Grepped five reels' notes, survey sheets, a subagent | ~1 h |
| 10 | Rounds 5b–7 | `shake_report.py` crashes on rotation-tagged files; phase correlation reads big subjects and bamboo grids as shake | Upright proxies; judged by eye on frame strips | ~45 min |
| 11 | Round 6c | $0.64 on an AI tram before checking stock photos (Unsplash had ~200) | A real photo with a slow push | ~40 min, $0.64 |
| 12 | Round 7 | The flower seller's "60 fps" stock repeats every 4th frame (it's 45 fps); `mpdecimate` missed the repeats | Repeats dropped by measured index → 45 fps file | ~30 min (and 3 rounds unseen) |
| 13 | Rounds 7–8 | `applyLumetriPreset` added a second Lumetri before the old one; dissolves came back shorter without warning; in-points landed 1 frame early | Pick the Lumetri by Look ≠ 0; read back everything | ~45 min |
| 14 | Phase 4 | The soft-bloom route (After Effects glow per shot) would have taken 13 round trips | A V2 Screen-mode highlight copy in Premiere | ~30 min |

## Change the studio (each one becomes a CR)
| # | Change | File / section | CR id |
|---|---|---|---|
| 1 | Landscape phone footage in 9:16 (orientation, the 4:5 window, the width rule) | CLAUDE.md §3, skill Phase 1, `analyze_footage.py`, `look_preview.py` | CR-20261104-kolkata-landscape-footage-9x16 |
| 2 | Soft bloom built in Premiere | effects-playbook §A, reality doc | CR-20261105-kolkata-premiere-soft-bloom |
| 3 | Song research step (and convert rips to WAV on intake) | skill Phase 0–1, new script | CR-20261106-kolkata-song-research |
| 4 | Report on the film-emulation-prompts skill's first use | `film-emulation-prompts`, `colour_report.py` fps bug | CR-20261107-kolkata-film-emulation-first-use |
| 5 | Lyric → shot skill (sung-line meanings, mixed-language transcription) | new skill | CR-20261107-kolkata-lyric-shot-skill |
| 6 | Line table and story check for montages | skill Phase 2.3, reviewer | CR-20261107-kolkata-montage-line-table |
| 7 | Effects in the offline preview | `preview_edl.py` | CR-20261107-kolkata-preview-fx |
| 8 | Footage catalogue; `shake_report` fixes; AE Pixel Motion ramps; in-point read-back | new script, `shake_report.py`, `ae_roundtrip.py`, reality doc | CR-20261108-kolkata-footage-catalogue |
| 9 | Look presets: find the look's Lumetri by Look ≠ 0; Eterna 3510 and linear intensity verified | effects-playbook §A3, reality doc | CR-20261108-kolkata-look-preset-second-lumetri |
| 10 | Title copy and type sheet in Round 2; a title tool; a font library (with Bengali shaping); a Phase 8 cover step; IG grid 3:4 | skill Round 2 / Phase 8, `instagram-strategy.md`, `assets/fonts/`, new script | CR-20261108-kolkata-cover-title-type |
| 11 | Stock search script (video and photos); repeated-frame check on intake; photos before AI | new script, `ingest_report.py` / `conform_clip.py`, `motion-and-ai.md` §3 | CR-20261108-kolkata-stock-intake |
| 12 | Late-round edit helper (swap a shot or still, keep keys, re-make transitions); pregate blur dips that ignore overlays; pregate scope against the last reviewed export | new script, `frame_scan.py`, `pregate.py` | CR-20261108-kolkata-late-round-edits |

## Director's notes pattern
What the director asked for in more than one round. These are likely candidates for new defaults.
- **Every shot must show its line.** Rounds 2, 4 and 6 ("try and understand the lyric and determine the shots"). → For any reel with words, a line table by meaning is the default, montage or not.
- **Stability.** Rounds 5b and 6d named handheld shots ("the bridge walk", "the lanes where the Ganga is visible"). → Stabilise every handheld moving shot by default and measure it before sending.
- **Specific clips from memory.** "the bus depot video", "people dancing during bhashan", "better Durga Puja frames". → A shared footage catalogue (CR #8).
- **Their own words on screen and the cover**, in type with character. The round-8 title and "Indo-western fonts". → Ask for the title copy and type in Round 2 (CR #10).
- **Plain cuts.** Round 6: "the transition sound and effects I do not like", so no whips, flashes or leaks; one dissolve. Matches the profile's "natural, never processed".
- **Free stock is fine** where their footage can't tell the story ("use free video from online"), but the strongest images they wanted were their own (the Pujo Durgas).
- **Pujo balance.** "Too many pooja shots" in round 5b, then a stronger Durga at the "passion" peak in round 8: few Pujo shots, but the best ones, at the emotional peak.
- **Look.** Camera-true until the cut was right, then a gentle film look (Eterna at 30 %) picked from a sheet of the reel's own frames.

## Tool reality check
Premiere MCP tools that failed, behaved unexpectedly or needed a different name than the docs say.
- `execute_extendscript` always returns "undefined"; results come back through `_es_out.txt` (Rule 2). An empty or missing `$.evalFile` target fails silently. Check the file exists and is non-empty.
- `app.project.applyLumetriPreset()` on a clip that already has a Lumetri **adds a second Lumetri before it**. The `Look` slot reads 1 after any preset. Find the look by Look ≠ 0 (CR #9).
- QE `addTransition(..., "00;00;00;10")` makes a **shorter, one-sided** transition when the clip has no media past its out-point, and reports nothing (C076: 5–6 frames).
- `setInPoint` + `overwriteClip` landed 1 frame early on 2 of 26 video clips and on 1 audio clip. Read back and correct with `trackItem.inPoint` (CR #8, item 5).
- `stabilize_clip` (warp) works and analyses by itself: `AnalysisStatusCounter` 104 = running, 408 = done; the property name carries the auto-scale, e.g. "Auto-scale (103.1%)". Changing smoothness after analysis doesn't re-solve.
- `export_frame` fails with `Illegal Parameter type` when the folder doesn't exist, as well as with `format: "png"`.
- `duplicate_sequence` copies effects and keys; the copy has to be opened (`openSequence`) before QE edits.
- Effects can't be removed by script. A layer's existing Lumetri was neutralised (vignette 0) rather than removed.
- After Effects round-trip: `ae_roundtrip.py` handles the camera's −90° rotation flag (an upright trim first) and Timewarp Pixel Motion cleanly. `time_remap` has no Pixel Motion (CR #8, item 4).
