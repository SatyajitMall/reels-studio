---
name: cinematic-reel
description: Turn the director's clips into a fully treated cinematic 9:16 Instagram Reel in Adobe Premiere Pro. Claude interviews the director, studies references, writes the brief, then cuts, colour-corrects, grades, adds effects, graphics, captions and sound design, and exports. Use when the user wants to make, edit or revise a reel.
---

# /cinematic-reel

The director answers questions, shares clips and references, and approves. **You write everything**: brief, cut list, treatment. This is never cut-and-stitch: every reel gets colour correction, a creative look, motion, transitions, type and sound design, planned in the brief and taken from `effects-playbook.md` (same folder; read it before Phase 2).

**Every reel follows one editing playbook** (`playbooks/`, same folder): the style rules for its kind of video, meaning pace, camera, type, transitions, sound (including whooshes), colour and the QA thresholds. Pick it in Phase 0, record it in the brief, and read it before Phase 2. `effects-playbook.md` is the menu of moves; the playbook says which ones this reel uses.

Stop at the three **⏸ checkpoints**. Follow every rule in `CLAUDE.md`.

Argument: reel name (folder under `projects/`). If it doesn't exist, run `scripts/new_reel.sh <name>`.

**This is a reel session** (`studio/ARCHITECTURE.md`). Write only to:
- `projects/<name>/`;
- `studio/change-requests/`;
- `studio/retros/`;
- new files in `assets/`.

When the architecture falls short:
- work around it inside the reel;
- log the workaround in `project.md`;
- file a CR from `studio/change-requests/_TEMPLATE.md`.

Never patch `CLAUDE.md`, skills, scripts or the template.

**Two files to read once per reel:**
- `studio/director-profile.md`: handle, type style and working preferences. Don't re-ask anything it answers.
- `premiere-mcp-reality.md` (this folder): which Premiere tools are broken and the verified fallbacks.

**Any manual step for the director** goes out as a short numbered list naming the panel and menu path, ending "come back and say done".

 If `project.md` says `Pilot: yes`, append to `## Friction log` whenever something:
- is slow;
- fails;
- needs a guess;
- needs a manual step;
- needs a workaround.

---

## Phase 0: Interview the director
Read `project.md` and `studio/director-profile.md` first. If a round is already in progress, resume it. Check `Arch version` against `studio/VERSION`. If they differ:
- check `studio/CHANGELOG.md` for changes since then;
- adopt minor or patch changes at the start of the next round;
- ask the director before adopting a major change.

Ask in **two short rounds**, with multiple choice wherever possible (AskUserQuestion when available). Never ask something the footage or a reference can answer.

**Round 1: the idea (ask before looking at footage)**
1. What's this reel about, in a sentence or two? What happens in the clips? Is anyone speaking (on camera or VO)? → sets **reel type**: `talking-head` · `music-montage` · `hybrid`. Record it in `project.md`.
   Then propose the **playbook** from `playbooks/README.md` (`music-montage` → `cinematic-montage`; `talking-head` → `creator-explainer`; `hybrid` → both, by stretch). If nothing fits, use the closest one and file a CR for a new playbook.
2. What should viewers feel or do at the end? (laugh · learn · be inspired · follow · save · click link)
3. Who's it for?
4. Length? (15–20 s · 30–45 s · 60 s · whatever the story needs)
5. Branding, only if `studio/director-profile.md` doesn't already answer it: handle, type style, brand colours. Ask now, not at the end card. Anything new goes into `project.md` and a CR to update the profile.
6. References: 1–3 reels or creators whose *feel* they want. Ask them to drop video files in `projects/<name>/references/` or paste links. Instagram links often can't be fetched, so ask for a screen recording or the downloaded file.

**Round 2: taste (ask after analysing footage and references, so the options are concrete)**
Offer choices that fit *this* footage, for example:
- Look: Warm Film · Teal & Orange · Moody Desat · Clean Bright · Mono Drama · Match reference. **Show, don't name:** run `scripts/look_preview.py` on 3–4 of the director's own stills (night, a face, a wide). It renders Premiere's own film-stock looks (effects-playbook §A3 film table) as one labelled sheet, with measurements. Offer 3–4 looks that fit the footage, not all 12. These are previews only; the real look is built in Premiere in Phase 4, from the same LUT
- Pace: calm (3–5 s shots) · medium (2–3 s) · fast (1–2 s), pre-selecting what the reference measured
- Effects intensity: subtle · signature moments only · heavy / stylised
- Captions / words: none · Clean · Bold Kinetic · Editorial. For music-montage, default to **title + end card only**. Use beat words only when the director supplies words that mean something; never invent filler words.
- Music: their file in `assets/music/` · mood + BPM for you to suggest
- Anything that must or must not happen

