# CR-20261020-uski-aankhein-director-profile

| Field | Value |
|---|---|
| From reel | `projects/uski-aankhein/` |
| Arch version | 0.6.0 |
| Type | rule · template |
| Severity | polish |
| Status | done (v0.9.0) |

## What happened
1. **Footage location.** The session brief said raw videos sit under `~/Documents/videos`. They're actually under `~/Documents/Video ` (trailing space), one folder per shoot day:
   - `Puja 2026 Oct 15/Media`, `Puja 2026 Oct 16/Media` (clips inside `Media/`);
   - `Pujo 2026 Oct 17 ` and `Puja 2026 Oct 18 ` (trailing spaces in the names);
   - `Pujo 2026 Oct 19`, `Pujo ki Sobar `, `Uski Ankehe`.

   Each has a `Proxy/` and sometimes a `Reffernce`/`Refference` folder. The director names a reel folder there and drops the reference reel in it.
2. **Clip ids collide across shoots.** The Blackmagic counter restarted: Oct15 and Oct19 both have C001–C032. A bare "C012" is ambiguous, so the shoot must always be named.
3. **Stock footage.** The profile says "no outside stock footage". For this reel the director asked for a stock bowed-string player and picked one from Pexels after watching 4 candidates. So the rule is a default, not a ban.
4. **Reference audio as the soundtrack** is now the director's habit: the third reel in a row uses it (puja-night-2, pujo-ki-asolei-sobar, uski-aankhein). The upload pattern is a `_mix` guide plus a muted `_IG` export, with the IG audio added at upload (see CR-20261018-puja-night-2-commercial-music-ig).

## Workaround used in the reel
- Listed `~/Documents/Video `, quoted every path.
- Named clips as `Oct17:C168` everywhere: survey, EDL, brief.
- Logged the stock clip as a per-reel brief override, with its licence and source in `raw/SOURCES.md`.

## Proposed change
`studio/director-profile.md`:
- **Footage:** "Raw footage: `~/Documents/Video /<shoot or reel folder>/` (note the trailing spaces in some folder names; Oct15/16 clips are under `Media/`). References: a `Ref*rence` subfolder, or the reel's own folder there. Clip ids repeat across shoots: always say `<shoot>:<clip>`."
- **Stock:** change "No outside stock footage" to "Own footage first. Stock only when the director asks: free licence (Pexels / Pixabay), the director picks it after watching, logged in `raw/SOURCES.md`, used as a layer or bridge, never for the subject."
- **Music:** add "Usually cuts to the reference reel's own audio and adds the IG library track at upload. Ask for the IG track name and start point at Checkpoint 1."
- **Content so far:** add puja-night-2, pujo-ki-asolei-sobar and uski-aankhein rows.

## HQ decision (v0.9.0, 2026-11-04)
**Accepted, v0.9.0.** `studio/director-profile.md` now has the footage location (quoted paths, trailing spaces, `Media/` on Oct 15–16, references in a `Ref*rence` subfolder), clip numbers named with their shoot (`Oct19:C012`), stock footage only on the director's ask (free licence, the director picks, logged in `raw/SOURCES.md`, never the subject), the existing-audio habit (guide copy, `_mix` + `_IG`, the audio page checked in Phase 1), and content rows for puja-night-2, pujo-ki-asolei-sobar, uski-aankhein and goddess. Making the tools key clips by shoot is Batch C item 19.
