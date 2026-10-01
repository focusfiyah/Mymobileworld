"""Run several Nano Banana Pro stills in parallel threads (one process, so kie_log.json stays locked).
  python3 par_stills.py S2 S3 ...   -> stills/<ID>.png + preview/stills_sheet.png
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

def one(sid):
    s = kie.SHOTS[sid]
    refs = [kie.upload(p) for p in kie.REFS] + [kie.upload(kie.ROOM)]
    prompt = (f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {s['still']} "
              f"{kie.J['identity_block']} {kie.J['scene_block']}"
              " The last reference image shows the same nightstand, room and light: match it.")
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs,
                                                             "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)

ids = sys.argv[1:]
[kie.upload(p) for p in kie.REFS + [kie.ROOM]]   # warm the upload cache before threads start
with ThreadPoolExecutor(len(ids)) as ex:
    list(ex.map(one, ids))
kie.sheet("stills", ".png")
