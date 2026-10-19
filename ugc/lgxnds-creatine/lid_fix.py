"""S7 v5 (2026-10-19): Seedance reference mode drew a second lid on the counter, left of the tub. The camera is locked
(phaseCorrelate < 0.4 px), so inpaint the lid ONCE on frame 0 and lay that same patch on every frame (no shimmer).
  python3 lid_fix.py IN OUT"""
import subprocess, sys
import cv2, numpy as np
src, dst = sys.argv[1:3]
c = cv2.VideoCapture(src); fps = c.get(cv2.CAP_PROP_FPS); F = []
while True:
    o, f = c.read()
    if not o: break
    F.append(f)
h, w = F[0].shape[:2]
m = np.zeros((h, w), np.uint8); cv2.ellipse(m, (262, 862), (44, 52), 0, 0, 360, 255, -1); m[:, 293:] = 0   # lid, never past the tub edge
# fill = the marble just left of the lid (inpaint pulled the tub's teal stripe in), brightness matched at low frequency
patch = F[0].copy(); x0, x1, y0, y1 = 212, 296, 800, 925; d = x1 - x0
src_ = F[0][y0:y1, x0 - d:x0].astype(np.float32); lo = lambda z: cv2.GaussianBlur(z, (0, 0), 12)
tgt_lo = lo(cv2.inpaint(F[0], m, 15, cv2.INPAINT_TELEA)[y0:y1, x0:x1].astype(np.float32))
patch[y0:y1, x0:x1] = np.clip(src_ - lo(src_) + tgt_lo, 0, 255).astype(np.uint8)
a = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 3)[..., None]; a[:, 290:] = (m[:, 290:, None] > 0)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
for f in F:
    p.stdin.write((patch * a + f * (1 - a)).astype(np.uint8).tobytes())
p.stdin.close(); p.wait()
cv2.imwrite(dst.rsplit(".", 1)[0] + "_chk.jpg", np.hstack([F[0][700:1100, 100:500], ((patch * a + F[0] * (1 - a)).astype(np.uint8))[700:1100, 100:500]]))
