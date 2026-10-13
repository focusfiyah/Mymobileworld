"""Free cut: 9 hands-only clips on the trimmed Grace B voiceover, no text overlay (Ralph has not asked for one).

  python3 cut.py   -> out/night_driving_glasses_r1_raw.mp4 (720x1280, 24fps), then ai_finish.sh -> out/night_driving_glasses_r1.mp4

Windows come from shots.json (vo.py). Every shot is real clip footage at 1.0x (no holds, no Ken Burns).
S1: the clip darkens fast at ~3.1s as the oncoming car passes; a short white bloom (2.7-3.45s) covers it on "goes white".
"""
import json, subprocess
from pathlib import Path

J = json.loads(Path("shots.json").read_text())
inputs, chains, labels = [], [], []
for i, s in enumerate(J["shots"]):
    t0, t1 = s["t"]; win = t1 - t0; src = f"clips/{s['id']}.mp4"
    clip_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    assert win <= clip_len + 0.05, f"{s['id']} window {win:.2f}s needs more clip than {clip_len:.2f}s"
    inputs += ["-i", src]
    chains.append(f"[{i}:v]trim=start=0:duration={win:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[v{i}]")
    labels.append(f"[v{i}]")
n = len(J["shots"]); total = J["shots"][-1]["t"][1]
chains[0] = chains[0].replace("[v0]", "[b0]")
chains.append("color=white:s=720x1280:r=24:d=4.3,format=rgba,fade=t=in:st=2.7:d=0.38:alpha=1,fade=t=out:st=3.08:d=0.37:alpha=1[wh]")
chains.append("[b0][wh]overlay=shortest=1:format=auto[v0]")
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
chains.append("[c0]format=yuv420p[vout]")
inputs += ["-i", "vo/voiceover_tight.mp3"]
chains.append(f"[{n}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/night_driving_glasses_r1_raw.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads", "4",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out, total)
