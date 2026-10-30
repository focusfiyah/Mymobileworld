"""Magnesium Night Trio (Grace) runner, 2026-10-30 (from ugc/oqq-wide-leg-pants/run.py). Script gate + BOOK lock run before every
paid call (kie.run_task). Prompts and refs live in shots.json (make_shots.py, prompt-master, Ralph's stack).
  python3 run.py stills S1 ...     Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())}


def still(sid):
    s = S[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def seedance(sid):
    """Seedance 2.0 Mini, reference mode (image 1 = the still), for the no-jar clips ($0.164 each, 4 s)."""
    s = S[sid]
    body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": Path(f"prompts/{sid}_clip.txt").read_text().strip(),
            "reference_image_urls": [kie.upload(r) for r in s["clip_refs"]],
            "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}
    url = kie.run_task(body, label=f"seedance {sid}")
    if url: kie.fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    if kind == "seedance":
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(seedance, ids))
    if kind == "stills":
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(still, ids))
