"""ONE still (Nano Banana Pro, 1K 9:16, $0.09): Grace's face, makeup being applied in bad bathroom light, cropped above the lips (Ralph + Grace 2026-10-04).
Refs: Ralph's 3 Grace photos (crops) + her hand refs. NOT the blue-shirt photo."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "grace")); from gate import require; require(pathlib.Path(__file__).resolve().parent)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import kie_ab as kie
prompt = ("Vertical 9:16 close-up photo, a single frame from a phone-shot UGC video. The woman in the first three reference images (the SAME woman: same face, "
 "dark brown skin, defined brows, dark brown eyes, long black knotless boho braids with curly ends in a side part) is doing her makeup at a bathroom mirror. "
 "We see her face from the top of her head down to just under her nose: the frame cuts off at the bottom of her nose, so her lips and chin are NOT in the frame. "
 "She looks straight ahead into the mirror (toward the camera), eyes open and relaxed, eyebrows relaxed and level, no forehead wrinkles. Her right hand brings a "
 "fluffy makeup blush brush to her cheekbone, pressing it on the cheek; the hand enters from the lower right edge of the frame and is shown only to the wrist. "
 "The hand is hers: long almond-shaped nails with a glossy dusty mauve-pink gel polish and a thin white French tip (the last two reference images show the hand). "
 "BAD LIGHTING: a single dull overhead bathroom light, flat and slightly yellow-green, harsh soft shadows under her eyes and nose and across her forehead, dim, "
 "no flattering glow, the skin looks a bit dull. Plain beige bathroom wall behind her, a little of the mirror frame edge visible. Real phone-camera look, "
 "natural skin texture with pores, no beauty filter, no text, no logos. She wears no visible clothing in frame (only face, hair and the hand with the brush).")
refs = ["refs/grace/g2_front_crop.jpg", "refs/grace/g1_over_shoulder_right_crop.jpg", "refs/grace/g3_over_shoulder_left_crop.jpg", "refs/hand_dorsal.png", "refs/hand_palm.png"]
url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in refs], "aspect_ratio": "9:16", "resolution": "1K"}})
if url: kie.fetch(url, "stills/OPEN_FACE.png"); print("OPEN_FACE ok")
