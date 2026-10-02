"""Free cut: 7 hands-only clips on the trimmed Grace B voiceover, classic hook caption on S1, real-box banner pop-up on S3.

  python3 cut.py   -> out/vicks_vaposhower.mp4 (720x1280, 24fps)

Windows come from shots.json (vo/words_trimmed.json). The banner (inserts/banner.png) is a crop of the real box front
(refs/box_front.png). Hook caption = Ralph's classic style (ugc-product-ad/scripts/classic_caption.py) + the 🚿 emoji
from Noto Color Emoji. SFX are CC0 (sfx/LICENSE.md).
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/ugc-product-ad/scripts"))
from classic_caption import classic_png

J = json.loads(Path("shots.json").read_text())
# Each shot = pieces that fill its window. ("clip", file, start[, dur]) plays from start; ("hold", png, dur, cx, cy, z) is
# a still frame with a slow push-in toward (cx, cy) by zoom z. The last piece fills whatever is left of the window.
PIECES = {
    "S1": [("clip", "clips_b/S1.mp4", 0.0)],                    # old session's S1: box stays front-on (ours turns it)
    "S5": [("clip", "clips/S5.mp4", 0.1)],                       # 0.1-1.74s; two pale hands walk in at 2.2s
}
HOOK = ("the only 10 min|you get to yourself", "🚿", 0.0, 2.6)   # (text, "|" = line break, emoji, start, end)
BANNER = ("inserts/banner.png", 9.87, 1.2)                       # on "ten percent more"
SFX = [("click", 9.87, 0.25)]                                    # (sfx/<name>.ogg, start, volume)


def hook_png(text, emoji, out, w=720, h=1280):
    img = classic_png(text, w, h)
    if emoji:                                                    # Noto Color Emoji is a 136px bitmap font: draw, scale
        from PIL import ImageDraw, ImageFont
        f = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109)
        e = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(e).text((80, 80), emoji, font=f, embedded_color=True, anchor="mm")
        k = w / 1080; size = round(48 * k); rows = text.split("|")   # same metrics as classic_png
        e = e.crop(e.getbbox()); e = e.resize((size, round(size * e.height / e.width)))
        tf = ImageFont.truetype(str(ROOT / ".claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf"), size)
        x = round(w / 2 + tf.getlength(rows[-1]) / 2 + 8 * k)
        yc = round(300 * k) + (len(rows) - 1) * int(size * 1.25)   # centre of the last row
        img.alpha_composite(e, (x, yc - e.height // 2))
    img.save(out); return out


Path("inserts").mkdir(exist_ok=True)
hook = hook_png(HOOK[0], HOOK[1], "inserts/hook_text.png")
shots = J["shots"]
inputs, chains, labels = [], [], []
def add(args):
    inputs.extend(args); return sum(1 for x in inputs if x == "-i") - 1
for i, s in enumerate(shots):
    win = s["t"][1] - s["t"][0]
    parts = PIECES.get(s["id"], [("clip", f"clips/{s['id']}.mp4", 0.0)])
    plabels, left = [], win
    for k, p in enumerate(parts):
        last = k == len(parts) - 1
        if p[0] == "clip":
            d = left if last else p[3]
            j = add(["-i", p[1]])
            chains.append(f"[{j}:v]trim=start={p[2]},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1,"
                          f"trim=duration={d:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[p{i}_{k}]")
        else:
            d = left; nf = int(round(d * 24)) + 1
            j = add(["-i", p[1]])
            chains.append(f"[{j}:v]scale=1440:2560,zoompan=z='1+{p[5]}*on/{nf}':x='iw*{p[3]}-iw/zoom*{p[3]}':"
                          f"y='ih*{p[4]}-ih/zoom*{p[4]}':d={nf}:s=720x1280:fps=24,trim=duration={d:.3f},"
                          f"setpts=PTS-STARTPTS,setsar=1[p{i}_{k}]")
        left -= d; plabels.append(f"[p{i}_{k}]")
    chains.append(f"{''.join(plabels)}concat=n={len(plabels)}:v=1:a=0[v{i}]")
    labels.append(f"[v{i}]")
n = len(shots); total = shots[-1]["t"][1]
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
# banner pops in with a short scale-up, sits in the upper third (the tablet is mid-frame), fades out
png, st, d = BANNER
j = add(["-loop", "1", "-t", f"{d + 0.2}", "-i", png])
chains.append(f"[{j}:v]format=rgba,scale=w='600*min(1,0.9+t*0.8)':h=-1:eval=frame,"
              f"fade=t=out:st={d - 0.15:.2f}:d=0.15:alpha=1,setpts=PTS-STARTPTS+{st}/TB[bn]")
chains.append(f"[c0][bn]overlay=x=(W-w)/2:y=300-h/2:enable='between(t,{st},{st + d})':eof_action=pass[c1]")
j = add(["-loop", "1", "-t", f"{HOOK[3] + 0.1}", "-i", hook])
chains.append(f"[{j}:v]format=rgba,fade=t=out:st={HOOK[3] - 0.15:.2f}:d=0.15:alpha=1[hook]")
chains.append(f"[c1][hook]overlay=0:0:enable='between(t,{HOOK[2]},{HOOK[3]})':eof_action=pass,format=yuv420p[vout]")
a = add(["-i", "vo/voiceover_tight.mp3"])
mix = []
for k, (name, st, vol) in enumerate(SFX):
    j = add(["-i", f"sfx/{name}.ogg"])
    chains.append(f"[{j}:a]volume={vol},adelay={int(st * 1000)}:all=1[d{k}]"); mix.append(f"[d{k}]")
chains.append(f"[{a}:a]{''.join(mix)}amix=inputs={len(mix) + 1}:normalize=0:duration=first,apad,atrim=duration={total},"
              f"loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/vicks_vaposhower.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out)
