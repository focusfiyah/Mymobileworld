"""Voiceover for v2g (Grace's own script, 2026-10-18): Grace B (eleven_v4) -> vo/voiceover.mp3, scribe_v2 words -> vo/stt.json,
pauses trimmed -> vo/voiceover_tight.mp3 + vo/words_trimmed.json. Same steps as ../vo.py, no shot windows (cut.py places shots)."""
import json, subprocess, sys, requests, re
def _gate():  # SCRIPT GATE (grace/gate.py): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[3] / "grace")); from gate import require; require(_h.parent)


VOICE = "gjmt5xZqVE6mjSY4NfQM"  # Grace (one voice since 2026-10-20)
RETIME = "--retime" in sys.argv  # reuse vo/voiceover.mp3 + vo/stt.json (no new ElevenLabs calls)
text = " ".join(open("vo/text.txt").read().replace("’", "'").split())
body = {"text": text, "model_id": "eleven_v4",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
if not RETIME:
  json.dump({"voice_id": VOICE, **body}, open("vo/vo.json", "w"), indent=1)
  _gate()
  r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
                  json=body, timeout=300); r.raise_for_status()
  open("vo/voiceover.mp3", "wb").write(r.content)
  r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                  files={"file": open("vo/voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
  json.dump(r.json(), open("vo/stt.json", "w"), indent=1)
d = json.load(open("vo/stt.json"))
print("raw", d["audio_duration_secs"], "|", d["text"])
W = [w for w in d["words"] if w["type"] == "word"]
segs = []
for i, w in enumerate(W):  # keep every word whole; shrink gaps to 0.16s after punctuation, 0.10s otherwise
    if i == 0:
        a = max(0, w["start"] - 0.05)
    else:
        p = W[i - 1]; keep = min(w["start"] - p["end"], 0.16 if p["text"][-1] in ".?!,:" else 0.10)
        segs[-1][1] = p["end"] + keep / 2; a = w["start"] - keep / 2
    segs.append([a, w["end"]])
segs[-1][1] = min(d["audio_duration_secs"], W[-1]["end"] + 0.25)
pos, out = 0, []
for w, (a, b) in zip(W, segs):
    out.append({"text": w["text"], "start": round(w["start"] - a + pos, 3), "end": round(w["end"] - a + pos, 3)}); pos += b - a
json.dump(out, open("vo/words_trimmed.json", "w"), indent=1)
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[s{i}];"
            for i, (a, b) in enumerate(segs))
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/voiceover.mp3", "-filter_complex", f, "-map", "[o]",
                "-c:a", "libmp3lame", "-b:a", "192k", "vo/voiceover_tight.mp3"], check=True)

print("tight", round(pos, 2))
