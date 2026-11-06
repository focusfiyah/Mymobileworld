"""Migrastil Neuropathy Cream (Grace) runner, 2026-11-06 (from ugc/oceanview-hair-oil/run.py). Script gate + BOOK lock run before
every paid call (kie.run_task). Prompts + refs (in image order) in shots.json (prompt-master, linted + marked).
  python3 run.py stills S1 ...     nano-banana-pro on Kie ($0.09 each) -> stills/<ID>.png
  python3 run.py seedance S2 ...   Seedance 2.0 Mini 4 s from the still ($0.164 each) -> clips/<ID>.mp4"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = json.loads(Path("shots.json").read_text())
fix = lambda p: "../../" + p if p.startswith("grace/") else p


def still(sid):
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": S[sid]["still"], "image_input": [kie.upload(fix(p)) for p in S[sid]["refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def seedance(sid):
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": S[sid]["clip"], "first_frame_url": kie.upload(f"stills/{sid}.png"),
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}, label=f"seedance {sid}")
    if url: kie.fetch(url, f"clips/{sid}.mp4", still=f"stills/{sid}.png"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    fn = {"stills": still, "seedance": seedance}[kind]
    with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(fn, ids))
