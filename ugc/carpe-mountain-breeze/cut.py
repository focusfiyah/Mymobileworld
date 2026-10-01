"""Free cut: the 9 clips timed to the Grace B voiceover, a whip-pan into S1, soft CC0 SFX.

  python3 cut.py   -> out/carpe_mountain_breeze.mp4 (720x1280, 24fps)

Shot windows come from shots.json (word timings of the trimmed voiceover). IN = where each clip starts being used;
S1 is slowed to fill its 6.2s window. SFX are CC0 (Kenney, sfx/LICENSE.md); the whoosh is generated noise.
"""
import json, subprocess
from pathlib import Path

J = json.loads(Path("shots.json").read_text())
IN = {"S3": 2.3, "S4": 0.3, "V4": 0.3, "V5": 0.5}   # skip lead-ins so the action lands on the words
WHIP_AT, WHIP = 9.96, 0.24                          # whip-pan V2 -> S1, centred on the cut
TICKS = [19.95, 20.3, 20.65, 21.0]                   # knob turns in S3
CAP = 22.95                                          # cap pops off in V4

shots = J["shots"]
end = shots[-1]["t"][1]
inputs, chains = [], []
for i, s in enumerate(shots):
    t0, t1 = s["t"]
    # pad half the whip on each side of the cut so the crossfade does not shift anything after it
    if s["id"] == "V2":
        t1 += WHIP / 2
    if s["id"] == "S1":
        t0 -= WHIP / 2
    dur = t1 - t0
    clip_len = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                              "-of", "csv=p=0", f"clips/{s['id']}.mp4"]))
    speed = max(1.0, dur / (clip_len - IN.get(s["id"], 0)))  # slow a clip that is shorter than its window
    inputs += ["-i", f"clips/{s['id']}.mp4"]
    chains.append(f"[{i}:v]trim=start={IN.get(s['id'], 0)},setpts=(PTS-STARTPTS)*{speed:.4f},"
                  f"tpad=stop_mode=clone:stop_duration=1,trim=duration={dur:.3f},setpts=PTS-STARTPTS,"
                  f"scale=720:1280,setsar=1,fps=24[v{i}]")
k = next(i for i, s in enumerate(shots) if s["id"] == "S1")
n = len(shots)
chains.append("".join(f"[v{i}]" for i in range(k)) + f"concat=n={k}:v=1:a=0[a]")
chains.append("".join(f"[v{i}]" for i in range(k, n)) + f"concat=n={n - k}:v=1:a=0[b]")
a_len = WHIP_AT + WHIP / 2
chains.append(f"[a][b]xfade=transition=slideleft:duration={WHIP}:offset={a_len - WHIP:.3f},"
              f"dblur=angle=0:radius=60:enable='between(t,{WHIP_AT - WHIP / 2 - 0.04:.3f},{WHIP_AT + WHIP / 2 + 0.04:.3f})',"
              f"format=yuv420p[vout]")
# audio: voiceover + whoosh + knob ticks + cap pop
vo = n
inputs += ["-i", "vo/voiceover.mp3", "-i", "sfx/tick.ogg", "-i", "sfx/click.ogg",
           "-f", "lavfi", "-t", "0.35", "-i", "anoisesrc=color=pink:amplitude=0.6"]
tick, click, noise = n + 1, n + 2, n + 3
sfx = [f"[{noise}:a]highpass=f=900,lowpass=f=6000,afade=t=in:d=0.15,afade=t=out:st=0.17:d=0.18,volume=0.35,"
       f"adelay={int((WHIP_AT - 0.2) * 1000)}:all=1[wh]",
       f"[{tick}:a]asplit={len(TICKS)}" + "".join(f"[t{j}]" for j in range(len(TICKS)))]
for j, t in enumerate(TICKS):
    sfx.append(f"[t{j}]volume=0.25,adelay={int(t * 1000)}:all=1[d{j}]")
sfx.append(f"[{click}:a]volume=0.35,adelay={int(CAP * 1000)}:all=1[cap]")
mix = f"[{vo}:a][wh]" + "".join(f"[d{j}]" for j in range(len(TICKS))) + "[cap]"
sfx.append(f"{mix}amix=inputs={len(TICKS) + 3}:normalize=0:duration=first,apad,atrim=duration={end},"
           f"loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + sfx),
                "-map", "[vout]", "-map", "[aout]", "-t", f"{end}", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "out/carpe_mountain_breeze.mp4"], check=True)
print("out/carpe_mountain_breeze.mp4")
