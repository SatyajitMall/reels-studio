# Review gate (skill Phase 7b)

**The editor never grades its own work.** Before any cut goes to the director, a reviewer on a **different model** watches it and lists what's broken. The director only sees a cut that has passed, or has failed with every finding answered.

Why: in the my-reel pilot, every defect the director or a later frame-by-frame check caught had already passed the editor's own number-based QA. That included a Timewarp in the wrong place, smear on C073 since v6, ghosting on C076, and decorative looks that cheapened v8.

## Steps
0. **The brief must be current.** Before the gate, update `brief.md` so it describes the plan the director has approved *so far*: structure, runtime, looks, type, must-haves. Log changes in its changelog section. The first gate run on my-reel judged v8 against the v1 brief and reported "brief drift" instead of real problems.
1. **Shot list:** write `analysis/shots_v<N>.json`, a list of `[name, start_s, end_s]` in **reel time**, from the cut plan for this version.
2. **Watch the export:**
   ```
   ./.venv/bin/python scripts/watch.py renders/exports/<reel>_v<N>.mp4 -o projects/<reel>/analysis/review_v<N>/watch --fps 2 --shots projects/<reel>/analysis/shots_v<N>.json
   ```
2b. **Scan every frame:** `./.venv/bin/python scripts/frame_scan.py renders/exports/<reel>_v<N>.mp4 -o projects/<reel>/analysis/review_v<N>/scan.json --shots projects/<reel>/analysis/shots_v<N>.json`. It takes seconds, and catches defects shorter than the 2 fps sheets can show.
3. **Call the reviewer:** the Agent tool with `subagent_type: "reel-reviewer"` and `model: "fable"` (it must differ from the editor's model; if the editor is Fable, use `opus`). The prompt gives:
   - the export path, `scan.json`, `watch/index.md`, `brief.md` and `studio/director-profile.md`;
   - a scratch dir for frames: `analysis/review_v<N>/frames/`;
   - this round's director notes, i.e. what was supposed to change.

   **Don't** pass your own QA conclusions or your reasons for choices. The reviewer judges blind.
   If `reel-reviewer` isn't listed as an agent type (an older session), use `general-purpose` with `model: "fable"` and tell it to read and follow `.claude/agents/reel-reviewer.md`.
4. **Save the report** as `analysis/review_v<N>.md`, unedited.
5. **Answer every blocker and major** in `project.md` under `## Round N — Review gate`:
   - **fixed:** what changed;
   - **intended:** why, and the director will be asked about it at Checkpoint 2;
   - **disagree:** with evidence, e.g. a frame showing the reviewer misread it.
6. **After fixes, re-run steps 2–4 on the new export.** At most 2 loops. If blockers are still open after the second loop, stop and tell the director.
7. **At Checkpoint 2,** include a 3-line review summary: the verdict, what was fixed, and what's left as intended or disputed.

## Calibration (my-reel v8, 2026-10-17)
Blind Fable review vs the pilot's own frame-by-frame QA:
- **Caught 5 of the pilot's 8 failing shots fully and 2 partly.** It missed C029's ray haze and C073's 0.2 s jerks.
- **Found 12 real issues the pilot's QA missed:** dissolves where the brief says hard cuts, the title not in the profile's type style, a repeated subject, a phone in frame, a music hit with no cut, a static hook.
- **Changes made after this run:** `frame_scan.py` catches both C073 jerks and C076's smear to within a few frames; the haze check went into the reviewer's checklist; step 0 keeps the brief current.

A review costs about 15 min and 200k tokens on Fable.

## Learning
- A finding that comes back in two reels is a studio rule: file a CR.
- A reviewer miss that the director catches is a gap in `.claude/agents/reel-reviewer.md`'s checklist: file a CR so HQ adds it.
