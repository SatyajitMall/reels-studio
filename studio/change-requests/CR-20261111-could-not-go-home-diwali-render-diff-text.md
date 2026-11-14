# CR-20261111-could-not-go-home-diwali-render-diff-text

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.10.2 |
| Type | script |
| Severity | polish (a review scope could miss a real change) |
| Status | open |

## What happened
In v4 every letter line moved from the black band below the picture onto the picture. Pregate's `render_diff.py` (v4 against v3f) listed the changed spans as:

> 0.24–4.56, 4.88–9.36, 9.6–18.88, 19.16–23.68 s

It **omitted 23.80–28.56**, although L6 moved there too: v3f has band text at 24.5, 26.0 and 28.0 s; v4's band is empty there.

The reviewer caught it by hand (`analysis/review_v4.md`, notes). A focused review that trusted `diff.json` would have skipped the L6 span.

The likely cause: a mean-difference threshold over the whole frame. A small text block that moves (about 0.5 % of the frame) falls under it.

## Workaround used in the reel
The reviewer's prompt listed every changed line span explicitly, rather than relying on `diff.json`.

## Proposed change
`render_diff.py`:
- flag a span when **any region** changes, for example the max over a 16×16 grid of tile mean differences, or the share of pixels changed by more than 25, not only the whole-frame mean;
- report overlay/band regions separately from the picture window when `--window` is given.

## Added 2026-11-12 (v7): the spans end one frame early
The blind reviewer measured per-frame PSNR between v7 and v6c and found two misses:
- **render_diff's changed spans stop one frame before the change ends.** The last frames of 01 (1.52 s, PSNR 32.5 dB) and of 03 (4.64 s, 20.5 dB) changed, but fall outside the reported spans "0.0–1.56, 3.12–4.68". So the span edges are off by one at the end (or the span is built from cut times, not from the frames that differ).
- **A text change that starts a few frames before the picture change is reported late.** L4's fade-in starts at 14.40, but the span begins at 14.48.

**Proposed addition:** build the spans from the frames that actually differ (PSNR below a floor, e.g. 45 dB), padded by one frame on each side. Encoder noise in GOPs that share a changed frame read 52–57 dB here, so a 45 dB floor leaves it out.

## Added 2026-11-12 (v8b): a local change reported as "no picture change"
- v8b changed only the region over one man's head on shot 19, a soft mask about 300×450 px of the 1080×1920 source.
- Pregate's render_diff against v8 reported "same structure, audio identical; no picture change", so the gate said "no review needed".
- My own measure:
  - 77 of 80 frames differ in that region, mean 1.5 and max 3.5 levels;
  - over the whole window, the max frame mean is 1.85.
- A whole-frame (or whole-window) mean threshold can't see a fix aimed at one face. The editor's fix would have reached the director unreviewed if the editor had trusted the tool.
- **Proposed addition:** flag a span as changed when any 64×64 tile's mean |Δ| passes the threshold, not the frame mean. And never print "no review needed" when the editor rebuilt a clip in this version.

## HQ decision
<!-- HQ fills this in. -->

## Addendum (v4d, 2026-11-11)
- It happened again: `render_diff` (v4d against v4c) did not list 02, 03 or 15 as changed, although all six letter lines were restyled. The reviewer measured 28–30 dB PSNR on those shots.
- Second issue found by the same reviewer: the `strips/` tile timestamps read **one frame early** against ffmpeg's frame index and pts. The tile stamped 1.52 is the frame that plays at 1.56; at the end card, 28.64 is shown for 28.68. Fix: stamp `n / fps` from the decoded frame's own index or pts.
