"""QC for out/V12_final.mp4 (2026-10-24, from ugc/jiyu-polish-pads/qc/check.py): prints CHECK_OK only if all pass.
flash: every detected scene cut sits on a planned clip boundary (+-0.08 s); black: no black frames; size 1080x1920;
duration = sum of EDIT windows; audio: a silent track exists (music-only, Grace adds the sound); jump: max frame-to-frame
brightness jump inside clips <= 3/255 (no flicker)."""
import re, subprocess, sys
import numpy as np
sys.path.insert(0, "."); from cut import EDIT
F = "out/V12_final.mp4"; bad = []
run = lambda c: subprocess.run(c, capture_output=True, text=True)
ed = EDIT["V12"]; bounds, t = [], 0.0
for e in ed[:-1]: t += e[2] - e[1]; bounds.append(round(t, 2))
dur = sum(e[2] - e[1] for e in ed)
out = run(["ffmpeg", "-i", F, "-vf", "scale=108:192,select='gt(scene,0.25)',metadata=print:file=-", "-an", "-f", "null", "-"]).stdout
cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", out)]
stray = [c for c in cuts if min(abs(c - b) for b in bounds) > 0.08]
if stray: bad.append(f"flash: cuts off the boundaries at {stray}")
if re.findall(r"black_start", run(["ffmpeg", "-i", F, "-vf", "blackdetect=d=0.05:pic_th=0.95", "-an", "-f", "null", "-"]).stderr): bad.append("black frames")
wh = run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", F]).stdout.strip()
if wh != "1080,1920": bad.append(f"size {wh}")
d = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", F]).stdout)
if abs(d - dur) > 0.1: bad.append(f"duration {d} vs {dur}")
if "audio" not in run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", F]).stdout: bad.append("no audio track")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", F, "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
m = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).mean((1, 2)); j = np.abs(np.diff(m)); fps = len(m) / d
inside = [k for k in range(len(j)) if min(abs((k + 1) / fps - b) for b in bounds) > 0.1]
mj = max(j[k] for k in inside)
if mj > 3: bad.append(f"flicker: jump {mj:.1f} at {(inside[int(np.argmax([j[k] for k in inside]))] + 1) / fps:.2f}s")
print(f"cuts {cuts} vs boundaries {bounds}; duration {d}; max in-clip jump {mj:.2f}")
print("\n".join(bad) if bad else "CHECK_OK")
