"""Dr. Nice's Boo-Boo Gel (Grace) runner, 2026-11-03 (copied from buttah-silky-towels). The script gate, the Production Book lock
and the prompt check run before every paid call (kie.run_task -> grace/gate.py). Prompts come from build_prompts.py.
  python3 run.py stills S1 S2 ...   Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png
  python3 run.py wan S1 ...         Wan 3.0 720P 5 s on Kie via wan_clip.py ($0.40, free upscale) (Ralph: all on Kie)
  python3 run.py seedance-first S2  Seedance 2.0 Mini 4 s from the approved still ($0.164)"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

R = json.loads(Path("prompts/refs.json").read_text())
WAN = "../../.claude/skills/ugc-product-ad/scripts/wan_clip.py"


def still(sid):
    prompt = Path(f"prompts/still_{sid}.txt").read_text().strip()
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in R[sid]["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def wan(sid, dry=False):
    refs = R[sid]["clip_refs"]
    cmd = ["python3", WAN, ".", sid, "--prompt-file", f"prompts/{sid}.txt", "--still", refs[0], "--seconds", "5"]
    for r in refs[1:]: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


def seedance_first(sid):
    prompt = Path(f"prompts/{sid}_seedance.txt").read_text().strip()
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": kie.upload(f"stills/{sid}.png"), "generate_audio": False,
                        "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}, label=f"{sid} seedance first-frame")
    if url: kie.fetch(url, f"clips/{sid}_seedance.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    Path("stills").mkdir(exist_ok=True); Path("clips").mkdir(exist_ok=True)
    fn = {"stills": still, "wan": wan, "wan-dry": lambda i: wan(i, True), "seedance-first": seedance_first}[kind]
    with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(fn, ids))
