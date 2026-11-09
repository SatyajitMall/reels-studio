---
name: film-emulation-prompts
description: |
  Write the light and colour part of the prompt for an AI-generated shot in the reels studio (scripts/gen_video.py, Veo 3.1), so the shot arrives looking like the director's own ungraded footage and the reel's V3 film look grades it like every other clip. Maps each look id in the effects-playbook §A3 film table to what to describe in the prompt and what to leave out (no film-stock names, grades, grain or halation in the prompt). Use only after the brief has approved an AI shot (motion-and-ai.md §3). Not for grading, look previews or picking a look: those are effects-playbook §A3, look_preview.py and Premiere.
---

> **Studio version** of the `color_grading_film_emulation` skill (0xzgbot / Hermes Agent, MIT; `LICENSE` in this folder), written by HQ on 2026-10-30 (studio v0.7.4). The original is prompt vocabulary for grading AI images toward a film stock. This version keeps its idea of describing light, shadow tint and highlight roll-off. It drops the grading:
> - **This studio grades in Premiere.** An AI shot goes through the same correct → look → texture chain as the director's clips. A grade baked into the prompt would get the look twice.
> - **Popular film-stock lore isn't what the stocks do on our footage.** The original says Vision3 500T has "cool blue-black shadows" and Eterna is "pastel". Our measured `k500t_2383` moves hue +1.5° toward gold with deep blacks, and `eterna_3510` is the *most* saturated look in the table (+0.063).
>
> **Untested:** no studio AI shot has been made with this skill yet. The first reel to use it reports in a CR: the prompt, the draft's numbers against its anchor still, and whether it needed a re-prompt. HQ then marks it verified here.

## Studio rules (read first)
1. **Only for an AI shot the brief already approved**, under every rule in `motion-and-ai.md` §3:
   - only when the footage can't provide the shot;
   - never the idol or the people;
   - never proof;
   - within the caps, with the director's yes before each paid run.

   This skill writes part of the prompt. It never approves a run.
2. **Describe the scene as the director's camera would record it, ungraded.** The reel's look (V3) and grain (V4) are added in Premiere, on the AI shot like on every clip (CLAUDE.md §2.5 and §3). A look baked into the prompt gets the look twice.
3. **Never put in the prompt:**
   - film-stock or print names (Kodak, Fuji, Vision3, 2383, CineStill, Ektachrome…);
   - grade words ("colour graded", "teal and orange", "bleach bypass", "film look", "LUT", "desaturated", "muted", "vintage");
   - "film grain", "halation", "bloom", "glow", "letterbox", "anamorphic";
   - a lone "cinematic". Veo tends to read it as a grade plus bars; name the framing and the move instead.

   Put the effects you don't want in `--negative` (below).
4. **The first-frame still is the strongest colour anchor** (verified 2026-10-18: frame 0 matched the still to 0.6/255). When you use one, the prompt's light must agree with it: same light source, same time, same white balance.
5. **Check the draft by numbers before the final** (below), then conform it with `conform_clip.py --match <still>` and grade it in Premiere like any clip.
6. **Words Veo takes literally** (kolkata, 2026-11-07):
   - Never name what a sign, board or label says ("route number board", "shop sign"): Veo writes the word (a board reading "ROUTE" with invented numbers). Ask for a "plain" or "blank" board and add "readable words" to `--negative`.
   - Regional objects need a visual description, not a name: "a yellow Ambassador taxi" came out as a New York checker cab. Better still, leave them out and let the real neighbouring shot carry them.

## The prompt's light and colour block
`gen_video.py --prompt` = the shot (subject, action, framing, move, from the brief) followed by this block:

```
Filmed on a phone held vertically, [13 / 26 / 52] mm lens, 4K, 9:16, [handheld with light
stabilisation | locked off], one slow [push-in / pan / tilt]. [LIGHT: source, direction,
colour in plain words, from the table below]. Natural colour and white balance for that light,
normal contrast, dark shadows that keep detail, bright lights that keep detail, clean image,
no text.
```

