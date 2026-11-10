"""PURCELL 247 Colostrum Ampoule Mist (2026-11-10): hard-cut of Grace's real footage, silent (no speech in her audio; she adds sound in TikTok).
SRC = her Drive original (1080x1920 HEVC 60 fps, 42.47 s). Segment list = the edit."""
import subprocess, json, os
SRC = os.environ.get("SRC", "orig/grace_orig.mov")
TAG = os.environ.get("TAG", "v1")
SEGS = [
 (29.4,31.0),  # hook: dewy glow on the back of her hand (the result)
 (3.0,4.3),    # box: before & after makeup, glowing skin, travel friendly
 (8.0,9.3),    # compact bottle front, small in her hand
 (15.0,16.4),  # close: front label + ingredients
 (16.9,17.8),  # pocket size between her fingers
 (23.2,24.8),  # back label + spray head
 (26.3,28.9),  # sprays it on, skin goes dewy
 (33.0,34.4),  # glow with the bottle beside it
 (36.0,37.4),  # bottle next to the glowing hand
 (41.1,42.4)]  # close: bottle in both hands
def render():
    f = "".join(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,setsar=1[v{i}];" for i,(a,b) in enumerate(SEGS))
    f += "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[out]"
    out = f"out/mist_{TAG}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",SRC,"-filter_complex",f,"-map","[out]","-an","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart","-threads","4",out],check=True)
    json.dump({"src":SRC,"segs":SEGS,"expected":round(sum(b-a for a,b in SEGS),2)},open(f"out/mist_{TAG}.json","w")); print(out)
render()
