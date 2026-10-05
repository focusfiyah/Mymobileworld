"""Free animated pointing shot from the CLEAN still hand (no AI clip artifacts): the small hand slides in from the left edge, points, bobs, slides out; whole frame has a slight handheld sway.
  python3 v3ab/hand_still_anim.py clips/P1_anim.mp4 [dur 4.0]"""
import subprocess, sys, math
import cv2, numpy as np
out = sys.argv[1]; dur = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0; FPS, W, H = 24, 800, 1422
P = cv2.imread("stills/P1.png"); B = cv2.imread("refs/base_A_916.jpg"); Hm = cv2.imread("v3ab/hand_mask.png", 0)
s, A, dst = 0.55, (230, 1000), (-5, 1010)
T = np.float32([[s, 0, dst[0] - s * A[0]], [0, s, dst[1] - s * A[1]]])
hp = cv2.warpAffine(P, T, (W, H), flags=cv2.INTER_AREA); hm = cv2.GaussianBlur(cv2.warpAffine(Hm, T, (W, H), flags=cv2.INTER_AREA), (0, 0), 1.0).astype(np.float32) / 255
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
ease = lambda x: x * x * (3 - 2 * x)
for i in range(int(dur * FPS)):
    t = i / FPS
    a = ease(min(1, t / 0.6)) * (1 - ease(min(1, max(0, (t - (dur - 0.6)) / 0.6))))      # in 0-0.6 s, out in the last 0.6 s
    dx = -140 * (1 - a) + 4 * math.sin(t * 3.1) * a; dy = 10 * (1 - a) + 5 * math.sin(t * 2.3 + 1) * a
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    hpm = cv2.warpAffine(hp, M, (W, H), flags=cv2.INTER_LINEAR); hmm = cv2.warpAffine(hm, M, (W, H), flags=cv2.INTER_LINEAR)[..., None] if hm.ndim == 3 else cv2.warpAffine(hm, M, (W, H))[..., None]
    frame = (hpm * hmm + B * (1 - hmm)).astype(np.uint8)
    z = 1.03 + 0.004 * math.sin(t * 1.7); sx = 6 * math.sin(t * 1.3); sy = 8 * math.sin(t * 1.1 + 0.5)       # handheld sway (whole frame)
    G = np.float32([[z, 0, W / 2 - z * W / 2 + sx], [0, z, H / 2 - z * H / 2 + sy]])
    ff.stdin.write(cv2.warpAffine(frame, G, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).tobytes())
ff.stdin.close(); ff.wait()
