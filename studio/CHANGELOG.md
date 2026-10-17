# Studio Changelog

## 0.5.0 — 2026-10-17
**Review gate + watch**, from the "Claude edits every video" workflow (Nishant Chahar), adapted to this studio.
- **New `scripts/watch.py`:** samples any video at N fps into labelled contact sheets, one per shot (`--shots`) or per section, with the audio waveform under each sheet, plus `index.md` / `index.json`. Takes about 9 s for a 50 s reel.
- **New `scripts/frame_scan.py`:** checks every frame for blur or smear dips, frozen frames, flicker and black or white frames. Takes about 2 s. It catches what 2 fps sheets can't: on my-reel v8 it flagged C073's camera jerks (30.40 and 30.88 s) and C076's Timewarp smear (37.96 s) to within a few frames.
- **New `.claude/agents/reel-reviewer.md`:** an independent reviewer on a **different model** (Fable) that judges a render blind against the brief and the director profile, and returns a verdict plus a defect table.
- **New skill Phase 7b + `review-gate.md`:** every version goes through the gate before Checkpoint 2.
  - Step 0 keeps `brief.md` current.
  - At most 2 fix loops.
  - Every blocker and major is answered as fixed, intended or disagree.
- **Calibration on my-reel v8**, blind vs the pilot's frame-by-frame QA:
  - 5 of 8 failing shots caught fully, 2 partly, 1 missed (ray haze);
  - 12 extra real issues found;
  - the misses led to the frame scan and a haze check.
- **Fix: `ae_roundtrip.py` `frame_match` and the compare still now rotate the source like the job.** v0.4.1 falsely failed `rotate: 180` shots; v8 s06 and s09 now pass.
- `CLAUDE.md` tooling lines for watch and the review gate.

## 0.4.1 — 2026-10-17
After Effects fixes from my-reel v7 (pilot reports).
- **Fix: Timewarp retimed from the start of the source file, not the shot's in-point.**
  - With `layer.startTime = -in_s`, Timewarp sampled (t + in_s) × speed. On C076 (in 15.96 s, 60 %) the output showed source 9.6–11.7 s.
  - Every shot is now built as a source comp starting at the in-point, and all ops apply to that nested comp.
  - Verified: frame 0 = in-point on C076 and on the C077 ramp (in 7.6 s); duration 2.11 s ÷ 0.6 = 3.52 s.
  - My v0.4.0 check missed this: its stills didn't match, and I blamed the still's timing instead of the render.
- **Fix: a pre-trimmed source went black after its media ended** on slow-mo shots. The source comp outlasts the output, so it's fixed; verified, no black tail. Pre-trimming is no longer needed.
- **New `frame_match` check** in `ae_roundtrip.py`: output frame 0 vs the source around the in-point, accounting for 24→25 fps conforms. It warns loudly on a mismatch, and the result is logged.
- **Glow defaults** are now threshold 80 / radius 25 / intensity 0.25, after 70 / 0.5 clipped 21–54 % of pixels on night shots. The docs note that glow shots need exposure checks against their neighbours.
- **Docs:** v7 denoise results (−12…−29 % dark-area noise), the frame_match step, and pre-trimming no longer needed.

## 0.4.0 — 2026-10-17
**After Effects finishing** (CR-20261017-my-reel-after-effects-bridge).
- **New `scripts/ae_bridge.py`:**
  - runs ExtendScript in the director's running AE via osascript `DoScript` with a file loader, and returns JSON;
  - `verify` checks the connection, and `effects` checks effect match names.
- **New `scripts/ae_roundtrip.py`:** jobs JSON → one AE project per shot → `aerender` ProRes 422 → before/after still + log.
  - Ops: `denoise`, `timewarp`, `time_remap` (true eased speed ramps), `glow`, `grain`.
  - Safety: it never touches another open AE project.
- **Verified by render on my-reel footage:**
  - Remove Grain needs Viewing Mode 4; it gets studio defaults that keep texture;
  - Timewarp and the time-remap ramp are clean;
  - Glow is `ADBE Glo2`.
- **Rejected:** Warp Stabilizer by script. It never analyses and renders a "Click Analyze to begin." banner, so stabilising stays in Premiere.
- **New `.claude/skills/cinematic-reel/after-effects.md`** + skill **Phase 5b**, and a `CLAUDE.md` tooling line.
- **Fix:** `shake_report.py` / `colour_report.py` crashed on files where ffprobe lists the stream twice (found testing ProRes output).
- **Backlog:** kumoproductions AE MCP (dependency decision), Adobe's own AE MCP (beta-gated), paid plugins (Neat Video, Twixtor, RSMB, Deep Glow), aerender speed, a ProRes 422 HQ template.

