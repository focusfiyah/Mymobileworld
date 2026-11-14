"""Joins vo/L<n>.wav into vo/ralph_cbx.wav: each line's leading/trailing silence trimmed, GAP s between lines,
0.12 s lead-in. Writes vo/offsets.json (line start times in the joined file)."""
import json, subprocess
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; SR = 24000; GAP = 0.38
GAPS = {3: 0.26}   # S3 (brushing) has 4.04 s of footage: line 3 + its pause must fit it, never stretch
lines = [l for l in (H / "vo/lines.txt").read_text().split("\n") if l.strip()]
out, off, t = [np.zeros(int(0.12 * SR), np.float32)], [], 0.12
for n in range(len(lines)):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(H / f"vo/L{n}.wav"), "-af", "loudnorm=I=-16:TP=-2:LRA=7", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32)
    env = np.convolve(np.abs(a), np.ones(240) / 240, "same"); on = np.where(env > 0.01)[0]
    a = a[max(on[0] - 480, 0): min(on[-1] + 1440, len(a))]
    off.append(round(t, 3)); out += [a, np.zeros(int(GAPS.get(n, GAP) * SR), np.float32)]; t += len(a) / SR + GAPS.get(n, GAP)
y = np.concatenate(out)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", str(H / "vo/ralph_cbx.wav")], input=y.tobytes(), check=True)
(H / "vo/offsets.json").write_text(json.dumps(off)); print("JOIN_OK", off, round(len(y) / SR, 2), "s")
