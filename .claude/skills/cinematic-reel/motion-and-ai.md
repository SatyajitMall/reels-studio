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

## 3. AI-generated video (OpenRouter → Google Veo 3.1 Lite, no audio)
**Policy** (director, 2026-10-18):
- **Only** for shots the director's own footage can't provide.
- **Never** for the subject itself (the idol, the people).
- Every generated shot is listed in `brief.md` as **"AI-generated"**, with its prompt, why it's needed and its cost. The director approves it at **Checkpoint 1**, and approves the chosen draft before its final.
- **No raw footage is ever sent.** At most one or two stills from the director's footage go up as first or last frames, to anchor the look. Everything else (selects, motion, QA, cut-outs, graphics) runs locally and free; the reviewer sees only contact sheets.

**Cost structure** (`studio/ai-budget.json`; `scripts/gen_video.py` enforces it before sending anything):

| | Settings | Cost |
|---|---|---|
| **draft** (default) | 720p · 4 s · no audio · Veo 3.1 Lite | ≈ $0.12 |
| **final** | 1080p · 8 s · no audio · Veo 3.1 Lite | ≈ $0.40 |
| per shot | at most 3 drafts + 1 final | ≈ $0.76 |
| per reel | at most **$2**, **2 final shots**, **16 s** of generated footage (and keep it under 25 % of the runtime) | |
| per month | at most **$10** (about 5 reels with AI shots) | |

- Audio is **off** by default: reels use the director's music, and audio costs about 60 % more on Lite.
- Prices are read **live** from OpenRouter on every run.
- The ledger (`studio/ledger/ai-spend.jsonl`) records the **actual** charged cost that OpenRouter reports per job.
- Failed generations aren't charged and don't count.

**How:**
1. Pick a still from the director's footage that the shot should continue from (optional, but it cuts retries). Export it with `ffmpeg -ss <t> -i <clip> -frames:v 1 still.png`.
2. Dry run: `./.venv/bin/python scripts/gen_video.py --reel <reel> --shot <name> --why "<why footage can't>" --prompt "<prompt>" [--first-frame still.png]`. It prints the cost and every cap, and spends nothing.
3. Put the shot and its draft cost in the brief, and get the director's yes. Run the draft with `--yes`.
4. Show the draft. On a yes, run the final: `--mode final --yes`.
5. The file lands in `projects/<reel>/renders/gen/<shot>_<mode>_<time>.mp4`, with a `.json` sidecar (prompt, cost, the "AI-generated" label).

**Fallback:** `--provider google` uses the Gemini API directly (`GEMINI_API_KEY`). Google always bills audio (Lite 1080p $0.08/s), so a final is about $0.64. Use it only if OpenRouter is down.

**Facts:**
- 9:16 is supported, at 4, 6 or 8 s.
- Every clip has Google's **SynthID** AI watermark.
- OpenRouter's video generation isn't eligible for zero data retention: providers keep outputs briefly.
- Google direct deletes videos after 2 days.
- Typical generation time is 30 s to a few minutes.

**Verified (2026-10-18, first real call, $0.12):**
- OpenRouter charged exactly the estimate.
- The output was 9:16 (720×1280), exactly 4.0 s, with **no audio track** (audio off is honoured).
- A `data:` URL first frame works: output frame 0 matched our C027 still (mean difference 0.6 on 0–255).
- The motion was a smooth push; `frame_scan.py` found 0 flags.
- **Veo outputs 24 fps.** Conform it to the reel's rate on import (`set_override_frame_rate`, as for 24 fps camera clips), or the sequence will repeat frames.
- Veo may "clean up" small details from the first frame: in the test it dropped a phone in the corner. Check the draft against the source still.

**Then:** primary-correct and match the generated shot like any other clip, and run it through the review gate like everything else.
