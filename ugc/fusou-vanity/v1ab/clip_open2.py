"""ONE clip (Seedance 2.0 Mini on Kie, 4 s, 720p 9:16, no audio, $0.164) from stills/OPEN_FACE2.png (Ralph OK 2026-10-04)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "grace")); from gate import require; require(pathlib.Path(__file__).resolve().parent)
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import kie_ab as kie
prompt = ("Locked-off phone camera on a stand, medium shot of a woman doing her makeup at a bathroom mirror, exactly as in the first frame, same framing, no zoom, no camera move. "
 "She sweeps the blush brush slowly and gently along her cheekbone, down and back up once, while she looks calmly at her reflection. Her whole face stays relaxed: calm neutral "
 "expression, mouth gently closed, she does not talk or smile, eyebrows relaxed and level, forehead smooth, no frown. Her head and body stay almost still, only tiny natural "
 "movements and blinks. The dull flat yellow-green bathroom light stays exactly the same, no lighting change. Her hand, nails, hair and top stay exactly the same. Real phone-footage look, no text.")
url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": kie.upload("stills/OPEN_FACE2.png"),
                    "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
if url: kie.fetch(url, "clips/OPEN_FACE2.mp4"); print("OPEN_FACE2 clip ok")
