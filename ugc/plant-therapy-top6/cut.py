"""Free cut: 7 clips on the trimmed Grace B voiceover, real-photo label pop-ups, soft CC0 click on each pop-up.

  python3 cut.py   -> out/plant_therapy_top6.mp4 (720x1280, 24fps)

Windows come from shots.json (vo/words_trimmed.json). Label cards (inserts/*.png) are crops of Plant Therapy's own
product photo (refs/product_row_full.jpg), approved by Ralph 2026-10-01. SFX are CC0 (sfx/LICENSE.md).
"""
import json, subprocess
from pathlib import Path

J = json.loads(Path("shots.json").read_text())
# Each shot = pieces that fill its window. ("clip", file, start) plays from start; ("hold", png, dur, cx, cy, z) is a still
# frame with a slow push-in toward (cx, cy) by zoom z. The last piece fills whatever is left of the window.
PIECES = {
    "S5": [("clip", "clips/S5.mp4", 0.2)],                       # 0.2-1.84s; at 2.6s the bottle turns up and its label drifts
    "S6": [("clip", "clips/S6.mp4", 0.0, 1.40),                  # drops; at 1.5s a cap appears on the open bottle
           ("hold", "frames/S6_hold.png", None, 0.35, 0.65, 0.12)],    # push in on the dish of carrier oil
    "S7": [("clip", "clips/S1.mp4", 2.55, 1.45),                 # continues the hook: hand sweeps the six bottles + box
           ("hold", "frames/S1_end.png", None, 0.30, 0.62, 0.30)],     # S7 clip itself drew 8 bottles and lost the box
}
CARDS = [("lavender", 2.62, 1.0), ("peppermint_eucalyptus", 4.06, 1.5),   # (card, start, duration): on the oil's name
         ("lemon", 6.66, 0.95), ("teatree", 7.74, 1.0)]

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
for k, (name, st, d) in enumerate(CARDS):     # each card pops in with a short scale-up and fades out
    j = add(["-loop", "1", "-t", f"{d + 0.2}", "-i", f"inserts/{name}.png"])
    chains.append(f"[{j}:v]format=rgba,scale=w='720*min(1,0.9+t*0.8)':h=-1:eval=frame,"
                  f"fade=t=out:st={d - 0.15:.2f}:d=0.15:alpha=1,setpts=PTS-STARTPTS+{st}/TB[k{k}]")
    chains.append(f"[c{k}][k{k}]overlay=x=(W-w)/2:y=(H-h)/2:enable='between(t,{st},{st + d})':eof_action=pass[c{k + 1}]")
chains.append(f"[c{len(CARDS)}]format=yuv420p[vout]")
a = add(["-i", "vo/voiceover_tight.mp3"]); click = add(["-i", "sfx/click.ogg"])
sfx = [f"[{click}:a]asplit={len(CARDS)}" + "".join(f"[t{k}]" for k in range(len(CARDS)))]
for k, (_, st, _) in enumerate(CARDS):
    sfx.append(f"[t{k}]volume=0.25,adelay={int(st * 1000)}:all=1[d{k}]")
sfx.append(f"[{a}:a]" + "".join(f"[d{k}]" for k in range(len(CARDS))) +
           f"amix=inputs={len(CARDS) + 1}:normalize=0:duration=first,apad,atrim=duration={total},"
           f"loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/plant_therapy_top6.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + sfx),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out)
