"""Re-voice ONE line in the middle of a voiceover (Grace B, same settings; previous and next lines as context) and splice it in.
  python3 vo_line.py N K "new line"     (K = 0-based line index in vo/vN_lines.json). Old files kept as vo/vN_*_preline.*
Ralph OK 2026-10-03 (Humanizer fix V1: no "heads up").
"""
import base64, json, os, shutil, subprocess, sys, requests
import numpy as np
from vo import VOICE, SETTINGS


def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)
SR = 44100
TMP = "/tmp/claude-0/-home-user/eb264d06-2517-557b-a9f3-9de446d2ca4a/scratchpad/line.mp3"


def pcm(f): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16).astype(np.float32)


def words_of(al):
    out, cur, s0 = [], "", None
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur: out.append({"text": cur, "start": s0, "end": e0}); cur = ""
            continue
        if not cur: s0 = a
        cur += c; e0 = b
    if cur: out.append({"text": cur, "start": s0, "end": e0})
    return out


n, k, new = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
for a, b in (("voiceover", "mp3"), ("words", "json"), ("lines", "json")):
    shutil.copy(f"vo/v{n}_{a}.{b}", f"vo/v{n}_{a}_preline.{b}")
W, L = json.load(open(f"vo/v{n}_words.json")), json.load(open(f"vo/v{n}_lines.json"))
i0 = sum(len(x["line"].split()) for x in L[:k]); i1 = i0 + len(L[k]["line"].split())
body = {"text": new, "model_id": "eleven_v4", "voice_settings": SETTINGS,
        "previous_text": " ".join(x["line"] for x in L[:k]), "next_text": " ".join(x["line"] for x in L[k + 1:])}
_gate()
r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", json=body, timeout=300)
if not r.ok: sys.exit(f"{r.status_code} {r.text[:200]}")
d = r.json(); open(TMP, "wb").write(base64.b64decode(d["audio_base64"])); nw = words_of(d["alignment"]); seg = pcm(TMP)
old = pcm(f"vo/v{n}_voiceover_preline.mp3")
a = W[i0 - 1]["end"] + 0.25 if i0 else 0.0            # keep the word before + a 0.25 s pause
b = W[i1]["start"] - 0.25 if i1 < len(W) else len(old) / SR
lead = max(nw[0]["start"] - 0.03, 0); tail = nw[-1]["end"] + 0.05
seg = seg[int(lead * SR):int(tail * SR)]
f = int(0.01 * SR); head, rest = old[:int(a * SR)].copy(), old[int(b * SR):].copy()
head[-f:] *= np.linspace(1, 0, f); rest[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
out = np.concatenate([head, seg, rest]); shift = (a + len(seg) / SR) - b
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-", "-b:a", "128k", f"vo/v{n}_voiceover.mp3"],
               input=np.clip(out, -32768, 32767).astype(np.int16).tobytes(), check=True)
nw = [{"text": w["text"], "start": w["start"] - lead + a, "end": w["end"] - lead + a} for w in nw]
W2 = W[:i0] + nw + [{"text": w["text"], "start": w["start"] + shift, "end": w["end"] + shift} for w in W[i1:]]
json.dump(W2, open(f"vo/v{n}_words.json", "w"), indent=1)
L2, j = [], 0
for x in L[:k] + [{"line": new}] + L[k + 1:]:
    c = len(x["line"].split()); L2.append({"line": x["line"], "start": round(W2[j]["start"], 2), "end": round(W2[j + c - 1]["end"], 2)}); j += c
json.dump(L2, open(f"vo/v{n}_lines.json", "w"), indent=1)
print(f"V{n} line {k}: {len(new)} chars, {len(out) / SR:.1f}s total")
