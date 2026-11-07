"""V3 runner (2026-11-07, from run.py). Script gate + BOOK lock run before every paid call (kie.run_task / wan_clip.py).
Prompts and refs: shots_v3.json (make_shots_v3.py, prompt-master, MARKED_OK).
  python3 run_v3.py stills S1 ...      nano-banana-pro 2K on Kie ($0.09) -> stills/v3_<ID>.png
  python3 run_v3.py seedance S3        Seedance 2.0 Mini first-frame (no product, 4 s, $0.164) -> clips/v3_<ID>.mp4
  python3 run_v3.py wan S2 ... [--dry] Wan 3.0 720P reference mode (5 s, $0.40) + free upscale -> clips/v3_<ID>.mp4"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots_v3.json").read_text())["shots"]}
WAN = str(Path(__file__).resolve().parents[2] / ".claude/skills/ugc-product-ad/scripts/wan_clip.py")


def still(sid):
    s = S[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["still"], "image_input": [kie.upload(p) for p in s["still_refs"]],
                        "aspect_ratio": "9:16", "resolution": "2K"}}, label=f"v3 still {sid}")
    if url: kie.fetch(url, f"stills/v3_{sid}.png"); print("still", sid, "ok", flush=True)


def seedance(sid):
    s = S[sid]
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": s["clip"], "first_frame_url": kie.upload(f"stills/v3_{sid}.png"),
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}}, label=f"v3 {sid} seedance first-frame")
    if url: kie.fetch(url, f"clips/v3_{sid}.mp4", still=f"stills/v3_{sid}.png"); print("clip", sid, "ok", flush=True)


def wan(sid, dry=False):
    s = S[sid]; Path("prompts").mkdir(exist_ok=True); Path(f"prompts/v3_{sid}.txt").write_text(s["clip"])
    cmd = ["python3", WAN, ".", f"v3_{sid}", "--prompt-file", f"prompts/v3_{sid}.txt", "--still", s["clip_refs"][0], "--seconds", str(s["secs"])]
    for r in s["clip_refs"][1:]: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


if __name__ == "__main__":
    kind, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    fn = {"stills": still, "seedance": seedance, "wan": lambda i: wan(i, "--dry" in sys.argv)}[kind]
    with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(fn, ids))
