"""Bite Toothpaste Bits music-only cut v1 (2026-11-03): 6 windows, 11.0 s, silent stereo track (Grace adds music),
then ai_finish.sh. No text overlay (hard rule 6)."""
import subprocess
W = [("S1", 0.0, 2.0), ("S2", 0.5, 1.6), ("S3", 1.0, 1.8), ("S4", 1.5, 2.0), ("S5", 2.0, 1.8), ("S6", 3.0, 1.8)]
inp, f = [], []
for i, (s, a, d) in enumerate(W):
    inp += ["-ss", str(a), "-t", str(d), "-i", f"clips/{s}.mp4"]
    f.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,setpts=PTS-STARTPTS[v{i}]")
f.append("".join(f"[v{i}]" for i in range(len(W))) + f"concat=n={len(W)}:v=1:a=0[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-f", "lavfi", "-t", "11", "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex", ";".join(f), "-map", "[v]", "-map", f"{len(W)}:a", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "cuts/v1_raw.mp4"], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", "cuts/v1_raw.mp4", "cuts/v1.mp4"], check=True)
