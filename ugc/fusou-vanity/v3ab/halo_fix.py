"""Free halo removal on a Kling pointing clip: the start still had a light sticker outline around the hand. Per frame: hand mask (HSV skin, blob on the left/right frame edge, holes filled),
band = ring just outside the hand, inpaint the band from the surrounding scene, then paste the untouched hand pixels back on top.
  python3 v3ab/halo_fix.py clips/P1_kling.mp4 clips/P1_kling_fix.mp4 [--side left|right]"""
import subprocess, sys
import cv2, numpy as np
src, out = sys.argv[1:3]; side = sys.argv[sys.argv.index("--side") + 1] if "--side" in sys.argv else "left"
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS) or 24; W, H = int(cap.get(3)), int(cap.get(4))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
K = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n)); col = 0 if side == "left" else W - 1
while True:
    ok, f = cap.read()
    if not ok: break
    h_, sa, v = cv2.split(cv2.cvtColor(f, cv2.COLOR_BGR2HSV))
    m = ((h_ >= 3) & (h_ <= 22) & (sa > 55) & (v < 225) & (v > 30)).astype(np.uint8)
    if side == "left": m[:, int(W * .5):] = 0
    else: m[:, :int(W * .5)] = 0
    m[:int(H * .35)] = 0; m[int(H * .95):] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, K(3)); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, K(25))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = [i for i in range(1, n) if st[i, 4] > 1200 and (lab[:, col] == i).any()]
    hand = np.isin(lab, keep).astype(np.uint8)
    cs, _ = cv2.findContours(hand, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); cv2.drawContours(hand, cs, -1, 1, cv2.FILLED)
    if not hand.any(): ff.stdin.write(f.tobytes()); continue
    band = (cv2.dilate(hand, K(23)) & (1 - cv2.erode(hand, K(3)))).astype(np.uint8) * 255      # ring around the hand incl. its own rim
    fixed = cv2.inpaint(f, band, 6, cv2.INPAINT_TELEA)
    a = cv2.GaussianBlur(cv2.erode(hand, K(5)).astype(np.float32), (0, 0), 1.2)[..., None]       # keep the original hand pixels
    ff.stdin.write((f * a + fixed * (1 - a)).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
