"""Grace B voiceovers for V1 versions A and B (Ralph OK 2026-10-03, ~1,060 ElevenLabs chars), same voice/settings as vo.py.
  python3 vo_ab.py A B   (run from ugc/fusou-vanity/v1ab) -> vo/vA_voiceover.mp3, vA_words.json, vA_lines.json, then free tighten -> vA_final.wav + _final_words/_lines.json
"""
import base64, json, re, subprocess, sys
from pathlib import Path
import numpy as np, requests
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "grace")); from gate import require
VOICE = "bGrsdLmwBbYUgHRuMFOI"; SETTINGS = {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}
SR, GAP, SPEED, PAD = 44100, 0.25, 1.2, 0.05
md = (HERE / "scripts.md").read_text()


def lines(v):
    sec = md.split(f"## Version {v}")[1].split("\n## ")[0]
    return [r.split("|")[2].strip() for r in sec.splitlines() if re.match(r"\|\s*\d", r)]


def make(v):
    L = lines(v); text = " ".join(L)
    require(HERE)
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
                      json={"text": text, "model_id": "eleven_v4", "voice_settings": SETTINGS}, timeout=300)
    if not r.ok: sys.exit(f"{v}: {r.status_code} {r.text[:200]}")
    d = r.json(); (HERE / f"vo/v{v}_voiceover.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    al = d["alignment"]; words, cur, s0 = [], "", None
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur: words.append({"text": cur, "start": s0, "end": e0}); cur = ""
            continue
        if not cur: s0 = a
        cur += c; e0 = b
    if cur: words.append({"text": cur, "start": s0, "end": e0})
    json.dump(words, open(HERE / f"vo/v{v}_words.json", "w"), indent=1)
    i, out = 0, []
    for line in L:
        k = len(line.split()); w = words[i:i + k]; i += k
        out.append({"line": line, "start": round(w[0]["start"], 2), "end": round(w[-1]["end"], 2)})
    json.dump(out, open(HERE / f"vo/v{v}_lines.json", "w"), indent=1)
    print(f"{v}: {len(text)} chars, {len(words)} words, {words[-1]['end']:.1f}s"); return len(text)


def prep(v):   # free: pauses > 0.25 s cut to 0.25 s, then 1.2x (same as vo_prep.py)
    P = HERE / "vo"
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(P / f"v{v}_voiceover.mp3"), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16).astype(np.float32)
    words = json.load(open(P / f"v{v}_words.json")); lns = json.load(open(P / f"v{v}_lines.json")); cuts = []
    for w0, w1 in zip(words, words[1:]):
        if w1["start"] - w0["end"] > GAP: cuts.append((w0["end"] + PAD + GAP / 2, w1["start"] - GAP / 2 + PAD))
    cuts = [(s, e) for s, e in cuts if e > s]; keep, t = [], 0.0
    for s, e in cuts: keep.append((t, s)); t = e
    keep.append((t, len(a) / SR)); fade = int(0.01 * SR); parts = []
    for s, e in keep:
        seg = a[int(s * SR):int(e * SR)].copy()
        if len(seg) > 2 * fade: seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        parts.append(seg)
    mapt = lambda x: (x - sum(min(max(x - s, 0), e - s) for s, e in cuts)) / SPEED
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-", "-af", f"atempo={SPEED}", str(P / f"v{v}_final.wav")],
                   input=np.clip(np.concatenate(parts), -32768, 32767).astype(np.int16).tobytes(), check=True)
    json.dump([{"line": L["line"], "start": round(mapt(L["start"]), 2), "end": round(mapt(L["end"]), 2)} for L in lns], open(P / f"v{v}_final_lines.json", "w"), indent=1)
    json.dump([{"text": w["text"], "start": round(mapt(w["start"]), 3), "end": round(mapt(w["end"]), 3)} for w in words], open(P / f"v{v}_final_words.json", "w"), indent=1)


if __name__ == "__main__":
    print("total chars", sum(make(v) for v in sys.argv[1:]))
    for v in sys.argv[1:]: prep(v)
