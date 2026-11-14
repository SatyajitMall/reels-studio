#!/usr/bin/env python3
"""Record-along guide for the director's own voiceover (2026-10-27: the reference reel's IG audio is only the song, so the
director records the lines himself). Landscape 1920x1080 for the Mac screen:
  left   the reel picture (v13 IG export, English subtitles in it), timed exactly as the cut
  right  teleprompter: the current line (romanised Hindi, big) + English meaning, a SPEAK / GET READY / PAUSE banner,
         a bar that fills across the line's slot (ticks on the words a cut lands on), the next line, and a strip of all lines
audio    the reference voice (guide) at -6 dB, plus one beep at the CLAP cue
Pre-roll: start recording -> CLAP on the beep (so the recording can be synced) -> 3-2-1 -> reel. Post-roll: stop.
Lines + timings: analysis/vo_hi/lines.json  [{"n", "start", "end", "hi", "en", "ticks": [[t, "word"], ...]}]
Usage: record_guide.py -> renders/guide/record_along_guide.mp4
"""
import json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
REEL = Path(__file__).resolve().parents[1]
LINES = json.loads((REEL / "analysis/vo_hi/lines.json").read_text())
VID = REEL / "renders/exports/pujo-ki-asolei-sobar_v13_IG.mp4"; VO = REEL / "audio/ref_audio_vo.wav"
OUT = REEL / "renders/guide"; OUT.mkdir(parents=True, exist_ok=True)
FPS, PRE, POST, DUR = 30, 6.0, 2.5, 35.8333
W, H = 1920, 1080; PW = 608
DIN = str(REEL / "graphics/title/assets/fonts/DINCondensed-Bold.ttf"); SANS = "/System/Library/Fonts/Supplemental/Arial.ttf"
f_big, f_mid, f_en, f_sm, f_huge = (ImageFont.truetype(DIN, 70), ImageFont.truetype(DIN, 44), ImageFont.truetype(SANS, 30),
                                    ImageFont.truetype(SANS, 24), ImageFont.truetype(DIN, 260))
BG, FG, DIM, GREEN, AMBER, GREY = (14, 14, 16), (245, 240, 230), (140, 140, 140), (60, 200, 110), (240, 170, 40), (70, 70, 74)

def wrap(d, text, font, width):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: out.append(cur); cur = w
    return out + [cur] if cur else out

