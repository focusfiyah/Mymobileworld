"""Real charm laid back onto a Seedance clip, frame by frame (Mini Bag Charm 2026-10-27). Seedance keeps the true size
but redraws the tiny real charm (a flap, a mark on the padlock, a wide scarf), so: the camera move is tracked on the
background (ORB + RANSAC, still -> frame), the AI charm is covered with the clean plate warped the same way, and the
real composite layer (charm, chain, ring, shadow) is warped on top. Free; a paste-back, so used only on Ralph's OK.
  python3 tools/track_paste.py S7 [--follow]  -> clips/S7_track.mp4  (--follow: the charm hangs from a moving hand, S4)"""
import subprocess, sys
import cv2, numpy as np

PLATE = {"S4": "stills/plate_S4.png", "S7": "stills/S7bg.png", "S8": "rooms/roomE_stocking2_crop.png", "S9": "stills/S9bg.png"}


def frames(path):
    cap = cv2.VideoCapture(path)
    while True:
        ok, f = cap.read()
        if not ok: return
        yield f


def charm_colours(f):
    """Pixels that belong to a burgundy charm, its pink / light blue / pale scarf, its tissue or its gold hardware."""
    b, g, r = [f[..., i].astype(int) for i in range(3)]
    burg = (r > 55) & (r < 175) & (g < r * 0.45) & (b > g) & (b < r * 0.8)
    pink = (r > 150) & (r - g > 30) & (b > g) & (g > r * 0.45)        # pink scarf, not a red stocking
    blue = (b > r + 15) & (b > 120)
    gold = (r > 150) & (g > 100) & (b < g * 0.7)
    return (burg | pink | blue | gold).astype(np.uint8) * 255


def run(sid, follow=False):
    still = cv2.imread(f"stills/{sid}.png"); plate = cv2.imread(PLATE[sid])
    diff = (np.abs(still.astype(int) - plate.astype(int)).max(2) > 3).astype(np.uint8) * 255
    diff = cv2.morphologyEx(diff, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    ov_a = cv2.GaussianBlur(diff, (3, 3), 0)                       # the real layer: charm, chain, ring, shadow
    import os
    if os.path.exists(f"stills/overlay_{sid}.png"):               # an uncut layer saved by composite.py (S8)
        o = cv2.imread(f"stills/overlay_{sid}.png", cv2.IMREAD_UNCHANGED); still = o[..., :3].copy(); ov_a = o[..., 3].copy()
    x, y, w, h = cv2.boundingRect(diff)
    keep = np.zeros(plate.shape[:2], np.uint8)                     # track the handbag NEAR the charm (no parallax from the far room)
    keep[max(0, y - h):y + 3 * h, max(0, x - 2 * w):x + 3 * w] = 255
    keep[max(0, y - h // 3):y + int(1.6 * h), max(0, x - w // 3):x + int(1.4 * w)] = 0
    orb = cv2.ORB_create(4000, fastThreshold=7); kp0, d0 = orb.detectAndCompute(cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY), keep)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    src = list(frames(f"clips/{sid}_seedance.mp4")); FH, FW = src[0].shape[:2]
    Ms = []
    for f in src:
        kp1, d1 = orb.detectAndCompute(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), None)
        mt = sorted(bf.match(d0, d1), key=lambda m: m.distance)[:600]
        a = np.float32([kp0[m.queryIdx].pt for m in mt]); b = np.float32([kp1[m.trainIdx].pt for m in mt])
        M, inl = cv2.estimateAffinePartial2D(a, b, method=cv2.RANSAC, ransacReprojThreshold=2.5)
        Ms.append(M)
    Ms = np.array(Ms); k = 7                                       # smooth the track (no jitter)
    Ms = np.array([Ms[max(0, i - k):i + k + 1].mean(0) for i in range(len(Ms))])
    hang0 = None; hx = []
    if follow:                                                     # where the AI charm hangs in each frame
        for f in src:
            m = charm_colours(f); m[:int(FH * 0.45)] = 0; ys, xs = np.nonzero(m)
            hx.append((np.median(xs), np.percentile(ys, 3)) if len(xs) > 200 else (np.nan, np.nan))
        hx = np.array(hx, float); good = ~np.isnan(hx[:, 0])
        for j in range(2): hx[:, j] = np.interp(np.arange(len(hx)), np.nonzero(good)[0], hx[good, j])
        hx = np.array([hx[max(0, i - 4):i + 5].mean(0) for i in range(len(hx))])
    out = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{FW}x{FH}", "-r", "24",
                            "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", f"clips/{sid}_track.mp4"],
                           stdin=subprocess.PIPE)
    for i, f in enumerate(src):
        M = Ms[i].copy()
        if follow:
            p0 = M @ np.array([x + w / 2, y, 1.0])
            if hang0 is None: hang0 = hx[0] - p0
            M[:, 2] += (hx[i] - p0) - hang0
        wp = cv2.warpAffine(plate, Ms[i], (FW, FH), borderMode=cv2.BORDER_REPLICATE)
        ws = cv2.warpAffine(still, M, (FW, FH), borderMode=cv2.BORDER_REPLICATE)
        wa = cv2.warpAffine(ov_a, M, (FW, FH)).astype(np.float32)[..., None] / 255
        # cover the AI charm: its colours near where the real one sits, grown a little, filled from the warped plate
        bx = cv2.boundingRect(cv2.warpAffine(diff, M, (FW, FH)))
        roi = np.zeros((FH, FW), np.uint8); X, Y, Wd, Hd = bx
        e = 0.35 if sid == 'S8' else 1.0               # S8: the AI charm sits where the real one does; spare the red stocking
        roi[max(0, Y - int(e * Hd)):Y + int((1 + e) * Hd), max(0, X - int(e * Wd)):X + int((1 + e) * Wd)] = 255
        cov = cv2.dilate(charm_colours(f) & roi, np.ones((13, 13), np.uint8))
        if sid == "S8":                                           # never paint over the cuff's own white fur
            fi = f.astype(int); cov[(fi.min(2) > 160) & (fi.max(2) - fi.min(2) < 45)] = 0
        ring = cv2.dilate(cov, np.ones((15, 15), np.uint8)) & ~cov
        fill = cv2.inpaint(f, cov, 7, cv2.INPAINT_TELEA).astype(np.float32)   # from the frame itself: no misaligned plate
        ca = cv2.GaussianBlur(cov, (9, 9), 0).astype(np.float32)[..., None] / 255
        g = f.astype(np.float32) * (1 - ca) + fill * ca
        if sid == "S8":                                           # the real charm stays BEHIND this frame's own white cuff
            fi = f.astype(int); fur = ((fi.min(2) > 165) & (fi.max(2) - fi.min(2) < 40)).astype(np.uint8) * 255
            fur = cv2.GaussianBlur(cv2.morphologyEx(fur, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)), (5, 5), 0)
            wa = wa * (1 - fur.astype(np.float32)[..., None] / 255)
        g = g * (1 - wa) + ws.astype(np.float32) * wa
        out.stdin.write(np.clip(g, 0, 255).astype(np.uint8).tobytes())
    out.stdin.close(); out.wait(); print(sid, "tracked", len(src), "frames -> clips/" + sid + "_track.mp4")


if __name__ == "__main__":
    run(sys.argv[1], "--follow" in sys.argv)
