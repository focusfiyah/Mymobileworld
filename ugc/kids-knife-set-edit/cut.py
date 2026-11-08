"""Kids Safe Kitchen Knife Set 17/28 pc (Grace edit, 2026-11-08): hard-cut Grace's real unboxing footage, 12-20 s, silent
(her audio is handling noise only; she adds music in TikTok, as on the other Grace edits).
Draft: python3 cut.py tg  (Telegram copy 464x848). HD: python3 cut.py hd orig/<file>  (same segments, same timeline).
Grace's HD original (aa7a43...mov, 60 fps) runs 0.1 s behind the Telegram copy: python3 cut.py hd orig/kitchen_orig_1106.mov --shift 0.1"""
import subprocess, sys, json, os
# (start, end) in seconds of Grace's 43 s video, in edit order
SEGS = [
  (10.8,12.1),  # hook: 3 serrated safe knives fanned out (the product's name, bold colours)
  (37.2,38.3),  # whole set laid out in the open box (everything you get)
  (26.75,28.0),  # wooden knife
  (9.0,10.0),   # cut-resistant gloves
  (15.5,16.9),  # green peeler
  (24.5,25.7),  # crinkle cutter
  (29.1,30.3),  # wavy scraper pair
  (20.0,21.1),  # veggie shape cutters
  (32.0,33.2),  # bear mold
  (17.2,18.2),  # food picks
  (33.6,35.0),  # cutting board
  (41.7,42.75), # box with the chef boy
]
def render(tag, src, shift=0.0, preset="medium"):
    segs=[(round(a+shift,3),round(b+shift,3)) for a,b in SEGS]
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}];" for i,(a,b) in enumerate(segs))
    f += "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[out]"
    out=f"out/knife_{tag}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":segs,"expected":round(sum(b-a for a,b in segs),2)},open(f"out/knife_{tag}.json","w")); print(out)
if __name__=="__main__":
    os.makedirs("out",exist_ok=True)
    tag=sys.argv[1]; src=sys.argv[2] if len(sys.argv)>2 and not sys.argv[2].startswith("--") else "tg/knife_tg.mp4"
    sh=float(sys.argv[sys.argv.index("--shift")+1]) if "--shift" in sys.argv else 0.0
    render(tag, src, sh)
