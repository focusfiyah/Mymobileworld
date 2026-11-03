"""ThunderFit 7-pack V1 cut (music only, no VO, no text). Each clip used from 0 s for its window, never stretched.
S7 trimmed to 1.5 s (push-in makes the ring read big after that), S3 +0.5 s: total 10.9 s. python3 cut.py [--final]"""
import subprocess, sys
W = [("S1",1.6),("S2",1.6),("S3",1.9),("S4",1.4),("S5",1.4),("S6a",0.65),("S6b",0.65),("S6c",0.7),("S7",1.5)]
fin = "--final" in sys.argv
args, f = [], []
for i,(s,d) in enumerate(W):
    args += ["-t", str(d), "-i", f"clips/{s}.mp4"]
    f.append(f"[{i}:v]trim=0:{d},setpts=PTS-STARTPTS,fps=30,scale=1080:1920,setsar=1[v{i}]")
f.append("".join(f"[v{i}]" for i in range(len(W))) + f"concat=n={len(W)}:v=1:a=0[out]")
out = "cut_v1_raw.mp4"
subprocess.run(["ffmpeg","-v","error","-y",*args,"-filter_complex",";".join(f),"-map","[out]","-c:v","libx264","-preset","slow" if fin else "veryfast","-crf","17","-pix_fmt","yuv420p","-threads","4",out],check=True)
print(out, sum(d for _,d in W))
