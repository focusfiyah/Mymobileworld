"""Free cut: hand shots = Seedance clips, hand-free shots = slow push-ins (F: stills, C: real listing crops composed on a blurred
background). On-screen hook text in Ralph's Classic caption style from frame 0 (text = shots.json hook_text). VO = vo/voiceover_tight.mp3.
  python3 cut.py   -> out/<job>.mp4        Windows come from shots.json (VO word timings)."""
import json, subprocess, os, sys
from pathlib import Path
from PIL import Image, ImageFilter
HERE = Path(__file__).resolve().parent; os.chdir(HERE)
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/ugc-product-ad/scripts"))
from classic_caption import classic_png
J = json.load(open("shots.json")); FPS = 24
tmp = Path("out/_seg"); tmp.mkdir(parents=True, exist_ok=True)
CROPS = {s["id"]: s for s in J["shots"] if s["kind"] == "C"}
CROP_SRC = {"youtheory-ashwagandha": "refs/pouch_crop.png", "youtheory-turmeric": "refs/jar_crop.png",
            "neuro-sour-mints": "refs/flavors_crop.png", "penetrex-gel": "refs/bottle_crop.png"}[J["product"]]
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def dur(s): return round(s["t"][1] - s["t"][0], 3)
def compose(src, out):  # real crop centred on a blurred copy of itself, 720x1280
    im = Image.open(src).convert("RGB"); bg = im.resize((720, int(720 * im.height / im.width)), Image.LANCZOS)
    bg = bg.resize((int(1280 * im.width / im.height), 1280), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40)) if bg.height < 1280 else bg
    bg = bg.crop(((bg.width - 720) // 2, 0, (bg.width - 720) // 2 + 720, 1280))
    w = 640; fg = im.resize((w, int(w * im.height / im.width)), Image.LANCZOS)
    if fg.height > 1180: fg = fg.resize((int(fg.width * 1180 / fg.height), 1180), Image.LANCZOS)
    bg.paste(fg, ((720 - fg.width) // 2, (1280 - fg.height) // 2)); bg.save(out)
def push(s, src, z1=1.10):
    d = int(round(dur(s) * FPS))
    vf = (f"scale=2160:3840:flags=lanczos,zoompan=z='1.0+({z1}-1.0)*on/{d}':x='(iw-iw/zoom)*0.5':y='(ih-ih/zoom)*0.5':d={d}:s=720x1280:fps={FPS},setsar=1")
    run(["-loop", "1", "-i", src, "-vf", vf, "-frames:v", str(d), "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(tmp / f"{s['id']}.mp4")])
for s in J["shots"]:
    k = s["kind"]
    if k in ("H", "N"):
        run(["-i", f"clips/{s['id']}.mp4", "-t", str(dur(s)), "-vf", f"fps={FPS},scale=720:1280,setsar=1", "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(tmp / f"{s['id']}.mp4")])
    elif k == "F": push(s, f"stills/{s['id']}.png")
    else: compose(CROP_SRC, "out/_crop.png"); push(s, "out/_crop.png", 1.12)
(tmp / "list.txt").write_text("".join(f"file '{s['id']}.mp4'\n" for s in J["shots"]))
classic_png(J["hook_text"], 720, 1280).save("out/_hook.png")
total = J["shots"][-1]["t"][1]
run(["-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-i", "vo/voiceover_tight.mp3", "-i", "out/_hook.png",
     "-filter_complex", f"[0:v][2:v]overlay=0:0:enable='between(t,0,2.6)'[v]", "-map", "[v]", "-map", "1:a",
     "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
     "-shortest", "-movflags", "+faststart", f"out/{J['product']}.mp4"])
print({s["id"]: dur(s) for s in J["shots"]}, "total", round(total, 2))
