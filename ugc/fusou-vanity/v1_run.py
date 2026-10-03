"""Video 1 (daylight, edit-the-real-photo method). Stills A (no hand, LEDs on) and B (hand on the desk edge); clips S2-S5; S1 = clips/EDIT_TEST2_clip.mp4 (paid, trimmed).
  python3 v1_run.py stills | python3 v1_run.py clips"""
import sys, threading
import kie
J = kie.J
KEEP = ("KEEP THE VANITY EXACTLY AS IT IS in the first image: do not redraw, move, resize or change anything on it: the same top row of 4 "
 "cubbies, the same two shelf columns with the same items, the same wide landscape makeup mirror, the same 4 glass-top drawers, the same two "
 "drawer towers, the same stool, the same tall mirror door on the right, the same crystal knobs. ")
FILL = ("The blurry bands above and below the photo are empty placeholders: repaint the TOP band as continuing beige wall and the BOTTOM band "
 "(about a quarter of the frame) as SHARP light oak plank floor with the same soft sunlight patches, planks running toward the camera in the "
 "same perspective, so nothing stays blurred. Switch both LED light lines (the makeup mirror and the tall mirror door) on to a warm white glow, "
 "like the second reference image. ")
STILLS = {
 "V1A": ("Edit the FIRST reference image into a vertical 9:16 phone photo. " + KEEP + FILL + "There are NO hands and no people in this photo. "
         "Camera straight-on, daylight, nothing else changes. " + J["blocks"]["phone"], ["refs/base_A_916.jpg", "refs/vanity_lit_room.jpg"]),
 "V1B": ("Edit the FIRST reference image into a vertical 9:16 phone photo. " + KEEP + FILL + "Add ONE hand reaching in from the lower left of the "
         "frame, only the fingertips resting lightly on the front edge of the desk at its left end, just above the first drawer, the fingers relaxed "
         "and slightly spread; the hand stays SMALL, no bigger than a fifth of the frame height, and covers almost none of the vanity. "
         + J["blocks"]["hand"] + " The third and fourth reference images show the hands. Camera straight-on, daylight, nothing else changes. "
         + J["blocks"]["phone"], ["refs/base_A_916.jpg", "refs/vanity_lit_room.jpg"] + kie.HAND_REFS),
}
SAME = ("The vanity, mirrors, shelves, drawers, stool and everything on them stay exactly as in the first frame: nothing appears, disappears or changes "
        "shape. The camera is locked off on a tripod: no zoom, no push-in, no pan, no shake unless stated. ")
CLIPS = {
 "V1S2": ("V1A_fix", 4, "Very slow, gentle push-in toward the makeup mirror, about 8 percent over the clip, smooth. No hands, no people. " + SAME + "No sound."),
 "V1S3": ("V1A_fix", 5, "The warm LED light lines of the makeup mirror and the tall mirror door slowly shift colour from warm yellow to cool white and then "
                     "back to warm white, as if cycling the light modes, and dim down a little and back up. No hands, no people. " + SAME + "No sound."),
 "V1S4": ("V1B_fix", 4, "The relaxed fingertips glide slowly along the front edge of the desk from the left end toward the right, past the crystal knobs, "
                     "then lift away out of frame. " + J["blocks"]["hand"] + " " + SAME + "No sound."),
 "V1S5": ("V1A_fix", 4, "Held steady, the warm LED glow holds with a very faint, slow shimmer; nothing moves. No hands, no people. " + SAME + "No sound."),
}
def still(k):
    p, refs = STILLS[k]
    u = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": p, "image_input": [kie.upload(r) for r in refs], "aspect_ratio": "9:16", "resolution": "1K"}})
    if u: kie.fetch(u, f"stills/{k}.png"); print("still", k, "ok", flush=True)
def clip(k):
    st, dur, p = CLIPS[k]
    u = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": p, "first_frame_url": kie.upload(f"stills/{st}.png"), "generate_audio": False,
                                                                     "resolution": "720p", "aspect_ratio": "9:16", "duration": dur}})
    if u: kie.fetch(u, f"clips/{k}.mp4"); print("clip", k, "ok", flush=True)
if __name__ == "__main__":
    fn, items = (still, list(STILLS)) if sys.argv[1] == "stills" else (clip, sys.argv[2:] or list(CLIPS))
    ts = [threading.Thread(target=fn, args=(k,)) for k in items]; [t.start() for t in ts]; [t.join() for t in ts]
