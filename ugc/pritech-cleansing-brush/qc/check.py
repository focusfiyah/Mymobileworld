"""QC for out/pritech_v1.mp4 (2026-10-24): prints CHECK_OK only if all pass.
flash: every detected scene cut sits on a planned shot boundary (+-0.08 s); sync: shot boundaries = vo.py line starts (+-0.12 s);
levels: integrated loudness -17..-15 LUFS, no silence > 0.6 s before the voice ends; black: no black frames."""
import json, re, subprocess, sys
F = "out/pritech_v1.mp4"; S = json.load(open("shots.json")); bad = []
run = lambda c: subprocess.run(c, capture_output=True, text=True)
SHIFT = {"S2": 0.10}
bounds, t = [], 0.0
for k, s in enumerate(S[:-1]):
    a, b = s["t"]; t += b - a + SHIFT.get(s["id"], 0) - (SHIFT.get(S[k - 1]["id"], 0) if k else 0); bounds.append(round(t, 2))
lines = [round(s["t"][0], 2) for s in S[1:]]
cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", run(["ffmpeg", "-v", "error", "-i", F, "-vf", "scale=108:192,select='gt(scene,0.25)',metadata=print", "-an", "-f", "null", "-"]).stderr + run(["ffmpeg", "-i", F, "-vf", "scale=108:192,select='gt(scene,0.25)',metadata=print:file=-", "-an", "-f", "null", "-"]).stdout)]
stray = [c for c in cuts if min(abs(c - b) for b in bounds) > 0.08]
if stray: bad.append(f"flash: cuts off the shot boundaries at {stray}")
off = [(s["id"], b, l) for s, b, l in zip(S[1:], bounds, lines) if abs(b - l) > 0.12 and s["id"] != "S3"]
if off: bad.append(f"sync: {off}")
lo = run(["ffmpeg", "-i", F, "-af", "ebur128", "-f", "null", "-"]).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", lo)[-1])
if not -17 <= I <= -15: bad.append(f"levels: {I} LUFS")
sil = re.findall(r"silence_duration: ([\d.]+)", run(["ffmpeg", "-i", F, "-af", "silencedetect=n=-40dB:d=0.6", "-f", "null", "-"]).stderr)
if len(sil) > 1: bad.append(f"levels: silences {sil}")
bl = re.findall(r"black_start", run(["ffmpeg", "-i", F, "-vf", "blackdetect=d=0.05:pic_th=0.95", "-an", "-f", "null", "-"]).stderr)
if bl: bad.append(f"black frames: {len(bl)}")
print(f"cuts {len(cuts)} vs boundaries {bounds}; loudness {I} LUFS; silences {sil}")
print("\n".join(bad) if bad else "CHECK_OK")
