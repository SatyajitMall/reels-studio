# Playbook: cinematic-montage

**For:** music-driven montages of places, festivals and events, with no speech (reel type `music-montage`; the montage stretches of a `hybrid`).
**Proven on:** my-reel (Durga Puja night, v10 final, 49.8 s) and puja-night-2 (v5, 55.6 s). Each rule cites its source.

## Pace and structure
- **The music decides the timing.** Get the beat grid first (`gemini_audio_and_beat_analyzer.py`); cuts land on beats, and section changes and hero shots land on accents or bar downbeats (CLAUDE.md §4c).
- **An energy arc, never one shot per bar.** Default arc: slow open → build → full → breath → payoff → outro. *Why:* my-reel v1 cut one shot per bar and read as mechanical, and you reopened it 5 times.
- **A slow open is allowed when the brief says so**, instead of a hard 3 s hook. *Source:* the director approved slow builds on both reels. Even then, something must move from frame 1, such as a push or a tilt.
- **Shot length:** take the reference's measured median as the target (`teardown.py`). Both reels landed at a median of about 1.6–1.8 s, with holds of 3–5 s on hero shots.
- **Pick the best moment, not the whole clip** (`selects_score.py`, then check by eye). Never repeat a subject or framing. *Source:* the v8 review flagged the same carved panel used twice, 9 s apart.

## Camera and motion
- **Handheld footage: no impact shakes or snap zooms.** They read as jumps on top of real hand movement. *Source:* my-reel round 2.
- **Digital push or pull only on steady holds** (`motion_holds.py`): 100→104–110 % over the shot, eased.
- **Stabilise handheld moves** with Warp in Premiere, then re-measure with `shake_report.py` and scan for Warp banners.
- **Slow-mo:** use Timewarp (After Effects) or Optical Flow only on calm shots. Check fast or crossing motion for ghosting. *Source:* the C076 smear in v8.

## Type and graphics
- **A title and an end card only**; beat words only when the director supplies words that mean something. *Source:* the v1 words "DUM · DUM · DURGA" read as meaningless.
- **Animated title** with HyperFrames: focus-pull settle, the profile's DIN Condensed Bold in cream, gold glow (or a dark halo for a calm reel), placed per shot and **never on the subject** (`motion-and-ai.md` §1).
- **Text behind the subject:** at most one signature moment, on a steady hold of an idol or person against a contrasting background (`text_behind.py`). *Source:* "MAA" behind the folk Durga in puja-night-2.

## Transitions
- **Hard cut by default.** Signature transitions are a flash or a 3-frame dip to white on a big hit, a whip on fast motion, and a dip to black at the end.
- **Never stack decorative looks**: no light leaks plus rays plus particles, and no Premiere *Light Leaks* transition (it strobes). *Source:* the v8 review and the pilot's QA. Dissolves only where the brief asks for them.

## Sound
- **The music leads.** Peaks −1…−3 dB, no ducking; natural sound muted or at −20 dB or quieter (CLAUDE.md §4c).
- **Swishes and whooshes: yes, but only on real fast motion**: a whip, a fast pan, a snap move or a flash transition. **Never under text or titles, and never just because a shot starts.** At about −13 dB in the mix, the level the director asked for in puja-night-2 ("louder swishes": raised from −18/−17 to −13 dB).
- **Risers into the big hits.** A sub-boom or bass drop on the 1–2 biggest accents, at −15…−18 dB.
- **Prepare every SFX** with `sfx_prep.py` (trim leading silence, peak −3 dBFS), and place it by its **transient**, not its file start.
- **Mixed version:** −14 LUFS ± 2, true peak ≤ −1 dBTP (`verify_render.py`; `--fix-loudness`). The IG version without music is judged on peak only.

## Colour and texture
- **Grade toward the warm, deep look of night festivals:** gold midtones (hue 30–45° on warm shots, `colour_report.py --gold`), blacks kept deep, blue accent shots kept clean (G−M ≈ 0).
- **Warm looks push red:** fix it with the look layer's temperature plus a little green tint, never by cooling the clips.
- **Grain 10–15 %, faded with the picture.** *Source:* 40 % was "too much grain" in my-reel round 2.
- **Denoise dark shots** in After Effects (`denoise`) when the frame scan or your eye shows noise. *Source:* my-reel v7, −12…−29 % dark-area noise.

## AI shots
- Rarely needed: both reels had **no gap** the footage couldn't fill. If one is needed, follow the policy in `motion-and-ai.md` §3, and never generate the idol or the crowd.

## QA thresholds for this style (review gate)
- Shot luma within ±0.03 of the montage median, unless a shot is a deliberate dark establisher or a blue accent.
- No phones, raised hands with screens, or bald heads drifting into hero frames. Reframe or mask them. *Source:* the most common review finding on puja-night-2.
- Every cut within ±2 frames of its beat, except deliberate off-grid holds noted in the brief.
