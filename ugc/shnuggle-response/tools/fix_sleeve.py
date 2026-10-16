"""Free fix (2026-10-16): Seedance printed a 'shnuggle' logo on R1-01's plain kraft coffee sleeve. From FROM s on, every non-kraft
pixel inside the sleeve's hull is filled from the surrounding kraft (normalized blur). python3 tools/fix_sleeve.py IN OUT [FROM=1.3]"""
import sys, subprocess, cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]; t0 = float(sys.argv[3]) if len(sys.argv) > 3 else 1.3
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); W, H = int(cap.get(3)), int(cap.get(4))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = cap.read()
    if not ok: break
    if i / fps >= t0:
        h = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
        kraft = ((h[..., 0] >= 6) & (h[..., 0] <= 22) & (h[..., 1] > 70) & (h[..., 2] > 60) & (h[..., 2] < 230)).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(kraft)
        if n > 1:
            k = 1 + int(np.argmax(st[1:, 4]))
            if st[k, 4] > 2000:
                comp = (lab == k).astype(np.uint8)
                hull = np.zeros_like(comp); cv2.fillPoly(hull, [cv2.convexHull(cv2.findNonZero(comp))], 1)
                hull = cv2.erode(hull, np.ones((35, 35), np.uint8))   # 17 px in: the 31 px median never reaches the white cup
                med = cv2.medianBlur(f, 31)                          # thin logo lines vanish, flat kraft stays
                f = f.copy(); f[hull == 1] = med[hull == 1]
    p.stdin.write(f.tobytes()); i += 1
p.stdin.close(); p.wait(); print("wrote", dst, i, "frames")
