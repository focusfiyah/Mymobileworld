"""PRITECH face scrubber cut (2026-10-24), from ugc/youtheory-collagen/cut.py: clean clip windows on Grace's voiceover, no text, AI finish last.
  python3 cut.py   -> out/pritech_review.mp4 (veryfast) + out/pritech_v1.mp4 (AI finish)
Each shot's window = its line's time (vo.py writes shots.json "t"). Every clip plays at 1.0x. Free fixes live in the clip files:
S1c = Omni take cropped (eye/mouth out), S2_fix = first 1.1 s + played back (makeup stays), S6_final = Ralph's Flow take, 0-2.5 s + played back (no turn)."""
import json, subprocess
from pathlib import Path

VO = "vo/vo_final.wav"          # echo 150 ms after clean.py (grace/voice/echo.py)
HOLD = 0.6                      # hold the last shot a beat after the voice ends
CLIP = {"S1": "S1c", "S2": "S2_fix", "S6": "S6_final"}
SHIFT = {"S2": 0.10}            # S2 runs 0.10 s into S3's line so S3 (4.11 s of words) fits its 4.04 s clip
S = json.load(open("shots.json"))
EDIT = []
for k, s in enumerate(S):
    a, b = s["t"]; d = b - a + (HOLD if k == len(S) - 1 else 0) + SHIFT.get(s["id"], 0) - (SHIFT.get(S[k - 1]["id"], 0) if k else 0)
    f = f"clips/{CLIP.get(s['id'], s['id'])}.mp4"
    L = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    assert d <= L + 1e-3, f"{s['id']} window {d:.2f} runs past its {L:.2f} s clip"
    EDIT.append((f, d))
END = sum(e[1] for e in EDIT)
Path("out").mkdir(exist_ok=True)
inputs, chains, cum = [], [], 0.0
for i, (f, d) in enumerate(EDIT):   # frame-exact: each segment ends on round(running total * 30), so rounding never adds up (drift was 0.16 s)
    nf = round((cum + d) * 30) - round(cum * 30); cum += d
    inputs += ["-i", f]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,trim=end_frame={nf},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", VO, "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-af", f"apad,atrim=0:{END:.3f},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/pritech_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/pritech_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/pritech_v1.mp4"], check=True)
print("out/pritech_v1.mp4", round(END, 2), "s")
for (f, d), s in zip(EDIT, S): print(s["id"], f, round(d, 2))
