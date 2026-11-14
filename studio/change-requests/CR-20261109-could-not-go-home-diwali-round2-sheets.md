# CR-20261109-could-not-go-home-diwali-round2-sheets

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 |
| Type | script · rule |
| Severity | workaround |
| Status | open |

## What happened
Round 2 asks for "show, don't name" choices. There's a tool for looks (`look_preview.py`), but none for the other two visual choices this reel needed.
- **Framing for landscape footage.** effects-playbook §B lists full-bleed, a 16:9 film frame and a 4:5 window. The reference used a **4:3 window**: 75 % of the camera width, with room for text in the black band below. The director picked it.
- **Title and type.** KOLKATA's CR-20261108-kolkata-cover-title-type (a title tool and a font library) is still open. This reel needed a title sheet and a letter-line style sheet in Round 2.
- PIL in `.venv` has **no raqm**, so Devanagari (and Bengali) can't be shaped. Titles stayed in Roman script, which the director's Hinglish choice allowed.

## Workaround used in the reel
Two reel-local tools:
- `projects/could-not-go-home-diwali/tools/framing_sheet.py`: 1080×1920 phone mockups of R 4:3 / C 4:5 / B 16:9 / A full-bleed on the director's own (depth-baked, upright) stills. It shades the IG bands (top 220, bottom 320, right 120), states "% of width kept", and places a sample line where each option would carry it (black band below the window when there's room, on the picture otherwise).
- `projects/could-not-go-home-diwali/tools/type_sheet.py`:
  - titles × 8 faces (Baskerville Italic, Didot Italic, DIN Condensed Bold, Snell Roundhand; Yatra One, Rozha One, Amita Bold, Eczar from `assets/fonts/`), cream `#F5E6C8` with a soft gold glow on a blurred dark frame of the reel;
  - 4 letter-line styles on a 4:3 phone frame.

The director chose from the sheets in one message each: 4:3, Rozha One, Baskerville Italic.

## Proposed change
1. **effects-playbook §B:** add **R: 4:3 window** (1080×810, centred in the safe area, 75 % of the width; text below the picture) to the landscape options, with "a reference's own frame" as a reason to pick it.
2. **`scripts/framing_sheet.py`:** promote the tool and call it in the skill's Round 2 next to `look_preview.py`.
3. **`scripts/type_sheet.py`:** promote it, or fold it into the title tool from CR-20261108-kolkata-cover-title-type, with a running-text (letter / subtitle) style row as well as titles.
4. **Complex scripts:** install Pillow with raqm (`brew install libraqm` + reinstall Pillow), or render Indic type through HyperFrames (browser shaping). Add a check to `setup.sh`.

## HQ decision
<!-- HQ fills this in. -->
