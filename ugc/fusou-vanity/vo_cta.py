"""Ralph 2026-10-03: no "order it now"; close with Grace's usual "It's in the orange cart." (keeps the real holiday reason, "don't put it off").
Re-voices ONLY the last line of each video (Grace B, same settings, previous lines as context), splices it in, updates scripts.md.
Old files kept as vo/vN_voiceover_v1.mp3 / vN_words_v1.json / vN_lines_v1.json.  ~610 ElevenLabs chars.
"""
import base64, json, os, shutil, subprocess, sys, requests
import numpy as np
from vo import VOICE, SETTINGS


def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)


SR = 44100
NEW = {1: "It ships in three boxes, so if you want it up before the holidays, don't put it off. It's in the orange cart.",
       2: "Holiday shipping gets slow, and it comes in three boxes. It's in the orange cart.",
       3: "That's five things in one order. It ships in three boxes, so don't put it off before the holidays. It's in the orange cart.",
       4: "It comes in three boxes, so if you want it done before the holidays, don't put it off. It's in the orange cart.",
       5: "Holiday get-ready season is close, and it ships in three boxes. It's in the orange cart.",
       6: "If someone in your house keeps asking for a vanity, this one ships in three boxes. It's in the orange cart."}


def pcm(f): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16)


def fix(n):
    for a, b in (("voiceover", "mp3"), ("words", "json"), ("lines", "json")):
        src, bak = f"vo/v{n}_{a}.{b}", f"vo/v{n}_{a}_v1.{b}"
        if not os.path.exists(bak): shutil.copy(src, bak)
    words, lines = json.load(open(f"vo/v{n}_words_v1.json")), json.load(open(f"vo/v{n}_lines_v1.json"))
    old_last = lines[-1]; k = len(words) - len(old_last["line"].split())
    prev = " ".join(L["line"] for L in lines[:-1])
    body = {"text": NEW[n], "model_id": "eleven_v4", "voice_settings": SETTINGS, "previous_text": prev}
    _gate()
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", json=body, timeout=300)
    if not r.ok: sys.exit(f"V{n}: {r.status_code} {r.text[:200]}")
    d = r.json(); open("/tmp/claude-0/-home-user/eb264d06-2517-557b-a9f3-9de446d2ca4a/scratchpad/cta.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    new = pcm("/tmp/claude-0/-home-user/eb264d06-2517-557b-a9f3-9de446d2ca4a/scratchpad/cta.mp3").astype(np.float32)
    al = d["alignment"]; nw, cur, s0 = [], "", None
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur: nw.append({"text": cur, "start": s0, "end": e0}); cur = ""
            continue
        if not cur: s0 = a
        cur += c; e0 = b
    if cur: nw.append({"text": cur, "start": s0, "end": e0})
    old = pcm(f"vo/v{n}_voiceover_v1.mp3").astype(np.float32)
    cut = words[k - 1]["end"] + 0.25                                    # keep the last word before the CTA + a natural 0.25 s pause
    lead = nw[0]["start"]; seg = new[int(max(lead - 0.03, 0) * SR):]   # drop the new clip's leading silence
    f = int(0.01 * SR); head = old[:int(cut * SR)].copy(); head[-f:] *= np.linspace(1, 0, f)
    out = np.concatenate([head, seg]); off = cut - max(lead - 0.03, 0)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-", "-b:a", "128k", f"vo/v{n}_voiceover.mp3"],
                   input=np.clip(out, -32768, 32767).astype(np.int16).tobytes(), check=True)
    allw = words[:k] + [{"text": w["text"], "start": w["start"] + off, "end": w["end"] + off} for w in nw]
    json.dump(allw, open(f"vo/v{n}_words.json", "w"), indent=1)
    lines = lines[:-1] + [{"line": NEW[n], "start": round(nw[0]["start"] + off, 2), "end": round(nw[-1]["end"] + off, 2)}]
    json.dump(lines, open(f"vo/v{n}_lines.json", "w"), indent=1)
    md = open("scripts.md").read()
    if old_last["line"] in md: open("scripts.md", "w").write(md.replace(old_last["line"], NEW[n]))
    else: print(f"   V{n}: old line not found in scripts.md (V1 lines live in vo_v1.py)")
    print(f"V{n}: {len(NEW[n])} chars, new CTA {nw[-1]['end'] - nw[0]['start']:.1f}s, total {len(out) / SR:.1f}s")
    return len(NEW[n])


if __name__ == "__main__":
    print("total chars", sum(fix(int(n)) for n in sys.argv[1:]))
