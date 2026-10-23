"""Youtheory Collagen cut v2 (2026-10-22; S3 = real box print, tracked): clean clip windows on Grace's voiceover, no text, AI finish last.
  python3 cut.py            -> out/youtheory_collagen_review.mp4 (veryfast) + out/youtheory_collagen_v2.mp4 (AI finish)
Each shot's window = its line's time in vo/words_trimmed.json (vo.py writes shots.json "t"); SRC = where in the clip it starts
(clean footage only, QC 2026-10-22). Every clip plays at 1.0x."""
import json, subprocess
from pathlib import Path

VO = "vo/voiceover_paced.mp3"
HOLD = 0.6                      # hold the last shot a beat after the voice ends
SRC = {"S5b": 0.0}             # shot -> source start (s); S5b: only before 1.5 s (the arm crosses the pouch after 2 s)
SPLIT = {"S7": [(0.0, 1.48), (4.55, None)]}
SHIFT = {"S6": 0.56}            # S6 runs this much into the next line ("And the individual packets" over the vanity pouch) so S7 fits its clean footage   # S7: a second hand enters at 1.6 s and both hands are leaving by 4.5 s; cut it out (jump cut)
S = json.load(open("shots.json"))["videos"][0]["shots"]
EDIT = []
for k, s in enumerate(S):
    a, b = s["t"]; d = b - a + (HOLD if k == len(S) - 1 else 0) + SHIFT.get(s["id"], 0) - (SHIFT.get(S[k - 1]["id"], 0) if k else 0)
    if s["id"] in SPLIT:
        (a1, l1), (a2, _) = SPLIT[s["id"]]; l2 = d - l1
        assert a2 + l2 <= s["seconds"] + 1e-6, f"{s['id']} tail runs past the clip"
        EDIT += [(s["id"], a1, l1), (s["id"], a2, l2)]; continue
    ss = SRC.get(s["id"], 0.0)
    assert ss + d <= s["seconds"] + 1e-6, f"{s['id']} window {ss}+{d:.2f} runs past its {s['seconds']} s clip"
    EDIT.append((s["id"], ss, d))
END = sum(e[2] for e in EDIT)
Path("out").mkdir(exist_ok=True)
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f"clips/{c}.mp4"]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-af", f"apad,atrim=0:{END:.3f},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/youtheory_collagen_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/youtheory_collagen_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/youtheory_collagen_v2.mp4"], check=True)
print("out/youtheory_collagen_v2.mp4", round(END, 2), "s")
