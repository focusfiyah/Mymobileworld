"""Power bank flashlight runner (Grace, 2026-10-21). Script gate runs before every paid call (kie.run_task).
  python3 run.py stills S4          Gemini 3 Pro Image stills on Kie ($0.09 each) -> stills/<ID>.png
  python3 run.py clips S4 ...      Seedance 2.0 Mini in reference mode ($0.041/s) -> clips/<ID>.mp4 (Kling shots go through the Kling MCP)
Stills use the APPROVED test still (stills/look_ref.png) as an extra look reference once it exists (PLAYBOOK §6: one test still first)."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

J = json.loads(Path("shots.json").read_text())
S = {s["id"]: s for s in J["shots"]}
FRONT, SHEET = J["refs"]["product"]
HAND = J["refs"]["hand"][0]
LOOK = "stills/look_ref.png"


def text(s):
    parts = [s["still"], J["hand_block"] if s["hand"] else J["no_hand_block"]]
    if s["product"]: parts.append(J["product_block"])
    parts.append(J["look_block"])
    return " ".join(parts)


def still(sid):
    s = S[sid]; refs, names = [], []
    if s["hand"]: refs.append(kie.upload(HAND)); names.append("Grace's hand reference sheet (skin, nails, rings, bracelets)")
    if s["product"]:
        refs += [kie.upload(FRONT), kie.upload(SHEET)]
        names += ["the flashlight's front view (main reference)", "the flashlight reference sheet (every side)"]
    if Path(LOOK).exists():
        refs.append(kie.upload(LOOK)); names.append("an approved frame from this same video (match its hand, rings and light)")
    note = " Reference images, in order: " + "; ".join(names) + "." if names else ""
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + text(s) + note
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def clip(sid):
    """Seedance reference mode (LGXNDS v5 method, Ralph 2026-10-19): image 1 = the clean still, 2 = product front, 3 = sheet."""
    s = S[sid]
    refs = [kie.upload(f"stills/{sid}.png")] + ([kie.upload(FRONT), kie.upload(SHEET)] if s["product"] else [])
    prompt = ("Recreate reference image 1 exactly (same place, framing, light" + (", hand, rings, bracelets" if s["hand"] else "") + ") as the first frame, then: "
              + s["video"] + " " + J["video_suffix"]
              + (" The flashlight must match reference image 2 exactly (orange button, white light window, carabiner hook, gunmetal colour); "
                 "reference image 3 shows it from every side." if s["product"] else ""))
    body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "reference_image_urls": refs, "generate_audio": False,
            "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}}
    url = kie.run_task(body)
    if url:
        kie.fetch(url, f"clips/{sid}{'_seedance' if s['model'] == 'kling' else ''}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    for d in ("stills", "clips"): Path(d).mkdir(exist_ok=True)
    with ThreadPoolExecutor(max(1, len(ids))) as ex:
        list(ex.map(still if kind == "stills" else clip, ids))
