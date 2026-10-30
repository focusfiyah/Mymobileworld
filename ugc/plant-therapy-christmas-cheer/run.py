"""Plant Therapy Christmas Cheer (Grace) runner, 2026-10-30 (from ugc/oqq-wide-leg-pants/run.py). Script gate + BOOK lock run
before every paid call (kie.run_task / omni_clip.py). Prompts and refs: shots.json (make_shots.py, prompt-master).
  python3 run.py stills S1 ...     Gemini 3 Pro Image on Kie (nano-banana-pro 2K, $0.09) -> stills/<ID>.png
  python3 run.py seedance S2 ...   Seedance 2.0 Mini first-frame from the still (no product, 4 s, $0.164) -> clips/<ID>.mp4
  python3 run.py omni S4 ... [--dry]   Omni 1.1 Flash on Kie, reference mode (4 s, $0.315) -> clips/<ID>.mp4"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())["shots"]}
OMNI = str(Path(__file__).resolve().parents[2] / ".claude/skills/ugc-product-ad/scripts/omni_clip.py")


def still(sid):
    s = S[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "2K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def seedance(sid):
    s = S[sid]
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": s["clip"], "first_frame_url": kie.upload(f"stills/{sid}.png"),
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}, label=f"{sid} seedance first-frame")
    if url: kie.fetch(url, f"clips/{sid}.mp4", still=f"stills/{sid}.png"); print("clip", sid, "ok", flush=True)


def omni(sid, dry=False):
    s = S[sid]; Path(f"prompts/{sid}.txt").write_text(s["clip"])
    cmd = ["python3", OMNI, ".", sid, "--prompt-file", f"prompts/{sid}.txt", "--still", s["clip_refs"][0], "--seconds", "4"]
    for r in s["clip_refs"][1:]: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


if __name__ == "__main__":
    kind, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    fn = {"stills": still, "seedance": seedance, "omni": lambda i: omni(i, "--dry" in sys.argv)}[kind]
    with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(fn, ids))
