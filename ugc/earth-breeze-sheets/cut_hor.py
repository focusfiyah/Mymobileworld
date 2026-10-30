"""House of Rameau version (Ralph 2026-10-30: HofR yes), from cut.py: same VO and words, own framing (tighter zoom per shot), other in-points, cooler brighter grade, hook text from frame 0 to 4.6 s, no captions.
Earth Breeze sheets cut (2026-10-30), from ugc/camera-detector/cut.py: clean clip windows on Grace's voiceover, no text,
washer brand logos cropped (S1, S4, S7) or blurred (S3) for free, AI finish last. Every clip plays at 1.0x.
  python3 cut.py [VO] [--hor]  -> out/earth_breeze_v1_review.mp4 (veryfast) + out/earth_breeze_v1.mp4 (AI finish)
Shot windows come from vo.py (shots.json "t"). A window longer than its clip ends at the clip's end and the next shot starts
that much earlier."""
import json, subprocess, sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
VO = args[0] if args else "vo/voiceover_paced.mp3"
NAME = "earth_breeze_hor_v1"
HOLD = 0.6
CLIPLEN = {"S3": 1.95, "S1": 4.0}  # S3: the washer behind melts after ~2 s
FILE = {"S3": "clips/S3_fix.mp4"}  # washer logo blurred (free)
SRC = {"S1": 0.3, "S2": 1.1, "S4": 1.6, "S5": 1.7, "S6": 1.1, "S7": 1.2, "S8": 1.0, "S9": 1.9}  # where each clip's action is
CROP = {"S1": "crop=810:1440:120:60,", "S2": "crop=900:1600:90:200,", "S3": "scale=1080:1920,crop=900:1600:180:320,",
        "S4": "scale=1080:1920,crop=860:1530:180:120,", "S5": "crop=920:1636:100:180,", "S6": "crop=900:1600:0:220,",
        "S7": "crop=880:1564:150:40,", "S8": "crop=900:1600:90:160,", "S9": "crop=920:1636:80:100,"}
S = json.load(open("shots.json"))["shots"]
keep = [[s["id"], s["t"][0]] for s in S]
starts = [a for sid, a in keep]
END_VO = S[-1]["t"][1]
EDIT, pos = [], 0.0
for k, (sid, a) in enumerate(keep):
    b = starts[k + 1] if k + 1 < len(keep) else END_VO + HOLD
    d = b - pos; ss = SRC.get(sid, 0.0)
    clip = CLIPLEN.get(sid, 4.0)
    if ss + d > clip: d = clip - ss
    EDIT.append((sid, ss, d)); pos += d
assert abs(pos - (END_VO + HOLD)) < 0.02, f"edit {pos:.2f} vs vo {END_VO + HOLD:.2f}"
for e in EDIT: print(e[0], f"src {e[1]:.2f}", f"len {e[2]:.2f}")
END = pos
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", FILE.get(c, f"clips/{c}.mp4")]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,{CROP.get(c, '')}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.03:contrast=1.04:saturation=1.05,colorbalance=bs=0.04:rs=-0.03[g];[g][{n+1}:v]overlay=0:0:enable='lt(t,4.6)'[v]"
# loudnorm drops the tail of any padding in the same chain (2026-10-29), so normalise first, then pad to the picture length
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO, "-af", "aresample=44100,loudnorm=I=-16:TP=-2.5:LRA=11", "-ar", "44100", "out/_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/_vo.wav", "-af", f"apad=whole_dur={END:.3f}", "-t", f"{END:.3f}", "-ar", "44100", "out/_mix.wav"], check=True)
adur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "out/_mix.wav"], capture_output=True, text=True).stdout)
assert abs(adur - END) < 0.05, f"audio {adur:.2f} s vs picture {END:.2f} s"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", "out/_mix.wav", "-i", "out/hor_hook.png", "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"out/{NAME}_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
