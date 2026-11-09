# CR-20261108-kolkata-look-preset-second-lumetri

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | skill (effects-playbook §A3, premiere-mcp-reality.md) |
| Severity | workaround |
| Status | done (v0.9.1) |

## What happened
The director picked **Fuji Eterna 250D → Fuji 3510 at 30 %** (2026-11-08) for `Reel_kolkata_v7`. The V3 adjustment layer was inherited from an earlier round and already held one Lumetri Color: no look, vignette −0.5.

1. **`applyLumetriPreset` on a layer that already has a Lumetri adds a second Lumetri and inserts it *before* the existing one.**
   - Component order after the call: `Opacity, Motion, Lumetri (preset: Look=1, Intensity 100), Lumetri (old: Look=0)`.
   - My script assumed the new Lumetri was the last one (as on puja-night-2, where the layer had none) and set Creative Intensity 30 on the old, look-less Lumetri.
   - The first render was ~3–4× the 30 % preview (sat +0.15 vs +0.04, crush +9 % vs +0.8 %). Only the render check caught it; the read-back said "intensity 30".
2. **Lumetri's Creative Intensity mixes linearly** (the playbook's open assumption, §A3 step 4). With intensity on the right Lumetri, Premiere matched `look_preview.py`'s 30 % tile within 0.003 on luma, saturation and warmth, on two stills (v6 Premiere still vs v7 Premiere still, same frame):

   | still | | Δ luma | Δ sat | Δ R−B | Δ hue |
   |---|---|---|---|---|---|
   | 12.5 s (Coffee House, night interior) | preview | −0.0092 | +0.0396 | +0.0269 | −0.76° |
   | | Premiere | −0.0089 | +0.0375 | +0.0265 | −0.79° |
   | 74.6 s (Academy of Fine Arts, night) | preview | −0.0087 | +0.0945 | +0.0386 | −0.55° |
   | | Premiere | −0.0083 | +0.0925 | +0.0380 | −0.57° |

   Crush rose less in Premiere (+0.5 %) than in the preview (+0.8–1.0 %).
3. **The `Look` slot reads 1 after a preset**, not a stable id (the playbook already warns not to trust it). It was still the only reliable way to tell the two Lumetris apart, together with prop 32 (the look path string, empty on a look-less Lumetri).

## Workaround used in the reel
`analysis/_es_look_v7_fix.jsx`: loop over every `Lumetri Color` on the layer and set Creative Intensity (prop 38) only on the one whose `Look` (prop 34) is non-zero. The inherited Lumetri was neutralised (vignette 0) so the layer carries only the picked look.

## Proposed change
1. **effects-playbook §A3 "Premiere build" step 1 / reality doc:** after `applyLumetriPreset`, find the look's Lumetri by `Look != 0` (or a non-empty prop 32), never by position. Or prefer a fresh adjustment-layer instance with no Lumetri on it.
2. **Mark Eterna 250D → 3510 (preset) verified** in the film table, and mark "Creative Intensity mixes linearly" as verified (step 4), with the table above.

## HQ decision (v0.9.1, 2026-11-08)
- **(1) Done.** effects-playbook §A3 Premiere build step 1 and a reality-doc row: after `applyLumetriPreset`, find the look's Lumetri by `Look` ≠ 0 or a non-empty look path (prop 32), never by position; neutralise or avoid an inherited Lumetri.
- **(2) Done.** `eterna_3510` marked verified (kolkata, 30 %), and "Creative Intensity mixes linearly" marked verified in step 4 with this CR's numbers.
