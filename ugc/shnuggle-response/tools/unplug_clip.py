"""Free fix (Ralph 2026-10-16: the AI plug is the wrong size/place, remove it): paint fixed ellipses out of every frame of a
static-camera clip. python3 tools/unplug_clip.py IN OUT cx,cy,rx,ry [cx,cy,rx,ry ...]  (clip pixels, 720x1280)"""
import sys, subprocess, cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]; els = [tuple(int(v) for v in a.split(",")) for a in sys.argv[3:]]
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); W, H = int(cap.get(3)), int(cap.get(4))
mask = np.zeros((H, W), np.uint8)
for cx, cy, rx, ry in els: cv2.ellipse(mask, (cx, cy), (rx, ry), 0, 0, 360, 255, -1)
soft = cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), 3)[..., None]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
n = 0
while True:
    ok, f = cap.read()
    if not ok: break
    fill = cv2.inpaint(f, cv2.dilate(mask, np.ones((5, 5), np.uint8)), 9, cv2.INPAINT_TELEA)
    f = (f * (1 - soft) + fill * soft).astype(np.uint8)
    p.stdin.write(f.tobytes()); n += 1
p.stdin.close(); p.wait(); print("wrote", dst, n, "frames")
