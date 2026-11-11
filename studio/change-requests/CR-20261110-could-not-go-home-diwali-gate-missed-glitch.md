# CR-20261110-could-not-go-home-diwali-gate-missed-glitch

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 |
| Type | script · skill · rule |
| Severity | blocker (a glitchy opening reached the director after four PASS loops) |
| Status | done (v0.10.2) |

## What happened
At Checkpoint 2 the director wrote: "The first few seconds are glitchy. Because they are recorded in low FPS, the frames are glitchy in certain sections… And they are not cinematic enough in nature… I also want to know how certain glitchy videos are passing the review cut."

The review gate passed v3b four times (`analysis/review_v3b.md` … `review_v3b4.md`), and pregate passed it too. A fresh H.264 export straight from Premiere (`renders/exports/could-not-go-home-diwali_v3b_premiere.mp4`) matches the ProRes master and the phone copy frame for frame (PSNR ≥ 47 dB on every frame, 769 frames). So the encode chain added nothing: the glitch is in the cut.

**What the glitch is.** Shot 01 (0–1.56 s) is a step-print: each image is held 3 frames, about 8 images a second, on a handheld night shot from inside a moving auto.
- Every new image jumps 6–21 px in a random direction.
- The auto's windscreen frame drops in steps through the shot.
- 11 jumps in 1.56 s; jitter 8.8 px RMS; jerk p95 14.5. That's the worst jerk in the reel except S1, where the hands' own motion inflates the number.
- Evidence: `projects/could-not-go-home-diwali/analysis/inspect_v3b_premiere/frames_000-038_shot01.png` (every frame) and `analysis/motion_v3b_premiere/motion_audit.json`.
- The camera itself shot 25 fps at 1/50 (ingest report). The "low FPS" the director sees is the step-print the editor added.

**Why four gate loops passed it:**
1. **The editor marks its own spans as designed.** Pregate ran with `--designed 0-1.56 9.52-9.60 17.40-18.96 28.56-30.76`. The first and third spans are the two step-prints. Every scan flag inside them counts as "expected". Nobody else checks that a designed span is really good; the editor's label is enough.
2. **The reviewer can't see it.** It watches at 2 fps (`scripts/watch.py` default), and the jerk happens 8 times a second, so on the sheets it looks like a row of unrelated stills.
   - It counted the holds (13 × 3 frames, even) and called the cadence clean.
   - It judged the content against the brief's wording ("the auto driver sits still while the bus and street streak past in steps") and wrote "driver static". The every-frame sheet shows the whole interior jumping.
3. **The motion numbers existed but decided nothing.** `tools/motion_audit.py` (reel-local) measured the 11 jumps. Nothing in pregate or the gate sets a limit on jitter, jerk or hold-to-hold shift. The editor read the numbers as "the device's character" and moved on.
4. **No rule says what a step-print can be made from.** A step-print turns every bump in the source into a 3-frame jerk. The reference's step-print is on a steady shot. Ours is on a shot from inside a moving auto, stabilised with Warp Smooth: the drift remains, and the step-print quantises it into jumps.
5. **The gate checks technique, not whether it's cinematic.** "Not cinematic enough" isn't on the reviewer's checklist.

## Workaround used in the reel
- Exported straight from Premiere, so the director inspects the true render.
- Made every-frame sheets of the opening and of the suspect shots (`analysis/inspect_v3b_premiere/`).
- The fix waits on the director's inspection. Options: drop the step-print on 01 and play it real time and stabilised, or step-print a steadier shot.

## Proposed change
1. **`scripts/pregate.py`: designed spans get a type.** For example `--designed 0-1.56:step-print 28.56-30.76:end-card`.
   - Only the flags that type expects are allowed: holds for a step-print; black and freeze for an end card.
   - A step-print span is still motion-checked. FAIL when the global shift from one hold to the next is above 4 px (1080-wide terms) after the shot's smooth path is removed.
2. **Promote `projects/could-not-go-home-diwali/tools/motion_audit.py` into `scripts/` and run it as a pregate step.**
   - It measures per-shot jitter, jerk p95, jumps and repeats on the export.
   - Starting limits: jerk p95 ≤ 6, no jump off the trend > 8 px. A shot over a limit needs a reviewer verdict on a full-rate strip, and the editor can't waive it.
   - The output must separate subject motion from camera motion (S1's 28 px is hands moving), for example by measuring a static background region.
3. **`review-gate.md` and the reel-reviewer prompt:**
   - Always run a 25 fps every-frame strip of the hook (0–3 s), of every designed span, and of every shot pregate flags for motion. Use `watch.py --fps <seq fps>` on those spans.
   - Tell the reviewer that the brief's description of a shot is the editor's intent, not a fact. It verifies it on the every-frame strip ("driver static" was false).
4. **Playbooks (cinematic-montage, story-montage): source rule for step-prints.**
   - Only from a locked-off shot, or one stabilised to ≤ 2 px residual shake.
   - Never from inside a moving vehicle unless the frame is locked to the vehicle.
   - Measure hold-to-hold shift before the director sees it.
5. **Reviewer checklist, "cinematic" line:** score each shot on motion quality (smooth vs jerky), sharpness and intent, not only on defects. Flag the hook when it reads as a fault rather than a style.

## HQ decision
**v0.10.2, 2026-11-11: done**, with the director's go-ahead ("Yes, fix it now"). Each cause was verified in the scripts first.

| # | Proposed | Done |
|---|---|---|
| 1 | Typed designed spans; step-print hold-to-hold shift FAIL > 4 px | ✅ `pregate.py --designed T0-T1:type` (fade, end-card, title, step-print, flash, transition, freeze; untyped allows black only), and the hold-shift FAIL in `motion_audit.py`. v3b shot 01: 7.9 px → FAIL; shot 12 (steady source): 0.3 px → PASS |
| 2 | `motion_audit` into `scripts/` and pregate, with limits, subject vs camera | ✅ `scripts/motion_audit.py`: the camera is measured on the frame's outer ring, subject on the whole window, `--window`. Jerk p95 > 6 or a jump > 8 px → REVIEW, which the editor can't waive |
| 3 | Full-rate strips for the reviewer; the brief is intent, not fact | ✅ pregate `strips/` (hook, designed spans, REVIEW shots, cropped to the window; `watch.py --crop`, frame-exact at full rate); `reel-reviewer.md` steps 1b and 1c; `review-gate.md` |
| 4 | Step-print source rule | ✅ effects-playbook §C and story-montage: a smooth camera path only, check the render's hold shift |
| 5 | Cinematic line in the checklist | ✅ `reel-reviewer.md`, with "an effect in the hook that reads as a fault is a major" |

For this reel's next gate: type the spans (`0-1.56:step-print 9.52-9.60:transition 17.40-18.96:step-print 28.56-30.76:end-card`) and add `--window 0,505,1080,810`. Shot 01 will FAIL until it is re-cut (play it in real time stabilised, or step-print a steadier shot).
