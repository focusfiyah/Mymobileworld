"""Power Bank Flashlight V2 (Grace) runner, 2026-10-22. Every paid call passes grace/gate.py (script gate, approved BOOK.md,
budget lock, paid-task ledger) through kie.run_task / omni_clip.py.
  python3 run.py stills S5 S6 ...   Kie nano-banana-pro ($0.09) with gemini_app/prompt_Sx.txt + its refs + Ralph's S1/S2 as look refs
  python3 run.py omni S4 ...        Omni 1.1 Flash on Kie ($0.315, 4 s) from stills/Sx.png + prompts/clip_Sx.txt
  python3 run.py omni-dry S4        prints cost + request, spends nothing"""
import re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

G = "gemini_app/"
REF = {"sheet": G + "ref1_product_sheet.png", "shape": G + "ref2_true_shape.png", "lens": G + "ref3_lens_closeup.png",
       "hand": G + "ref4_grace_hand.jpg", "port": G + "ref5_port_closeup.png", "logo": G + "ref6_logo_closeup.png"}
STILL_REFS = {"S5": ["sheet", "shape", "logo", "lens"], "S6": ["sheet", "shape", "logo"], "S7": ["sheet", "shape", "hand"],
              "S8": ["sheet", "shape", "logo", "hand"], "S9": ["sheet", "shape", "logo", "hand"]}
HAND_SHOTS = {"S1", "S4", "S7", "S8", "S9"}
# Omni image order must match the numbering in prompts/clip_Sx.txt: still, logo, [lens|port], sheet, [hand]
CLIP_EXTRA = {"S2": ["port"], "S4": ["lens"], "S5": ["lens"]}
OMNI = "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py"


def still(sid):
    text = Path(f"{G}prompt_{sid}.txt").read_text()
    refs = [REF[r] for r in STILL_REFS[sid]]
    extra = []
    if sid in HAND_SHOTS:
        refs.append("stills/S1.png"); extra.append(f"Image {len(refs)} = an approved photo from this same series: match its hand, skin, French-tip nails, rings and bracelets exactly")
    refs.append("stills/S2.png"); extra.append(f"Image {len(refs)} = an approved photo of the same campsite from this series: match its tent, picnic table, pine trees, mountains, colours and how dark the scene is")
    text = re.sub(r"^I am uploading \d+ reference images\. (.*?)\.\n", lambda m: f"I am uploading {len(refs)} reference images. {m.group(1)}; " + "; ".join(extra) + ".\n", text, count=1)
    text += ("\nLIGHT: the scene is dim like the approved campsite photo, the dusk sky darkened closer to night, so the flashlight's own "
             "light glows clearly and is the brightest thing in the photo, while the campsite stays visible.\n")
    Path("prompts").mkdir(exist_ok=True); Path(f"prompts/still_{sid}.txt").write_text(text)
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": text, "image_input": [kie.upload(p) for p in refs],
                        "aspect_ratio": "9:16", "resolution": "2K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def small(path):  # Kie Omni answered 500 twice on the full-size PNG inputs (8 MB total); youtheory's working takes used ~1 MB files
    return f"omni_in/{Path(path).stem}.jpg"


def omni(sid, dry=False):
    refs = [REF["logo"]] + [REF[r] for r in CLIP_EXTRA.get(sid, [])] + [REF["sheet"]] + ([REF["hand"]] if sid in HAND_SHOTS else [])
    cmd = ["python3", OMNI, ".", sid, "--prompt-file", f"prompts/clip_{sid}.txt", "--still", small(f"stills/{sid}.png"), "--seconds", "4", "--res", "1080p"]
    for r in refs: cmd += ["--ref", small(r)]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    Path("clips").mkdir(exist_ok=True)
    if kind == "stills":
        with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(still, ids))
    elif kind in ("omni", "omni-dry"):
        with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(lambda i: omni(i, kind == "omni-dry"), ids))
