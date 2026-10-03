"""Grace B voiceovers for Videos 2-6 (Ralph OK 2026-10-03, ~1,660 ElevenLabs chars), same settings as V1 (vo_v1.py).

  python3 vo.py 2 3 4 5 6   -> vo/vN_voiceover.mp3, vo/vN_words.json, vo/vN_lines.json (lines read from the scripts.md table)
"""
import base64, json, re, sys, requests
VOICE = "bGrsdLmwBbYUgHRuMFOI"
SETTINGS = {"stability": 0.4, "similarity_boost": 0.8, "style": 0.0, "speed": 1.0}
md = open("scripts.md").read()


def lines(n):
    sec = md.split(f"## Video {n}:")[1].split("\n## ")[0]
    return [r.split("|")[2].strip() for r in sec.splitlines() if re.match(r"\|\s*\d", r)]


def make(n):
    L = lines(n); text = " ".join(L)
    body = {"text": text, "model_id": "eleven_v4", "voice_settings": SETTINGS}
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128", json=body, timeout=300)
    if not r.ok: sys.exit(f"V{n}: {r.status_code} {r.text[:200]}")
    d = r.json(); open(f"vo/v{n}_voiceover.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
    al = d["alignment"]; words, cur, s0 = [], "", None
    for c, a, b in zip(al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]):
        if c.isspace():
            if cur: words.append({"text": cur, "start": s0, "end": e0}); cur = ""
            continue
        if not cur: s0 = a
        cur += c; e0 = b
    if cur: words.append({"text": cur, "start": s0, "end": e0})
    json.dump(words, open(f"vo/v{n}_words.json", "w"), indent=1)
    i, out = 0, []
    for line in L:
        k = len(line.split()); w = words[i:i + k]; i += k
        out.append({"line": line, "start": round(w[0]["start"], 2), "end": round(w[-1]["end"], 2)})
    json.dump(out, open(f"vo/v{n}_lines.json", "w"), indent=1)
    print(f"V{n}: {len(text)} chars, {len(words)} words, {words[-1]['end']:.1f}s, {len(words) / words[-1]['end']:.2f} wps")
    return len(text)


if __name__ == "__main__":
    print("total chars", sum(make(int(n)) for n in sys.argv[1:]))
