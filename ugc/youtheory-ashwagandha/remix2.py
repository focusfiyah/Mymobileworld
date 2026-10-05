"""Ashwagandha v2 (Grace's notes 2026-10-04): Grace-B VO of the adult-juice-box scripts, shots matched to the words
(straw pouch on the juice-box hook, pills on the pills line, twelve pouches on "twelve"), no text, no cards, bright grades,
S1 only outside its 0.7-2.0 s pouch-to-carton morph.  python3 remix2.py -> out/final_v2/Ashwagandha <n>.mp4
Plan: remix2.json, each video = list of [clip, start, seconds]; they must add up to the VO length (vo/g<n>/windows.json).
Usable sections (frame QC 2026-10-04): H1 from 1.75 s (angled until ~1.6 s), C1 dropped (stray hand after 1.6 s, box front differs), B1/P1/X2 whole."""
import json, subprocess, os
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
ns = {}; src = open("remix.py").read(); exec(src[src.index("GRADE = {"):src.index("def run(")], ns); GRADE = ns["GRADE"]
P = json.load(open("remix2.json")); FPS = 24
def run(a): subprocess.run(["ffmpeg", "-v", "error", "-y", *a], check=True)
def length(c): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"clips/{c}.mp4"], capture_output=True, text=True).stdout)
out = Path("out/final_v2"); out.mkdir(parents=True, exist_ok=True)
for v in P["videos"]:
    W = json.load(open(f"vo/g{v['vo']}/windows.json"))["windows"]; tmp = Path(f"out/_remix2/{v['vo']}"); tmp.mkdir(parents=True, exist_ok=True)
    z, ay = v["zoom"], v["anchor"]
    crop = f"crop=iw/{z}:ih/{z}:(iw-iw/{z})/2:(ih-ih/{z})*{ay}," if z > 1.0 else ""
    vf = f"fps={FPS},{crop}scale=720:1280:flags=lanczos,setsar=1,{'unsharp=5:5:0.5,' if z > 1.0 else ''}{GRADE[v['grade']]}"
    lst = []; total = W[-1][1]
    assert abs(sum(d for _, _, d in v["segs"]) - total) < 0.06, f"{v['name']}: shots {sum(d for _,_,d in v['segs']):.2f}s vs VO {total:.2f}s"
    for k, (clip, st, d) in enumerate(v["segs"]):
        assert st + d <= length(clip) + 0.01, f"{v['name']}: {clip} from {st} needs {d}s, clip is {length(clip):.2f}s"
        f = tmp / f"{k}.mp4"; lst.append(f"file '{f.name}'\n")
        run(["-ss", str(st), "-i", f"clips/{clip}.mp4", "-t", str(d), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(f)])
    (tmp / "list.txt").write_text("".join(lst))
    run(["-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"), "-i", f"vo/g{v['vo']}/voiceover_tight.mp3", "-map", "0:v", "-map", "1:a",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(out / f"{v['name']}.mp4")])
    print(v["name"], v["segs"], "total", total)
