"""Cut one single-shot muted loop per approved ad for the site (free, ffmpeg).
Usage: python3 clips.py  (writes /home/user/focusfiyah.github.io/media/<name>.mp4 + .jpg poster)"""
import subprocess as sp, re, os
UGC = "/home/user/Mymobileworld/ugc"
DL = "/tmp/claude-0/-home-user/d532a940-ce98-56c2-93b0-73c4f8def487/scratchpad/lp/dl"  # Vans V1 from Drive (not in git)
OUT = "/home/user/focusfiyah.github.io/media"
CLIPS = [  # name, source, where in the ad (0-1) or (start, length); only videos that made sales (Grace's tracker + Ralph 2026-10-28)
    # reel
    ("castor", "bodyj-castor-rollon/out/bodyj_castor_v2g_r1_final.mp4", 0.15),
    ("vans", DL + "/vans_v1.mp4", (0.2, 3.8)),
    ("cards", "throw-hands-rps/out/throw_hands_r2b_raw.mp4", 0.55),
    ("beam", "powerbank-flashlight-v2/out/flashlight_v2_r1.mp4", 0.35),
    ("brush", "pritech-cleansing-brush/out/pritech_review.mp4", 0.65),
    # grid
    ("path", "powerbank-flashlight/out/powerbank_flashlight_r4.mp4", 0.45),
    ("pouches", "sofyre-rodent-pouches/out/sofyre_r1_raw.mp4", 0.55),
    ("dilator", "mute-nasal-dilator/out/mute_nasal_dilator_r4.mp4", 0.55),
    ("roller", "bodyj-castor-rollon/out/bodyj_castor_v2g_r1_final.mp4", 0.55),
    # ("box", card game) replaced 2026-10-29 by the night driving glasses clip (Ralph). Source = the posted video that sold,
    # downloaded with tiktok.py video https://www.tiktok.com/@shewiththeglow/video/7696285070046301470 (not in git);
    # glasses = 18.10 s + 4.40 s (hand holding the glasses, no on-screen text in that shot).
    ("rinse", "pritech-cleansing-brush/out/pritech_review.mp4", 0.15),
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
