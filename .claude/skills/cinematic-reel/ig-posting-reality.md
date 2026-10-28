# Posting through iPhone Mirroring: what actually works

A reality note, like `premiere-mcp-reality.md`. It covers driving the Instagram app on the director's iPhone through macOS **iPhone Mirroring** with computer use. Learned on Pujo ki Asolei Sobar (v19, 2026-10-27; CR-20261027-pujo-ki-asolei-sobar-ig-strategy-posting).

## Rules (non-negotiable)
1. **Only when the director asks for this post.** Packaging approval (Checkpoint 3) isn't permission to post. Ask, and get a clear yes for this reel.
2. **Stop before Share.** Prepare everything, then hand over. **The director taps Share.**
3. **Consent and privacy prompts are the director's:**
   - **"New ways to reuse"**, shown on Next: tapping OK opts the reel into remix and reuse by default. Show it to the director and let them choose.
   - **Limited Photos access:** Instagram may only see selected photos, so a newly AirDropped video is invisible. Widening access (Manage ▸ Select more photos) changes a privacy setting. The director does it, adding only the one file.
4. **Touch nothing else in the account.** No likes, saves, follows, comments or DMs. A misclick near the bottom-right saved another creator's post once. If anything like that happens, undo it at once and tell the director.

## Connection
- Mirroring needs the **phone locked and untouched**. Any touch on the phone drops the session ("iPhone in Use"). Ask the director to leave it locked.
- While the Claude window is **full screen** in its own Space, background control can't reach the Mirroring window. It needs full-screen control approval, so request it once, up front.

## Typing
- `type` sends text as held keys. iOS then shows its accent pop-up and **drops letters**. Use **per-key `key` presses** in batches (about 160 keys per call).
- **Shift symbols don't arrive** except digits and `;`: `?` comes out as `/`, and `_` as `-`. **Emoji can't be typed.**
- **No paste.** Mac clipboard paste is greyed out in Mirroring (Edit ▸ Paste disabled), and Universal Clipboard showed no Paste bubble.
- **So:**
  - type the caption without `?` and emoji;
  - give the director a short numbered list of the exact edits to make on the phone ("line 1: add ? after 'sobar'");
  - plan about 670 key presses for a full caption.
- **Hashtags and handles type fine:** letters and digits, and `#` and `@` came through as typed in practice. Check the result on a screenshot anyway.

## Scrolling and sliders
- The scroll wheel and quick drags don't scroll. Use a **slow drag**: `left_mouse_down`, several small `mouse_move` steps, then `left_mouse_up`.
- **Sliders lag.** Release about 10 px past the target, then check the value.
- The audio fade controls are **rulers you swipe**, not handles you drag.

## Afterwards
Record in `project.md`: what was posted (version, caption file), which settings the director chose (reuse, audio, cover), and anything that went wrong. A new dead end goes in a CR.
