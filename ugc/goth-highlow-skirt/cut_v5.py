"""V5 (Ralph 2026-10-22: V4 "only shows one leg"): V4's continuous Kling take (knee, turn, one leg) + the shortest look
(both sides up, both legs) from VS, on a cut. Free. Music-only, no text, AI finish last."""
import subprocess
TOP = 0.29
k = f"crop=trunc(ih*{1 - TOP}*9/16/2)*2:trunc(ih*{1 - TOP}/2)*2:(iw-ow)*0.5:ih*{TOP}"
v = "scale=1080:1920,crop=trunc(iw*0.87/2)*2:trunc(ih*0.87/2)*2:(iw-ow)/2:ih*0.13"
G = "scale=1080:1920:flags=lanczos,fps=30,setsar=1,eq=brightness=0.02:contrast=1.03"
fc = (f"[0:v]setpts=PTS-STARTPTS,{k},{G}[a];[1:v]setpts=PTS-STARTPTS,{v},{G}[b];[a][b]concat=n=2:v=1:a=0,"
      "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-t", "11.3", "-i", "clips/K2_kling.mp4", "-ss", "0.5", "-t", "3.2", "-i", "clips/VS_seed_1_skin2.mp4",
                "-f", "lavfi", "-t", "14.5", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-shortest",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-maxrate", "7M", "-bufsize", "14M", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-movflags", "+faststart", "out/goth_v5_final.mp4"], check=True)
print("-> out/goth_v5_final.mp4")
