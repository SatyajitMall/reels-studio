# Instagram strategy (skill Phase 8)

The studio's own rules for packaging and posting a reel. Phase 8 uses the `instagram-marketing` pack (`ig-hook-extractor`, `ig-caption-writer`, `ig-hashtag-strategist`, `ig-humanizer`) for drafting. **Where the pack and this file disagree, this file wins.** The pack is third-party and reinstalled by `setup.sh`, so studio rules live here.

**Source:** CR-20261027-pujo-ki-asolei-sobar-ig-strategy-posting. The reel session researched it at posting time on 2026-10-27 (sources at the end). HQ hasn't re-verified the figures. **Re-check them every year, or when a post underperforms.**

## Hashtags: at most 5, all on topic
- **Instagram caps a post at 5 hashtags** (announced by @creators on 2025-12-18).
- Hashtags now mostly **classify** the post for search and topic pages; they add little reach on their own.
- **All 5 describe the post's real subject:** the event, the place, the genre. E.g. `#durgapuja #durgapujo2026 #pujodiaries #streetportraits #indianstreetphotography`.
- **Never mix tool or brand tags** (#ai, #premierepro, #claude) into a topical post. The tool story gets its own post (backlog: a "made with AI" behind-the-scenes playbook).

## Captions: search, sends, one call to action
- **Keywords in the caption text.** Public posts from professional accounts can be indexed by Google (since July 2025), and Instagram search reads the words, so name the subject plainly in the first lines ("Durga Puja in Kolkata", not only "this night").
- **The hook sits in the first 125 characters** (pack rule), and the caption is humanised (`ig-humanizer`).
- **One concrete "send this to…" call to action**, e.g. "Send this to the friend you go pandal-hopping with". Sends weigh most for reach beyond your followers.
- **Alt text and location** on every post. Write the alt text in the package.
- **Credit people:** the voiceover's creator, the music's licence holder, and anyone filmed who asked to be credited.

## What ranks a reel (as of 2026)
Per Instagram's head (Mosseri), the signals that matter most:
1. **Watch time:** the share of the reel watched, and seconds watched. The hook and the pace serve this (CLAUDE.md §4a).
2. **Likes per reach.**
3. **Sends per reach**, the strongest signal for reaching people who don't follow you.

**Originality:** since 2026-04-30 the originality rules cover all formats. Accounts that mostly repost lose recommendations, and original footage is favoured. The director's own footage is the advantage. Never post a reel built mostly from stock or others' clips.

## AI credit and the AI label
Two different things. Don't mix them up:

| The reel… | Caption | Instagram's "AI info" label |
|---|---|---|
| was **edited** with AI (cut, graded, finished) from the director's **own footage** | **One detailed credit line** saying what AI did, and that the footage and direction are the director's | **Off.** It signals AI-*generated* content, which this isn't |
| contains **any AI-generated shot** (`motion-and-ai.md` §3) | The same credit line, plus which shot was generated (and, when it shows a person or the idol, say so) | **On**: Meta requires it for realistic generated content. Non-negotiable |

- **Why detailed:** studies of AI labels report about a 7–8 % engagement drop. A specific disclosure ("AI edited my footage") softens it more than a vague "made with AI" (JCR 2026; SSIR).
- **The line used on Pujo ki Asolei Sobar** (adapt per reel):
  > Edited with AI: @claudeai cut, graded and finished it in Adobe Premiere Pro (@adobevideo) via MCP, from my footage and direction.

**Verified handles** (checked on instagram.com, 2026-10-27; re-check before reuse):

| Tool | Handle | Note |
|---|---|---|
| Claude (Anthropic) | **@claudeai** | "Claude by Anthropic" |
| Adobe Premiere Pro / After Effects | **@adobevideo** | Adobe Video, "official home for … Premiere, After Effects" |
| — | ~~@premierepro~~ | **Not Adobe**: an unrelated small account. Never tag it |

## Director's standing choices
From `studio/director-profile.md`: no collab-post invites, no sharing the reel to Story. Don't suggest them as traction tactics.

## Cover
- **The profile grid shows a 3:4 crop of the cover** (re-check this yearly; it was 4:5 before). On 1080×1920 that's y 240–1680.
- The cover is a full 9:16 picture judged in that crop. A frame from a windowed reel (kolkata's 4:5 matte) shows the black band in the grid, so take the cover from the camera file at full frame, with the reel's look and title applied.
- Upload it from the camera roll at posting (`ig-posting-reality.md`).

## Posting
Instagram-library music can't be added outside the app, so posts that use it go through the phone.
- **iPhone Mirroring:** follow `ig-posting-reality.md`. Prepare the post **only when the director asks for that post**, and **stop before Share**: the director taps it.
- **A reel with its own licensed audio** could go through Meta's Graph API instead: the pack's Publora flow, or the Instagram plugin's `instagram:configure`. That needs the director's account set up first, and still needs the director's explicit approval per post.

## Sources (from the CR)
- Ranking signals: dataslayer.ai "Instagram algorithm 2025"; Hootsuite "social media algorithm".
- 5-hashtag cap: later.com hashtag guide; creatorlanehq.com "instagram-5-hashtag-limit-2026".
- Originality: MediaPost, "Instagram algorithm update discourages reposted content".
- AI disclosure: Journal of Consumer Research (2026, doi 10.1093/jcr/ucag013); Stanford Social Innovation Review, "AI disclosures and social media disengagement".
- Instagram SEO: inro.social.
