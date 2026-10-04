"""Remove the "three boxes" clause from each final voiceover (Ralph 2026-10-03: take it out of all 6), free: ffmpeg splice at word boundaries.
Originals are kept as vo/vN_final_pre_boxes.{wav,words.json,lines.json}. Run once."""
import json, os, shutil, subprocess, sys
D = 0.012   # crossfade at the joint
SPEC = {1: (-3, 2), 2: (-4, 1), 3: (-3, 2), 4: (-3, 2), 5: (-4, 1), 6: (-4, 1)}   # words removed = [j+a, j+b] where j = index of "three"
for n, (a, b) in SPEC.items():
    wav, wj, lj = f"vo/v{n}_final.wav", f"vo/v{n}_final_words.json", f"vo/v{n}_final_lines.json"
    if os.path.exists(f"vo/v{n}_final_pre_boxes.wav"): print(n, "already spliced"); continue
    W = json.load(open(wj)); j = next(i for i, w in enumerate(W) if w["text"].lower().startswith("three") and W[i + 1]["text"].lower().startswith("boxes"))
    i0, i1 = j + a, j + b; gone = [w["text"] for w in W[i0:i1 + 1]]
    A = min(W[i0 - 1]["end"] + 0.04, W[i0]["start"]); B = max(W[i1 + 1]["start"] - 0.04, W[i1]["end"])
    print(f"V{n}: removing {gone} | keep to {A:.2f}, resume at {B:.2f}")
    for ext, f in (("wav", wav), ("words.json", wj), ("lines.json", lj)): shutil.copy(f, f"vo/v{n}_final_pre_boxes.{ext}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"vo/v{n}_final_pre_boxes.wav", "-filter_complex",
                    f"[0:a]atrim=0:{A},asetpts=PTS-STARTPTS[x];[0:a]atrim={B},asetpts=PTS-STARTPTS[y];[x][y]acrossfade=d={D}:c1=tri:c2=tri[o]", "-map", "[o]", wav], check=True)
    shift = (B - A) + D
    N = [dict(w) for k, w in enumerate(W) if not (i0 <= k <= i1)]
    for w in N:
        if w["start"] >= B - 1e-6: w["start"] = round(w["start"] - shift, 3); w["end"] = round(w["end"] - shift, 3)
    json.dump(N, open(wj, "w"), indent=1)
    L = json.load(open(lj)); phrase = " ".join(gone)
    for o in (L if isinstance(L, list) else L.get("lines", [])):
        if o.get("start", 0) >= B - 1e-6: o["start"] = round(o["start"] - shift, 3)
        if o.get("end", 0) >= B - 1e-6: o["end"] = round(o["end"] - shift, 3)
    json.dump(L, open(lj, "w"), indent=1)
    print("   new length", subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout.strip(),
          "| words now:", " ".join(w["text"] for w in N[-12:]))
