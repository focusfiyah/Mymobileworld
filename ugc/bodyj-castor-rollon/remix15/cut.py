"""Cut a 15 s remix (2026-10-20): edits.json video N over vo/vN.mp3. Each shot starts on its anchor word (first match
after the previous anchor, from vo/vN_words.json), cut in the gap before the word; clips at 1.0x, never stretched.
Real-label clips from ../clips_label. Grades are bright only (no dark/yellow). No text, no music.
  python3 cut.py N [--final]   (--final = libx264 medium + ai_finish.sh; default = veryfast review render)"""
import json, re, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; C = H.parent
N = sys.argv[1]; E = json.load(open(H / "edits.json"))[N]
W = json.load(open(H / f"vo/v{N}_words.json"))
GRADE = {"natural": "eq=saturation=1.02", "neutral": "eq=contrast=1.05:saturation=1.04:brightness=0.03",
         "cool": "colortemperature=temperature=7500:mix=0.6,eq=contrast=1.03:brightness=0.04",
         "punchy": "eq=brightness=0.05:contrast=1.06:saturation=1.10"}
LABEL = {"S1", "S5", "S7", "S8", "S9", "N4"}
PRE = {"N3": "crop=562:1000:80:40,"}   # brows: lips cropped out (no talking mouth during the VO)
norm = lambda t: re.sub(r"[^a-z']", "", t.lower().replace("’", "'"))
aud = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(H / f"vo/v{N}.mp3")], capture_output=True, text=True).stdout)
starts, j = [], 0
for k, a, word in E["shots"]:
    while norm(W[j]["text"]) != norm(word): j += 1
    starts.append(0.0 if not starts else round((W[j - 1]["end"] + W[j]["start"]) / 2, 3)); j += 1
ends = starts[1:] + [aud]
z = E["zoom"]; zf = f"scale=iw*{z}:ih*{z},crop=720:1280," if z > 1 else ""
ins, f, plan = [], "", []
for i, ((k, a, word), s, e) in enumerate(zip(E["shots"], starts, ends)):
    d = e - s; assert a + d <= 5.04, f"v{N} {k}: {a}+{d:.2f}s > clip (never stretch)"
    plan.append(f"{s:6.2f}-{e:5.2f} {k} @{a} '{word}'")
    ins += ["-i", str(C / ("clips_label" if k in LABEL else "clips") / f"{k}.mp4")]
    f += f"[{i}:v]trim={a}:{a + d:.3f},setpts=PTS-STARTPTS,{PRE.get(k, '')}scale=720:1280,{zf}scale=1080:1920:flags=lanczos,fps=30,{GRADE[E['grade']]},format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(E["shots"]))) + f"concat=n={len(E['shots'])}:v=1:a=0[v]"
final = "--final" in sys.argv
out = H / f"out/remix15_v{N}{'_pre' if final else '_review'}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", str(H / f"vo/v{N}.mp3"), "-filter_complex", f, "-map", "[v]", "-map", f"{len(ins)//2}:a",
                "-c:v", "libx264", "-preset", "medium" if final else "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
if final:
    subprocess.run(["bash", str(H.parents[2] / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"), str(out), str(H / f"out/remix15_v{N}_final.mp4")], check=True)
print("\n".join(plan)); print("wrote", out)
