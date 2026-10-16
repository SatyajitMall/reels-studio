# Studio Architecture

How the studio is run: one **HQ session** owns the architecture, and each reel is a **sub-project** edited in its own **reel session**.

Current version: see `studio/VERSION`. History: `studio/CHANGELOG.md`.

## 1. Two kinds of session

| | HQ session | Reel session |
|---|---|---|
| Purpose | Design and evolve the studio: rules, skills, scripts, harness, templates | Make one reel, start to finish |
| How to start | New Code session in `reels-studio/`, first message `/studio-hq` | New Code session in `reels-studio/`, first message `/cinematic-reel <reel-name>` |
| How many | One at a time (the latest `/studio-hq` claims HQ) | One per reel. Several can run side by side |
| Writes | Anything | Only `projects/<its-reel>/`, `studio/change-requests/`, `studio/retros/`, and new files in `assets/` |
| When it finds an architecture gap | Fixes it, bumps the version, logs it | Works around it inside its own reel, files a change request |

Always open sessions at the `reels-studio/` root, never inside `projects/<reel>/`: the Premiere MCP config (`.mcp.json`) and the skills load from the root.

## 2. Who owns what

| Path | Owner | Notes |
|---|---|---|
| `CLAUDE.md`, `README.md`, `setup.sh`, `.mcp.json` | HQ | Studio rules and setup |
| `.claude/` (skills, hooks, settings) | HQ | The harness |
| `scripts/` | HQ | Shared tooling |
| `studio/` | HQ | Except the two carve-outs below |
| `studio/director-profile.md` | HQ | Director's branding and preferences. Every reel reads it; changes arrive by CR |
| `studio/upstream/` | HQ | Drafted bug reports for third-party tools. Filing them is the director's call |
| `studio/change-requests/` | Any session | Reel sessions file requests here |
| `studio/retros/` | Any session | Reel sessions copy their finished retro here |
| `projects/_template/` | HQ | New reels are copied from it |
| `projects/<reel>/` | That reel's session | Brief, log, analysis, renders, retro |
| `assets/` | Shared | Any session may **add** files. Only HQ renames or deletes |

**Enforcement.** `.claude/hooks/guard_architecture.py` denies Edit/Write on HQ-owned paths from any session that isn't the current HQ. A prompt starting with `/studio-hq` claims HQ by writing its session id to `.claude/state/hq_session`. Shell writes aren't intercepted, so `CLAUDE.md` §0.1 also states the rule.

## 3. Change requests (reel → HQ)

1. The reel session hits a gap: a missing rule, a wrong tool name, a script bug, a missing reel type, an effect that doesn't work over MCP.
2. It works around the gap **inside its own reel folder** and says so in that reel's `project.md`.
3. It files `studio/change-requests/CR-<YYYYMMDD>-<reel>-<slug>.md` from `_TEMPLATE.md`.
4. The HQ session triages it with `/studio-hq`:
   - **accept**: apply it, bump the version, add a `CHANGELOG.md` entry, and set the CR's status to `done vX.Y.Z`;
   - **defer**: add it to `BACKLOG.md`;
   - **reject**: set the status and give the reason.

## 4. Pilot reels

The first reels are **pilots**: `Pilot: yes` in their `project.md`. A pilot reel session also:
- logs friction as it goes, under `## Friction log` in `project.md` (anything slow, failed, guessed, or done by hand);
- writes `retro.md` at the end (template in `projects/_template/retro.md`), copies it to `studio/retros/<reel>.md`, and turns each "change the studio" item into a CR.

HQ harvests the retros into skills, rules, scripts and templates. A reel stops being a pilot when the director says the architecture is stable.

## 5. Versioning

- `studio/VERSION` uses semver:
  - **major**: a reel in progress must change how it works;
  - **minor**: a new capability, rule or reel type;
  - **patch**: a fix or clarification.
- Each reel records the version it started on, in `project.md`. A reel in progress keeps its version for the current round. It picks up minor and patch changes at the next round. A major change needs the director's OK for reels in progress.
- The repo is tracked in git, so any architecture change can be rolled back. Media (raw clips, renders, assets) is git-ignored.

## 6. Reel types

Set in `brief.md` and `project.md`. They drive which editorial rules apply (`CLAUDE.md` §4):

| Type | What it is | Timing source | Transcription |
|---|---|---|---|
| `talking-head` | Someone speaks to camera or in voiceover | Word boundaries | Yes |
| `music-montage` | No speech. The music carries it | Beat grid of the music track | No |
| `hybrid` | Montage with spoken lines or VO moments | Words in spoken parts, beats in the rest | Spoken clips only |
