"""JIYU NAD+ Moisturizer, House of Rameau Black Friday version (Ralph 2026-11-12): Ralph's free Chatterbox VO (vo/), Grace's
approved real footage (her HD original, ugc/jiyu-nad-moisturizer/orig/jiyu_orig.mov) in a new order and framing, one free
Pexels gift clip on the gift line (broll/SOURCES.md), hook text from frame 0. Shots start on their line (vo/words.json).
  python3 cut.py  (REVIEW_ONLY=1 for the quick render)"""
import sys
sys.path.insert(0, "../_bf_c_tools")
from build import build
G = "../../../ugc/jiyu-nad-moisturizer/orig/jiyu_orig.mov"
PX = "../_bf_c_tools/pexels/"
SEGS = [  # (VO line, offset s, source, in s, crop w:h:x:y)
    (0, 0.0, G, 54.30, "1000:1778:40:60"),    # hook: close on the thick whipped cream in the jar
    (1, 0.0, G, 3.00, "960:1707:60:100"),     # dry/tight: the pink box
    (1, 1.80, G, 7.20, "1000:1778:40:80"),    # insert card "time is part of the formula"
    (2, 0.0, G, 46.20, "940:1671:70:130"),    # "Jiyu moisturizer, powered by NAD+": jar label front
    (3, 0.0, G, 61.80, "1000:1778:40:80"),    # scoop on her fingertip
    (3, 1.30, G, 66.00, "960:1707:60:120"),   # rubs it in on the back of her hand
    (4, 0.0, G, 70.00, "1000:1778:40:90"),    # brag: still rubbing it in, skin soft
    (5, 0.0, PX + "6098638.mp4", 1.0, "1080:1920:0:0"),  # gift: red gift box with bow (Pexels 6098638)
    (5, 1.60, G, 11.50, "1000:1778:30:60"),   # the pink box open, jar inside (ends before the 14.2 s zoom blur)
    (6, 0.0, G, 29.50, "980:1742:50:80"),     # close: pink lid, JIYU logo
]
build("bf_jiyu_nad", SEGS, "I do not think the|picture really shows|how thick this is")
