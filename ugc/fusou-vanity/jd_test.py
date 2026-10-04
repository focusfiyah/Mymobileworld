"""V2 motion shot JD (Ralph OK 2026-10-03, plan $0.918): top-down hand slides a white vanity drawer open on makeup, jewelry, perfume in trays. Still $0.09; clip (4 s, $0.164) after review."""
import sys, kie
J = kie.J
P = ("Vertical 9:16 phone photo taken straight from above (top-down, camera pointing down) at a white vanity drawer that is half open, from the first reference image's drawer style: "
     "a plain white flat-front drawer with a round clear crystal knob in the middle (like the knobs in the third reference image), white drawer sides, light oak floor just visible at the very bottom edge of the frame. "
     "One small hand with long almond nails (the hands in the first two reference images) holds the crystal knob and is pulling the drawer toward the camera. "
     "Inside the open drawer, a tidy white organizer tray with separate compartments holds: a row of lipsticks and a small makeup palette, a few gold rings and necklaces laid in a velvet-lined compartment, "
     "and two small perfume bottles. Soft natural daylight from a window, clean and bright, everything neatly arranged. No other hands, no people, no text. "
     + J["blocks"]["hand"] + " " + J["blocks"]["phone"])
if sys.argv[1] == "still":
    refs = kie.HAND_REFS + ["refs/base_closeup_drawers.jpg", "refs/vanity_glass_top.jpg"]
    u = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": P, "image_input": [kie.upload(r) for r in refs], "aspect_ratio": "9:16", "resolution": "1K"}})
    if u: kie.fetch(u, "stills/JD1.png"); print("JD1 ok")
else:
    C = ("Top-down shot. The small hand slides the white drawer smoothly further open toward the camera by its crystal knob, revealing more of the tray: the lipsticks, rings, necklaces and perfume bottles slide into view. "
         "The camera is locked off, steady. Everything else stays exactly as in the first frame: same white drawer, same knob, same tray, same light. No other hands, no people. No sound, no on-screen text.")
    u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": C, "first_frame_url": kie.upload("stills/JD1.png"), "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
    if u: kie.fetch(u, "clips/JD1a.mp4"); print("JD1a ok")
