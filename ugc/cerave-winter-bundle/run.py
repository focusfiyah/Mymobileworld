"""CeraVe Winter Skin Bundle (Grace) runner, 2026-11-02 (from ugc/magnesium-night-trio/run.py). Script gate + BOOK lock
run before every paid call. Prompts and refs live in shots.json (make_shots.py, prompt-master, Ralph's stack).
  python3 run.py stills S1 ...   Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png
  python3 run.py clips S1 ...    Omni 1.1 Flash on Kie via omni_clip.py ($0.315 per 4 s) -> clips/<ID>.mp4"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())}
OMNI = "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py"


def still(sid):
    s = S[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: Path("stills").mkdir(exist_ok=True); kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def clip(sid, dry=False):
    s = S[sid]; refs = s["clip_refs"]
    cmd = [sys.executable, OMNI, ".", sid, "--prompt-file", f"prompts/{sid}_clip.txt", "--still", refs[0], "--seconds", "4", "--res", "1080p"]
    for r in refs[1:]: cmd += ["--ref", r]
    if dry: cmd.append("--dry")
    subprocess.run(cmd, check=False)


if __name__ == "__main__":
    kind, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    f = still if kind == "stills" else (lambda i: clip(i, "--dry" in sys.argv))
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(f, ids))
