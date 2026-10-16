# CR-20261016-my-reel-playbook-pilot-notes

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.2.5 |
| Type | skill · rule |
| Severity | polish |
| Status | done v0.3.1 |

## What happened
Smaller lessons from Phases 5–6 of the first pilot that aren't tool bugs:
1. **Grain shows at fades.** V4 grain in Overlay over a fading V1 becomes a visible grey veil on black (frame luma 0.24 instead of ~0). It has to fade with the picture.
2. **Speed ramp.** With this MCP, `speed_change 2.0` on a razored piece keeps its timeline duration and doubles the source span. The playbook §C recipe assumes the clip shortens. The working ramp was: razor → `speed_change` on part 1 → `slip_edit {deltaSeconds}` part 2 forward by the extra source used.
3. **Type without HyperFrames.** Kinetic words were rendered as 1080×1920 transparent PNGs with PIL (font, glow, shadow, safe-zone check from `getbbox()`), placed on V5, with a 3-frame scale pop by keyframe. Fast, predictable and easy to review. Anton / Bebas aren't installed by default; macOS has DIN Condensed Bold / Impact.
4. **End cards must avoid the subject.** The first end card covered Durga's face; check it over the actual outro frame.
5. **Branding question timing.** The handle and font were asked at the very end and arrived late.
6. **Manual-step phrasing.** The director needed explicit numbered steps for the one manual Premiere action.

## Workaround used in the reel
As above; all logged in `projects/my-reel/project.md`.

## Proposed change
- Playbook §A4: "Fade V4 texture together with V1 at every fade to/from black."
- Playbook §C speed ramp: replace with the razor → speed_change → slip recipe above (keep the old one as an alternative if the MCP changes).
- Playbook §E: add the "PIL PNG word cards" recipe (and a small `scripts/render_type_cards.py` taking words, font and y) as the default for 1–2-word kinetic type; HyperFrames for anything animated beyond a pop. List system font fallbacks for Anton/Bebas.
- Playbook §E: "Composite the end card over the real outro frame and check it clears faces / the main subject."
- Skill Phase 0 Round 1: ask handle / font / brand colours up front (store in project.md).
- Skill: any manual step for the director is a numbered list naming panel and menu path, ending "come back and say done".

## HQ decision
**Accepted, done in v0.3.1.** Changes: §A4 fade V4 with the picture; §C speed-ramp recipe replaced; §E PIL word cards via new `scripts/render_type_cards.py` (safe-zone guard, DIN Condensed fallback), plus the end-card-over-outro check. Skill Phase 0 asks branding in Round 1, and only if `studio/director-profile.md` doesn't answer it. The new director profile holds the handle @satyajitmall, type style and working preferences. Manual steps are always a numbered list ending in 'come back and say done'.
