import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
W = "C:/dev/OpenMontage/projects/tiger_eye_ralph/"
load_dotenv("C:/dev/OpenMontage/.env")
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"))
refs = [Image.open(W + f) for f in ["ralph_preview_v2.png", "necklace_closeup_crop.png", "necklace_worn_chest.png"]]
BASE = (
 "Image 1 is the man and the necklace. Keep his exact identity details visible in this crop: same dark brown skin "
 "tone, same short clean-cut beard with sharp lines and slight grey at the chin, same lips, same plain black crew-neck "
 "t-shirt, same warm evening home study light. No morphing. "
 "NECKLACE, the hero: exactly the necklace from Image 1, matched to the look in Images 2 and 3: small round glossy "
 "black onyx beads with bright highlights and golden-brown tiger eye beads in pairs all along the strand, a pair of "
 "tiger eye beads right above the pendant, and a smooth polished TEARDROP tiger eye pendant: narrow rounded top, "
 "wide rounded bottom, glossy dome, vivid golden chatoyant bands, small silver bail. Not square, not a rough chunk. "
 "Realistic hands with his same dark brown skin tone, natural nails, five fingers, correct anatomy. Real physical "
 "object, correct small scale, never pasted in. Vertical 9:16 phone video frame, authentic phone-camera look, "
 "shallow depth of field, realistic unretouched skin. No other people. No text, no watermark, no logos. "
)
SHOTS = {
 "still_pendant_closeup": (
  "SHOT: extreme close-up like Image 2. The top of the frame crops through his mouth and beard (mouth slightly open, "
  "mid-sentence, eyes not visible); his thumb and index finger pinch the teardrop pendant and hold it toward the lens "
  "in the lower-middle of the frame, tilted so the golden bands flash in the warm lamp light. The pendant is in razor "
  "sharp focus, the beads leading up both sides of the frame toward his neck."),
 "still_beads_slide": (
  "SHOT: close-up of his chest from the chin down. His fingertips run along one side of the strand, lightly lifting "
  "the beads so the alternating glossy black onyx and golden tiger eye beads catch the light; the teardrop pendant "
  "hangs centered below on the black t-shirt, in focus. Beard and chin just visible at the top edge."),
}
cfg = types.GenerateContentConfig(response_modalities=["IMAGE"], image_config=types.ImageConfig(aspect_ratio="9:16", image_size="2K"))
for name, shot in SHOTS.items():
    try:
        resp = client.models.generate_content(model="gemini-3-pro-image", contents=[BASE + shot, *refs], config=cfg)
    except Exception as e:
        print(name, "FAILED", str(e)[:300]); continue
    parts = [p for c in (resp.candidates or []) for p in (c.content.parts if c.content else [])]
    img = next((p.inline_data.data for p in parts if getattr(p, "inline_data", None)), None)
    if not img:
        print(name, "NO IMAGE"); continue
    open(W + name + ".png", "wb").write(img)
    open(W + name + "_prompt.txt", "w", encoding="utf-8").write(BASE + shot)
    print(name, "OK")
