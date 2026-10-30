"""PRITECH V2-V4 (Grace) runner, 2026-10-27. Script gate + BOOK lock + prompt check + paid-task ledger run before every paid call
(kie.run_task -> grace/gate.py start_task). Prompts and refs come verbatim from shots.json (make_shots.py, prompt-master).
  python3 run.py stills S1 ...    Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09) -> stills/<ID>.png
  python3 run.py omni S5 ...      Omni 1.1 Flash on Kie, 4 s ($0.315) via ugc-product-ad omni_clip.py -> clips/<ID>.mp4
  python3 run.py seedance S1 ...  Seedance 2.0 Mini, reference mode, 4 s ($0.164) -> clips/<ID>.mp4 (no product in frame)
  python3 run.py omni-dry S5      print the Omni request and cost, spend nothing"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())["shots"]}
OMNI = "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py"


def still(sid):
    s = S[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def omni(sid, dry=False):
    s = S[sid]; assert s["product"], sid
    Path("prompts").mkdir(exist_ok=True); pf = Path(f"prompts/{sid}.txt"); pf.write_text(s["clip"])
    cmd = ["python3", OMNI, ".", sid, "--prompt-file", str(pf), "--still", s["clip_refs"][0], "--seconds", "4"]
    for r in s["clip_refs"][1:]: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


def seedance(sid):
    s = S[sid]; assert not s["product"], sid
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": s["clip"], "reference_image_urls": [kie.upload(p) for p in s["clip_refs"]],
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}, label=f"clip {sid}")
    if url: kie.fetch(url, f"clips/{sid}.mp4", still=f"stills/{sid}.png"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    Path("stills").mkdir(exist_ok=True); Path("clips").mkdir(exist_ok=True)
    fn = {"stills": still, "omni": omni, "omni-dry": lambda i: omni(i, True), "seedance": seedance}[kind]
    with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(fn, ids))
