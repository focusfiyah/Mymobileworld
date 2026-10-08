"""Free cut v2: 8 hands-only clips on the trimmed Grace B voiceover, no text overlay (default; Ralph has not asked for one).

  python3 cut.py   -> out/thunderfit_ring_v2.mp4 (720x1280, 24fps)

Every shot is real clip footage at 1.0x (no holds, no speed changes, no Ken Burns). Ralph 2026-10-08: the ring must be on the bench at
the very start, the removal is cut out (S1 uses only its last second), so every shot runs its full useful length back to back and the
picture leads the words by up to ~2.4 s in the middle and re-syncs at the end (S5 lift lands on "Gym", S8 on the CTA).
S4 skips its first 1.4 s (ring at the fingertip of a finger that wears a ring, Ralph 2026-10-08).
"""
import json, subprocess
from pathlib import Path

SEGS = [("S1", 4.0, 1.04), ("S2", 0.0, 5.04), ("S3", 0.0, 5.04), ("S4", 1.4, 3.64),
        ("S5", 0.0, 4.04), ("S6", 0.0, 4.04), ("S7", 0.0, 4.04), ("S8", 0.0, 8.04)]
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
assert sum(d for _, _, d in SEGS) >= total, "footage shorter than the voiceover"
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0,format=yuv420p[vout]")
inputs += ["-i", VO]
chains.append(f"[{n}:a]apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/thunderfit_ring_v2.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-t", str(total),
                "-movflags", "+faststart", out], check=True)
print(out, total)
