"""Read every voice line back with faster-whisper small.en, trim its silence, and build the voiceover.
  ~/.presenter-tools/fw/bin/python -I readback.py POST [gap_s=0.22] [tempo=1.0]
Writes POST/vo/ralph.wav (lines joined with gaps) and POST/vo/timing.json (each line's start/end on the VO timeline).
Prints READBACK_OK only when every line's words match the script (ratio >= 0.9, no missing word)."""
import json, re, sys, difflib, subprocess
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
post = Path(sys.argv[1]).resolve(); gap = float(sys.argv[2]) if len(sys.argv) > 2 else 0.22
tempo = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
lines = [l.strip() for l in (post / "vo/lines.txt").read_text().splitlines() if l.strip()]
model = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4)
NUM = {"5": "five", "10": "ten", "12": "twelve", "3": "three", "1": "one", "2": "two", "4": "four"}
SAME = {"cents": "scents", "sense": "scents"}   # homophones whisper cannot tell apart
def norm(w):
    w = re.sub(r"[^a-z0-9]", "", w.lower()); w = NUM.get(w, w); return SAME.get(w, w)
SR = 44100; parts, timing, bad, t = [], [], [], 0.0
for n, line in enumerate(lines):
    trim = post / f"vo/L{n}.trim.wav"
    af = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.03,areverse,"
          "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.06,areverse,afade=t=in:d=0.01")
    if tempo != 1.0: af += f",atempo={tempo}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(post / f"vo/L{n}.wav"), "-af", af, "-ar", str(SR), "-ac", "1", str(trim)], check=True)
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(trim), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
    segs, _ = model.transcribe(np.frombuffer(pcm, np.float32), word_timestamps=True, language="en", beam_size=5)
    heard = [x for s in segs for w in s.words for x in w.word.strip().replace('-', ' ').split()]
    say = [norm(w) for w in line.split()]; got = [norm(w) for w in heard]
    sm = difflib.SequenceMatcher(None, say, got, autojunk=False)
    matched = sum(b.size for b in sm.get_matching_blocks()); missing = len(say) - matched
    dur = len(pcm) / 4 / 16000
    ok = sm.ratio() >= 0.9 and missing == 0
    print(f"L{n} {'OK ' if ok else 'BAD'} {dur:.2f}s ratio {sm.ratio():.2f} heard: {' '.join(heard)}")
    if not ok: bad.append(n)
    timing.append({"n": n, "text": line, "start": round(t, 3), "end": round(t + dur, 3)})
    parts.append(str(trim)); t += dur + gap
inp = sum((["-i", p] for p in parts), [])
fc = "".join(f"[{i}:a]apad=pad_dur={gap}[a{i}];" for i in range(len(parts))) + "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", fc, "-map", "[o]", "-ar", str(SR), str(post / "vo/ralph.wav")], check=True)
(post / "vo/timing.json").write_text(json.dumps(timing, indent=1))
print(f"VO length {t - gap:.2f}s")
print("READBACK_OK" if not bad else f"READBACK_BAD lines {bad} (re-seed: SEED=2000 vo_gen.py POST {' '.join(map(str, bad))})")
