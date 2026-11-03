"""House of Rameau version (Ralph 2026-11-03 tapped "Yes, make it"): own order, windows, framing and grade; on-screen hook
text from frame 0 held to the end of the first shot (safe zone y 360-1340); no captions; no audio. -> out/hofr_v1.mp4"""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, "../../.claude/skills/ugc-product-ad/scripts")
from classic_caption import classic_png
HOOK = "wait, this is apple|cider vinegar?"
# different windows + order than Grace's V1; zoom 1.12 punch-in; bright cool grade
SEG = [("clips/S1.mp4", 0.0, 2.4), ("clips/S5_seedance.mp4", 1.6, 1.8), ("clips/S2.mp4", 2.6, 2.0),
       ("clips/S4.mp4", 0.0, 1.8), ("clips/S3.mp4", 2.6, 1.8), ("clips/S6.mp4", 2.8, 2.2)]
VF = "scale=1210:2150:flags=lanczos,crop=1080:1920,setsar=1,fps=30,eq=brightness=0.02:saturation=0.97,colorbalance=bs=0.03:bm=0.02"
Path("out/h").mkdir(parents=True, exist_ok=True); parts = []
for i, (c, ss, d) in enumerate(SEG):
    o = f"out/h/seg{i}.mp4"; parts.append(o)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", c, "-t", str(d), "-an", "-vf", VF, "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-threads", "4", o], check=True)
Path("out/h/list.txt").write_text("".join(f"file '{Path(p).name}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/h/list.txt", "-c", "copy", "out/h/raw.mp4"], check=True)
from PIL import Image, ImageDraw, ImageFont   # hook card like the approved NovaTabz HofR (2026-10-30): readable over any footage
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 62)
d.rounded_rectangle((200, 1140, 880, 1330), radius=36, fill=(255, 255, 255, 240))
for i, line in enumerate(HOOK.split("|")): d.text((540, 1195 + i * 80), line, fill=(40, 20, 22), font=f, anchor="mm")
card.save("out/h/hook.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/h/raw.mp4", "-i", "out/h/hook.png", "-filter_complex",
                f"[0][1]overlay=0:0:enable='lt(t,{SEG[0][2]})'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "out/h/text.mp4"], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", "out/h/text.mp4", "out/hofr_v1.mp4"], check=True)
print("OK out/hofr_v1.mp4")
