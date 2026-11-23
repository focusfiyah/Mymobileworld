"""HofR BF cut from a shots.json (copied from bf-novatabz/cut.py, Ralph 2026-11-12): Ralph's Chatterbox VO (vo/ralph.wav),
Grace's silent CURRENT V1 cut in a new order and framing, optional Pexels holiday b-roll, hook text card from frame 0,
no captions, no AI finish (Grace's footage is real). Every clip 1.0x; each shot starts at its line's first word + off.
  python3 cut.py JOB [--final]   (run in houseoframeau/posts) -> JOB/out/bf_<job>.mp4 (review preset veryfast; --final medium)
shots.json: {"hook": "line1|line2", "hook_y": 380, "seg": [[src, in_s, line, off_s, "w:h:x:y" crop of 1080x1920 or null], ...]}"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
J = Path(sys.argv[1]); final = "--final" in sys.argv; name = J.name[3:]
S = json.loads((J / "shots.json").read_text()); W = json.loads((J / "vo/words.json").read_text())
END = round(W["total"] + 0.6, 3)
(J / "out").mkdir(exist_ok=True)
T = [W["lines"][l]["start"] + off for _, _, l, off, _ in S["seg"]]
assert T[0] == 0 and T == sorted(T), T
ins, ch = [], []
for i, (src, ss, l, off, crop) in enumerate(S["seg"]):
    d = (T[i + 1] if i + 1 < len(T) else END) - T[i]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True, cwd=J).stdout)
    assert ss + d <= dur + 0.01, f"{src} needs {ss + d:.2f} s from {ss}, has {dur:.2f} (never stretch)"
    assert d >= 0.8, f"shot {i} only {d:.2f} s"
    ins += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", src]
    c = f",crop={crop},scale=1080:1920:flags=lanczos" if crop else ""
    ch.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920{c},fps=30,format=yuv420p,setsar=1[v{i}]")
n = len(S["seg"])
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 60)
hl = S["hook"].split("|"); y0 = S["hook_y"]; h = 100 + 80 * (len(hl) - 1) + 40
dr.rounded_rectangle((80, y0, 920, y0 + h), radius=36, fill=(255, 255, 255, 240))
for k, line in enumerate(hl): dr.text((500, y0 + 70 + k * 80), line, fill=(20, 40, 70), font=f, anchor="mm"); bb = dr.textbbox((500, y0 + 70 + k * 80), line, font=f, anchor="mm"); assert bb[0] >= 100 and bb[2] <= 900, (line, bb)
card.save(J / "out/hook.png")
json.dump({"box": f"80,{y0},840,{h}"}, open(J / "out/hookbox.json", "w"))
hold = max(T[1] if n > 1 else END, 2.5)
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.015:contrast=1.02[g];" \
     f"[g][{n + 1}:v]overlay=0:0:enable='lt(t,{hold:.3f})'[v];[{n}:a]loudnorm=I=-14.5:TP=-1.5:LRA=11,apad,atrim=0:{END}[a]"
out = J / f"out/bf_{name}.mp4"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", "vo/ralph.wav", "-i", "out/hook.png", "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-t", f"{END}", "-c:v", "libx264", "-preset", "medium" if final else "veryfast",
                "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", str(out.relative_to(J))], check=True, cwd=J)
print("CUT", out, END, "s", "hook held", hold)
