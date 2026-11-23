"""OQQ Women's Casual High-Waisted Loose Pants (Grace edit, 2026-11-18): hard-cut Grace's real footage, 7-20 s, silent
(she adds music herself: group msg 559 brief). SEGS filled in once her HD original lands in Originals 1JuBJ5rjYJBz4PCQS1Gx8qg0faFUVG8lU.
Run: python3 cut.py v1 orig/pants_orig.mov"""
import subprocess, sys, json, os
# (start, end) in seconds of Grace's 52 s video, in edit order; one product feature per shot
SEGS = [  # TODO when the original lands: one feature per shot (high waist, side hidden pocket + phone, loose straight leg, full-length hem, walk)
]
def render(tag, src, preset="medium"):
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out=f"out/pants_{tag}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/pants_{tag}.json","w")); print(out)
if __name__=="__main__":
    os.makedirs("out",exist_ok=True)
    render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "medium")
