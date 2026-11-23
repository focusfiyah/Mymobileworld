"""Put the matted talking head on a new background: cover-fit the photo to 1080x1920, soft blur (phone depth of field),
light wrap of the background onto the edge, and a gentle match of the person to the background's light.
Usage: <musetalk venv python> bgswap.py TALK.mp4 ALPHA.mp4 BG.jpg OUT.mp4 [--still N]   (--still N writes OUT as a png of frame N)"""
import sys, subprocess, cv2, numpy as np
talk, alpha, bgp, out = sys.argv[1:5]; still = int(sys.argv[sys.argv.index("--still") + 1]) if "--still" in sys.argv else None
W, H = 1080, 1920
bg = cv2.imread(bgp); s = max(W / bg.shape[1], H / bg.shape[0]); bg = cv2.resize(bg, (int(bg.shape[1] * s + .5), int(bg.shape[0] * s + .5)), interpolation=cv2.INTER_AREA)
y0, x0 = (bg.shape[0] - H) // 2, (bg.shape[1] - W) // 2; bg = bg[y0:y0 + H, x0:x0 + W]
bg = cv2.GaussianBlur(bg, (0, 0), 7).astype(np.float32)
bgmean = bg.reshape(-1, 3).mean(0)
wrapsrc = cv2.GaussianBlur(bg, (0, 0), 25)


def comp(f, a):
    a = cv2.erode(a, np.ones((3, 3), np.uint8), iterations=1)          # pull the edge in 1-2 px: no kitchen specks
    a = cv2.GaussianBlur(a, (0, 0), 1.2).astype(np.float32)[..., None] / 255
    f = f.astype(np.float32)
    fm = f[a[..., 0] > 0.9].mean(0) if (a > 0.9).sum() > 1000 else f.reshape(-1, 3).mean(0)
    f = f * (1 + 0.12 * (bgmean / (fm + 1e-6) - 1))          # 12% pull of the person's colour toward the room light
    edge = np.clip(a * (1 - a) * 4, 0, 1)                      # light wrap only on the soft edge
    f = f * (1 - 0.35 * edge) + wrapsrc * 0.35 * edge
    return np.clip(f * a + bg * (1 - a), 0, 255).astype(np.uint8)


ct, ca = cv2.VideoCapture(talk), cv2.VideoCapture(alpha)
if still is not None:
    ct.set(1, still); ca.set(1, still); _, f = ct.read(); _, a = ca.read(); cv2.imwrite(out, comp(f, a[..., 0])); print("STILL_OK", out); sys.exit()
fps = ct.get(5)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-i", talk, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-pix_fmt", "yuv420p",
                      "-c:a", "copy", out], stdin=subprocess.PIPE)
while True:
    ok, f = ct.read(); ok2, a = ca.read()
    if not (ok and ok2): break
    p.stdin.write(comp(f, a[..., 0]).tobytes())
p.stdin.close(); p.wait(); print("BGSWAP_OK", out)
