"""Frame sheet: frame 0 + the middle of every segment (out/<key>_plan.json). python3 sheet.py key [video]"""
import json, subprocess, sys
k = sys.argv[1]; P = json.load(open(f"out/{k}_plan.json")); v = sys.argv[2] if len(sys.argv) > 2 else f"out/{P['name']}_review.mp4"
ts, t = [0.0], 0.0
for a, b in P["segs"]: ts.append(t + (b - a) / 2); t += b - a
fr = []
for i, x in enumerate(ts):
    p = f"out/_f{i}.png"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{x:.2f}", "-i", v, "-frames:v", "1", "-vf", f"scale=270:480,drawtext=text='{x:.1f}':x=5:y=5:fontsize=24:fontcolor=yellow:box=1:boxcolor=black", p], check=True); fr.append(p)
cols = 7; ins = sum((["-i", p] for p in fr), [])
lay = "|".join(f"{(i % cols) * 270}_{(i // cols) * 480}" for i in range(len(fr)))
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f"xstack=inputs={len(fr)}:layout={lay}:fill=black", f"out/{k}_sheet.png"], check=True)
print(f"out/{k}_sheet.png", len(fr))
