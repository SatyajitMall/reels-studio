# Retro — written by the editor at the end of the reel

| Field | Value |
|---|---|
| Reel | pujo-ki-asolei-sobar ("Pujo ki Asolei Sobar?", the men who work through Durga Puja nights; pilot) |
| Reel type | hybrid (an external Hindi VO + bed from the reference reel drives the cut; no speech in our footage; IG audio added at upload) |
| Arch version | 0.5.3 |
| Rounds to approval | Checkpoint 1 after 4 proposal passes (v1–v1d). Then 14 review rounds: depth / sepia (R1–R2) → cine look (R3) → stabilisation (R4) → skin (R5) → B&W alternate (R6–R7) → mains flicker (R8) → re-cut, 14 men + slow-mo (R9) → dark faces / speed ramp (R10) → "over-processed" → natural (R11) → second dhaki shot replaced (R12) → phone check: flicker + too dark (R13) → posting: designed cover; the reference's IG audio turned out to be song-only, so the director voiced it himself, matched to the reference (v18); then the creator gave permission and his voice was split from the song (demucs) and baked in, with the song re-added from IG's library (R14, final v19). IG package approved in R2. |
| Final runtime | 35.80 s (1075 frames @ 30). 13 shots in 12 VO-line slots, 14 different men, one dissolve. Final upload `renders/exports/pujo-ki-asolei-sobar_v19_IG.mp4` (creator's VO with permission, song removed and re-added in IG; v13 picture). v18 (director's own VO) kept as a fallback. The B&W alternate was last exported at v11. Upload kit: `deliver/`. |

## What worked (keep doing)
- **The blind review gate.** 9 loops (fable reviewer) across rounds 9–12. Every loop found real defects that my own numeric QA and `frame_scan` passed:
  - optical-flow smear on passers-by;
  - a 48 px same-take jump;
  - waxy slow-mo faces;
  - a warm → cool cast swing;
  - an over-red face.

  It also found the "brightness normalised on every shot" problem behind "over-processed".
- **Camera-original / current / proposed sheets** before a big change (`analysis/look_n1/compare.jpg`). The director decided the look in one answer after 10 rounds of incremental fixes.
- **Option sheets with stills** for choices (look, shot-3 replacements, dhaki speed clips): one answer per question, no back-and-forth.
- **An offline preview assembler** (`tools/preview_assemble.py`) that mirrors the Premiere timeline within 2–3 / 255. Premiere was held by another reel five times; review never stopped.
- **Baked, reproducible shot pipeline.** JSON EDL + focus files → render → skin → deflicker → trim → build → preview. Every round's change was a parameter edit plus a batch script, and every step was measured.
- **Path guard + IDs in every ExtendScript.** Imports never landed in another reel's project, even when Premiere switched projects mid-session.
- **Measuring before claiming:**
  - VO onsets to the frame (cuts within 0–20 ms of the word);
  - flicker by lock-in on the 3-frame cycle;
  - skin by person-gated median;
  - brightness against the camera original.
- **Full-pool contact sheets** (327 clips, 19 sheets) when the director asked for more people: 7 new men found in one pass.

