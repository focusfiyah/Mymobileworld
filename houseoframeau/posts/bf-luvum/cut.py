"""LUVUM Collagen Gel Mask, House of Rameau Black Friday version (Ralph 2026-11-12): Ralph's free Chatterbox VO (vo/), Grace's
approved real footage (her HD original, ugc/luvum-gel-mask/orig/luvum_orig.mov, 21.25 s) in a new order and framing, two free
Pexels holiday clips on the gift lines (broll/SOURCES.md; her footage alone is shorter than the voice), hook text from frame 0.
Grace's blurs (0-0.4 s, 7.9-9.4 s) are left out. Shots start on their line (vo/words.json).
  python3 cut.py  (REVIEW_ONLY=1 for the quick render)"""
import sys
sys.path.insert(0, "../_bf_c_tools")
from build import build
G = "../../../ugc/luvum-gel-mask/orig/luvum_orig.mov"
PX = "../_bf_c_tools/pexels/"
SEGS = [  # (VO line, offset s, source, in s, crop w:h:x:y)
    (0, 0.0, G, 9.40, "960:1707:60:0"),       # hook: the pouches laid out, camera moves along (wall above = room for the hook)
    (1, 0.0, G, 0.60, "1000:1778:40:40"),     # tired by the end of the week: the Luvum box in her hand
    (2, 0.35, G, 4.90, "1000:1778:40:60"),    # "Luvum collagen gel masks": the pouches fanned in her hand (ends before the 7.9 s blur)
    (3, 0.0, G, 13.95, "920:1636:80:140"),    # ingredients: pouch close, text on the front
    (3, 2.60, G, 16.55, "1000:1778:40:60"),   # one pouch held up
    (4, 0.0, PX + "5974521.mp4", 3.0, "1080:1920:0:0"),  # holiday: a woman wrapping a gift with a blue ribbon (Pexels 5974521)
    (4, 2.13, G, 12.40, "960:1707:60:100"),   # pouch close-up
    (5, 0.0, PX + "10602683.mp4", 1.0, "1080:1920:0:0"),  # holiday: a woman holding a wrapped gift by the tree (Pexels 10602683)
    (6, 0.0, G, 19.72, "1000:1778:40:60"),    # close: pouch held up
]
build("bf_luvum", SEGS, "I already know exactly|who would love this", hook_y=362, tail=0.25)
