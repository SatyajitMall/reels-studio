# Director profile

Standing preferences that apply to every reel. Reel sessions **read `studio/director-profile.md` in Phase 0** and don't ask again for anything already answered there. They pre-fill it into `brief.md`, and the director can override it per reel. HQ owns the file: a reel session that learns something new about the director files a CR, and HQ updates it.

**This is the blank template.** `setup.sh` copies it to `studio/director-profile.md`, which is git-ignored: it holds one person's handle, camera folders and taste, so it stays on their Mac. Fill it in as the first reels teach the studio, or leave a row as "not set yet (ask once)".

## Branding
| Field | Value |
|---|---|
| Instagram handle | not set yet (ask once) |
| Type style | not set yet (ask with a type sheet in Phase 0) |
| Type colour used | not set yet |
| Brand colours | not set yet (ask once, then record here via a CR) |

## Camera
What the ingest check (`scripts/ingest_report.py --scan`) found about the director's camera and app settings:
- Camera, app, codec, bit depth, colour space (log or Rec.709), usual frame rate and shutter.
- Where the clips live on disk, and how shoots and clip numbers are named.
- Anything the footage needs every time (rotation, depth bake, flicker under mains lamps).

See `studio/shooting-guide-blackmagic-cam.md` for the settings the studio recommends.

## Instagram
- How the director credits AI tools in captions, if at all.
- Collab invites, Story shares, hashtag style: what they do and don't want suggested.
- Whether they cut to Instagram library audio added at upload (then the edit uses a guide copy; CLAUDE.md §4c).
- Who taps Share (always the director).

## Taste
Notes that held across reels, each with the review note that taught it, for example:
- how processed the picture may look (the default grade is camera-true, effects-playbook §A0);
- where cuts land (on words, on beats);
- how literally the picture should show the words or lyrics;
- transitions, sound effects and type they like or have rejected.

## Working preferences
- Where they judge cuts (phone or Mac) and how review copies reach them.
- Own footage first, or stock allowed; which stock licences.
- How they like choices presented (a recommendation with numbers, multiple choice).
- AI-generated footage: allowed or not, budget caps, approval per paid run (`.claude/skills/cinematic-reel/motion-and-ai.md`).

## Content so far
| Reel | Subject | Type | Look | Length |
|---|---|---|---|---|
| | | | | |
