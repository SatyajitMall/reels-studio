# CR-20261027-pujo-ki-asolei-sobar-ig-strategy-posting

| Field | Value |
|---|---|
| From reel | `projects/pujo-ki-asolei-sobar/` |
| Arch version | 0.5.3 |
| Type | skill (instagram-marketing ig-* skills, cinematic-reel Phase 8 packaging) · harness (posting via iPhone Mirroring) · rule (AI-credit disclosure) |
| Severity | workaround (strategy researched by hand at posting time; posting driven through iPhone Mirroring with many dead ends) |
| Status | done (v0.7.2), part deferred |

## What happened
1. **The director asked for the posting strategy after the reel was live.** They wanted to know: are there enough hashtags for traction, is the caption right, and how should the post credit the AI tools (Claude, Adobe Premiere via MCP)?
   - The studio's IG skills still carry pre-2026 assumptions, so I researched the current rules by hand (sources below).
2. **The director asked me to post it for them.** The harness has no IG posting path that keeps Instagram-library audio, so I drove the Instagram app through **iPhone Mirroring** with full-screen computer use. What I learned:
   - **Typing:** `type` text arrives as held keys. iOS shows its accent pop-up and drops letters.
     - Only per-key `key` presses work.
     - Shift-symbols other than digits and `;` don't come through: `?` and `_` arrive as `/` and `-`.
     - Emoji can't be typed.
     - Mac clipboard paste is greyed out in Mirroring (Edit ▸ Paste disabled), and Universal-Clipboard long-press showed no Paste bubble.
     - So a caption takes ~670 key presses in batches of 160, and loses "?" and emoji.
   - **Scrolling:** wheel and quick drags don't scroll. Use slow `left_mouse_down` → `mouse_move` steps → `left_mouse_up`. Sliders lag (release about 10 px past the target). The IG fade controls are rulers that are swiped, not dragged.
   - **Connection:** Mirroring needs the phone **locked and untouched**. Any touch drops it ("iPhone in Use").
   - **Full-screen Space:** while the Claude window is full screen, background app_* control can't reach the window. It needs full-screen control approval.
   - **Photos access:** IG had **limited Photos access**, so a newly AirDropped video is invisible until "Manage ▸ Select more photos". That is a privacy-scope change; add only the one file.
   - **"New ways to reuse" notice:** IG showed it on Next. Tapping OK accepts remix and reuse by default, so it is a consent decision for the director.
   - **Misclicks:** one bottom-right misclick saved another creator's post to the director's Saved. Undone at once.
3. **AI disclosure.** The director wanted the post to credit the AI tools. Two verified handles, checked on instagram.com on 2026-10-27:
   - **@claudeai** = "Claude by Anthropic", 2.3M followers;
   - **@adobevideo** = Adobe Video, 751K, "official home for … Premiere, After Effects".

   **@premierepro is NOT Adobe**: an unrelated account with 131 followers.
4. **Director preferences surfaced:** no collab-post invites, no sharing the reel to Story. The director declined both.

## Workaround used in the reel
- **Caption kept its hook, a keyword ("Durga Puja") in the text, a sends CTA and the voiceover credit.** Added a detailed AI-credit line:
  > Edited with AI: @claudeai cut, graded and finished it in Adobe Premiere Pro (@adobevideo) via MCP, from my footage and direction.

  Hashtags stayed topical: `#durgapuja #durgapujo2026 #pujodiaries #streetportraits #indianstreetphotography`. Files: `projects/pujo-ki-asolei-sobar/deliver/caption_edit_ai_credit.txt`, `project.md`.
- **Posting:** done through Mirroring as above. The director pressed Share.

## Proposed change
1. **`ig-hashtag-strategist` + `ig-caption-writer` (and `references/hashtag-strategy.md`):**
   - Instagram caps posts at **5 hashtags** (announced by @creators on 2025-12-18). Hashtags classify the topic for search and topic pages more than they add reach.
   - Keep all 5 on the post's real topic. Never mix in tool or brand tags on a topical post; give the tool story its own post.
   - Put search keywords in the caption text, and add alt text and location. Public posts from professional accounts can be indexed by Google (since July 2025).
