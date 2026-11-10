"""Crowned Skin Body Butter 5 Scent Pack (Grace, 2026-11-10): hard cuts of Grace's 1080x1920 original at 1.0x, silent
(her audio is handling noise; she adds music in TikTok, as on Meat Sticks / Merach). Pattern: ugc/meat-sticks-jerky/cut.py."""
import subprocess, json, os
SRC="orig/hd.mov"
SEGS=[(63.2,64.6),   # hook: seal peeled back, butter revealed
      (1.6,2.4),     # five coloured crown lids in the box
      (10.8,12.2),   # EMPIRE label
      (38.0,39.4),   # KING
      (43.2,44.6),   # PRINCE
      (49.4,50.8),   # MONARCH
      (56.4,57.8),   # REIGN
      (72.2,73.6),   # finger glides through the whipped butter
      (76.0,77.4),   # scoop on the fingertip
      (78.1,80.6),   # rubbed into the back of the hand, glow (one take: two cuts of this framing read as a jump)
      (98.6,100.4)]  # all five labels lined up in the box
os.makedirs("out",exist_ok=True)
args=[]
for a,b in SEGS: args+=["-ss",str(a),"-t",f"{b-a:.3f}","-i",SRC]
f="".join(f"[{i}:v]fps=30,scale=1080:1920:flags=lanczos,setsar=1,setpts=PTS-STARTPTS[v{i}];" for i in range(len(SEGS)))
f+="".join(f"[v{i}]" for i in range(len(SEGS)))+f"concat=n={len(SEGS)}:v=1:a=0,format=yuv420p[o]"
subprocess.run(["ffmpeg","-v","error","-y",*args,"-filter_complex",f,"-map","[o]","-an","-c:v","libx264","-preset","slow","-crf","17",
  "-movflags","+faststart","-threads","4","out/crowned_v1.mp4"],check=True)
json.dump({"expected":round(sum(b-a for a,b in SEGS),2)},open("out/crowned_v1.json","w"))
