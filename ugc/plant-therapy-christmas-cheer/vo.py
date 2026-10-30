"""Christmas Cheer VO (2026-10-30), the flashlight way (grace/voice/README.md): Grace cloned v5, eleven_v4 0.4/0.8/0/1.0 ->
vo/voiceover.mp3, scribe_v2 word times -> vo/stt.json, pauses tightened, atempo to 3.5 words/s (max 1.25x), loudnorm -16 ->
vo/voiceover_final.mp3 + vo/words.json; shot windows (by line) written into vo/windows.json. --retime reuses the render."""
import json, pathlib, re, subprocess, sys, requests
def _gate():
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)
VOICE = "KI3g39BKXX7dow9OHoHI"   # Grace cloned v5 (Ralph 2026-10-28 approved)
LINES = [l.strip() for l in pathlib.Path("vo_lines.txt").read_text().splitlines() if l.strip()]
text = " ".join(LINES)
body = {"text": text, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
if "--retime" not in sys.argv:
    _gate(); json.dump({"voice_id": VOICE, **body}, open("vo/vo.json", "w"), indent=1)
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", json=body, timeout=300); r.raise_for_status()
    open("vo/voiceover.mp3", "wb").write(r.content)
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                      files={"file": open("vo/voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
    json.dump(r.json(), open("vo/stt.json", "w"), indent=1)
d = json.load(open("vo/stt.json")); print("raw", d["audio_duration_secs"], "|", d["text"])
W = [w for w in d["words"] if w["type"] == "word"]; segs = []
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
f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[o]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/voiceover.mp3", "-filter_complex", f, "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "192k", "vo/voiceover_tight.mp3"], check=True)
wps = len(out) / pos; k = max(1.0, min(1.25, 3.5 / wps)); print("words/s", round(wps, 2), "-> atempo", round(k, 3))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/voiceover_tight.mp3", "-af", f"atempo={k:.4f},loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", "vo/voiceover_final.mp3"], check=True)
for w in out: w["start"] = round(w["start"] / k, 3); w["end"] = round(w["end"] / k, 3)
json.dump(out, open("vo/words.json", "w"), indent=1)
# shot windows: line i spans its first word start .. next line's first word start (shots = the 7 lines in make_shots.LINES)
import make_shots
n = [len(l.split()) for l in make_shots.LINES]; idx, starts = 0, []
for c in n: starts.append(out[idx]["start"] if idx < len(out) else None); idx += c
dur = pos / k; starts[0] = 0.0
win = [(round(starts[i], 2), round(starts[i + 1] if i + 1 < len(starts) else dur, 2)) for i in range(len(starts))]
json.dump({"duration": round(dur, 2), "windows": win, "words_total": len(out), "words_script": sum(n)}, open("vo/windows.json", "w"), indent=1)
print("final", round(dur, 2), "s; windows", win, "| stt words", len(out), "script words", sum(n))
