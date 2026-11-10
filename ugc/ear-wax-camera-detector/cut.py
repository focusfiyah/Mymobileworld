"""Hard-cut edit of Grace's original (orig/hd.mov) -> out/ear_v1.mp4, silent, 1080x1920 30 fps, 1.0x (no stretch).
Segments picked from 2 fps + 6 fps sheets of the whole 56.2 s video (2026-11-10)."""
import subprocess,json,os
SEG=[(19.17,2.0,"hook: live magnified skin on the IPS screen"),
     (30.20,1.5,"probe tip with its light on, side angle"),
     (13.00,1.5,"screen on, held front"),
     (23.50,1.5,"skin view, second angle"),
     (33.60,1.4,"probe light, straight on"),
     (35.60,1.2,"screen live view"),
     (38.00,1.5,"clear tip case"),
     (44.00,1.5,"two soft tips"),
     (48.60,2.0,"all tips fanned"),
     (52.00,1.3,"Good Bye screen + USB cable"),
     (3.60,1.4,"box: Smart Detector with Screen")]
os.makedirs("out",exist_ok=True)
inp=[];fl=[]
for i,(s,d,_) in enumerate(SEG):
    inp+=["-ss",str(s),"-t",str(d),"-i","orig/hd.mov"]
    fl.append(f"[{i}:v]fps=30,scale=1080:1920,setsar=1,setpts=PTS-STARTPTS[v{i}]")
fc=";".join(fl)+";"+"".join(f"[v{i}]" for i in range(len(SEG)))+f"concat=n={len(SEG)}:v=1:a=0[o]"
subprocess.run(["ffmpeg","-v","error","-y",*inp,"-filter_complex",fc,"-map","[o]","-an","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-threads","4","-movflags","+faststart","out/ear_v1.mp4"],check=True)
json.dump({"expected":round(sum(d for _,d,_ in SEG),2),"segments":SEG},open("out/ear_v1.json","w"),indent=1)
print("rendered",sum(d for _,d,_ in SEG))
