# Plan: AI shots and bad-footage repair (drafted 2026-11-10; built in v0.10.0, 2026-11-11)

Why: the director wants AI video wherever stock doesn't fit or our own footage is bad, and asked whether Claude Fable 5.2 can make it in-house.

## Facts checked (2026-11-10)
- **Claude Fable 5.2** (`claude-fable-5-2`, released 2026-11-09):
  - Anthropic's model page lists "Text and images → text". It writes text and code; it can't output a frame of video, fill frames or stabilise.
  - Anthropic has released no video skills. Claude Motion (beta) makes code-built animations to MP4 in claude.ai and uses no generated footage.
- **Real-looking footage needs a video model**, paid per second through OpenRouter (public model list, read 2026-11-10):

  | Model | What it does | Price |
  |---|---|---|
  | `google/veo-3.1-lite` | New shot from a prompt plus a first and/or last still; 4, 6 or 8 s, 24 fps | $0.03/s 720p, $0.05/s 1080p, no sound |
  | `google/gemini-omni-1.2-flash` | New shot, or the frames between a first and a last still; 3–15 s | Sound is always billed: $0.07/s 720p, $0.10/s 1080p (upscaled) |

  - Editing or extending **our own clip** with Omni means uploading the clip to Google (Gemini API, Files API). OpenRouter doesn't document it.
  - FLUX Video Edit and Aleph take a source video only as a public URL.
- **`gen_video.py --provider google` is dead.** Its Veo `-preview` models on the Gemini API were shut down on 2026-10-22, and Google points to `gemini-omni-1.2-flash` instead. The OpenRouter route (the default) still works.

## Director's decisions (2026-11-10)
1. **AI may show the reel's subjects too** (people, the idol). This changes the 2026-10-18 rule "never the subject".
   - Kept unless the director says otherwise: **never proof**, never words put in someone's mouth, labelled "AI-generated" in the brief, and Instagram's AI label on at posting.
2. **Stills only.** No clip is uploaded; at most a first and a last still go up.
3. **Fable 5.2 runs it in-house.** The director wants Fable 5.2, not another service, for this work.
   - What Fable 5.2 can do in-house, at no per-shot cost:
     - plan the shot;
     - write the prompt (`film-emulation-prompts`);
     - pick the anchor stills;
     - read every frame of a draft against the footage;
     - repair footage with local tools;
     - build graphic shots in code.
   - What it can't do: make the real-looking frames.
4. **Paid generation stays as the ladder's last step, with $4, 4 shots and 24 s per reel and $20 a month** (director, "Keep, $4/reel caps").

## The bad-footage ladder (every reel, cheapest first)
1. **Fix it locally** (free, Fable 5.2 drives the tools):
   - shake: Premiere Warp, measured with `shake_report.py`;
   - dropped frames or gaps under about 1 s: After Effects Pixel Motion or Timewarp (`ae_roundtrip.py`, `"blend": "pixel"`);
   - noise: AE denoise;
   - soft focus: a tighter crop only within the 70 % width floor.
2. **Another take** of the same moment from the director's pool.
3. **Free stock** (video and photos), if the director allows stock for the reel.
4. **Code-built shot** (HyperFrames, simple 3D) when the moment can be graphic.
5. **Paid AI shot from stills** (if kept), drafted at 720p before the final:
   - Veo Lite for a new shot;
   - Omni for the frames between two good stills.

## Build (done in v0.10.0, except item 5)
1. **`gen_video.py`:**
   - an `omni` alias, and a `between` mode that requires `--first-frame` and `--last-frame`;
   - pricing that knows Omni bills sound;
   - durations 3–15 s for Omni;
   - remove the dead Google route, or point it at Omni on the Gemini API (needs a `GEMINI_API_KEY` that the director adds).
2. **`studio/ai-budget.json`:** the caps the director picks (today $2 and 2 shots / 16 s per reel, $10 a month).
3. **Rules:**
   - `motion-and-ai.md` §3: policy, the ladder, Omni;
   - `gen_video.py` POLICY docstring;
   - director profile (AI bullet);
   - SKILL Phase 2 (where the ladder is decided) and Phase 5;
   - `instagram-strategy.md` (AI label mandatory when a subject is generated).
4. **Review gate:** `reel-reviewer` gets AI-shot checks:
   - hands and fingers;
   - faces staying the same person across the shot;
   - text and signs;
   - details the model dropped from the anchor still.
5. **One paid test, only with the director's OK on that run:** the same Diwali still pair through Veo Lite and Omni at 720p, 4 s (about $0.12 + $0.28), to compare.
