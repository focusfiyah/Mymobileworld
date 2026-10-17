"""QC for a cut (2026-10-17): every cut point falls between words, no freeze, no black frame, voice level sane, length 20-40s.
  python3 qc/check_cut.py OUT.mp4   -> prints each check and 'ALL OK' only if every one passes"""
import json, re, subprocess, sys
sys.path.insert(0, "."); src = open("cut.py").read(); EDIT = eval(src[src.index("EDIT = [") + 7: src.index("]\nCLIP") + 1])
out = sys.argv[1]; W = json.load(open("vo/words_trimmed.json")); bad = []
t = 0
for k, a, d in EDIT[:-1]:
    t += d
    inside = [w["text"] for w in W if w["start"] + 0.02 < t < w["end"] - 0.02]
    if inside: bad.append(f"cut {t:.2f}s inside word {inside}")
print("cuts between words:", "OK" if not any("cut" in b for b in bad) else "FAIL")
r = lambda *c: subprocess.run(c, capture_output=True, text=True).stderr
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
print(f"length {dur:.2f}s:", "OK" if 20 <= dur <= 40 else "FAIL"); dur <= 40 and dur >= 20 or bad.append("length")
fz = re.findall(r"freeze_start: ([\d.]+)", r("ffmpeg", "-i", out, "-vf", "freezedetect=n=0.001:d=0.6", "-an", "-f", "null", "-"))
print("no freeze >0.6s:", "OK" if not fz else f"FAIL {fz}"); fz and bad.append(f"freeze {fz}")
bk = re.findall(r"black_start:([\d.]+)", r("ffmpeg", "-i", out, "-vf", "blackdetect=d=0.05:pix_th=0.08", "-an", "-f", "null", "-"))
print("no black frames:", "OK" if not bk else f"FAIL {bk}"); bk and bad.append(f"black {bk}")
lv = r("ffmpeg", "-i", out, "-af", "ebur128", "-vn", "-f", "null", "-"); I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", lv)[-1])
print(f"loudness {I} LUFS:", "OK" if -24 <= I <= -10 else "FAIL"); -24 <= I <= -10 or bad.append("loudness")
print("ALL OK" if not bad else f"FAIL {bad}")