## Friction (from the friction log, ranked by time lost)
| # | Phase | What happened | Workaround | Time lost |
|---|---|---|---|---|
| 1 | Colour, R1–R11 | Look churn: depth + sepia (rejected) → cine look matched to the reference → skin anchor → face / toe lifts → "over-processed, not natural" → natural-matched. Each fix was stacked on the last and passed its own metric. | Partial-strength "natural-matched" mode, brightness halfway to the original, person-gated skin, no clarity. Shown against the camera original. | ~5 rounds |
| 2 | Edit, R1 + R9 | Picture vs words: cuts placed in VO pauses (3 rounds), depiction not literal, then the same drummer 3× and tea seller 2× from my "one man per voice" reading. | Cut on measured onsets; one different man per line from a full-pool survey. | ~4 rounds |
| 3 | Effects, R1–R2, R9–R11 | Synthetic effects asked for and then rejected: depth-model bokeh (unconvincing on night iPhone footage); optical-flow slow-mo on 30 fps soft handheld (smear, ghosts, waxy faces). | Bokeh dropped; slow-mo only on calm shots (5, 10, 11, 12); the dhaki and the young balloon seller at real speed. | ~3 rounds |
| 4 | Premiere | Premiere shared with 2–3 other reels; our project was not the active one five times, and closing another reel's project was blocked. | Path guard, offline previews, builds deferred; finally `open_project` to switch. | hours of waiting, 4 deferred builds |
| 5 | Finishing, R2 + R4 | No scriptable stabiliser; my first one (translation only) missed roll and sway. | Own similarity stabiliser (patch phase correlation + RANSAC), 2 passes, per-shot lock / smooth. | 2 rounds |
| 6 | Finishing, R8 + R13 | Mains flicker (1/60 s under 50 Hz lamps → a 10 Hz cycle at 30 fps) reached round 8 unmeasured; ffmpeg `deflicker` is global only. My per-tile fix left 2–6 % on LED / bulb shots, which the director saw on the phone (R13). Root cause: estimating in linear light under-corrects mid-tones where steady ambient and flickering lamp light mix. Also an LED rolling-shutter band crawled across one shot (C213). | Display-domain, fine-grid deflicker (`--display --grid 160x90`): residual ≤ 0.4 % on every shot; per-frame band inpaint (`tools/band_remove.py`). | 2 rounds |
| 7 | Phase 1 | ElevenLabs key rejected (401), no local Whisper → no word timings → pause-based cuts (fed #2). | Subtitle-band + speech-band onset detection (`tools/vo_timing.py`). | part of #2 |
| 9 | Posting, R14 | The plan to add the reference VO in Instagram at upload failed at the last step. The reference's IG audio is a library song; the creator's voice is not in it. | The director recorded his own VO (browser recorder + record-along guide); phrases placed on cuts; PSOLA pitch / formant + half-octave EQ match to the reference; subtitles re-worded offline. 5 voice iterations (v14–v18): a vocoder match sounded synthetic, a jagged EQ sounded nasal. | 1 long round |
| 8 | QA | `frame_scan` passed a half-second optical-flow smear and a 48 px jump; `replace_clip` reported failure on a correct replace. | Blind review + property readback. | ~1 round |

## Change the studio (each one becomes a CR)
| # | Change | File / section | CR id |
|---|---|---|---|
| 1 | Survey a footage pool across all shoot folders → pick sheets → copy picks; storyboard tool with fps flags | skill Phase 0–1, `link_footage.sh`, new `pool_index` / `pool_sheets` / `storyboard` | CR-20261019-pujo-ki-asolei-sobar-pool-survey |
| 2 | External VO as the soundtrack (reel type / rules), cut on clause onsets, local word timing (`hyperframes transcribe`) | ARCHITECTURE §6, skill Phase 1–2, CLAUDE.md §4 | CR-20261019-pujo-ki-asolei-sobar-external-vo-audio |
| 3 | Measure the reference's grade in Phase 1; person-gated skin protection in trims | skill Phase 1, playbook §A | CR-20261020-pujo-ki-asolei-sobar-reference-grade-match |
| 4 | Depth / lens blur as an option with its limits; similarity stabiliser; denoise / clarity stages; 3-frame QA per shot | playbook §A–B, finishing tools | CR-20261020-pujo-ki-asolei-sobar-lens-bokeh |
| 5 | Director profile: words drive pictures, literal depiction, vary the people, natural over processed, copies not links, IG audio at upload, shoot 60 fps / 1/100 s | `studio/director-profile.md` | CR-20261021-pujo-ki-asolei-sobar-director-profile |
| 6 | Premiere ops: one project at a time / lock file, path-guard helper, reality-doc items (gaps, floors, stills, bridge drop, `$.global`, `replace_clip`) | harness, `premiere-mcp-reality.md` | CR-20261021-pujo-ki-asolei-sobar-premiere-ops |
| 7 | VFR / jump / smear / translation checks in `analyze_footage` and `frame_scan`; synthesised slow-mo rules | scripts, playbook "Slow-mo B-roll" | CR-20261021-pujo-ki-asolei-sobar-vfr-jump-qa |
| 8 | Mains-flicker scan + per-tile deflicker; interview note on shutter vs mains | scripts, skill Phase 4, interview | CR-20261023-pujo-ki-asolei-sobar-mains-flicker |
| 9 | `vs_original` sheet at every Checkpoint 2; corrections at partial strength by default; cap on stacked corrections | colour QA, `reel-reviewer.md`, playbook §A2 | CR-20261023-pujo-ki-asolei-sobar-correction-stacking |
| 10 | Person-gated skin consistency check in `colour_report.py`; face-only skin correction | `colour_report.py`, playbook §A2 | CR-20261024-pujo-ki-asolei-sobar-skin-qa |

+1s added to other reels' CRs: CR-20261018-my-reel-premiere-shared-between-sessions (×5), CR-20261018-puja-night-2-extendscript-notes (still-image overwrite), CR-20261018-puja-night-2-premiere-session-setup (bridge drop).

Round 13 also added follow-ups to the mains-flicker CR (display-domain estimation, a ≤ 1.5 % residual target) and the correction-stacking CR (phone brightness floor, phone check before Checkpoint 2).

## Director's notes pattern
What the director asked for in more than one round. These are likely candidates for new defaults.
- **Pictures change on the words, and show what the words say.** Asked in 4 rounds (cut placement, depiction, "match the footage with the words").
- **Different people.** "Same set of people a few many times" (R9); "two successive shots of the drummer" (R12).
- **Natural over processed.** Bokeh rejected (R2), sepia rejected (R3), "over-processed, not natural" (R11). Approved: a light, warm, matched grade close to the camera.
- **Faces must read, and the reel must not be dark on a phone.** "A little dark", "very dark, not clear" (R10); "too dark" on the phone (R13, +½ stop chosen); skin "not on point" (R5).
- **Check the reference's IG audio page before planning to "use audio" at upload** (R14): a song label means the voice won't come with it.
- **Natural over processed, for voice too** (R14): the vocoder match was rejected; a light PSOLA + smooth EQ was approved.
- **Watch the final on a phone.** The R13 phone check caught flicker and darkness that every desktop check had passed.
- **Stability and clarity** (R2, R4): handheld shake is noticed immediately.
- **Slow motion for drama, but only where it holds up** (R9 asked, R10–R11 rejected where it smeared): "slow where needed".
- **Alternates on request** (B&W + gold, R6–R7), then dropped at the end ("no black and white needed").

## Tool reality check
Premiere MCP tools that failed, behaved unexpectedly or needed a different name than the docs say.
- **`replace_clip` (preserveEffects):** returns `success:false` ("motion scale not restored") although the replace is correct. Verify by readback.
- **`add_to_timeline_batch`:** non-frame times leave 1-frame gaps. Premiere also **floors** fractional source in-points (1.6333 s → frame 48, not 49): set in / out by ticks (`frames × 8467200000`).
- **`overwriteClip` with a still** uses the 5 s default and silently overwrites the clips behind it. Set the item's in / out first.
- **`exportAsMediaDirect`** can drop the MCP bridge (`bridge_unavailable`) although the export completes. `verify_premiere_connection`, then continue.
- **`$.global` values persist between `evalScript` calls.** Every caller must set every parameter (or null it), e.g. the A3 trim or fade.
- **`open_project`** on an already-open project makes it the active one. That is how to take Premiere back from another reel without closing its project.
- **Audio Level** via ExtendScript is linear with a +15 dB offset (`10^((dB − 15) / 20)`). Keyframes are in source time (`inPoint + offset`).
- **`duplicate_sequence`**, QE Cross Dissolve via `addTransition` and Motion scale keyframes all worked as documented.
