"""Kie runner for the Shnuggle slideshow (Grace, 2026-10-19). Gate-protected; reuses ../shnuggle-response/kie.py plumbing.

  python3 kie.py stills [S1 ...]   Nano Banana Pro (Gemini 3 Pro Image) stills, 2K -> stills_raw/<ID>.png
Refs on every still: refs/tub_front_real.png (real photo), refs/shnuggle_tub_6view.jpg (real 6 views). (Grippy texture photo dropped: Ralph 2026-10-19, the dots do not exist on his product.)
"""
import json, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "shnuggle-response"))
os.chdir(HERE)
import kie as base  # noqa: E402  (run_task gates on the CURRENT working dir's job via _gate -> patched below)

def _gate():
    sys.path.insert(0, str(HERE.parents[1] / "grace")); from gate import require; require(HERE)
base._gate = _gate
base.LOG = HERE / "kie_log.json"; base.CACHE = HERE / "upload_cache.json"
J = json.loads((HERE / "slides.json").read_text()); SL = {s["id"]: s for s in J["slides"]}
REFS = ["refs/tub_front_real.png", "refs/shnuggle_tub_6view.jpg"]

def one(sid):
    s = SL[sid]; refs = [base.upload(p) for p in REFS]
    prompt = f"{s['still']} {J['product_block']} {J['nothing_added']} {J['look']}"
    url = base.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "2K"}})
    if url: base.fetch(url, f"stills_raw/{sid}.png"); print("still", sid, "ok", flush=True)
    else: print("still", sid, "FAILED", flush=True)

if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    ids = sys.argv[2:] or list(SL)
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(one, ids))
