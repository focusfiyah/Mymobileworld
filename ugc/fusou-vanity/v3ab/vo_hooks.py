"""FUSOU V3 motion redo (2026-10-05): Grace B voices ONLY line 1 (library hook + 'All of this is ONE piece of furniture.') for A and B,
then splices it onto Grace's existing take of lines 2-10 (vo/vA_final.wav). Same voice/settings/tighten as vo_ab.py.
  python3 v3ab/vo_hooks.py A B   (from ugc/fusou-vanity) -> vo/v{A,B}h_final.wav + v{A,B}h_final_lines.json"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent)); import vo_ab
LINES = vo_ab.lines   # keep the real reader (a patched vo_ab.lines once voiced A's hook for B, 99 chars lost)
HERE = vo_ab.HERE; P = HERE / "vo"; SR = vo_ab.SR


def run(v):
    t = f"v{v}h"; L1 = LINES(v)[0]
    import base64, requests
    if (P / f"{t}_words.json").exists(): return splice(v, t)   # already voiced: never pay twice
    vo_ab.require(HERE)
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vo_ab.VOICE}/with-timestamps?output_format=mp3_44100_128",
                      json={"text": L1, "model_id": "eleven_v4", "voice_settings": vo_ab.SETTINGS}, timeout=300)
    if not r.ok: sys.exit(f"{v}: {r.status_code} {r.text[:200]}")
    d = r.json(); (P / f"{t}_voiceover.mp3").write_bytes(base64.b64decode(d["audio_base64"]))
    al = d["alignment"]; words, cur, s0 = [], "", None
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur: words.append({"text": cur, "start": s0, "end": e0}); cur = ""
            continue
        if not cur: s0 = a
        cur += c; e0 = b
    if cur: words.append({"text": cur, "start": s0, "end": e0})
    json.dump(words, open(P / f"{t}_words.json", "w"), indent=1)
    json.dump([{"line": L1, "start": words[0]["start"], "end": words[-1]["end"]}], open(P / f"{t}_lines.json", "w"), indent=1)
    print(v, len(L1), "chars"); splice(v, t)


def splice(v, t):
    vo_ab.prep(t[1:])
    # splice: hook + 0.14 s gap (same as Grace's line1->line2 gap) + her take from line 2 on
    pcm = lambda f: np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout, np.int16).astype(np.float32)
    hook = pcm(P / f"{t}_final.wav"); hl = json.load(open(P / f"{t}_final_lines.json"))[0]
    rest = pcm(P / "vA_final.wav"); RL = json.load(open(P / "vA_final_lines.json"))
    cut0 = RL[1]["start"] - 0.07; hook = hook[:int((hl["end"] + 0.07) * SR)]
    f = int(0.01 * SR); hook[-f:] *= np.linspace(1, 0, f); tail = rest[int(cut0 * SR):].copy(); tail[:f] *= np.linspace(0, 1, f)
    out = np.concatenate([hook, tail]); off = len(hook) / SR - cut0
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-", str(P / f"{t}_final.wav")],
                   input=np.clip(out, -32768, 32767).astype(np.int16).tobytes(), check=True)
    lines = [{"line": hl["line"], "start": hl["start"], "end": hl["end"]}] + [{"line": l["line"], "start": round(l["start"] + off, 2), "end": round(l["end"] + off, 2)} for l in RL[1:]]
    json.dump(lines, open(P / f"{t}_final_lines.json", "w"), indent=1); print(v, f"{len(out) / SR:.2f}s, line 2 at {lines[1]['start']}")


if __name__ == "__main__":
    for v in sys.argv[1:]: run(v)
