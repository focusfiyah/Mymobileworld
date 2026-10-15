"""Free fix: the AI tints the pouch edges pink (nail-polish bleed). Real pouch = plain white. Desaturate pink-ish low-sat pixels
that are not on skin/nails (skin mask dilated). Raw stills stay in old/."""
import cv2, numpy as np, sys
for n in sys.argv[1:]:
    im = cv2.imread(f'old/{n}_raw.png'); hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32); h, s, v = cv2.split(hsv)
    skin = ((h < 25) & (s > 70) & (v > 40)).astype(np.uint8); skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    near = cv2.dilate(skin, np.ones((21, 21), np.uint8)) > 0
    pink = ((h > 150) | (h < 8)) & (s > 12) & (s < 170) & (v > 170) & ~near
    # keep it to pixels that sit next to a very white pouch body
    white = cv2.GaussianBlur(((s < 25) & (v > 200)).astype(np.float32), (0, 0), 9) > 0.15
    mk = (pink & white).astype(np.float32); mk = cv2.GaussianBlur(mk, (0, 0), 2.0)
    s2 = s * (1 - 0.9 * mk); out = cv2.cvtColor(cv2.merge([h, s2, v]).astype(np.uint8), cv2.COLOR_HSV2BGR)
    cv2.imwrite(f'stills/{n}.png', out); print(n, 'pixels fixed', int((mk > 0.5).sum()))
