"""Ocean View hair oil (Grace) runner, 2026-11-02 (from ugc/oqq-wide-leg-pants/run.py). Script gate + BOOK lock run before
every paid call (kie.run_task). Prompts in shots.json (prompt-master, linted + marked).
  python3 run.py stills S1 ...     nano-banana-pro on Kie ($0.09 each) -> stills/<ID>.png"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = json.loads(Path("shots.json").read_text())
P = ["refs/product_sheet.png", "refs/real/label_closeup.png", "refs/real/cap_closeup.png"]
HANDS = "refs/grace_hands.jpg"   # Grace hand sheet, without bracelet (Ralph 2026-11-02)
ROOM = {"S1": "px_7986061.jpg", "S2": "px_33375679.jpg", "S3": "px_6394549.jpg", "S4": "px_7986061.jpg",
        "S5": "px_7986061.jpg", "S6": "pb_8896510.jpg", "S7": "px_30387008.jpg"}


def refs(sid):
    room = "rooms/cand/" + ROOM[sid]
    n = S[sid]["still_refs"]
    return {1: [room], 2: [room, HANDS], 4: P + [room], 5: P + [room, HANDS], 6: P + [room, HANDS, "stills/S3.png"]}[n]


def still(sid):
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": S[sid]["still"], "image_input": [kie.upload(p) for p in refs(sid)],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    if kind == "stills":
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(still, ids))
