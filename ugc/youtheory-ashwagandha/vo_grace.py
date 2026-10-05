"""Grace-VO v2 scripts (adult juice box), voiced in Grace B. Variant voiceover: Grace B (eleven_v4) for vo/v<N>_lines.json -> vo/v<N>/voiceover_tight.mp3 + windows.json (one window per shot,
lines mapped to shots in order). Pauses trimmed like vo.py; if longer than 15.8 s, sped up free (atempo, pitch kept).
  python3 vo_variant.py N [--retime]"""
import json, re, subprocess, sys, requests, os
from pathlib import Path
N = sys.argv[1]; D = Path(f"vo/g{N}"); D.mkdir(parents=True, exist_ok=True)
J = json.load(open("shots.json")); lines = json.load(open(f"vo/g{N}_lines.json"))
TTS = {"Youtheory": "You-theory"}
text = " ".join(lines)
tts = text
for a, b in TTS.items(): tts = tts.replace(a, b)
if "--retime" not in sys.argv:
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{J['voice']['voice_id']}?output_format=mp3_44100_128",
                      json={"text": tts, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}, timeout=300)
    r.raise_for_status(); (D / "voiceover.mp3").write_bytes(r.content)
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                      files={"file": open(D / "voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
    json.dump(r.json(), open(D / "stt.json", "w"), indent=1)
d = json.load(open(D / "stt.json")); W = [w for w in d["words"] if w["type"] == "word"]
segs = []
for i, w in enumerate(W):
    if i == 0: a = max(0, w["start"] - 0.05)
    else:
        p = W[i - 1]; keep = min(w["start"] - p["end"], 0.16 if p["text"][-1] in ".?!,:" else 0.10)
        segs[-1][1] = p["end"] + keep / 2; a = w["start"] - keep / 2
    segs.append([a, w["end"]])
segs[-1][1] = min(d["audio_duration_secs"], W[-1]["end"] + 0.25)
pos, out = 0, []
for w, (a, b) in zip(W, segs):
    out.append({"text": w["text"], "start": w["start"] - a + pos, "end": w["end"] - a + pos}); pos += b - a
f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[s{i}];" for i, (a, b) in enumerate(segs))
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1"
sp = max(1.0, round(pos / 15.7, 3))
if sp > 1.0: f += f",atempo={sp}"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(D / "voiceover.mp3"), "-filter_complex", f + "[o]", "-map", "[o]",
                "-c:a", "libmp3lame", "-b:a", "192k", str(D / "voiceover_tight.mp3")], check=True)
for o in out: o["start"] /= sp; o["end"] /= sp
pos /= sp
import difflib
tok = lambda x: [t for t in re.sub(r"[^a-z0-9 ]", " ", x.lower()).split() if t]
sw, lid = [], []
for k, l in enumerate(lines):
    for t in tok(l): sw.append(t); lid.append(k)
ow, oi = [], []
for k, o in enumerate(out):
    for t in tok(o["text"]): ow.append(t); oi.append(k)
m = {}
for blk in difflib.SequenceMatcher(None, sw, ow, autojunk=False).get_matching_blocks():
    for q in range(blk.size): m[blk.a + q] = blk.b + q
starts = []
for k in range(len(lines)):
    idx = [i for i, l in enumerate(lid) if l == k]
    hit = next((m[i] for i in idx if i in m), None)
    assert hit is not None, f"line {k} not found in audio"
    first = idx.index(next(i for i in idx if i in m))   # unmatched words before the first match: step back that many
    starts.append(out[max(0, oi[hit] - first)]["start"])
win = []
for k in range(len(lines)):
    a = 0.0 if k == 0 else round(starts[k] - 0.05, 2); b = round(starts[k + 1] - 0.05, 2) if k + 1 < len(lines) else round(pos, 2)
    win.append([a, b])
json.dump({"speed": sp, "total": round(pos, 2), "windows": win, "stt_text": d["text"]}, open(D / "windows.json", "w"), indent=1)
rep = [(a["text"], b["text"]) for a, b in zip(W, W[1:]) if a["text"].lower().strip(".,?!") == b["text"].lower().strip(".,?!")]
frag = [w["text"] for w in W if w["text"].endswith("-")]
print(f"V{N} total {pos:.2f}s speed {sp} windows {win} repeats {rep} frags {frag}")
