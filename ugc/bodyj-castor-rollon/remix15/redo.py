"""Redo r3 (2026-10-21, REDO_PLAN.md): 4 new shots for lines whose picture didn't match the words.
  python3 redo.py stills [R1 ...]    nano-banana-pro (Gemini 3 Pro Image) on Kie, $0.09 each -> redo/stills/R*.png
  python3 redo.py clip R3            Seedance 2.0 Mini, 5 s, $0.205 (hand shot); R1 R2 R4 go to Kling (MCP)"""
import sys
from pathlib import Path
H = Path(__file__).resolve().parent; P = H.parent
sys.path.insert(0, str(P)); sys.path.insert(0, str(H.parents[2] / "grace"))
import os; os.chdir(P)          # kie.py logs + upload cache live in the parent job
import kie
from gate import require
kie._gate = lambda: require(H)  # this job's own script gate (remix15/checklist.json)
SHEET, FRONT = "refs/ralph_sheet_bottle.jpg", "refs/bottle_front.png"
BATH, BED = "stills/S8.png", "stills/S9.png"
PROD = ("The BodyJ4You castor oil roll-on: a short squat amber-brown glass bottle, white plastic collar, a pink rose quartz "
        "roller ball on top, white label with a plum band, plum serif 'CASTOR OIL', green USDA ORGANIC seal. It must match the "
        "product reference sheet exactly (the big front view is the real label); keep it upright and the label facing camera.")
LOOK = "Bright, clean, neutral daylight, true colours, no yellow or golden tint, no dark or moody look. No text, no logos other than the product label."
S = {
 "R1": {"refs": [SHEET, FRONT, BATH], "p": f"Close shot of the castor oil roll-on standing on the white marble counter of the sage-green tiled bathroom from the last reference image, soft morning sun from the window. One fat clear golden drop of castor oil sits on top of the rose quartz roller ball and catches the light like liquid gold. No hands. {PROD}"},
 "R2": {"refs": [SHEET, FRONT, BED], "p": f"A small round mirrored vanity tray on the wooden nightstand of the bedroom from the last reference image. On the tray, left: a pretty faceted glass perfume bottle with pale pink perfume and a round glass cap, no brand, no writing. Right, a little apart: the castor oil roll-on. No hands. {PROD}"},
 "R3": {"refs": ["stills/S5.png"], "p": "Seen from above and behind, no face. EXACTLY TWO HANDS in the whole frame, both hers: an older Black grandmother's hands (brown skin with fine wrinkles, short natural unpainted nails, a thin gold wedding band) part her short grey coily hair and work plain golden castor oil into the scalp at the part with her fingertips. In her other hand, an old unbranded clear glass bottle of golden oil with no label. Lavender cardigan sleeve at the wrist. Soft bright bedroom light, same framing and light as the reference image, but grey hair and older hands. Her right hand works the oil in at the part; her left hand holds the bottle low in the frame. No third hand, no hand on top of the head. Whole wrists, both coming from the bottom edge of the frame."},
 "R4": {"refs": [SHEET, FRONT, BATH], "p": f"A white bathroom shelf in the sage-green tiled bathroom from the last reference image. Left: a big old messy unbranded plastic bottle of castor oil, thick golden oil dripped down its side and a sticky oily ring under it on the shelf, no label text. Right, a little apart: the clean castor oil roll-on. No hands. {PROD}"},
}
def still(sid):
    s = S[sid]
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + s["p"] + " " + LOOK
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(r) for r in s["refs"]], "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, str(H / f"redo/stills/{sid}.png")); print("still", sid, "ok", flush=True)
if __name__ == "__main__":
    if sys.argv[1] == "stills":
        for sid in sys.argv[2:] or list(S): still(sid)
