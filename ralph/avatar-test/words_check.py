"""Every script word heard in vo/line_cbx.wav (faster-whisper small.en, local, free). Prints WORDS_OK or the missing words.
Run: ~/.presenter-tools/fw/bin/python -I words_check.py"""
import re, difflib, subprocess, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
HERE = Path(__file__).parent
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
want = [norm(w) for w in (HERE / "script.txt").read_text().split() if norm(w)]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(HERE / "vo/line_cbx.wav"), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
segs, _ = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=4).transcribe(np.frombuffer(pcm, np.float32), language="en", beam_size=5)
heard_text = " ".join(s.text for s in segs); heard = [norm(w) for w in heard_text.split() if norm(w)]
miss = [want[i] for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, want, heard).get_opcodes() if op in ("delete", "replace") for i in range(i1, i2)]
print("HEARD:", heard_text.strip()); print("WORDS_OK" if not miss else f"WORDS_MISSING {miss}")
