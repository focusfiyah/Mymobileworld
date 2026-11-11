"""Wig Milk Spray (2026-11-11): hard-cut Grace's real footage (her HD original WigMilkSpray2.mov, 1080x1920 HEVC 30fps), silent like the Calmi edit (she adds sound in TikTok)."""
import subprocess, sys, json, os
SRC = os.environ.get("SRC", "orig/WigMilkSpray2.mov")
# r2 (Grace msg 438: her reference transcript is the script): shots timed to each line at her pace (~3.5 words/s, the 25 s reference)
LINES = [
 ("I swear I was about to toss this synthetic wig in the garbage,", [(5.1,8.5)]),            # tangled wig pulled apart
 ("but this little spray right here came in clutch.", [(28.4,30.7)]),                      # bottle up to camera, hair still tangled (4:01 bottle shot dropped: hair already smooth, broke before/after)
 ("This is why I don't buy synthetic wigs. They get tangled, matted and start looking worn out way too quickly.", [(11.5,14.5),(15.0,18.0)]),  # frizzy, matted strands
 ("But this wig milk spray is a two-in-one leave-in conditioner and detangler made for synthetic wigs.", [(30.7,33.3),(102.0,104.3)]),  # bottle + brush, then spraying
 ("It helps condition dry looking fibers, loosen tangles, and restore shine, and make the combing so much easier.", [(146.4,149.0),(189.0,191.5)]),  # brushing through, brush glides on smooth hair
 ("And you don't even have to rinse this out.", [(230.0,232.6)]),                          # smooth shiny hair flip
 ("It's linked in the orange cart.", [(551.0,553.6)]),                                     # final smile
]
SEGS = [s for _,ss in LINES for s in ss]
GRADE = os.environ.get("GRADE", "eq=brightness=0.02:contrast=1.03")
def render(name="wig", preset="veryfast"):
    ins = sum((["-ss",f"{a:.3f}","-t",f"{b-a:.3f}","-i",SRC] for a,b in SEGS),[])  # one seeked input per shot (a single input with 6 trims buffers minutes of 1080p and got OOM-killed)
    f = "".join(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1,{GRADE}[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(*sys.argv[1:])
