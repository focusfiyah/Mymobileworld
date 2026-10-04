"""Walk-in clip test (Ralph OK 2026-10-03, 5 s = $0.205) from the bedroom plate WB."""
import kie
P = ("Shot on a phone by someone walking slowly forward into the bedroom toward the vanity: a smooth steady forward walk with a very slight natural handheld bob, the camera moves "
     "closer to the vanity by about a third over the clip so the near floor and the rug slide past and the vanity grows in frame, then keeps walking. No people, no hands. "
     "The vanity, its mirrors and the light glow, shelves, drawers, stool, the door on the left, the window and the bed stay exactly as in the first frame: nothing appears, "
     "disappears or changes shape. Natural daylight, no sound, no on-screen text.")
u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": P, "first_frame_url": kie.upload("stills/WB.png"), "generate_audio": False,
                                                                  "resolution": "720p", "aspect_ratio": "9:16", "duration": 5}})
if u: kie.fetch(u, "clips/WK1.mp4"); print("WK1 ok")
