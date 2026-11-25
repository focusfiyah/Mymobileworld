"""HofR Black Friday cut of the ili double flap case (Ralph 2026-11-25: "I want the double eyeglass case. The flap eyeglass case";
tapped "Re-cut 18-20 s" and "Ear Wax Camera (today)"). Own shot order and framing vs Grace's 13.8 s V1, hook card from frame 0, no captions, with Ralph's Chatterbox voice (Ralph 2026-11-25 tapped "Your voice (Chatterbox)"), shots timed to his lines."""
import subprocess, os
from PIL import Image, ImageDraw, ImageFont
SRC = "orig/ili.mov"
SEGS = [(51.0, 55.85), (24.3, 27.08), (17.5, 21.7), (82.0, 85.47), (36.0, 39.57), (62.0, 66.99)]  # one shot per VO line (Ralph's Chatterbox voice at 1.08x)
VO = "../../houseoframeau/posts/bf-ili-case/vo/ralph.wav"
HOOK = ["One case for your sunglasses", "AND your everyday glasses"]; BOX = (110, 380, 860, 190); HOOK_UNTIL = 3.5
os.makedirs("out/hofr", exist_ok=True)
x, y, w, h = BOX; card = Image.new("RGBA", (1080, 1920)); d = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 54)
d.rounded_rectangle((x, y, x + w, y + h), radius=36, fill=(255, 255, 255, 242))
for k, line in enumerate(HOOK): d.text((x + w / 2, y + h * (0.32 + 0.38 * k)), line, fill=(20, 40, 70), font=f, anchor="mm")
card.save("out/hofr/hook.png")
ins, fc = [], []
for i, (a, b) in enumerate(SEGS):
    ins += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", SRC]
    fc.append(f"[{i}:v]fps=30,crop=iw/1.05:ih/1.05:(iw-iw/1.05)*0.5:(ih-ih/1.05)*0.6,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p[v{i}]")
n = len(SEGS); ins += ["-i", "out/hofr/hook.png"]
fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.03:contrast=1.03:saturation=1.02[g]")
fc.append(f"[g][{n}:v]overlay=0:0:enable='lt(t,{HOOK_UNTIL})'[v]")
ins += ["-i", VO]; fc.append(f"[{n + 1}:a]atempo=1.08,adelay=100|100,loudnorm=I=-14:TP=-1.5:LRA=11,apad[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{sum(b - a for a, b in SEGS):.3f}", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-threads", "4", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", "out/hofr/ili_hofr.mp4"], check=True)
print("CUT_DONE", round(sum(b - a for a, b in SEGS), 2))
