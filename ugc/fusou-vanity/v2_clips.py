"""V2 motion clips (Ralph OK 2026-10-03, plan $0.918): B2 under-sink bag (still $0.09 / clip $0.164), WK2 walk-in with mirror light fade-on ($0.205), WK3 dolly-out ($0.205)."""
import sys, kie
J = kie.J
STAY = ("The vanity, its mirrors, shelves, drawers, stool, the door, the window and the bed stay exactly as in the first frame: nothing appears, disappears or changes shape. Natural daylight, no sound, no on-screen text.")
what = sys.argv[1]
if what == "B2still":
    P = ("Vertical 9:16 phone photo of a small, slightly cramped bathroom, taken from standing height looking down at about 45 degrees at the open cabinet under a white pedestal-free bathroom sink: "
         "inside the dark cabinet, a stuffed clear-and-beige zip makeup bag crammed in next to a bottle of cleaner and a roll of toilet paper, a few makeup products (a lipstick, a foundation bottle, a brush) spilled around it. "
         "One small hand with long almond nails (the hands in the two reference images) is gripping the makeup bag's zipper pull and starting to drag the bag out toward the camera. "
         "Plain white bathroom tile floor, grey grout, cool bathroom light, slightly messy and real. No people, no mirror shown, no text. " + J["blocks"]["hand"] + " The two reference images show the hands. " + J["blocks"]["phone"])
    u = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": P, "image_input": [kie.upload(r) for r in kie.HAND_REFS], "aspect_ratio": "9:16", "resolution": "1K"}})
    if u: kie.fetch(u, "stills/B2.png"); print("B2 ok")
elif what == "B2clip":
    C = ("The small hand drags the stuffed makeup bag out of the cabinet toward the camera in one smooth pull, and a lipstick and a brush tumble out of it onto the tile. "
         "The camera is steady, no zoom. The bathroom, the sink and the light stay exactly as in the first frame. No other hands, no people. No sound, no on-screen text.")
    u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": C, "first_frame_url": kie.upload("stills/B2.png"), "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
    if u: kie.fetch(u, "clips/B2a.mp4"); print("B2a ok")
elif what == "WK2":
    P = ("Shot on a phone by someone walking slowly forward into the bedroom toward the vanity while drifting a little to the right: a smooth steady walk with a very slight natural handheld bob, the camera gets closer "
         "to the vanity by about a third so the floor and rug slide past. As the camera approaches, the wide landscape makeup mirror's built-in light strip fades on from off to a soft warm white glow. No people, no hands. " + STAY)
    u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": P, "first_frame_url": kie.upload("stills/WB.png"), "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 5}})
    if u: kie.fetch(u, "clips/WK2.mp4"); print("WK2 ok")
elif what == "WK3":
    P = ("Shot on a phone by someone walking slowly BACKWARD away from the vanity across the bedroom: a smooth steady backward walk with a very slight natural handheld bob, the camera pulls back so the vanity gets smaller, "
         "the floor and rug slide toward the camera and more of the bedroom (door, window, bed) comes into view. No people, no hands. " + STAY)
    u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": P, "first_frame_url": kie.upload("stills/WK1_f25.png"), "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 5}})
    if u: kie.fetch(u, "clips/WK3.mp4"); print("WK3 ok")
