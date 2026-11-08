"""Momo & Nashi Erasable Tracing Books (Grace edit, 2026-11-08): hard-cut Grace's real footage, silent (her audio is
background chatter, no voiceover; she adds music in TikTok). Same segments for the Telegram draft and the HD original.
Usage: python3 cut.py draft   (orig/tg_786406597.mp4 -> out/momo_draft.mp4)
       python3 cut.py hd SRC  (her original -> out/momo_hd.mp4; set OFFSET if her original starts earlier than the Telegram copy)"""
import subprocess, sys, json, os
SEGS = [  # (start, end) in the Telegram copy; what it shows
 (9.0,10.8),   # 1 hook: lid opens on the full kit (book, markers, smiley eraser)
 (5.2,6.6),    # 2 box carried by its rope handle
 (13.3,14.7),  # 3 six erasable markers in their bag
 (16.6,19.0),  # 4 smiley eraser, flipped to the felt side
 (21.9,23.0),  # 5 spiral book cover close-up, moving
 (26.2,27.6),  # 6 book held, Lines/Shapes/Letters tabs
 (31.0,32.4),  # 7 Straight Lines page
 (34.4,35.8),  # 8 Basic Shapes page
 (41.4,42.6),  # 9 Big Letters F E H
 (45.6,46.2),  # 10 Numbers 1 to 5
 (47.0,48.2),  # 11 Numbers 6 to 10
 (0.3,1.0),    # 12 box front (hand sweeps in after 1.0), 35 activities, ages 3-5
]
def render(mode, src=None, offset=0.0, preset="medium"):
    src = src or "orig/tg_786406597.mp4"
    segs = [(round(a+offset,3), round(b+offset,3)) for a,b in SEGS]
    vf = "fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1"
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,{vf}[v{i}];" for i,(a,b) in enumerate(segs))
    f += "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[out]"
    out = f"out/momo_{mode}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264",
        "-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"offset":offset,"segs":segs,"expected":round(sum(b-a for a,b in segs),2)},open(f"out/momo_{mode}.json","w"))
    print(out)
if __name__=="__main__":
    os.makedirs("out",exist_ok=True)
    m = sys.argv[1] if len(sys.argv)>1 else "draft"
    render(m, sys.argv[2] if len(sys.argv)>2 else None, float(os.environ.get("OFFSET","0")))
