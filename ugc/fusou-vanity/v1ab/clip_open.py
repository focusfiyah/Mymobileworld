"""ONE clip (Seedance 2.0 Mini on Kie, 4 s, 720p 9:16, no audio, $0.164) from stills/OPEN_FACE.png (Ralph OK 2026-10-04)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "grace")); from gate import require; require(pathlib.Path(__file__).resolve().parent)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import kie_ab as kie
prompt = ("Locked-off phone camera on a stand, close-up of a woman's face doing her makeup at a bathroom mirror, exactly as in the first frame. She sweeps the "
 "blush brush slowly and gently along her cheekbone, down and back up once, then lifts it a little, while her eyes stay on the mirror. Her head stays almost still, "
 "only tiny natural movements. Her mouth stays closed and relaxed, she does not talk, her eyebrows stay relaxed and level, no forehead wrinkles. The dull flat "
 "yellow-green bathroom light stays exactly the same, no lighting change, no zoom, no camera move. The hand and nails stay the same. Real phone-footage look, no text.")
url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": kie.upload("stills/OPEN_FACE.png"),
                    "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
if url: kie.fetch(url, "clips/OPEN_FACE.mp4"); print("OPEN_FACE clip ok")
