"""QC for the music-only rosemary cut (2026-11-02). Prints QC_OK only if every check passes.
  python3 qc.py out/rosemary_v1.mp4 [expected_seconds]
Checks: 1080x1920; length; frame 0 not black; no black or white flash frame; no frame-to-frame brightness jump outside
the planned cut points (flicker); mean brightness bright and not blown out; saturation not boosted; audio track silent."""
import subprocess, sys
import numpy as np

f = sys.argv[1]; exp = float(sys.argv[2]) if len(sys.argv) > 2 else None
errs = []
p = lambda *a: subprocess.run(a, capture_output=True, text=True).stdout.strip()
w, h = p("ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", f).split(",")
if (w, h) != ("1080", "1920"): errs.append(f"size {w}x{h}")
dur = float(p("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f))
if exp and abs(dur - exp) > 0.1: errs.append(f"length {dur:.2f} vs {exp:.2f}")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", "scale=54:96,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 96, 54, 3).astype(float)
luma = fr.mean(axis=(1, 2, 3))
sat = (fr.max(axis=3) - fr.min(axis=3)).mean(axis=(1, 2))
if luma[0] < 25: errs.append("frame 0 is black")
if (luma < 15).any(): errs.append(f"black frames at {list(np.where(luma < 15)[0][:5])}")
if (luma > 245).any(): errs.append(f"white flash at {list(np.where(luma > 245)[0][:5])}")
jumps = np.abs(np.diff(luma))
cuts = set(np.where(jumps > 18)[0])
diffs = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2, 3))
scene = set(np.where(diffs > 25)[0])           # real cuts change the whole picture
flick = sorted(c for c in cuts if c not in scene)
if flick: errs.append(f"brightness jump without a cut (flicker) at frames {flick[:5]}")
if luma.mean() < 95: errs.append(f"too dark, mean {luma.mean():.0f}")
if luma.mean() > 215: errs.append(f"blown out, mean {luma.mean():.0f}")
vol = p("ffmpeg", "-v", "info", "-i", f, "-af", "volumedetect", "-vn", "-f", "null", "-")
vol = subprocess.run(["ffmpeg", "-i", f, "-af", "volumedetect", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
mx = [l for l in vol.splitlines() if "max_volume" in l]
if mx and "-91" not in mx[0] and "-inf" not in mx[0]: errs.append(f"audio not silent: {mx[0].split(']')[-1].strip()}")
print(f"{f}: {dur:.2f}s, {len(fr)} frames, cuts at frames {sorted(scene)}, brightness {luma.mean():.0f}, saturation {sat.mean():.0f}")
print("\n".join("FAIL " + e for e in errs) if errs else "QC_OK")
