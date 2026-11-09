# CR-20261108-kolkata-cover-title-type

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | skill · script · asset |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
After approving the reel and the Instagram package (2026-11-08), the director rejected the cover and took a fourth round on the title. Their notes, verbatim:
> "Not the thumnail please look for a bvetter thumbnail" · "use better cinematic fonts" · "KOLKATA / The cityof / Culture Heritage and Surprises / thsi whoculd obe on the vdieo and teh thumbnail" · "Do not we have any better durga puja frames to use?" · "Find differnt indo western fonst"

Four gaps showed up:
1. **No cover step.** Phase 8 says only "the cover frame timecode". I offered a frame from the reel with the old title pasted on. The director wanted a designed cover: their own title text, a strong picture of the subject, and type with character.
2. **No title copy and no type choice before the build.** The brief had a one-word title ("Kolkata", Big Caslon, yellow with a red offset shadow). The director's real title, with a tagline, only came out at the package stage, so the video needed a re-export and two review runs.
3. **No font library.** This Mac has system fonts plus one Adobe font (Bebas Neue). The director profile's "bold condensed (Anton / Bebas)" was the only guidance. "Indo-western" type (Latin with an Indian hand, or with Bengali script beside it) needed free fonts downloaded from Google Fonts. Pillow here has no libraqm, so complex Bengali can't be shaped; কলকাতা happens to need no shaping.
4. **Instagram's profile grid is 3:4 now** (it was 4:5). A cover taken from our 4:5-window reel shows the black matte band in the grid crop. The cover has to be a full 9:16 picture.

## Workaround used in the reel
- `projects/kolkata/tools/make_title_v7.py`: a title card renderer (1080×1920 RGBA PNG, the V5 convention) with 10 styles.
  - Western: Didot, Bebas, Futura, Bodoni.
  - Indo-western: Rozha One, Yatra One, Galada, Eczar, Amita, Teko, with an optional কলকাতা line in Tiro Bangla or Galada.
  - Cream #F5E6C8, a soft shadow, and a soft dark band for bright backgrounds.
  - Lines are shrunk to fit x 120–960, and `--sheet` renders every style on given frames.
- Fonts in `assets/fonts/` (OFL, licence files beside them): RozhaOne, YatraOne, Eczar[wght], Galada, TiroBangla Regular and Italic, Amita Bold, Teko[wght].
- **Covers:** the camera frame at full 9:16, with the reel's look applied by ffmpeg (Eterna 3510 `.cube` at 30 %) and the title composited. Judged in the 3:4 grid crop (y 240–1680).
- **On the video:** the new PNG replaced the old title on V5, and the old keys were read and re-applied (`analysis/_es_title_v8.jsx`).
- **Two traps the reviewer caught:**
  - the title sat on the subject: the caps line rested on the record cartridge's printed label;
  - the shrink-to-fit quietly cancelled a requested +15 % size change.

## Proposed change
1. **Skill Phase 2 / Round 2:** ask for the **title copy** (the words, any tagline) and show a **type sheet** once there are stills: 3 western and 3 Indo-western styles, plus a Bengali or Hindi line where the reel is local. Record the choice in the brief. Move the director profile's "type style" to "ask per reel, default bold condensed".
2. **`scripts/make_title.py`** (promote `make_title_v7.py`):
   - styles in a JSON file in `assets/fonts/`;
   - `--sheet` mode;
   - the safe-zone check;
   - report the final size of any line it shrinks, so a size change can't vanish silently;
   - a `--avoid x0,y0,x1,y1` box for the subject (e.g. a printed label), so the title is placed clear of it.
3. **`assets/fonts/` as a studio library** with the OFL fonts above, and a README of what each is for. Install libraqm in the `.venv` (`brew install libraqm`, then rebuild Pillow) so Bengali and Devanagari shape correctly.
4. **Skill Phase 8, a cover step:**
   - 3–4 cover candidates: the strongest subject frames from the footage, not only from the cut;
   - full 9:16, the reel's look applied, the reel's title type;
   - shown in the 3:4 grid crop.

   `instagram-strategy.md`: note that the profile grid is 3:4 (and re-check it yearly), and that the cover is uploaded from the camera roll.

## HQ decision (v0.9.1, 2026-11-08)
- **(4, the grid) Done.** `instagram-strategy.md` has a Cover section: the profile grid shows a 3:4 crop (y 240–1680), the cover is a full 9:16 picture judged in that crop, uploaded from the camera roll.
- **Director profile done:** their own words on screen and on the cover, in type with character; ask for the title early with a type sheet.
- **(1, 2, 4 the Phase 8 step) Accepted for v0.10:** title copy and a type sheet in Round 2, `scripts/make_title.py` promoted from `make_title_v7.py` (styles JSON, `--sheet`, safe-zone check, reports any shrink, `--avoid` box), and a Phase 8 cover step.
- **(3) Fonts:** already in `assets/fonts/` with their OFL files; a README comes with v0.10. Bengali shaping: Pillow here reports no raqm. HQ will test `brew install fribidi` (Pillow's wheels load it at run time) with the director's OK, else use Batch C's HTML cards.
