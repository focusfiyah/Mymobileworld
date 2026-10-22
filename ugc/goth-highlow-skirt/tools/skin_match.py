"""Free fix (Ralph's skin-consistency rule, 2026-10-22 goth skirt): match the leg skin of a clip to the reference clip (V1,
Grace's medium-dark skin) by scaling only skin-hued pixels inside a leg box, with a feathered mask, frame by frame.
  python3 tools/skin_match.py CLIP x0 y0 x1 y1   (box in 720x1280 coordinates) -> clips/CLIP_skin.mp4"""
import subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
import os
SATMIN = int(os.environ.get("SATMIN", 55))   # 30 also catches pale highlights on legs (VS)
TARGET = np.array([105.0, 62.0, 43.0])   # V1_veo_1 leg mean (RGB), measured 2026-10-22


def mask_of(im, box):
    hsv = np.asarray(im.convert("HSV")).astype(float)
    m = ((hsv[..., 0] < 28) & (hsv[..., 1] > SATMIN) & (hsv[..., 1] < 205) & (hsv[..., 2] > 55)).astype(np.uint8) * 255
    keep = np.zeros_like(m); x0, y0, x1, y1 = box; keep[y0:y1, x0:x1] = 255
    m = np.minimum(m, keep)
    return np.asarray(Image.fromarray(m).filter(ImageFilter.GaussianBlur(4))).astype(float)[..., None] / 255


def main():
    clip, box = sys.argv[1], tuple(int(v) for v in sys.argv[2:6])
    src = f"clips/{clip}.mp4"; W, H = 720, 1280
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True)
    frames = np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3)
    first = Image.fromarray(frames[len(frames) // 2]); m0 = mask_of(first, box)
    mean = (np.asarray(first).astype(float) * m0).sum((0, 1)) / max(m0.sum(), 1)
    lum = lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    ratio = 0.5 * (TARGET / mean) + 0.5 * (lum(TARGET) / lum(mean))   # half hue match, half brightness: plain per-channel went orange
    print(clip, "leg mean", mean.round(), "ratio", ratio.round(3))
    out = []
    for f in frames:
        im = Image.fromarray(f); m = mask_of(im, box); a = f.astype(float)
        out.append(np.clip(a * (1 - m) + a * ratio * m, 0, 255).astype(np.uint8))
    enc = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "24", "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", f"clips/{clip}_skin.mp4"],
                         input=np.stack(out).tobytes(), check=True)
    print("OK", f"clips/{clip}_skin.mp4")


if __name__ == "__main__":
    main()
