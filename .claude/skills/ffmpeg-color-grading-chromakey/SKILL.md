---
name: ffmpeg-color-grading-chromakey
description: |
  FFmpeg colour and keying recipes for work OUTSIDE Premiere in the reels studio: look previews on stills before the director picks a look, pre-rendered effect shots planned in the brief (colour isolation, sepia, film looks), green/blue-screen keying into ProRes 4444 alpha overlays for V5, despill, LUT application to stock or AI clips, and colour-tag fixes. Not for the reel's grade: per-clip correction and the creative look stay in Premiere (CLAUDE.md §2, effects-playbook §A).
---

> **Imported** from [josiahsiegel/claude-plugin-marketplace](https://github.com/josiahsiegel/claude-plugin-marketplace) (`plugins/ffmpeg-effects/skills/ffmpeg-color-grading-chromakey`, commit `9ae4e4a`), MIT licence (`LICENSE` in this folder), © 2025 Josiah Siegel. HQ imported it on 2026-10-21 (studio v0.6.1).
> Every recipe was run on ffmpeg 9.0.2 against a real reel still and a test green screen. The ones that failed or misled are corrected below, marked **Studio fix**. The upstream Windows path rule was dropped, since the studio runs on macOS.

## Studio rules (read first)
- **The reel's grade lives in Premiere.** Primary correction goes on the clips (Lumetri) and the look goes on the V3 adjustment layer. Never grade the reel, or its export, here: grading twice and re-encoding loses quality and breaks shot matching.
- **Where ffmpeg colour is used:**
  1. **Look previews (skill Phase 0, Round 2).** Render each look option on 3–4 stills from the director's footage, as one labelled contact sheet, so the director picks from their own shots instead of from names.
  2. **Pre-rendered effect shots** the brief plans, such as colour isolation (keep only the red), sepia or a film look on one shot. Treat them like After Effects renders: the original stays, the render replaces the shot at the same timeline position, and the brief says so.
  3. **Keying** a green or blue-screen stock element into a ProRes 4444 alpha overlay for V4/V5.
  4. **Stock and AI clips:** use `scripts/conform_clip.py`, which already applies the colour match with `lut3d`.
- **Every render gets BT.709 tags**: `setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv` at the end of the filter chain, plus `-color_primaries bt709 -color_trc bt709 -colorspace bt709` (and `-movflags +write_colr` for `.mov`). The output flags alone leave ProRes half-tagged. Check a still of it against the source before it goes in Premiere.
- **Test a look on a still first.** On warm night footage some recipes go too far. Measured on a Durga Puja night still (mean R/G/B 72/44/20):
  - teal & orange crushed blue to 7/255;
  - `curves=preset=vintage` lifted blue from 20 to 53, a magenta cast.
  - the "35mm Film Look" chain (its `curves=preset=cross_process`) turned the temple green-yellow and the sky red.
- **Labelling sheets:** this ffmpeg has no `drawtext` (built without freetype). Render the tiles with ffmpeg, then label and stack them with Pillow (`./.venv/bin/python`).
- **Not available here: HDR → SDR.** The tone-mapping recipes need `zscale`, which this ffmpeg build lacks (Homebrew without libzimg). For iPhone HLG or HDR clips, let Premiere convert them (BACKLOG G6).

## Quick Reference

| Task | Command |
|------|---------|
| Green screen removal | `-vf "chromakey=<sampled colour>:0.15:0.1,despill=type=green"` (studio fix: sample the screen, start low) |
| Blue screen removal | `-vf "chromakey=<sampled colour>:0.15:0.1,despill=type=blue"` |
| Keep one colour, grey the rest | `-vf "colorhold=color=0xC83C1E:similarity=0.25:blend=0.1"` |
| Apply LUT | `-vf "lut3d=cinematic.cube"` |
| Color curves | `-vf "curves=preset=vintage"` |
| Adjust saturation | `-vf "eq=saturation=1.5"` |
| Hue shift | `-vf "hue=h=30"` |
| White balance | `-vf "colortemperature=6500"` |

## When to Use This Skill

Use for **color manipulation operations**:
- Removing green/blue screen backgrounds
- Applying LUT color grading
- Color correction and enhancement
- Creating cinematic color looks
- HDR/SDR conversions
- Color keying for compositing

---

# FFmpeg Color Grading & Chromakey (2025)

Complete guide to color manipulation, green screen removal, LUT grading, and advanced color effects with FFmpeg.

## Green Screen (Chromakey) Removal

### Basic Chromakey

```bash
# Remove green screen (standard green 0x00FF00)
ffmpeg -i foreground.mp4 -i background.mp4 \
  -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.1[fg];[1:v][fg]overlay" \
  -c:v libx264 -crf 18 output.mp4

# Parameters:
# - color: The key color (hex 0xRRGGBB)
# - similarity: How close to key color (0.0-1.0, lower = more precise)
# - blend: Edge softness (0.0-1.0, higher = softer edges)
```

### Chromakey Parameter Tuning

```bash
# Tight key (clean edges, may leave green fringe)
ffmpeg -i green_screen.mp4 -i background.jpg \
  -filter_complex "[0:v]chromakey=0x00FF00:0.1:0.0[fg];[1:v][fg]overlay" \
  output.mp4

# Loose key (removes all green, may eat into subject)
ffmpeg -i green_screen.mp4 -i background.jpg \
  -filter_complex "[0:v]chromakey=0x00FF00:0.5:0.2[fg];[1:v][fg]overlay" \
  output.mp4

# Balanced (recommended starting point)
ffmpeg -i green_screen.mp4 -i background.jpg \
  -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.1[fg];[1:v][fg]overlay" \
  output.mp4
```

> **Studio fix:** the key colour must be the screen's **real colour**, and 0.3 isn't a safe start. Keying a 0x00B140 screen at `0x00B140:0.3:0.1` made a warm, skin-toned subject partly transparent: (208,128,96) became (66,51,93) over the background. A real screen is never pure `0x00FF00`. Sample it from a frame first:
> `ffmpeg -ss 1 -i green_screen.mp4 -vf "crop=20:20:10:10,scale=1:1" -frames:v 1 -f rawvideo -pix_fmt rgb24 - | xxd -p` (prints RRGGBB).
> Start at similarity **0.10–0.15**, blend 0.05–0.1. Raise it only until the background is clean, then check the subject's alpha (`alphaextract`) on 3 frames.

### Blue Screen Removal

```bash
# Remove blue screen
ffmpeg -i blue_screen.mp4 -i background.mp4 \
  -filter_complex "[0:v]chromakey=0x0000FF:0.3:0.1[fg];[1:v][fg]overlay" \
  output.mp4

# Chroma blue (common broadcast blue)
ffmpeg -i footage.mp4 -i background.mp4 \
  -filter_complex "[0:v]chromakey=0x0047AB:0.3:0.15[fg];[1:v][fg]overlay" \
  output.mp4
```

### Sample Green Screen Colors

| Name | Hex | Use Case |
|------|-----|----------|
| Pure Green | 0x00FF00 | Digital green screens |
| Chroma Green | 0x00B140 | Professional film/TV |
| Light Green | 0x90EE90 | Lighter backgrounds |
| Pure Blue | 0x0000FF | Digital blue screens |
| Chroma Blue | 0x0047AB | Professional broadcast |

### Advanced Chromakey with Despill

Green spill removal (green reflection on subject):

> **Studio fix:** use ffmpeg's own **`despill`** filter: `chromakey=<sampled>:0.15:0.1,despill=type=green` (or `type=blue`). It neutralised the green edge, (109,159,94) → (47,46,95), and left the subject untouched. The `colorbalance` recipes below tint the whole subject: its green fell from 124 to 107. The `hue=s=0.9` one only desaturates everything.

```bash
# Remove green screen with despill
ffmpeg -i green_screen.mp4 -i background.mp4 \
  -filter_complex "\
    [0:v]chromakey=0x00FF00:0.3:0.1,\
    colorbalance=gs=-0.1:gm=-0.1:gh=-0.1[fg];\
    [1:v][fg]overlay" \
  output.mp4

# More aggressive despill using hue filter
ffmpeg -i green_screen.mp4 -i background.mp4 \
  -filter_complex "\
    [0:v]chromakey=0x00FF00:0.3:0.1,\
    hue=s=0.9[fg];\
    [1:v][fg]overlay" \
  output.mp4
```

## Colorkey Filter (Transparency)

Colorkey creates actual transparency (alpha channel) instead of compositing:

```bash
# Create transparent video (WebM with alpha)
ffmpeg -i green_screen.mp4 \
  -vf "colorkey=0x00FF00:0.3:0.1" \
  -c:v libvpx-vp9 -pix_fmt yuva420p \
  output_transparent.webm

# Create transparent PNG sequence
ffmpeg -i green_screen.mp4 \
  -vf "colorkey=0x00FF00:0.3:0.1" \
  frame_%04d.png
```

**Studio overlay format (V4/V5 in Premiere): ProRes 4444 with alpha.** Tested: alpha 0 on the screen, 255 on the subject.
```bash
ffmpeg -i green_screen.mp4 \
  -vf "colorkey=<sampled>:0.15:0.1,despill=type=green,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuva444p10le,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv" \
  -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le -an \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +write_colr overlay_alpha.mov
```
The `setparams` + `-movflags +write_colr` pair is what makes ProRes keep all three BT.709 tags; with the output flags alone it writes only the primaries.

### Colorkey vs Chromakey

| Feature | colorkey | chromakey |
|---------|----------|-----------|
| Output | Alpha channel | Composited |
| Format | Requires alpha support | Any format |
| Use | Create masks | Direct compositing |
| Formats | WebM, PNG, ProRes 4444 | MP4, MKV, etc. |

## LUT Color Grading

### Apply 3D LUT

```bash
# Apply .cube LUT file
ffmpeg -i input.mp4 \
  -vf "lut3d=cinematic.cube" \
  -c:v libx264 -crf 18 output.mp4

# Apply .3dl LUT
ffmpeg -i input.mp4 \
  -vf "lut3d=film_look.3dl" \
  output.mp4

# Specify interpolation method
ffmpeg -i input.mp4 \
  -vf "lut3d=lut.cube:interp=trilinear" \
  output.mp4
```

### LUT Interpolation Methods

| Method | Quality | Speed |
|--------|---------|-------|
| nearest | Lowest | Fastest |
| trilinear | Good | Fast |
| tetrahedral | Best | Slower |

```bash
# High quality LUT application
ffmpeg -i input.mp4 \
  -vf "lut3d=film.cube:interp=tetrahedral" \
  -c:v libx264 -crf 18 output.mp4
```

### Blend Original with LUT

```bash
# 50% LUT strength
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]split[a][b];\
    [a]lut3d=cinematic.cube[graded];\
    [b][graded]blend=all_expr='A*0.5+B*0.5'" \
  output.mp4
```

> **Studio fix:** the upstream "variable LUT intensity using colorbalance" recipe was removed: an all-zero `colorbalance` does nothing. Vary the strength with the `blend` weights above (tested: `0.5/0.5` lands halfway between the source and the full LUT).

### Popular LUT Styles

Create common looks without external LUTs:

```bash
# Teal and Orange (blockbuster look)
ffmpeg -i input.mp4 \
  -vf "colorbalance=rs=0.1:gs=-0.1:bs=-0.2:rm=0.05:gm=-0.05:bm=-0.1:rh=0.1:gh=-0.05:bh=-0.15" \
  output.mp4

# Vintage/Retro
ffmpeg -i input.mp4 \
  -vf "curves=preset=vintage,eq=saturation=0.8:contrast=1.1" \
  output.mp4

# High Contrast Cinematic
ffmpeg -i input.mp4 \
  -vf "eq=contrast=1.2:brightness=-0.05:saturation=1.1,unsharp=5:5:0.8" \
  output.mp4

# Desaturated/Bleach Bypass
ffmpeg -i input.mp4 \
  -vf "eq=saturation=0.5:contrast=1.3:brightness=-0.02" \
  output.mp4

# Warm/Golden Hour
ffmpeg -i input.mp4 \
  -vf "colortemperature=5000,eq=saturation=1.2:brightness=0.05" \
  output.mp4

# Cool/Moonlight
ffmpeg -i input.mp4 \
  -vf "colortemperature=8000,eq=saturation=0.9:brightness=-0.05" \
  output.mp4
```

## Color Curves

### Preset Curves

```bash
# Vintage look
ffmpeg -i input.mp4 -vf "curves=preset=vintage" output.mp4

# Cross process (film developing effect)
ffmpeg -i input.mp4 -vf "curves=preset=cross_process" output.mp4

# Negative image
ffmpeg -i input.mp4 -vf "curves=preset=negative" output.mp4

# Increase contrast
ffmpeg -i input.mp4 -vf "curves=preset=strong_contrast" output.mp4

# Lighter
ffmpeg -i input.mp4 -vf "curves=preset=lighter" output.mp4

# Darker
ffmpeg -i input.mp4 -vf "curves=preset=darker" output.mp4

# Linear contrast
ffmpeg -i input.mp4 -vf "curves=preset=linear_contrast" output.mp4

# Medium contrast
ffmpeg -i input.mp4 -vf "curves=preset=medium_contrast" output.mp4
```

### Custom Curves

```bash
# S-curve for contrast (RGB)
ffmpeg -i input.mp4 \
  -vf "curves=all='0/0 0.25/0.20 0.5/0.5 0.75/0.80 1/1'" \
  output.mp4

# Lift shadows, lower highlights
ffmpeg -i input.mp4 \
  -vf "curves=all='0/0.05 0.5/0.5 1/0.95'" \
  output.mp4

# Per-channel curves (R, G, B)
ffmpeg -i input.mp4 \
  -vf "curves=r='0/0 0.5/0.6 1/1':g='0/0 0.5/0.5 1/1':b='0/0 0.5/0.4 1/1'" \
  output.mp4

# Crushed blacks (film look)
ffmpeg -i input.mp4 \
  -vf "curves=all='0/0.03 0.15/0.15 0.5/0.5 0.85/0.85 1/1'" \
  output.mp4
```

## Color Balance

### colorbalance Filter

```bash
# Warm highlights, cool shadows
ffmpeg -i input.mp4 \
  -vf "colorbalance=rs=-0.1:gs=-0.05:bs=0.1:rh=0.1:gh=0.05:bh=-0.1" \
  output.mp4

# Parameters:
# rs/gs/bs = red/green/blue shadows (-1 to 1)
# rm/gm/bm = red/green/blue midtones (-1 to 1)
# rh/gh/bh = red/green/blue highlights (-1 to 1)
```

### Common Color Balance Presets

```bash
# Orange and Teal (cinematic)
ffmpeg -i input.mp4 \
  -vf "colorbalance=rs=0.15:bs=-0.15:rh=0.1:bh=-0.1" \
  output.mp4

# Warm overall
ffmpeg -i input.mp4 \
  -vf "colorbalance=rs=0.1:rm=0.05:rh=0.1:bs=-0.05:bm=-0.03:bh=-0.05" \
  output.mp4

# Cool shadows, warm highlights (split toning)
ffmpeg -i input.mp4 \
  -vf "colorbalance=rs=-0.1:bs=0.1:rh=0.15:bh=-0.1" \
  output.mp4
```

## Hue and Saturation

### hue Filter

```bash
# Rotate hue by 30 degrees
ffmpeg -i input.mp4 -vf "hue=h=30" output.mp4

# Increase saturation
ffmpeg -i input.mp4 -vf "hue=s=1.5" output.mp4

# Decrease saturation (desaturate)
ffmpeg -i input.mp4 -vf "hue=s=0.5" output.mp4

# Adjust brightness
ffmpeg -i input.mp4 -vf "hue=b=0.1" output.mp4

# Animated hue rotation
ffmpeg -i input.mp4 \
  -vf "hue=h=t*36" \
  output.mp4  # Full rotation every 10 seconds
```

### eq Filter (Comprehensive)

```bash
# Full color adjustment
ffmpeg -i input.mp4 \
  -vf "eq=contrast=1.1:brightness=0.05:saturation=1.2:gamma=1.1" \
  output.mp4

# eq parameters:
# contrast: 0-2 (default 1)
# brightness: -1 to 1 (default 0)
# saturation: 0-3 (default 1)
# gamma: 0.1-10 (default 1)
# gamma_r/gamma_g/gamma_b: per-channel gamma
```

## White Balance

### colortemperature Filter (FFmpeg 5.1+)

```bash
# Warm up (lower temperature)
ffmpeg -i input.mp4 \
  -vf "colortemperature=temperature=5000" \
  output.mp4

# Cool down (higher temperature)
ffmpeg -i input.mp4 \
  -vf "colortemperature=temperature=8000" \
  output.mp4

# Neutral daylight
ffmpeg -i input.mp4 \
  -vf "colortemperature=temperature=6500" \
  output.mp4
```

### Manual White Balance

```bash
# Using colorbalance for white balance
# Correct blue cast (add warmth)
ffmpeg -i input.mp4 \
  -vf "colorbalance=rs=0.1:rm=0.05:bs=-0.1:bm=-0.05" \
  output.mp4

# Correct yellow/orange cast (add blue)
ffmpeg -i input.mp4 \
  -vf "colorbalance=rs=-0.1:rm=-0.05:bs=0.1:bm=0.05" \
  output.mp4
```

## Color Space Conversions

### SDR Color Spaces

```bash
# Convert BT.601 to BT.709
ffmpeg -i input.mp4 \
  -vf "colorspace=bt709:iall=bt601-6-625:fast=1" \
  -c:v libx264 -crf 18 \
  output.mp4

# Force color space metadata
ffmpeg -i input.mp4 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:v libx264 -crf 18 output.mp4
```

### HDR to SDR Tone Mapping

> **Studio note:** these need `zscale` (libzimg), which this machine's ffmpeg doesn't have. Use Premiere for HLG/HDR clips (see Studio rules).

```bash
# Basic HDR to SDR (BT.2020/PQ to BT.709)
ffmpeg -i hdr_input.mp4 \
  -vf "zscale=t=linear:npl=100,format=gbrpf32le,\
       zscale=p=bt709,tonemap=tonemap=hable:desat=0,\
       zscale=t=bt709:m=bt709:r=tv,format=yuv420p" \
  -c:v libx264 -crf 18 sdr_output.mp4

# HDR10 to SDR with better quality
ffmpeg -i hdr10_input.mp4 \
  -vf "zscale=t=linear:npl=100,format=gbrpf32le,\
       zscale=p=bt709,tonemap=tonemap=reinhard:param=0.4:desat=0,\
       zscale=t=bt709:m=bt709,format=yuv420p" \
  -c:v libx264 -crf 18 output.mp4
```

### Tone Mapping Algorithms

| Algorithm | Characteristic |
|-----------|----------------|
| none | Clipping only |
| clip | Hard clip to SDR range |
| linear | Linear scale |
| gamma | Gamma curve |
| reinhard | Soft rolloff, natural |
| hable | Film-like, John Hable |
| mobius | S-curve, smooth |

## Selective Color Manipulation

### Color Isolation (Selective Desaturation)

```bash
# Keep only one colour, greyscale the rest (Sin City effect)
# Studio fix: the upstream chain desaturated everything first, so no colour survived (the output was pure grey).
# colorhold / hsvhold do it in one filter. Sample the colour to keep from the frame.
ffmpeg -i input.mp4 \
  -vf "colorhold=color=0xC83C1E:similarity=0.25:blend=0.1" \
  output.mp4

# Hue-based (steadier when lighting varies): hue in degrees, sat/val 0-1
ffmpeg -i input.mp4 \
  -vf "hsvhold=hue=15:sat=0.6:val=0.5:similarity=0.25:blend=0.1" \
  output.mp4
```

### colorchannelmixer

```bash
# Convert to grayscale with proper luminance weights
ffmpeg -i input.mp4 \
  -vf "colorchannelmixer=.3:.59:.11:0:.3:.59:.11:0:.3:.59:.11" \
  output.mp4

# Sepia tone
ffmpeg -i input.mp4 \
  -vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131" \
  output.mp4

# Swap red and blue channels
ffmpeg -i input.mp4 \
  -vf "colorchannelmixer=0:0:1:0:0:1:0:0:1:0:0:0" \
  output.mp4

# Boost reds, reduce blues
ffmpeg -i input.mp4 \
  -vf "colorchannelmixer=1.2:0:0:0:0:1:0:0:0:0:0.8:0" \
  output.mp4
```

## Professional Grading Chains

### Film Emulation

```bash
# 35mm Film Look
ffmpeg -i input.mp4 \
  -vf "\
    eq=contrast=1.1:saturation=0.95:gamma=1.05,\
    curves=preset=cross_process,\
    colorbalance=rs=0.05:bh=-0.05,\
    noise=c0s=3:c1s=3:c0f=t:c1f=t,\
    unsharp=3:3:0.5" \
  -c:v libx264 -crf 18 film_look.mp4

# Kodak Portra Style
ffmpeg -i input.mp4 \
  -vf "\
    eq=saturation=0.9:contrast=1.05,\
    colorbalance=rs=0.1:gs=-0.02:rm=0.05:gm=-0.02,\
    curves=r='0/0.02 1/0.98':g='0/0 1/1':b='0/0.02 1/0.95'" \
  output.mp4

# Fuji Film Style
ffmpeg -i input.mp4 \
  -vf "\
    eq=saturation=1.1:contrast=1.05,\
    colorbalance=gs=0.05:bs=0.08:gm=0.02:bm=0.05,\
    curves=g='0/0.02 1/1'" \
  output.mp4
```

### Modern Cinematic

```bash
# Blockbuster Orange & Teal
ffmpeg -i input.mp4 \
  -vf "\
    eq=contrast=1.15:saturation=1.1:brightness=-0.02,\
    colorbalance=rs=0.12:gs=-0.04:bs=-0.15:rh=0.08:bh=-0.12,\
    curves=all='0/0.02 0.5/0.5 1/0.98',\
    unsharp=5:5:0.6" \
  -c:v libx264 -crf 18 cinematic.mp4

# Moody/Dark Cinematic
ffmpeg -i input.mp4 \
  -vf "\
    eq=contrast=1.2:brightness=-0.08:saturation=0.85,\
    colorbalance=bs=0.1:bm=0.05:gh=-0.05,\
    curves=all='0/0.05 0.5/0.45 1/0.9'" \
  output.mp4

# High Key Bright
ffmpeg -i input.mp4 \
  -vf "\
    eq=contrast=0.9:brightness=0.1:saturation=0.9:gamma=0.85,\
    colorbalance=rs=0.05:gs=0.02:bs=0.02" \
  output.mp4
```

### Music Video Styles

```bash
# Neon/Cyberpunk
ffmpeg -i input.mp4 \
  -vf "\
    eq=contrast=1.3:saturation=1.5:brightness=-0.05,\
    colorbalance=rs=0.2:bs=0.2:rm=-0.1:bm=0.15,\
    unsharp=5:5:1.0" \
  output.mp4

# VHS/Retro
ffmpeg -i input.mp4 \
  -vf "\
    eq=saturation=1.2:contrast=0.95,\
    chromashift=cbh=2:cbv=2,\
    noise=c0s=10:c1s=5:allf=t,\
    curves=preset=vintage" \
  output.mp4

# Dream/Ethereal
# Studio fix: blend in RGB (format=gbrp). Screen-blending YUV planes pushes the chroma and turns warm footage magenta
# (measured R-B −8 vs the source); in RGB the warmth holds.
ffmpeg -i input.mp4 \
  -filter_complex "\
    [0:v]format=gbrp,split[a][b];\
    [a]gblur=sigma=15,eq=brightness=0.1[blur];\
    [b][blur]blend=all_mode=screen:all_opacity=0.3,format=yuv420p[out]" \
  -map "[out]" -c:v libx264 -crf 18 dream.mp4
```
The same applies to any `blend=all_mode=` other than a weighted average (screen, overlay, softlight, multiply): convert to `gbrp` first.

## Animated Color Effects

### Time-Based Color Changes

> **Studio fix:** `colorbalance` and `colortemperature` don't accept expressions (`t`), so the upstream recipes error out. Animate them with `sendcmd` instead. `eq` evaluates its expressions only once unless you add **`eval=frame`**: without it the "change over time" never moves. `hue` evaluates every frame by default. All of the recipes below were tested.

```bash
# Gradually warm over 30 s (colorbalance via sendcmd; TI runs 0→1 across the interval)
ffmpeg -i input.mp4 \
  -vf "sendcmd=c='0-30 [expr] colorbalance rs 0.1*TI',colorbalance" \
  output.mp4

# Pulsing saturation (hue takes expressions per frame)
ffmpeg -i input.mp4 \
  -vf "hue=s='1+0.3*sin(t*2)'" \
  output.mp4

# Day to night over 30 s
ffmpeg -i input.mp4 \
  -vf "\
    sendcmd=c='0-30 [expr] colortemperature temperature 8000-3000*TI',colortemperature,\
    eq=brightness='-0.2*t/30':saturation='1-0.3*t/30':eval=frame" \
  output.mp4
```
Note: in ffmpeg's `colortemperature`, a **lower** temperature makes the image **warmer** (tested: 5000 K raised R−B from +51 to +56; 8000 K lowered it to +41).

## Troubleshooting

### Common Issues

**Banding in gradients after grading:**
```bash
# Add dithering
ffmpeg -i input.mp4 \
  -vf "lut3d=lut.cube,format=yuv420p10le" \
  -c:v libx264 -profile:v high10 -crf 18 output.mp4

# Or add subtle noise
ffmpeg -i input.mp4 \
  -vf "lut3d=lut.cube,noise=c0s=2:c0f=a" \
  output.mp4
```

**Color shift after encoding:**
```bash
# Force color space flags
ffmpeg -i input.mp4 \
  -vf "your_filters" \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:v libx264 -crf 18 output.mp4
```

**Chromakey green fringe:**
```bash
# Use despill with colorbalance
ffmpeg -i green_screen.mp4 -i bg.mp4 \
  -filter_complex "\
    [0:v]chromakey=0x00FF00:0.25:0.1,\
    colorbalance=gs=-0.15:gm=-0.1[fg];\
    [1:v][fg]overlay" \
  output.mp4
```

This guide covers FFmpeg color grading and chromakey operations. For transitions see `ffmpeg-transitions-effects`, for shapes see `ffmpeg-shapes-graphics`.
