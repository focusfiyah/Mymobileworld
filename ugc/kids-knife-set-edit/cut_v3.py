"""Kids Kitchen Set V2 reframe (Ralph 2026-11-08 tapped "Free reframe now"): only moments NOT in V1, each pushed in
with a crop (zoom <= 1.35x of the 1080x1920 HD original), new order. HD timeline (aa7a43...mov). Silent, no text.
python3 cut_v3.py  -> out/knife_v3.mp4 (+ .json). Overlap with V1 is checked by overlap.py."""
import subprocess, json, os
SRC="orig/kitchen_orig_1106.mov"
# (start, end, zoom, cx, cy)  cx/cy = crop centre as a fraction of the frame
SEGS=[
 (20.0,21.4,1.30,0.50,0.50),  # hook: veggie shape cutters turning in her hand
 (11.6,13.0,1.25,0.50,0.38),  # three serrated knives, blades closer
 (6.0,6.6,1.30,0.55,0.55),    # tray just opened, gloves on top
 (9.0,9.9,1.25,0.50,0.45),    # gloves in their bag
 (16.2,17.2,1.30,0.48,0.42),  # peeler facing camera
 (27.4,28.4,1.25,0.52,0.40),  # wooden crocodile knife
 (24.6,25.8,1.30,0.50,0.48),  # crinkle cutter
 (30.0,31.2,1.25,0.50,0.48),  # wavy scrapers
 (17.25,18.0,1.30,0.48,0.50), # food picks
 (38.5,39.6,1.35,0.72,0.74),  # tray: bear mold + cutters corner
 (33.7,34.5,1.20,0.50,0.45),  # cutting board
 (41.8,42.85,1.20,0.60,0.47), # purple chef-boy box
]
def render(preset="medium"):
    f=""
    for i,(a,b,z,cx,cy) in enumerate(SEGS):
        w,h=round(1080/z/2)*2,round(1920/z/2)*2
        x=min(max(0,round(cx*1080-w/2)),1080-w); y=min(max(0,round(cy*1920-h/2)),1920-h)
        f+=f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,setsar=1,eq=brightness=0.02:saturation=1.04[v{i}];"
    f+="".join(f"[v{i}]" for i in range(len(SEGS)))+f"concat=n={len(SEGS)}:v=1:a=0[out]"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset",preset,"-crf","18","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4","out/knife_v3.mp4"],check=True)
    json.dump({"src":SRC,"segs":[s[:2] for s in SEGS],"expected":round(sum(b-a for a,b,*_ in SEGS),2)},open("out/knife_v3.json","w")); print("out/knife_v3.mp4")
if __name__=="__main__": render()
