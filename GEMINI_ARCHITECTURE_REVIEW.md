# Gemini Deep Audit & Upgrade Guide for `reels-studio/`

> **Zero-Mutation Guarantee:** No existing files created by Claude Code in `reels-studio/` were modified. All Gemini additions live in `GEMINI_ARCHITECTURE_REVIEW.md` and `scripts/gemini_*.py`.

## 1. What Claude Code Built Exceptionally Well

Claude Code evolved the initial bootstrap specification into a strong **Director–Editor studio workflow**. Specifically, Claude made five smart architectural decisions worth keeping:

1. **Separating Captions Above the Color Grade (`V5` vs. `V3`/`V4`):**
   Moving captions to `V5` above the `V3` LUT adjustment layer and `V4` film grain ensures text remains crisp white or brand-colored instead of getting tinted or darkened by the grade.
2. **The Single-Lumetri Rule (`effects-playbook.md` §A1):**
   Claude accurately noted that calling `color_correct` in [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/adobe_premiere_pro_mcp) appends a **new** Lumetri Color effect instance every time—and Premiere 2026's ExtendScript DOM cannot remove individual effects. Calling `color_correct` once per clip on `V1`/`V2` for primary balance and using `set_effect_property` afterward prevents stacked Lumetri instances.
3. **3-Slice Speed Ramp Workaround (`effects-playbook.md` §C):**
   Because Premiere's ExtendScript API cannot script Bezier velocity curves on time-remapping keyframes, slicing a B-roll clip into `Fast (1.5–3x) -> Slow (0.4x) -> Fast` with short cross-dissolves between slices is the most reliable way to automate speed ramps over MCP.
4. **Visual Contact Sheets + Reference Pacing (`scripts/analyze_footage.py`):**
   Generating `contact.png` frame grids alongside exposure (`luma_mean`), contrast (`luma_p02`–`luma_p98`), midtone color cast (`warm_cool`, `green_magenta`), slow-mo headroom (`fps >= 50`), and FFmpeg scene-cut detection (`--reference`) gives Claude grounded visual metrics before writing `brief.md`.
5. **Two-Round Director Interview (`SKILL.md` Phase 0):**
   Splitting the interview into Round 1 (concept/goal before analysis) and Round 2 (concrete look/pace choices *after* measuring the footage and reference reels) prevents generic guesswork.

---

## 2. Six Critical Gaps & Production Bugs Found in Claude's Current Harness

While auditing `CLAUDE.md`, `.claude/skills/cinematic-reel/`, `scripts/`, and `.vendor/video-use/`, six concrete issues surfaced that will either break execution or degrade visual/audio quality when you run `/cinematic-reel`:

| # | File / Component | The Bug or Gap in Claude's Current Setup | Impact During a Reel Edit | Gemini Fix Provided |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `assets/luts/`, `assets/sfx/`, `assets/overlays/` | All asset folders contain only `.gitkeep` (0 actual `.cube`, `.wav`, or `.mp4` files), yet `SKILL.md` Phase 4–6 requires importing LUTs, grain overlays, and 6 SFX types from `assets/`. | Phase 4 (`apply_lut`), Phase 4 (`V4` texture), and Phase 6 (`A2` SFX) fail or skip because no asset files exist. | Run `scripts/gemini_generate_starter_pack.py` to generate 5 mathematical `.cube` LUTs, 6 `.wav` SFX, and a 16mm grain loop (`gemini_*`). |
| **2** | `.env` & `scripts/transcribe_reel.sh` | `.env` currently has `ELEVENLABS_API_KEY=` blank, and `.vendor/video-use/helpers/transcribe.py` hard-exits if the key is empty (and hardcodes `scribe_v1` on line 88 instead of `scribe_v2`). | Without an ElevenLabs key, `transcribe_reel.sh` crashes and Claude loses all word-level cutting, retake grouping, and caption generation. | Use `scripts/gemini_transcribe_fallback.py`, which supports `scribe_v2` AND auto-falls back to free local Whisper (`mlx-whisper` / `faster-whisper`) outputting Scribe-compatible JSON. |
| **3** | `scripts/analyze_footage.py` | Only analyzes video pixels; does **not** measure audio loudness (LUFS / peak dBFS) or music BPM / beat timestamps, even though `librosa` is already installed in `.venv`! | Claude guesses clip gain adjustments (`-6 to -3 dB` dialogue target) and cannot align B-roll cuts or flash transitions to actual music beats. | Run `scripts/gemini_audio_and_beat_analyzer.py` to output exact dialogue LUFS/peak gain deltas and a music `beats.json` + beat-drop map. |
| **4** | `CLAUDE.md` §3 Track Layout (`V2` vs. `V3`) | Places both **B-roll** AND **HyperFrames motion graphics** on `V2` *underneath* the `V3` Creative Look Adjustment Layer and `V4` grain. | The `V3` LUT and vignette discolor your HyperFrames UI cards, stat callouts, and brand hex colors. | Put only B-roll on `V2` (under the `V3` LUT). Place HyperFrames graphic overlays on **`V5`** and captions on **`V6`** above the grade. |
| **5** | `effects-playbook.md` & `CLAUDE.md` Tool Names | References `set_clip_opacity`, `speed_change`, and `reverse_clip` as direct tool names. In [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/adobe_premiere_pro_mcp), opacity is set via `set_clip_properties` (`opacity` field). | Direct calls to `set_clip_opacity` fail with tool-not-found unless Claude queries `search_tools` / `get_tool_schema` first. | Instruct Claude in `CLAUDE.md` to use `set_clip_properties` for opacity/transform batches and always verify schema via `get_tool_schema`. |
| **6** | `scripts/analyze_footage.py` iPhone HDR / Log Detection | Checks `color_transfer in ("arib-std-b67", "smpte2084")` for HDR, which catches iPhone Dolby Vision HLG (`arib-std-b67`), **but** Premiere Pro 2025/2026 auto-tone-maps HLG unless color space override is set. | Applying a Log-to-Rec709 LUT on already tone-mapped iPhone HLG footage causes severe highlight blowout and over-saturation. | Check `get_footage_interpretation` / `set_footage_interpretation` (or `set_clip_color_space` in MCP) to force Rec.709 color management before grading iPhone HDR clips. |

