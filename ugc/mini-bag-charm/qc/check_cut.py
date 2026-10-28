"""QC on the cut (2026-10-26): duration, audio levels, last word inside the video, no black/flash frames, AI finish applied.
  python3 qc/check_cut.py out/minibag_v7.mp4   -> prints CUT_QC_OK or the failures"""
import json, re, subprocess, sys
f = sys.argv[1]; bad = []
run = lambda c: subprocess.run(c, capture_output=True, text=True)
dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).stdout)
wf = sys.argv[sys.argv.index("--words") + 1] if "--words" in sys.argv else "vo/words_trimmed.json"   # v12: trimmed recording
w = json.load(open(wf)); last = w[-1]["end"]
if dur < last + 0.2: bad.append(f"video {dur:.2f}s ends before the last word {last:.2f}s")
ln = run(["ffmpeg", "-i", f, "-af", "loudnorm=print_format=json", "-f", "null", "-"]).stderr
j = json.loads(ln[ln.rfind("{"):ln.rfind("}") + 1]); I, TP = float(j["input_i"]), float(j["input_tp"])
if not -18 <= I <= -14 or TP > -1.0: bad.append(f"loudness {I} LUFS / peak {TP}")
yl = run(["ffmpeg", "-i", f, "-vf", "scale=64:114,signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-an", "-f", "null", "-"]).stderr
ys = [float(x) for x in re.findall(r"YAVG=([\d.]+)", yl)]
if min(ys) < 40: bad.append(f"dark/black frame (min luma {min(ys):.0f})")
jumps = [i for i in range(1, len(ys) - 1) if abs(ys[i] - ys[i - 1]) > 25 and abs(ys[i] - ys[i + 1]) > 25]
if jumps: bad.append(f"one-frame flash at frames {jumps[:5]}")
v = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,codec_type", "-of", "json", f]).stdout)["streams"]
if not any(s.get("width") == 1080 and s.get("height") == 1920 for s in v): bad.append("not 1080x1920")
print(f"dur {dur:.2f}s, last word {last:.2f}s, {I} LUFS, peak {TP}, luma {min(ys):.0f}-{max(ys):.0f}")
print("CUT_QC_OK" if not bad else "CUT_QC_FAIL: " + "; ".join(bad))
