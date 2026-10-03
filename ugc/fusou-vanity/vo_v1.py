"""Video 1 voiceover: ElevenLabs Grace B (eleven_v4), word times from the TTS alignment (no extra STT call)."""
import base64, json, re, requests


def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)


LINES = ["Tap it once. Again. Now hold it.",
         "Bathroom light makes your makeup look fine, until you step outside.",
         "This mirror has three light colors and it dims, so you can match wherever you're going.",
         "Heads up, it's almost six feet wide. Measure your wall first.",
         "It ships in three boxes, so if you want it up before the holidays, order it now."]
VOICE = "bGrsdLmwBbYUgHRuMFOI"
text = " ".join(LINES)
body = {"text": text, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
_gate()
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", json=body, timeout=300)
print(r.status_code, r.text[:200] if not r.ok else "")
r.raise_for_status(); d = r.json()
open("vo/v1_voiceover.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
al = d["alignment"]; ch, st, en = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
words, cur, s0 = [], "", None
for c, a, b in zip(ch, st, en):
    if c.isspace():
        if cur: words.append({"text": cur, "start": s0, "end": e0}); cur = ""
        continue
    if not cur: s0 = a
    cur += c; e0 = b
if cur: words.append({"text": cur, "start": s0, "end": e0})
json.dump({"voice_id": VOICE, **body}, open("vo/v1_vo.json", "w"), indent=1); json.dump(words, open("vo/v1_words.json", "w"), indent=1)
i = 0; out = []
for L in LINES:
    n = len(L.split()); w = words[i:i + n]; i += n; out.append({"line": L, "start": round(w[0]["start"], 2), "end": round(w[-1]["end"], 2)})
for o in out: print(o["start"], o["end"], round(o["end"] - o["start"], 2), o["line"][:50])
print("words", len(words), "total", round(words[-1]["end"], 2), "wps", round(len(words) / (words[-1]["end"] - words[0]["start"]), 2))
json.dump(out, open("vo/v1_lines.json", "w"), indent=1)
