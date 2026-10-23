"""QC for the final cut (run from the repo root): python3 ugc/shnuggle-next-bath/qc/cut_qc.py [file]. Prints one line per check
and 'CUT QC PASS' only if all pass. Checks: duration 25-35 s, video = audio length, loudness -16 +/-1 LUFS, every hard cut lands on a
shot boundary from shots.json (+/-0.1 s), no extra cuts (a jump inside a shot = a clip redrawing itself), no black frames, no
single-frame flashes (a luma spike up and back down)."""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np
JOB = Path(__file__).resolve().parents[1]; F = Path(sys.argv[1]) if len(sys.argv) > 1 else JOB / "out/shnuggle_next_bath.mp4"
S = json.loads((JOB / "shots.json").read_text())["shots"]; bad = []
run = lambda c: subprocess.run(c, capture_output=True, text=True)
def chk(name, ok, info): print(("PASS " if ok else "FAIL ") + name + ": " + info); ok or bad.append(name)
dur = lambda kind: float(run(["ffprobe", "-v", "error", "-select_streams", kind, "-show_entries", "stream=duration", "-of", "csv=p=0", str(F)]).stdout)
dv, da = dur("v:0"), dur("a:0")
chk("duration", 25 <= dv <= 35, f"{dv:.2f} s"); chk("av_sync", abs(dv - da) < 0.1, f"video {dv:.2f} / audio {da:.2f}")
lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", run(["ffmpeg", "-nostats", "-i", str(F), "-af", "ebur128", "-f", "null", "-"]).stderr)[-1])
chk("loudness", abs(lufs + 16) <= 1, f"{lufs} LUFS")
p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(F), "-vf", "fps=30,scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True)
fr = np.frombuffer(p.stdout, np.uint8).reshape(-1, 96, 54).astype(np.float32); y = fr.reshape(len(fr), -1).mean(1)
d = np.abs(np.diff(fr, axis=0)).mean((1, 2))   # frame-to-frame change; a hard cut is a spike well above its neighbours
med = np.array([np.median(d[max(0, i - 8):i + 9]) for i in range(len(d))])
cuts = [(i + 1) / 30 for i in range(len(d)) if d[i] > 20 and d[i] > 3 * med[i]]   # real cuts here measure 33-58; motion + 24->30 fps cadence + grain stay under 11
bounds = [s["t"][0] for s in S[1:]]
found = [b for b in bounds if any(abs(c - b) <= 0.1 for c in cuts)]
punch = [(round(s["t"][0] * 30) + (round(s["t"][1] * 30) - round(s["t"][0] * 30)) // 2) / 30 for s in S if s.get("punch")]   # planned mid-shot punch-ins (cut.py)
extra = [c for c in cuts if min(abs(c - b) for b in bounds + punch) > 0.1]
chk("cuts_found", len(found) >= len(bounds) - 1, f"{len(found)} of {len(bounds)} shot boundaries show a cut (positive control)")
chk("no_extra_jumps", not extra, f"{len(cuts)} jumps ({len(punch)} planned punch-ins allowed), unplanned at {[round(c, 2) for c in extra]}")
chk("no_black", y.min() > 20, f"darkest frame mean luma {y.min():.1f}")
spike = [i for i in range(1, len(y) - 1) if abs(y[i] - y[i - 1]) > 18 and abs(y[i] - y[i + 1]) > 18 and np.sign(y[i] - y[i - 1]) == np.sign(y[i] - y[i + 1])]
chk("no_flash", not spike, f"single-frame luma spikes at frames {spike[:5]}")
print("CUT QC PASS" if not bad else f"CUT QC FAIL: {bad}")
