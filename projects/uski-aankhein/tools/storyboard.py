"""Storyboard for an eye-line-locked EDL: 3 frames per shot (in / mid / out) through the planned 9:16 crop.
Usage: python tools/storyboard.py analysis/edl_v1.json analysis/picks/storyboard_v1.jpg
Reel-local tool (see CR-20261019-pujo-ki-asolei-sobar-pool-survey for the studio version request)."""
import json, subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
edl = json.load(open(sys.argv[1])); out = sys.argv[2]
rows = {f"{r['shoot']}:{r['clip_id'].split('_')[-1]}": r for r in json.load(open('analysis/survey/eyes_candidates.json'))}
fps_seq = edl['seq_fps']; TW, TH = 240, 427
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf', 18)
except Exception: font = ImageFont.load_default()
tmp = tempfile.mkdtemp()
def frame(src, t, rot):
    p = os.path.join(tmp, 'f.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1'] + (['-vf', 'hflip,vflip'] if rot else []) + [p], check=True)
    return Image.open(p).convert('RGB')
def crop(im, ex, ey, cw):
    W, H = im.size; cwp = cw * W; chp = cwp * 16 / 9
    l = min(max(ex * W - cwp * .5, 0), W - cwp); t = min(max(ey * H - chp * .40, 0), H - chp)
    return im.crop((int(l), int(t), int(l + cwp), int(t + chp))).resize((TW, TH), Image.LANCZOS)
shots = edl['shots']; LW = 330
S = Image.new('RGB', (LW + 3 * TW + 8, len(shots) * (TH + 6)), (12, 12, 12)); d = ImageDraw.Draw(S)
for i, s in enumerate(shots):
    r = rows[s['key']]; rot = 'UPSIDE' in r['orientation']; src_fps = float(r['fps'])
    dur = s['seq_out'] - s['seq_in']; real = dur * fps_seq / src_fps if abs(src_fps - fps_seq) > .5 else dur
    y = i * (TH + 6)
    for j, f in enumerate((0.02, 0.5, 0.98)):
        cw = s['cw'] + (s.get('cw_end', s['cw']) - s['cw']) * f
        ex, ey = s['ex'], s['ey'] + (s.get('ey_end', s['ey']) - s['ey']) * f
        if 'track' in s:  # [[frac, ex, ey], ...] piecewise-linear crop follow
            tr = s['track']; k = max(i for i in range(len(tr)) if tr[i][0] <= f) if f < tr[-1][0] else len(tr) - 2
            a, b = tr[k], tr[min(k + 1, len(tr) - 1)]; u = 0 if b[0] == a[0] else (f - a[0]) / (b[0] - a[0])
            ex, ey = a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u
        t = s['src_in'] if s.get('freeze') else s['src_in'] + real * f
        tile = crop(frame(r['source'], t, rot), ex, ey, cw)
        ImageDraw.Draw(tile).line([(0, TH * .4), (TW, TH * .4)], fill=(0, 200, 200), width=1)
        S.paste(tile, (LW + j * TW + j * 2, y))
    txt = [f"#{s['n']}  {s['key']}", f"seq {s['seq_in']:.2f}-{s['seq_out']:.2f} ({dur:.2f}s)", (f"FREEZE src {s['src_in']:.2f}" if s.get('freeze') else f"src {s['src_in']:.2f}-{s['src_in']+real:.2f}") + f" @{src_fps:g}fps" + (' ROT180' if rot else ''), f"crop {1/s['cw']:.1f}x" + (f" -> {1/s['cw_end']:.1f}x" if 'cw_end' in s else '')]
    words = s['role'].split(); line = ''
    for w in words:
        if len(line) + len(w) > 34: txt.append(line); line = ''
        line += w + ' '
    txt.append(line); txt.append(s['beat'])
    for k, tline in enumerate(txt): d.text((8, y + 8 + k * 22), tline, fill=(255, 210, 90) if k == 0 else (225, 225, 225), font=font)
os.makedirs(os.path.dirname(out), exist_ok=True); S.save(out, quality=86); print('wrote', out, S.size)
