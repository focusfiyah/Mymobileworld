"""Free "room lights off" grade (Ralph 2026-10-03: darken the room to showcase the vanity's light colours).
Room drops to evening darkness (slightly cool); the mirror + door LED lines stay at full brightness with a soft glow that spills onto the
vanity; optional dip of the LEDs (for the word "dims").
  python3 darkroom.py IN OUT [--mask led_mask.png] [--colors T1 T2] [--on T0 T1] [--ramp T0 T1] [--dip T0 T1] [--dark 0.28] [--boxes x0,y0,x1,y1 ...]
"""
import subprocess, sys
import cv2, numpy as np
a = sys.argv; opt = lambda k, n=2: list(map(float, a[a.index(k) + 1:a.index(k) + 1 + n])) if k in a else None
src, out = a[1], a[2]; RAMP = opt("--ramp") or [0.0, 0.01]; DIP = opt("--dip"); DARK = (opt("--dark", 1) or [0.28])[0]
ON = opt("--on")   # LEDs switch on between T0 and T1 (before that they stay dark with the room)
COLS = opt("--colors")   # switch times: cold white -> warm white at T1 -> warm yellow at T2 (the listing's 3 modes)
MASK = a[a.index("--mask") + 1] if "--mask" in a else None   # static LED-line mask (lit frame minus the real unlit photo)
BOXES = [tuple(map(int, b.split(","))) for i, b in enumerate(a) if i > 0 and a[i - 1] == "--boxes"] or [(170, 430, 425, 660), (525, 360, 665, 920)]


def led_mask(f):
    g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32); hp = g - cv2.GaussianBlur(g, (0, 0), 6)
    m = ((hp > 9) & (g > 205)).astype(np.uint8); box = np.zeros_like(m)
    for x0, y0, x1, y1 in BOXES: box[y0:y1, x0:x1] = 1
    m &= box; m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)                    # keep long thin pieces (LED lines), drop specks
    keep = [i for i in range(1, n) if max(st[i, 2], st[i, 3]) > 40]
    return np.isin(lab, keep).astype(np.float32)


def ease(t, t0, t1): x = np.clip((t - t0) / max(t1 - t0, 1e-3), 0, 1); return x * x * (3 - 2 * x)


cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); w, h = int(cap.get(3)), int(cap.get(4))
ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                       "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
i, prev = 0, None
while True:
    ok, f = cap.read()
    if not ok: break
    t = i / fps; ff32 = f.astype(np.float32)
    if MASK: m = prev if prev is not None else cv2.resize(cv2.imread(MASK, 0), (w, h)).astype(np.float32) / 255; prev = m
    else: m = led_mask(f); m = m if prev is None else np.maximum(m, prev * 0.7); prev = m      # steady mask (no flicker)
    k = ease(t, *RAMP)                                                                       # 0 = daylight, 1 = room dark
    lit = ease(t, *ON) if ON else 1.0
    dip = 1 - 0.55 * (np.sin(np.pi * np.clip((t - DIP[0]) / (DIP[1] - DIP[0]), 0, 1)) if DIP else 0)
    room = ff32 * (1 - k * (1 - DARK)); room *= np.array([1 + 0.06 * k, 1.0, 1 - 0.05 * k], np.float32)   # darker + a touch cooler
    if COLS:   # BGR targets: cold white, warm white, warm yellow; 0.15 s cross-fade at each tap
        tg = [np.array(c, np.float32) for c in ((255, 242, 222), (205, 228, 255), (125, 200, 255))]
        e1, e2 = ease(t, COLS[0], COLS[0] + 0.15), ease(t, COLS[1], COLS[1] + 0.15)
        col = tg[0] * (1 - e1) + tg[1] * e1; col = col * (1 - e2) + tg[2] * e2
        lum = ff32.max(2, keepdims=True) / 255; src_led = lum * col
    else: src_led = ff32
    led = (src_led * m[..., None])
    core = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None]
    glow = cv2.GaussianBlur(led, (0, 0), 6) * 1.1 + cv2.GaussianBlur(led, (0, 0), 24) * 0.9           # LED light spilling onto the vanity
    core = core * lit
    o = room * (1 - core) + src_led * core * dip + k * dip * lit * glow
    ff.stdin.write(np.clip(o, 0, 255).astype(np.uint8).tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("darkroom", out, i, "frames")
