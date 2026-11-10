"""HEVEBLUE edit V1: python3 cut.py [final] -> out/heveblue_v1.mp4 + .json. Grace's own footage, 1.0x only, silent, no text."""
import subprocess,json,sys
SRC="orig/heveblue.mov"
SHOTS=[(69.0,70.5,"hook: cream comes out of the metal tip onto her hand"),
 (4.0,5.75,"the set: both tubes held up"),
 (7.5,9.25,"Lifting Eye Cream close-up, ingredient list"),
 (13.0,14.5,"Lifting AUTO Eye Cream held up"),
 (55.5,56.75,"cap off, metal tip shown"),
 (39.0,41.0,"metal massage head close-up"),
 (26.25,28.0,"head turned, dispensing hole"),
 (71.25,73.25,"swatch: cream wave on the hand"),
 (59.5,61.25,"end: both tubes side by side")]
f=[];n=len(SHOTS)
for i,(a,b,_) in enumerate(SHOTS):
    f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,format=yuv420p[v{i}]")
f.append("".join(f"[v{i}]" for i in range(n))+f"concat=n={n}:v=1:a=0[out]")
fin=len(sys.argv)>1
subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",";".join(f),"-map","[out]","-an","-c:v","libx264",
 "-preset","slow" if fin else "veryfast","-crf","17" if fin else "20","-threads","4","-movflags","+faststart","out/heveblue_v1.mp4"],check=True)
exp=round(sum(b-a for a,b,_ in SHOTS),2)
json.dump({"expected":exp,"shots":SHOTS},open("out/heveblue_v1.json","w"),indent=1); print("expected",exp)
