"""QC for the House of Rameau PRITECH V3 cut (GATES.md). python3 qc.py basic|different|grade"""
import json, subprocess, sys
import numpy as np
OUT = "out/pritech_v3_hor.mp4"
REF = sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-0/-home-user/a22c8252-2d0c-523f-8338-9dafee75637e/scratchpad/hv3/grace_v3.mp4"   # Grace's approved V3 (git show origin/main:ugc/pritech-15s/review/vid/V3_cut1.mp4)
def fail(m): print("FAIL", m); sys.exit(1)
def probe(f, k): return subprocess.run(["ffprobe", "-v", "error", *k, "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
def frame(f, t, w=270, h=480):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(h, w, 3).astype(float)
cmd = sys.argv[1]
if cmd == "basic":
    wh = probe(OUT, ["-select_streams", "v", "-show_entries", "stream=width,height"]); d = float(probe(OUT, ["-show_entries", "format=duration"]))
    a = probe(OUT, ["-select_streams", "a", "-show_entries", "stream=codec_name"])
    vol = subprocess.run(["ffmpeg", "-i", OUT, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mean = float(vol.split("mean_volume:")[1].split("dB")[0])
    if wh != "1080,1920" or not 18.8 <= d <= 19.6 or not a or mean < -35: fail(f"{wh} {d} {a} {mean}")
    print("PASS basic", wh, round(d, 2), "s", a, mean, "dB")
elif cmd == "different":
    n = len(json.load(open("out/edit.json")))
    if n < 11: fail(f"{n} shots")
    diffs = [float(np.mean(np.abs(frame(OUT, t) - frame(REF, t)))) for t in (0.5, 2.8, 4.5, 7.0, 8.6, 11.5, 15.6, 17.0)]
    if min(diffs) < 12: fail(f"too close to Grace's V3: {[round(x,1) for x in diffs]}")
    print("PASS different", n, "shots, min diff", round(min(diffs), 1))
elif cmd == "grade":
    ts = np.linspace(0.5, 18.5, 10)
    A = np.mean([frame(OUT, t).reshape(-1, 3).mean(0) for t in ts], 0); B = np.mean([frame(REF, t).reshape(-1, 3).mean(0) for t in ts], 0)
    la, lb = A @ [.299, .587, .114], B @ [.299, .587, .114]
    if la < lb or (A[2] - A[0]) < (B[2] - B[0]) - 3: fail(f"luma {la:.1f} vs {lb:.1f}, b-r {A[2]-A[0]:.1f} vs {B[2]-B[0]:.1f}")
    print("PASS grade", f"luma {la:.1f} vs {lb:.1f}, b-r {A[2]-A[0]:.1f} vs {B[2]-B[0]:.1f}")
