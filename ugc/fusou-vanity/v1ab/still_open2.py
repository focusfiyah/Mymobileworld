"""Face still v2 (Nano Banana Pro, 1K 9:16, $0.09): Ralph 2026-10-04: face farther away (full face, not tight), relaxed, mouth closed. Refs = his 3 Grace photos (crops) + hand refs."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "grace")); from gate import require; require(pathlib.Path(__file__).resolve().parent)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import kie_ab as kie
prompt = ("Vertical 9:16 photo, a single frame from a phone-shot UGC video, framed as a medium shot from the chest up: the woman's WHOLE head, hair and shoulders are in "
 "frame with plenty of space around her, her face takes up only about a quarter of the frame height, nothing is cropped. She is the SAME woman as in the first three reference images "
 "(same face, dark brown skin, defined brows, dark brown eyes, full lips, long black knotless boho braids with curly ends, half up with a side part), wearing a plain dark brown long-sleeve top. "
 "She stands at a bathroom mirror doing her makeup, looking calmly at her reflection (toward the camera). HER FACE IS RELAXED: soft neutral calm expression, mouth gently closed, "
 "eyebrows relaxed and level, forehead smooth with no wrinkles, no frown, no squinting. Her right hand holds a fluffy blush brush against her cheekbone, the whole hand and wrist visible "
 "at a natural small size. The hand is hers: long almond-shaped nails, glossy dusty mauve-pink gel polish with a thin white French tip (the last two reference images show the hand). "
 "BAD LIGHTING: one dull overhead bathroom light, flat and slightly yellow-green, a bit dim, soft shadows under her brows and nose and chin, the skin looks a little dull and tired, no flattering glow. "
 "Plain beige bathroom wall behind her with a little of a door frame, a corner of the bathroom counter at the bottom. Real phone-camera look, natural skin texture, no beauty filter, no text, no logos.")
refs = ["refs/grace/g2_front_crop.jpg", "refs/grace/g1_over_shoulder_right_crop.jpg", "refs/grace/g3_over_shoulder_left_crop.jpg", "refs/hand_dorsal.png", "refs/hand_palm.png"]
url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in refs], "aspect_ratio": "9:16", "resolution": "1K"}})
if url: kie.fetch(url, "stills/OPEN_FACE2.png"); print("OPEN_FACE2 ok")
