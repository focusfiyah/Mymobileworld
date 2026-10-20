"""Free glare opener: oncoming-headlight starburst that grows to a white-out, then clears.
python3 flare.py IN OUT CX CY [DUR]  (CX,CY = headlight point in a 720x1280 frame)"""
import subprocess, sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter

src, dst, cx, cy = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
dur = float(sys.argv[5]) if len(sys.argv) > 5 else 3.8
W, H, FPS = 720, 1280, 30
N = int(dur * FPS)

def flare(k):
    """k 0..1 strength: one headlight pair with starburst rays + bloom."""
    img = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(img)
    for dx in (-38, 38):                       # two headlights
        x, y = cx + dx * (0.4 + k), cy
        r = 6 + 60 * k
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
        L = 80 + 900 * k
        for a in np.linspace(0, np.pi, 8, endpoint=False) + 0.2:
            ex, ey = np.cos(a) * L, np.sin(a) * L
            d.line([x - ex, y - ey, x + ex, y + ey], fill=int(120 + 100 * k), width=2)
    core = np.asarray(img.filter(ImageFilter.GaussianBlur(3)), np.float32) / 255
    bloom = np.asarray(img.filter(ImageFilter.GaussianBlur(40 + 120 * k)), np.float32) / 255
    return np.clip(core + bloom * (1.5 + 3 * k), 0, 1)

def strength(t):
    if t < 2.6: return (t / 2.6) ** 1.6          # build
    if t < 3.0: return 1.0                        # hold the white-out
    return max(0.0, 1 - (t - 3.0) / 0.5)          # clear fast

dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-t", str(dur), "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
tint = np.array([1.0, 0.98, 0.94], np.float32)   # slightly warm white like LED glare
for i in range(N):
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    k = strength(i / FPS)
    g = flare(k)[..., None] * tint
    wash = 0.92 * max(0.0, (k - 0.6) / 0.4) ** 2      # full-frame white-out near the peak
    out = 1 - (1 - f) * (1 - g)                        # screen blend
    out = out * (1 - wash) + wash
    enc.stdin.write((np.clip(out, 0, 1) * 255).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); dec.wait()
