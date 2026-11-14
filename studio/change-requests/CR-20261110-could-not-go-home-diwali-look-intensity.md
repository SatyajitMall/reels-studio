# CR-20261110-could-not-go-home-diwali-look-intensity

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 |
| Type | rule · script |
| Severity | polish (would have shipped a look 1.45× stronger than approved) |
| Status | open |

## What happened
The director approved the reference look on an offline preview. That preview applied `ref_match.cube` through ffmpeg as a **linear 60 % blend** (`lut3d` + `blend=all_opacity=0.6`, the same mix `look_preview.py`-style previews use). In Premiere I set the V3 adjustment layer's Lumetri **Creative Intensity to 60**.

Measured on 8 shots that are identical in both versions (window mean RGB, look minus camera-true), Premiere at 60 moved the picture about 1.45× further than the preview: ΔRGB −0.029/−0.015/−0.039 against −0.020/−0.010/−0.027, and Δsat +0.042 against +0.025.

## Workaround used in the reel
Set Intensity 40 and measured again. Premiere's shift then matched the preview within 0.006 RGB and 0.013 saturation on every shot.

## Proposed change
- **Effects-playbook §A3 and the reality doc:**
  - Lumetri Creative Intensity is not a linear mix: Intensity ≈ 0.67 × the preview's blend % (measured with one custom .cube).
  - After loading a look, always match the build's look-minus-camera-true shift to the approved preview's, on shots identical in both, before export. The snippet is in this reel's `project.md`, Phase 4 look notes.
- **`look_preview.py` / `preview_edl.py`:** label preview mixes as "linear blend %", and print the matching Lumetri Intensity estimate.
