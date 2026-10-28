"""Mini Bag Charm cut (2026-10-27), from ugc/monbix-remy-comforter/cut.py: clean clip windows on Grace's voiceover,
no text, AI finish last. Every clip plays at 1.0x (Seedance 2.0 Mini first-frame clips, 4/5/6 s).
  python3 cut.py   -> out/minibag_v11_review.mp4 (veryfast) + out/minibag_v11.mp4 (AI finish)
Shot windows come from vo.py (shots.json "t"). Dropped shots (S5) hand their time to the next shot; a window longer than
its clip ends at the clip's end and the next shot starts that much earlier. SRC = where in the clip a window starts (QC)."""
import json, subprocess
from pathlib import Path

VO, HOLD = "vo/voiceover_paced.mp3", 0.6
CLIPLEN = {"S9": 6.0}
USE = {}                                   # v2: S1 r3 clip is clean from 1.0 s (SRC)
FILE = {"S1": "clips/S1_nokey.mp4", "S4": "clips/S4N_track.mp4", "S7": "clips/S7N_track.mp4", "S8": "clips/S8L_track_rev.mp4", "S9": "clips/S9_track.mp4"}   # v4 (Grace 2026-10-27): real charm laid on each frame (Ralph OK), S1 Omni with the added key painted out
SRC = {"S8": 0.64}                                   # v4: every clip from 0 (S5a uses its clean first 1.66 s)
LATE = {}
CROP = {}                                  # S9 r2 (2026-10-26, Ralph: lie along the bed) needs no crop; r1 needed one to hide toes
S = json.load(open("shots.json"))["shots"]
keep = []
for s in S:                                # a dropped shot's line goes to the next kept shot
    if s.get("dropped"): nxt_start = s["t"][0]; continue
    a = locals().pop("nxt_start", None)
    keep.append([s["id"], a if a is not None else s["t"][0]])
starts = [a + LATE.get(sid, 0) for sid, a in keep]
END_VO = S[-1]["t"][1]
EDIT, pos = [], 0.0
for k, (sid, a) in enumerate(keep):
    b = starts[k + 1] if k + 1 < len(keep) else END_VO + HOLD
    d = b - pos; ss = SRC.get(sid, 0.0)
    clip = USE.get(sid, CLIPLEN.get(sid, 4.0))
    if ss + d > clip:                      # end at the clean end; the next shot starts earlier
        d = clip - ss
    EDIT.append((sid, ss, d)); pos += d
assert abs(pos - (END_VO + HOLD)) < 0.02 , f"edit {pos:.2f} vs vo {END_VO + HOLD:.2f}"
for e in EDIT: print(e[0], f"src {e[1]:.2f}", f"len {e[2]:.2f}")
END = pos
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", FILE.get(c, f"clips/{c}_seedance.mp4")]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,{CROP.get(c, '')}scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-af", f"apad,atrim=0:{END:.3f},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/minibag_v11_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/minibag_v11_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/minibag_v11.mp4"], check=True)
print("out/minibag_v11.mp4", round(END, 2), "s")
