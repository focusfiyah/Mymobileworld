"""Voiceover (Grace's ONE voice, grace/voice/grace.json, Grace's pick 2026-10-20): eleven_v4 render -> vo/voiceover_raw.mp3,
free pace to 3.5 words/s + -16 LUFS (grace/voice/pace.py) -> vo/voiceover_paced.mp3, free echo clean (grace/voice/clean.py)
-> vo/voiceover.mp3, scribe_v2 word times on the final file -> vo/stt.json, shot windows written back into shots.json.
  python3 vo.py            full run (ElevenLabs TTS + STT are paid characters; gate-protected)
  python3 vo.py --after-pace   reuse vo/voiceover_paced.mp3: clean + STT only
  python3 vo.py --retime   reuse vo/voiceover.mp3 + vo/stt.json (no paid calls)"""
import json, re, subprocess, sys
from pathlib import Path
import requests
def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)


HERE = Path(__file__).resolve().parent; VOICE_DIR = HERE.parents[1] / "grace/voice"
G = json.loads((VOICE_DIR / "grace.json").read_text())
J = json.loads((HERE / "shots.json").read_text()); P = HERE / "vo"
text = " ".join(s["vo"] for s in J["shots"])
AFTER = "--after-pace" in sys.argv   # resume after a failed clean step: reuse vo/voiceover_paced.mp3 (no new TTS)
if "--retime" not in sys.argv and not AFTER:
    body = {"text": text, "model_id": G["model_id"], "voice_settings": G["voice_settings"]}
    json.dump({"voice_id": G["voice_id"], **body}, open(P / "vo.json", "w"), indent=1)
    _gate()
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{G['voice_id']}?output_format=mp3_44100_128", json=body, timeout=300); r.raise_for_status()
    (P / "voiceover_raw.mp3").write_bytes(r.content)
    subprocess.run([sys.executable, str(VOICE_DIR / "pace.py"), str(P / "voiceover_raw.mp3"), str(P / "voiceover_paced.mp3"), "--wps", "3.5"], check=True)
if "--retime" not in sys.argv:
    subprocess.run([sys.executable, str(VOICE_DIR / "clean.py"), str(P / "voiceover_paced.mp3"), str(P / "voiceover.mp3")], check=True)
    _gate()
    r = requests.post("https://api.elevenlabs.io/v1/speech-to-text", data={"model_id": "scribe_v2", "timestamps_granularity": "word"},
                      files={"file": open(P / "voiceover.mp3", "rb")}, timeout=300); r.raise_for_status()
    json.dump(r.json(), open(P / "stt.json", "w"), indent=1)
d = json.load(open(P / "stt.json")); print("final", d["audio_duration_secs"], "|", d["text"])
W = [w for w in d["words"] if w["type"] == "word"]
ALIAS = {"schnuggle": "shnuggle", "wanna": "wantto"}  # STT spellings of what the script says (brand spelling; fast "want to")
def norm(x):
    x = re.sub(r"[^a-z0-9 ]", "", x.lower().replace("\u2019", "'").replace("'", ""))
    return "".join(ALIAS.get(w, w) for w in x.split())
i, starts = 0, []
for s in J["shots"]:  # consume transcript words until they spell this shot's line (catches dropped or misheard words)
    starts.append(W[i]["start"]); target, got = norm(s["vo"]), ""
    while got != target:
        assert len(got) < len(target) and i < len(W), f"transcript doesn't match {s['id']}: {got!r} vs {target!r}"
        got += norm(W[i]["text"]); i += 1
assert i == len(W), f"word count mismatch: script {i} vs audio {len(W)}"
end = round(d["audio_duration_secs"], 2)
for k, s in enumerate(J["shots"]):
    a = 0.0 if k == 0 else round(starts[k] - 0.05, 2)
    b = round(starts[k + 1] - 0.05, 2) if k + 1 < len(starts) else end
    s["t"] = [a, b]; print(s["id"], a, b, round(b - a, 2), "clip", s["dur"], "OK" if b - a <= s["dur"] else "TOO LONG")
json.dump(J, open(HERE / "shots.json", "w"), indent=1)
