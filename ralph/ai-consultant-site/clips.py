"""Cut one single-shot muted loop per approved ad for the site (free, ffmpeg).
Usage: python3 clips.py  (writes /home/user/focusfiyah.github.io/media/<name>.mp4 + .jpg poster)"""
import subprocess as sp, re, os
UGC = "/home/user/Mymobileworld/ugc"
OUT = "/home/user/focusfiyah.github.io/media"
CLIPS = [  # name, source, where in the ad (0-1) the wanted shot is
    ("pouch", "youtheory-b12b6/out/youtheory_b12b6_v1.mp4", 0.2),
    ("vanity", "fusou-vanity/v3ab/out/fusou_v3A_motion.mp4", 0.2),
    ("oils", "plant-therapy-top6/out/plant_therapy_top6.mp4", 0.8),
    ("tablet", "vicks-vaposhower/out/vicks_vaposhower.mp4", (12.9, 3.4)),  # scene detect misses this cut
    ("scoop", "lgxnds-creatine/out/lgxnds_creatine_v3.mp4", 0.5),
    ("heater", "space-heater-ptc/out/heater_V1.mp4", 0.8),
    ("tub", "shnuggle-next-bath/out/shnuggle_next_bath.mp4", 0.8),
    ("stick", "carpe-mb-15s/out/carpe_mb_15s_r2.mp4", 0.5),
    ("jar", "jiyu-polish-pads/out/jiyu_v2.mp4", 0.2),
    ("juice", "youtheory-ashwagandha/out/youtheory-ashwagandha_v5.mp4", 0.5),
    ("serum", "base-labs/oil/out/oil.mp4", (23.5, 1.65)),  # skips the packshot pop-up
]
def dur(f):
    return float(sp.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
def cuts(f):
    r = sp.run(["ffmpeg","-nostdin","-i",f,"-vf","select='gt(scene,0.3)',showinfo","-an","-f","null","-"],capture_output=True,text=True)
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]
def pick(f, pos):
    d = dur(f); t = d*pos
    c = [0.0] + cuts(f) + [d]
    a = max(x for x in c if x <= t); b = min(x for x in c if x > t)
    a += 0.15; b -= 0.1                          # stay clear of the cut frames
    length = min(5.0, b - a)
    return max(a, min(t - length/2, b - length)), length

def encode(name, f, start, length):
    sp.run(["ffmpeg","-nostdin","-v","error","-y","-ss",f"{start:.3f}","-i",f,"-t",f"{length:.3f}","-an",
            "-vf","scale=480:-2:flags=lanczos,fps=30","-c:v","libx264","-preset","slow","-crf","24","-pix_fmt","yuv420p",
            "-movflags","+faststart",f"{OUT}/{name}.mp4"],check=True)
    sp.run(["ffmpeg","-nostdin","-v","error","-y","-i",f"{OUT}/{name}.mp4","-frames:v","1","-q:v","4",f"{OUT}/{name}.jpg"],check=True)
    print(name, f"{start:.2f}+{length:.2f}s", os.path.getsize(f"{OUT}/{name}.mp4")//1024, "KB")

os.makedirs(OUT, exist_ok=True)
for name, src, pos in CLIPS:
    f = os.path.join(UGC, src)
    start, length = pos if isinstance(pos, tuple) else pick(f, pos)
    encode(name, f, start, length)
