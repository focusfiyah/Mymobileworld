"""V2 (Grace's own script, verbatim) Grace B voiceover (Ralph OK 2026-10-03, ~706 ElevenLabs chars). Writes vo/v2g_voiceover.mp3 + vo/v2g_words.json (text alignment) and
vo/v2g_stt.json (scribe_v2 check: the alignment does NOT show stutters, so every take is STT-checked)."""
import base64, json, sys, requests
from vo import VOICE, SETTINGS, _gate
text = open("research/v2_script.txt").read().strip()
_gate()
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                  json={"text": text, "model_id": "eleven_v4", "voice_settings": SETTINGS}, timeout=300)
if not r.ok: sys.exit(f"{r.status_code} {r.text[:200]}")
d = r.json(); open("vo/v2g_voiceover.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
al = d["alignment"]; words, cur, s0 = [], "", None
for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
    if c.isspace():
        if cur: words.append({"text": cur, "start": s0, "end": e0}); cur = ""
        continue
    if not cur: s0 = a
    cur += c; e0 = b
if cur: words.append({"text": cur, "start": s0, "end": e0})
json.dump(words, open("vo/v2g_words.json", "w"), indent=1)
print(len(text), "chars,", len(words), "words,", round(words[-1]["end"], 1), "s")
s = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"}, files={"file": open("vo/v2g_voiceover.mp3", "rb")}, timeout=300)
if s.ok:
    j = s.json(); json.dump(j, open("vo/v2g_stt.json", "w"), indent=1); print("STT:", j["text"])
else: print("STT failed", s.status_code, s.text[:200])
