"""Grace's on-screen line for V3 (Ralph tapped "Yes, whole video" 2026-11-07): TikTok-style white rounded boxes, one per
line, dark text, centred in the top half, inside the safe zone x 60-940, y 360-1340. Writes v3/overlay/text.png (1080x1920,
transparent) and prints the box for hook_check.py --hook."""
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
LINES = ["It's beginning to smell", "a lot like Christmas"]
f = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 66)
im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
padx, pady, gap, y = 34, 20, 10, 430
boxes = []
for ln in LINES:
    x0, y0, x1, y1 = d.textbbox((0, 0), ln, font=f); tw, th = x1 - x0, y1 - y0
    bw, bh = tw + 2 * padx, th + 2 * pady; bx = (W - bw) // 2
    d.rounded_rectangle((bx, y, bx + bw, y + bh), radius=22, fill=(255, 255, 255, 245))
    d.text((bx + padx - x0, y + pady - y0), ln, font=f, fill=(28, 24, 24, 255))
    boxes.append((bx, y, bx + bw, y + bh)); y += bh + gap
X0 = min(b[0] for b in boxes); Y0 = boxes[0][1]; X1 = max(b[2] for b in boxes); Y1 = boxes[-1][3]
assert X0 >= 60 and X1 <= 940 and Y0 >= 360 and Y1 <= 1340, (X0, Y0, X1, Y1)
im.save("v3/overlay/text.png"); print(f"HOOK_BOX {X0},{Y0},{X1-X0},{Y1-Y0}")
