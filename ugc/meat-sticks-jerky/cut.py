"""Meat Sticks + Sweet Heat Jerky (Grace, 2026-11-08): hard cuts of Grace's 1080x1920 original, 1.0x, silent
(her audio is unboxing noise only; she adds music in TikTok, as on PLAYA/Haiti). Pattern: ugc/haiti-flag/cut.py."""
import subprocess, json, os
SRC="orig/hd.mov"
SEGS=[(93.0,94.6),   # hook: close sweep across all 4 flavors
      (6.2,7.5),     # box open, wrapped bundles (no desk LED)
      (37.0,38.3),   # jerky peeks out of the paper
      (43.2,44.6),   # Sweet Heat jerky held up
      (57.0,58.3),   # stick pack close
      (65.3,66.6),   # sticks spread in the box
      (70.0,71.5),   # Pink Himalayan Salt
      (74.5,76.0),   # Pineapple Chili Lime
      (78.0,79.5),   # Original
      (81.0,82.5),   # Hot Honey
      (104.0,105.5), # everything lined up in the box
      (109.0,110.3)] # close on the full pack
os.makedirs("out",exist_ok=True)
args=[]
for a,b in SEGS: args+=["-ss",str(a),"-t",f"{b-a:.3f}","-i",SRC]
f="".join(f"[{i}:v]fps=30,scale=1080:1920:flags=lanczos,setsar=1,setpts=PTS-STARTPTS[v{i}];" for i in range(len(SEGS)))
f+="".join(f"[v{i}]" for i in range(len(SEGS)))+f"concat=n={len(SEGS)}:v=1:a=0,format=yuv420p[o]"
subprocess.run(["ffmpeg","-v","error","-y",*args,"-filter_complex",f,"-map","[o]","-an","-c:v","libx264","-preset","slow","-crf","17",
  "-movflags","+faststart","-threads","4","out/meat_v1.mp4"],check=True)
json.dump({"expected":round(sum(b-a for a,b in SEGS),2)},open("out/meat_v1.json","w"))
