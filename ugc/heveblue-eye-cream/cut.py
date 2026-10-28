"""HEVEBLUE eye cream cut (2026-10-27), from ugc/mini-bag-charm/cut.py: clean clip windows on Grace's voiceover, no text,
a free 200 Hz buzz (12,000 a minute) under S1-S2 only (Ralph's answer 7), AI finish last. Every clip plays at 1.0x.
  python3 cut.py [VO]   -> out/heveblue_v2_review.mp4 (veryfast) + out/heveblue_v2.mp4 (AI finish)
Shot windows come from vo.py (shots.json "t"). A window longer than its clip ends at the clip's end and the next shot starts
that much earlier; LATE moves a shot's start later (the shot before plays longer)."""
import json, subprocess, sys
from pathlib import Path

VO = sys.argv[1] if len(sys.argv) > 1 else "vo/voiceover_clean.wav"
HOLD = 0.6
CLIPLEN = {"S5": 6.0, "S9": 6.0}
FILE = {"S1": "clips/S1_ripple.mp4", "S2": "clips/S2_ripple.mp4"}   # free ripple boost on the water (tools/ripple.py)
SRC = {}
LATE = {"S2": 0.34}                        # S2's line runs 4.34 s on a 4 s clip: S1 plays 0.34 s longer (same water scene)
CROP = {"S5": "crop=iw*0.82:ih*0.82:iw*0.04:0,", "S2": "crop=iw*0.77:ih*0.77:iw*0.12:ih*0.23,"}   # S2: cuts the big garbled tube text at the end of the push-in   # v2 (right hand, right eye): 1.25x left/top, removes the lips at the right edge
BUZZ = ("sfx/buzz_glass_8s.wav", 0.0, "S3")      # from 0 s to the start of S3, -> under S1 + S2 only
S = json.load(open("shots.json"))["shots"]
keep = [[s["id"], s["t"][0]] for s in S]
starts = [a + LATE.get(sid, 0) for sid, a in keep]
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
bz_end = sum(d for sid, _, d in EDIT[:[e[0] for e in EDIT].index(BUZZ[2])])
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", FILE.get(c, f"clips/{c}_seedance.mp4")]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,{CROP.get(c, '')}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
# audio first, on its own (2026-10-27: loudnorm inside the amix graph dropped the last 2.9 s of the voice)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO, "-af", f"aresample=44100,loudnorm=I=-16:TP=-2.5:LRA=11,apad,atrim=0:{END:.3f}", "-ar", "44100", "out/_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/_vo.wav", "-i", BUZZ[0], "-filter_complex",
                f"[1:a]atrim=0:{bz_end:.3f},afade=t=out:st={bz_end-0.25:.3f}:d=0.25,volume=0.22,apad,atrim=0:{END:.3f}[bz];[0:a][bz]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "[a]", "-ar", "44100", "out/_mix.wav"], check=True)
adur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "out/_mix.wav"], capture_output=True, text=True).stdout)
assert abs(adur - END) < 0.05, f"audio {adur:.2f} s vs picture {END:.2f} s"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", "out/_mix.wav", "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/heveblue_v2_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/heveblue_v2_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/heveblue_v2.mp4"], check=True)
print("out/heveblue_v2.mp4", round(END, 2), "s; buzz 0 -", round(bz_end, 2))
