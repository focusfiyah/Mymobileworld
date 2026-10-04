"""r4 (Ralph OK 2026-10-03): re-voice the V2 and V5 closers with Grace B (same settings, previous lines as context) and splice them into vo/vN_final.wav.
Keeps vo/vN_final_pre_r4.* backups. ~120 ElevenLabs chars."""
import base64, json, os, shutil, subprocess, sys, requests
import numpy as np
from vo import VOICE, SETTINGS


def _gate():
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)


SR = 44100
NEW = {2: ("Holiday", "If you want it up for the holidays, it's in the orange cart."), 5: ("Holiday", "Holiday get-ready season is close. It's in the orange cart.")}
KEEP_THROUGH = {2: "parts.", 5: "tool."}   # last word before the closer


def pcm(f): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16)


def fix(n):
    for a in ("wav", "words.json", "lines.json"):
        src = f"vo/v{n}_final.wav" if a == "wav" else f"vo/v{n}_final_{a.split('.')[0]}.json"
        bak = f"vo/v{n}_final_pre_r4.{a}"
        if not os.path.exists(bak): shutil.copy(src, bak)
    W = json.load(open(f"vo/v{n}_final_pre_r4.words.json")); L = json.load(open(f"vo/v{n}_final_pre_r4.lines.json"))
    k = max(i for i, w in enumerate(W) if w["text"] == KEEP_THROUGH[n])           # closer starts after this word
    prev = " ".join(w["text"] for w in W[:k + 1]); text = NEW[n][1]
    body = {"text": text, "model_id": "eleven_v4", "voice_settings": SETTINGS, "previous_text": prev}
    _gate()
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", json=body, timeout=300)
    if not r.ok: sys.exit(f"V{n}: {r.status_code} {r.text[:200]}")
    d = r.json(); tmp = f"/tmp/claude-0/cta_v{n}.mp3"; open(tmp, "wb").write(base64.b64decode(d["audio_base64"]))
    new = pcm(tmp).astype(np.float32); al = d["alignment"]; nw, cur, s0 = [], "", None
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur: nw.append({"text": cur, "start": s0, "end": e0}); cur = ""
            continue
        if not cur: s0 = a
        cur += c; e0 = b
    if cur: nw.append({"text": cur, "start": s0, "end": e0})
    old = pcm(f"vo/v{n}_final_pre_r4.wav").astype(np.float32)
    cut = W[k]["end"] + 0.25; lead = nw[0]["start"]; seg = new[int(max(lead - 0.03, 0) * SR):]
    f = int(0.01 * SR); head = old[:int(cut * SR)].copy(); head[-f:] *= np.linspace(1, 0, f)
    out = np.concatenate([head, seg]); off = cut - max(lead - 0.03, 0)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-", f"vo/v{n}_final.wav"], input=np.clip(out, -32768, 32767).astype(np.int16).tobytes(), check=True)
    json.dump(W[:k + 1] + [{"text": w["text"], "start": round(w["start"] + off, 3), "end": round(w["end"] + off, 3)} for w in nw], open(f"vo/v{n}_final_words.json", "w"), indent=1)
    last_old = L[-1]; L[-1] = {**last_old, "line": text, "start": round(nw[0]["start"] + off, 2), "end": round(nw[-1]["end"] + off, 2)}
    json.dump(L, open(f"vo/v{n}_final_lines.json", "w"), indent=1)
    print(f"V{n}: {len(text)} chars, closer {nw[-1]['end'] - nw[0]['start']:.1f}s, total {len(out) / SR:.1f}s | words:", " ".join(w["text"] for w in nw))
    return len(text)


if __name__ == "__main__":
    print("total chars", sum(fix(int(n)) for n in sys.argv[1:]))
