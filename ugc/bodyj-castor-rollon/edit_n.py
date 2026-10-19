"""Edit the v2g brows (N3) and cuticle (N4) stills (2026-10-18): keep the shot, move only the roller ball to the right spot. $0.09 each.
  python3 edit_n.py N3 N4"""
import sys, kie
P = {
 "N3": ("stills_raw/N3_r1.png", "Edit the FIRST image only. Keep the woman, her skin, her closed eye, her hand, the bedroom and the light exactly the same. "
        "Change only two things: (1) her hand moves the roll-on up so the pink rose quartz ball rests ON the eyebrow hairs, at the middle of the "
        "eyebrow arch, not near the eye or the nose; (2) reframe as a tighter close-up so only the eyebrow, the closed eye, the temple and a little "
        "forehead and hair show: no nose tip, no lips, no mouth, no chin. The bottle and its label must look exactly like the bottle in the SECOND "
        "image (amber glass, white collar, label 'Body4You 100% Premium Quality CASTOR OIL' upright). No text."),
 "N4": ("stills_raw/N4_r1.png", "Edit the FIRST image only. Keep her left hand on the towel, her nails, the mauve tee, the bathroom and the light exactly "
        "the same. Change only this: her right hand moves the roll-on so the pink rose quartz ball presses ON the cuticle of her left middle finger: "
        "the thin strip of skin right at the base of the nail, where the nail meets the finger. Not on the fingertip, not on the nail surface, not "
        "on the knuckle. Show that fingernail base clearly. The bottle and its label must look exactly like the bottle in the SECOND image "
        "(label upright and readable). No text."),
}
ref = kie.upload("refs/bottle_front.png")
for sid in sys.argv[1:]:
    src, prompt = P[sid]
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(src), ref], "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, f"stills/{sid}.png"); print(sid, "edit ok")
    else: print(sid, "edit FAILED")
