"""Free cut. Hand shots = Seedance clips, F = push-in on a still, C = push-in on the real listing crop (blurred-fill 9:16).
Hook text in Ralph's Classic caption style from frame 0 (2.6 s). If a clip is shorter than its VO window, the picture
cut moves into the neighbouring push-in shot (VO untouched): never a stretch or a freeze.
  python3 cut.py            -> out/<job>.mp4            (script v1: shots.json windows, vo/voiceover_tight.mp3)
  python3 cut.py N          -> out/<job>_v<N>.mp4       (variant N: vo/v<N>/windows.json, vo/v<N>/voiceover_tight.mp3)"""
import json, subprocess, os, sys, re
from pathlib import Path
from PIL import Image, ImageFilter
HERE = Path(__file__).resolve().parent; os.chdir(HERE)
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/ugc-product-ad/scripts"))
from classic_caption import classic_png
J = json.load(open("shots.json")); FPS = 24
N = sys.argv[1] if len(sys.argv) > 1 else None
if N:
    W = json.load(open(f"vo/v{N}/windows.json"))["windows"]; VO = f"vo/v{N}/voiceover_tight.mp3"
    HOOK = re.search(rf'## V{N}: on-screen "(.*?)"', Path("scripts_variants.md").read_text()).group(1); OUT = f"out/{J['product']}_v{N}.mp4"
else:
    W = [s["t"] for s in J["shots"]]; VO = "vo/voiceover_tight.mp3"; HOOK = J["hook_text"]; OUT = f"out/{J['product']}.mp4"
USABLE = J.get("usable", {}); OFFSET = J.get("offset", {})   # OFFSET: seconds skipped at a clip start          # seconds of a clip that pass QC (e.g. the label drifts after that)
tmp = Path(f"out/_seg{N or ''}"); tmp.mkdir(parents=True, exist_ok=True)
CROP_SRC = {"youtheory-ashwagandha": "refs/pouch_crop.png", "youtheory-turmeric": "refs/jar_crop.png",
            "neuro-sour-mints": "refs/flavors_crop.png", "penetrex-gel": "refs/bottle_crop.png"}[J["product"]]
S = J["shots"]; w = [list(x) for x in W]
def cliplen(s):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"clips/{s['id']}.mp4"], capture_output=True, text=True).stdout)
    return min(d, USABLE.get(s["id"], d)) - OFFSET.get(s["id"], 0) - 0.05
for k, s in enumerate(S):            # move overflow into a neighbouring push-in shot
    if s["kind"] in ("H", "N"):
        over = (w[k][1] - w[k][0]) - cliplen(s)
        if over > 0:
            if k + 1 < len(S) and S[k + 1]["kind"] in ("F", "C"): w[k][1] -= over; w[k + 1][0] -= over
            elif k > 0 and S[k - 1]["kind"] in ("F", "C"): w[k][0] += over; w[k - 1][1] += over
            else: sys.exit(f"{s['id']}: clip {cliplen(s):.2f}s shorter than window {w[k][1]-w[k][0]:.2f}s and no push-in neighbour")
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def compose(src, out):   # real listing crop as a card over a soft blur of this job's own kitchen (S1 still)
    from PIL import ImageEnhance, ImageDraw
    im = Image.open(src).convert("RGB")
    bg = Image.open("stills/S1.png").convert("RGB").resize((720, 1290)).crop((0, 5, 720, 1285)).filter(ImageFilter.GaussianBlur(28))
    bg = ImageEnhance.Brightness(bg).enhance(0.92)
    fg = im.resize((600, int(600 * im.height / im.width)), Image.LANCZOS)
    if fg.height > 1060: fg = im.resize((int(im.width * 1060 / im.height), 1060), Image.LANCZOS)
    x, y = (720 - fg.width) // 2, (1280 - fg.height) // 2
    sh = Image.new("L", (720, 1280), 0); ImageDraw.Draw(sh).rounded_rectangle((x + 6, y + 12, x + fg.width + 6, y + fg.height + 12), 24, fill=110)
    bg.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
    m = Image.new("L", fg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fg.width - 1, fg.height - 1), 24, fill=255)
    bg.paste(fg, (x, y), m); bg.save(out)
def push(sid, d, src, z1=1.10):
    n = int(round(d * FPS))
    vf = f"scale=2160:3840:flags=lanczos,zoompan=z='1.0+({z1}-1.0)*on/{n}':x='(iw-iw/zoom)*0.5':y='(ih-ih/zoom)*0.5':d={n}:s=720x1280:fps={FPS},setsar=1"
    run(["-loop", "1", "-i", src, "-vf", vf, "-frames:v", str(n), "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(tmp / f"{sid}.mp4")])
compose(CROP_SRC, "out/_crop.png")
for s, (a, b) in zip(S, w):
    d = round(b - a, 3)
    if s["kind"] in ("H", "N"):
        run(["-ss", str(OFFSET.get(s["id"], 0)), "-i", f"clips/{s['id']}.mp4", "-t", str(d), "-vf", f"fps={FPS},scale=720:1280,setsar=1", "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(tmp / f"{s['id']}.mp4")])
    elif s["kind"] == "F": push(s["id"], d, f"stills/{s['id']}.png")
    else: push(s["id"], d, "out/_crop.png", 1.12)
(tmp / "list.txt").write_text("".join(f"file '{s['id']}.mp4'\n" for s in S))
classic_png(HOOK, 720, 1280).save(tmp / "hook.png")
run(["-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-i", VO, "-i", str(tmp / "hook.png"),
     "-filter_complex", "[0:v][2:v]overlay=0:0:enable='between(t,0,2.6)'[v]", "-map", "[v]", "-map", "1:a",
     "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
     "-shortest", "-movflags", "+faststart", OUT])
print(OUT, {s["id"]: round(b - a, 2) for s, (a, b) in zip(S, w)}, "total", round(w[-1][1], 2))
