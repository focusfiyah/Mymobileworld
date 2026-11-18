"""Baby Soft-Sole Walking Shoes (Grace edit, 2026-11-16): hard-cut Grace's real footage, 7-20 s, silent
(she adds music herself: group msg 559 "I will have music in the background ensure all aspects of product features show").
# Source and SEGS set once Grace's original lands (template: baby-soft-sole-shoes-edit).
# Source and SEGS set once Grace's original lands (template: baby-soft-sole-shoes-edit).
import subprocess, sys, json, os
# (start, end) in seconds of Grace's 52 s video, in edit order; one product feature per shot
SEGS = [
  (21.8,23.8),  # hook: folds the shoe in half (soft, flexible sole)
  (1.4,3.4),    # the pair from the front (checker knit, rubber toe cap)
  (16.4,18.4),  # sole up: non-slip tread
  (26.0,28.0),  # fingers stretch the knit opening (easy on, breathable sock knit)
  (36.0,38.0),  # side profile: low wraparound rubber sole, heel tab
  (41.2,42.4),  # back view, pull tab
  (47.0,48.5),  # close pair to end
]
def render(tag, src, preset="medium"):
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out=f"out/squishy_{tag}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/squishy_{tag}.json","w")); print(out)
if __name__=="__main__":
    os.makedirs("out",exist_ok=True)
    render(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "medium")
