"""Nano Banana Pro stills in parallel threads (one process, kie_log.json stays locked). Same prompts/refs as kie.stills.
  python3 par_stills.py S2a S2b S3 ...
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

def one(sid):
    s = kie.SHOTS[sid]
    refs = [kie.upload(p) for p in kie.HAND] + ([kie.upload(kie.PROD)] if (s["box"] or s["mask"] or s["wrap"]) else [])
    room = [kie.upload("stills/S1.png")]
    prompt = (f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {s['still']} {kie.blocks(sid)} {kie.J['scene_block']}"
              " The last reference image shows the same garage, light and bench: match them.")
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs + room,
                                                             "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)
    else:
        print("still", sid, "FAILED", flush=True)

ids = sys.argv[1:]
[kie.upload(p) for p in kie.HAND + [kie.PROD, "stills/S1.png"]]
with ThreadPoolExecutor(len(ids)) as ex:
    list(ex.map(one, ids))
kie.sheet("stills", ".png")
