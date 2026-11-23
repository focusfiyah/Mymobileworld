"""QC for a HofR version (GATES.md). python3 qc.py KEY [final]  -> prints QC_OK KEY or QC_FAIL ...
basic: 1080x1920, >= 15 s and = plan length, audio present, -16..-14 LUFS. hook: tools/hookcheck HOOK_OK on the card box.
different: every frame differs from Grace's cut at 8 sample times (mean abs diff >= 12, houseoframeau/posts/pritech-v3/qc.py)."""
import json, os, re, subprocess, sys
import numpy as np
from pathlib import Path
k = sys.argv[1]; P = json.load(open(f"out/{k}_plan.json"))
OUT = f"out/{P['name']}.mp4" if "final" in sys.argv else f"out/{P['name']}_review.mp4"
REF = str(Path(os.environ.get("HOFR_SRC", "/tmp/claude-0/-home-user-Mymobileworld/51ac50b9-7e30-5689-9468-bfbffe972254/scratchpad/grace")) / f"{k}.mp4")
def probe(f, a): return subprocess.run(["ffprobe", "-v", "error", *a, "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
def frame(f, t, w=270, h=480):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(float)
bad = []
wh = probe(OUT, ["-select_streams", "v", "-show_entries", "stream=width,height"]); d = float(probe(OUT, ["-show_entries", "format=duration"]))
a = probe(OUT, ["-select_streams", "a", "-show_entries", "stream=codec_name"])
ll = subprocess.run(["ffmpeg", "-i", OUT, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", ll)[-1])
if wh != "1080,1920" or d < 15 or abs(d - P["len"]) > 0.15 or not a or not -16.2 <= lufs <= -13.8: bad.append(f"basic {wh} {d:.2f}s {a} {lufs} LUFS")
x, y, w, h = P["hook_box"]
hk = subprocess.run(["python3", "/home/user/Mymobileworld/tools/hookcheck/hook_check.py", OUT, "--hook", f"{x},{y},{w},{h}", "--hold", "2.0"], capture_output=True, text=True).stdout
if "HOOK_OK" not in hk: bad.append("hook " + hk.strip())
ts = np.linspace(0.4, d - 0.6, 8)
diffs = [float(np.mean(np.abs(frame(OUT, t) - frame(REF, t)))) for t in ts]
if min(diffs) < 12: bad.append(f"different {[round(v, 1) for v in diffs]}")
print(("QC_FAIL " + " | ".join(bad)) if bad else "QC_OK", k, wh, f"{d:.2f}s", f"{lufs} LUFS", "min diff", round(min(diffs), 1), hk.strip().split("\n")[-1][:80])
sys.exit(1 if bad else 0)
