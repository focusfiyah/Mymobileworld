"""Migrastil Neuropathy Cream music-only cut v1 (2026-11-06): 6 windows, 13.5 s, silent stereo track (Grace adds music),
then ai_finish.sh. No text overlay (hard rule 6). Windows picked from the frame strips (S2 after its 1.5 s jump)."""
import subprocess
W = [("S1", 0.5, 2.2), ("S2", 2.5, 2.2), ("S3", 1.0, 2.4), ("S4", 1.0, 2.0), ("S5", 0.5, 2.2), ("S6", 1.5, 2.5)]
T = round(sum(d for _, _, d in W), 2)
inp, f = [], []
for i, (s, a, d) in enumerate(W):
    inp += ["-ss", str(a), "-t", str(d), "-i", f"clips/{s}.mp4"]
    f.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1,setpts=PTS-STARTPTS[v{i}]")
f.append("".join(f"[v{i}]" for i in range(len(W))) + f"concat=n={len(W)}:v=1:a=0[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-f", "lavfi", "-t", str(T), "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex", ";".join(f), "-map", "[v]", "-map", f"{len(W)}:a", "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "18", "-pix_fmt", "yuv420p", "-threads", "4", "-c:a", "aac", "-shortest", "cuts/v1_raw.mp4"], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", "cuts/v1_raw.mp4", "cuts/v1.mp4"], check=True)
print("cut", T)