## 0.3.2 — 2026-10-17
Montage craft from my-reel rounds 2–6 (CR-20261016-my-reel-montage-craft).
- **Brief (skill Phase 2, CLAUDE.md §4c):** music-montage briefs state an **energy arc** (default: slow open → build → full → breath → payoff → outro) and a **motion style**. Never one shot per bar throughout.
- **New scripts**, generalised from the pilot's and tested on v6 (numbers match the pilot's reports):
  - `selects_score.py`: best 1 s moments per clip, shoot-wide ranking;
  - `motion_holds.py`: static holds and pans per clip;
  - `shake_report.py`: per-shot jitter for before/after stabilisation;
  - `colour_report.py`: per-frame colour QA with montage targets and a gold-hue check.
- **Playbook:**
  - no shake or snap zoom on handheld footage (push/pull on holds instead);
  - Optical Flow slow-mo allowed at 25 fps on calm shots;
  - grain 10–15 % by default;
  - warm-look red-push warning;
  - music-montage words default to title + end card.
- **Skill Phase 5:** Warp Stabilizer on handheld moves by default (nest recipe for speed-changed or interpreted clips), then re-measure and scan for Warp banners.
- **Skill Phase 4:** colour QA on every frame before review.
- **Checkpoint 2:** the director watches full-screen with sound, and gets one "what would make it more cinematic?" question.

