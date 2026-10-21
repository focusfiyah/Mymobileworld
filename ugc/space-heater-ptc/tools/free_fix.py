"""Free still fixes (Ralph 2026-10-19: free methods first, paid edits only if these fail). Sources are kept in stills/r2, stills/r3.
  python3 tools/free_fix.py S3|S5|S8"""
import sys
import cv2, numpy as np
from PIL import Image

def s3():
    """Round 2's S3 (right heater + grip, wrong rope-chain bracelet): crop the bracelet out of frame, so the hand enters from the top edge."""
    im = Image.open("stills/r2/V1S3.png").convert("RGB"); y0 = 418; h = im.height - y0; w = round(h * 9 / 16)
    x0 = 108; im.crop((x0, y0, x0 + w, im.height)).resize((768, 1376), Image.LANCZOS).save("stills/V1S3.png")

{"S3": s3}[sys.argv[1]]() if sys.argv[1] in ("S3",) else None


def s5():
    """Round 3's S5 had the blue ring on the THUMB: Poisson-clone thumb skin from 55 px further along the thumb over the ring (no ring
    visible in this shot; her ring finger is hidden behind the mug)."""
    im = cv2.imread("stills/r3/V1S5.png"); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (85, 30, 50), (125, 255, 255)); m[:700] = 0; m[900:] = 0; m[:, :250] = 0; m[:, 350:] = 0
    m = cv2.dilate(m, np.ones((11, 11), np.uint8)); ys, xs = np.where(m > 0)
    src = cv2.warpAffine(im, np.float32([[1, 0, 18], [0, 1, -55]]), (im.shape[1], im.shape[0]), borderMode=cv2.BORDER_REFLECT)
    sub = np.zeros_like(m); sub[ys.min() - 2:ys.max() + 3, xs.min() - 2:xs.max() + 3] = m[ys.min() - 2:ys.max() + 3, xs.min() - 2:xs.max() + 3]
    cv2.imwrite("stills/V1S5.png", cv2.seamlessClone(src, im, sub, (int((xs.min() + xs.max()) / 2), int((ys.min() + ys.max()) / 2)), cv2.NORMAL_CLONE))


if __name__ == "__main__" and sys.argv[1] == "S5":
    s5()


def s8():
    """Round 3's S8 (right hand) had word buttons 'ECO' and 'MODE' (the real panel has icons only): inside each button keep the outline
    (largest bright component), inpaint the letters, draw a thin white icon (lock, thermometer) at the outline's centre; fingertip kept."""
    im = cv2.imread("stills/r3/V1S8.png"); out = im.copy(); g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    skin = cv2.dilate(cv2.inRange(hsv, (0, 40, 60), (25, 255, 255)) | cv2.inRange(hsv, (160, 30, 60), (180, 255, 255)), np.ones((5, 5), np.uint8))
    W = (235, 235, 235)
    for (cx, cy, icon) in [(290, 529, "lock"), (414, 611, "thermo")]:
        x0, y0 = cx - 34, cy - 26; box = g[y0:cy + 26, x0:cx + 34]
        b = ((box > 95) & (skin[y0:cy + 26, x0:cx + 34] == 0)).astype(np.uint8)
        n, lab, st, cen = cv2.connectedComponentsWithStats(b, 8)
        ring = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA] * (st[1:, cv2.CC_STAT_WIDTH] + st[1:, cv2.CC_STAT_HEIGHT]))
        rx, ry, rw, rh = st[ring, :4]; ocx, ocy = x0 + rx + rw / 2, y0 + ry + rh / 2
        txt = np.zeros(g.shape, np.uint8)
        for i in range(1, n):
            if i != ring: txt[y0:cy + 26, x0:cx + 34][lab == i] = 255
        txt = cv2.dilate(txt, np.ones((3, 3), np.uint8)) & ~skin
        out = cv2.inpaint(out, txt, 3, cv2.INPAINT_TELEA)
        s = min(rw, rh) * 0.55
        if icon == "lock":
            cv2.rectangle(out, (int(ocx - s * .4), int(ocy - s * .05)), (int(ocx + s * .4), int(ocy + s * .55)), W, 1, cv2.LINE_AA)
            cv2.ellipse(out, (int(ocx), int(ocy - s * .05)), (int(s * .25), int(s * .38)), 0, 180, 360, W, 1, cv2.LINE_AA)
        else:
            ty = ocy - 3   # thermometer: short stem + small bulb, kept above the fingertip
            cv2.line(out, (int(ocx), int(ty - 7)), (int(ocx), int(ty + 3)), W, 1, cv2.LINE_AA)
            cv2.circle(out, (int(ocx), int(ty + 6)), 3, W, 1, cv2.LINE_AA)
            for k in (-4, -1): cv2.line(out, (int(ocx + 2), int(ty + k)), (int(ocx + 4), int(ty + k)), W, 1, cv2.LINE_AA)
        out[skin > 0] = im[skin > 0]
    cv2.imwrite("stills/V1S8.png", out)


if __name__ == "__main__" and sys.argv[1] == "S8":
    s8()
