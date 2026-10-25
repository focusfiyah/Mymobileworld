"""Free fix (2026-10-24): Seedance redrew eyelash tips past the profile on S6/S9 (Ralph: no eyes). Per frame, find thin
dark strokes (black-hat) in a box around the profile edge, keep only small pieces (lashes, not hair), inpaint them.
usage: python3 tools/lash_video.py S6 x0 y0 x1 y1  -> clips/S6_fix.mp4 (same fps/size, no audio)"""
import sys, subprocess, cv2, numpy as np
sid, x0, y0, x1, y1 = sys.argv[1], *map(int, sys.argv[2:6])
cap = cv2.VideoCapture(f"clips/{sid}.mp4"); fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps),
                      "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", f"clips/{sid}_fix.mp4"], stdin=subprocess.PIPE)
k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)); n = 0
while True:
    ok, f = cap.read()
    if not ok: break
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY); roi = g[y0:y1, x0:x1]
    bh = cv2.morphologyEx(roi, cv2.MORPH_BLACKHAT, k)
    m = ((bh > 28) & (roi < 95)).astype(np.uint8) * 255
    cnt, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = np.zeros_like(m)
    for i in range(1, cnt):
        if st[i, cv2.CC_STAT_AREA] < 400: keep[lab == i] = 255
    keep = cv2.dilate(keep, np.ones((5, 5), np.uint8))
    full = np.zeros((H, W), np.uint8); full[y0:y1, x0:x1] = keep
    if full.any(): f = cv2.inpaint(f, full, 6, cv2.INPAINT_TELEA); n += 1
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait(); print(sid, "frames painted", n)
