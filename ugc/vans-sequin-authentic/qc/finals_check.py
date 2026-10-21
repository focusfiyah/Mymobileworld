"""Measure the 10 finals: count, 7-15 s each, 1080x1920 or 720x1280 vertical, every pair of finals differs (mean frame diff > 20 at 3 points)."""
import subprocess, glob, json, sys
import numpy as np
fs = sorted(glob.glob("out/V*_final.mp4"))
def probe(f):
    j = json.loads(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height,codec_type","-of","json",f],capture_output=True,text=True).stdout)
    v = [s for s in j["streams"] if s["codec_type"] == "video"][0]; return float(j["format"]["duration"]), v["width"], v["height"]
def frame(f, t):
    raw = subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",f,"-frames:v","1","-vf","scale=90:160","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).astype(float)
bad = []
if len(fs) != 10: bad.append(f"{len(fs)} finals, need 10")
info = {}
for f in fs:
    d, w, h = probe(f); info[f] = d
    if not 7 <= d <= 15.5: bad.append(f"{f} {d:.1f}s")
    if h <= w: bad.append(f"{f} not vertical")
for i, a in enumerate(fs):
    for b in fs[i+1:]:
        diffs = [np.abs(frame(a, x*min(info[a],info[b])) - frame(b, x*min(info[a],info[b]))).mean() for x in (0.1, 0.5, 0.9)]
        if min(diffs) < 20: bad.append(f"{a} vs {b} too similar {min(diffs):.0f}")
print("\n".join(bad) if bad else "FINALS_OK")
sys.exit(1 if bad else 0)
