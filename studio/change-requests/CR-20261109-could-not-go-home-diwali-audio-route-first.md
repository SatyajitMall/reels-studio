# CR-20261109-could-not-go-home-diwali-audio-route-first

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 |
| Type | skill |
| Severity | polish |
| Status | open |

## What happened
In Round 1 the director answered "30–45 s" for length, then said the soundtrack would be "an IG library song: the same as the reference's".

The reference's Instagram page (opened in Chrome from the link they gave) showed something else:
- the audio is **"Original audio" by howwdeep.exe** (300 reels use it), not a library song;
- the creator's reply in the comments names the song ("telephones – vacation");
- the original audio is only **20.8 s** long.

The director then chose to use that original audio, which caps the reel at about 21 s. The length answer from Round 1 no longer held, and the letter (the reel's words) had to be planned for ~20 s instead of 30–45 s.

The skill asks for length (Round 1 Q4) before the soundtrack (Q7) and checks the audio page in Phase 1, so the length answer was given without the audio's real length. Also: no step compares the guide copy's length with the target runtime.

## Workaround used in the reel
- Opened the reference link, read the audio page and the comments, and put the three routes to the director with their consequences: library version of the named song (full length), the creator's original audio (~21 s), or another song.
- The guide is the reference's own audio (`audio/guide_ref.wav`, stereo, 20.8 s), which is the whole original audio.
- Runtime target reset to ≈ 20.7 s and logged in `project.md`.

## Proposed change
1. **Skill Phase 0, Round 1:** when the soundtrack is existing IG audio, check the audio page *during* Round 1, before asking length, as soon as the director gives the reference link. Ask for the link with the references question.
2. **Skill Phase 1 step 4:** "Original audio" sets a hard runtime cap equal to its length. Write the guide's length next to the target runtime in `project.md`, and if the guide is shorter than the target, say so and offer the routes (library version of the song if one exists, the original audio at its length, another song).
3. **`instagram-strategy.md`:** a line on "Original audio" that is really a commercial song: library route vs reuse route, and that using another creator's audio needs their OK (director profile).

## HQ decision
<!-- HQ fills this in. -->
