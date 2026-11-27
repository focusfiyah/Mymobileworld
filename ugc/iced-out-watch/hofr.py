"""HofR Black Friday cut of the Men's Iced Out Watch (Ralph 2026-11-27, relayed by the HofR BF session: "create a House of
Rameau version for that and use my voice with Chatterbox"). Grace's real footage (orig/a.mov, one 43 s take, no talking),
own order, punch-in per shot, hook card from frame 0, no captions, Ralph's Chatterbox VO at 1.08x. Real footage: no ai_finish."""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
T = 1.08
SRC = [27.0, 19.3, 6.9, 2.4, 35.4, 23.6, 39.72, 15.0, 33.0]   # a.mov start per VO line, picked by line, no overlap (hofr/SHOTS.md)
ZOOM = [1.04, 1.08, 1.02, 1.10, 1.04, 1.06, 1.03, 1.08, 1.05]
L = json.load(open("hofr/vo/words.json"))["lines"]
DUR = [((L[i + 1]["start"] if i + 1 < len(L) else L[i]["end"] + 0.5) - L[i]["start"]) / T for i in range(len(L))]
DUR[0] += 0.1  # adelay
HOOK = ["When he's impossible", "to shop for"]; BOX = (130, 400, 800, 190); HOOK_UNTIL = 3.0
out = Path("out/hofr"); out.mkdir(parents=True, exist_ok=True)
x, y, w, h = BOX; card = Image.new("RGBA", (1080, 1920)); d = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 60)
d.rounded_rectangle((x, y, x + w, y + h), radius=36, fill=(255, 255, 255, 242))
for k, line in enumerate(HOOK): d.text((x + w / 2, y + h * (0.31 + 0.38 * k)), line, fill=(20, 40, 70), font=f, anchor="mm")
card.save(out / "hook.png")
ins, fc = [], []
for i, (a, z) in enumerate(zip(SRC, ZOOM)):
    ins += ["-ss", str(a), "-t", f"{DUR[i]:.3f}", "-i", "orig/a.mov"]
    fc.append(f"[{i}:v]fps=30,crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})*0.45,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p[v{i}]")
n = len(SRC); ins += ["-i", str(out / "hook.png"), "-i", "hofr/vo/ralph.wav"]
fc.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.03:contrast=1.03:saturation=0.97[g];[g][{n}:v]overlay=0:0:enable='lt(t,{HOOK_UNTIL})'[v]")
fc.append(f"[{n+1}:a]atempo={T},adelay=100|100,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
tot = sum(DUR)
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{tot:.3f}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                "-movflags", "+faststart", str(out / "watch_hofr_v1.mp4")], check=True)
print("CUT_DONE", round(tot, 2), [round(x, 2) for x in DUR])
