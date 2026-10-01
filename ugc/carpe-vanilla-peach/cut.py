"""Free rough cut: the 9 clips cut to the Grace B voiceover, a badge close-up insert, soft CC0 SFX.

  python3 cut.py   -> out/carpe_vanilla_peach_roughcut.mp4 (720x1280, 24fps)

Cut points are the shot windows in shots.json (from the voiceover's word timings). SFX are CC0 (Kenney), copied
from focusfiyah/Dayone-ai assets/sfx (see sfx/LICENSE.md).
"""
import json, subprocess
from pathlib import Path

J = json.loads(Path("shots.json").read_text())
CLIP_IN = {"S9": 1.4}            # S9: skip setting the stick down so the cap tap lands on "linked"
END = {"S9": 36.6}               # hold S9 past "below" so the point-down reads
BADGE = (25.95, 0.8)             # badge close-up over "a hundred hours" (26.02-26.90)
TICKS = [8.25, 8.65, 9.05, 9.45, 9.85, 10.25]   # knob turns in S3
TAP = 35.0                       # finger taps the cap in S9

shots = J["shots"]
inputs, chains, labels = [], [], []
for i, s in enumerate(shots):
    t0, t1 = s["t"][0], END.get(s["id"], s["t"][1])
    dur = t1 - t0
    inputs += ["-i", f"clips/{s['id']}.mp4"]
    chains.append(f"[{i}:v]trim=start={CLIP_IN.get(s['id'], 0)},setpts=PTS-STARTPTS,"
                  f"tpad=stop_mode=clone:stop_duration=1,trim=duration={dur:.3f},setpts=PTS-STARTPTS,"
                  f"scale=720:1280,setsar=1,fps=24[v{i}]")
    labels.append(f"[v{i}]")
n = len(shots)
total = END.get(shots[-1]["id"], shots[-1]["t"][1])
# badge close-up: 9:16 crop of the S7 still around the 100hr shield, slow push-in
inputs += ["-loop", "1", "-t", str(BADGE[1] + 0.1), "-i", "stills/S7.png"]
b = n
chains.append(f"[{b}:v]crop=270:480:353:350,scale=1440:2560,zoompan=z='1+0.003*on':x='iw/2-(iw/zoom/2)':"
              f"y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=24,trim=duration={BADGE[1]},"
              f"setpts=PTS-STARTPTS+{BADGE[0]}/TB[badge]")
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[cat]")
chains.append(f"[cat][badge]overlay=enable='between(t,{BADGE[0]},{BADGE[0] + BADGE[1]})':eof_action=pass,format=yuv420p[vout]")
# audio: voiceover + ticks + tap
inputs += ["-i", "vo/voiceover.mp3"]
a = n + 1
inputs += ["-i", "sfx/tick.ogg", "-i", "sfx/click.ogg"]
tick, click = n + 2, n + 3
sfx = [f"[{tick}:a]asplit={len(TICKS)}" + "".join(f"[t{k}]" for k in range(len(TICKS)))]
for k, t in enumerate(TICKS):
    sfx.append(f"[t{k}]volume=0.25,adelay={int(t * 1000)}:all=1[d{k}]")
sfx.append(f"[{click}:a]volume=0.35,adelay={int(TAP * 1000)}:all=1[tap]")
mix = f"[{a}:a]" + "".join(f"[d{k}]" for k in range(len(TICKS))) + "[tap]"
sfx.append(f"{mix}amix=inputs={len(TICKS) + 2}:normalize=0:duration=first,apad,atrim=duration={total},"
           f"loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/carpe_vanilla_peach_roughcut.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + sfx),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out)
