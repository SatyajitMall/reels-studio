# CR-20261108-kolkata-stock-intake

| Field | Value |
|---|---|
| From reel | `projects/kolkata/` |
| Arch version | 0.9.0 |
| Type | script · skill |
| Severity | workaround |
| Status | partly done (v0.9.1) |

## What happened
KOLKATA used free stock where the director's footage couldn't tell the story. The director asked for it in round 5: "use free video from online". 13 of 26 shots are stock (51 % of the runtime): Pexels and Unsplash, all logged in `projects/kolkata/raw/SOURCES.md`. Three problems repeated.

1. **No stock search tool.**
   - `.env` has `PEXELS_API_KEY=` empty, and the studio has no search script.
   - Every search went through Chrome instead:
     - search-page HTML for the IDs;
     - `__NEXT_DATA__` for size, fps, length and author;
     - screenshots to check what's actually in the clip.
   - Each search took 15–40 min. Rounds 2, 5, 6b, 6c, 6d and 7 each needed one: tram, bus, ghat, Kumartuli.
   - Pexels titles can be wrong: "Howrah Bridge" 27496938 is a different bridge.
   - Logged in the friction log as "no CR yet" twice.
2. **Doubled frames in "60 fps" stock.**
   - Pexels 39276190 (the flower seller) is 45 fps footage up-converted to 60: every 4th frame is a repeat.
   - Interpreted to 25 fps for slow motion, it hitched every 0.16 s.
   - It was in the reel from round 5 to round 7 before the review gate caught it.
   - `ffmpeg mpdecimate` didn't drop the repeats (encoder noise kept them above its block thresholds).
3. **Photos before AI.** Free stock video had no running Kolkata tram front-on, but free stock photos had about 200 (Unsplash). $0.64 went on an AI tram before the director asked for a photo.

## Workaround used in the reel
- Chrome searches, with every pick checked by eye on a candidate sheet through the reel's 4:5 window (e.g. `analysis/round7_kumartuli_pool.jpg`).
- **Repeated-frame fix:**
  - measure the mean absolute difference between consecutive frames (270×480 grey);
  - a value under 1.0, against about 8 for real motion, is a repeat;
  - drop those frames by index with `select`, write the result at the true rate (45 fps), and interpret it to 25 fps;
  - result: `renders/fx_preview/stock_flower_seller_dedup45.mov`, 81 unique frames.

## Proposed change
1. **`scripts/stock_search.py`** (Pexels API, plus the Pixabay API where a key exists):
   - query → a contact sheet of candidates through the reel's frame;
   - per clip: id, author, size, fps, length and licence;
   - `--download` writes to `raw/stock/` and appends to `raw/SOURCES.md`;
   - also searches **photos**.
   - `setup.sh` asks for the free API key.
2. **Repeated-frame check on intake:** `ingest_report.py`, or `conform_clip.py`, flags clips whose consecutive-frame difference collapses periodically and reports the true rate. `conform_clip.py --dedup` writes the de-duplicated file at that rate.
3. **Skill / `motion-and-ai.md` §3, before proposing an AI shot:** search stock photos too (a still with a slow push can carry a line). Record the photo search in the AI row of the brief.

## HQ decision (v0.9.1, 2026-11-08)
- **(3) Done.** `motion-and-ai.md` §3: when the director has allowed stock, search free stock video **and photos** before proposing an AI shot, and record both searches in the brief's AI row.
- **(1, 2) Accepted for v0.11:** `scripts/stock_search.py` (Pexels API, video and photos; the director adds the free key to `.env`), and a repeated-frame check on intake with `conform_clip.py --dedup`.
