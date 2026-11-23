"""WARSUN X608 Flashlight (Grace edit, 2026-11-17): hard-cut Grace's HD original (103 s, 1080x1920 HEVC 60 fps), 7-20 s, silent
(Grace adds music herself, group msg 559: "ensure all aspects of product features show").  python3 cut.py v1 orig/warsun_orig.mov"""
import subprocess, sys, json, os
SEGS = [
  (54.2,55.9),   # hook: side RGB strip glowing green -> blue (most eye-catching)
  (2.2,3.3),     # front COB light + blue battery-level bars (stops before the lunge blur)
  (35.1,35.75),  # top spotlight beam straight at camera (stops before the dark frame)
  (79.5,81.2),   # flood beam on the wall
  (41.4,43.0),   # green laser dot
  (13.0,14.5),   # red laser pointer dot on the wall
  (66.2,67.6),   # purple strip mode
  (84.2,85.8),   # side white work light
  (28.1,29.2),   # UV purple light
  (60.0,61.6),   # multicolour strip mode
  (92.4,93.6),   # rugged body side, lanyard (after the jump in her clip at 92.3)
  (100.8,102.6), # close: UV top light, then front view held up
]
def render(tag, src, preset="medium"):
    """One segment at a time (12 HEVC branches in one graph ran out of memory), then a lossless concat."""
    parts=[]
    for i,(a,b) in enumerate(SEGS):
        p=f"out/seg_{tag}_{i:02d}.mp4"; parts.append(p)
        subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{max(a-2,0):.3f}","-i",src,"-ss",f"{a-max(a-2,0):.3f}","-t",f"{b-a:.3f}",
          "-vf","fps=30,scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p","-an","-c:v","libx264","-preset",preset,"-crf","18",
          "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709","-threads","4",p],check=True)
    open(f"out/list_{tag}.txt","w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
    out=f"out/warsun_{tag}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"out/list_{tag}.txt","-c","copy","-movflags","+faststart",out],check=True)
    json.dump({"src":src,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/warsun_{tag}.json","w")); print(out)
if __name__=="__main__":
    os.makedirs("out",exist_ok=True); render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "medium")
