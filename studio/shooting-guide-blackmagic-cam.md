# Shooting guide: Blackmagic Cam on iPhone

One page for the director, before a shoot. It's built from the 329 clips of the Pujo 2026 nights, as measured by `scripts/ingest_report.py` on 2026-10-27. Every rule fixes something that cost editing time.

**What the camera gave us:** HEVC, **8-bit**, Rec.709, about 56 Mb/s, from Blackmagic Cam 3.5 on the iPhone 17.
- **Frame rates:** five different rates (25, 30, 24, 24.9, 23.976), even within one night.
- **Flicker:** **144 clips flicker** under lamps (30 fps at a 1/60 s shutter).
- **White balance:** **93 of the 123 clips set at 5600 K came out orange** under warm pandal light.
- **Variable frame rate:** 10 clips; one dropped 15 frames and jumped mid-shot.
- **LUT:** whether a LUT was burned in is **not saved in the file**.

## Set once, before the night
| Setting | Use | Why |
|---|---|---|
| **Frame rate** | **25 fps** for everything, all night | One rate means no conforming. 25 fps can't pulse under India's 50 Hz lamps |
| **Shutter** | **1/50 s** (shutter as speed, not auto) | 1/50 s takes in exactly two lamp pulses per frame (lamps pulse 100 times a second), so the picture neither pulses nor bands. **Never 1/60 under Indian lights** |
| **Slow-motion moments** | **50 fps at 1/100 s**, then back to 25 | Only footage shot at 2× the reel's rate slows cleanly. Synthesised slow motion failed on 2 hero shots this season. 1/100 s is still pulse-free |
| **Resolution** | 4K, phone held vertical | The app stores it landscape with a rotation flag. Premiere and our tools handle that |
| **Holding the phone landscape** | Avoid for reels. If you do, check the orientation lock (the iPhone's or the app's) is off, or write "landscape" in the slate Notes | KOLKATA2026 was shot mostly landscape, but every clip was tagged portrait and lay on its side; nothing in the files said which way up, so 101 clips were sorted by eye. A landscape shot also shows only a third of its width in 9:16 |
| **Codec** | **HEVC 10-bit, or Apple Log, if your app version offers it**; otherwise HEVC at the highest bitrate | 8-bit bands and blocks when graded. 10-bit has four times as many levels per colour, so grades stay smooth. Apple Log needs a log → Rec.709 conversion in the edit, which the studio hasn't tested yet: **tell HQ before the first log shoot** |
| **Cinematic mode** | Fine to use for depth. The f-number can be changed after the shoot, and the recorded focus is kept | The blur isn't in the picture: Apple apps draw it from a depth track, so on the Mac it looks sharp until the studio bakes it (`cine_bake`, Diwali). It records 8-bit HEVC like the normal mode. Slowed shots of hands or tools crossing the focus shimmer at f/2; f/2.8 is safer there |
| **ISO** | As low as the scene allows; above 1600 only when there's no other way | 75 clips were shot at ISO 1000 or more. In 8-bit, noise turns into blotches in dark areas |

## Every new location
1. **White balance: set it to the light and lock it.** Pandal and tungsten lamps: **3200 K**. Mixed LED street light: 4000–4500 K. Daylight: 5600 K. Unsure? Set it off a sheet of white paper. Never leave 5600 K under warm lamps.
2. **Protect the highlights.** Expose so lamps, idols' faces and gold keep detail. A slightly dark night is fine; blown gold and crushed black can't be brought back in 8-bit.
3. **LUT: for the monitor only.** Use it to judge the look, but don't burn it into the recording. If you do burn one in, **type its name in the clip's slate Notes** (or Project name). The ingest check reads it there; otherwise nobody can tell later.

## Every shot
- **Hold 5–10 s, with one camera move per shot.** The edit picks its best second, and a cut needs handles on both sides.
- **Main 26 mm lens** for most shots; 13 mm for wide pandals; 52 mm for faces. No digital zoom.
- **Turn on the app's stabilisation** when walking, and keep the phone steady for holds. Warp in Premiere can't fix a jerk.
- **Record 10 s of ambience** (dhak, crowd, conch) at each place. The sound mix uses it.

## After the shoot
Copy the card into `~/Documents/Video /<Pujo YYYY Mon DD>/` as now (the app's `Proxy` folder can stay; the studio skips it). Each reel session runs `scripts/ingest_report.py` on its clips in Phase 1. It reports what's above for every clip, and measures flicker and jumps frame by frame.
