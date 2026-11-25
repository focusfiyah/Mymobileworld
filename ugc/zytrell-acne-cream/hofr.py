"""HofR Black Friday cut of ZYTRELL (Ralph 2026-11-25: "Zytrel Acne Cream Treatment" for the challenge; Grace's V1 is 11.8 s, too short).
16.4 s from the paid clips, own order (pimple, product, cream, dab, clear, product) + 1.04 framing, hook card from frame 0, silent
(music added in TikTok), ai_finish last. Keeps Ralph's S3 trim 2.1-3.9 and S4 ending at 3.1 (finger lift showed a disc)."""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
SHOTS = [("S1", 0.0, 3.0), ("S3", 2.1, 3.9), ("S2", 0.4, 3.2), ("S4", 0.4, 3.1), ("S6_fix", 0.2, 3.4), ("S5", 1.0, 3.9)]
HOOK = ["That one pimple that shows up", "right before every event"]; BOX = (110, 1150, 860, 180); HOOK_UNTIL = 3.0
out = Path("out/hofr"); out.mkdir(parents=True, exist_ok=True)
x, y, w, h = BOX; card = Image.new("RGBA", (1080, 1920)); d = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 52)
d.rounded_rectangle((x, y, x + w, y + h), radius=36, fill=(255, 255, 255, 242))
for k, line in enumerate(HOOK): d.text((x + w / 2, y + h * (0.32 + 0.38 * k)), line, fill=(20, 40, 70), font=f, anchor="mm")
card.save(out / "hook.png")
ins, fc = [], []
for i, (c, a, b) in enumerate(SHOTS):
    ins += ["-ss", str(a), "-t", f"{b - a:.3f}", "-i", f"clips/{c}.mp4"]
    fc.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,crop=iw/1.04:ih/1.04:(iw-iw/1.04)/2:(ih-ih/1.04)*0.4,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p[v{i}]")
n = len(SHOTS); ins += ["-i", str(out / "hook.png")]
fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.02:contrast=1.02[g];[g][{n}:v]overlay=0:0:enable='lt(t,{HOOK_UNTIL})'[v]")
raw = out / "zytrell_hofr_raw.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-threads", "4", str(raw)], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", str(raw), str(out / "zytrell_hofr.mp4")], check=True)
print("CUT_DONE", round(sum(b - a for _, a, b in SHOTS), 2))
