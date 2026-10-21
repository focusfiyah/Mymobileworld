"""Cut a 15 s remix (2026-10-20): edits.json video N over vo/vN.mp3. Each shot starts on its anchor word (first match
after the previous anchor, from vo/vN_words.json), cut in the gap before the word; clips at 1.0x, never stretched.
Real-label clips from ../clips_label. Grades are bright only (no dark/yellow). No text, no music.
  python3 cut.py N [--final]   (--final = libx264 medium + ai_finish.sh; default = veryfast review render)"""
import difflib, json, re, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; C = H.parent
N = sys.argv[1]; E = json.load(open(H / "edits.json"))[N]
W = json.load(open(H / f"vo/v{N}_words.json"))
GRADE = {"natural": "eq=saturation=1.02", "neutral": "eq=contrast=1.05:saturation=1.04:brightness=0.03",
         "cool": "colortemperature=temperature=7500:mix=0.6,eq=contrast=1.03:brightness=0.04",
         "punchy": "eq=brightness=0.05:contrast=1.06:saturation=1.10"}
LABEL = {"S1", "S5", "S7", "S8", "S9", "N4"}
PRE = {"N3": "crop=562:1000:80:40,", "V2e": "crop=350:622:110:10,", "V4d1": "crop=350:622:0:210,"}   # brows: mouth cropped out (no still mouth on screen during the VO)
norm = lambda t: re.sub(r"[^a-z']", "", t.lower().replace("’", "'"))
aud = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(H / f"vo/v{N}.mp3")], capture_output=True, text=True).stdout)
starts, j = [], 0
for k, a, word in E["shots"]:
    while not (norm(W[j]["text"]) == norm(word) or len(word) > 4 and difflib.SequenceMatcher(None, norm(W[j]["text"]), norm(word)).ratio() >= 0.75): j += 1   # fuzzy only for long words ("Caster")
    starts.append(0.0 if not starts else round((W[j - 1]["end"] + W[j]["start"]) / 2, 3)); j += 1
ends = starts[1:] + [aud]
for i, (k, a, word) in enumerate(E["shots"][:-1]):   # a clip up to 0.15 s short of its line: move the cut that much earlier (into the pause before the next word)
    src = H / "redo/clips" / f"{k}.mp4"
    if src.exists():
        cl = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout) - 0.005
        over = a + ends[i] - starts[i] - cl
        if 0 < over <= 0.15: ends[i] -= over; starts[i + 1] -= over
z = E["zoom"]; zf = f"scale=iw*{z}:ih*{z},crop=720:1280," if z > 1 else ""
ins, f, plan = [], "", []
for i, ((k, a, word), s, e) in enumerate(zip(E["shots"], starts, ends)):
    src = H / "redo/clips" / f"{k}.mp4" if (H / "redo/clips" / f"{k}.mp4").exists() else C / ("clips_label" if k in LABEL else "clips") / f"{k}.mp4"
    cl = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout)
    d = e - s; assert d >= 0.6, f"v{N} {k}: {d:.2f}s shot reads as a flash"; assert a + d <= cl + 0.01, f"v{N} {k}: {a}+{d:.2f}s > clip {cl:.2f}s (never stretch)"
    plan.append(f"{s:6.2f}-{e:5.2f} {k} @{a} '{word}'")
    ins += ["-i", str(src)]
    a0, L = round(a * 30), round(e * 30) - round(s * 30)   # whole output frames, so cuts land exactly on the planned word gaps (no drift)
    f += f"[{i}:v]fps=30,trim=start_frame={a0}:end_frame={a0 + L},setpts=PTS-STARTPTS,{PRE.get(k, '')}scale=720:1280,{zf}scale=1080:1920:flags=lanczos,{GRADE[E['grade']]},format=yuv420p[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(E["shots"]))) + f"concat=n={len(E['shots'])}:v=1:a=0[v]"
final = "--final" in sys.argv
out = H / f"out/remix15_v{N}{'_pre' if final else '_review'}.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-i", str(H / f"vo/v{N}.mp3"), "-filter_complex", f, "-map", "[v]", "-map", f"{len(ins)//2}:a",
                "-c:v", "libx264", "-preset", "medium" if final else "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)], check=True)
if final:
    subprocess.run(["bash", str(H.parents[2] / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"), str(out), str(H / f"out/remix15_v{N}_final.mp4")], check=True)
json.dump({"starts": starts, "shots": [k for k, *_ in E["shots"]], "audio": aud}, open(H / f"out/remix15_v{N}_plan.json", "w"))
print("\n".join(plan)); print("wrote", out)
