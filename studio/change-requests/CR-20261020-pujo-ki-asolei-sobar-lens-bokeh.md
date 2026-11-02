# CR-20261020-pujo-ki-asolei-sobar-lens-bokeh

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | script · skill · rule · setup |
| Severity | workaround |
| Status | rejected in part (v0.8.0) |

## What happened
The director shoots on an iPhone (Blackmagic Cam, 4K HEVC) and wants a cinema-lens look: "they don't have a bokeh on the back and they don't have a natural depth. You need to add that in post-processing." The studio had no depth tool. `hyperframes remove-background` only cuts out people, so the v1d "depth" was a person-matte defocus that read as mild blur. It couldn't treat idols, objects or near/far planes.

The director also wanted a strong look ("very sepia, filmy"), identical across shots shot under blue, green and orange light, and chose to have it **baked into each shot** rather than loaded as a LUT on the V3 adjustment layer (which CLAUDE.md §2.5 and §3 prescribe).

## Workaround used in the reel
- Director-approved downloads, kept reel-local: `onnxruntime` via `pip --target projects/<reel>/renders/_pylib` (the shared `.venv` stays untouched; the duplicate numpy was removed), and **Depth-Anything-V2-Small** ONNX (99 MB) in `renders/models/`. CPU is faster than CoreML here: 0.35 s vs 3.4 s per 518×924 frame.
- `tools/lens.py`:
  - per-frame relative depth, normalised with a per-shot fixed range;
  - circle of confusion from the distance to a per-shot focus point, with a minimum depth span (0.30) so near-flat scenes barely blur;
  - layered far-to-near anti-aliased disc blur (half resolution for big radii);
  - highlight boost in linear light, so lights become bokeh discs;
  - near layers composited last, so there's no bleed onto the subject.
- `tools/shot_render.py`: crop/reframe → exact 30 fps (fixes VFR clips) → per-shot neutral match (grey-world midtones + exposure, constant gains) → bokeh (depth EMA, median-filtered focus) → sepia look → halation, vignette, grain → ProRes 422 HQ + source audio, with handles. About 2 s/frame; 5 shots in parallel on 14 cores.
- Edges checked at 100 % (no halos) and `frame_scan.py` on every render.

## Proposed change
- Promote `lens.py` + `shot_render.py` to `scripts/` as `lens_bokeh.py` (a generic "treat a shot" renderer with pluggable looks), and add onnxruntime + the model to `setup.sh` (pinned sha256).
- Playbook §B / §A: add "Synthetic shallow depth of field (iPhone)", with when to use it (subjects with real depth separation), the focus-point config, and its limits (fast pans, thin structures).
- CLAUDE.md §2.5 / §3: allow a **baked look** when the director chooses it. Record the look parameters in the brief so a re-render reproduces it, and keep V3 empty in that case.

## Follow-up (end of reel, 2026-10-21)
- **Limit:** the director rejected the synthetic bokeh in round 2 ("not coming out ok"), even after review fixes (hero-only person matte, fill from out-of-focus pixels, per-shot floor and luma match). Monocular depth on night iPhone footage is plausible on stills but not convincing in motion. Keep it as an option, never the default.
- **What the director called "cinematic" instead:** correction, stability, clarity. `tools/shot_render_v2.py` adds:
  - hqdn3d at 4K (temporal-heavy) → lanczos supersample to a 10 % stabilisation margin;
  - a phase-correlation translation stabiliser (smoothed path; locked on holds; a background ROI where the subject moves);
  - fine detail + local-contrast clarity on luma;
  - white balance from near-neutral pixels + a per-shot tonal match;
  - grain 0.012.

  Measured: camera shake −21…−80 % on handheld shots (on the static background), sharpness +22 % to ×4, shot luma within ±0.006. ~100 s/shot. Fast handheld swings (~450 px/s) can't be stabilised: replace the shot. Proposed: promote as `scripts/shot_finish.py` (the stages as flags) and a playbook entry "Finishing iPhone night footage".
- **QA:** check first / mid / last frames of every baked shot (mid-only missed a face that melted late), and measure stability on a background ROI. `shake_report` over the whole frame counts subject motion (drum, hands) as shake.
- **Baked look:** the director chose a look baked per shot over a LUT on the V3 adjustment layer. CLAUDE.md §2.5 / §3 should allow that, with the parameters recorded in the brief.

## HQ decision (v0.8.0, 2026-11-01)
- **Synthetic bokeh: rejected** as a studio tool. The director asked for it in round 1 and rejected it in round 2 ("not coming out ok").
- **A look baked per shot: not a default.** Goddess approved one on stills and rejected it on the full reel. A reel may still bake one when the director picks it on a full-reel phone sample, with the parameters recorded in the brief.
- **Stabilisation bake and its QA:** deferred to `BACKLOG.md`.
