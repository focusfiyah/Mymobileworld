"""PRITECH V2-V4 voiceovers (2026-10-27), copied from ugc/pritech-cleansing-brush/vo.py (the approved flashlight method): Grace cloned
(eleven_v4, stability 0.4, similarity 0.8) -> scribe_v2 word times -> pauses trimmed -> atempo to 3.5 words/s + loudnorm -16
-> vo/<V>/voiceover_paced.mp3 + words_trimmed.json + windows.json (each shot's [start, end] in the paced VO).
  python3 vo.py V2 V3 V4            render (ElevenLabs, ~340 chars each)
  python3 vo.py V2 --retime         reuse vo/V2/voiceover.mp3 + stt.json, no new ElevenLabs call"""
import json, re, subprocess, sys
from pathlib import Path
import requests


def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)


VOICE = "Rh3oAQMqRVf78UIVpBoQ"  # "Grace cloned", Grace's one voice (grace/voice/README.md)
SHOTS = json.load(open("shots.json"))
RETIME = "--retime" in sys.argv


def norm(x):
    x = re.sub(r"[^a-z0-9]", "", x.lower())
    for k in ("onehundredandfour", "ahundredandfour", "hundredandfour"): x = x.replace(k, "104")
    return x


def make(v):
    P = Path(f"vo/{v}"); P.mkdir(parents=True, exist_ok=True)
    shots = [s for s in SHOTS if s["video"] == v]
    text = " ".join(s["line"] for s in shots)
    body = {"text": text, "model_id": "eleven_v4", "voice_settings": {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}}
    if not RETIME:
        json.dump({"voice_id": VOICE, **body}, open(P / "vo.json", "w"), indent=1)
        _gate()
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128", json=body, timeout=300); r.raise_for_status()
        (P / "voiceover.mp3").write_bytes(r.content)
        r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                          files={"file": open(P / "voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
        json.dump(r.json(), open(P / "stt.json", "w"), indent=1)
    d = json.load(open(P / "stt.json")); print(v, "raw", d["audio_duration_secs"], "|", d["text"])
    W = [w for w in d["words"] if w["type"] == "word"]
    segs = []
    for i, w in enumerate(W):  # keep every word whole; shrink gaps to 0.16 s after punctuation, 0.10 s otherwise
        if i == 0: a = max(0, w["start"] - 0.05)
        else:
            p = W[i - 1]; keep = min(w["start"] - p["end"], 0.16 if p["text"][-1] in ".?!,:" else 0.10)
            segs[-1][1] = p["end"] + keep / 2; a = w["start"] - keep / 2
        segs.append([a, w["end"]])
    segs[-1][1] = min(d["audio_duration_secs"], W[-1]["end"] + 0.25)
    pos, out = 0, []
    for w, (a, b) in zip(W, segs):
        out.append({"text": w["text"], "start": round(w["start"] - a + pos, 3), "end": round(w["end"] - a + pos, 3)}); pos += b - a
    f = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={b-a-0.005:.3f}:d=0.005[s{i}];" for i, (a, b) in enumerate(segs))
    f += "".join(f"[s{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(P / "voiceover.mp3"), "-filter_complex", f, "-map", "[o]", "-c:a", "libmp3lame", "-b:a", "192k", str(P / "voiceover_tight.mp3")], check=True)
    wps = len(out) / pos; k = max(1.0, min(1.25, 3.5 / wps)); print("words/s", round(wps, 2), "-> atempo", round(k, 3))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(P / "voiceover_tight.mp3"), "-af", f"atempo={k:.4f},loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", str(P / "voiceover_paced.mp3")], check=True)
    for w in out: w["start"] = round(w["start"] / k, 3); w["end"] = round(w["end"] / k, 3)
    pos /= k
    json.dump(out, open(P / "words_trimmed.json", "w"), indent=1)
    i, starts = 0, []
    for s in shots:  # consume transcript words until they spell this shot's line
        starts.append(out[i]["start"]); target, got = norm(s["line"]), []
        while norm(" ".join(got)) != target:
            assert i < len(out) and len(norm(" ".join(got))) < len(target) + 20, f"transcript doesn't match {s['id']}: {got!r} vs {target!r}"
            got.append(out[i]["text"]); i += 1
    assert i == len(out), f"word count mismatch: script {i} vs audio {len(out)}"
    win = {}
    for j, s in enumerate(shots):
        a = 0.0 if j == 0 else round(starts[j] - 0.05, 2)
        b = round(starts[j + 1] - 0.05, 2) if j + 1 < len(starts) else round(pos, 2)
        win[s["id"]] = [a, b]; print(s["id"], a, b, round(b - a, 2), "OK" if b - a <= 4 else "TOO LONG")
    json.dump(win, open(P / "windows.json", "w"), indent=1)
    print(v, "paced", round(pos, 2), "s")


if __name__ == "__main__":
    for v in [a for a in sys.argv[1:] if a.startswith("V")]: make(v)
