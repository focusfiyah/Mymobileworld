"""Nano Banana Pro stills in parallel threads (one process, so kie_log.json stays locked). Same prompts/refs as kie.stills.
  python3 par_stills.py S2 S3 S6 S7   then   python3 par_stills.py S4 S5   (S4/S5 use the S3 still as the tablet ref)
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

def one(sid):
    s = kie.SHOTS[sid]
    refs = [kie.upload(p) for p in kie.REFS]
    base = refs[:2] if sid in kie.NO_BOX else refs
    extra = kie.TABLET_REF if sid in kie.NO_BOX else kie.ROOM
    room = [kie.upload(extra)] if Path(extra).exists() else []
    prompt = (f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {s['still']} "
              f"{kie.blocks(sid)} {kie.J['scene_block']}"
              + (" The last reference image shows the same bathroom, light and tablet: match them." if room else ""))
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": base + room,
                                                             "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)
    else:
        print("still", sid, "FAILED", flush=True)

ids = sys.argv[1:]
assert not (set(ids) & kie.NO_BOX) or Path(kie.TABLET_REF).exists(), "render S3 before S4/S5"
[kie.upload(p) for p in kie.REFS + [kie.ROOM] + ([kie.TABLET_REF] if Path(kie.TABLET_REF).exists() else [])]
with ThreadPoolExecutor(len(ids)) as ex:
    list(ex.map(one, ids))
kie.sheet("stills", ".png")
