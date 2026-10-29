"""Vans V13-V17 (Grace) runner, 2026-10-29 (from ugc/vans-sequin-v12/run.py). Script gate + BOOK lock + prompt check run
before every paid call (kie.run_task). Prompts and refs live in shots.json (tools/make_shots.py, prompt-master).
  python3 run.py stills V13A ...   Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png ("all" = every shot)"""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = json.loads(Path("shots.json").read_text())


def still(sid):
    s = S[sid]
    if Path(f"stills/{sid}.png").exists(): print("still", sid, "exists, skipped", flush=True); return
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    ids = list(S) if ids == ["all"] else ids
    Path("stills").mkdir(exist_ok=True)
    if kind == "stills":
        with ThreadPoolExecutor(min(20, len(ids))) as ex: list(ex.map(still, ids))


def clip(sid):
    """Omni 1.1 Flash 4 s on Kie via ugc-product-ad omni_clip.py (gate, ledger, clip check, audio stripped) -> clips/<ID>.mp4"""
    import subprocess
    s = S[sid]
    if Path(f"clips/{sid}.mp4").exists(): print("clip", sid, "exists, skipped", flush=True); return
    Path("prompts").mkdir(exist_ok=True); pf = Path(f"prompts/{sid}.txt"); pf.write_text(s["clip"])
    cmd = ["python3", "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py", ".", sid, "--prompt-file", str(pf),
           "--still", s["clip_refs"][0]] + [x for r in s["clip_refs"][1:] for x in ("--ref", r)] + ["--seconds", "4"]
    r = subprocess.run(cmd + (["--dry"] if DRY else []), capture_output=True, text=True)
    print("clip", sid, "rc", r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:] , flush=True)


DRY = "--dry" in sys.argv
if __name__ == "__main__" and sys.argv[1] == "clips":
    ids = [i for i in sys.argv[2:] if not i.startswith("--")]
    ids = list(S) if ids == ["all"] else ids
    with ThreadPoolExecutor(min(20, len(ids))) as ex: list(ex.map(clip, ids))
