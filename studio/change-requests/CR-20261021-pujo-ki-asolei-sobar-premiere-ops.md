# CR-20261021-pujo-ki-asolei-sobar-premiere-ops

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | harness · rule · skill (premiere-mcp-reality.md) |
| Severity | workaround (one near-miss into another reel's project) |
| Status | partly done (v0.9.0) |

## What happened
**Shared Premiere: 4 incidents in this reel** (adds to CR-20261018-my-reel-premiere-shared-between-sessions):
1. At rough-cut start, `puja-night-2.prproj` was active while reel-2 showed "working", although the director had said Premiere was free.
2. Closing that project (`closeDocument(0,0)`) was **denied by the permission classifier** ("interfere with workloads"), even with the director's go and reel-2 marked done. I opened this reel's project alongside.
3. Mid-session, Premiere switched to reel-4's `uski-aankhein.prproj`. My next import would have landed there; the project-path guard in every script refused it ("wrong project"), and `duplicate_sequence` failed harmlessly ("Sequence not found").
4. With 3 projects open, the director loaded reel-4's `.cube` with no clip selected, and reel-4 warned it might have hit our project. A read-only scan found it clean.

**ExtendScript gotchas found here:**
5. `track.overwriteClip(stillImage, t)` uses the default still duration (5 s) and **silently overwrote two subtitle cards** behind it before `end` was set. Fix: `item.setInPoint(0,4); item.setOutPoint(len,4)` before the overwrite, then `clearInPoint / clearOutPoint`.
6. After setting `trackItem.end` to close a gap, `outPoint` reads back stale (confirms puja-night-2's item 15). Set `outPoint = inPoint + duration` explicitly.
7. `add_to_timeline_batch` at non-frame times left 1-frame gaps (7 of 19 cuts).
8. The MCP bridge dropped (`bridge_unavailable`) during a blocking `exportAsMediaDirect`. The export completed; `verify_premiere_connection` reconnected.
9. `$.global` values persist between `evalScript` calls, so stale parameters (a keep-list) leak into the next script unless every caller sets them.

10. `replace_clip` (preserveEffects true) reports `success:false` with "Clip was replaced but settings were not fully restored: motion scale" on a ProRes alpha title and a PNG still, yet every Motion / Opacity property, the timing and the in/out read back identical to the original. False negative: the check should compare values, not report a failed set call.

11. 2026-10-23: between two of my rounds, reel-4's project became Premiere's active project while its session was running. With no lock, a reel can't tell whether another session is mid-script, so this reel's Premiere build waited and the director reviewed an offline preview. (5th occurrence across reels; see CR-20261018-my-reel-premiere-shared-between-sessions.)

## Workaround used in the reel
- Every script checks `app.project.path` against this reel's `.prproj` and addresses sequences by ID (no "active" assumptions).
- Read-only cross-checks before trusting state (open projects list, effect scan per clip).
- An **offline preview** (`tools/preview_assemble.py`) mirrors the timeline (cuts, dissolve, pushes, overlays, VO) so review isn't blocked while Premiere is busy. Measured against the later Premiere export: mean pixel diff 2–4 / 255.

## Proposed change
- **One project open at a time** (harness rule plus a lock file `studio/locks/premiere.lock` with reel, session and time), released after `save_project`. A session that finds another reel's project open asks the director to close it; the editor can't close it.
- **Path guard as a shared helper** (`scripts/premiere_guard.jsx`) prepended to every reel's ExtendScript.
- Reality doc: add items 5–11, and the "plan in frames, then convert" rule for batch placement.
- Skill: offer the offline preview whenever Premiere is held by another reel.

## HQ decision (v0.9.0, 2026-11-04)
**The offline preview accepted, v0.9.0:** `scripts/preview_edl.py` (from this reel's `tools/preview_assemble.py`) builds the cut from the EDL off the camera files, so review isn't blocked while Premiere is busy, and the skill settles pace, picks and framing on previews before the Premiere build. **The Premiere lock and the other items stay open** (Batch C items 16 and 17).
