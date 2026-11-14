"""faster-whisper small.en: read every vo/L<n>.wav back (vo/readback.json), then word times on vo/ralph_cbx.wav
(vo/words.json) and each line's first-word start (vo/line_starts.json). Run with ~/.presenter-tools/fw/bin/python -I."""
import json, sys
from pathlib import Path
from faster_whisper import WhisperModel
import subprocess, numpy as np
def A(f): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',str(f),'-ac','1','-ar','16000','-f','f32le','-'],capture_output=True,check=True).stdout, np.float32)
H = Path(__file__).resolve().parent
lines = [l for l in (H / "vo/lines.txt").read_text().split("\n") if l.strip()]
m = WhisperModel("small.en", device="cpu", compute_type="int8")
if sys.argv[1:] == ["lines"]:
    rb = [" ".join(s.text.strip() for s in m.transcribe(A(H / f"vo/L{n}.wav"), beam_size=5)[0]) for n in range(len(lines))]
    (H / "vo/readback.json").write_text(json.dumps(rb, indent=1)); [print(n, r) for n, r in enumerate(rb)]
else:
    segs, _ = m.transcribe(A(H / "vo/ralph_cbx.wav"), word_timestamps=True, beam_size=5)
    w = [[x.word.strip(), round(x.start, 2), round(x.end, 2)] for s in segs for x in s.words]
    (H / "vo/words.json").write_text(json.dumps(w))
    off = json.loads((H / "vo/offsets.json").read_text())   # where join.py placed each line
    starts = []
    for o in off:   # first heard word at or after the line's placement
        starts.append(min((x[1] for x in w if x[1] >= o - 0.05), default=o))
    (H / "vo/line_starts.json").write_text(json.dumps(starts)); print("STARTS", starts, "END", w[-1][2])
