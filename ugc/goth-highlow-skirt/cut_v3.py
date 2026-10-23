"""V3 (Ralph 2026-10-22, due 13:45): back sway + Kling 4.0 pull (knee -> above knee -> one leg, cropped waist-down so the
phone/face never show) + shortest look. Music-only, no text, AI finish last."""
import subprocess
EDIT = [("VB_veo_1", 0.0, 1.3, None), ("K1_kling", 0.0, 6.3, (0.29, 0.5)), ("VS_seed_1_skin2", 0.5, 3.7, None)]
GRADE = "eq=brightness=0.02:contrast=1.03"
ins, parts = [], []
for i, (c, a, b, crop) in enumerate(EDIT):
    ins += ["-ss", str(a), "-t", str(round(b - a, 3)), "-i", f"clips/{c}.mp4"]
    if crop:   # top cut (fraction of height) then 9:16 window centred on her
        top, cx = crop
        cf = f"crop=trunc(ih*{1 - top}*9/16/2)*2:trunc(ih*{1 - top}/2)*2:(iw-ow)*{cx}:ih*{top}"
    else:      # same 13% top crop as cut 1 (phone hand)
        cf = "scale=1080:1920,crop=trunc(iw*0.87/2)*2:trunc(ih*0.87/2)*2:(iw-ow)/2:ih*0.13"
    parts.append(f"[{i}:v]setpts=PTS-STARTPTS,{cf},scale=1080:1920:flags=lanczos,fps=30,setsar=1,{GRADE}[v{i}]")
n = len(EDIT); dur = round(sum(b - a for _, a, b, _ in EDIT), 3)
fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{n}:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest", "-movflags", "+faststart", "out/goth_v3_review.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "out/goth_v3_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-maxrate", "7M", "-bufsize", "14M", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/goth_v3_final.mp4"], check=True)
print(dur, "s -> out/goth_v3_final.mp4")
