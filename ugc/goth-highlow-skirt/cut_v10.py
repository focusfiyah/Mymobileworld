"""V10 (Ralph 2026-10-22: "make the transitions as seamless as possible"): V9's windows with (1) matched framing: the Kling
takes are reframed so the waist sits at ~19% and the boots at ~91% of the frame, the same as the Veo back clip shown full frame;
(2) the back clip colour-trimmed to the Kling wall colour; (3) 0.3 s dissolves at every join. Free. AI finish last."""
import subprocess
XF = 0.3
K = "crop=trunc(ih*0.60*9/16/2)*2:trunc(ih*0.60/2)*2:(iw-ow)*0.5:ih*0.339"   # Kling (FULL framing): waist ~19%, boots ~91%
V = "colorchannelmixer=rr=0.93:gg=0.945:bb=0.955"                            # Veo back clip, full frame, wall matched to Kling
EDIT = [("K2_kling", 0.0, 1.8, K), ("VB_veo_1", 0.0, 1.3, V), ("K1_kling", 1.7, 6.0, K), ("K3_kling", 7.6, 10.0, K)]
G = "scale=1080:1920:flags=lanczos,fps=30,setsar=1,format=yuv420p,eq=brightness=0.02:contrast=1.03"
ins, parts = [], []
for i, (c, a, b, cf) in enumerate(EDIT):
    ins += ["-ss", str(a), "-t", str(round(b - a, 3)), "-i", f"clips/{c}.mp4"]
    parts.append(f"[{i}:v]setpts=PTS-STARTPTS,{cf},{G}[v{i}]")
lens = [round(b - a, 3) for _, a, b, _ in EDIT]
chain, cur, off = [], "v0", 0.0
for i in range(1, len(EDIT)):
    off += lens[i - 1] - XF
    out = f"x{i}"
    chain.append(f"[{cur}][v{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[{out}]")
    cur = out
dur = round(sum(lens) - XF * (len(EDIT) - 1), 3)
fc = ";".join(parts + chain) + f";[{cur}]eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{len(EDIT)}:a", "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-maxrate", "7M",
                "-bufsize", "14M", "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", "out/goth_v10_final.mp4"], check=True)
print(dur, "s -> out/goth_v10_final.mp4")