## Phase 1: Preflight & footage analysis
1. `verify_premiere_connection`. If it fails, stop and give the CEP panel steps. Read `premiere://config/get_instructions` once.
2. `get_project_info`, `list_sequences`, `list_project_items`.
   - **Premiere sample media:** Premiere 2026's New Project screen imports Adobe sample clips by default (`mediaPath` under `/Users/Shared/Adobe/Premiere Pro/*/Sample Media/`), plus an auto-built `Sequence 01`.
     - If you find them, list them for the director and ask before removing anything.
     - On a yes, remove them with the temp-bin delete in `premiere-mcp-reality.md` (`delete_multiple_project_items` and `delete_project_item` are broken), plus `delete_sequence`. Confirm with `list_project_items`. Only the project references go; Adobe's sample files on disk stay untouched.
     - Never delete a sequence the director made.
3. If the director's footage lives outside the studio, link it in rather than copying it. The originals stay untouched:
   ```
   scripts/link_footage.sh <name> "<source folder>" [a-roll|b-roll]
   ```
   Then run the analysers (no API key needed):
   ```
   .venv/bin/python scripts/analyze_footage.py projects/<name>/raw/a-roll projects/<name>/raw/b-roll -o projects/<name>/analysis
   .venv/bin/python scripts/analyze_footage.py projects/<name>/references -o projects/<name>/analysis/references --reference
   ```
   **Look at the `overview_*.jpg` sheets first.** They show every clip's middle frame, labelled. Use them to:
   - shortlist hero clips;
   - spot upside-down or sideways clips; orientation isn't auto-detected, so fix those with a 180° / 90° rotation and log it.

   Then open the `contact.png` of each candidate and read `summary.md`. On dark shoots (night, stage, candle-lit), exposure is judged relative to the shoot's median, so "darker than the shoot" is the flag that matters. If a reference's contact sheet shows more distinct shots than the cut count, rerun it with `--scene-threshold 0.1`. Trust the count once two thresholds agree. Note per clip: exposure, colour cast, flat/log, fps (slow-mo headroom), orientation, what's actually in the shot, hero moments.

   **Measure the references** the same way we'll measure our cut:
   ```
   .venv/bin/python scripts/teardown.py --ref projects/<name>/references/<ref>.mp4 -o projects/<name>/analysis/teardown
   ```
   It gives cuts per minute, shot lengths, flashes, motion, picture (luma, contrast, saturation, warmth) and loudness. Put the numbers in the brief as targets.
4. Timing source, by reel type (CLAUDE.md §4):
   - `talking-head` / `hybrid`: transcribe dialogue with `scripts/transcribe_reel.sh <name>`, which produces `transcripts/takes_packed.md`. If there's no ElevenLabs key, use `detect_silence` and tell the director word-level cutting is off.
   - `music-montage` / `hybrid`: run the beat grid on the music track:
     ```
     .venv/bin/python scripts/gemini_audio_and_beat_analyzer.py --music assets/music/<track> -o projects/<name>/analysis
     ```
     Then read `analysis/audio_summary.md`. Use its **Energy / sections** table and **Candidate cuts** (best start/end for 15/30/45/60 s) to pick the music section. Check the labels by ear, since they're heuristic. No music yet: ask for it in Round 2. The EDL can't be planned without it.
5. `create_bin` (`01_A-Roll`, `02_B-Roll`, `03_Graphics`, `04_Textures`, `05_SFX`, `06_Music`), then import everything with the ExtendScript `importFiles` snippet in the reality doc. `import_folder` is broken, and `import_media` ignores `binName`. Confirm with `list_project_items`.
6. Conform outlier frame rates now, before anything is placed: `set_override_frame_rate` to the sequence fps (CLAUDE.md §3).
7. **Selects and motion** (music-montage / hybrid: always; talking-head: for B-roll). Run these in the background while Round 2 is asked:
   ```
   .venv/bin/python scripts/selects_score.py projects/<name>/raw/b-roll -o projects/<name>/analysis --skip <unusable ids>
   .venv/bin/python scripts/motion_holds.py projects/<name>/raw/b-roll -o projects/<name>/analysis --skip <unusable ids>
   ```
   `selects.md` ranks every clip's best 1 s moments (sharp, colourful, steady). `motion.json` gives each clip's static holds and pans. **Review the top moments by eye** (contact sheets / stills) before writing the EDL. The score can't judge meaning, faces or composition. In the pilot, this found better shots than picking from mid-frames.

→ Now ask **Round 2** of the interview.

