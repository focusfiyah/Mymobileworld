"""Free pointing-hand clips on the REAL BEDROOM wide (stills/BEDROOM_WIDE_drive_v2.png, from the approved Drive Video 2). Ralph 2026-10-04: all free.
The small hand (Grace's hand from stills/P1.png, eroded mask, no halo) slides in from the frame edge, points at the lit mirror (P1, left edge) or the full-length mirror (P2, right edge), holds, slides out.
2.5D move: background and hand zoom at different rates (parallax) + slight handheld sway. Camera never reveals a forearm: the wrist sits on the frame edge.
  python3 v3ab/hand_bedroom.py P1 clips/P1_O1.mp4 3.0 clips/O1.mp4 0   (hand over a 3D clip)  |  python3 v3ab/hand_bedroom.py P1 clips/P1_bed.mp4 4.0     |     python3 v3ab/hand_bedroom.py P2 clips/P2_bed.mp4 2.0   (run from ugc/fusou-vanity)"""
import math, subprocess, sys
import cv2, numpy as np
which, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3]); W, H, FPS = 720, 1280, 24
VID = sys.argv[4] if len(sys.argv) > 4 else None; VSS = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0   # 2026-10-05 motion redo: hand over a REAL 3D camera clip (the hand moves with the camera, like the hand of whoever holds the phone)
cap = None
if VID: cap = cv2.VideoCapture(VID); cap.set(cv2.CAP_PROP_POS_FRAMES, round(VSS * FPS))
BG = cv2.imread("stills/BEDROOM_WIDE_drive_v2.png"); P = cv2.imread("stills/P1.png"); Hm = cv2.imread("v3ab/hand_mask.png", 0)
S, ANG, A = 0.495, -20, (230, 1000)                                           # scale into the 720x1280 frame; rotate the finger toward the mirror; wrist anchor in P1 coords
dst = (-6, 820) if which == "P1" else (-6, 820)
M = cv2.getRotationMatrix2D(A, ANG, S); M[0, 2] += dst[0] - A[0]; M[1, 2] += dst[1] - A[1]
hp = cv2.warpAffine(P, M, (W, H), flags=cv2.INTER_AREA); hm = (cv2.warpAffine(Hm, M, (W, H), flags=cv2.INTER_AREA) > 127).astype(np.uint8)
hm = cv2.erode(hm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
hsv = cv2.cvtColor(hp, cv2.COLOR_BGR2HSV); white = ((hsv[..., 2] > 195) & (hsv[..., 1] < 45)).astype(np.uint8)          # near-white patches = the old photo showing through (knuckle gaps, rim): not skin
core = cv2.erode(hm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))                                              # deep inside the hand: keep everything (white French tips!)
white = cv2.dilate(white, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))) * (1 - core); hm = hm * (1 - white)
hm = cv2.GaussianBlur(hm.astype(np.float32), (0, 0), 0.8)
if which == "P2": hp, hm = cv2.flip(hp, 1), cv2.flip(hm, 1)                    # right edge, pointing up-left
side = -1 if which == "P1" else 1                                                # slide-in direction offset sign
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
ease = lambda x: x * x * (3 - 2 * x); C = np.float32([W / 2, H / 2])
def zoom(img, z, dx=0, dy=0, interp=cv2.INTER_LINEAR):
    G = np.float32([[z, 0, C[0] - z * C[0] + dx], [0, z, C[1] - z * C[1] + dy]]); return cv2.warpAffine(img, G, (W, H), flags=interp, borderMode=cv2.BORDER_REFLECT)
for i in range(int(dur * FPS)):
    t = i / FPS; p = t / dur
    TI, TO = (1.4, 0.9) if cap is not None else (0.5, 0.45)                                   # Ralph 2026-10-05: "slow down the hand, it comes in too fast" -> 1.4 s in over 3D clips
    a = ease(min(1, t / TI)) * (1 - ease(min(1, max(0, (t - (dur - TO)) / TO))))
    hx = side * 140 * (1 - a) + 3 * math.sin(t * 3.1) * a; hy = 8 * (1 - a) + 4 * math.sin(t * 2.3 + 1) * a
    sx, sy = 5 * math.sin(t * 1.3), 7 * math.sin(t * 1.1 + 0.5)                               # handheld sway
    if cap is not None: ok, fr = cap.read(); assert ok, "background clip too short (never stretch)"; bg = cv2.resize(fr, (W, H)); sx, sy = sx * 0.5, sy * 0.5
    else: bg = zoom(BG, 1.0 + 0.06 * p, sx, sy)                                                # background push-in (far)
    Mh = np.float32([[1, 0, hx], [0, 1, hy]])
    hpl = cv2.warpAffine(hp, Mh, (W, H), flags=cv2.INTER_LINEAR); hml = cv2.warpAffine(hm, Mh, (W, H), flags=cv2.INTER_LINEAR)
    hpl, hml = zoom(hpl, 1.0 + (0 if cap is not None else 0.09) * p, sx * 1.4, sy * 1.4), zoom(hml, 1.0 + (0 if cap is not None else 0.09) * p, sx * 1.4, sy * 1.4)   # hand push-in is faster (near) = parallax
    a3 = hml[..., None]; ff.stdin.write((hpl * a3 + bg * (1 - a3)).astype(np.uint8).tobytes())
ff.stdin.close(); ff.wait()
