"""Cut the Manners V1 edit from Grace's original. python3 cut.py [--fast]"""
import subprocess,json,sys
SRC="orig/manners.mov"
SEG=[(1.6,3.4,"hook: cover tilts to camera"),(14.0,15.6,"pages fan open"),(19.6,20.8,"folds into a desk stand"),
(24.4,25.6,"flip to Control Your Volume"),(26.8,28.0,"Volume page push-in"),(29.5,31.0,"Treat Homes With Respect"),
(35.5,36.9,"flip to Respect Privacy"),(44.1,45.2,"flip to Make Room"),(50.0,51.6,"Make Room angled close"),(55.2,56.7,"close: back to the cover")]
fast="--fast" in sys.argv
fc="".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920,setsar=1[v{i}];" for i,(a,b,_) in enumerate(SEG))
fc+="".join(f"[v{i}]" for i in range(len(SEG)))+f"concat=n={len(SEG)}:v=1:a=0,format=yuv420p[o]"
subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",fc,"-map","[o]","-an","-c:v","libx264","-preset","veryfast" if fast else "slow","-crf","18","-threads","4","-movflags","+faststart","out/manners_v1.mp4"],check=True)
exp=round(sum(b-a for a,b,_ in SEG),2); json.dump({"expected":exp,"segments":SEG},open("out/manners_v1.json","w"),indent=1); print("rendered",exp)
