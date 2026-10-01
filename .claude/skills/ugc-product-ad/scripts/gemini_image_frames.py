"""Re-render product shots with Gemini 3 Pro Image (Google key) for a realistic, in-scene bottle."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

import storyboard_shots  # noqa: F401  (sets sb.BASE / sb.FRAMES)
import storyboard as sb

MODEL = os.environ.get("G_MODEL", "gemini-3-pro-image")
SUFFIX = os.environ.get("SB_SUFFIX", "_g3")

REALISM = (
    "PRODUCT REALISM - most important: the Restlex bottle must look like a real physical object "
    "photographed in this room, never pasted in. Real-world size: about 4.5 inches tall, roughly the "
    "height of an adult hand. Fingers wrap naturally around it and slightly overlap the label edges. "
    "The label curves around the cylindrical bottle with correct perspective. The warm lamp light, "
    "soft shadows and color temperature of the room fall on the bottle; subtle glossy highlight on "
    "the white plastic; same focus, grain and phone-camera noise as the rest of the image. The label "
    "text must read exactly: APPROVED SCIENCE, RESTLEX, +BIOPERINE. "
)

FRAMES = {
    "s5_bottle_to_face": (
        "Shot: two-shot from beside the bed on Az's side, slightly over his shoulder. The woman is "
        "sitting up, tired and unimpressed, not smiling, holding the Restlex bottle up near Az's face "
        "with the label toward the camera. Az is awake, eyes open, looking at the bottle sheepishly, "
        "not smiling."
    ),
    "s6_end_blanket": (
        "Shot: medium shot from the foot of the bed. The woman is rolled away from Az with the duvet "
        "pulled completely over her head, just a lump under the duvet, her face not visible. Az lies "
        "on his back awake, holding the Restlex bottle loosely in both hands on his chest, label toward "
        "the camera, with a sheepish guilty look, not smiling."
    ),
}


def main() -> None:
    load_dotenv("C:/dev/OpenMontage/.env")
    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
    refs = [Image.open(sb.SRC / r) for r in sb.REFS]
    try:
        cfg = types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(aspect_ratio="9:16", image_size="2K"),
        )
    except (AttributeError, TypeError) as e:
        print("ImageConfig unsupported, falling back:", e)
        cfg = types.GenerateContentConfig(response_modalities=["IMAGE"])
    for name in sys.argv[1:] or list(FRAMES):
        prompt = sb.BASE + REALISM + FRAMES[name]
        try:
            resp = client.models.generate_content(model=MODEL, contents=[prompt, *refs], config=cfg)
        except Exception as e:
            print(name, "FAILED", type(e).__name__, str(e)[:400])
            continue
        parts = [p for c in (resp.candidates or []) for p in (c.content.parts if c.content else [])]
        img = next((p.inline_data.data for p in parts if getattr(p, "inline_data", None)), None)
        if not img:
            print(name, "NO IMAGE", getattr(resp, "prompt_feedback", None),
                  [getattr(c, "finish_reason", None) for c in (resp.candidates or [])])
            continue
        dest = sb.OUT / f"{name}{SUFFIX}.png"
        dest.write_bytes(img)
        (sb.OUT / f"{name}{SUFFIX}_prompt.txt").write_text(prompt, encoding="utf-8")
        print(name, "OK", dest, Image.open(dest).size)


if __name__ == "__main__":
    main()