def panel(t):
    """t = reel time (negative during the pre-roll)"""
    im = Image.new("RGB", (W - PW, H), BG); d = ImageDraw.Draw(im); X, WW = 50, W - PW - 100
    if t < 0:                                                   # pre-roll
        msg = "START RECORDING NOW" if t < -3.4 else ("CLAP!" if t < -2.8 else str(int(np.ceil(-t))))
        col = AMBER if msg == "CLAP!" else FG
        f = f_huge if len(msg) <= 5 else f_big
        d.text(((W - PW) / 2, H / 2 - 40), msg, font=f, fill=col, anchor="mm")
        d.text(((W - PW) / 2, H / 2 + 140), "Clap once on the beep, then the reel starts after 3-2-1." if t < -2.8 else "Get ready for line 1",
               font=f_en, fill=DIM, anchor="mm")
        return im
    if t > DUR:
        d.text(((W - PW) / 2, H / 2), "STOP RECORDING", font=f_big, fill=FG, anchor="mm"); return im
    cur = next((L for L in LINES if L["start"] - 0.9 <= t < L["end"] + 0.15), None)
    nxt = next((L for L in LINES if L["start"] - 0.9 > t), None)
    if cur and t >= cur["start"]: state, col = "SPEAK", GREEN
    elif cur: state, col = "GET READY", AMBER
    else: state, col = "PAUSE", GREY
    d.rounded_rectangle((X, 50, X + 330, 120), 14, fill=col); d.text((X + 165, 85), state, font=f_mid, fill=BG, anchor="mm")
    d.text((X + WW, 85), f"{t:5.2f} s", font=f_mid, fill=DIM, anchor="rm")
    if cur:
        d.text((X, 175), f"LINE {cur['n']} / {len(LINES)}   ·   {cur['end'] - cur['start']:.1f} s", font=f_en, fill=DIM)
        y = 235
        for ln in wrap(d, cur["hi"], f_big, WW): d.text((X, y), ln, font=f_big, fill=FG); y += 80
        y += 12
        for ln in wrap(d, cur["en"], f_en, WW): d.text((X, y), ln, font=f_en, fill=DIM); y += 40
        # slot bar
        by = 640; d.rounded_rectangle((X, by, X + WW, by + 34), 10, fill=GREY)
        p = np.clip((t - cur["start"]) / (cur["end"] - cur["start"]), 0, 1)
        if p > 0: d.rounded_rectangle((X, by, X + max(int(WW * p), 20), by + 34), 10, fill=GREEN)
        for tt, word in cur.get("ticks", []):
            x = X + WW * (tt - cur["start"]) / (cur["end"] - cur["start"])
            d.line((x, by - 10, x, by + 44), fill=FG, width=3); d.text((x, by + 52), word, font=f_sm, fill=FG, anchor="mt")
    if nxt:
        d.text((X, 790), "NEXT", font=f_en, fill=DIM)
        d.text((X, 830), wrap(d, nxt["hi"], f_mid, WW)[0] + (" …" if len(wrap(d, nxt["hi"], f_mid, WW)) > 1 else ""), font=f_mid, fill=(190, 190, 190))
    # strip of all lines
    sy = 960; d.rectangle((X, sy, X + WW, sy + 26), fill=(30, 30, 34))
    for L in LINES:
        x0, x1 = X + WW * L["start"] / DUR, X + WW * L["end"] / DUR
        d.rectangle((x0, sy, x1, sy + 26), fill=GREEN if L is cur and t >= L["start"] else (90, 90, 96))
        d.text(((x0 + x1) / 2, sy + 13), str(L["n"]), font=f_sm, fill=BG, anchor="mm")
    px = X + WW * t / DUR; d.line((px, sy - 12, px, sy + 38), fill=AMBER, width=4)
    return im

def frames_of(path, n):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={PW}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    for _ in range(n):
        b = p.stdout.read(PW * H * 3)
        if len(b) < PW * H * 3: break
        yield Image.frombytes("RGB", (PW, H), b)

if __name__ == "__main__":
    n_pre, n_reel, n_post = int(PRE * FPS), int(round(DUR * FPS)), int(POST * FPS)
    beep = OUT / "_beep.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=1000:duration=0.12", "-af", "volume=0.5", str(beep)], check=True)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", str(VO), "-i", str(beep), "-filter_complex",
                            f"[1:a]adelay={int(PRE * 1000)}|{int(PRE * 1000)},volume=-6dB[g];[2:a]adelay={int((PRE - 3.0) * 1000)}|{int((PRE - 3.0) * 1000)}[b];[g][b]amix=inputs=2:normalize=0[a]",
                            "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                            "-t", f"{PRE + DUR + POST:.3f}", str(OUT / "record_along_guide.mp4")], stdin=subprocess.PIPE)
    black = Image.new("RGB", (PW, H), (0, 0, 0)); src = frames_of(VID, n_reel); last = black
    for i in range(n_pre + n_reel + n_post):
        t = i / FPS - PRE
        if 0 <= t < DUR: last = next(src, last)
        fr = Image.new("RGB", (W, H), BG); fr.paste(last if t >= 0 else black, (0, 0)); fr.paste(panel(t), (PW, 0))
        enc.stdin.write(fr.tobytes())
    enc.stdin.close(); enc.wait(); beep.unlink()
    print(f"✓ {OUT / 'record_along_guide.mp4'}  ({PRE + DUR + POST:.1f} s: {PRE:.0f} s pre-roll with CLAP cue at -3.0 s)")
