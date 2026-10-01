"""Free cut: 7 clips on the trimmed Grace B voiceover, real-photo label pop-ups, soft CC0 click on each pop-up.

  python3 cut.py   -> out/plant_therapy_top6.mp4 (720x1280, 24fps)

Windows come from shots.json (vo/words_trimmed.json). Label cards (inserts/*.png) are crops of Plant Therapy's own
product photo (refs/product_row_full.jpg), approved by Ralph 2026-10-01. SFX are CC0 (sfx/LICENSE.md).
"""
import json, subprocess
from pathlib import Path

J = json.loads(Path("shots.json").read_text())
CLIP_IN = {}                      # per-shot start offset into the clip, set after QC
CARDS = [("lavender", 2.62, 1.0), ("peppermint_eucalyptus", 4.06, 1.5),   # (card, start, duration): on the oil's name
         ("lemon", 6.66, 0.95), ("teatree", 7.74, 1.0)]

shots = J["shots"]
inputs, chains, labels = [], [], []
for i, s in enumerate(shots):
    t0, t1 = s["t"]
    inputs += ["-i", f"clips/{s['id']}.mp4"]
    chains.append(f"[{i}:v]trim=start={CLIP_IN.get(s['id'], 0)},setpts=PTS-STARTPTS,"
                  f"tpad=stop_mode=clone:stop_duration=1,trim=duration={t1 - t0:.3f},setpts=PTS-STARTPTS,"
                  f"scale=720:1280,setsar=1,fps=24[v{i}]")
    labels.append(f"[v{i}]")
n = len(shots); total = shots[-1]["t"][1]
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
for k, (name, st, d) in enumerate(CARDS):     # each card pops in with a short scale-up and fades out
    inputs += ["-loop", "1", "-t", f"{d + 0.2}", "-i", f"inserts/{name}.png"]
    j = n + k
    chains.append(f"[{j}:v]format=rgba,scale=w='720*min(1,0.9+t*0.8)':h=-1:eval=frame,"
                  f"fade=t=out:st={d - 0.15:.2f}:d=0.15:alpha=1,setpts=PTS-STARTPTS+{st}/TB[k{k}]")
    chains.append(f"[c{k}][k{k}]overlay=x=(W-w)/2:y=(H-h)/2:enable='between(t,{st},{st + d})':eof_action=pass[c{k + 1}]")
chains.append(f"[c{len(CARDS)}]format=yuv420p[vout]")
a = n + len(CARDS); click = a + 1
inputs += ["-i", "vo/voiceover_tight.mp3", "-i", "sfx/click.ogg"]
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
