# CR-20261017-my-reel-after-effects-bridge

| Field | Value |
|---|---|
| From reel | `projects/my-reel/` |
| Arch version | 0.3.0 |
| Type | harness · script · skill |
| Severity | polish (new capability; the director asked for it) |
| Status | done v0.4.0 (stabilise: rejected) |

## What happened
The director approved v6 and asked how After Effects could make the reel more professional: remove grain/noise, better stabilisation, better slow motion, cinematic effects and shots. They have an After Effects subscription and asked HQ ("the master chat") to set up a bridge.

Installed on this machine: `/Applications/Adobe After Effects 2026/` with `aerender` (CLI renderer) and `Adobe After Effects Render Engine 2026.app`. There is no After Effects MCP in the studio today; Premiere's MCP can't apply AE-only effects.

Footage facts that drive the need (my-reel): 8-bit Rec.709 iPhone 17 / Blackmagic Cam HEVC, mostly 25 fps (some 24, interpreted), night, lifted shadows → visible sensor noise; handheld; slow-mo currently Premiere Optical Flow; speed ramp faked as two clips (250 % → 60 %).

## Workaround used in the reel
None yet. Premiere-only options: drop the V4 grain overlay; Premiere has no good temporal denoiser.

## Proposed change
Build an **After Effects round-trip** for reel sessions (HQ owns `.mcp.json`, `scripts/`, skills):

1. **Bridge** (pick one, HQ to evaluate):
   - an After Effects MCP server if a maintained one exists (check npm / GitHub; same review bar as the Premiere one); or
   - a script bridge: `osascript -e 'tell application "Adobe After Effects 2026" to DoScriptFile "<jsx>"'` to run ExtendScript, plus `aerender -project … -comp … -output …` for headless renders. Results written to a JSON file (lesson from Premiere: script return values get lost).
   - A `verify_ae_connection` check (AE running, scripting enabled: Preferences > Scripting & Expressions > "Allow Scripts to Write Files and Access Network").
2. **`scripts/ae_roundtrip.py`**: input = list of shots `{source, in, out, ops[]}` from a reel's EDL; builds an `.aep` per shot via JSX, applies ops, renders ProRes 422 HQ (or 4444 with alpha) to `projects/<reel>/renders/ae/<shot>.mov` with `aerender`, logs to `projects/<reel>/analysis/ae_log.json`. The reel then imports and replaces the clip in Premiere.
3. **Ops to support first** (built-in effects, no paid plugins required):
   - `denoise`: Remove Grain (Viewing Mode: Final Output; noise samples auto), then optional Add Grain at a low amount;
   - `timewarp`: Timewarp, Pixel Motion, speed %, with motion-vector quality high; and `time_remap` with eased ramp keyframes (speed curve from → to over N frames);
   - `stabilise`: Warp Stabilizer (with analysis wait + status check) or Mocha AE planar track → corner pin (manual fallback);
   - `glow`: halation (Glow on highlights, warm tint, low radius), `lens_blur` vignette, `light_rays` optional;
   - `3d_push`: layer in 3D with a slow camera dolly for static holds.
4. **Optional paid plugins** (the director decides; don't assume): Neat Video (denoise), Twixtor (slow-mo), RSMB (motion blur on speed-ups), Deep Glow, Optical Flares. Detect installed plug-ins and use them when present.
5. **QA hooks**: after render, re-run the reel's colour and shake reports (`analysis/colour_*.json`, `shake_*.json` recipes from my-reel) on the AE output vs the Premiere original; reject if luma shifts > 0.02 or shake rises.
6. **Skill/playbook**: a "Phase 5b — After Effects finishing (optional)" section, with when to use which op and the 25 fps slow-mo limits.

First use: my-reel v7. Denoise the 6 darkest shots (C027, C003, C034, C041, C036-area, C013-area as now cut), rebuild the 10.72 s hit as a Time Remap curve ramp, re-time the 4 slow-mo shots with Timewarp, Mocha-stabilise C073 / C072 / C011, and add light halation on the diya and temple shots.

## HQ decision
**Accepted, done in v0.4.0, apart from stabilisation.**

**Bridge:** our own script bridge, `scripts/ae_bridge.py`, rather than an AE MCP.
- The best candidate, `@kumoproductions/mcp-aftereffects`, is 2 months old with one contributor. It's in the backlog as a dependency decision for the director.
- AE 26.5's built-in MCP server is disabled behind a beta gate.
- Verified on AE 26.5x89:
  - `DoScript` runs a one-line loader that evals a generated .jsx; results come back through a JSON file, because AppleScript replies are always "0" or "1";
  - `DoScriptFile` must not be used: it didn't run and left a blocking dialog;
  - never enumerate `app.effects`: it took 5+ minutes and blocked AE. `ae_bridge.py effects <matchName>` checks names instead;
  - Glow is `ADBE Glo2`, not `ADBE GloH`.

**Round-trip:** `scripts/ae_roundtrip.py` (jobs JSON → one .aep per shot → aerender ProRes 422 → `_compare.png` + `analysis/ae_log.json`). Safety: it refuses to run over another open project, tags its own projects, and closes a half-built one on error.

**Ops verified by render:**
- `denoise`: Viewing Mode must be 4 (Final Output). 3 rendered a black matte. AE's defaults cut noise 30 % but smeared texture; the studio default (0.6, 2 passes, temporal) cuts 19 % and keeps texture.
- `timewarp`: Pixel Motion, exact duration, clean on a calm shot.
- `time_remap`: smooth eased ramp in one clip; output can run 1 frame long.
- `glow`.
- `grain`: available, not render-tested.

**Rejected: `stabilise` (and Mocha).** Added by script, Warp Stabilizer never analyses: every frame had a "Click Analyze to begin." banner, and the shake numbers even looked better because the tracker locked onto the banner. Keep stabilising in Premiere.

**Docs:** `.claude/skills/cinematic-reel/after-effects.md` and skill Phase 5b.

Ready for my-reel v7: the denoise, ramp, Timewarp and halation shots.


## Follow-up from my-reel v8 (2026-10-17, reel session)
- Proposed new ops for `ae_roundtrip.py`: `light_rays` (CC Light Rays; center from the brightest blob, intensity 110–140, radius 55–60 — verified visible on night lamp shots), `handles` (pad in/out so Premiere transitions don't freeze). Reel-local version: `projects/my-reel/analysis/ae_looks/looks.py`.
- Not working by script on 26.5: CC Particle World (renders black with property sets by name) and a Fractal-Noise light leak (flat wash). Reel used procedural overlays instead (`analysis/ae_looks/overlays.py`: amber light leaks, bokeh embers, ProRes, Screen blend) — candidate `scripts/overlays.py`.
- `frame_match` gives false mismatches on `rotate: 180` shots (compares with the unrotated source).
- Premiere rule for the skill: Warp clips + transitions → align the transition to the non-Warp side (QE alignment 0) or Warp only after the transition exists; never centre a transition on a Warp clip.
- **Update after v9:** the director rejected the decorative looks (rays, leaks, embers) as "cringe", and v9 removed them. So **withdraw the `light_rays` op proposal**, and don't promote the reel-local procedural leak/ember overlays. `handles`, the frame_match rotate fix and the Warp+transition rule still stand.
