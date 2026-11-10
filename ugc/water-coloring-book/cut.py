"""3/6 Reusable Water Coloring Book (Grace edit, 2026-11-10): hard cuts of Grace's real footage (orig/grace_orig.mov,
1080x1920 59.94 fps, 195 s). Usage: python3 cut.py hd [preset]  -> out/wcb_hd.mp4"""
import subprocess, sys, json, os
SEGS = [  # (start, end) in her original; what it shows
 (170.0,172.0),  # 1 hook: close-up, pen paints colour onto the white part of the castle page, wet shine
 (78.2,79.4),    # 2 book opens on a blank white page
 (17.0,18.4),    # 3 the pens (blue, yellow, green) fanned in her hands
 (54.0,56.0),    # 4 pen filled with plain water from a bottle
 (2.0,3.3),      # 5 Magic Water Book cover (steady)
 (28.6,30.0),    # 6 bonus unicorn sticker sheet
 (91.6,93.0),    # 7 red princess dress appears under the pen
 (101.0,102.4),  # 8 flowers and grass appear
 (176.0,177.6),  # 10 castle scene nearly done
 (181.0,183.0),  # 11 finished page held up, stack of books behind
]
def render(mode="hd", src="orig/grace_orig.mov", preset="veryfast"):
    vf = "fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1"
    os.makedirs("out/segs",exist_ok=True); parts=[]
    for i,(a,b) in enumerate(SEGS):  # one seeked render per segment (11 trims on one decode ran out of memory)
        p=f"out/segs/{mode}_{i:02d}.mp4"; parts.append(p)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-i",src,"-t",f"{b-a:.3f}","-vf",vf,"-an","-c:v","libx264",
            "-preset",preset,"-crf","18","-pix_fmt","yuv420p","-threads","4",p],check=True)
    open("out/segs/list.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    out = f"out/wcb_{mode}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","out/segs/list.txt","-c","copy","-movflags","+faststart",out],check=True)
    json.dump({"src":src,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/wcb_{mode}.json","w"))
    print(out)
if __name__=="__main__":
    os.makedirs("out",exist_ok=True); render(sys.argv[1] if len(sys.argv)>1 else "hd", preset=sys.argv[2] if len(sys.argv)>2 else "veryfast")