2. **`references/algorithm-heuristics.md`:**
   - Ranking signals per Mosseri: watch time (% and seconds), likes per reach, sends per reach. Sends weigh most for unconnected reach.
   - Since 2026-04-30 the originality rules cover all formats: repost-heavy accounts lose recommendations. Original footage is favoured.
   - Every caption keeps one concrete "send this to…" CTA.
3. **New rule, "AI credit" (cinematic-reel Phase 8 + ig-caption-writer):**
   - When AI edited (not generated) the reel, add one detailed disclosure line saying what AI did and that footage and direction are the creator's. Research: detailed disclosures soften the ~7–8 % engagement drop seen with AI labels (JCR 2026, TikTok); SSIR.
   - Do **not** switch on IG's "AI info" label for real footage. It signals AI-generated content.
   - Keep a verified-handles table: @claudeai, @adobevideo; @premierepro is not Adobe.
4. **Director profile (`studio/director-profile.md`, see CR-20261021-pujo-ki-asolei-sobar-director-profile):** no collab invites, no Story share in traction advice.
5. **Harness, posting via iPhone Mirroring:** add a `premiere-mcp-reality`-style note (`.claude/skills/cinematic-reel/ig-posting-reality.md`) covering:
   - key-press-only typing;
   - no `?`, `_` or emoji, and no paste: put "?" and emoji lines in the caption for the director to add on the phone;
   - slow-drag scrolling;
   - locked-phone rule;
   - the full-screen Space limit;
   - IG limited Photos access;
   - the reuse-consent notice;
   - always stopping before Share.

   Better still: a sanctioned posting path (Meta Graph API via Publora is in `ig-caption-writer`) for reels that don't need IG-library audio. And add a behind-the-scenes "made with AI" reel template to the playbooks for the tool and brand angle.

Sources:
- Mosseri signals: https://www.dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers, https://blog.hootsuite.com/social-media-algorithm/
- 5-hashtag cap: https://later.com/blog/ultimate-guide-to-using-instagram-hashtags/, https://creatorlanehq.com/blog/instagram-5-hashtag-limit-2026
- Originality: https://www.mediapost.com/publications/article/414773/instagram-algorithm-update-discourages-reposted-co.html
- AI disclosure: https://academic.oup.com/jcr/advance-article/doi/10.1093/jcr/ucag013/8672493, https://ssir.org/articles/entry/ai-disclosures-social-media-disengagement
- IG SEO: https://www.inro.social/blog/instagram-seo

## HQ decision
**Accepted, v0.7.2 (2026-10-28), with the director's go-ahead.** Applied in studio-owned files, not in the `ig-*` pack: the pack is third-party, gitignored and reinstalled by `setup.sh`, so edits there would be lost.
- **Items 1–3** → new `.claude/skills/cinematic-reel/instagram-strategy.md`, which overrides the pack where they disagree:
  - the 5-hashtag cap, topical only;
  - caption keywords, alt text and location;
  - the ranking signals and one "send this to…" call to action;
  - originality;
  - the AI-credit line with the verified-handles table.
  - **One clarification:** the AI info label stays **on** whenever the reel contains an AI-generated shot (Meta requires it; `motion-and-ai.md` §3 now says both). The "label off" rule applies only to AI-edited real footage.
- **Phase 8** of the skill is rewritten to match, and posting is only on the director's ask, stopping before Share.
- **Item 4** → `studio/director-profile.md`, new Instagram section.
- **Item 5** → new `.claude/skills/cinematic-reel/ig-posting-reality.md`: the Mirroring facts, plus four firm rules (only on the director's ask; the director taps Share; reuse-consent and Photos access are the director's; touch nothing else in the account).
- **Not re-verified by HQ:** the research figures. They're recorded with their sources and a re-check note.
- **Deferred to the backlog:** a "made with AI" behind-the-scenes playbook; a Graph API posting path set up with the director's account.