`--negative` (always, plus the shot's own, such as "faces, people" from the brief):
```
colour grade, teal and orange, film grain, noise, halation, glow, lens flare, letterbox, black bars,
vignette, faded blacks, oversaturated, text, watermark
```
`--negative` reaches Veo as `negativePrompt` on both providers (`gen_video.py`).

### Light, as the director's footage records it
Pick the row that matches the shots the AI shot sits between. Check those shots' numbers in `analysis/` (`colour_report.py` or `analyze_footage.py`) rather than guessing.

| Scene in our footage | Describe the light as | Notes |
|---|---|---|
| Pandal interior, night | "warm tungsten lamps and strings of small bulbs overhead, golden light on the idol, deep shadows at the edges" | Many pandal clips were set to 5600 K and came out orange (93 of 123 such clips on the Pujo 2026 nights). Per-clip correction neutralises them, so ask for natural colour, not "orange" |
| Pandal exterior / street, night | "mixed white LED and warm bulb light, dark sky, light falling off into the street" | Coloured LED arches: name their colours plainly ("blue and pink LED arches") |
| Sodium street / bridge, night | "orange sodium street lamps, dark blue sky" | Strongly mono-orange; the per-clip correction tames it |
| Oil lamps, diyas, aarti | "small flames as the only light, warm, faces lit from below" (no faces in AI shots: light the object) | Point lights for `cinestill` (below) |
| Daylight street | sunny: "low afternoon sun from the side". Overcast: "a hazy overcast afternoon, no direct sun, a soft white-grey sky", with "bright sunshine, blue sky, hard shadows" in `--negative` | 5600 K footage is close to neutral here. **"Soft daylight under light cloud" came out as bright sun and a blue sky** (kolkata draft 1); the overcast wording fixed it in one draft. Overcast gives a pale, neutral, partly clipped sky, so a warm hazy anchor still needs `conform_clip.py --match` and the Premiere primary. Untested candidate for warm haze: "late-afternoon haze, the sky a small pale strip between treetops" |
| River ghat at dusk (Dashami) | "blue dusk sky, last light on the water, a few warm lamps on the bank" | Mixed cool and warm. Don't call it "golden hour" unless the anchor still is |

Camera words that match the footage: phone, 13 / 26 / 52 mm, 4K vertical, Rec.709, 25 fps. Veo outputs 24 fps; `conform_clip.py` retimes it. Many night clips are ISO 1000+ and noisy (75 of 329), but ask for a **clean** image: grain comes from V4, and Veo noise doesn't match ours.

## By the reel's look (effects-playbook §A3 film table)
The brief names the look. Give that look a scene it lands well on, and leave out what it already adds. The "look adds" column is our measured character at the table's intensity.

| Look id | Look adds (measured) | Ask the prompt for | Leave out of the prompt |
|---|---|---|---|
| `k500t_2383` | Contrast +0.035, warmth +0.018, hue +1.5° toward gold, deep blacks, highlight roll-off | Correctly exposed night, practical lights that keep detail, normal contrast | "golden grade", "teal shadows", crushed blacks |
| `k500t_2395` | **Lifts blacks** (crush → 0 %), brighter, softer | Full, deep blacks; normal exposure | "faded", "matte", "lifted blacks", "soft" (it would fade twice) |
| `k250d_3510` | Clean and warm, sat +0.027, warmth +0.034 | Neutral daylight, true white balance | "warm", "golden" |
| `f125_2393` (Warm Film) | Darker, sat +0.051, warmth +0.048, **hue toward red**, crush 7.4 % | Shadows with detail, moderate saturation, neutral or slightly cool skin and gold | "red", "orange", "warm tint", "dark", "moody" |
| `f125_2395` | **Strongest red push**, lifted blacks | Neutral colour, deep blacks | "warm", "red", "faded" |
| `eterna_3510` | **Most saturated** (+0.063), warm (+0.060) | Natural, moderate saturation | "vivid", "vibrant", "rich colour", "saturated" |
| `eterna_2395` | **Brightest** (+0.039), lifted blacks | Normal exposure, deep blacks | "bright", "airy", "soft", "faded" |
| `reala_2393` | Sat +0.060, warmth +0.057, crush 7.2 % | Moderate saturation, shadows with detail | "vivid", "punchy", "dark" |
| `mono_500t`, `mono_eterna` | B&W, applied in Premiere | **Colour**, with clear tonal separation (light against dark). The B&W conversion needs colour to work with, and the shot keeps its option | "black and white", "monochrome" |
| `cinestill` | 500T plus a **red halation bake** around point lights (ffmpeg, per shot, before Premiere) | Bare bulbs or flames **against a dark background**, in the frame | "halation", "bloom", "glow", "lens flare": the bake adds it, so a second bloom would double |
| `bleach` | Contrast +0.094, sat −0.113, cooler | Normal contrast and colour | "gritty", "desaturated", "metallic", "high contrast" |
| `muted_red` | Keeps hues within ±T° of red (the brief's tolerance, 45 on gold footage); all others at 46 % saturation | **The reds and gold the story needs, clearly in the frame**: sindoor, red-bordered saris (no faces), red lights, gold. Everything else in natural colour | "muted", "desaturated", "selective colour", "only red": the Hue vs Sat curve does it in Premiere |

## Check the draft before the final
A draft is ≈ $0.12, and a shot gets at most 3 drafts. Measure the draft before asking for the final, so a baked-in look is caught early.
1. Measure the draft from 1 s on, after Veo's settle-in. Measure the neighbouring shot's source clip over the range the EDL uses, or the anchor still's clip around its time. `colour_report.py` takes a video plus a `--shots` JSON of `[name, start_s, end_s]`:
   ```
   ./.venv/bin/python scripts/colour_report.py projects/<reel>/renders/gen/<shot>_draft_<time>.mp4 \
       -o projects/<reel>/analysis/colour_<shot>_draft.json --shots <draft_range>.json
   ./.venv/bin/python scripts/colour_report.py raw/b-roll/<neighbour>.mov \
       -o projects/<reel>/analysis/colour_<shot>_anchor.json --shots <anchor_range>.json
   ```
2. Compare the two reports against the shot-matching tolerances (effects-playbook §A2): luma within ±0.04, warm/cool within ±0.03.
3. Look for a baked look:
   - p02 > 0.06 means lifted blacks;
   - shadows clearly teal, or highlights orange, against the anchor;
   - visible grain on the contact sheet;
   - black bars.
4. **If the draft has a baked look, re-prompt.** Remove the word that caused it and add it to `--negative`. Don't fight it in Premiere, where a correction can't fully undo a look.
5. Record the prompt, the negative and the numbers in `project.md`. The first reel to use this skill copies them into its CR (see the top of this file).

## Example (night pandal reel, `k500t_2383`, no faces)
```
--prompt "Slow push-in toward a pandal entrance made of carved white thermocol arches at night,
marigold strings hanging at the sides, no people. Filmed on a phone held vertically, 26 mm lens,
4K, 9:16, handheld with light stabilisation, one slow push-in. Warm tungsten lamps and strings of
small bulbs overhead, golden light on the arches, deep shadows at the edges. Natural colour and
white balance for that light, normal contrast, dark shadows that keep detail, bright lights that
keep detail, clean image, no text."
--negative "people, faces, colour grade, teal and orange, film grain, noise, halation, glow,
lens flare, letterbox, black bars, vignette, faded blacks, oversaturated, text, watermark"
```
