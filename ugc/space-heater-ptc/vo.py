"""Voiceover for one video (default V1): Grace C (eleven_v4) -> vo/<V>_voiceover.mp3, scribe_v2 word times -> vo/<V>_stt.json,
pauses trimmed + loudnorm -16 LUFS -> vo/<V>_tight.mp3 + vo/<V>_words.json, shot windows "t" written back into shots.json.
Copied from ugc/lgxnds-creatine/vo.py."""
import json, re, subprocess, sys, requests
def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)

V = next((a for a in sys.argv[1:] if a.startswith("V")), "V1"); P = f"vo/{V}_"
VOICE = "P8OUGBCvq8OBS4xlb65A"   # Grace C (Grace's default since 2026-10-18)
J = json.load(open("shots.json")); SH = [s for s in J["shots"] if s["video"] == V]
text = open(f"vo/{V}.txt").read().strip()
assert text == " ".join(s["line"] for s in SH)
if "--retime" not in sys.argv:
    body = {"text": text, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
    _gate()
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", json=body, timeout=300); r.raise_for_status()
    open(P + "voiceover.mp3", "wb").write(r.content)
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                      files={"file": open(P + "voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
    json.dump(r.json(), open(P + "stt.json", "w"), indent=1)
d = json.load(open(P + "stt.json")); print("raw", d["audio_duration_secs"], "|", d["text"])
W = [w for w in d["words"] if w["type"] == "word"]
seen = [w["text"].lower().strip(".,?!") for w in W]   # stutter check (PLAYBOOK: repeated words / hyphen fragments)
bad = [f"{seen[i]}" for i in range(1, len(seen)) if seen[i] == seen[i - 1]] + [w["text"] for w in W if w["text"].endswith("-")]
print("STUTTER:", bad if bad else "none")
segs = []
for i, w in enumerate(W):   # keep every word whole; shrink gaps to 0.16 s after punctuation, 0.10 s otherwise
    if i == 0: a = max(0, w["start"] - 0.05)
    else:
        p = W[i - 1]; keep = min(w["start"] - p["end"], 0.16 if p["text"][-1] in ".?!,:" else 0.10)
        segs[-1][1] = p["end"] + keep / 2; a = w["start"] - keep / 2
    segs.append([a, w["end"]])
segs[-1][1] = min(d["audio_duration_secs"], W[-1]["end"] + 0.25)
pos, out = 0, []
for w, (a, b) in zip(W, segs):
    out.append({"text": w["text"], "start": round(w["start"] - a + pos, 3), "end": round(w["end"] - a + pos, 3)}); pos += b - a
json.dump(out, open(P + "words.json", "w"), indent=1)
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[s{i}];" for i, (a, b) in enumerate(segs))
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11[o]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", P + "voiceover.mp3", "-filter_complex", f, "-map", "[o]", "-ar", "44100",
                "-c:a", "pcm_s16le", P + "tight.wav"], check=True)
NUM = {"1500": "fifteenhundred", "eco": "eco"}
norm = lambda x: "".join(NUM.get(w, w) for w in re.sub(r"[^a-z0-9 ]", "", x.lower()).split())
i, starts = 0, []
for s in SH:   # consume transcript words until they spell this shot's line
    starts.append(out[i]["start"]); target, got = norm(s["line"]), ""
    while got != target:
        assert len(got) < len(target) and i < len(out), f"transcript doesn't match {s['id']}: {got!r} vs {target!r}"
        got += norm(out[i]["text"]); i += 1
assert i == len(out), f"word count mismatch: script {i} vs audio {len(out)}"
for k, s in enumerate(SH):
    a = 0.0 if k == 0 else round(starts[k] - 0.05, 2); b = round(starts[k + 1] - 0.05, 2) if k + 1 < len(starts) else round(pos, 2)
    s["t"] = [a, b]; print(s["id"], a, b, round(b - a, 2), "OK" if b - a <= s["dur"] else "TOO LONG")
json.dump(J, open("shots.json", "w"), indent=1)
print("tight", round(pos, 2))
