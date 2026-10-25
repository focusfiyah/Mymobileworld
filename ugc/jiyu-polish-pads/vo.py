"""JIYU polish pads (2026-10-24) voiceover, copied from ugc/pritech-cleansing-brush/vo.py, copied from ugc/youtheory-collagen/vo.py (itself the approved flashlight VO), copied from the approved power bank flashlight VO: Grace (eleven_v4) from shots.json vo lines -> vo/voiceover.mp3, scribe_v2 word times -> vo/stt.json,
pauses trimmed -> vo/voiceover_tight.mp3 + vo/words_trimmed.json, shot windows written back into shots.json."""
import json, subprocess, sys, requests, re
def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)


P = "vo/"
D = json.load(open("shots.json"))
J = {"shots": D}
for s in J["shots"]: s["vo"] = s["line"]; s["dur"] = 4
VOICE = "Rh3oAQMqRVf78UIVpBoQ"  # "Grace cloned", Grace's one voice (grace/voice/README.md)
RETIME = "--retime" in sys.argv  # reuse vo/voiceover.mp3 + vo/stt.json (no new ElevenLabs calls)
import pathlib
text = " ".join(s["vo"] for s in J["shots"])  # Grace's storyboard script, word for word
body = {"text": text, "model_id": "eleven_v4",
        "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
if not RETIME:
  json.dump({"voice_id": VOICE, **body}, open(P + "vo.json", "w"), indent=1)
  _gate()
  r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
                  json=body, timeout=300); r.raise_for_status()
  open(P + "voiceover.mp3", "wb").write(r.content)
  r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                  files={"file": open(P + "voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
  json.dump(r.json(), open(P + "stt.json", "w"), indent=1)
d = json.load(open(P + "stt.json"))
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
json.dump(out, open(P + "words_trimmed.json", "w"), indent=1)
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[s{i}];"
            for i, (a, b) in enumerate(segs))
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", P + "voiceover.mp3", "-filter_complex", f, "-map", "[o]",
                "-c:a", "libmp3lame", "-b:a", "192k", P + "voiceover_tight.mp3"], check=True)
# pace to 3.5 words/s (the voice's own note) and loudnorm -16 LUFS; word times scale with the tempo
wps = len(out) / pos; k = max(1.0, min(1.25, 3.5 / wps)); print("words/s", round(wps, 2), "-> atempo", round(k, 3))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", P + "voiceover_tight.mp3", "-af", f"atempo={k:.4f},loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", P + "voiceover_paced.mp3"], check=True)
for w in out: w["start"] = round(w["start"] / k, 3); w["end"] = round(w["end"] / k, 3)
pos = pos / k
json.dump(out, open(P + "words_trimmed.json", "w"), indent=1)

NUM = {"104": "onehundredandfour", "104f": "onehundredandfourdegreesfahrenheit", "f": "fahrenheit"}  # STT writes numbers as digits
norm = lambda x: "".join(NUM.get(w, w) for w in re.sub(r"[^a-z0-9% ]", "", x.lower().replace("-", "")).split())
i, starts = 0, []
for s in J["shots"]:  # consume transcript words until they spell this shot's line
    starts.append(out[i]["start"]); target, got = norm(s["vo"]), ""
    while got != target:
        assert len(got) < len(target) and i < len(out), f"transcript doesn't match {s['id']}: {got!r} vs {target!r}"
        got += norm(out[i]["text"]); i += 1
assert i == len(out), f"word count mismatch: script {i} vs audio {len(out)}"
for k, s in enumerate(J["shots"]):
    a = 0.0 if k == 0 else round(starts[k] - 0.05, 2)
    b = round(starts[k + 1] - 0.05, 2) if k + 1 < len(starts) else round(pos, 2)
    s["t"] = [a, b]; print(s["id"], a, b, round(b - a, 2), "clip", s["dur"], "OK" if b - a <= s["dur"] else "TOO LONG")
json.dump(D, open("shots.json", "w"), indent=1)
print("tight", round(pos, 2))
