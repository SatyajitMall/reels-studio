#!/usr/bin/env python3
"""Build the studio's PDF guides from their Markdown: docs/GUIDE.md and the shooting guide.

Markdown → HTML (markdown-it-py, CommonMark + tables, installed by setup.sh) → PDF with headless Google Chrome, on A4 with page
numbers. Run it after editing either source, and commit the PDFs with the Markdown.

Usage:  ./.venv/bin/python scripts/build_guide_pdf.py [--only guide|shooting] [--chrome PATH]
"""
from __future__ import annotations

import argparse
import html
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = {
    "guide": (ROOT / "docs/GUIDE.md", ROOT / "docs/GUIDE.pdf", "Cinematic Reels Studio: the complete guide"),
    "shooting": (ROOT / "studio/shooting-guide-blackmagic-cam.md", ROOT / "docs/shooting-guide.pdf",
                 "Shooting guide: Blackmagic Cam on iPhone"),
}
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]
CSS = """
@page { size: A4; margin: 16mm 15mm 18mm 15mm;
        @bottom-center { content: counter(page); font: 9pt -apple-system, Helvetica, sans-serif; color: #777; } }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font: 10.3pt/1.5 -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1d1d1f; }
h1 { font-size: 22pt; line-height: 1.2; margin: 0 0 6pt; color: #111; }
h2 { font-size: 15pt; margin: 20pt 0 6pt; padding-top: 6pt; border-top: 1.5pt solid #c9a227; break-after: avoid; }
h3 { font-size: 12pt; margin: 14pt 0 4pt; break-after: avoid; }
p, li { orphans: 3; widows: 3; }
ul, ol { padding-left: 18pt; margin: 4pt 0 8pt; }
li { margin: 1.5pt 0; }
a { color: #0a58ca; text-decoration: none; }
code { font: 8.8pt "SF Mono", Menlo, Consolas, monospace; background: #f3f1ea; padding: 0.5pt 3pt; border-radius: 3pt; }
pre { background: #f6f5f0; border: 0.6pt solid #ddd8c8; border-radius: 4pt; padding: 7pt 9pt; overflow: hidden;
      white-space: pre-wrap; word-break: break-word; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 7.6pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 9pt; break-inside: auto; }
tr { break-inside: avoid; }
th, td { border: 0.6pt solid #d6d2c4; padding: 3.5pt 5pt; text-align: left; vertical-align: top; }
th { background: #f1ede0; }
hr { display: none; }  /* every h2 already carries a rule */
blockquote { margin: 6pt 0; padding: 2pt 10pt; border-left: 3pt solid #c9a227; color: #444; }
em:first-child { color: #555; }
"""


def find_chrome(explicit: str | None) -> str:
    for cand in [explicit, os.environ.get("CHROME"), *CHROME_CANDIDATES]:
        if cand and Path(cand).exists():
            return cand
    sys.exit("Google Chrome (or Chromium) not found. Install it, or pass --chrome / set CHROME.")


def to_html(md_path: Path, title: str) -> str:
    try:
        from markdown_it import MarkdownIt
    except ImportError:
        sys.exit("markdown-it-py is missing: ./.venv/bin/pip install markdown-it-py (setup.sh installs it).")
    # CommonMark (GitHub's list and code rules) plus tables and strikethrough, so the PDF matches GitHub's view.
    body = MarkdownIt("commonmark", {"typographer": False}).enable(["table", "strikethrough"]).render(md_path.read_text())
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")


def build(key: str, chrome: str) -> Path:
    src, out, title = DOCS[key]
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / f"{key}.html"
        page.write_text(to_html(src, title))
        # A throwaway profile, so the user's own Chrome profile is never touched.
        cmd = [chrome, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
               f"--user-data-dir={Path(tmp) / 'profile'}", "--no-pdf-header-footer",
               f"--print-to-pdf={out}", page.as_uri()]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if p.returncode != 0 or not out.exists() or out.stat().st_size < 2000:
            sys.exit(f"{key}: Chrome didn't write the PDF.\n{(p.stderr or p.stdout)[-600:]}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=sorted(DOCS), help="build one PDF instead of all")
    ap.add_argument("--chrome", help="path to the Chrome or Chromium binary")
    a = ap.parse_args()
    chrome = find_chrome(a.chrome)
    for key in ([a.only] if a.only else DOCS):
        out = build(key, chrome)
        print(f"✓ {out.relative_to(ROOT)}  ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
