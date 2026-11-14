"""v7 type (reel-local, 2026-11-12): L4 "Phone pe aarti dikha dena." moves top-left. The new 12 (Pexels 34565049, a
woman lighting a diya at home) has bright yellow cards bottom-left; top-left is black there, and on 10 it clears the
vendor's phone hand (review_v6 minor 3). Same type as make_type_v6 (Avenir Next Medium 46, cream, glow + shadow).
Writes renders/overlays/v6/v7_line_04.png. Usage (reel folder): ../../.venv/bin/python tools/make_type_v7.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from make_type_v6 import line, LINES  # noqa: E402

im = line(LINES[3][0], "TL", {})
out = Path("renders/overlays/v6/v7_line_04.png"); im.save(out); print(out, im.getbbox())
