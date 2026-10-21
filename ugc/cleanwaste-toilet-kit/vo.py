"""Voiceover for V1 (Grace's script word for word): Grace C (eleven_v4) -> vo/voiceover.mp3, scribe_v2 word times -> vo/stt.json,
pauses trimmed (no word clipped) -> vo/voiceover_tight.wav at -16 LUFS (Grace C runs quiet), shot windows -> vo/windows.json.
Only line-end punctuation is added for delivery; the words are Grace's (checked against the STT below).
  python3 vo.py            paid: ~480 ElevenLabs chars + one STT
  python3 vo.py --retime   free: reuse vo/voiceover.mp3 + vo/stt.json"""
import json, re, subprocess, sys
from pathlib import Path
import requests

def _gate():
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)

VOICE = "Rh3oAQMqRVf78UIVpBoQ"   # "Grace" clone picked by Ralph 2026-10-20 (account note: eleven_v4 0.4/0.8/0, then pace to 3.5 words/s); Grace C was deleted (404 tested 2026-10-21)
SH = [s for s in json.load(open("shots.json"))["videos"][0]["shots"]]
lines = [l.split(": ", 1)[1] for l in open("scripts.md").read().splitlines() if l.startswith("L")]
text = " ".join(l + ("?" if i == 0 else ".") for i, l in enumerate(lines))
Path("vo").mkdir(exist_ok=True)
json.dump({"V1": lines}, open("vo/v1_lines.json", "w"), indent=1)
if "--retime" not in sys.argv:
    _gate()
    body = {"text": text, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
    json.dump({"voice_id": VOICE, **body}, open("vo/vo.json", "w"), indent=1)
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", json=body, timeout=300); r.raise_for_status()
    open("vo/voiceover.mp3", "wb").write(r.content)
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                      files={"file": open("vo/voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
    json.dump(r.json(), open("vo/stt.json", "w"), indent=1)
d = json.load(open("vo/stt.json")); print("raw", d["audio_duration_secs"], "|", d["text"])
W = [w for w in d["words"] if w["type"] == "word"]
segs = []
for i, w in enumerate(W):   # keep every word whole; gaps shrink to 0.18 s after punctuation, 0.10 s otherwise
    if i == 0: a = max(0, w["start"] - 0.05)
    else:
        p = W[i - 1]; keep = min(w["start"] - p["end"], 0.18 if p["text"][-1] in ".?!,:" else 0.10)
        segs[-1][1] = p["end"] + keep / 2; a = w["start"] - keep / 2
    segs.append([a, w["end"]])
segs[-1][1] = min(d["audio_duration_secs"], W[-1]["end"] + 0.3)
pos, out = 0, []
for w, (a, b) in zip(W, segs):
    out.append({"text": w["text"], "start": round(w["start"] - a + pos, 3), "end": round(w["end"] - a + pos, 3)}); pos += b - a
json.dump(out, open("vo/words_trimmed.json", "w"), indent=1)
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[s{i}];" for i, (a, b) in enumerate(segs))
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[o]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/voiceover.mp3", "-filter_complex", f, "-map", "[o]", "-ar", "48000", "vo/voiceover_tight.wav"], check=True)
norm = lambda x: "".join(re.sub(r"[^a-z0-9]", "", x.lower()))   # letters only: STT writes the brand "Clean Waste", the script "Cleanwaste"
said = "".join(norm(w["text"]) for w in out); want = "".join(norm(l) for l in lines)
print("WORDS_MATCH" if said == want else f"WORD MISMATCH:\n said {said}\n want {want}")
i, win = 0, []
for s in SH:    # consume STT words until they spell this shot's words; the window starts at its first word
    target, got, j = norm(s["words"]), "", i
    while got != target:
        assert len(got) < len(target) and j < len(out), f"transcript doesn't match {s['id']}: {got!r} vs {target!r}"
        got += norm(out[j]["text"]); j += 1
    win.append({"id": s["id"], "start": out[i]["start"], "end": out[j - 1]["end"]}); i = j
assert i == len(out)
for k in range(len(win) - 1): win[k]["cut"] = round(win[k + 1]["start"] - 0.05, 3)
win[-1]["cut"] = round(pos, 3)
json.dump(win, open("vo/windows.json", "w"), indent=1)
prev = 0
for w in win: print(w["id"], w["start"], "->", w["cut"], round(w["cut"] - prev, 2)); prev = w["cut"]
print("total", round(pos, 2), "words/s", round(len(want and [l for l in " ".join(lines).split()]) / pos, 2))
