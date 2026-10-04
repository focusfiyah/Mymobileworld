"""V4 pain shot (Ralph OK 2026-10-03): bags and shoes on the bedroom floor, Grace's small hand lifting a bag. Still $0.09; clip (4 s, $0.164) after review."""
import sys, kie
J = kie.J
P = ("Vertical 9:16 phone photo, a mid-close shot taken from standing height looking down at about 45 degrees at a patch of light oak plank floor beside a beige wall with a white baseboard "
     "and the edge of a soft grey rug, the same floor, rug and soft window sunlight patches as the third reference image. On the floor, dropped in a messy pile: a tan leather handbag lying on its side "
     "with its strap (the handbag looks like the one in the fourth reference image), a pair of nude high heels tipped over, and a pair of beige ankle boots. One small hand comes in from the right of the frame, "
     "the fingers just closing around the handbag's handle, about to lift it. There is NO furniture, NO vanity, NO mirror and no other people in this photo. "
     + J["blocks"]["hand"] + " The first two reference images show the hands. " + J["blocks"]["phone"])
if sys.argv[1] == "still":
    refs = kie.HAND_REFS + ["refs/base_floor_crop.jpg", "refs/listing_18.jpg"]
    u = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": P, "image_input": [kie.upload(r) for r in refs], "aspect_ratio": "9:16", "resolution": "1K"}})
    if u: kie.fetch(u, "stills/FL1.png"); print("FL1 ok")
else:
    C = ("The small hand lifts the tan leather handbag up off the floor by its handle and out of the top of the frame, slowly and smoothly; the heels and boots stay on the floor where they are. "
         "The camera is locked off, no zoom, no movement. The floor, the rug and the sunlight stay exactly as in the first frame. No other hands, no people, no furniture. No sound, no on-screen text.")
    u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": C, "first_frame_url": kie.upload("stills/FL1.png"), "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
    if u: kie.fetch(u, "clips/FL1a.mp4"); print("FL1a ok")
