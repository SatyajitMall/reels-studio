# CR-20261111-could-not-go-home-diwali-film-emulation-first-use

| Field | Value |
|---|---|
| From reel | `projects/could-not-go-home-diwali/` |
| Arch version | 0.9.1 (studio at v0.10.2) |
| Type | skill |
| Severity | polish (first use, as the skill asks: "The first reel to use it reports in a CR") |
| Status | open |

## What happened
This is the first studio AI shot written with `film-emulation-prompts`. The shot is image-to-video from a stock photo, not a gap fill between two of the director's stills.
- **The shot:** the reel's last shot, Pexels photo 5882889 (a man lighting a cracker at night), animated with Veo 3.1 Lite. The first frame is that photo cropped to 9:16 (`renders/gen/S31_first_frame_9x16.png`).
- **Director:** chose "Animate photo with AI" after the story QC, approved the draft, then "Yes, make the final".
- **Prompt:** `renders/gen/S31_prompt.txt`. Shot, then camera (low at his eye level, 52 mm, 9:16, locked off on a tripod, shallow depth like f/2), then light (small flames as the only light).
- **Negative:** `renders/gen/S31_negative.txt`. The skill's list plus "camera move, zoom, extra people, second person, extra hands, extra fingers, distorted hands, morphing face, changing face, explosion, fireball, bright room lights".
- **No re-prompt.** One draft ($0.12), one final ($0.40). Total $0.52 against a $4 reel cap.

**Numbers against the anchor still** (full 1080×1920 frame):

| Frame | Mean luma | p02 | p99 | R−B | Saturation |
|---|---|---|---|---|---|
| Anchor still | 14.0 | 0 | 181 | 20.2 | 0.59 |
| Draft, frame 0 | 13.7 | 0 | 182 | 20.2 | 0.59 |
| Draft, frame 24 (fountain on) | 22.8 | 0 | 250 | 28.4 | 0.63 |
| Final, frame 0 | 13.6 | 0 | 181 | 20.2 | 0.68 |
| Final, frame 12 | 13.8 | 0 | 182 | 19.9 | 0.70 |

- The first frame anchors the colour exactly, as the skill says.
- There's no lifted black and no baked look.
- The final is a little more saturated (+0.09–0.11) than the still.

**Two things the skill doesn't say:**
1. **The final isn't the draft at 1080p.** Same prompt and first frame, but the action differs. The draft's fountain was about head height; the final's runs off the top of the frame, and 16–19 % of the window clips white from 1.25 s. The draft-then-final check approves an idea, not the frames. Every frame of the final needs checking again, and its usable range picked anew. Kolkata saw the same thing with the tram.
2. **Size words are ignored.** "a small fountain of golden sparks, about a hand's height" didn't hold in the final. Brightness and scale of practical effects (sparks, fire) need a negative too ("tall fountain, sparks above his head, overexposed").

## Workaround used in the reel
- I picked the final's frames 12–51 (lighting → eruption) and interpreted 24 → 25 fps in Premiere.
- The reel's V3 look grades it like every clip. Measured in the reel: max channel 247, blacks p1 11.
- The review gate checked faces, hands and clipping (`analysis/review_v5.md`).

## Proposed change
1. **`film-emulation-prompts`:**
   - mark it verified for image-to-video from a still, with this reel's numbers;
   - add "the final is a new generation: re-check every frame and re-pick the range";
   - for practical effects, put the unwanted scale in `--negative`, not only the wanted scale in the prompt.
2. **`gen_video.py`:** pass the draft's seed to the final when the provider returns one. OpenRouter returned no seed here: the draft's JSON has none.
3. **`motion-and-ai.md` §3:** add a still → animate route for a stock photo the director picked (ladder step 3 → 5). The label is ON whenever a real-looking person moves.

## HQ decision
<!-- HQ fills this in. -->
