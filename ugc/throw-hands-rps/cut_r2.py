"""Free cut: 9 hands-only clips on the trimmed Grace B voiceover, no text overlay (Ralph has not asked for one).

  python3 cut.py [tag]   -> out/throw_hands_<tag>_raw.mp4 (720x1280, 24fps); then ai_finish.sh -> out/throw_hands_<tag>.mp4

Windows come from shots.json "t" (vo.py). Every shot is real clip footage at 1.0x (no holds, no Ken Burns).
PARTS: which clip and which seconds fill each window. S4 (Hailuo) skips 0.85-3.35s (crumpled cards, then a stray long arm crosses the table).
S9's line is 6.65s but its clip is 6s: "Girls," is cut from the voiceover (CUT_A..CUT_B, free) instead of paying for a longer clip.
S8 (Hailuo) has the box stand up by itself after 1.3s, so its window is filled with S8 0-1.3 (gathering), S7 3.9-4.5 (open hands)
and S5 3.6-end (a new round slap). S1, S3 and S9 use the *_fixed clips (real box pasted back frame by frame, boxfix.py).
"""
import json, subprocess, sys
from pathlib import Path

tag = sys.argv[1] if len(sys.argv) > 1 else "r1"
J = json.loads(Path("shots.json").read_text())
T = {s["id"]: list(s["t"]) for s in J["shots"]}
CUT_A, CUT_B, END = 23.40, 24.00, 29.97      # drop "Girls," and 0.1s of the end tail
T["S8"][1] = CUT_A; T["S9"] = [CUT_A, END - (CUT_B - CUT_A)]
T["S3"][1] = T["S4"][0] = round(T["S4"][0] + 0.31, 2)   # S3 holds the box 0.31s longer so S4 can skip the stray arm
H = "clips_hailuo/"; S = "clips/"; V = "clips_veo/"
PARTS = {  # shot -> [(file, start)] in order; the last part runs to fill the window
    "S1": [(S + "S1_fixed.mp4", 0)], "S2": [(S + "S2.mp4", 0)], "S3": [(S + "S3_fixed2.mp4", 0)],
    "S4": [(H + "S4.mp4", 0, 0.85), (H + "S4.mp4", 3.35)],
    "S5": [(V + "S5.mp4", 0, 0.67), (V + "S5.mp4", 3.85)], "S6": [(S + "S6.mp4", 0)], "S7": [(H + "S7.mp4", 4.0)],
    "S8": [(H + "S8.mp4", 0, 1.3), (H + "S4.mp4", 0.85, 1.35), (H + "S5.mp4", 4.2)], "S9": [(S + "S9_fixed.mp4", 0)],
}
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
inputs, chains, labels, k = [], [], [], 0
for s in J["shots"]:
    sid = s["id"]; left = T[sid][1] - T[sid][0]
    for j, p in enumerate(PARTS[sid]):
        f, a = p[0], p[1]; last = j == len(PARTS[sid]) - 1
        d = left if last else p[2]
        assert a + d <= dur(f) + 0.03, f"{sid} needs {a}+{d:.2f}s of {f} ({dur(f):.2f}s)"
        inputs += ["-i", f]
        chains.append(f"[{k}:v]trim=start={a}:duration={d:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[v{k}]")
        labels.append(f"[v{k}]"); k += 1; left -= d
    print(sid, round(T[sid][0], 2), round(T[sid][1], 2), [p[0] for p in PARTS[sid]])
total = T["S9"][1]
chains.append(f"{''.join(labels)}concat=n={k}:v=1:a=0,format=yuv420p[vout]")
inputs += ["-i", "vo/voiceover_tight.mp3"]
chains.append(f"[{k}:a]asplit[a1][a2];[a1]atrim=0:{CUT_A},afade=t=out:st={CUT_A - 0.01}:d=0.01[p1];[a2]atrim={CUT_B}:{END},asetpts=PTS-STARTPTS,afade=t=in:d=0.01[p2];"
              f"[p1][p2]concat=n=2:v=0:a=1,apad,atrim=duration={total},loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True); out = f"out/throw_hands_{tag}_raw.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains), "-map", "[vout]", "-map", "[aout]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads", "4", "-c:a", "aac", "-b:a", "160k",
                "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out, total)
