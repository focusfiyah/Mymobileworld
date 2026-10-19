"""Grace B voiceover per video: python3 vo.py R1|R2 [--retime]
-> vo/<V>.mp3, vo/<V>_stt.json (scribe_v2), vo/<V>_tight.mp3 (pauses shortened, words whole), vo/<V>_words.json, shot windows into shots.json."""
import json, re, subprocess, sys, requests
def _gate():
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)
V = sys.argv[1]; RETIME = "--retime" in sys.argv
J = json.load(open("shots.json")); S = J["videos"][V]
text = " ".join(s["vo"] for s in S)
if not RETIME:
    _gate()
    body = {"text": text, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
    json.dump({"voice_id": J["voice"]["voice_id"], **body}, open(f"vo/{V}_req.json", "w"), indent=1)
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{J['voice']['voice_id']}?output_format=mp3_44100_128", json=body, timeout=300); r.raise_for_status()
    open(f"vo/{V}.mp3", "wb").write(r.content)
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                      files={"file": open(f"vo/{V}.mp3", "rb")}, timeout=300); r.raise_for_status()
    json.dump(r.json(), open(f"vo/{V}_stt.json", "w"), indent=1)
d = json.load(open(f"vo/{V}_stt.json")); print("raw", d["audio_duration_secs"], "|", d["text"])
W = [w for w in d["words"] if w["type"] == "word"]
segs = []
for i, w in enumerate(W):
    if i == 0: a = max(0, w["start"] - 0.05)
    else:
        p = W[i - 1]; keep = min(w["start"] - p["end"], 0.22 if p["text"][-1] in ".?!" else 0.14 if p["text"][-1] in ",:" else 0.10)
        segs[-1][1] = p["end"] + keep / 2; a = w["start"] - keep / 2
    segs.append([a, w["end"]])
segs[-1][1] = min(d["audio_duration_secs"], W[-1]["end"] + 0.3)
pos, out = 0, []
for w, (a, b) in zip(W, segs):
    out.append({"text": w["text"], "start": round(w["start"] - a + pos, 3), "end": round(w["end"] - a + pos, 3)}); pos += b - a
json.dump(out, open(f"vo/{V}_words.json", "w"), indent=1)
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[s{i}];" for i, (a, b) in enumerate(segs))
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"vo/{V}.mp3", "-filter_complex", f, "-map", "[o]", "-ar", "48000", "-c:a", "pcm_s16le", f"vo/{V}_tight.wav"], check=True)
NUM = {"14": "fourteen", "12": "twelve", "1": "one", "3": "three", "6": "six"}
norm = lambda x: "".join(NUM.get(t, t) for t in re.sub(r"[^a-z0-9 ]", " ", x.lower().replace("’", "'").replace("'", "")).split())
i, starts = 0, []
for s in S:
    starts.append(out[i]["start"]); target, got = norm(s["vo"]), ""
    while got != target:
        assert len(got) < len(target) and i < len(out), f"transcript doesn't match {s['id']}: {got!r} vs {target!r}"
        got += norm(out[i]["text"]); i += 1
assert i == len(out), f"word count mismatch: script {i} vs audio {len(out)}"
for k, s in enumerate(S):
    a = 0.0 if k == 0 else round(starts[k] - 0.05, 2); b = round(starts[k + 1] - 0.05, 2) if k + 1 < len(starts) else round(pos, 2)
    s["t"] = [a, b]; print(s["id"], a, b, round(b - a, 2), "clip", s["dur"], "OK" if b - a <= s["dur"] else "TOO LONG")
json.dump(J, open("shots.json", "w"), indent=1); print(V, "tight", round(pos, 2))
