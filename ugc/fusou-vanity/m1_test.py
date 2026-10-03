"""Plan v2 step 1 TEST (Ralph OK 2026-10-03, $0.254): still M1 ($0.09) + clip M1a ($0.164), both pasted back onto the real photo.

  python3 m1_test.py still   -> stills/M1_raw.png, stills/M1.png (+ _mask)
  python3 m1_test.py clip    -> clips/M1a_raw.mp4, clips/M1a.mp4
Base = refs/base_M1.png: real listing photo 01 cropped 9:16 around the makeup mirror (x140-500, y40-680), 720x1280.
"""
import subprocess, sys
import kie
J = kie.J
STILL = ("Edit the FIRST reference image, a real photo of a white vanity. KEEP EVERYTHING IN IT EXACTLY AS IT IS: do not redraw, "
 "move, resize, sharpen or recolour anything; same cubbies, same items on the shelves, same landscape mirror with its LED line OFF, "
 "same glass top, same drawers, same crystal knobs, same stool, same wall, same framing. Only ADD ONE HAND: a forearm and hand "
 "reach in from the bottom right edge of the frame, at the same distance from the camera as the vanity, so the hand is natural "
 "size next to the furniture (the hand is about a third as wide as the mirror). The index finger is extended and its fingertip "
 "is just below the small round touch button on the lower edge of the mirror glass (the tiny blue dot), about to tap it; the "
 "other fingers are loosely curled. The hand and forearm only cover part of the stool and the drawers below the mirror, never "
 "the mirror itself. " + J["blocks"]["hand"] + " The second and third reference images show the hands. " + J["blocks"]["phone"])
CLIP = ("Locked-off camera on a tripod: the camera does NOT move, no zoom, no push-in, no pan, no shake; the frame stays exactly the "
 "same for the whole clip. The index fingertip moves up and taps the small round touch button on the lower edge of the mirror "
 "glass once, then the hand lowers a little and rests. At the tap, the thin rounded-rectangle LED line inset around the edge of "
 "the makeup mirror switches on to a soft warm white glow and stays on. Nothing else moves or changes: every shelf item, drawer, "
 "knob, the stool and the wall stay exactly the same. Fingers stay anatomically correct (five fingers), long almond mauve nails "
 "with white French tips. No sound. No on-screen text.")

if sys.argv[1] == "still":
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": STILL, "aspect_ratio": "9:16", "resolution": "1K",
                        "image_input": [kie.upload(p) for p in ["refs/base_M1.png"] + kie.HAND_REFS]}})
    if url:
        kie.fetch(url, "stills/M1_raw.png")
        subprocess.run(["python3", "pasteback.py", "still", "refs/base_M1.png", "stills/M1_raw.png", "stills/M1.png"], check=True)
else:
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": CLIP, "first_frame_url": kie.upload("stills/M1.png"),
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
    if url:
        kie.fetch(url, "clips/M1a_raw.mp4")
        subprocess.run(["python3", "pasteback.py", "video", "refs/base_M1.png", "clips/M1a_raw.mp4", "clips/M1a.mp4"], check=True)