## Phase 2: Write the brief + cut plan
1. Fill in `projects/<name>/brief.md` completely: **playbook** (and any rule this reel overrides, with the reason), idea, hook, references turned into measured parameters, **Treatment** (pace, colour stages A1–A4, named effects and transitions with their beats, type, sound), the clip table, must/must-nots, open questions.
   For **music-montage**, the Treatment must also include:
   - **Energy arc:** which song sections go up or down and where the shot length changes. Default: slow open → build → full → breath → payoff → outro. **Never one shot per bar for the whole reel.** That read as mechanical in the pilot. The music may be edited (e.g. intro joined to the main section on a downbeat).
   - **Generated shots (if any):** every AI-generated shot gets its own row, labelled **AI-generated**, with the prompt, why your footage can't provide it, and the cost from the `gen_video.py` dry run. The director approves each at Checkpoint 1 (`motion-and-ai.md` §3).
   - **Motion style:** which shots stay as handheld movement, which are held, and where digital push/pull goes (only on `motion.json` holds). Plus where slow-mo goes (calm shots only).
2. In `project.md`, under `## Round 1 — Proposal`:
   - 3 hook options with a recommendation. Talking-head hooks quote the line and its source timecode. Music-montage hooks give the shot, its source timecode and the accent beat it lands on;
   - EDL table: `# | clip | in | out | text / action | V1 move | V2/V5 | transition out | SFX`;
   - estimated runtime.

### ⏸ Checkpoint 1: brief + cut plan
Give the director a short summary in chat: the concept, hook, look, 4–6 signature moments, runtime, and anything from their answers you couldn't honour. Wait for a yes or for changes.

## Phase 3: Rough cut (V1 / A1)
1. `duplicate_sequence`, or create a 1080×1920 sequence at the footage's most common frame rate (CLAUDE.md §3) → `Reel_<name>_v<round>`, then open it in the timeline. `create_sequence` needs an `.sqpreset`, so use `create_sequence_from_clips` on a clip that has the target size and fps.
2. Assemble the approved EDL with `add_to_timeline_batch`, or razor + `ripple_delete` on the duplicate.
3. Reframe to 9:16 (`auto_reframe_sequence` or `set_clip_scale` / `set_clip_position`).
4. Check with `get_timeline_gaps` (zero unintended gaps) and `get_timeline_summary` (matches the EDL).
5. A1: Constant Power crossfade at every cut (`batch_add_transitions`, ~1 frame). `save_project`.

## Phase 4: Colour (playbook §A, strictly in order)
1. **A1 primary correction**: one `color_correct` per clip with contrast, temperature and tint only, then set exposure, highlights, shadows and saturation by script (playbook §A1, reality doc). Copy to same-setup clips with `copy_effects_between_clips`. Check the first clip by exported still before copying.
2. **A2 shot match**: compare adjacent shots and fine-tune with `set_effect_property`.
3. **A3 creative look**: ask the director for the one manual step (create an Adjustment Layer), place it on V3, apply the look's built-in Lumetri preset and set its intensity (playbook §A3).
4. **A4 texture**: grain / leaks on V4, with the blend mode set by script (enum in the reality doc) + `set_clip_opacity`. Fade V4 with the picture at every fade to black.
5. Export 3–4 still frames (or a short preview) and check skin tones and contrast with your own eyes. `save_project`.
6. **Colour QA on every frame** before review: `scripts/colour_report.py <export> -o analysis/colour_v<N>.json --shots <shots.json> [--gold]`.
   - Targets: shots within ±0.03 of the montage luma, crushed < 25 % (except true-black skies), clipped < 2 %, gold midtone hue 30–45°, blue shots G−M ≈ 0.
   - Fix the unintended flags. Note the deliberate ones in `project.md`.

## Phase 5: Motion, effects, B-roll, graphics, captions
Execute the Treatment from the brief, beat by beat:
1. V1 moves (punch-ins, slow pushes, snap zooms, shakes), playbook §B. **Not on handheld footage**: shakes and snap zooms read as "jumps" there, so use push/pull on holds.
   Stabilise handheld moving shots by default with Warp Stabilizer. For speed-changed or interpreted clips, nest first: `seq.setInPoint/OutPoint`, target only V1, `createSubsequence(false)`, swap the nest in, then Warp the nest. Afterwards:
   - re-measure with `scripts/shake_report.py` (before vs after);
   - scan the export for Warp's "Analyzing" banner, a text band mid-frame.
2. B-roll on V2 at the trigger words, with time effects (slow-mo, ramps, freeze, reverse), §C.
3. Transitions at the planned cuts, §D. Hard cut is the default; keep it to 3–4 non-cut transitions per 30 s.
4. Graphics: HyperFrames motion graphics rendered as ProRes 4444 alpha and placed on V5, positioned per shot. Text-behind-subject goes on holds only, via `scripts/text_behind.py` (`motion-and-ai.md` §1–2).
5. Captions on V5, in the style from the brief and inside the safe zone.
6. After each group: `get_timeline_summary`, `list_clip_effects` on 2–3 clips to confirm nothing stacked twice, then `save_project`.

