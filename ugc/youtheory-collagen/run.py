"""Youtheory Collagen Liquid (Grace) runner, 2026-10-22. Script gate runs before every paid call (kie.run_task).
  python3 run.py stills S5b ...    Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png
  python3 run.py omni S5b ...      Google Omni 1.1 Flash on Kie via omni_clip.py (product lock)
  python3 run.py seedance S1       Seedance 2.0 Mini reference mode ($0.041/s), no product in frame
  python3 run.py prompt S5b        print the still prompt (free)
Prompts follow prompt-master (Ralph's stack): size first, numbered references named in the prompt, the print matched
letter for letter, one motion, no text. stills/look_ref.png (the approved test still) is passed on every later hand still."""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

D = json.loads(Path("shots.json").read_text()); B = D["blocks"]
S = {s["id"]: s for s in D["videos"][0]["shots"]}
SHEET, LOGO, WORD, TAB = "refs/product_sheet.png", "refs/closeup_C.png", "refs/closeup_D.png", "refs/closeup_E.png"
BOXREF, HANDREF, LOOK = "refs/real/ralph_pouches_in_box.jpg", "../../grace/ref/hand-sheets/with_bracelet.jpg", "stills/look_ref.png"


def still_refs(s):
    r, names = [], []
    def add(p, what): r.append(p); names.append(f"image {len(r)} = {what}")
    if s["product"]:
        add(SHEET, "the product reference sheet built from real photos (A = the real pouch front)")
        add(LOGO, "a close-up of the real 'youtheory' logo and dot circle")
        add(WORD, "a close-up of the real 'collagen liquid' wordmark and claim lines")
        add(TAB, "a close-up of the real orange tear tab")
        if s["id"] == "S3": add(BOXREF, "the real pouches standing in the open carton")
    if s["hand"]: add(HANDREF, "Grace's hand reference sheet (skin, French-tip nails, rings, bracelets)")
    if s["hand"] and Path(LOOK).exists() and s["id"] != "S5b":
        add(LOOK, "an approved frame from this same video: match its hand, rings, bracelets, light and colours")
    return r, ("Reference images: " + "; ".join(names) + ". The pouch print must match images 1 to 4 letter for letter and colour for colour." if s["product"]
               else ("Reference images: " + "; ".join(names) + ".") if names else "")


def still_prompt(s):
    refs, note = still_refs(s)
    parts = ["Vertical 9:16 photo, a single frame from a phone-shot UGC video."]
    if s["product"]: parts.append(B["size_first"])
    parts += [s["still"], B["hand_block"] if s["hand"] else B["no_hand"]]
    if s["product"]: parts.append(B["pouch_block"])
    if s["id"] == "S3": parts.append(B["box_block"])
    parts += [B["scene_suffix"], note]
    return refs, " ".join(p for p in parts if p)


def still(sid):
    refs, prompt = still_prompt(S[sid])
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in refs],
                        "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


FRONT = "refs/real/ralph_pouch_upright.jpg"
OMNI = "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py"


def omni_prompt(s):
    refs = [FRONT, TAB, SHEET] + ([HANDREF] if s["hand"] else [])
    head = B["omni_head"].replace("{hand}", ", hand, rings and bracelets" if s["hand"] else "")
    head = head.replace("Image 2 is the real front print of the pouch (logo, dot circle, 'collagen liquid' wordmark and claim lines)",
                        "Image 2 is a real photo of the pouch front (logo, dot circle, 'collagen liquid' wordmark and claim lines)")
    hand = (" Image 5 is Grace's hand sheet: the French-tip nails, crown ring, gold solitaire ring, blue silicone band, flat gold link bracelet"
            " and pearl chain with the leaf charm stay exactly as in images 1 and 5; no other jewellery appears." if s["hand"] else
            " No hand, no fingers and no people appear at any time, at any edge of the frame.")
    return refs, f"{head}{hand} Motion: {s['motion']} {B['omni_tail']}"


def omni(sid, dry=False):
    s = S[sid]; refs, prompt = omni_prompt(s)
    Path("prompts").mkdir(exist_ok=True); pf = Path(f"prompts/{sid}.txt"); pf.write_text(prompt)
    cmd = ["python3", OMNI, ".", sid, "--prompt-file", str(pf), "--still", f"stills/{sid}.png", "--seconds", str(s["seconds"])]
    for r in refs: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


def seedance(sid):
    """No product in frame (S1): Seedance 2.0 Mini reference mode; image 1 = the still, image 2 = Grace's hand sheet."""
    s = S[sid]
    refs = [kie.upload(f"stills/{sid}.png"), kie.upload(HANDREF)]
    prompt = ("Recreate reference image 1 exactly (same kitchen, framing, light, hand, rings and bracelets) as the first frame, then: " + s["motion"]
              + " The hand keeps Grace's French-tip nails, crown ring, gold solitaire ring, blue silicone band, flat gold link bracelet and pearl chain with the leaf charm exactly as in reference image 2. Only this one hand appears. "
              + B["seedance_tail"])
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "reference_image_urls": refs, "generate_audio": False,
                        "resolution": "720p", "aspect_ratio": "9:16", "duration": s["seconds"]}})
    if url: kie.fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    Path("stills").mkdir(exist_ok=True); Path("clips").mkdir(exist_ok=True)
    if kind == "prompt":
        for i in ids: print(still_prompt(S[i]))
    elif kind in ("omni", "omni-dry"):
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(lambda i: omni(i, kind == "omni-dry"), ids))
    elif kind == "seedance":
        for i in ids: seedance(i)
    elif kind == "stills":
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(still, ids))
