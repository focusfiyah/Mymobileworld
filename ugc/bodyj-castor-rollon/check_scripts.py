"""Gate checks for this job (GATES.md G2, G3, G7). Run from the job folder."""
import re, subprocess, sys, json
s = open("scripts.md").read()
opts = re.findall(r"## Option (\w)[^\n]*\n(.*?)(?=\n## |\Z)", s, re.S)
def lines(b): return [l.strip() for l in b.strip().splitlines() if l.strip()]
if "--cut" in sys.argv:
    f = sys.argv[sys.argv.index("--cut") + 1]
    o = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", f], capture_output=True, text=True).stdout)
    w, h, d = o["streams"][0]["width"], o["streams"][0]["height"], float(o["format"]["duration"])
    print("CUT_OK" if (w, h) == (1080, 1920) and 20 <= d <= 40 else f"CUT_BAD {w}x{h} {d:.1f}s"); sys.exit()
bad = []
if len(opts) != 3: bad.append(f"{len(opts)} options, want 3")
for k, b in opts:
    L = lines(b)
    cc = [i for i, l in enumerate(L) if "cradle cap" in l.lower()]
    if len(cc) != 1 or cc[0] > 1: bad.append(f"{k}: cradle cap in lines {cc}")
    if not L[-1].endswith("It's in the orange cart."): bad.append(f"{k}: close")
    if "--grade" in sys.argv:
        out = subprocess.run(["python3", "../../.claude/skills/tiktok-shop-coach/scripts/tiktok.py", "readability", " ".join(L)], capture_output=True, text=True).stdout
        g = float(re.search(r"grade[^0-9]*([0-9.]+)", out, re.I).group(1))
        print(k, "grade", g, len(" ".join(L).split()), "words")
        if g > 6: bad.append(f"{k}: grade {g}")
print(("GRADE_OK" if "--grade" in sys.argv else "SCRIPTS_OK") if not bad else "FAIL " + "; ".join(bad))
