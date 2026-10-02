"""Close-up test: crop of the real photo (left drawer tower) + Grace's hand pulling a drawer. Then a 4s test clip from EDIT_TEST2."""
import kie
J = kie.J
p1 = ("Edit the FIRST reference image (a soft, low-resolution crop of the real vanity's left drawer tower, with the first "
 "drawer of the top row at the top) into a SHARP vertical 9:16 close-up phone photo. Keep every drawer, knob and edge EXACTLY "
 "as in the first image: the same white flat drawer fronts with thin shadow gaps, the same round crystal knobs on chrome stems, "
 "the same proportions; do not add or remove drawers. Make it crisp with natural daylight. Add one hand from the right "
 "pulling the second drawer from the top open about three inches by its crystal knob, showing a white divider tray with a "
 "few makeup items inside. " + J["blocks"]["hand"] + " The second and third reference images show the hands. Straight-on "
 "camera, nothing else changes. " + J["blocks"]["phone"])
body = {"model": "nano-banana-pro", "input": {"prompt": p1, "image_input": [kie.upload("refs/base_closeup_drawers.jpg")] + [kie.upload(x) for x in kie.HAND_REFS],
                                              "aspect_ratio": "9:16", "resolution": "1K"}}
import threading
def still():
    u = kie.run_task(body)
    if u: kie.fetch(u, "stills/CLOSEUP_TEST.png"); print("CLOSEUP_TEST ok", flush=True)
def clip():
    prompt = ("The index fingertip presses the small round touch button at the lower left corner of the makeup mirror and "
              "lifts off; right after, the two warm LED light lines dim for a moment and come back on. The camera does not move. "
              + J["blocks"]["hand"] + " The vanity, mirrors, shelves, drawers, stool and everything on them stay exactly as in the "
              "first frame: nothing appears, disappears or changes shape. " + J["video_suffix"])
    u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": kie.upload("stills/EDIT_TEST2.png"),
                      "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
    if u: kie.fetch(u, "clips/EDIT_TEST2_clip.mp4"); print("CLIP ok", flush=True)
ts = [threading.Thread(target=still), threading.Thread(target=clip)]
[t.start() for t in ts]; [t.join() for t in ts]
