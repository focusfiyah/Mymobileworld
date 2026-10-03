"""Free voiceover tightening (2026-10-03): pauses over 0.25 s cut to 0.25 s, then 1.2x (atempo, pitch kept), like V1's 1p2x.

  python3 vo_prep.py 1 2 3 4 5 6   -> vo/vN_final.wav + vo/vN_final_lines.json (line start/end in the final audio)
"""
import json, subprocess, sys
import numpy as np
SR, GAP, SPEED, PAD = 44100, 0.25, 1.2, 0.05


def prep(n):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"vo/v{n}_voiceover.mp3", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32)
    words = json.load(open(f"vo/v{n}_words.json")); lines = json.load(open(f"vo/v{n}_lines.json"))
    cuts = []                                                  # (start, end) of removed audio
    for w0, w1 in zip(words, words[1:]):
        g = w1["start"] - w0["end"]
        if g > GAP: cuts.append((w0["end"] + PAD + GAP / 2, w1["start"] - PAD - (GAP / 2 - 2 * PAD) if False else w1["start"] - GAP / 2 + PAD))
    cuts = [(s, e) for s, e in cuts if e > s]
    keep, t = [], 0.0
    for s, e in cuts: keep.append((t, s)); t = e
    keep.append((t, len(a) / SR))
    fade = int(0.01 * SR); parts = []
    for s, e in keep:
        seg = a[int(s * SR):int(e * SR)].copy()
        if len(seg) > 2 * fade: seg[:fade] *= np.linspace(0, 1, fade); seg[-fade:] *= np.linspace(1, 0, fade)
        parts.append(seg)
    out = np.concatenate(parts)
    def mapt(x): return (x - sum(min(max(x - s, 0), e - s) for s, e in cuts)) / SPEED
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-", "-af", f"atempo={SPEED}",
                    f"vo/v{n}_final.wav"], input=np.clip(out, -32768, 32767).astype(np.int16).tobytes(), check=True)
    fl = [{"line": L["line"], "start": round(mapt(L["start"]), 2), "end": round(mapt(L["end"]), 2)} for L in lines]
    json.dump(fl, open(f"vo/v{n}_final_lines.json", "w"), indent=1)
    json.dump([{"text": w["text"], "start": round(mapt(w["start"]), 3), "end": round(mapt(w["end"]), 3)} for w in words], open(f"vo/v{n}_final_words.json", "w"), indent=1)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"vo/v{n}_final.wav"], capture_output=True, text=True).stdout)
    print(f"V{n}: {dur:.1f}s, {len(words) / dur:.2f} wps"); [print(f"   {x['start']:5.2f}-{x['end']:5.2f}  {x['line'][:70]}") for x in fl]


for n in sys.argv[1:]: prep(int(n))
