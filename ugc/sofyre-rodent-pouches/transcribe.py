# Free word-timed transcript of a local video (faster-whisper, CPU). Usage: python3 transcribe.py <video> [...]
import sys, subprocess, numpy as np, os
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8")
for v in sys.argv[1:]:
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, word_timestamps=True)
    lines = [f"{s.start:5.1f}-{s.end:5.1f} {s.text.strip()}" for s in segs]
    out = os.path.join(os.path.dirname(v), "transcript_timed.txt"); open(out, "w").write("\n".join(lines) + "\n")
    print(v); print("\n".join(lines))
