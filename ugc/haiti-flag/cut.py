"""Haiti flag (2026-11-06): hard-cut real footage, no sound (Grace adds music in TikTok). Source 464x848 upscaled to 1080x1920 (cover crop)."""
import subprocess, json, os
SRC="orig/IMG_0351.MOV"
SEGS=[(3.0,4.3),(9.0,10.3),(12.0,13.3),(18.0,19.3),(27.0,28.3),(35.5,36.8),(38.5,39.8),
      (42.0,43.3),(48.0,49.3),(54.0,55.0),(69.0,70.3)]
os.makedirs("out",exist_ok=True)
f="".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1974:flags=lanczos,crop=1080:1920,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
f+="".join(f"[v{i}]" for i in range(len(SEGS)))+f"concat=n={len(SEGS)}:v=1:a=0[o]"
subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[o]","-an","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4","out/haiti_v1.mp4"],check=True)
json.dump({"expected":round(sum(b-a for a,b in SEGS),2)},open("out/haiti_v1.json","w"))
