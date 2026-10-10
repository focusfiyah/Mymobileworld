"""Free cut v3: 8 hands-only clips on the trimmed Grace B voiceover, no text overlay (default; Ralph has not asked for one).

  python3 cut.py   -> out/thunderfit_ring_v4.mp4 (720x1280, 24fps)

Every shot is real clip footage at 1.0x (no holds, no speed changes). Windows follow the voiceover (shots.json), so picture and words match.
S1 = blue ring on the bench from frame 0, bare hand (Ralph 2026-10-08); S2 = bare hand (no heart ring); S4 skips its first 1.4 s (ring never goes onto a ringed finger).
"""
import json, subprocess
from pathlib import Path

SEGS = [["S1", 0.0, 4.04], ["S2", 0.0, 4.44], ["S3", 0.0, 4.94], ["S4", 1.4, 3.6], ["S5", 0.3, 3.6], ["S6", 0.0, 2.55], ["S7", 0.0, 4.04], ["S8", 0.0, 7.59]]
VO = "vo/voiceover_tight.mp3"
total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VO],
                             capture_output=True, text=True).stdout)
inputs, chains, labels = [], [], []
for i, (sid, st, d) in enumerate(SEGS):
    cl = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"clips/{sid}.mp4"],
                              capture_output=True, text=True).stdout)
    assert st + d <= cl + 0.05, f"{sid}: needs {st + d:.2f}s of a {cl:.2f}s clip"
    inputs += ["-i", f"clips/{sid}.mp4"]
    chains.append(f"[{i}:v]trim=start={st}:duration={d},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[v{i}]")
    labels.append(f"[v{i}]")
n = len(SEGS)
assert abs(sum(d for _, _, d in SEGS) - total) < 0.1, "segments must add up to the voiceover length"
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0,format=yuv420p[vout]")
inputs += ["-i", VO]
chains.append(f"[{n}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/thunderfit_ring_v4.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-t", str(total),
                "-movflags", "+faststart", out], check=True)
print(out, total)
