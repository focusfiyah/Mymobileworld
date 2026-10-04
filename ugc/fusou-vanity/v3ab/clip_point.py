"""ONE clip (Seedance 2.0 Mini on Kie, 4 s, 720p 9:16, no audio, $0.164) from stills/P1_small.png (Ralph OK 2026-10-04). Locked camera (paste-back needs it); handheld sway is added free in the cut."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import kie_ab as kie
prompt = ("First-person POV phone shot of a white vanity desk with mirrors and drawers against a wall, exactly as in the first frame, same framing, camera does not move or zoom. "
 "A woman's small hand and wrist enter from the far left edge of the frame and stay small, at the left edge, with no forearm or sleeve visible. "
 "Her index finger is extended and points toward the lit makeup mirror in the middle of the vanity, the other fingers loosely curled. "
 "The hand makes one small slow gesture: the fingertip rises a little and gently points toward the mirror, holds, then settles. The hand stays inside the left side of the frame, about the same small size, never crosses the vanity, never touches it. "
 "The vanity, drawers, shelves, products, mirrors, plant, floor and light stay exactly the same and completely still, nothing else moves. Her nails stay glossy dusty mauve-pink with a thin white French tip. Real phone-footage look, no text.")
url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": kie.upload("stills/P1_small.png"),
                    "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
if url: kie.fetch(url, "clips/P1_raw.mp4"); print("P1 clip ok")
