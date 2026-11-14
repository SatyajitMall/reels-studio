# design.md: Cinematic Reels Studio, director style (studio/director-profile.md)

- **Use:** a transparent overlay for a 9:16 Instagram Reel of Durga Puja night footage. It sits on Premiere's V5, above the grade.
- **Canvas:** 1080×1920, **25 fps** (the reel's sequence rate), transparent background (alpha overlay).
- **Font:** DIN Condensed Bold, local file `assets/fonts/DINCondensed-Bold.ttf` (use @font-face, no CDN). Bold condensed, Anton/Bebas style.
- **Palette:** cream `#F5E6C8` for the text and a DARK soft halo `rgba(26,15,5,0.85)` + drop shadow (puja-night-2 is a calm reel: no gold glow). No other colours.
- **Mood:** reverent, cinematic, premium. Calm and confident, not hyper or glitchy. No glitter or particles: the director rejected "glitter" looks as cheap.
- **Safe zone:** keep all text clear of the top 220 px, the bottom 320 px and the right 120 px. Never place text where it would cover a face (centre-high placement, around y = 350–700, is safest over idol shots).
- **Motion rules:** one dominant motif; a hook within 0.5 s; legible for most of the duration; end on a clean hold, or fade out so it can be dissolved in Premiere.

- **puja-night-2 endcard:** `@satyajitmall`, 84 px, cap top y = 360 px, 3.72 s; one motif (focus-pull settle), clean hold, fade-out.
