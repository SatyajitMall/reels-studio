# CR-20261023-pujo-ki-asolei-sobar-mains-flicker

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | script (analyze_footage.py, frame_scan.py, new deflicker tool) · skill (colour phase) |
| Severity | workaround (the director found it by eye at round 8; no studio check measures it) |
| Status | partly done (v0.7.1) |

## What happened
The director noticed a light flicker. The cause: Blackmagic Cam footage shot at a 1/60 s shutter under India's 50 Hz mains. Lamps pulse at 100 Hz, and a 30 fps capture aliases that to **10 Hz**, a 3-frame brightness cycle. Every harmonic aliases to 10 Hz or DC, so the whole pattern repeats every 3 frames. It shows up in two forms:
- **global pumping:** shot 4 measured 3.1 %, and 5.6 % at the p95 frame-to-frame step;
- **rolling horizontal bands** from the rolling shutter, where the phase changes down the frame: shots 2, 5, 7 and 10 had 1.5–2.8 % bands that cancel to ≤ 0.8 % in a whole-frame mean.

Bare bulbs flicker locally: one tile in shot 6 measured 13 %. The 25 fps clips (C043, C052) were clean, since 100 Hz = 4 × 25.

None of the studio checks measures this:
- `frame_scan.py` flags flashes and jumps, not a periodic ±3 % cycle;
- `analyze_footage.py` reads exposure, white balance and fps, but not shutter versus mains;
- ffmpeg's `deflicker` only evens out the whole-frame mean, so the bands and local lamps survive it.

## Workaround used in the reel
- **`projects/pujo-ki-asolei-sobar/tools/flicker_scan.py`:**
  - lock-in on the 3-frame cycle;
  - global, row-band and tile amplitude, in % of the level;
  - band phase spread, to tell banding apart.
- **`tools/deflicker.py`**, per shot render:
  - per-tile (32 × 12) log luma in linear light;
  - sliding lock-in on the 10 Hz cycle (gaussian σ 5 frames), which follows phase drift on VFR clips;
  - Wiener shrink by how much of the residual is 10 Hz, so people moving through a tile barely count;
  - 2 passes (4 on the bulb shot), with the correction clamped to ±15–20 %;
  - smooth bicubic gain map, applied in linear light. Brightness only, so no ghosting.
- **Result**, on 11 shots:
  - global 10 Hz amplitude down 3–8× (e.g. 3.08 → 0.57 %, 3.37 → 0.90 %);
  - bands ≤ 1 %;
  - p95 frame step 5.6–5.9 % → 1.3–2.4 %.
- **Checked:** consecutive-frame stills before and after.

## Proposed change
- **`analyze_footage.py`:**
  - read the shutter (QuickTime / Blackmagic metadata when present);
  - flag "mains-flicker risk" when the fps does not divide the local mains × 2. For India and Europe (50 Hz → 100 Hz), 25 / 50 fps are safe and 24 / 30 / 60 fps are at risk. For 60 Hz regions it's the reverse;
  - always run the 10 Hz / band lock-in scan per clip and write the result into `summary.md`.
- **`frame_scan.py`:** add a `flicker` check on exports: a periodic-cycle amplitude per tile, above ~0.8 %.
- **Promote the reel's `deflicker.py` to `scripts/deflicker.py`** as a per-clip pre-pass, before the clip goes into Premiere (or on baked renders). It takes the alias period as a parameter, computed rather than hard-coded: 30 fps at 100 Hz → 10 Hz → 3 frames; 24 fps at 100 Hz → |100 − 4 × 24| = 4 Hz → 6 frames.
- **Interview / director profile:** "Shoot at 1/50 s (or 1/100) under Indian mains lighting, or at 25 fps." Tell the director once, since every Pujo night shoot is lamp-lit.
- Skill, colour phase (`SKILL.md` Phase 4 / playbook §A2): deflicker comes **before** shot matching, since flicker skews the per-shot exposure readings.

## HQ decision
**Partly accepted, v0.7.1 (2026-10-27).**
- **Detection is done** in the new `scripts/ingest_report.py` (Phase 1):
  - it reads the Blackmagic Cam shutter and rates each clip against `--mains` (50 by default): exposure in whole lamp pulses, and the alias frequency for the fps;
  - with `--scan` it measures the aliased cycle by lock-in, on the whole frame and 6 bands;
  - it's verified on this reel's clips: C028 measured 3.9 % / 6.1 %, C043 (25 fps, 1/50 s) rated safe, 39 of 54 clips ≥ 1 %.
- **The shooting guide** (`studio/shooting-guide-blackmagic-cam.md`) asks for 25 fps at 1/50 s, and 50 fps at 1/100 s for slow motion.
- **Deferred to the backlog:**
  - promoting `deflicker.py` to `scripts/` (with display-domain estimation as the default);
  - the `flicker` check in `frame_scan.py`;
  - the ≤ 1.5 % per-tile QA target on exports.

## Follow-up 2026-10-24 (round 13)
On a phone the director still saw flicker on several shots after the round-8 deflicker: the measured residual was 2–6 % per tile on LED / bulb-lit shots (sources up to 13 %). A sweep found that 8 passes, clamp 35 %, 64×24 tiles and temporal σ 3 cut the residual to ≈ 1.2 % max with no edge artefacts. **Proposed:** a QA target of ≤ 1.5 % per-tile 10 Hz residual on every 30 fps shot, measured on the export. When a shot fails, the deflicker settings are raised until it passes.

## Follow-up 2026-10-24 (round 13b): estimate in display brightness
Even the stronger settings plateaued at ≈ 0.8 % mean tile on a static, lamp-lit shot. The corrected frames were flat in linear light but not in display brightness. A tile mixes ambient (steady) and lamp (flickering) light, so one linear-light gain per tile under-corrects the mid-tones. Estimating and correcting in code values (`deflicker.py --display`) on a finer grid (160×90, spatial smoothing 1.0) cut the residual 5× (0.76 → 0.14 %, global 0.53 → 0.06 %) with no edge artefacts. **Proposed:** make display-domain estimation the default in the promoted `scripts/deflicker.py`, and measure the QA residual in display brightness.
