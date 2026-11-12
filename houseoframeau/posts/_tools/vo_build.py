"""Read back every line with faster-whisper small.en, trim each line to its words (+40 ms / +120 ms), join with GAP s of
silence -> JOB/vo/ralph.wav + JOB/vo/words.json {"lines": [{text, start, end, dur}]} on the joined timeline.
  /root/.presenter-tools/fw/bin/python -I vo_build.py JOB..."""
import json, subprocess, sys
import numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
GAP = 0.22
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4)
for J in map(Path, sys.argv[1:]):
    n = len([l for l in (J / "vo/lines.txt").read_text().splitlines() if l.strip()])
    out, t, parts = [], 0.0, []
    for i in range(n):
        f = J / f"vo/L{i}.wav"
        pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ar", "16000", "-ac", "1", "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
        segs = list(m.transcribe(pcm, word_timestamps=True, language="en")[0])
        words = [w for s in segs for w in s.words]
        a, b = max(0, words[0].start - 0.04), words[-1].end + 0.12
        tr = J / f"vo/T{i}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-ar", "44100", "-ac", "1", str(tr)], check=True)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(tr)], capture_output=True, text=True).stdout)
        out.append({"text": " ".join(s.text.strip() for s in segs), "start": round(t, 3), "end": round(t + d, 3), "dur": round(d, 3)})
        parts.append(str(tr)); t += d + GAP
    lst = J / "vo/concat.txt"
    sil = J / "vo/gap.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", str(GAP), str(sil)], check=True)
    lst.write_text("".join(f"file '{Path(p).name}'\nfile 'gap.wav'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "pcm_s16le", str(J / "vo/ralph.wav")], check=True)
    json.dump({"lines": out, "total": round(t - GAP, 3)}, open(J / "vo/words.json", "w"), indent=1)
    print("VO_BUILT", J, round(t - GAP, 2), "s")
    for o in out: print(f"  {o['start']:6.2f} {o['dur']:5.2f} {o['text']}")
