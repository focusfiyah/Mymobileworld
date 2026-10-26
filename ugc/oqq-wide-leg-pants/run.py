"""OQQ pants (Grace) runner, 2026-10-25 (from ugc/vans-sequin-v12/run.py). Script gate + BOOK lock run before every paid call
(kie.run_task). Prompts and refs live in shots.json (tools/make_shots.py, prompt-master, Ralph's stack).
  python3 run.py prompt S1         print the still prompt and refs (free)
  python3 run.py stills S1 ...     Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())["shots"]}


def still(sid):
    s = S[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def seedance(sid, prompt_file, refs):
    """Seedance 2.0 Mini, reference mode (image 1 = the still), for a product clip Omni refused (Ralph 2026-10-26: OK)."""
    body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": Path(prompt_file).read_text().strip(), "reference_image_urls": [kie.upload(r) for r in refs],
            "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}
    url = kie.run_task(body, label=f"seedance {sid}")
    if url: kie.fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    if kind == "prompt":
        for i in ids: print(S[i]["still_refs"], S[i]["still"])
    elif kind == "seedance":
        seedance(ids[0], ids[1], ids[2:])
    elif kind == "stills":
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(still, ids))
