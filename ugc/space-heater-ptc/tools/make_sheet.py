"""My product reference sheet, real listing pixels only (Antarctic Star listing, TikTok Shop 1731771753156284835).
refs/product_sheet.png: big real front (cut out of d01, no heat glow) + real top panel (g01) + real top at an angle (g09)
+ real remote (g09) + facts. Free. Run: python3 tools/make_sheet.py"""
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
R = "refs/listing/"
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
f_big, f_sm = ImageFont.truetype(F, 34), ImageFont.truetype(F.replace("-Bold", ""), 26)
BG = (226, 226, 226)

def grab(img, box):
    """GrabCut cut-out inside box -> RGBA (used for the big front; threshold left beige wedges at the base)."""
    m = np.zeros(img.shape[:2], np.uint8); bg, fg = np.zeros((1, 65)), np.zeros((1, 65))
    x0, y0, x1, y1 = box
    cv2.grabCut(img, m, (x0, y0, x1 - x0, y1 - y0), bg, fg, 6, cv2.GC_INIT_WITH_RECT)
    k = np.where((m == 1) | (m == 3), 255, 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(k); k = ((lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])) * 255).astype(np.uint8)
    cnts, _ = cv2.findContours(k, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); k = np.zeros_like(k); cv2.drawContours(k, cnts, -1, 255, -1)
    k = cv2.GaussianBlur(cv2.erode(k, np.ones((3, 3), np.uint8)), (3, 3), 0)
    rgba = np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), k]); x, y, w, h = cv2.boundingRect((k > 128).astype(np.uint8))
    return Image.fromarray(rgba[y:y+h, x:x+w])

def cutout(img, box, thr=95):
    """Dark product on a light background -> RGBA (largest dark blob, holes filled, edge softened)."""
    a = img[box[1]:box[3], box[0]:box[2]]
    g = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    m = (g < thr).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); m = (lab == k).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = np.zeros_like(m); cv2.drawContours(m, cnts, -1, 255, -1)
    m = cv2.erode(m, np.ones((3, 3), np.uint8)); m = cv2.GaussianBlur(m, (5, 5), 0)
    rgba = np.dstack([cv2.cvtColor(a, cv2.COLOR_BGR2RGB), m])
    x, y, w, h = cv2.boundingRect((m > 128).astype(np.uint8))
    return Image.fromarray(rgba[y:y+h, x:x+w])

d01, g01, g09 = (cv2.imread(R + f) for f in ("d01.jpg", "g01.jpg", "g09.jpg"))
front = grab(d01, (478, 540, 1072, 1390))
top = Image.fromarray(cv2.cvtColor(g01[300:560, 480:1270], cv2.COLOR_BGR2RGB))       # real touch panel, close (no glow)
angle = Image.fromarray(cv2.cvtColor(d01[540:640, 480:1070], cv2.COLOR_BGR2RGB))       # real top seen from the front (eye level)
remote = cutout(g09, (100, 1070, 330, 1500), thr=110)

W, H = 2000, 1500
s = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(s)
fh = 1240; fw = round(front.width * fh / front.height); fr = front.resize((fw, fh), Image.LANCZOS)
s.paste(fr, (60, 150), fr)
d.text((60, 40), "REAL FRONT (listing photo): matte black cylinder, 8.7 in tall x 6.2 in wide", font=f_big, fill=(20, 20, 20))
d.text((60, 90), f"height = {fh/fw:.2f} x width. Hex mesh all round; rectangular heater window with vertical bars; plain dark base band", font=f_sm, fill=(40, 40, 40))
x0 = 60 + fw + 70; cw = W - x0 - 50
def panel(img, y, title, sub, h):
    w = round(img.width * h / img.height)
    if w > cw: w, h = cw, round(img.height * cw / img.width)
    im = img.resize((w, h), Image.LANCZOS)
    if im.mode == "RGBA": s.paste(im, (x0, y + 80), im)
    else: s.paste(im, (x0, y + 80))
    d.text((x0, y), title, font=f_big, fill=(20, 20, 20)); d.text((x0, y + 42), sub, font=f_sm, fill=(40, 40, 40))
    return y + 80 + h + 40
y = panel(top, 150, "REAL TOP: round glossy black touch panel", "white display '73', 6 outlined buttons + red power; slotted vent ring", 400)
y = panel(angle, y, "REAL TOP at eye level", "panel is a thin raised disc; vent slots ring it; nothing sticks up", 150)
w = round(remote.width * 300 / remote.height); rm = remote.resize((w, 300), Image.LANCZOS); s.paste(rm, (x0, y + 80), rm)
d.text((x0, y), "REAL REMOTE", font=f_big, fill=(20, 20, 20))
d.text((x0 + w + 40, y + 90), "small black remote,\n7 buttons:\npower, lock, fan/light,\ntimer, mode, minus, plus", font=f_sm, fill=(40, 40, 40))
d.text((60, H - 55), "Real pixels only (Antarctic Star listing). The listing has no back or bottom photo: do not invent a handle or vents.", font=f_sm, fill=(120, 0, 0))
s.save("refs/product_sheet.png")
front.save("refs/front_cutout.png"); remote.save("refs/remote_cutout.png"); top.save("refs/top_panel.png")
print("ok", front.size, remote.size, f"ratio {front.height/front.width:.2f}")
