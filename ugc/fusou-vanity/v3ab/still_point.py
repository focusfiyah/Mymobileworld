"""Pointing-hand stills for V3 (Ralph OK 2026-10-04, $0.09 each, nano-banana-pro 9:16 1K). Base = real listing photo; paste-back keeps the vanity pixels.
  python3 v3ab/still_point.py P1|P2   (run from ugc/fusou-vanity)"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import kie_ab as kie
SAME = ("Keep this photo EXACTLY as it is: the white vanity, every drawer, mirror, shelf, product and the room are unchanged, same camera, same light, nothing moved or added except the hand. "
        "Add ONE woman's right hand and forearm entering from the very edge of the frame in the foreground, closer to the camera than the vanity so it looks larger and a little soft. "
        "The hand is hers: warm brown skin, long almond-shaped nails, glossy dusty mauve-pink gel polish with a thin white French tip (see the hand reference images). "
        "The index finger is extended and POINTS toward the vanity, the other fingers loosely curled, the hand relaxed and natural, the whole wrist and forearm visible all the way to the frame edge, "
        "exactly five fingers, no ring, no bracelet, no sleeve. Real phone-camera look, no text, no logos.")
P = {"P1": "The arm comes in from the bottom left corner, the fingertip pointing up and to the right at the center of the lit makeup mirror. ",
     "P2": "The arm comes in from the bottom right corner, the fingertip pointing up and to the left across the whole vanity at the tall full-length mirror on the right and the cabinet. "}
k = sys.argv[1]
url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": P[k] + SAME, "image_input": [kie.upload(p) for p in ["refs/base_A_916.jpg", "refs/hand_dorsal.png", "refs/hand_palm.png"]], "aspect_ratio": "9:16", "resolution": "1K"}})
if url: kie.fetch(url, f"stills/{k}_raw.png"); print(k, "ok")
