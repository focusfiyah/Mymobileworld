"""52 Modern Manners for Kids, House of Rameau Black Friday version (Ralph 2026-11-12): Ralph's free Chatterbox VO (vo/), Grace's
approved real footage (her HD original, ugc/52-modern-manners-book/orig/manners.mov) in a new order and framing, one free Pexels
gift clip on the gift line (broll/SOURCES.md), holiday hook text from frame 0 over the wall above the standing book (the cover
shots fill the top of the frame, so the card would sit on the title). Shots start on their line (vo/words.json).
  python3 cut.py  (REVIEW_ONLY=1 for the quick render)"""
import sys
sys.path.insert(0, "../_bf_c_tools")
from build import build
G = "../../../ugc/52-modern-manners-book/orig/manners.mov"
PX = "../_bf_c_tools/pexels/"
SEGS = [  # (VO line, offset s, source, in s, crop w:h:x:y)
    (0, 0.0, G, 48.00, "1000:1778:40:0"),     # hook: the book standing on the counter, then picked up ("Make room" page; title stays under the card)
    (1, 0.0, G, 14.50, "960:1707:60:100"),    # kids get loud: the book opened wide in her hands
    (2, 0.0, G, 2.20, "1000:1778:40:60"),     # "52 Modern Manners for Kids": the cover, tilted close
    (2, 2.30, G, 55.50, "940:1671:70:120"),   # the cover held up
    (3, 0.0, G, 24.60, "1000:1778:40:80"),    # "control your volume" page
    (4, 0.0, G, 37.00, "960:1707:60:100"),    # "respect privacy" page
    (5, 0.0, G, 29.50, "1000:1778:40:80"),    # brag: "treat homes with respect" page
    (6, 0.0, PX + "5704517.mp4", 1.0, "1080:1920:0:0"),  # holiday: someone carrying a tall stack of gift boxes (Pexels 5704517)
    (6, 1.50, G, 45.00, "1000:1778:40:60"),   # the book standing on the counter
    (7, 0.0, G, 22.20, "1000:1778:40:60"),    # close: the cover held flat (ends before the 24.2 s page flip)
]
build("bf_manners", SEGS, "This is going to matter once|the family comes over|for Christmas", hook_y=362)
