"""Voiceover per remix video (2026-10-20), grace/voice/README.md steps: "Grace" clone (eleven_v4 0.4/0.8/0) -> vo/v<N>_raw.mp3
(the only paid step), then free: pace.py --wps 3.5 -> vo/v<N>_paced.mp3, clean.py -> vo/v<N>.mp3 (-16 LUFS),
local Whisper word times -> vo/v<N>_words.json. Text = scripts.json video N.
  python3 vo.py N [--retime]   (--retime reuses the raw mp3, no ElevenLabs call)"""
import json, subprocess, sys, requests
from pathlib import Path
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H.parents[2] / "grace")); from gate import require
N = int(sys.argv[1]); RETIME = "--retime" in sys.argv
VOICE = "Rh3oAQMqRVf78UIVpBoQ"  # "Grace", her one voice since 2026-10-20 (Ralph: "Use Grace new voice as the VO")
text = " ".join(next(s for s in json.load(open(H / "scripts.json")) if s["video"] == N)["text"].replace("’", "'").split())
raw = H / f"vo/v{N}_raw.mp3"; V = H.parents[2] / "grace/voice"
if not RETIME:
    require(H)
    body = {"text": text, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
    json.dump({"voice_id": VOICE, **body}, open(H / f"vo/v{N}_req.json", "w"), indent=1)
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", json=body, timeout=300); r.raise_for_status()
    raw.write_bytes(r.content)
paced, final = H / f"vo/v{N}_paced.mp3", H / f"vo/v{N}.mp3"
if "--words-only" in sys.argv: pass
else:
  subprocess.run([sys.executable, str(V / "pace.py"), str(raw), str(paced), "--wps", "3.5"], check=True)
  if "--no-clean" not in sys.argv:
    subprocess.run([sys.executable, str(V / "clean.py"), str(paced), str(final)], check=True)
  else:
    final.write_bytes(paced.read_bytes())
from faster_whisper import WhisperModel
sys.path.insert(0, str(V)); from echo import load   # PyAV decode breaks here; pass samples like pace.py
segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(load(str(final))[0], language="en", word_timestamps=True,
    initial_prompt="castor oil roll-on, grandmama, Imma do y'all a favor")   # small + prompt: base heard "Caster", "I'm gonna"
out = [{"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)} for s_ in segs for w in s_.words]
json.dump(out, open(H / f"vo/v{N}_words.json", "w"), indent=1)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout)
heard = " ".join(w["text"] for w in out)
print(f"v{N} {d:.2f}s | heard: {heard}")
