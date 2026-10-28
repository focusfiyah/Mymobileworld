"""Seedance 2.0 Mini first-frame clip prompts (Ralph 2026-10-27: Omni on Kie gave 500s, "Seedance from the stills now"; size fix: real 9.5 x 5.5 cm,
one item inside at a time). prompt-master, Ralph's stack. python3 seedance_prompts.py S1 S2 ... -> prompts/<ID>_seedance.txt"""
import json, sys
from pathlib import Path
S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())["shots"]}
PROD = ("The burgundy mini bag charm stays exactly as in the first frame for the whole clip: the same open-top bucket shape and the same TINY size "
        "(9.5 cm tall with its handles, 5.5 cm wide, never growing), matte pebbled burgundy leather, two rolled handles with darker edges, the gold rectangular buckle "
        "and the gold padlock with three engraved lines and no letters, four small gold feet, the small plain gold ring on a short gold chain with nothing hanging from it "
        "(no key, no charm, no emblem), and the pink, light blue and white twilly scarf on its handle. It never changes shape, size or colour, never turns, flips or swings, "
        "and no text, letters or logos appear on it.")
EXTRA = {"S1": " The hand keeps the same pinch on both handles the whole clip and never lets go; no second hand appears.",
         "S5a": " Only the one earbuds case goes in; nothing else appears inside the charm.",
         "S5b": " Only the one lip gloss goes in; nothing else appears inside the charm.",
         "S8": " No ring, chain or key appears; nothing else goes into the stocking."}
for sid in sys.argv[1:]:
    s = S[sid]
    hand = (" Only one hand: its French-tip nails, rings and bracelets stay exactly as in the first frame, the flat gold link bracelet never becomes a watch, "
            "the hand keeps one grip and enters and leaves from the frame edge.") if s["hand"] else " No hand, fingers or people appear at any time."
    prod = PROD.replace(", the small plain gold ring on a short gold chain with nothing hanging from it (no key, no charm, no emblem)", "") if sid == "S8" else PROD
    p = f"Animate this image as the first frame. {s['motion']} {prod}{EXTRA.get(sid, '')}{hand} Bright neutral daylight that never changes. No music, no voice, no captions, no on-screen text."
    Path(f"prompts/{sid}_seedance.txt").write_text(p + "\n"); print(sid, len(p))
