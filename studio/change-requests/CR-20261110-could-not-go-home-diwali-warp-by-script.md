# CR-20261110-could-not-go-home-diwali-warp-by-script

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 |
| Type | script · skill · rule |
| Severity | workaround (did it the slow way, about 1 h of trial) |
| Status | open |

## What happened
The director's note after v3: "multiple jumps and misalignment, shake and frame rate issue". The plan was to stabilise 12 handheld shots with Warp Stabilizer in Premiere 26.5.2, by script.

1. **The method can't be chosen through `stabilize_clip`.** Its `method` argument is ignored: the code adds Warp by QE and sets only Smoothness. Warp's default Method is **3 = Subspace Warp**, which bends the picture. That is the "distortion" this director rejected in v1b.
   - The properties, by index:

     | Index | Property |
     |---|---|
     | 3 | Result (0 = Smooth Motion, 1 = No Motion) |
     | 4 | Smoothness |
     | 5 | Method (0 = Position, 1 = Position/Scale/Rotation, 2 = Perspective, 3 = Subspace Warp) |
     | 9 | Framing |
     | 11 | Maximum Scale |
     | 31 | AnalysisStatusCounter |

2. **Setting properties on many clips at once breaks the analysis queue.** I added Warp to 11 clips by QE and set Method/Smoothness in the same loop. 7 clips stayed at status **201** (never analysed); 4 analysed. Setting property 0 (probably the Analyze button) to true did nothing.
3. **Changing Method after analysis doesn't re-solve.**
   - The status stays 408 and the "Auto-scale (x %)" label keeps its old value.
   - An export took 5.8 s for 699 frames of 4K. That's a render with no Warp work: jitter barely moved on most shots and got worse on one.
   - A clean solve exported in 136 s.
4. **No Motion past Maximum Scale** (C049 inside a moving auto) renders every frame **black**, with a vertical red banner: "To avoid extreme cropping set Framing to Stabilize Only or adjust other parameters". Status still reads 408; the label has no %.
5. **Warp can lock onto a moving crowd.** On C056 (a still man in front of a passing crowd) jitter went from 3.4 to 7.2 px with No Motion.

## Workaround used in the reel
- **A clip-sized stabilisation sequence** (`STAB_v3`, created from a bake so the sequence is 2160×3840 like the clip, Scale 100). All shaky shots sit back to back with 0.4 s handles. The sequence is exported once to ProRes, and the main sequence cuts from that file with the usual Rotation, Scale and push keys. This avoids Warp on resized clips (puja-night-2's 2-frame judder) and makes before/after measurable.
- **Per clip, one at a time** (`projects/could-not-go-home-diwali/analysis/es/rewarp.jsx`, `warp_next.jsx`):
  1. Remove the clip and re-place it fresh (a clean effect stack).
  2. QE `addVideoEffect("Warp Stabilizer")`, then immediately set Result, Method 1, Smoothness and Maximum Scale 120.
  3. Wait for status 408 before starting the next clip.
- **Measure before and after** (`projects/could-not-go-home-diwali/tools/stab_compare.py`: phase-correlation jitter inside the window crop), and look at the frames for the black banner.
  - Keep the Warp render where it helps: 02 4.6→1.2 px, 10 4.2→2.3, 11 6.5→0.3, 18 4.9→1.7.
  - Use the plain clip where it doesn't: 06, 09, 15, 17.
- **Avoid camera bumps by picking the window**, not by stabilising. `projects/could-not-go-home-diwali/tools/clean_window.py` gives per-frame sharpness and shift of a clip, and lists the clean runs (sharpness ≥ 0.85 × median, step ≤ 6 px). C062's bump at 1.0 s and C054's tail swing were cut around this way.

## Proposed change
1. **Reality doc, the `stabilize_clip` row:**
   - `method` is ignored and the default is Subspace Warp;
   - add the property index table above;
   - "set properties right after adding, one clip at a time, wait for 408";
   - a method change after analysis doesn't re-solve, so re-place the clip and re-add Warp;
   - No Motion over Maximum Scale renders black with a banner, so always check a frame.
2. **Skill Phase 5.1:** stabilise in a clip-sized sequence, export it, measure (shake before/after), and cut the main sequence from the render. Default Method = Position/Scale/Rotation; Result = No Motion for still subjects and Smooth for moves. Keep a Warp render only where it measurably helps.
3. **Script:** promote `stab_compare.py` and `clean_window.py` into `scripts/` (or fold them into `shake_report.py --compare` / `--clean-runs`). Make `frame_scan.py` flag Warp's black "extreme cropping" frames.
4. **Playbook (cinematic-montage), jump cuts:** when two shots of the same subject sit on the same axis, give the size change to the **steadier** shot of the pair. A punch-in magnifies handheld drift: 09 went from 6.6 to 15.8 px when punched in, so 08 took the close-up instead.
5. **Step-print rule:** at 25 fps use `--step 8.333` (exactly 3-frame holds, as in the reference). `--step 8` gives 3-3-3-4 holds, which read as a once-a-second hitch.

## HQ decision
<!-- HQ fills this in. -->
