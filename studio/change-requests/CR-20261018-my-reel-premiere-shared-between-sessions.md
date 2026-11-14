# CR-20261018-my-reel-premiere-shared-between-sessions

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.5.3 |
| Type | harness · rule |
| Severity | blocker (for parallel reels) |
| Status | open |

## What happened
I went to build my-reel v11, and `duplicate_sequence` on v10 returned "Sequence not found". `verify_premiere_connection` showed Premiere had `projects/puja-night-2/puja-night-2.prproj` open, with `Reel_puja-night-2_v3` active: the reel-2 session's project. Every Premiere MCP tool and ExtendScript call acts on `app.project` / `app.project.activeSequence`. If two reel sessions run at once, one session opening its project silently retargets the other's edits.

## Workaround used in the reel
Stopped before touching Premiere and asked the director. All the v11 assets were rendered outside Premiere.

## Proposed change
1. A Premiere **lock file**: `studio/locks/premiere.lock`, holding the reel name, session and time. A reel session takes it before opening its project and releases it after `save_project`. `verify_premiere_connection` wrapper / skill step 1: refuse mutations if the open project ≠ this reel's `.prproj`.
2. Skill rule: start every Premiere step with "the open project is mine", checked from `verify_premiere_connection().project.path`.
3. ARCHITECTURE: one Premiere at a time. Reel sessions queue for it; non-Premiere work (graphics, AE, analysis) can run in parallel.
