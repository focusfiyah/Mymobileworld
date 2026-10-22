"""V9 (Ralph 2026-10-22: "edit all the videos to take what we need ... the closest match to the inspo"): best paid windows in
the inspo's order, free. Knee (K2) -> back (VB, real solid tiers) -> waist pull, rise, one leg at mid-thigh (K1) -> both legs +
crossed step (K3). Waist-down, music-only, no text, AI finish last. Skips: FULL2 takes (see-through), hand-lift frames."""
import subprocess
K = "crop=trunc(ih*0.71*9/16/2)*2:trunc(ih*0.71/2)*2:(iw-ow)*0.5:ih*0.29"             # FULL-framed Kling takes
V = "scale=1080:1920,crop=trunc(iw*0.87/2)*2:trunc(ih*0.87/2)*2:(iw-ow)/2:ih*0.13"   # S2-framed Veo clips
EDIT = [("K2_kling", 0.0, 1.5, K), ("VB_veo_1", 0.0, 1.3, V), ("K1_kling", 2.0, 6.0, K), ("K3_kling", 7.6, 10.0, K)]
G = "scale=1080:1920:flags=lanczos,fps=30,setsar=1,eq=brightness=0.02:contrast=1.03"
ins, parts = [], []
for i, (c, a, b, cf) in enumerate(EDIT):
    ins += ["-ss", str(a), "-t", str(round(b - a, 3)), "-i", f"clips/{c}.mp4"]
    parts.append(f"[{i}:v]setpts=PTS-STARTPTS,{cf},{G}[v{i}]")
n = len(EDIT); dur = round(sum(b - a for _, a, b, _ in EDIT), 3)
fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{n}:a", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-maxrate", "7M", "-bufsize", "14M",
                "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", "out/goth_v9_final.mp4"], check=True)
print(dur, "s -> out/goth_v9_final.mp4")
