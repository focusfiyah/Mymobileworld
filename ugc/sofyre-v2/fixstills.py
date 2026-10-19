"""Free still fixes (2026-10-15): paste Ralph's reference bag over AI bags with a wrong print, crop a phone status bar,
remove brand text from props that must not carry it. Raw stills are kept in old/."""
import cv2, numpy as np, sys
def bag_paste(name, ref='view_1', hand=False, roi=None):
    im = cv2.imread(f'old/{name}_raw.png'); H, W = im.shape[:2]
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    r = np.zeros((H, W), np.uint8); x0, y0, x1, y1 = roi or (0, 0, W, H); r[y0:y1, x0:x1] = 1
    m = ((g < 75) & (r > 0)).astype(np.uint8); m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = 1 + np.argmax(st[1:, 4])
    cs, _ = cv2.findContours((lab == k).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = cv2.convexHull(max(cs, key=cv2.contourArea)); full = np.zeros((H, W), np.uint8); cv2.fillConvexPoly(full, hull, 1)
    x, y, w, h = cv2.boundingRect(hull); print(name, 'bag bbox', x, y, w, h, 'aspect', round(w / h, 2))
    b = {'view_1': (77, 36, 250, 293), 'view_2': (95, 31, 219, 364)}[ref]; rf = cv2.imread(f'refs/{ref}.jpg')[b[1]:b[1] + b[3], b[0]:b[0] + b[2]]
    up = cv2.resize(rf, (w, h), interpolation=cv2.INTER_AREA); canvas = im.copy(); canvas[y:y + h, x:x + w] = up
    mk = cv2.erode(full, np.ones((3, 3), np.uint8)).astype(np.float32)
    if hand:
        skin = ((hsv[..., 0] < 25) & (hsv[..., 1] > 55) & (hsv[..., 2] > 40)).astype(np.uint8)
        skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)); mk *= 1 - cv2.dilate(skin, np.ones((5, 5), np.uint8))
    mk = cv2.GaussianBlur(mk, (0, 0), 1.0)[..., None]
    out = (canvas * mk + im * (1 - mk)).astype(np.uint8); cv2.imwrite(f'stills/{name}.png', out)
    cv2.imwrite(f'/tmp/fix_{name}.png', np.hstack([im, out]))
if sys.argv[1] == 'bag':
    bag_paste('V1S6', 'view_1', roi=(100, 600, 700, 1376)); bag_paste('V3S1', 'view_1', hand=True, roi=(215, 470, 622, 1200))
else:
    im = cv2.imread('old/V1S2_raw.png'); H, W = im.shape[:2]; c = im[54:, :]; c = cv2.resize(c, None, fx=H / c.shape[0], fy=H / c.shape[0], interpolation=cv2.INTER_CUBIC)
    o = (c.shape[1] - W) // 2; cv2.imwrite('stills/V1S2.png', c[:, o:o + W]); print('V1S2', c.shape)
    im = cv2.imread('old/V3S2_raw.png'); box = (640, 800, 768, 870); sub = im[box[1]:box[3], box[0]:box[2]]
    gg = cv2.cvtColor(sub, cv2.COLOR_BGR2GRAY); mk = np.zeros(im.shape[:2], np.uint8); mk[box[1]:box[3], box[0]:box[2]] = ((gg < np.median(gg) - 25) * 255).astype(np.uint8)
    mk = cv2.dilate(mk, np.ones((7, 7), np.uint8)); cv2.imwrite('stills/V3S2.png', cv2.inpaint(im, mk, 5, cv2.INPAINT_TELEA))
    im = cv2.imread('old/V3S3_raw.png'); mk = np.zeros(im.shape[:2], np.uint8); mk[515:640, 585:730] = 255
    cv2.imwrite('stills/V3S3.png', cv2.inpaint(im, mk, 9, cv2.INPAINT_TELEA))
