"""Vans sequin V12 (Grace) runner, 2026-10-24 (from ugc/jiyu-polish-pads/run.py). Script gate + BOOK lock run before every
paid call (kie.run_task). Prompts and refs live in shots.json (prompt-master, Ralph's stack).
  python3 run.py prompt S1         print the still prompt and refs (free)
  python3 run.py stills S1 ...     Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = json.loads(Path("shots.json").read_text())


def still(sid):
    s = S[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    if kind == "prompt":
        for i in ids: print(S[i]["still_refs"], S[i]["still"])
    elif kind == "stills":
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(still, ids))


def still_r2(sid):
    """Round 2 (2026-10-24): prompts/stills_r2.json; mode edit = image 1 is the round-1 still, ONE item changes. -> stills/<ID>_r2.png"""
    p = json.loads(Path(f"prompts/stills_{RND}.json").read_text())[sid]
    refs = ([p["base"]] if p["mode"] == "edit" else []) + p["refs"]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": p["prompt"], "image_input": [kie.upload(r) for r in refs],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {RND} {sid}")
    if url: kie.fetch(url, f"stills/{sid}_{RND}.png"); print("still", RND, sid, "ok", flush=True)


RND = {"stills3": "r3"}.get(sys.argv[1] if len(sys.argv) > 1 else "", "r2")
if __name__ == "__main__" and sys.argv[1] in ("stills2", "stills3"):
    with ThreadPoolExecutor(max(1, len(sys.argv[2:]))) as ex: list(ex.map(still_r2, sys.argv[2:]))