---

## 3. How to Use the New Gemini Scripts (`scripts/gemini_*.py`)

### 3.1 Generate Your Starter LUTs, SFX & Film Grain (`gemini_generate_starter_pack.py`)
Creates 5 `.cube` 3D LUTs (matching the exact 5 looks in `effects-playbook.md`), 6 synthesized cinematic `.wav` SFX, and a 1080×1920 16mm film grain overlay—all prefixed with `gemini_` so your asset folders work out of the box:

```bash
./.venv/bin/python scripts/gemini_generate_starter_pack.py
```

**Generated files:**
- `assets/luts/gemini_warm_film_2383.cube` (Warm Film: lifted warm shadows, golden midtones, soft highlight roll-off)
- `assets/luts/gemini_teal_and_orange.cube` (Teal & Orange: complementary shadow/skin separation)
- `assets/luts/gemini_moody_desat.cube` (Moody Desat: desaturated cool shadows, punchy midtone contrast)
- `assets/luts/gemini_clean_bright.cube` (Clean Bright: airy creator look with gentle highlight protection)
- `assets/luts/gemini_log_to_rec709.cube` (Flat/Log to Rec.709 S-curve normalization LUT)
- `assets/sfx/gemini_whoosh_soft.wav`, `gemini_riser_sub_hit.wav`, `gemini_snap_swish.wav`, `gemini_text_pop_click.wav`, `gemini_camera_shutter.wav`, `gemini_bass_drop_boom.wav`
- `assets/overlays/gemini_film_grain_16mm.mp4` (4-second seamless 1080×1920 monochrome grain loop for `V4` Overlay/Soft Light mode)

### 3.2 Run Audio Loudness & Music Beat Detection (`gemini_audio_and_beat_analyzer.py`)
Analyzes dialogue clips (measuring integrated LUFS, True Peak dBFS, and the exact `set_clip_volume` dB adjustment needed in Premiere to hit `-4.5 dBFS` peak) AND analyzes your music track with `librosa` to extract exact BPM, beat timestamps, and high-energy beat drops:

```bash
./.venv/bin/python scripts/gemini_audio_and_beat_analyzer.py \
  projects/<reel-name>/raw/a-roll \
  --music assets/music/<track.mp3> \
  -o projects/<reel-name>/analysis
```

### 3.3 Transcribe with Scribe v2 or Free Offline Whisper (`gemini_transcribe_fallback.py`)
Drop-in replacement for `scripts/transcribe_reel.sh` that upgrades ElevenLabs from `scribe_v1` to `scribe_v2` AND automatically falls back to local free Whisper (`mlx-whisper` on Apple Silicon or `faster-whisper`) when `ELEVENLABS_API_KEY` is blank:

```bash
./.venv/bin/python scripts/gemini_transcribe_fallback.py <reel-name>
```

---

## 4. Prompt to Hand to Claude Code to Adopt These Upgrades

Paste this into Claude Code inside `reels-studio/` whenever you want Claude to merge these improvements into its workflow:

```text
Read GEMINI_ARCHITECTURE_REVIEW.md and inspect scripts/gemini_generate_starter_pack.py, scripts/gemini_audio_and_beat_analyzer.py, and scripts/gemini_transcribe_fallback.py.

Please apply the following upgrades to our studio setup:
1. Run `./.venv/bin/python scripts/gemini_generate_starter_pack.py` so `assets/luts/`, `assets/sfx/`, and `assets/overlays/` are populated with the starter `.cube` LUTs, `.wav` SFX, and 16mm grain loop.
2. Update `CLAUDE.md` and `.claude/skills/cinematic-reel/SKILL.md` so:
   - Track layout uses 6 video tracks (`V1` A-roll, `V2` B-roll, `V3` Creative Look Adjustment Layer, `V4` Texture Overlays, `V5` HyperFrames Graphics, `V6` Captions) so HyperFrames graphics sit above the LUT grade and never get discolored.
   - `set_clip_properties` (with `opacity`) is used instead of the non-existent `set_clip_opacity` tool, and iPhone HLG/HDR clips (`arib-std-b67`) are checked for color-space override before grading.
   - Phase 1 also runs `scripts/gemini_audio_and_beat_analyzer.py` (for exact dialogue dB gain targets and music beat-grid timestamps) and uses `scripts/gemini_transcribe_fallback.py` when `ELEVENLABS_API_KEY` is not set.
```
