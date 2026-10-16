"""Free fix (Ralph 2026-10-16: the AI-drawn plug is the wrong size/place; remove it, the VO only mentions it). Tracks each object
from a seed frame forwards and backwards (template match, re-templated slowly for push-ins), stops where the match is lost, and
paints it out (OpenCV inpaint, soft edge). python3 tools/unplug_track.py IN OUT "t,cx,cy,hw,hh" [...]  [--check DIR]"""
import sys, subprocess, cv2, numpy as np
av = sys.argv[1:]; ci = av.index("--check") if "--check" in av else len(av); args = av[:ci]; src, dst = args[0], args[1]
seeds = [tuple(float(v) for v in a.split(",")) for a in args[2:]]
chk = sys.argv[sys.argv.index("--check") + 1] if "--check" in sys.argv else None
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
N, (H, W) = len(frames), frames[0].shape[:2]
def track(t, cx, cy, hw, hh):
    i0 = min(int(round(t * fps)), N - 1); pos = {i0: (cx, cy, 1.0)}
    g = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]
    T0 = g[i0][int(cy - hh):int(cy + hh), int(cx - hw):int(cx + hw)].astype(np.float32)
    for step in (1, -1):
        x, y, s, T = cx, cy, 1.0, T0.copy(); i = i0 + step
        while 0 <= i < N:
            best = (-1, None)
            for sc in (s * 0.96, s, s * 1.04):
                th, tw = max(int(2 * hh * sc), 8), max(int(2 * hw * sc), 8); Tt = cv2.resize(T, (tw, th))
                x0, y0 = int(max(x - tw / 2 - 30, 0)), int(max(y - th / 2 - 30, 0)); x1, y1 = int(min(x + tw / 2 + 30, W)), int(min(y + th / 2 + 30, H))
                R = g[i][y0:y1, x0:x1].astype(np.float32)
                if R.shape[0] <= th or R.shape[1] <= tw: continue
                r = cv2.matchTemplate(R, Tt, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
                if mv > best[0]: best = (mv, (x0 + ml[0] + tw / 2, y0 + ml[1] + th / 2, sc))
            if best[0] < 0.45: break
            x, y, s = best[1]; pos[i] = (x, y, s)
            th, tw = int(2 * hh * s), int(2 * hw * s)
            P = g[i][int(y - th / 2):int(y - th / 2) + th, int(x - tw / 2):int(x - tw / 2) + tw].astype(np.float32)
            if P.shape == (th, tw) and th > 0 and tw > 0: T = 0.85 * cv2.resize(T, (tw, th)) + 0.15 * P; T = cv2.resize(T, (int(2 * hw), int(2 * hh)))
            i += step
    return pos
tracks = [track(*sd) for sd in seeds]
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
for i, f in enumerate(frames):
    m = np.zeros((H, W), np.uint8)
    for (t, cx, cy, hw, hh), tr in zip(seeds, tracks):
        if i in tr:
            x, y, s = tr[i]; cv2.ellipse(m, (int(x), int(y)), (int(hw * s * 1.35), int(hh * s * 1.35)), 0, 0, 360, 255, -1)
    if m.any():
        fill = cv2.inpaint(f, m, 9, cv2.INPAINT_TELEA); soft = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 3)[..., None]
        f = (f * (1 - soft) + fill * soft).astype(np.uint8)
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
print(dst, "frames", N, "tracked:", [(min(tr) / fps, max(tr) / fps) for tr in tracks])
if chk:
    for k, (t, cx, cy, hw, hh) in enumerate(seeds):
        i0 = int(round(t * fps)); c = frames[min(i0, N - 1)][max(int(cy - hh * 3), 0):int(cy + hh * 3), max(int(cx - hw * 3), 0):int(cx + hw * 3)]
        if c.size: cv2.imwrite(f"{chk}/seed_{k}.png", cv2.resize(c, None, fx=2, fy=2))
