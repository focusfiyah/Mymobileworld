"""Tiger eye necklace 15s spot on Seedance 2.0 Mini (Kie REST). Usage: python kie_tiger_eye.py tiger15 v1 [taskId]"""
import json
from pathlib import Path
import kie_seedance_mini as k


def _gate():  # SCRIPT GATE (gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven; job dir = $UGC_JOB or cwd
    import os as _o, sys as _s, pathlib as _p; _s.path.insert(0, str(_p.Path(__file__).resolve().parent))
    from gate import require; require(_o.environ.get("UGC_JOB") or _o.getcwd())



P = Path("C:/dev/OpenMontage/projects/tiger_eye_ralph")
k.P, k.R = P, P / "renders"
k.URLS = json.loads((P / "hosted_urls.json").read_text())

k.PROMPTS["tiger15"] = (
    "Vertical 9:16 realistic TikTok creator video, filmed on a phone propped on a desk in a warm evening home study. "
    "Reference image 1 is the man, the room and the necklace: keep his EXACT identity for the whole clip - bald head, "
    "dark brown skin, slim face and build, short clean-cut beard with sharp lines and slight grey at the chin, thin matte "
    "black rectangular glasses, plain black crew-neck t-shirt. No morphing, no facial drift. Walnut bookshelves, brass "
    "table lamp, soft warm bokeh lights behind him. "
    "Reference images 2 and 3 show the necklace up close: small round glossy black onyx beads with pairs of golden-brown "
    "tiger eye beads all along the strand, and a smooth polished teardrop tiger eye pendant with shimmering golden bands "
    "on a small silver bail. The necklace looks identical in every shot. "
    "He speaks straight to the camera in a deep, energetic, confident male American voice, fast-paced and excited, like "
    "a creator hyping a product he loves. No arm reaching toward the camera; both hands are free. "
    "Shot 1 (0-2.8s): medium shot from mid-torso up. He holds the necklace strand up toward the lens with both hands, "
    "pendant dangling in the middle, and says: \"Okay, if this is your year to level up, do not scroll past this.\" "
    "Shot 2 (2.8-6s): same medium shot. He lets the necklace drop onto his chest, then taps the pendant with two fingers "
    "and says: \"This isn't just jewelry. It's your everyday reminder to attract wealth and abundance.\" "
    "Shot 3 (6-9.8s): extreme close-up matching reference image 2: his mouth and beard at the top of frame, his thumb and "
    "index finger pinch the teardrop pendant toward the lens and tilt it so the golden bands flash in the lamp light. He "
    "says: \"Genuine tiger eye. Look how it catches the light. Heavy, solid, the real deal.\" "
    "Shot 4 (9.8-11.7s): close-up matching reference image 3: his fingertips run slowly along the strand, lifting the "
    "black and gold beads into the light, pendant hanging below. He says: \"Black and gold beads, all the way around.\" "
    "Shot 5 (11.7-15s): back to the medium shot. He leans in and says: \"These keep selling out.\" Then he points down "
    "toward the bottom of the screen and says: \"Link's down there, grab yours.\" He grins and says just once: \"Trust "
    "me, thank me later.\" "
    "Audio: only those spoken lines, each said just once. Fast, energetic pace but crisp, clear articulation: every word pronounced fully and separately, never slurred or blended into the next word, with a short breath between sentences. Quiet room tone. No background music. No other "
    "dialogue. No on-screen text, captions or logos."
)
k.CLIP_REFS["tiger15"] = ["medium", "pendant_closeup", "beads_slide"]

_orig_submit = k.submit
def submit(clip, headers, record):
    import requests, time
    body = {"model": "bytedance/seedance-2-mini", "input": {
        "prompt": k.PROMPTS[clip], "reference_image_urls": [k.URLS[x] for x in k.CLIP_REFS[clip]],
        "generate_audio": True, "resolution": "720p", "aspect_ratio": "9:16", "duration": 15}}
    _gate()
    r = requests.post(f"{k.API}/createTask", headers=headers, json=body, timeout=60)
    resp = r.json()
    print("createTask HTTP", r.status_code, json.dumps(resp)[:300])
    record.update({"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "request": body, "create_response": resp})
    return (resp.get("data") or {}).get("taskId")
k.submit = submit

if __name__ == "__main__":
    k.main()
