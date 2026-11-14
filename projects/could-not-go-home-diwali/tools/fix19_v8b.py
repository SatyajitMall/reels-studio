"""v8b (reel-local, 2026-11-12): review_v8 minor 1. Where sparks cross the man's face, Timewarp draws grey vein-like
streaks, and one breaks the glasses frame (30.04 s). Timewarp synthesises EVERY output frame (even frames differ from the
nearest source frame by ~10/255), while Veo's own frames are clean. He doesn't move (subject jitter 0.1 px), so inside a
soft mask over his head and shoulders every frame comes from the source instead: output n = source 22 + n/2 on even
frames, the average of the two source neighbours on odd frames (a frame mix). A spark crossing his face is then Veo's own
spark, half-stepped. Everywhere else stays Timewarp. Colour matches (static wall 0.4/1023 on frame 0).
Native yuv422p10le, ProRes 422 HQ.
Usage (reel folder): ../../.venv/bin/python tools/fix19_v8b.py
"""
import subprocess
from pathlib import Path

import numpy as np
import scipy.ndimage as nd
from PIL import Image, ImageDraw

SRC = "renders/ae/19_S31_cracker_tw50.mov"
ORIG = "renders/ae_src/S31_final_conform25.mov"   # 25 fps conform of the Veo final; output frame 0 = source frame 22
OUT = Path("renders/v8/19_S31_cracker_tw50_facemix.mov")
W, H = 1080, 1920


def mask():
    m = Image.new("L", (W, H), 0); d = ImageDraw.Draw(m)
    d.ellipse((265, 655, 575, 1005), fill=255)              # head, hair, glasses, beard
    d.polygon([(200, 940), (520, 940), (540, 1110), (200, 1110)], fill=255)   # collar and shoulders
    a = nd.gaussian_filter(np.asarray(m, np.float32) / 255, 14)
    Image.fromarray((a * 255).astype(np.uint8)).save("analysis/v8_notes/19_facemix_mask.png")
    return a


def frames(src=SRC):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "yuv422p10le", "-"], capture_output=True).stdout
    a = np.frombuffer(b, np.uint16); n = W * H * 2
    out = []
    for i in range(a.size // n):
        f = a[i * n:(i + 1) * n]
        out.append((f[:W * H].reshape(H, W), f[W * H:W * H * 3 // 2].reshape(H, W // 2), f[W * H * 3 // 2:].reshape(H, W // 2)))
    return out


def main():
    my = mask(); mc = my[:, ::2].copy()
    X = frames(); n = len(X); Y = frames(ORIG)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv422p10le", "-s", f"{W}x{H}", "-r", "25",
                            "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-i", "-",
                            "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", str(OUT)], stdin=subprocess.PIPE)
    changed = 0
    for i in range(n):
        k = 22 + i // 2
        nb = [Y[k]] if i % 2 == 0 else [Y[k], Y[k + 1]]
        if True:
            planes = []
            for p, mm in ((0, my), (1, mc), (2, mc)):
                cur = X[i][p].astype(np.float32)
                avg = sum(x[p].astype(np.float32) for x in nb) / len(nb)
                planes.append(np.clip(np.rint(cur + mm * (avg - cur)), 0, 1023).astype(np.uint16))
            changed += 1
        enc.stdin.write(b"".join(p.tobytes() for p in planes))
    enc.stdin.close(); enc.wait()
    print(OUT, n, "frames,", changed, "frames take the face region from the source")


if __name__ == "__main__":
    main()
