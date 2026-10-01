"""Free cut: 7 clips on the trimmed Grace B voiceover (vo/voiceover_tight.mp3), hook text on S1, the box's own
"10% MORE" banner pop-up on S3, a soft CC0 click on each pop-up, a quiet shower-water bed under the shower shots.

  python3 cut.py   -> out/vicks_vaposhower.mp4 (720x1280, 24fps)

Windows come from shots.json (vo/words_trimmed.json). Overlays: inserts/hook.png (PIL), inserts/banner.png (crop of
Vicks' own packshot refs/box_front.png). SFX: sfx/click.ogg (CC0, see sfx/LICENSE.md); the water bed is ffmpeg noise.
"""
import json, subprocess
from pathlib import Path

J = json.loads(Path("shots.json").read_text())
# Each shot = pieces that fill its window. ("clip", file, start[, dur]) plays from start; the last piece fills what is
# left of the window (a clip that runs out freezes on its last frame). ("hold", png, dur, cx, cy, z) = still frame
# with a slow push-in toward (cx, cy) by zoom z.
PIECES = {
    "S5": [("clip", "clips/S5.mp4", 0.1)],   # 0.1-1.74s; two pale hands walk in at 2.2s
}
# (png, start, duration, y, click): pop in with a short scale-up, fade out
CARDS = [("hook", 0.15, 2.9, 170, False),
         ("banner", 9.80, 1.6, 860, True)]   # "ten percent more" starts at 9.87s
WATER = (12.44, 16.64)   # S4 + S5: tablet in the shower stream

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
            chains.append(f"[{j}:v]trim=start={p[2]},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=2,"
                          f"trim=duration={d:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[p{i}_{k}]")
        else:
            d = left if last else p[2]; nf = int(round(d * 24)) + 1
            j = add(["-i", p[1]])
            chains.append(f"[{j}:v]scale=1440:2560,zoompan=z='1+{p[5]}*on/{nf}':x='iw*{p[3]}-iw/zoom*{p[3]}':"
                          f"y='ih*{p[4]}-ih/zoom*{p[4]}':d={nf}:s=720x1280:fps=24,trim=duration={d:.3f},"
                          f"setpts=PTS-STARTPTS,setsar=1[p{i}_{k}]")
        left -= d; plabels.append(f"[p{i}_{k}]")
    chains.append(f"{''.join(plabels)}concat=n={len(plabels)}:v=1:a=0[v{i}]")
    labels.append(f"[v{i}]")
total = shots[-1]["t"][1]
chains.append(f"{''.join(labels)}concat=n={len(shots)}:v=1:a=0[c0]")
for k, (name, st, d, y, _) in enumerate(CARDS):
    j = add(["-loop", "1", "-t", f"{d + 0.2}", "-i", f"inserts/{name}.png"])
    chains.append(f"[{j}:v]format=rgba,scale=w='iw*min(1,0.9+t*0.8)':h=-1:eval=frame,"
                  f"fade=t=out:st={d - 0.15:.2f}:d=0.15:alpha=1,setpts=PTS-STARTPTS+{st}/TB[k{k}]")
    chains.append(f"[c{k}][k{k}]overlay=x=(W-w)/2:y={y}:enable='between(t,{st},{st + d})':eof_action=pass[c{k + 1}]")
chains.append(f"[c{len(CARDS)}]format=yuv420p[vout]")

a = add(["-i", "vo/voiceover_tight.mp3"]); click = add(["-i", "sfx/click.ogg"])
pops = [st for (_, st, _, _, c) in CARDS if c]
w0, w1 = WATER
sfx = [f"[{click}:a]asplit={len(pops)}" + "".join(f"[t{k}]" for k in range(len(pops)))]
sfx += [f"[t{k}]volume=0.25,adelay={int(st * 1000)}:all=1[d{k}]" for k, st in enumerate(pops)]
sfx.append(f"anoisesrc=color=pink:amplitude=0.5:duration={w1 - w0:.2f}:sample_rate=44100,highpass=f=500,lowpass=f=7000,"
           f"volume=0.05,afade=t=in:d=0.3,afade=t=out:st={w1 - w0 - 0.4:.2f}:d=0.4,"
           f"adelay={int(w0 * 1000)}:all=1[wb]")
sfx.append(f"[{a}:a]" + "".join(f"[d{k}]" for k in range(len(pops))) + "[wb]" +
           f"amix=inputs={len(pops) + 2}:normalize=0:duration=first,apad,atrim=duration={total},"
           f"loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/vicks_vaposhower.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + sfx),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out)
