"""Free cut: an edit list of clip pieces laid end to end under the Grace B voiceover, a whip-pan into S1, CC0 SFX.

  python3 cut.py   -> out/carpe_mountain_breeze.mp4 (720x1280, 24fps)

Nothing is slowed down (Ralph 2026-10-01: "why is the whole video in slow motion"). Clips play at 1.0x or faster;
the walking selfie (V1) is cut (Ralph): the hook is the S1 close-up pull-back, and "This is Carpe…" is the S1a
hero close-up plus spare S3/S4 product moments. Shots after V4 shift by up to 0.4s. V5 stops before Seedance added
the deodorant. SFX are CC0 (Kenney, sfx/LICENSE.md); the whoosh is generated noise.
"""
import subprocess
from pathlib import Path

# (source, in, length used from the source, speed, extra video filter); output length = length / speed
EDL = [
    ("clips/S1.mp4", 0.0, 4.13, 1.0, ""),                               # hook: close-up on the stick, pull back to her
    ("clips/V2.mp4", 0.0, 5.83, 1.0, ""),
    ("S1a", 0.0, 3.2, 1.0, ""),                                          # hero close-up, slow push-in, label sharp
    ("clips/S3.mp4", 0.0, 2.1, 1.0, ""),                                 # holding the stick before the twist
    ("clips/S4.mp4", 3.15, 0.89, 1.0, ""),                               # stick upright, label to camera
    ("clips/S2.mp4", 0.0, 4.0, 1.1, ""),
    ("clips/S3.mp4", 2.1, 1.645, 1.15, ""),
    ("clips/S4.mp4", 0.3, 1.725, 1.15, ""),
    ("clips/V4.mp4", 0.3, 4.74, 1.0, ""),
    ("clips/V5.mp4", 0.0, 3.35, 1.0, ""),
    ("clips/S10.mp4", 0.0, 4.04, 1.0, ""),
]
END = 35.03                                          # voiceover length; S10 holds its last frame to here
WHIP_AT, WHIP = 9.96, 0.24                           # whip-pan V2 -> S1a, centred on the cut
TICKS = [19.95, 20.3, 20.65, 21.0]                   # knob turns in S3
CAP = 22.95                                          # cap pops off in V4
WHIP_INTO = 2                                        # EDL index the whip-pan lands on (V2 -> hero close-up)

inputs, chains, t = [], [], 0.0
for i, (src, t_in, length, speed, vf) in enumerate(EDL):
    out_len = length / speed
    if i == WHIP_INTO - 1:
        out_len += WHIP / 2                          # pad both sides of the whip so the crossfade shifts nothing
    if i == WHIP_INTO:
        out_len += WHIP / 2
    if i == len(EDL) - 1:
        out_len = END - t
    if src == "S1a":
        frames = int(round(out_len * 24))
        inputs += ["-loop", "1", "-framerate", "24", "-t", f"{out_len + 0.1:.3f}", "-i", "stills/S1a.png"]
        chains.append(f"[{i}:v]scale=1440:2560,zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':"
                      f"y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=24,trim=duration={out_len:.3f},setpts=PTS-STARTPTS,"
                      f"setsar=1[v{i}]")
    else:
        inputs += ["-i", src]
        chains.append(f"[{i}:v]trim=start={t_in}:end={t_in + length:.3f},setpts=(PTS-STARTPTS)/{speed},{vf}"
                      f"scale=720:1280,setsar=1,fps=24,tpad=stop_mode=clone:stop_duration=2,"
                      f"trim=duration={out_len:.3f},setpts=PTS-STARTPTS[v{i}]")
    t += out_len - (WHIP if i == WHIP_INTO else 0)
n = len(EDL)
chains.append("".join(f"[v{i}]" for i in range(WHIP_INTO)) + f"concat=n={WHIP_INTO}:v=1:a=0[a]")
chains.append("".join(f"[v{i}]" for i in range(WHIP_INTO, n)) + f"concat=n={n - WHIP_INTO}:v=1:a=0[b]")
chains.append(f"[a][b]xfade=transition=slideleft:duration={WHIP}:offset={WHIP_AT - WHIP / 2:.3f},"
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
for j, tt in enumerate(TICKS):
    sfx.append(f"[t{j}]volume=0.25,adelay={int(tt * 1000)}:all=1[d{j}]")
sfx.append(f"[{click}:a]volume=0.35,adelay={int(CAP * 1000)}:all=1[cap]")
mix = f"[{vo}:a][wh]" + "".join(f"[d{j}]" for j in range(len(TICKS))) + "[cap]"
sfx.append(f"{mix}amix=inputs={len(TICKS) + 3}:normalize=0:duration=first,apad,atrim=duration={END},"
           f"loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains + sfx),
                "-map", "[vout]", "-map", "[aout]", "-t", f"{END}", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
                "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "out/carpe_mountain_breeze.mp4"], check=True)
print("out/carpe_mountain_breeze.mp4")
