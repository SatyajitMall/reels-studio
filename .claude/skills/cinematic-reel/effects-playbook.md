# Effects & Colour Playbook

Named moves the editor can propose in the brief's **Treatment** section. Every recipe uses Premiere Pro MCP tools. Effect names can differ between Premiere versions and languages, so check them once per session with `list_available_effects` and `list_available_transitions`.

**Golden rule:** Premiere's scripting API can't remove an effect once it's added. Plan what goes on each clip before applying anything, and change existing effects with `set_effect_property` instead of adding new ones. Check what's on a clip with `list_clip_effects` / `get_effect_properties`.

---

## A. Colour (three stages, always in this order)

### A1. Primary correction: per clip, on the clip itself
Goal: neutral, correctly exposed footage with natural skin.
- Read `analysis/summary.md` and look at each `contact.png` first.
- Call `color_correct` **exactly once per clip**. Every call adds a *new* Lumetri effect, and it can't be removed. Pass every value in that one call: exposure → `brightness`, `contrast`, `highlights`, `shadows`, `temperature`, `tint`, `saturation`.
- Need to fine-tune later? Use `set_effect_property` on that same Lumetri. Never call `color_correct` again on that clip.
- Starting points from the analyser:
  - exposure < 0.30 → brightness +15…+30, shadows +10…+20
  - "flat / log-like" → contrast +20…+35, saturation +10…+20 (or the camera's log→Rec709 LUT, applied once as the clip's only Lumetri via `apply_lut`)
  - warm cast → temperature −10…−25; cool cast → temperature +10…+25
  - green tint → tint +5…+15 (toward magenta); magenta tint → tint −5…−15
  - clipped highlights → highlights −20…−40
- Clips shot on the same setup: correct one, then `copy_effects_between_clips` to the rest.

### A2. Shot matching
Re-run `scripts/analyze_footage.py` on a frame export, or compare contact sheets. Adjacent shots should land within about ±0.04 exposure and ±0.03 warm/cool of each other. Tweak with `set_effect_property`.

### A3. Creative look: V3 adjustment layer only
`add_adjustment_layer` across the reel, then on that layer:
- `apply_lut` with a LUT from `assets/luts/`, then lower intensity / Lumetri "Look intensity" to 40–80 % via `set_effect_property`
- `color_correct` once for the look's contrast / saturation / split-tone direction
- vignette via the Lumetri vignette properties (`set_effect_property`), amount −0.5…−1.5

Look presets to propose:
| Name | Recipe |
|---|---|
| **Warm Film** | warm LUT (Kodak 2383-style) 60 %, contrast +15, saturation −10, temp +8, soft vignette, grain on V4 |
| **Teal & Orange** | contrast +20, push shadows teal / highlights orange via LUT, skin kept natural, saturation +5 |
| **Moody Desat** | saturation −30, contrast +25, temp −8, crushed blacks (shadows −15), heavy vignette |
| **Clean Bright** | exposure +5, contrast +10, saturation +10, no grain: creator / lifestyle look |
| **Mono Drama** | `Black & White` on the adjustment layer, contrast +30, grain heavy |
| **Match Reference** | measure the reference with the analyser, mirror its exposure / contrast / warmth numbers |

### A4. Texture: V4 overlays
Grain, dust, light leaks and film burns from `assets/overlays/` go on V4 with `set_blend_mode`:
- grain → Overlay or Soft Light, `set_clip_opacity` 15–35 %
- light leaks → Screen, 40–80 %, on transitions or emotional beats
- film burn / flash → Screen or Add, 3–8 frames, on hard cuts

---

## B. Motion on V1 (the talking head)

| Move | Recipe | Use for |
|---|---|---|
| **Punch-in** | razor at an emphasis word, Motion Scale 100→108 % on the second half (hard, no keyframe) | stressing a key word, hiding a jump cut |
| **Slow push** | `add_keyframe` Scale 100→106 % over the shot, `set_keyframe_interpolation` ease | hook, emotional lines |
| **Snap zoom** | Scale 100→125 % in 4–6 frames, ease-in | punchlines, reveals |
| **Impact shake** | Transform / Position keyframes ±12 px over 6 frames, decaying | bass hit, "boom" moments |
| **Reframe** | `set_clip_position` + `set_clip_scale` to keep eyes on the upper third | horizontal source in 9:16 |
| **Split-screen** | `crop_clip` + `set_clip_position` on V1/V2 | before/after, comparisons |

## C. Time

| Move | Recipe | Notes |
|---|---|---|
| **Slow-mo B-roll** | `speed_change` 0.4–0.8 + `set_frame_blend` (Optical Flow) | only if source fps ≥ 50 (see analyser "Slow-mo") |
| **Speed ramp** | razor the clip into 3 parts: fast (1.5–3×) → slow (0.4×) → fast. `speed_change` each part, then a short Cross Dissolve or Dip between parts | real time-remap curves aren't scriptable; this fakes it convincingly |
| **Freeze + text** | `freeze_frame` on the beat, then a title / HyperFrames card on top | "this is me 2 years ago" moments |
| **Rewind** | `reverse_clip` 0.3–0.6 s + rewind SFX | callbacks, "wait, go back" |
| **Stutter** | razor 3–4 identical 2-frame slices back-to-back | beat drops |

## D. Transitions (between shots)

Default is a **hard cut**. Transitions are seasoning: at most 3–4 non-cut transitions per 30 s.
| Move | Recipe |
|---|---|
| **Flash cut** | `add_transition` Dip to White, 2–4 frames, + camera-click SFX |
| **Whip / zoom blur** | outgoing clip: Transform scale 100→140 % + Directional / Gaussian Blur ramp over the last 5 frames; incoming: reverse; + whoosh SFX |
| **Light-leak dissolve** | Cross Dissolve 8–12 frames + light-leak overlay on V4 in Screen mode |
| **Match cut** | cut on matching shape or motion between clips (planned in the EDL, not an effect) |
| **Glitch hit** | `VR Digital Glitch` (or RGB-split via Offset) for 3–6 frames + glitch SFX |
| **Blur reveal** | Gaussian Blur 60→0 over 10 frames at the start of a section |

## E. Type, graphics, captions (V5 + V2)

- Captions: phrase-aware, 2–4 words, safe zone (clear of top 220 px, bottom 320 px, right 120 px). Styles: *Clean* (white, subtle shadow), *Bold Kinetic* (key word highlighted in brand colour, pop-in), *Editorial* (serif, lower-third). Use `/embedded-captions` for animated styles, `create_caption_track` for clean ones.
- HyperFrames cards (`/motion-graphics`): stat callouts, lists, step numbers, maps, quotes. Render 1080×1920 alpha `.mov` → `renders/overlays/`.
- Text behind subject: only when the subject is cleanly separable. Propose it, and warn that it's a HyperFrames / manual roto job.

## F. Sound design (A2 / A3)

| Moment | SFX |
|---|---|
| Hook / title | riser into sub-hit |
| B-roll entrance | soft whoosh |
| Punch-in / snap zoom | short swish or tick |
| Text pop | click / pop |
| Flash cut | camera shutter |
| Emotional turn | music drops out for 0.5–1 s (silence is an effect) |

Music: cut on the beat for section changes, duck under speech, last note lands on the final frame.
