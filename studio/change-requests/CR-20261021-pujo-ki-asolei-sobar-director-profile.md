# CR-20261021-pujo-ki-asolei-sobar-director-profile

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | template (studio/director-profile.md) |
| Severity | polish |
| Status | done (v0.9.0) |

## What happened
New, repeated preferences from this reel (8 director note rounds), not yet in `studio/director-profile.md`:
1. **Pictures change on the words** in any VO-driven reel: cut on sentence / clause onsets, never in pauses (3 rounds lost before this was explicit).
2. **Depiction must match the narration literally**, one subject per voice or idea ("cut and depiction not accurate", "go through the narration and fit accordingly").
3. **Deity shots only with a narrative reason.** In a people-led reel, the Devi opens it (aarti) and otherwise stays out ("too many shots of the Durga unnecessarily").
4. **One grade across shots lit differently** (blue, green, orange light): neutralise each shot first, then one look.
5. **"Cinematic" means correction, stability and clarity**, not synthetic effects. Synthetic bokeh was asked for, then rejected as unconvincing; stabilised, denoised, sharpened footage was accepted ("for now finalise it").
6. For this reel's subject (working men at Pujo), a **very sepia, filmy** look was chosen. Treat that as reel-specific, not a brand default.
7. The director shoots **4K vertical on Blackmagic Cam (iPhone)**, often variable frame rate, across several dated folders named `Puja/Pujo <date>` under `~/Documents/Video /` (some with trailing spaces).
8. The director wants **copies, not links**, of chosen clips in the reel folder.
9. A commercial or another creator's audio is fine as a **guide**, with IG audio at upload (`_mix` + `_IG` exports).

10. **Vary the people (round 9):** "again we are choosing the same set of people a few many times". One subject per line, never the same person twice unless it's a deliberate callback. (This supersedes my round-1 reading of item 2 as "one man carries every 'first' line".)
11. **Slow motion for drama (round 9):** asked for at emotional lines, but the whole pool is 24–30 fps. Profile note for the shoot: film moments that may be slowed at 60 fps (Blackmagic Cam supports it), and at 1/100 s under 50 Hz lamps (see CR-20261023-pujo-ki-asolei-sobar-mains-flicker).

## Workaround used in the reel
Applied each preference once the director stated it; logged in `projects/pujo-ki-asolei-sobar/project.md`.

## Proposed change
Add items 1–5, 7–11 to `studio/director-profile.md` → "Working preferences" (6 under "Content so far" as this reel's look). Add a row to "Content so far": pujo-ki-asolei-sobar | working men behind Pujo, Hindi VO | hybrid (external VO) | sepia film, stabilised | 35.8 s.

## HQ decision (v0.9.0, 2026-11-04)
**Accepted, v0.9.0.** Items 1–5 and 7–11 are in `studio/director-profile.md` (a new "Taste" section and "Working preferences"); item 6, the sepia look, is in this reel's content row as reel-specific. Item 1 (pictures change on the words) is also CLAUDE.md §4b's cut rule and a reviewer check; item 8 (copies, not links) says to copy the shortlist until `link_footage.sh` gets a copy mode (Batch C).
