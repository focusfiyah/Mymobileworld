"""Audio gap meter: python3 gapmeter.py VIDEO [LIMIT] -> lead, tail, longest quiet run between her words, every run > LIMIT.
Quiet = 10 ms RMS (120 Hz high-pass, 30 ms smoothing) below floor + 22% of (peak - floor), floor/peak = 10th/97th percentile
of the whole cut. Prints GAPS_OK when lead <= 0.15 s, tail <= 0.35 s and every internal quiet run <= LIMIT (default 0.25 s)."""
import subprocess, sys, numpy as np
f = sys.argv[1]; lim = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-ac", "1", "-ar", "16000", "-af", "highpass=f=120", "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; n = len(x) // 160
db = 20 * np.log10(np.sqrt((x[:n * 160].reshape(n, 160) ** 2).mean(1)) + 1e-6); db = np.convolve(db, np.ones(3) / 3, "same")
fl, pk = np.percentile(db, 10), np.percentile(db, 97); v = db > fl + 0.22 * (pk - fl)
idx = np.flatnonzero(v); lead, tail = idx[0] * 0.01, (n - 1 - idx[-1]) * 0.01
runs, k = [], idx[0]
while k < idx[-1]:
    if v[k]: k += 1; continue
    s = k
    while not v[k]: k += 1
    runs.append((round((k - s) * 0.01, 2), round(s * 0.01, 2)))
big = sorted([r for r in runs if r[0] > lim], reverse=True)
mx = max([r[0] for r in runs] or [0])
print(f"{f}: dur={n*0.01:.1f}s lead={lead:.2f}s tail={tail:.2f}s longest_gap={mx:.2f}s gaps_over_{lim}={len(big)} total_over={sum(r[0] for r in big):.1f}s top={big[:6]}")
import json
if "--json" in sys.argv: print(json.dumps({"lead": lead, "tail": tail, "runs": [[float(a), float(b)] for a, b in big]}))
print("GAPS_OK" if lead <= 0.15 and tail <= 0.35 and not big else "GAPS_FAIL")
