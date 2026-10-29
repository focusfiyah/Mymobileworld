"""Free fix: recolour a stray blue silicone band (Omni moved it onto the wrist) to a gold bangle. Only strongly blue
pixels change (hue 190-250 deg, sat > 0.35); nothing else in these scenes is that blue (checked per clip).
python3 tools/blue_fix.py IN.mp4 OUT.mp4 [--frame N out.png]"""
import subprocess, sys
import numpy as np

def fix(rgb):
    f = rgb.astype(np.float32) / 255; r, g, b = f[..., 0], f[..., 1], f[..., 2]
    mx, mn = f.max(-1), f.min(-1); d = mx - mn + 1e-6
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = d / (mx + 1e-6)
    m = (h > 190) & (h < 250) & (s > 0.35) & (mx > 0.15)
    m = m.astype(np.float32)
    # soften the mask edge 1 px
    m = np.maximum(m, 0.5 * (np.roll(m, 1, 0) + np.roll(m, -1, 0)) * m.max())
    v = mx[..., None]
    gold = np.concatenate([v * 0.93, v * 0.74, v * 0.36], -1)
    out = f * (1 - m[..., None]) + gold * m[..., None]
    return (np.clip(out, 0, 1) * 255).astype(np.uint8), float(m.mean())

def main():
    src, dst = sys.argv[1], sys.argv[2]
    w, h = 1080, 1920
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    o = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", "24", "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    n = 0; cov = []
    while True:
        buf = p.stdout.read(w * h * 3)
        if len(buf) < w * h * 3: break
        fr, c = fix(np.frombuffer(buf, np.uint8).reshape(h, w, 3)); cov.append(c); o.stdin.write(fr.tobytes()); n += 1
    o.stdin.close(); o.wait()
    print(f"{n} frames, blue share max {max(cov):.4f} mean {np.mean(cov):.4f}")

if __name__ == "__main__":
    main()
