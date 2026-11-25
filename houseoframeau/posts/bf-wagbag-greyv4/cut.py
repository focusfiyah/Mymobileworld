"""HofR cut of a finished Grace edit: own crop + grade + hook card from frame 0, no captions.
   python3 cut.py POST SRC.mp4 -> POST/out/hofr.mp4"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
post = Path(sys.argv[1]).resolve(); src = sys.argv[2]; cfg = json.loads((post / "post.json").read_text())
x, y, w, h = map(int, cfg["hook_box"].split(",")); hl = cfg["hook_text"].split("|")
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
f = ImageFont.truetype(str(Path(__file__).resolve().parents[3] / ".claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf"), 64)
dr.rounded_rectangle((x, y, x + w, y + h), radius=36, fill=(255, 255, 255, 242))
lh = h / (len(hl) + 0.6)
for k, line in enumerate(hl): dr.text((x + w / 2, y + lh * (k + 0.8)), line, fill=(20, 40, 70), font=f, anchor="mm")
card.save(post / "out/hook.png")
fc = f"[0:v]crop={cfg['crop']},scale=1080:1920:flags=lanczos,{cfg['grade']},format=yuv420p,setsar=1[g];[g][1:v]overlay=0:0:enable='lt(t,{cfg['hook_until']})'[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", str(post / "out/hook.png"), "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "copy", "-movflags", "+faststart", str(post / "out/hofr.mp4")], check=True)
print("CUT_DONE", post / "out/hofr.mp4")
