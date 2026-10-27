"""Mini Bag Charm (Grace) runner, 2026-10-26 (copied from ugc/youtheory-b12b6). The script gate, the Production Book lock and the prompt check run
before every paid call (kie.run_task -> grace/gate.py). Prompts come from build_prompts.py (prompts/*.txt, refs.json).
  python3 run.py stills S1 S2 ...   Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png
  python3 run.py omni S6 ...        Google Omni 1.1 Flash on Kie via omni_clip.py (only if Ralph's Flow take fails, asked)"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

R = json.loads(Path("prompts/refs.json").read_text())
OMNI = "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py"


def still(sid):
    prompt = Path(f"prompts/still_{sid}.txt").read_text().strip()
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in R[sid]["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def omni(sid, dry=False):
    refs = R[sid]["clip_refs"]
    cmd = ["python3", OMNI, ".", sid, "--prompt-file", f"prompts/{sid}.txt", "--still", refs[0], "--seconds", str(OMNI_S.get(sid, 4))]
    for r in refs[1:]: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


OMNI_S = {"S9": 6}
DUR = {"S9": 6}   # their lines run 4.7 s and 5.2 s


def seedance_prod(sid):
    """Product clips on Seedance 2.0 Mini first-frame (Ralph 2026-10-27, Omni on Kie gave 500s: "Seedance from the stills now")."""
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": Path(f"prompts/{sid}_seedance.txt").read_text().strip(), "first_frame_url": kie.upload(f"stills/{sid}.png"),
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": DUR.get(sid, 4)}}, label=f"{sid} seedance first-frame")
    if url: kie.fetch(url, f"clips/{sid}_seedance.mp4", still=f"stills/{sid}.png"); print("clip", sid, "ok", flush=True)


def seedance_first(sid):
    """No product in frame (S3): Seedance 2.0 Mini, first frame = the approved still (BOOK.md, $0.164)."""
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": Path(f"prompts/{sid}.txt").read_text().strip(), "first_frame_url": kie.upload(f"stills/{sid}.png"),
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}, label=f"{sid} seedance first-frame")
    if url: kie.fetch(url, f"clips/{sid}_seedance.mp4", still=f"stills/{sid}.png"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    Path("stills").mkdir(exist_ok=True); Path("clips").mkdir(exist_ok=True)
    fn = {"stills": still, "omni": omni, "omni-dry": lambda i: omni(i, True), "seedance-first": seedance_first, "seedance": seedance_prod}[kind]
    with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(fn, ids))
