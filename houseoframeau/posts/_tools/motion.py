"""Mean abs frame difference (gray 108x192) between frames 0.5 s apart; < ~1.5 reads as a still photo."""
import subprocess, sys, numpy as np
for f in sys.argv[1:]:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-t", "6", "-vf", "fps=2,scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 192, 108).astype(float)
    d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
    print(f"{f}: mean {d.mean():.2f} min {d.min():.2f}")
