"""Label-drift bake-off (Ralph 2026-10-18: "find what model keeps the product image from drifting").
Same start still (stills/S8.png, real label pasted) as FIRST and LAST frame, same prompt, 720p 9:16, no audio.
  python3 modeltest/run.py            -> modeltest/{seedance_mini,kling3_omni,veo31_lite}.mp4
Quoted: Seedance 2.0 Mini 5 s $0.205 + Kling 3.0 Omni 5 s $0.35 + Veo 3.1 Lite 6 s $0.15 = $0.705. Runs only on Ralph's OK.
Goes through kie.run_task, so the script gate runs before every paid call."""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kie

STILL = "stills/S8.png"
PROMPT = ("Locked-off phone camera on a bright kitchen counter in daylight. The hand enters from the right frame edge, "
          "presses the white lid down onto the tub with its fingertips, then lifts a little and rests on the lid. "
          "The tub never moves, never turns and never tilts: its front label faces the camera the whole time and every "
          "printed word, logo and stripe stays sharp and exactly the same. Only the hand moves. No new objects, no text, no music.")


def jobs(url):
    return {
        "seedance_mini": {"model": "bytedance/seedance-2-mini", "input": {"prompt": PROMPT, "first_frame_url": url,
                          "last_frame_url": url, "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 5}},
        "kling3_omni": {"model": "kling-3.0-omni/image-to-video", "input": {"prompt": PROMPT, "image_urls": [url, url],
                        "duration": 5, "resolution": "720p", "aspect_ratio": "auto", "audio": False}},
        "veo31_lite": {"model": "veo-3-1", "input": {"prompt": PROMPT, "model": "veo3_lite", "image_urls": [url, url],
                       "generation_type": "FIRST_AND_LAST_FRAMES_2_VIDEO", "aspect_ratio": "9:16", "resolution": "720p", "duration": 6}},
    }


def one(item):
    name, body = item
    out = Path(f"modeltest/{name}.mp4")
    if out.exists():
        print("cached", out); return
    u = kie.run_task(body)
    if u:
        kie.fetch(u, out); print("ok", name, flush=True)


if __name__ == "__main__":
    url = kie.upload(STILL)
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(one, jobs(url).items()))
