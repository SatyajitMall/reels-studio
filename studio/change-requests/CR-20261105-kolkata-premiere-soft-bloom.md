# CR-20261105-kolkata-premiere-soft-bloom

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | skill · rule |
| Severity | polish |
| Status | partly done (v0.9.1) |

## What happened
- The director picked a "film stack" look from a Round 2 effects sheet: camera colour + soft bloom / mist + vignette + 5 % grain.
- The playbook's only bloom route is After Effects `glow` per shot (after-effects.md). For 13 shots that means ~50 min of round trips, swapping each ProRes render back into V1, and re-applying primaries and Motion on the swapped clips.
- Premiere 2026's Gaussian Blur is a new effect (`AE.Impact_Blur_FX`) whose size property is **Amount**, not "Blurriness". A script looking for "Blurriness" fails with `null is not an object`.
- Premiere 2026 also lists new glow effects (`Wonder Glow`, `Echo Glow`, `Edge Glow`, `VR Glow`, `Alpha Glow`). Untested.

## Workaround used in the reel
A Premiere-native soft bloom, fully scripted (`projects/kolkata/analysis/_es_bloom_v1.jsx`):
- per V1 shot, an identical copy on V2 (same project item, in-point, start, Motion values and push keys); its linked audio is removed from A2;
- one Lumetri on the copy that keeps only the highlights: Exposure −2, Contrast 100, Shadows −100, Blacks −100 (plus the V1 clip's own primary, if any);
- Gaussian Blur, Amount 20;
- Opacity 30 %, blend Screen (22).

The V3 adjustment layer (vignette) grades V1 + V2 together.

Tuned by render against the approved ffmpeg mist tile (luma +0.003–0.017, p98 +0.014–0.016) to luma +0.009–0.020, p98 +0.001–0.019 and saturation −0.002…−0.03 across 13 shots. The first values (Exp −1, Contrast 60, Amount 40, 40 %) were 3–5× too strong: hazy, with p02 doubled.

## Proposed change
1. `effects-playbook.md` §A4 (or a new §A3b "soft bloom / mist"): add this Premiere route with the verified numbers, as the default for a whole-reel bloom. Keep AE `glow` for halation on point lights.
2. `premiere-mcp-reality.md`: note that Gaussian Blur (2026) uses **Amount**, and list the new glow effects as untested.
3. `look_preview.py` or the ffmpeg skill: add the "mist" and "film stack" recipes, so Round 2 shows them like the film stocks, with measured deltas the Premiere build can be tuned to.

## HQ decision (v0.9.1, 2026-11-08)
- **(1) Done.** effects-playbook §A4: the V2 highlight-copy soft bloom with the verified numbers, as the whole-reel route; After Effects `glow` stays for halation on point lights.
- **(2) Done.** Reality doc rows: Gaussian Blur (2026) uses **Amount**; the new glow effects are listed as untested.
- **(3) Accepted for v0.12:** "mist" and "film stack" recipes in `look_preview.py`, so Round 2 shows them with measured deltas.
