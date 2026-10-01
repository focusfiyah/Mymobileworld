"""Free timing animatic: one card per shot, cut to the Grace B voiceover (hook 1 + body)."""
import json, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
out_dir = sys.argv[1]
J = json.load(open("shots.json")); shots = {s["id"]: s for s in J["shots"]}
H = 4.206  # hook1.mp3 length; body starts here
cuts = [0, H, H+6.19, H+10.01, H+12.52, H+15.76, H+19.43, H+24.0, 31.16]
order = ["H1","S2","S3","S4","S5","S6","S7","S8"]
ref = {"H1":"refs/product_open.png","S2":"refs/product_front.png","S3":"refs/product_open.png","S4":"refs/hand_palm.png",
       "S5":"refs/hand_dorsal.png","S6":"refs/product_front.png","S7":"refs/product_front.png","S8":"refs/hand_dorsal.png"}
F = lambda s, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if b else ''}.ttf", s)
cream, ink, orange = (246,239,226), (34,30,26), (240,110,30)
lst = open(f"{out_dir}/list.txt","w")
for i, sid in enumerate(order):
    s = shots[sid]; im = Image.new("RGB",(720,1280),cream); d = ImageDraw.Draw(im)
    d.text((40,40),"PREVIEW 1 · TIMING ANIMATIC · placeholder art",font=F(22),fill=(140,130,120))
    d.text((40,80),f"{sid}  ·  {s['beat'].upper()}",font=F(40,True),fill=orange)
    d.text((40,132),f"{cuts[i]:.1f}s – {cuts[i+1]:.1f}s",font=F(26),fill=ink)
    r = Image.open(ref[sid]).convert("RGB"); r.thumbnail((420,460)); im.paste(r,((720-r.width)//2,185))
    y = 670; d.text((40,y),"WHAT THE HAND DOES",font=F(22,True),fill=(140,130,120)); y += 34
    for ln in textwrap.wrap(s["video"].replace("Shot 1 ","").replace("Shot 2 ",""),46)[:9]:
        d.text((40,y),ln,font=F(25),fill=ink); y += 34
    d.rectangle((0,1060,720,1280),fill=ink); y = 1080
    for ln in textwrap.wrap("“"+s["vo"]+"”",34)[:5]:
        d.text((40,y),ln,font=F(30,True),fill=cream); y += 40
    p = f"{out_dir}/{i:02d}.png"; im.save(p)
    lst.write(f"file '{p}'\nduration {cuts[i+1]-cuts[i]:.3f}\n")
lst.write(f"file '{p}'\n"); lst.close()
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{out_dir}/list.txt","-i","vo/full_hook1_body.mp3",
  "-vf","fps=24,format=yuv420p","-c:v","libx264","-crf","26","-c:a","aac","-b:a","128k","-shortest","preview/preview1_animatic.mp4"],check=True)
