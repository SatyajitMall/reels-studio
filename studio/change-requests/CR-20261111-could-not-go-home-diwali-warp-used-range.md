# CR-20261111-could-not-go-home-diwali-warp-used-range

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.10.2 |
| Type | skill · rule |
| Severity | polish (the reel shipped over-cropped, shaky shots until the director complained) |
| Status | open |

## What happened
At Checkpoint 2 (v3c), the director's notes were:
- "still jumping";
- "frames seem cut or incomplete";
- "don't crop the shots too much, it looks odd, the background should be there".

Every stabilised shot had been solved by Warp Stabilizer over a clip in `STAB_v3` that was longer than the part the reel plays. The clips ran 47–60 frames; the reel plays 39–40. Warp sizes its auto-scale to the worst displacement over the **whole analysed clip**, and the solve chases motion the reel never shows. 18's catch-up snap in v3c loop 1 had the same cause.

Re-solving each shot over **only the frames the reel plays (±2)** gave lower crop and equal or steadier results:

| Shot | Mode | Crop before → after | Camera jitter before → after |
|---|---|---|---|
| 02 | No Motion | 116.3 → 109.8 % | 0.48 → 0.33 px |
| 10 | No Motion | 112.7 → 111.4 % | 0.30 → 0.26 px |
| 11 | No Motion | 120.0 → 109.6 % | 0.16 → 0.14 px |
| 14 | Smooth | 115.4 → 104.8 % | 3.69 → 2.97 px |
| 01 | No Motion (was Smooth) | 112.2 → 113.3 % | 6.05 → 2.15 px |

Measurements are in the 4:3 window with `scripts/motion_audit.py`. Evidence: `projects/could-not-go-home-diwali/project.md` "v3d build".

Crop also stacks: Warp auto-scale × the reel's own Scale × the 4:3 window. 11 showed about 42 % of the camera width in v3c, and nothing measured that.

## Workaround used in the reel
- A clone `STAB_v3d`: each shot was re-placed with handles of ±2 frames, then Warp added, one clip at a time.
- Crop was read from the Warp property label "Auto-scale (x%)".
- Shake was measured on test exports; the steadier mode was kept, with a cap of about 110 %.
- The shots were re-placed, keeping their Motion keys. Positions were moved so the window centre keeps its scene point.

Scripts: `analysis/es/rewarp_v3d.jsx`, `build_v3d.jsx`.

## Proposed change
1. **effects-playbook §B/§C (stabilise):** analyse Warp over only the frames the reel plays, plus 2-frame handles. Never stabilise the whole take and trim it afterwards.
2. **Crop cap:** Warp auto-scale ≤ 110 % by default. Above that, try the other Result mode (Smooth vs No Motion) over the used range before accepting it.
3. **Crop in pregate:** report each shot's total crop as camera width shown = window ÷ (reel Scale × Warp scale), and flag any shot below the director's floor. Today only the reel Scale is checked (effects-playbook §B "≥ 70 % width").
4. **Optional:** a `scripts/` helper that re-places a clip in a stab sequence over a given range, adds Warp with Result/Method/Smoothness/Max scale, waits for status 408 and returns the auto-scale. This reel's version is `analysis/es/rewarp_v3d.jsx` plus `warp_status_v3d.jsx`.

## HQ decision
<!-- HQ fills this in. -->
