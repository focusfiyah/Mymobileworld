"""V6 (Ralph 2026-10-22: "What about the other movements"): V4's take 0-6.0 s (knee + turn) + a Kling 4.0 continuation from
V4's 6.0 s frame (front pull to mid-thigh, one leg, both legs, walk + cross). Same crop both parts, so it reads as one take.
  python3 cut_v6.py [K3_end]"""
import subprocess, sys
end = sys.argv[1] if len(sys.argv) > 1 else "10"
TOP = 0.29
k = f"crop=trunc(ih*{1 - TOP}*9/16/2)*2:trunc(ih*{1 - TOP}/2)*2:(iw-ow)*0.5:ih*{TOP},scale=1080:1920:flags=lanczos,fps=30,setsar=1"
SEG = [("K2_kling", 0.0, 6.0), ("K3_kling", 0.04, 1.6), ("K3_kling", 2.7, 5.7), ("K3_kling", 7.6, 10.0)]   # K3 1.7-2.5 s and 5.8-7.4 s: she lifts the front by hand and black shorts show (not in the inspo)
ins, parts = [], []
for i, (c, x, y) in enumerate(SEG):
    ins += ["-ss", str(x), "-t", str(round(y - x, 3)), "-i", f"clips/{c}.mp4"]
    parts.append(f"[{i}:v]setpts=PTS-STARTPTS,{k}[s{i}]")
n = len(SEG); dur = round(sum(y - x for _, x, y in SEG), 3)
fc = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.02:contrast=1.03,eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{n}:a", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-maxrate", "7M", "-bufsize", "14M",
                "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", "out/goth_v6_final.mp4"], check=True)
print("-> out/goth_v6_final.mp4")
