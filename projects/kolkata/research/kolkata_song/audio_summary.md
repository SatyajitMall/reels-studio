# Audio Loudness & Beat Grid Analysis

## Music: `kolkata.wav` (A3)
- **Tempo:** 117.5 BPM · 1 bar = 2.043 s · 582 beats over 301.23 s
- **Beats detected:** 0.79 s → 300.28 s (outside that range there's no steady beat)
- **Strongest accents (s):** `9.89, 37.27, 95.2, 208.93, 229.16, 250.87, 293.71, 296.15`
- **Bar downbeats (every 4th beat; first 16):** `0.79, 2.81, 4.85, 6.9, 8.92, 10.94, 12.91, 15.0, 17.04, 19.04, 20.99, 23.2, 25.33, 27.19, 29.07, 31.14`

### Energy / sections
Heuristic labels from per-bar loudness relative to the loudest bar. Check by ear before committing a section.

| Section | Start | End | Length | Level |
|---|---|---|---|---|
| intro | 0.79 s | 27.19 s | 26.4 s | low |
| build | 27.19 s | 153.14 s | 125.9 s | mixed |
| drop / full | 153.14 s | 194.49 s | 41.4 s | high |
| breakdown | 194.49 s | 227.63 s | 33.1 s | mixed |
| full | 227.63 s | 246.22 s | 18.6 s | high |
| breakdown | 246.22 s | 252.42 s | 6.2 s | mid |
| full | 252.42 s | 281.33 s | 28.9 s | high |
| outro | 281.33 s | 300.28 s | 18.9 s | low |

### Candidate cuts
Start on a bar downbeat; end on the bar closest to the target length. Scored on energy, first hit ≤ 3 s in, a clean ending (section or track end) and starting on a 4-bar phrase.

| Target | Start | End | Length | First hit after | Mean energy | Clean end | Phrase start |
|---|---|---|---|---|---|---|---|
| 15 s | 231.76 s | 246.22 s | 14.46 s | 0.0 s | -1.8 dB | yes | yes |
| 15 s | 266.91 s | 281.33 s | 14.42 s | 0.0 s | -2.5 dB | yes | no |
| 15 s | 180.02 s | 194.49 s | 14.47 s | 1.05 s | -2.8 dB | yes | no |
| 30 s | 250.36 s | 281.33 s | 30.97 s | 0.51 s | -2.6 dB | yes | no |
| 30 s | 231.76 s | 262.78 s | 31.02 s | 0.0 s | -2.7 dB | no | yes |
| 30 s | 217.25 s | 246.22 s | 28.97 s | 0.0 s | -3.9 dB | yes | no |
| 45 s | 149.03 s | 194.49 s | 45.46 s | 2.04 s | -3.5 dB | yes | yes |
| 45 s | 235.89 s | 281.33 s | 45.44 s | 1.56 s | -2.7 dB | yes | no |
| 45 s | 231.76 s | 277.27 s | 45.51 s | 0.0 s | -2.5 dB | no | yes |
| 60 s | 223.52 s | 283.47 s | 59.95 s | 2.02 s | -3.1 dB | no | yes |
| 60 s | 186.22 s | 246.22 s | 60.0 s | 0.51 s | -4.5 dB | yes | no |
| 60 s | 149.03 s | 208.93 s | 59.9 s | 2.04 s | -3.7 dB | no | yes |

> Cut section changes and hero shots on accents or bar downbeats (CLAUDE.md §4c). Full per-bar energy is in `beats.json`.