## Phase 5b: After Effects finishing (optional)
For shots that need **denoise, a real speed-ramp curve, Timewarp slow-mo or glow/halation**, follow `after-effects.md` (same folder):
1. Write `analysis/ae_jobs.json` from the EDL.
2. Run `scripts/ae_roundtrip.py`, in the background, at about 4 min per shot.
3. Check every `_compare.png` and the before/after reports.
4. Swap the ProRes renders in at the same timeline positions.

Plan which shots go through After Effects in the brief's Treatment, and say so in the round summary. Stabilisation stays in Premiere (Phase 5): AE's Warp Stabilizer can't be run by script.

## Phase 6: Sound design & mix
- SFX on A2 where **this reel's playbook** allows them (its Sound section), from the menu in `effects-playbook.md` §F. Run `scripts/sfx_prep.py` first and place each by its transient. Levels: the playbook's (cinematic-montage swishes about −13 dB; otherwise −14…−18 dB).
- Music on A3:
  - section changes on the beat;
  - planned silence drops;
  - talking-head / hybrid: `setup_ducking` under A1 (−18…−22 dB under speech, about −8 dB in gaps);
  - music-montage: music leads, peaks −1…−3 dB, no ducking.
- A1:
  - talking-head: dialogue peaks −6…−3 dB;
  - music-montage: natural sound muted or ≤ −20 dB unless it adds impact.

## Phase 7: QA & export
1. `validate_project_for_export`, `check_offline_media`, `get_timeline_gaps`, `set_sequence_in_out_points`.
2. Export H.264 1080×1920, high bitrate → `renders/exports/<name>_v<round>.mp4`, using a built-in `.epr` (paths in the reality doc).
   **Check the audio straight away** (`ffmpeg -af volumedetect`, max_volume > −20 dB). If it's silent, write `analysis/mix.json` and rebuild the audio with `scripts/mix_from_edl.py`. Note it in the round summary.
3. Run `analyze_footage.py` on the export, look at its contact sheet, and check the first 3 s plus 2–3 risky cuts with `scripts/cut_view.sh`.
4. **Verify the file** (codec, size, fps, bitrate, BT.709 tags, black or frozen frames, audio length, loudness):
   ```
   .venv/bin/python scripts/verify_render.py renders/exports/<name>_v<round>.mp4 --fps <seq fps> --expect <runtime>
   .venv/bin/python scripts/verify_render.py renders/exports/<name>_v<round>_IG.mp4 --profile ig-quiet   # no-music upload version
   ```
   Fix every FAIL before the review gate: `--fix-tags` for missing colour tags, `--fix-loudness` for a mix outside −14 ± 2 LUFS. Re-run on the fixed copy.
5. **Compare with the reference:** `scripts/teardown.py --ref <ref> --ours <export> -o analysis/teardown`. Read `COMPARE.md`, and either fix each gap beyond tolerance or say in the round notes why it's deliberate.

## Phase 7b: Review gate (every version, before the director sees it)
Follow `review-gate.md` (same folder):
1. Make the shot list.
2. Run `scripts/watch.py` on the export.
3. Have the `reel-reviewer` agent on a **different model** judge it blind.
4. Save the report.
5. Fix or answer every blocker and major.
6. Re-run the gate, at most 2 loops.
Never skip it because your own metrics passed: in the pilot, every shipped defect had passed metric QA.

### ⏸ Checkpoint 2: review the cut
Send the export path, runtime and a 3-line "what I did" summary. Ask the director to **watch it full-screen on a phone with sound**, then ask one question before accepting approval: "What would make it more cinematic?" (In the pilot, v1 was approved and then reopened five times.) On notes: start round N+1 and log the notes in `project.md`. Change only what was asked, on a new sequence version, then reply with a numbered list of changes mapped 1:1 to the notes.

## Phase 8: Instagram package (after final approval)
Using `ig-hook-extractor`, `ig-caption-writer`, `ig-hashtag-strategist` and `ig-humanizer`, write to `project.md`:
- 3 first-line hooks (< 125 characters);
- the caption (hook in the first 125 characters, humanised);
- 3–5 sized hashtags;
- the cover frame timecode;
- if the reel has an AI-generated shot: a note to turn on Instagram's **AI info** label when posting (`motion-and-ai.md` §3).

### ⏸ Checkpoint 3: approve the package.

## Phase 9: Retro (pilot reels; optional for others)
After the package is approved:
1. Fill in `projects/<name>/retro.md`. Use the friction log, every workaround and every CR already filed. Be concrete: name the tool, the step, how long it took and what you'd change.
2. Copy it to `studio/retros/<name>.md`.
3. Turn each "change the studio" item into a CR in `studio/change-requests/`, unless one is already filed.
4. Set `Status` in `project.md` to `done`. Tell the director: "N change requests filed for HQ. Run `/studio-hq` in the HQ session to apply them."

