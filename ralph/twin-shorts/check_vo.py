"""G2: every script word heard in vo/vo.wav (faster-whisper small.en). Prints VO_WORDS_OK or the missing words."""
import re, subprocess, sys
PY = "/root/.presenter-tools/cbx/bin/python"
code = "from faster_whisper import WhisperModel as W;m=W('small.en',device='cpu',compute_type='int8');import torchaudio as ta,torchaudio.functional as F;w,sr=ta.load('vo/vo.wav');a=F.resample(w.mean(0),sr,16000).numpy();s,_=m.transcribe(a);print(' '.join(x.text for x in s))"
heard = subprocess.run([PY, "-c", code], capture_output=True, text=True).stdout.lower()
norm = lambda t: re.findall(r"[a-z0-9]+", t.lower().replace("fifty two", "52").replace("a hundred and twenty", "a 120").replace("d m", "dm").replace("d.m.", "dm"))
h = set(norm(heard.replace("fifty-two", "fifty two"))); h.add("120") if "120" in heard else None
miss = [w for w in norm(open("script.txt").read()) if w not in h and not (w == "52" and ("52" in heard or "fifty" in heard))]
print("HEARD:", heard.strip()); print("VO_WORDS_OK" if not miss else f"MISSING {miss}")
