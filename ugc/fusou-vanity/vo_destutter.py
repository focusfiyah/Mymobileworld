"""r5 (Ralph 2026-10-03: V5 'holiday' twice, V6 'if' twice): Grace B's own TTS stuttered ("Ho- holiday", "If, if someone"). Cut the stutter fragment out of the final wav
(times from an ElevenLabs STT check), keep backups vo/vN_final_pre_stutter.*, shift the later word times. Free apart from the STT check."""
import json, os, shutil, subprocess
D = 0.008
CUTS = {5: (13.36, 13.62), 6: (13.05, 13.255)}   # seconds in vo/vN_final.wav: the "Ho-" fragment / the first "If,"
for n, (a, b) in CUTS.items():
    wav, wj = f"vo/v{n}_final.wav", f"vo/v{n}_final_words.json"
    if os.path.exists(f"vo/v{n}_final_pre_stutter.wav"): print(n, "already done"); continue
    shutil.copy(wav, f"vo/v{n}_final_pre_stutter.wav"); shutil.copy(wj, f"vo/v{n}_final_pre_stutter.words.json"); shutil.copy(f"vo/v{n}_final_lines.json", f"vo/v{n}_final_pre_stutter.lines.json")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"vo/v{n}_final_pre_stutter.wav", "-filter_complex",
                    f"[0:a]atrim=0:{a},asetpts=PTS-STARTPTS[x];[0:a]atrim={b},asetpts=PTS-STARTPTS[y];[x][y]acrossfade=d={D}:c1=tri:c2=tri[o]", "-map", "[o]", wav], check=True)
    sh = (b - a) + D; W = json.load(open(wj))
    for w in W:
        if w["start"] >= a - 0.05: w["start"] = round(w["start"] - sh, 3); w["end"] = round(w["end"] - sh, 3)
    json.dump(W, open(wj, "w"), indent=1)
    L = json.load(open(f"vo/v{n}_final_lines.json"))
    for o in L:
        for k in ("start", "end"):
            if o.get(k, 0) >= a - 0.05: o[k] = round(o[k] - sh, 2)
    json.dump(L, open(f"vo/v{n}_final_lines.json", "w"), indent=1)
    print(n, "removed", a, "-", b, "shift", round(sh, 3), "| tail words:", [(w["text"], w["start"]) for w in W[-6:]])
