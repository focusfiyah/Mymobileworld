"""Crème Shop Heating & Cooling Mask edit (2026-11-20): hard-cut Grace's original, silent (she adds music). SRC = argv[1] (default orig/original.mov)."""
import subprocess, sys, json, os
# (start, end, what it shows)
SEGS = [(2.3,4.0,"both boxes: Cool Quench leave-on + Heat Up Glow Up wash-off"),
        (7.2,8.8,"Heat Up box close: warming icon"),
        (14.3,15.8,"Heat Up Glow Up tube"),
        (20.3,21.8,"Cool Quench tube"),
        (25.3,27.0,"both tubes side by side"),
        (34.3,35.2,"flat lay: boxes + sticker sheets"),
        (35.3,37.0,"peeling a sticker"),
        (52.2,54.0,"LA sticker on the pink tube"),
        (64.3,66.0,"star sticker on the blue tube"),
        (76.5,79.0,"final duo with stickers")]
def render(src, name="creme", w=1080, h=1920):
    f = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[v{i}];" for i,(a,b,_) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    os.makedirs("out",exist_ok=True); out=f"out/{name}_v1.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":src,"segs":SEGS,"expected":round(sum(b-a for a,b,_ in SEGS),2)},open(f"out/{name}_v1.json","w")); print(out)
if __name__=="__main__": render(sys.argv[1] if len(sys.argv)>1 else "orig/original.mov")
