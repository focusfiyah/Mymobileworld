"""QC for a House of Rameau version of an approved Grace cut (2026-11-15 HofR batch: Cleanwaste, BodyJ, PRITECH, Vans).
Copied from houseoframeau/posts/pritech-v3/qc.py and made generic.
  python3 hor_qc.py HOR.mp4 GRACE.mp4 HOOKBOX.json [sheet OUT.jpg EDIT.json]
Prints PASS/FAIL per check and ends with QC_OK or QC_FAIL:
  basic     1080x1920, has audio, length >= 15 s and within 1.5 s of Grace's cut, integrated loudness -16.5..-13.5 LUFS
  hook      tools/hookcheck/hook_check.py on the card box must print HOOK_OK (whole hook in frame 0, held >= 2 s)
  different mean abs diff vs Grace's cut at 8 sample times >= 12 each (her own threshold from pritech-v3)
  grade     average luma >= Grace's and blue-minus-red no lower than hers - 3 (brighter, cool-neutral, never golden)
sheet: frame 0 + the middle of each shot (EDIT.json list of {at, len}) on one contact sheet to look at."""
import json, subprocess, sys
from pathlib import Path
import numpy as np

HOR, REF, BOX = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
ROOT = Path(__file__).resolve().parents[3]
bad = []
def probe(f, k): return subprocess.run(["ffprobe", "-v", "error", *k, "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
def frame(f, t, w=270, h=480):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(float)
def res(name, ok, msg):
    print("PASS" if ok else "FAIL", name, msg)
    if not ok: bad.append(name)

wh = probe(HOR, ["-select_streams", "v", "-show_entries", "stream=width,height"])
d, dr = float(probe(HOR, ["-show_entries", "format=duration"])), float(probe(REF, ["-show_entries", "format=duration"]))
a = probe(HOR, ["-select_streams", "a", "-show_entries", "stream=codec_name"])
ebu = subprocess.run(["ffmpeg", "-i", HOR, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
lufs = float(ebu.rsplit("I:", 1)[1].split("LUFS")[0])
res("basic", wh == "1080,1920" and bool(a) and d >= 15 and abs(d - dr) <= 1.5 and -16.5 <= lufs <= -13.5, f"{wh} {d:.2f}s (Grace {dr:.2f}s) {a} {lufs} LUFS")

hc = subprocess.run(["python3", str(ROOT / "tools/hookcheck/hook_check.py"), HOR, "--hook", BOX["box"], "--hold", str(min(2.0, BOX.get("hold", 2.0) - 0.2))], capture_output=True, text=True).stdout
res("hook", "HOOK_OK" in hc, hc.strip().replace("\n", " | "))

ts = np.linspace(0.5, min(d, dr) - 0.5, 8)
diffs = [float(np.mean(np.abs(frame(HOR, t) - frame(REF, t)))) for t in ts]
res("different", min(diffs) >= 12, f"min {min(diffs):.1f} at 8 times {[round(x, 1) for x in diffs]}")

ts = np.linspace(0.5, min(d, dr) - 0.5, 10)
A = np.mean([frame(HOR, t).reshape(-1, 3).mean(0) for t in ts], 0); B = np.mean([frame(REF, t).reshape(-1, 3).mean(0) for t in ts], 0)
la, lb = A @ [.299, .587, .114], B @ [.299, .587, .114]
res("grade", la >= lb and (A[2] - A[0]) >= (B[2] - B[0]) - 3, f"luma {la:.1f} vs {lb:.1f}, b-r {A[2]-A[0]:.1f} vs {B[2]-B[0]:.1f}")

if len(sys.argv) > 5 and sys.argv[4] == "sheet":
    edit = json.load(open(sys.argv[6]))
    times = [0.0] + [e["at"] + e["len"] / 2 for e in edit]
    tmp = Path(sys.argv[5]).with_suffix(""); tmp.mkdir(exist_ok=True)
    for i, t in enumerate(times):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", HOR, "-frames:v", "1", "-vf", "scale=270:480", str(tmp / f"f{i:02d}.png")], check=True)
    cols = min(len(times), 7)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "f%02d.png"), "-vf", f"tile={cols}x{-(-len(times) // cols)}", "-frames:v", "1", sys.argv[5]], check=True)
    print("sheet", sys.argv[5], "times", [round(t, 2) for t in times])
print("QC_OK" if not bad else "QC_FAIL " + ",".join(bad))
sys.exit(1 if bad else 0)
