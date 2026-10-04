"""Free remix (Ralph 2026-10-04): every video from EXISTING clips only, no text, no product cards, no stills.
Each video: its own shot order, clip sections, framing (zoom/anchor) and colour grade, so no two look alike.
  python3 remix.py            -> out/final/<Product> <n>.mp4 for every entry in remix.json"""
import json, subprocess, os, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; os.chdir(HERE)
J = json.load(open("shots.json")); R = json.load(open("remix.json")); FPS = 24
GRADE = {"natural": "eq=saturation=1.02",                                   # daylight
         "warm": "colortemperature=temperature=3300:mix=0.85,eq=saturation=1.12:brightness=0.02,curves=all='0/0.04 0.5/0.52 1/0.96'",   # golden hour
         "cool": "colortemperature=temperature=8500:mix=0.7,eq=contrast=1.03:saturation=0.95:brightness=0.04",                          # bright, cool daylight
         "moody": "eq=brightness=0.06:contrast=1.06:saturation=1.18,curves=all='0/0.03 0.5/0.56 1/1'"}  # bright, punchy (Ralph 2026-10-04: no dark looks)
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def windows(v):
    if v == 1: return [s["t"] for s in J["shots"]], "vo/voiceover_tight.mp3"
    return json.load(open(f"vo/v{v}/windows.json"))["windows"], f"vo/v{v}/voiceover_tight.mp3"
out_dir = Path("out/final"); out_dir.mkdir(parents=True, exist_ok=True)
for vid in R["videos"]:
    W, VO = windows(vid["vo"]); total = W[-1][1]; bounds = [w[0] for w in W[1:]]
    pool = R["pool"]; segs = []
    end_seg = pool[vid["end"]]; last = W[-1][1] - W[-1][0]
    t_end = total - min(last, end_seg[2] - end_seg[1])   # closing (point) clip covers the CTA line
    c = 0.0
    for name in vid["order"]:
        if t_end - c < 0.8: break   # never a flash cut: the closing clip grows to cover a short gap
        clip, a, b = pool[name]; L = b - a
        cands = [x for x in bounds if max(c + 1.0, c + L - 0.6) < x <= c + L + 1e-6 and x < t_end]   # snap to a line start only if it wastes < 0.6 s
        e = max(cands) if cands and (c + L < t_end) else min(c + L, t_end)
        segs.append((clip, a, round(e - c, 3))); c = e
    if t_end - c > 0.05:
        if (end_seg[2] - end_seg[1]) >= total - c: t_end = c
        else: sys.exit(f"{vid['name']}: footage short by {t_end - c:.2f}s")
    segs.append((end_seg[0], end_seg[1], round(total - t_end, 3)))
    z, ay = vid.get("zoom", 1.0), vid.get("anchor", 0.5)
    crop = f"crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})*{ay}," if z > 1.0 else ""
    vf = f"fps={FPS},{crop}scale=720:1280:flags=lanczos,setsar=1,{'unsharp=5:5:0.5,' if z > 1.0 else ''}{GRADE[vid['grade']]}"
    tmp = Path(f"out/_remix/{vid['name']}"); tmp.mkdir(parents=True, exist_ok=True); lst = []
    for k, (clip, a, d) in enumerate(segs):
        f = tmp / f"{k}.mp4"; lst.append(f"file '{f.name}'\n")
        run(["-ss", str(a), "-i", f"clips/{clip}.mp4", "-t", str(d), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(f)])
    (tmp / "list.txt").write_text("".join(lst))
    o = out_dir / f"{vid['name']}.mp4"
    run(["-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-i", VO, "-map", "0:v", "-map", "1:a",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(o)])
    print(o.name, vid["grade"], z, [(s[0], s[1], s[2]) for s in segs], "total", round(total, 2))
