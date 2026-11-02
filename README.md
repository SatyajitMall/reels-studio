# Cinematic Reels Studio

You direct, Claude edits, in Adobe Premiere Pro. You drop in your clips, answer a few questions and share references. Claude **writes the brief**, then turns the clips into a fully treated cinematic 9:16 Instagram Reel, never just cuts stitched together. Every reel gets:
- colour correction per clip and matching between shots;
- a camera-true grade, plus a creative look or film texture when you pick one;
- punch-ins and camera moves;
- speed ramps and transitions;
- graphics and captions;
- sound design.

## One-time setup (≈15 min)

1. Open **Terminal**, `cd` into this folder, then run:
   ```bash
   bash setup.sh
   ```
   This installs the Premiere MCP bridge, ffmpeg, the transcription tools, and the HyperFrames and Instagram skills.
2. Put your ElevenLabs API key in `.env` (`ELEVENLABS_API_KEY=...`). Transcription needs it for word-accurate cuts.
3. In **Premiere Pro** (one time):
   - Settings → Plugins → turn on **UXP developer mode**, then restart Premiere
   - Window → Extensions → **MCP Bridge (CEP)**
   - Set Temp Directory to `/tmp/premiere-mcp-bridge` → **Save Configuration** → **Start Bridge** → **Test Connection**
4. Quit and reopen the Claude app.

## How the studio runs: HQ + one session per reel

- **HQ session** (`/studio-hq`): one chat that owns the architecture. It covers the rules, skills, scripts, hooks and templates.
- **Reel sessions** (`/cinematic-reel <name>`): a new chat per reel, which only touches `projects/<name>/`. When a reel session hits a gap, it files a change request in `studio/change-requests/` instead of patching the studio.
- **Pilot reels**: these log friction and write a retro, which HQ turns into improvements.

Open every session at the `reels-studio/` root. Details are in `studio/ARCHITECTURE.md`, and history is in `studio/CHANGELOG.md`.

## Making a reel

```bash
scripts/new_reel.sh gym-morning-routine
```
1. Put your main or talking-head clips in `projects/gym-morning-routine/raw/a-roll/` and cutaways in `raw/b-roll/`. For a music-only reel, all clips can go in `raw/b-roll/`. If your footage already lives somewhere else, link it in without copying it:
   ```bash
   scripts/link_footage.sh gym-morning-routine "/path/to/your/footage"
   ```
2. Optionally, put reference reels you like in `references/`. Screen recordings are fine.
3. Open Premiere with a project open and the bridge started.
4. Open a **new** Code session at the `reels-studio/` root and say **`/cinematic-reel gym-morning-routine`**.

Claude will:
1. **Ask you a few quick questions**: the idea, the goal, references, then look and pace options picked to fit your footage.
2. **Analyse every clip and reference**: exposure, colour cast, slow-mo headroom, and the reference's cut pacing.
3. **Write `brief.md`** with the full treatment, plus 3 hooks and a cut list. ⏸ *You approve.*
4. Cut it in a **duplicate sequence**, so your original is never touched.
5. Colour: correct each clip toward its camera file → match the shots → a look or texture only if you picked one.
6. Add the planned moves, transitions, B-roll, graphics and captions, then the sound design and a music mix that dips under speech.
7. Export `renders/exports/<name>_v1.mp4`. ⏸ *You give notes, and Claude makes `_v2` with only those changes.*
8. Write the Instagram caption, hook lines and hashtags. ⏸ *You approve.*

The full menu of looks, moves and transitions is in `.claude/skills/cinematic-reel/effects-playbook.md`. You can ask for any of them by name, e.g. "Warm Film look, a speed ramp on the gym shot, flash cuts on the beat".

Each kind of video has an **editing playbook** with its own style rules (pace, camera, type, sound), in `.claude/skills/cinematic-reel/playbooks/`: `cinematic-montage` for music montages, `story-montage` for narrated montages with one recurring character, `creator-explainer` for talking to camera. Claude proposes one in the first interview round; you can override any rule for a single reel.

## Before you shoot

The one-page camera guide is `studio/shooting-guide-blackmagic-cam.md`. It covers 25 fps at 1/50 s under Indian lamps, white balance set to the light, and a LUT for the monitor only (or its name in the slate notes). It comes from what the Pujo 2026 footage measured.

## Giving notes after a cut

Specific notes work best:
- "Open on the line about waking up at 5am."
- "Faster, about 2 s per shot."
- "Less grain."
- "Bold yellow captions, 3 words max."
- "Cut the part about protein shakes entirely."
- "Make the ending feel like [reference]."

## Library: drop your stuff here
| Folder | What goes in |
|---|---|
| `assets/luts/` | `.cube` LUTs (your go-to looks) |
| `assets/music/` | Licensed music beds |
| `assets/sfx/` | Whooshes, risers, hits, clicks (`.wav`) |
| `assets/overlays/` | Grain, light leaks, textures |
| `assets/mogrts/` | Premiere Essential Graphics templates |
| `assets/presets/` | Export presets (`.epr`) |

## Layout
```
CLAUDE.md                     rules Claude follows (tracks, guardrails, editing style)
.claude/skills/cinematic-reel the 7-phase workflow behind /cinematic-reel
.mcp.json                     Premiere MCP config for Claude Code in Terminal
scripts/                      the studio's tools (CLAUDE.md §5 lists them): ingest and footage analysis, camera check,
                              delivery encode, file check, pregate, review sheets, After Effects round-trip, and more
projects/<reel>/              brief.md (Claude writes) · project.md · raw/ · references/ · analysis/ · transcripts/ · renders/
```

## Troubleshooting
- **"Premiere not connected"**: Premiere must be open with a project loaded, and the CEP panel must show the bridge as started. If it still fails, right-click the panel and choose **Reload**.
- **Health check**: run `premiere-pro-mcp --doctor`.
- **No transcript**: check `ELEVENLABS_API_KEY` in `.env`, then run `scripts/transcribe_reel.sh <reel>`.