## 0.3.1 — 2026-10-16
The rest of the first pilot's feedback (`my-reel` retro + 5 CRs). Main lesson: **many Premiere MCP tools report success without doing the work.**
- **New `.claude/skills/cinematic-reel/premiere-mcp-reality.md`:** every broken or partly working tool on Premiere 26.5.2 / MCP 1.2.9, with the fallback the pilot verified. It covers import, delete, colour, adjustment layer, LUT, blend mode, transitions, volume, slip, razor, export presets, silent export and script results. CLAUDE.md §2 now requires **verify by render, never by the tool's reply**.
- **Conform by interpretation (CLAUDE.md §3):** outlier frame rates are fixed with `set_override_frame_rate` before placement, not with `speed_change`.
- **Colour (CLAUDE.md §2.5, playbook §A1/§A3/§A4):**
  - `color_correct` only for contrast / temperature / tint, plus a Lumetri script recipe for the rest;
  - the adjustment layer is one manual step for the director;
  - looks use built-in Lumetri presets (custom `.cube` files can't be loaded by script);
  - blend-mode enum documented;
  - V4 fades with the picture.
- **Transitions / sound / export:**
  - QE transition snippet and Dip-to-Black fades;
  - volume formula;
  - built-in `.epr` paths;
  - mandatory audio check after export;
  - new **`scripts/mix_from_edl.py`**, the fallback that rebuilds the mix and muxes it onto the picture.
- **Type:** new **`scripts/render_type_cards.py`** renders PNG word and end cards with a safe-zone guard and a system-font fallback. End cards must be checked over the real outro frame.
- **New `studio/director-profile.md`:** handle, type style and working preferences, read by every reel in Phase 0, so branding is asked once.
- **Speed ramp recipe** rewritten for how `speed_change` actually behaves.
- **Upstream:** 15 issues drafted in `studio/upstream/premiere-mcp-issues.md` (not filed).

## 0.3.0 — 2026-10-16
First pilot feedback applied. Both change requests are from `my-reel`.
- **CR-20261016-my-reel-beat-summary → `gemini_audio_and_beat_analyzer.py`:**
  - "4-Bar Downbeats" is renamed "Bar downbeats (every 4th beat)", and the bar length is shown;
  - the beat range is stated (the beatless intro and outro are now visible);
  - a new **Energy / sections** table labels intro, build, drop, breakdown and outro from per-bar loudness;
  - new **Candidate cuts** give the best 3 start/end pairs for 15/30/45/60 s, scored on energy, first hit ≤ 3 s, a clean ending and starting on a phrase;
  - the dialogue table only appears when clips are passed.

  Tested on Dum Durga: the sections match the pilot's hand-made map, and the 30 s candidates include its chosen 61.9 s start.
- **CR-20261016-my-reel-footage-overview → `analyze_footage.py`:**
  - new `overview_<n>.jpg`: labelled mid-frame thumbnails, 20 per sheet, built from frames already grabbed (no extra decoding);
  - new `--norm auto|talking-head|shoot`: by default, a shoot with median exposure < 0.30 is judged relative to its own median. On `my-reel` that's 19 darker and 7 brighter clips, instead of 70/77 "underexposed".
  - **Not done: auto upside-down detection.** On the pilot's 5 known upside-down clips, the top-vs-bottom brightness and detail heuristics were spread across the whole range, and the metadata of upside-down and upright clips is identical apart from timestamps. Upside-down clips are spotted on the overview sheets instead. That check found 3 more likely ones (C014, C015, C020).
- **Skill Phase 1:** look at the overview sheets first, then the candidates' contact sheets; use the energy/sections table and candidate cuts to pick the music section.

## 0.2.5 — 2026-10-16
- **Skill Phase 1: handle Premiere sample media.**
  - Premiere 2026's New Project screen imports 17 Adobe sample clips and a `Sequence 01` by default. This was found in `my-reel.prproj`.
  - The reel session now lists them and asks the director before removing the project references.
- **Bridge verified end to end:** `verify_premiere_connection` → connected (Premiere 26.5.2).

## 0.2.4 — 2026-10-16
- **`link_footage.sh`:**
  - new `references` role, which links into `projects/<reel>/references/`;
  - footage roles now skip reference folders (`*ref*rence*`, which also matches the director's "Refference" spelling), so a reference reel can't be linked in as footage.
- **`analyze_footage.py`: default `--scene-threshold` lowered from 0.3 to 0.15.**
  - On `my-reel`'s dark, beam-lit reference, 0.3 found 3 cuts (5.4 s average).
  - The count settles at 8 cuts from 0.15 down to 0.1 (2.4 s average, 1.6 s median), which matches the contact sheet.
- **Skill Phase 1:** cross-check the reference cut count against its contact sheet.

## 0.2.3 — 2026-10-16
- **Starter asset pack adopted (G1).** `scripts/gemini_generate_starter_pack.py` was reviewed and run. It generates:
  - 5 LUTs in `assets/luts/`;
  - 6 SFX in `assets/sfx/`;
  - a 16mm grain loop in `assets/overlays/`.

  The files are git-ignored and can be regenerated. `setup.sh` now generates them when no LUTs exist.
- **Fixes to the generator after testing on real `my-reel` frames:**
  - Teal & Orange turned pure black navy. The tint now fades in from black.
  - The "Log to Rec709" LUT was a contrast curve, not a real camera conversion. It's renamed `gemini_flat_contrast_boost.cube` so it can't be mistaken for the clip-level log LUT that CLAUDE.md §2.5 allows.
- **Playbook:**
  - §A3 maps each look to its LUT file, with notes from the test;
  - §A4 adds a stronger grain range (40–60 %), because 30 % is barely visible;
  - §F names each SFX file and notes they're placeholders.

## 0.2.2 — 2026-10-16
Found while preparing the first pilot (`my-reel`: 77 iPhone 17 / Blackmagic Cam clips, mostly 25 fps).
- **Rule: sequence frame rate matches the footage** (CLAUDE.md §3, skill Phase 3).
  - The most common frame rate in the footage wins.
  - Outlier clips are conformed with `speed_change`.
  - This replaces the old "30 fps default", which would have made 25 fps footage stutter.
- **New: `scripts/link_footage.sh <reel> <dir> [a-roll|b-roll]`.**
  - Symlinks footage that lives outside the studio into `raw/` and records it in `raw/SOURCES.md`.
  - Originals are never copied or moved.
  - Skips macOS `._*` files and camera `Proxy/` folders.
  - Safe to re-run.
- **Fix: `analyze_footage.py` skips `._*` metadata files** when scanning a folder.

## 0.2.1 — 2026-10-16
- **New: `scripts/check_tool_names.sh`.** It lists the Premiere MCP server's tools over stdio and fails if any tool name in `CLAUDE.md` or the cinematic-reel skill and playbook doesn't exist. Premiere doesn't need to be running. Result today: all 52 names are valid against server 1.2.9 (283 tools).
- **Gemini review triage.**
  - G4 (move graphics above the grade): rejected by the director.
  - G5 (wrong tool names): rejected; the check above shows the claim is false.
- Guard hook installed (`.claude/settings.json`).

## 0.2.0 — 2026-10-15
- **HQ / reel-session split.**
  - Each reel is its own sub-project, edited in its own session.
  - One HQ session owns the architecture (`studio/ARCHITECTURE.md`).
- **Guard hook.** `.claude/hooks/guard_architecture.py` blocks edits to HQ-owned files from reel sessions. The hook is staged in `studio/harness/settings.json`. It becomes active once installed into `.claude/settings.json`.
- **Change requests.** Reel sessions file them in `studio/change-requests/`, and HQ triages them with `/studio-hq`.
- **Pilot programme.**
  - Every pilot reel keeps a friction log.
  - Every pilot reel writes a `retro.md`, copied to `studio/retros/`.
- **Reel types.** `talking-head`, `music-montage` and `hybrid` are now defined. Music-montage cuts on the music's beat grid and skips transcription.
- **`project.md` fields.** The template now records the architecture version, reel type and pilot flag. `new_reel.sh` fills in the version.

## 0.1.0 — 2026-10-15
- Initial bootstrap. Covers:
  - `CLAUDE.md` contract;
  - `/cinematic-reel` skill and effects playbook;
  - analysis and transcription scripts;
  - Premiere MCP setup.
