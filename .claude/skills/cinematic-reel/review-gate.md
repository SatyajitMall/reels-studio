# Review gate (skill Phase 7b)

**The editor never grades its own work.** Before any cut goes to the director, a reviewer on a **different model** watches it and lists what's broken. The director only sees a cut that has passed, or has failed with every finding answered.

Why: in the my-reel pilot, every defect the director or a later frame-by-frame check caught had already passed the editor's own number-based QA. That included a Timewarp in the wrong place, smear on C073 since v6, ghosting on C076, and decorative looks that cheapened v8.

## Steps
0. **The brief must be current.** Before the gate, update `brief.md` so it describes the plan the director has approved *so far*: structure, runtime, looks, type, must-haves. Log changes in its changelog section. The first gate run on my-reel judged v8 against the v1 brief and reported "brief drift" instead of real problems.
1. **Shot map:** write `analysis/map_v<N>.json` in **reel time** from this version's cut (skill Phase 3), one object per shot. For an offline preview, the EDL it was rendered from is the map, and the pregate takes `--profile ig-quiet`:
   ```json
   [{"name": "01_C010", "start": 0.00, "end": 2.32, "clip": "projects/<reel>/raw/b-roll/A001_10211852_C010.mov", "src_in": 0.00, "rate": 1.0},
    {"name": "05_C051", "start": 8.40, "end": 10.24, "clip": "projects/<reel>/raw/b-roll/A001_10212101_C051.mov", "src_in": 4.00, "rate": 0.553},
    {"name": "13_end_card", "start": 27.48, "end": 29.84}]
   ```
   - `clip` is the **camera file**, relative to the studio root, even for a slow-mo shot swapped for an After Effects render (then `rate` = the speed). `src_in` is camera seconds at the shot's first frame; `rate` is camera seconds per reel second (× interpreted / native fps for a conformed clip). Names are unique. Cards, graphics and AI shots need only name, start and end. Details in `scripts/camera_fidelity.py`.
2. **Pregate (scripts, minutes, no tokens),** from the studio root:
   ```
   ./.venv/bin/python scripts/pregate.py projects/<reel>/renders/exports/<reel>_v<N>.mp4 \
       --map projects/<reel>/analysis/map_v<N>.json -o projects/<reel>/analysis/pregate_v<N> \
       --fps <seq fps> --expect <runtime s> --designed <T0-T1 …> \
       [--reviewed projects/<reel>/renders/exports/<reel>_v<last PASS>.mp4 --reviewed-map projects/<reel>/analysis/map_v<last PASS>.json] \
       [--allow <shots>] [--look] [--exclude-band 0.72,0.82]
   ```
   - `--designed`: the intended black or flagged spans in seconds (a fade-in `0-0.5`, an end card `27.3-29.84`).
   - `--exclude-band`: leave the subtitle band out of the colour stats (white captions can trip the burn check).
   - `--allow` / `--look`: the shots and the look the brief names as deliberate departures from the camera.

   It runs `verify_render.py`, `frame_scan.py` (every frame), `camera_fidelity.py` and, with `--reviewed` (the last version that **passed** the gate, not just the previous export), `render_diff.py`, then `watch.py` for the sheets. A check that crashes counts as a FAIL. **Fix every FAIL first:** in the first five reels 47 of 59 gate runs failed, mostly on things a script can see. It writes `shots.json` and states the review scope in `PREGATE.md`: full, focused on the changed shots, sound only, or no change (nothing to review).
3. **Call the reviewer:** the Agent tool with `subagent_type: "reel-reviewer"` and a **`model` other than the editor's own**: Fable for an Opus editor; Opus for a Fable or Sonnet editor. If that model is out of credits or unavailable, take the remaining model that still isn't the editor's (Sonnet for an Opus or Fable editor, Fable for a Sonnet editor). Never the editor's own model; if none is available, stop and tell the director.
   - **Full review** for a new cut (the first review, or when pregate says the structure changed). The prompt gives the export path, the pregate folder (`scan.json`, `watch/index.md`, `fidelity/FIDELITY.md` and `fidelity/fidelity_sheet.jpg`), `brief.md`, the brief's playbook (`playbooks/<name>.md`) and `studio/director-profile.md`.
   - **Focused review** for a fix version with the same cut: the same inputs plus `diff.json`, and the instruction to judge **only the changed shots** and confirm the rest is untouched (frames and audio md5). Goddess v9b–v10b ran this way. For a sound-only change, the reviewer judges the sound at the changed moments.
   - Both get a scratch dir for frames (`analysis/review_v<N>/frames/`), this round's director notes (what was supposed to change), and **the editor's model name**, so the reviewer can refuse to run on the same model.

   **Don't** pass your own QA conclusions or your reasons for choices. The reviewer judges blind.
   If `reel-reviewer` isn't listed as an agent type (an older session), use `general-purpose` with the same `model` rule and tell it to read and follow `.claude/agents/reel-reviewer.md`.
4. **Save the report** as `analysis/review_v<N>.md`, unedited.
5. **Answer every blocker and major** in `project.md` under `## Round N — Review gate`:
   - **fixed:** what changed;
   - **intended:** why, and the director will be asked about it at Checkpoint 2;
   - **disagree:** with evidence, e.g. a frame showing the reviewer misread it.
6. **After fixes, re-run steps 2–4 on the new export.** At most 2 loops; then one **focused check of the last fixes** (changed shots only), so no fix reaches the director unseen. In four reels the cap was hit and the last fixes went unreviewed. If blockers are still open after that, stop and tell the director.
7. **At Checkpoint 2,** include a 3-line review summary: the verdict, what was fixed, and what's left as intended or disputed.

## Calibration (my-reel v8, 2026-10-17)
Blind Fable review vs the pilot's own frame-by-frame QA:
- **Caught 5 of the pilot's 8 failing shots fully and 2 partly.** It missed C029's ray haze and C073's 0.2 s jerks.
- **Found 12 real issues the pilot's QA missed:** dissolves where the brief says hard cuts, the title not in the profile's type style, a repeated subject, a phone in frame, a music hit with no cut, a static hook.
- **Changes made after this run:** `frame_scan.py` catches both C073 jerks and C076's smear to within a few frames; the haze check went into the reviewer's checklist; step 0 keeps the brief current.

A full review costs about 15 min and 200k tokens on Fable. In the first five reels the gate ran 59 times (47 FAIL); goddess alone ran 23, which used up the week's Fable allowance. Hence the pregate, focused reviews and the model fallback (v0.8).

## Learning
- A finding that comes back in two reels is a studio rule: file a CR.
- A reviewer miss that the director catches is a gap in `.claude/agents/reel-reviewer.md`'s checklist: file a CR so HQ adds it.
