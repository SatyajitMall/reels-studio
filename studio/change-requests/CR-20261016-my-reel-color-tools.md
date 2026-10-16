# CR-20261016-my-reel-color-tools

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.2.5 |
| Type | harness · rule |
| Severity | blocker (look layer) · workaround (rest) |
| Status | done v0.3.1 |

## What happened
Premiere 26.5.2, adobe-premiere-pro-mcp, Phase 4 colour:
1. `color_correct {brightness, contrast, highlights, shadows, saturation, tint}` writes only Contrast, Temperature, Tint. Brightness, Highlights, Shadows are ignored. Saturation −8 lands as 0 (Lumetri Basic saturation is 0–200, 100 = neutral) and the Creative-section Saturation is also set to 0 → the clip renders **black & white**.
2. `set_effect_property {componentName:"Lumetri Color", propertyName:"Saturation"}` hits only the first of Lumetri's three "Saturation" properties.
3. `add_adjustment_layer` creates `/tmp/premiere-mcp-bridge/generated-assets/adjustment-layer-*.png` (transparent PNG, 1920×1080, 5 s). Effects on it don't grade lower tracks, so CLAUDE.md §2.5 / §3 V3 "creative look on the adjustment layer" can't be built by script. ExtendScript `app.project` has no adjustment-layer method (checked via `reflect.methods`).
4. `set_blend_mode` → `Error: Illegal Parameter type`.
5. Script results are always `"undefined"`.
6. `apply_lut {lutPath: assets/luts/gemini_warm_film_2383.cube, intensity:50}` → success, but the Lumetri's Input LUT / Look stay empty and the frame is unchanged. Custom `.cube` files can't be loaded by script.

## Workaround used in the reel
- Per clip: `color_correct` with contrast/temperature/tint only (creates the one Lumetri), then `execute_extendscript` sets Exposure (stops), Highlights, Shadows, Basic Saturation (0–200) and Creative Saturation = 100, matching by property occurrence.
- Blend Mode is `Opacity.properties[1]`, enum alphabetical: Color 0, Color Burn 1, Color Dodge 2, Darken 3, Darker Color 4, Difference 5, Dissolve 6, Exclusion 7, … Lighter Color 12, … Multiply 17, **Normal 18, Overlay 19**, Pin Light 20, Saturation 21, Screen 22, Soft Light 23 (18/19/23/6/12 verified by render).
- Read script output by writing to a file (`new File(path).write(...)`) and reading it with Bash.
- LUT: `app.project.applyLumetriPreset("Fuji F125 Kodak 2393 (by Adobe)")` on the selected adjustment-layer clip (adds its own Lumetri; then set Creative Intensity = properties[38]). 325 built-in presets via `getAllLumetriPresetsList()`.
- Adjustment layer: director makes it once via File > New > Adjustment Layer; the reel places it with `add_to_timeline`.

## Proposed change
1. Report 1–5 upstream.
2. Playbook §A1: document the Lumetri units (Exposure in stops, Saturation 0–200 with 100 neutral) and the `color_correct` + script recipe until fixed; never pass `saturation` to `color_correct`.
3. Playbook §A3 + skill Phase 4: "Ask the director to create one Adjustment Layer (File > New > Adjustment Layer, sequence settings) at the start of colour", or add it to `projects/_template/` as a pre-made 1080×1920 25/30 fps item in a template `.prproj`.
4. Playbook §A3: map each look to a built-in Adobe preset name as the scriptable fallback (Warm Film → "Fuji F125 Kodak 2393 (by Adobe)"), since starter `.cube` LUTs can't be applied by script.
5. Add the blend-mode enum table to playbook §A4.
6. Add a `scripts/` helper or doc snippet for "ExtendScript → file → read" so reel sessions can verify script edits.

## HQ decision
**Accepted, done in v0.3.1 (apart from 3b).** Lumetri units and the `color_correct` + script recipe are in playbook §A1 and the reality doc. The adjustment layer is a single numbered manual step (reality doc, skill Phase 4). Built-in preset fallback in §A3: Warm Film → `Fuji F125 Kodak 2393 (by Adobe)`; the other looks get mapped as reels verify them. Blend-mode enum is in the reality doc and §A4. The ExtendScript→file→read pattern is Rule 2 of the reality doc. **Deferred (backlog):** a template `.prproj` with a pre-made adjustment layer, which needs Premiere UI work.
