"""Nano Banana Pro stills in parallel threads (one process, so kie_log.json stays locked). Same prompts/refs as kie.stills.
  python3 par_stills.py S2 S3 S4 S5 S6 S7   (S1 first: it is the room reference)"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

def one(sid):
    s = kie.SHOTS[sid]
    refs = [kie.upload(p) for p in kie.REFS]
    base = [] if sid == "S2" else (refs[2:] if sid in kie.NO_HAND else refs)
    room = [kie.upload(kie.ROOM)] if Path(kie.ROOM).exists() and sid not in kie.NO_HAND else []  # S1 shows a hand and the jar
    prompt = (f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {s['still']} "
              f"{kie.blocks(sid)} {kie.J['scene_block']}"
              + (" The last reference image shows the same kitchen, light and counter: match them." if room else ""))
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": base + room,
                                                             "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)
    else:
        print("still", sid, "FAILED", flush=True)

ids = sys.argv[1:]
[kie.upload(p) for p in kie.REFS + [kie.ROOM]]
with ThreadPoolExecutor(len(ids)) as ex:
    list(ex.map(one, ids))
kie.sheet("stills", ".png")
