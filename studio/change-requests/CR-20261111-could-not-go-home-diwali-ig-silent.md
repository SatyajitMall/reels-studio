# CR-20261111-could-not-go-home-diwali-ig-silent

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.10.2 |
| Type | script |
| Severity | polish (a false FAIL on the upload file) |
| Status | open |

## What happened
The director chose to add the soundtrack in Instagram (library song) at upload. This is a `music-montage` reel, and its natural sound was muted from v3b on (CLAUDE.md §4c allows "muted or ≤ −20 dB"). So the `_IG` file carries a silent stereo track.

`scripts/verify_render.py <reel>_v3f_IG.mp4 --profile ig-quiet --allow-black 28.56-30.76` gives:

```
FAIL  audio present        silent
```

The `ig-quiet` profile assumes quiet natural sound under the music Instagram adds. A deliberately silent upload has no way through.

## Workaround used in the reel
- The `_IG` file was accepted with that single FAIL, after checking that every other check PASSes or WARNs. It's logged in `project.md`.
- The `_mix` (guide baked in, archive only) PASSes.

## Proposed change
- `verify_render.py`: add `--silent-ok` (or a profile `ig-silent`) for music-montage uploads whose natural sound is muted by design. It passes when the track is silent, and still checks that the track exists, its length and its layout.
- `pregate.py` passes the flag through when the brief's reel type is `music-montage` and the audio route is "added in Instagram".

## HQ decision
<!-- HQ fills this in. -->
