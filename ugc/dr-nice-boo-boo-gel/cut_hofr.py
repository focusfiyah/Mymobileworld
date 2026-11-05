"""House of Rameau version (Ralph 2026-11-05: "Make the HofR version"): own order, windows, framing and grade; on-screen hook
text from frame 0 held through the first shot (safe zone y 360-1340); no captions; no audio. Template: ../foodology-red-jelliquid.
  python3 cut_hofr.py -> out/hofr_v1.mp4"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
HOOK = "the bandaid fight|is officially over"   # curiosity text (research/hooks.md V1 option), never names the product
# Grace's V1 order is S1 S2 S3 S4 S5 S6; HofR opens on the knee, different windows, 1.10 punch-in, bright cool grade
SEG = [("clips/S3_seedance.mp4", 0.3, 2.5), ("clips/S1.mp4", 1.6, 2.0), ("clips/S2_seedance.mp4", 1.8, 1.6),
       ("clips/S6.mp4", 1.5, 2.0), ("clips/S5.mp4", 2.2, 2.0), ("clips/S4.mp4", 2.6, 1.9)]
VF = "scale=1188:2112:flags=lanczos,crop=1080:1920,setsar=1,fps=30,eq=brightness=0.02:saturation=0.97,colorbalance=bs=0.03:bm=0.02"
Path("out/h").mkdir(parents=True, exist_ok=True); parts = []
for i, (c, ss, d) in enumerate(SEG):
    o = f"out/h/seg{i}.mp4"; parts.append(o)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", c, "-t", str(d), "-an", "-vf", VF, "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-threads", "4", o], check=True)
Path("out/h/list.txt").write_text("".join(f"file '{Path(p).name}'\n" for p in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "out/h/list.txt", "-c", "copy", "out/h/raw.mp4"], check=True)
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 62)
d.rounded_rectangle((170, 420, 910, 610), radius=36, fill=(255, 255, 255, 240))   # top of the safe zone: the knee and gel stay clear below
for i, line in enumerate(HOOK.split("|")): d.text((540, 475 + i * 80), line, fill=(20, 40, 70), font=f, anchor="mm")
card.save("out/h/hook.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "out/h/raw.mp4", "-i", "out/h/hook.png", "-filter_complex",
                f"[0][1]overlay=0:0:enable='lt(t,{SEG[0][2]})'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "out/h/text.mp4"], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", "out/h/text.mp4", "out/hofr_v1.mp4"], check=True)
print("OK out/hofr_v1.mp4")
