import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
W = "C:/dev/OpenMontage/projects/tiger_eye_ralph/"
load_dotenv("C:/dev/OpenMontage/.env")
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
refs = [Image.open(W + f) for f in ["ralph_preview_v1.png", "ralph_face.png", "necklace_closeup_crop.png", "necklace_worn_chest.png"]]
prompt = (
 "Image 1 is the man to reproduce. Image 2 is the same man's real face photo. Keep his EXACT identity and look from "
 "Image 1: same face, eyes, nose, lips, skin tone, bald head, same slim face and build as Image 1, the same short "
 "clean-cut neatly trimmed beard with sharp lines and slight grey at the chin, and the same thin matte black "
 "rectangular glasses. No morphing, no facial drift, no beautification. "
 "WARDROBE: a plain black crew-neck cotton t-shirt, no print, no logo. "
 "NECKLACE (the hero of the image, most important): copy the necklace shown in Images 3 and 4 exactly. A strand of "
 "small round glossy black onyx beads with bright specular highlights, with golden-brown tiger eye beads placed in "
 "pairs regularly all the way along the strand, about every few centimetres, and a pair of tiger eye beads directly "
 "above the pendant. The pendant is a smooth polished rounded TEARDROP tiger eye stone, narrow at the top and wide "
 "and rounded at the bottom, glossy, with vivid golden chatoyant bands that shimmer in the light, hanging from a small "
 "silver bail. NOT a square, NOT a rough tumbled chunk. It is worn over the black t-shirt, the strand clearly "
 "outlined against the fabric, pendant resting mid-chest in sharp focus and fully visible, catching the warm lamp "
 "light. Real physical object with correct small scale and soft shadow, never pasted in. "
 "SCENE: vertical 9:16 phone video frame. The phone is propped on the desk in front of him, so NO arm is extended "
 "toward the camera and both hands are free; framed from mid-torso up, he is seated, leaning slightly toward the "
 "lens, one hand raised in an open expressive gesture, looking straight into the lens with an energetic, friendly, "
 "open-mouthed expression as if mid-sentence. Background: the same warm evening home study as Image 1, walnut "
 "bookshelves, brass table lamp, soft warm bokeh lights, slightly out of focus. Warm natural indoor light, realistic "
 "unretouched skin texture, authentic phone-camera look, no cinematic grading. No other people. No text, no "
 "watermark, no logos."
)
cfg = types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="9:16", image_size="2K"))
resp = client.models.generate_content(model="gemini-3-pro-image", contents=[prompt, *refs], config=cfg)
parts = [p for c in (resp.candidates or []) for p in (c.content.parts if c.content else [])]
img = next((p.inline_data.data for p in parts if getattr(p, "inline_data", None)), None)
if not img:
    print("NO IMAGE", getattr(resp, "prompt_feedback", None), [getattr(c, "finish_reason", None) for c in (resp.candidates or [])]); raise SystemExit(1)
open(W + "ralph_preview_v2.png", "wb").write(img)
open(W + "ralph_preview_v2_prompt.txt", "w", encoding="utf-8").write(prompt)
print("OK", Image.open(W + "ralph_preview_v2.png").size)
