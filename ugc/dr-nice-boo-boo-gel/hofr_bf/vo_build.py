"""Trim each Chatterbox line (silence edges), join with short gaps -> vo/ralph.wav; line starts -> vo/starts.json.
Then read every line back with faster-whisper small.en -> vo/heard.json (qc.py words checks it).
Run with the fw venv: ~/.presenter-tools/fw/bin/python vo_build.py"""
import json, subprocess, numpy as np
from pathlib import Path
lines = json.loads(Path("vo/lines.json").read_text())
GAP = [0.22, 0.25, 0.30, 0.25, 0.20]   # pause after each line (a breath; a touch longer before "Only problem?")
SR = 24000
def load(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,"
                        "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse",
                        "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype=np.float32)
parts, starts, t = [], [], 0.0
for n in range(len(lines)):
    a = load(f"vo/L{n}.wav"); starts.append(round(t, 3)); parts.append(a); t += len(a) / SR
    if n < len(GAP): parts.append(np.zeros(int(GAP[n] * SR), np.float32)); t += GAP[n]
full = np.concatenate(parts)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "vo/ralph.wav"], input=full.tobytes(), check=True)
Path("vo/starts.json").write_text(json.dumps({"starts": starts, "end": round(t, 3)}))
from faster_whisper import WhisperModel
m = WhisperModel("small.en", compute_type="int8"); heard = []
for n, p in enumerate(parts[::2]):
    a16 = np.interp(np.arange(0, len(p), SR / 16000), np.arange(len(p)), p).astype(np.float32)
    seg, _ = m.transcribe(a16, language="en"); heard.append(" ".join(s.text.strip() for s in seg))
Path("vo/heard.json").write_text(json.dumps(heard, indent=1))
print("VO_BUILT", round(t, 2), "s", starts); [print(n, h) for n, h in enumerate(heard)]
