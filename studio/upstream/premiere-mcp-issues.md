# Draft upstream issues: hetpatel-11/Adobe_Premiere_Pro_MCP

**Status: draft, not filed.** Filing publishes to GitHub, so the director decides whether and when to post these, and from which account. Environment for all of them:
- macOS, Premiere Pro 26.5.2 (build 5)
- adobe-premiere-pro-mcp 1.2.9, CEP bridge
- `PREMIERE_MCP_TOOLSET=full`

Found in the `my-reel` pilot on 2026-10-16. The workarounds are in `.claude/skills/cinematic-reel/premiere-mcp-reality.md`.

## 1. Import: `import_folder` fails for every file; `import_media` ignores `binName`
- `import_folder` → `ReferenceError: targetBin.importFiles is not a function` (77/77 files).
- `import_media {binName}` succeeds, but the item lands in the project root.
- Works: `app.project.importFiles(paths, true, targetBin, false)`.

## 2. Delete: `delete_multiple_project_items` crashes; `delete_project_item` gives a false success
- `delete_multiple_project_items {itemIds}` → `deleteResults.filter is not a function`.
- `delete_project_item` on footage → `{"deleted":true,"method":"deleteBin"}`, but the item remains.
- Works: move the items into a temp bin, then `deleteBin()`.

## 3. `execute_extendscript` / `evaluate_expression` never return the script's value
- Both always return `"undefined"` / `{type:"undefined"}`.

## 4. `export_frame` with `format:"png"` → `Error: Illegal Parameter type`
- It works when `format` is omitted.

## 5. `color_correct` writes only contrast / temperature / tint; `saturation` turns the clip black and white
- `brightness`, `highlights` and `shadows` are ignored.
- `saturation: -8` sets Basic Saturation to 0 (its range is 0–200, 100 = neutral) and also zeroes Creative Saturation.

## 6. `set_effect_property` matches only the first property with a given name
- Lumetri has 3 × "Saturation", 2 × "Intensity" and 2 × "Contrast". There's no way to target the others.

## 7. `add_adjustment_layer` creates a transparent PNG, not an adjustment layer
- It writes `/tmp/premiere-mcp-bridge/generated-assets/adjustment-layer-*.png` at 1920×1080, 5 s.
- Effects on it don't affect lower tracks.

## 8. `apply_lut` reports success but loads nothing
- The Input LUT and Look stay empty, and the frame is unchanged.
- `applyLumetriPreset(<built-in>)` works.

## 9. `set_blend_mode` → `Illegal Parameter type`
- Setting `Opacity.properties[1]` with the alphabetical enum works (Normal 18, Overlay 19, Screen 22, Soft Light 23).

## 10. `add_transition` / `add_transition_to_clip` land one cut off
- `add_transition {clipId1:A, clipId2:B}` lands at the end of B.
- `add_transition_to_clip {clipId:X, position:"end"}` lands at the end of the clip before X.
- Both return `accepted_unverified`.
- Looks like a QE item-index off-by-one.

## 11. `set_clip_volume {volumeDb}` writes a linear 0 (silent)
- Premiere's Level is linear (0.17783 = 0 dB), so the dB value needs converting: `Level = 10^((dB − 15) / 20)`.

## 12. `slip_edit` ignores `offset`; only `deltaSeconds` works
- Either accept both, or document `deltaSeconds`.

## 13. `razor_timeline_at_time` with `audioTrackIndices: []` cuts every audio track
- An empty array should mean "none".

## 14. `get_encoder_presets` finds no factory presets
- The presets exist under the app bundles' `Settings/IngestPresets/Transcode/` and AME `MediaIO/systempresets/`.

## 15. (Unconfirmed: cause unknown) `exportAsMediaDirect` exports silent audio
- With two built-in presets, the picture is correct but the AAC is −91 dB, even though the tracks are unmuted and the levels verified.
- The sequence was created with `create_sequence_from_clips`, and the music is an MP3.
- Needs a minimal repro before filing.
