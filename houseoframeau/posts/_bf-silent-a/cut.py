"""Generic HofR Black Friday cut for one post (Ralph's VO over Grace's approved silent edit + free holiday b-roll).
  python3 cut.py POST   -> POST/out/bf_<name>.mp4 (veryfast review encode at crf 17 is the final: real footage, no AI finish)
POST/post.json: hook_text ("line|line"), hook_box "x,y,w,h" (card area), grade (ffmpeg eq/colorbalance chain),
segs: [{"src": "G" (Grace cut in /tmp/claude-0/src/<name>.mp4) or "broll/x.mp4", "in": s, "at": line n or seconds,
        "off": s added to the line start, "crop": "w:h:x:y" of the 1080x1920 frame, "max": last usable second in src}].
Each seg runs to the next seg's start; the last one to the VO end + tail. Every clip plays at 1.0x (asserted, never stretched)."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
post = Path(sys.argv[1]).resolve(); name = post.name.replace("bf-", "")
cfg = json.loads((post / "post.json").read_text()); tim = json.loads((post / "vo/timing.json").read_text())
END = round(tim[-1]["end"] + cfg.get("tail", 0.45), 3)
def at(s):
    t = s["at"]; return round((tim[t]["start"] if isinstance(t, int) else t) + s.get("off", 0.0), 3)
segs = cfg["segs"]; starts = [at(s) for s in segs]; assert starts[0] == 0.0 and starts == sorted(starts), starts
(post / "out").mkdir(exist_ok=True); ins, ch = [], []
for i, s in enumerate(segs):
    src = f"/tmp/claude-0/src/{name}.mp4" if s["src"] == "G" else str(post / s["src"])
    d = round((starts[i + 1] if i + 1 < len(segs) else END) - starts[i], 3)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    lim = min(dur, s.get("max", dur))
    assert s["in"] + d <= lim + 0.02, f"seg {i} {s['src']} needs {s['in']}+{d:.2f} > {lim:.2f} (never stretch)"
    ins += ["-ss", f"{s['in']:.3f}", "-t", f"{d:.3f}", "-i", src]
    crop = s.get("crop", "1080:1920:0:0")
    ch.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop={crop},"
              f"scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setsar=1[v{i}]")
n = len(segs)
x, y, w, h = map(int, cfg["hook_box"].split(",")); hl = cfg["hook_text"].split("|")
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
f = ImageFont.truetype(str(Path(__file__).resolve().parents[3] / ".claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf"), cfg.get("font", 58))
dr.rounded_rectangle((x, y, x + w, y + h), radius=36, fill=(255, 255, 255, 242))
lh = h / (len(hl) + 0.6)
for k, line in enumerate(hl): dr.text((x + w / 2, y + lh * (k + 0.8)), line, fill=(cfg.get("ink", [20, 40, 70])[0], cfg.get("ink", [20, 40, 70])[1], cfg.get("ink", [20, 40, 70])[2]), font=f, anchor="mm")
card.save(post / "out/hook.png")
hook_end = cfg.get("hook_until", max(2.5, tim[1]["start"])); assert hook_end >= 2.0
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,{cfg.get('grade', 'null')}[g];" \
     f"[g][{n + 1}:v]overlay=0:0:enable='lt(t,{hook_end})'[v];[{n}:a]loudnorm=I=-14.5:TP=-1.5:LRA=11,apad,atrim=0:{END}[a]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", str(post / "vo/ralph.wav"), "-i", str(post / "out/hook.png"), "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-t", f"{END}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", str(post / f"out/bf_{name}.mp4")], check=True)
print("CUT_DONE", post / f"out/bf_{name}.mp4", END, "s", "starts", starts)
