# CR-20261112-could-not-go-home-diwali-stock-ai-blend

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.10.3 |
| Type | script + skill + reality doc |
| Severity | workaround (about 70 min, two renders and two sequences) |
| Status | open |

## What happened
After approving v8b, the director looked again at the two shots that aren't theirs:
- 12, a Pexels diya close-up;
- 19, a Veo shot of a man with a cracker fountain.

Both are slowed 50 % with AE Timewarp. The director's note: "Looks a little fake ... a little different from rest of the footage ... the hand is not shaking, not moving, and the pan looks too good to be true. Don't need to change it, but optimise it so they blend."

The studio has no route for this. `conform_clip.py` matches frame rate, size and colour. Nothing measures or matches:
- **how the camera moves:** a stock slider rise or a Veo glide against the director's stabilised phone handheld;
- **grain:** Veo is about 3× cleaner than the director's night clips;
- **crispness.**

The AI-shot ladder (`motion-and-ai.md` §3) and the `film-emulation-prompts` skill shape a shot before it is made. Nothing helps once a stock or AI shot is in the cut.

### Workaround (reel-local)
1. **`tools/measure_blend_v10.py`:** per shot, inside the window, on the export:
   - camera wander: the outer-ring path (`motion_audit.ring_shift`) minus its straight line;
   - fine shake: the path minus a 6-frame gaussian;
   - grain: luma minus its 3×3 median, std over the flattest 30 %;
   - detail: p90 of |Laplacian|.

   Real shots measured: wander 0.2–1.1 px, shake 0.1–1.3 px, grain 0.33–0.66. 12: 0.54 / 0.21 / 0.47. 19: grain 0.16.
2. **`tools/blend_v10.py`:**
   - **Motion.** The director's own handheld camera path, taken from five real shots of the same reel (detrended, chained, ×1.25), is added to the stock or AI clip as a sub-pixel move inside a 2 % zoom. Window px are converted to source px through the clip's Premiere scale.
   - **Grain.** Luma grain (σ 0.6) is added, stronger in the shadows, with weaker chroma grain. The amount is solved from the export/source grain ratio.
   - **19 only:** a 0.5 px luma softening.

   The output replaces the clip's media, keeping its keys and Lumetri (read back).
3. **Result:**
   - 12: wander 1.15, shake 0.48, grain 0.45;
   - 19: grain 0.37, after a second pass (see 4).

   Pregate PASS; review in `analysis/review_v10.md`.

### Gaps hit
1. **No blend tool.** The two scripts above are the proposal.
   - Promote them as `scripts/blend_insert.py <clip> --like <export> --shots <real shots> --scale <premiere scale>`, with the measure step as `--report`.
   - Add a line to `motion-and-ai.md` §3 and to the stock intake: every stock or AI insert gets the reel's own handheld path and grain before review.
   - The director noticed both shots after approval. A pregate check comparing an insert's grain and shake with the real shots' range would have flagged 19 (grain 0.16 against 0.33–0.66) earlier.
2. **The grain solve misses after Premiere sharpening.**
   - The export/source ratio was measured on content, but Sharpen −30 removes fine grain much more than content. The added grain landed at 0.20 instead of 0.48.
   - **Proposed:** solve against a test export of the clip, or add grain after the grade (a V4 grain overlay per insert, effects-playbook §A4), which avoids the clip's own Lumetri.
3. **Reality doc: ES3 reserved words.**
   - `{new: x}` makes `$.evalFile` fail with only "ExtendScript execution failed via CEP evalScript()": no line and no output file.
   - `node --check` accepts it.
   - **Proposed:** a note in `premiere-mcp-reality.md` (quote keys, or avoid `new`, `class`, `default`, `delete`, `in`), and a check in any jsx lint the studio adds.
4. **The review gate can run on the editor's model.**
   - `.claude/agents/reel-reviewer.md` has no `model:` in its frontmatter, so it inherits the session's model unless the call sets one.
   - The v10b review ran on Opus 5.5, the editor's model. The reviewer noticed and said to throw it away, and it was re-run on Fable.
   - **Proposed:** pin `model:` in the agent's frontmatter to a model other than the studio's editor default. Also make review-gate.md step 3 a hard check: the reviewer's first line names its model, and the editor rejects a match.
