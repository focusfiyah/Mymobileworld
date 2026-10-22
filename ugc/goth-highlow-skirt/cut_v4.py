"""V4 (Ralph 2026-10-22: "Just do it with AI", "the string is not that long"): ONE continuous Kling 4.0 take (13 s) of all five
inspo looks from the full-body still, cropped waist-down like the inspo. Music-only, no text, AI finish last.
  python3 cut_v4.py [IN OUT]   (seconds to keep; default whole clip)"""
import subprocess, sys
a, b = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) > 2 else (0.0, None)
TOP, CX = 0.29, 0.5   # cut the phone/face off the top; 9:16 window centred on her
cf = f"crop=trunc(ih*{1 - TOP}*9/16/2)*2:trunc(ih*{1 - TOP}/2)*2:(iw-ow)*{CX}:ih*{TOP}"
inp = ["-ss", str(a)] + (["-t", str(round(b - a, 3))] if b else []) + ["-i", "clips/K2_kling.mp4"]
subprocess.run(["ffmpeg", "-y", "-v", "error", *inp, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex",
                f"[0:v]setpts=PTS-STARTPTS,{cf},scale=1080:1920:flags=lanczos,fps=30,setsar=1,eq=brightness=0.02:contrast=1.03,"
                "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t[v]", "-map", "[v]", "-map", "1:a", "-shortest",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-maxrate", "7M", "-bufsize", "14M", "-threads", "4",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", "out/goth_v4_final.mp4"], check=True)
print("-> out/goth_v4_final.mp4")
