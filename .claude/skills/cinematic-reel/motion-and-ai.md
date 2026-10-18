# Motion graphics, text behind the subject, AI video (skill Phases 2 and 5)

These are three capabilities HQ tested on 2026-10-18 (v0.5.1), inspired by the "Claude edits every video" workflow. Each one has a verified recipe and a known limit.

## 1. Motion graphics (HyperFrames → transparent overlay → Premiere V5)
**Use for:** animated titles, end cards, lower-thirds, stat or map hits, kinetic words. Short, designed and unnarrated.

**How:**
1. Load `/hyperframes`. It routes a short animated title to `/motion-graphics`, which runs a director subagent, then a builder subagent, then checks.
2. Make the project under `projects/<reel>/graphics/<name>/`. Before planning, write its `design.md` from `studio/director-profile.md`:
   - font, with a local file copied in (DIN Condensed Bold on this Mac);
   - palette: cream `#F5E6C8` + gold `#D4A017`;
   - no glitter;
   - safe zone;
   - **25 fps** or the reel's rate;
   - transparent background.
3. Check, then take proof snapshots, then render: `npx hyperframes render --format mov --fps <reel fps> -o renders/<name>-alpha.mov`. That gives **ProRes 4444 with alpha**. The HQ test rendered a 3 s 1080×1920 title in 7 s.
4. Composite-check it over the real shot before placing it: `ffmpeg … overlay` on an exported still.
5. Import it into Premiere on **V5**, above the grade.

**Learned:**
- **Placement is per shot.** The same y that sat clear on the blue Durga landed "2026" on the gold Durga's crown. Choose y from the frame it sits on.
- The `catalog` search finds blocks (e.g. `tracking-in`), so reuse them before hand-building.
- HyperFrames' usage allowance reads as "unknown" on this machine (unsupported auth), so don't guess it.
- **Not yet verified:** the Premiere import of the alpha MOV. Confirm on the first real use: transparency, and that the clip lines up on V5.

## 2. Text behind the subject (local, free)
**Use for:** one hero word passing *behind* the idol or person, e.g. "DURGA" behind the crown. It's a signature moment, at most once or twice per reel.

**How:** `scripts/text_behind.py <clip> --in <s> --dur <s> --text WORD --y <top px> [--x-shift] [--size] -o projects/<reel>/renders/behind/<shot>`.
- It cuts the subject out with HyperFrames' `remove-background` (CPU, about 4 frames/s), stacks the footage, then the glowing word, then the cut-out, and writes ProRes 422 HQ plus a compare strip. It also runs `frame_scan.py`, so any matte flicker gets flagged.
- Place the baked clip on V1 in place of the original shot, **before** colour. It's part of the image now, so it gets graded like the shot. That's intended, because the word lives *in* the scene.

**Where it works** (my-reel tests):

| Shot | Result |
|---|---|
| Idol or person, medium or close-up, contrasting background (blue Durga) | ✅ clean; stable over handheld; 0 scan flags |
| Wide shot, small subject | ⚠️ works, but little is occluded |
| Busy, ornate full-frame close-up (gold Durga) | ❌ the matte turns to mush |

**Limits:**
- The word is fixed to the screen, so only use it on **steady holds** (`motion_holds.py`).
- The model is trained on people, so check every new subject type on a still first. Running `remove-background` on a single `.png` takes seconds.

## 3. AI-generated video (Google Veo 3.1, Gemini API)
**Policy** (director, 2026-10-18):
- **Only** for shots the director's own footage can't provide.
- Every generated shot is listed in `brief.md` as **"AI-generated"**, with its prompt, why it's needed and its cost.
- The director approves them at **Checkpoint 1**.
- Never use it for the subject itself (the idol, the people): use the real footage.

**Budget:** `studio/ai-budget.json`, **$10/month**. Every paid call is logged in `studio/ledger/ai-spend.jsonl`. The script refuses any call that would exceed the month's remaining budget.

**How:**
1. Dry run: `./.venv/bin/python scripts/gen_video.py --reel <reel> --name <shot> --why "<why footage can't>" --prompt "<prompt>" [--model fast|lite|standard] [--res 1080p|720p] [--duration 8|6|4] [--negative ...] [--image first_frame.png]`. It prints the cost and the remaining budget, and spends nothing.
2. Put the shot and its cost in the brief, and get the director's yes.
3. Re-run with `--yes`. The file lands in `projects/<reel>/renders/gen/` with a `.json` sidecar (the prompt and the "AI-generated" label).

**Facts** (Google's docs and pricing pages, checked 2026-10-18):
- 9:16 is supported;
- 4, 6 or 8 s, with 1080p only at 8 s;
- Fast at 1080p is $0.12/s, so **≈ $0.96 per 8 s shot**; Lite is $0.08/s; Standard is $0.40/s;
- there's no free tier, so the key needs billing on;
- every clip has a **SynthID** AI watermark;
- Google deletes generated videos after **2 days**, so the script downloads immediately;
- latency is 11 s to 6 min.

**Not yet verified:** a real call. It needs the director's `GEMINI_API_KEY` in `.env`. Google's page also carries a note that video generation is "only available with the generateContent API", which contradicts its own REST examples (`predictLongRunning`, which the script uses). If the first real call is rejected, file a CR with the exact error.

**Then:** primary-correct and match the generated shot like any other clip, and run it through the review gate like everything else.
