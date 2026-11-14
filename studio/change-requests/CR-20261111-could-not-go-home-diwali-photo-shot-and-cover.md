# CR-20261111-could-not-go-home-diwali-photo-shot-and-cover

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 (project.md; the studio was at v0.10.2 during the late rounds) |
| Type | script |
| Severity | workaround |
| Status | open |

## What happened
After approving v4e, the director asked for a different last shot: "a middle-aged man bursting a cracker".
- I searched Pexels and Pixabay video and Pexels and Unsplash photos, over 30 queries, about 25 min. No free video has one.
- The ladder's step 3 (a real photo with a slow push) gave the answer: Pexels photo 5882889.
- Three tools didn't fit along the way.

1. **`conform_clip.py --push` can't make this shot.**
   - It makes a centred `zoompan` to a full 1080×1920 frame. ffmpeg's zoompan steps in whole pixels, so a slow push jitters.
   - It has no option for a windowed reel (4:3 here) and can't hold a chosen point (the hands and the flame) still while it pushes.
2. **The pregate has no span type for a photo.** `frame_scan` FAILed the shot as "frozen 27.04–28.48 s (0.11)". The nearest type is `freeze`, so the span went in as `26.96-28.56:freeze`. A photo push isn't a freeze, and the reviewer's strip index calls it one.
3. **No cover tool.** The cover has to be a full 9:16 frame from the camera file, with the reel's grade and title (instagram-strategy.md). Kolkata did it by hand too (CR-20261108-kolkata-cover-title-type).
   - **Orientation:** ffmpeg PNG grabs of the Apple Cinematic clips came back sideways when read again; they carry a display-matrix rotation of −90. Decoding to raw RGB with `-noautorotate` gives the upright frame.
   - **Grade:** fitting the colour curve on the cover crop itself pushed the skin red.

## Workaround used in the reel
1. **The push is in Premiere, on a 4:3 crop of the photo.**
   - The crop is saved as a PNG (`renders/stock_v4f/S31_man_cracker_4x3.png`).
   - Scale goes 42.2 → 43.9 (×1.04), linear. Position keys come from p = P + (p0 − P)·r, so the point P (the hands) stays still.
   - The window coverage is checked at both keys (`analysis/es/build_v4f.jsx`).
2. The span went in as `--designed 26.96-28.56:freeze`. The reviewer judged its strip.
3. **`tools/make_cover_v4f.py`** makes the cover.
   - It decodes the bake frame as raw rgb48 with `-noautorotate`.
   - It takes the 9:16 crop around the subject.
   - It fits a per-channel quantile curve (24 knots) from the camera region the reel's window shows to the reel's own render of the same moment, then applies it to the crop. The cover carries the reel's exact balance and look, with no second grade.
   - It sets the title in the reel's type (`make_type_v4d.py`), and draws the 3:4 grid lines on the review sheet.

## Proposed change
1. **`scripts/conform_clip.py`, still input:**
   - add `--window x,y,w,h` (a windowed reel) and `--hold x,y` (the point that stays still);
   - render the push with sub-pixel scaling at 2× and then downscale, not `zoompan`;
   - or document the Premiere recipe above in `premiere-mcp-reality.md` and have the tool write only the crop PNG plus the Scale/Position keys.
2. **`scripts/pregate.py`:** a `photo` span type that expects `frozen`, and that `motion_audit` checks for a smooth push: the scale step per frame is constant and the hold point drifts ≤ 1 px.
3. **`scripts/make_cover.py`** (studio-wide; it would also close the cover half of CR-20261108-kolkata-cover-title-type):
   - input: a camera clip or bake plus a time, the reel's export plus the matching frame, a crop centre, and the title text and type;
   - decode raw with `-noautorotate`;
   - fit the grade on the window region;
   - write the 9:16 cover and a grid-crop check sheet.
4. **`effects-playbook` / `motion-and-ai.md` ladder step 3:** when the photo is portrait and the reel is windowed, the crop and the push are set in the 4:3 window, and the hold point is the action.

### More evidence (2026-11-12, after approval)
- **The director rejected the approved package's cover:** "use a better picture and typography and font style which will fit in my Instagram feed based on the previous post."
- **The miss.** The cover was designed as a frame from this reel, with the reel's own type (Avenir) set as a subtitle line. It didn't fit the feed, where every earlier cover follows one pattern:
  - one cinematic subject;
  - a title in the upper third, inside the grid crop;
  - one of two type families: DIN Condensed caps + a tracked sub-line (Pujo, Uski), or Didot caps + italic (Goddess).
- **The rework.** I read the five earlier covers by hand and wrote `tools/cover_v10.py` (four options + `feed_mock.jpg`, each option in a mock grid of the earlier covers). That makes the cover tool the fourth reel-local one (Pujo `cover_design.py` / `cover_cine.py`, Uski `cover_r9.py`, Goddess `cover_cinematic.py`, this reel `make_cover_v4f.py` / `cover_v10.py`).
- **Proposed in addition to 3:**
  - the cover tool reads the feed (the earlier reels' `deliver/cover.jpg`) and offers the feed's type families by default;
  - it always renders the feed mock, so the director judges the cover in the grid, not alone.
- **Second rejection (same day):** the feed-style pick B1 (the car washer, daytime) was "not festive enough". The director asked for "a free stock image of a man looking at crackers", liked C2 (the reel's own Pexels cracker photo, Didot white + gold), then picked **D5** from an 8-photo Pexels board (Pexels 19467413, a young man with a sparkler; `tools/cover_v10c.py`). ~30 min more.
  - **Proposed in addition:** the cover tool's option set always includes one frame that names the occasion at a glance (a flame, a sparkler, the idol), and offers a stock photo when the director's own frames don't. A cover photo that isn't in the reel is credited in the caption.

## HQ decision
<!-- HQ fills this in. -->
