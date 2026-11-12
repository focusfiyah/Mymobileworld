"""Momo & Nashi Erasable Tracing Book, House of Rameau Black Friday version (Ralph 2026-11-12): Ralph's free Chatterbox VO (vo/),
Grace's approved real footage (her HD original, ugc/momo-nashi-tracing/orig/momo_orig.mov) in a new order and framing, one free
Pexels holiday clip on the gift line (broll/SOURCES.md), holiday hook text from frame 0. Shots start on their line (vo/words.json).
  python3 cut.py  (REVIEW_ONLY=1 for the quick render)"""
import sys
sys.path.insert(0, "../_bf_c_tools")
from build import build
G = "../../../ugc/momo-nashi-tracing/orig/momo_orig.mov"
PX = "../_bf_c_tools/pexels/"
SEGS = [  # (VO line, offset s, source, in s, crop w:h:x:y)
    (0, 0.0, G, 5.20, "1000:1778:40:0"),      # hook: the boxed set swinging from its handle
    (1, 0.0, G, 0.40, "960:1707:60:110"),     # always asking for something to do: hand on the box, 35 activities
    (2, 0.0, G, 23.00, "1000:1778:40:80"),    # "Momo and Nashi erasable tracing book": the book cover
    (3, 0.0, G, 30.00, "1000:1778:40:80"),    # lines page
    (3, 0.75, G, 34.00, "960:1707:60:100"),   # shapes page
    (3, 1.50, G, 41.00, "1000:1778:40:80"),   # big letters page
    (3, 2.30, G, 46.00, "960:1707:60:100"),   # numbers page
    (4, 0.0, G, 13.00, "1000:1778:40:80"),    # the erasable markers
    (4, 1.80, G, 17.00, "1000:1778:40:60"),   # the smiley eraser
    (5, 0.0, G, 42.50, "940:1671:70:120"),    # brag: letters pages under her hand
    (6, 0.0, PX + "8247256.mp4", 1.0, "1080:1920:0:0"),  # holiday: a dad and his little girl unwrapping a big gift (Pexels 8247256)
    (6, 1.60, G, 9.20, "1000:1778:40:60"),    # the open box: book, markers, eraser
    (7, 0.0, G, 27.00, "1000:1778:40:80"),    # close: book held up
]
build("bf_momo_nashi", SEGS, "Put this on your list|before Christmas", hook_y=362)
