"""Render the 10 edits from out/plan.json. python3 cut.py [V numbers...] [--preset veryfast]. Hard cuts, silent (Grace adds music in TikTok).
Fast seek per shot; zoom = centre crop then lanczos back to 1080x1920 (<=1.08x)."""
import subprocess, sys, json, os
SRC = {"A": "orig/A.mov", "B": "orig/B.mov"}
args = sys.argv[1:]; preset = "veryfast"
if "--preset" in args: i = args.index("--preset"); preset = args[i+1]; del args[i:i+2]
plan = json.load(open("out/plan.json")); want = {int(a) for a in args} or {p["video"] for p in plan}
for p in plan:
    if p["video"] not in want: continue
    ins, f = [], ""; z = p["zoom"]
    for i, s in enumerate(p["shots"]):
        ins += ["-ss", f"{s['start']:.3f}", "-t", f"{s['dur']+0.1:.3f}", "-i", SRC[s["src"]]]
        crop = f"crop=iw/{z}:ih/{z}," if z > 1 else ""
        f += (f"[{i}:v]setpts=PTS-STARTPTS,fps=30,trim=end_frame={round(s['dur']*30)},{crop}scale=1080:1920:flags=lanczos,setsar=1,"
              f"{'hflip,' if s['flip'] else ''}{p['grade']}[v{i}];")
    n = len(p["shots"]); f += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[out]"
    out = f"out/necklace_V{p['video']}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f, "-map", "[out]", "-an", "-c:v", "libx264", "-preset", preset,
                    "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-threads", "4", out], check=True)
    print(out)
