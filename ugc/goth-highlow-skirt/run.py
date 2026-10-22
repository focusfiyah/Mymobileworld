"""Goth High-Low Skirt (Grace) runner, 2026-10-22. Script gate runs before every paid call (kie.run_task / omni_clip.py).
  python3 run.py prompt S2          print the still prompt (free)
  python3 run.py stills S2 [S1 ..]   Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png, in parallel
  python3 run.py omni S2 [--dry]     Google Omni 1.1 Flash on Kie, 4 s $0.315 (product lock; the skirt is in every shot)
Prompts written with prompt-master (Ralph's stack): numbered real references named in the prompt, colour matched, one motion, no text."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

SHEET, TIE, RUCH, HAND, LOOK = "refs/product_sheet.png", "refs/closeup_tie.png", "refs/closeup_ruching.png", "../../grace/ref/hand-sheets/with_bracelet.jpg", "stills/S2.png"
HANDS = {"S2"}
ROOM = "refs/room.jpg"
OMNI = "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py"


def still_prompt(sid):
    look = Path("prompts/look.txt").read_text().strip()
    p = Path(f"prompts/{sid}_still.txt").read_text().replace("<<LOOK>>", look)
    refs = [SHEET, TIE, RUCH] + ([HAND] if sid in HANDS else [LOOK]) + [ROOM]
    return refs, "Vertical 9:16 photo, a single frame from a phone-shot mirror video. " + p


def still(sid):
    refs, prompt = still_prompt(sid)
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(r) for r in refs],
                        "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def omni(sid, dry=False):
    refs = [TIE, RUCH, SHEET] + ([HAND] if sid in HANDS else [])  # S4 starts from the S3 still (free route, Ralph 2026-10-22)
    cmd = ["python3", OMNI, ".", sid, "--prompt-file", f"prompts/{sid}_clip.txt", "--still", f"stills/{sid}.png", "--seconds", "4"]
    for r in refs: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


if __name__ == "__main__":
    cmd, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    if cmd == "prompt":
        for i in ids: r, p = still_prompt(i); print(r); print(p)
    elif cmd == "stills":
        Path("stills").mkdir(exist_ok=True)
        with ThreadPoolExecutor(4) as ex: list(ex.map(still, ids))
    elif cmd == "omni":
        with ThreadPoolExecutor(4) as ex: list(ex.map(lambda i: omni(i, "--dry" in sys.argv), ids))
