# Editing playbooks: one per kind of video

The studio edits different kinds of video, and they need different rules. A whoosh that sells a whip pan in a festival montage is noise under a creator's explainer text. So the *style* rules live in **playbooks**, one file per kind of video. The rest stays shared:

| File | Holds | Scope |
|---|---|---|
| `studio/director-profile.md` | who the director is: handle, type style, standing preferences, AI policy | every reel |
| `CLAUDE.md` | studio contract: tracks, Premiere guardrails, safe zone, the review gate | every reel |
| `effects-playbook.md` | the **menu** of moves and how to build them in Premiere / After Effects | every reel |
| **`playbooks/<style>.md`** | the **style**: which moves, how often, with what numbers. Pace, camera, type, transitions, sound (incl. whooshes), colour, QA thresholds | the reels that pick it |

## Picking a playbook (skill Phase 0 → brief)
- In Round 1, propose a playbook from the reel type, the reference and the director's intent. Record it in `brief.md` (`Playbook: <name>`) and in `project.md`.
- A brief may **override** single rules ("this reel: no swishes"). Write the override in the brief with the reason.
- The reviewer judges against the brief, so overrides carry through to the review gate.
- When no playbook fits, pick the closest one and file a CR proposing a new one.

| Playbook | For | Status |
|---|---|---|
| [`cinematic-montage.md`](cinematic-montage.md) | Music-driven montages of places, festivals, events, with no speech | **Proven**: my-reel (v10), puja-night-2 (v5) |
| [`story-montage.md`](story-montage.md) | Narrated montages carried by one recurring character: travel, city, festival-as-story, with VO and subtitles | **Untested here**: measured from "Two Sides of Bangkok" (no audio in the reference). The first narrated reel is its pilot |
| [`creator-explainer.md`](creator-explainer.md) | Talking to camera: explainers, tips, stories, with captions and graphics | **Untested here**: adapted from the WeAreNoCode YouTube Editor kit (16:9 YouTube). The first talking-head reel is its pilot |

## Making a new playbook
1. **A liked result becomes a playbook.** When the director approves a reel whose style differs from the existing playbooks, write it down: run `scripts/teardown.py` on the approved export and its reference to get the numbers, then fill in every section below with them.
2. Every rule carries **its reason**, and its source where there is one (a reel and round, or a director note). Rules without reasons drift.
3. When a later note contradicts a rule, replace the rule; never keep both.
4. HQ owns these files. Reel sessions propose changes by CR.

## Sections every playbook has
Purpose and reel types · Pace and structure · Camera and motion · Type and graphics · Transitions · **Sound** (including whooshes) · Colour and texture · AI shots · QA thresholds (what the review gate should hold this style to)
