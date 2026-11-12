"""PURCELL 247 Colostrum Mist, House of Rameau Black Friday version (Ralph 2026-11-12): Ralph's free Chatterbox VO (vo/),
Grace's approved real footage (her HD original, ugc/purcell-colostrum-mist/orig/grace_orig.mov) in a new order and framing,
one free Pexels stocking clip (broll/SOURCES.md) on the stocking line, hook text from frame 0. Shots start on their line (vo/words.json).
  python3 cut.py  (REVIEW_ONLY=1 for the quick render)"""
import sys
sys.path.insert(0, "../_bf_c_tools")
from build import build
G = "../../../ugc/purcell-colostrum-mist/orig/grace_orig.mov"
PX = "../_bf_c_tools/pexels/"
SEGS = [  # (VO line, offset s, source, in s, crop w:h:x:y)
    (0, 0.0, G, 8.10, "1000:1778:40:0"),     # hook: bottle brought up in her hand (purse size)
    (1, 0.0, G, 3.40, "980:1742:60:40"),      # tired/oily: the box, before & after makeup, glowing skin
    (1, 1.65, G, 23.30, "1000:1778:30:60"),   # back label + spray head
    (2, 0.0, G, 12.00, "940:1671:70:120"),    # "Purcell colostrum mist": front label close
    (3, 0.0, G, 25.90, "1000:1778:40:80"),    # one spray onto the back of her hand, goes dewy
    (4, 0.0, G, 29.60, "900:1600:120:200"),   # before/over makeup: tight on the dewy glow
    (5, 0.0, G, 33.00, "1000:1778:20:80"),    # brag: glowing hand, bottle comes in
    (6, 0.0, PX + "6111172.mp4", 1.0, "1080:1920:0:0"),  # holiday: white tree with gifts (Pexels 6111172)
    (6, 1.30, G, 36.60, "960:1707:60:110"),   # bottle held up by the glowing hand
    (7, 0.0, G, 38.00, "1000:1778:40:70"),    # close: bottle in both hands (stops before the 39.75 s refocus blur)
]
build("bf_purcell", SEGS, "This stays in my wife's|purse for a reason", hook_y=362)
