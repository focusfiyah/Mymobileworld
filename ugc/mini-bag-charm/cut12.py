"""Mini Bag Charm v12 (Ralph 2026-10-28: "Free re-cut, no pasted shots", then "Yes, cut it"): only the AI-made shots that
look filmed (S1, S2, S3, S5a, S5b, S6). Grace's same recording, trimmed at word boundaries (vo/words_trimmed.json):
lines kept 1-3, "and you can stash ... inside." (the 'and' kept: cutting it clipped "you") and the CTA; dropped: "It clips right onto your
handbag", "The scarf and gold hardware make it look so much more expensive...", the stocking-stuffer line. No text.
Every clip at 1.0x. AI finish last.  python3 cut12.py -> out/minibag_v12_review.mp4 + out/minibag_v12.mp4 + vo/words_v12.json"""
import json, subprocess
from pathlib import Path

VO = "vo/voiceover_paced.mp3"
# (start, end) in the recording, then the silence after it
AUD = [(0.0, 7.36, 0.20), (8.96, 13.70, 0.25), (21.10, 26.15, 0.60)]   # "and you" is one sound: cutting before "you" clipped it, so "and" stays
# (clip, src start, length): S1 stops at 1.45 s (from ~1.5 s the painted-out key leaves a stub on the ring), S2 starts there; S5a only its clean first 1.66 s; the CTA over S6 then the end of S1
EDIT = [("clips/S1_nokey.mp4", 0.0, 1.45), ("clips/S2_seedance.mp4", 0.0, 2.73), ("clips/S3_seedance.mp4", 0.0, 3.18),
        ("clips/S5a_seedance.mp4", 0.0, 1.66), ("clips/S5b_seedance.mp4", 0.0, 3.32),
        ("clips/S6_seedance.mp4", 0.0, 4.04), ("clips/S1_nokey.mp4", 2.14, 1.82)]
END = sum(b - a + gap for a, b, gap in AUD)
assert abs(sum(d for _, _, d in EDIT) - END) < 0.05, (sum(d for _, _, d in EDIT), END)

# word timings on the new timeline (for qc/check_cut.py --words)
w = json.load(open("vo/words_trimmed.json")); out, t0 = [], 0.0
for a, b, gap in AUD:
    out += [dict(x, start=round(x["start"] - a + t0, 3), end=round(x["end"] - a + t0, 3)) for x in w if a <= x["start"] and x["end"] <= b]
    t0 += b - a + gap
json.dump(out, open("vo/words_v12.json", "w"), indent=1)
print(" ".join(x["text"] for x in out))

inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", c]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT); inputs += ["-i", VO]
aparts = []
for k, (a, b, gap) in enumerate(AUD):
    chains.append(f"[{n}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,apad=pad_dur={gap}[a{k}]")
    aparts.append(f"[a{k}]")
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v];" + \
     "".join(aparts) + f"concat=n={len(AUD)}:v=0:a=1,loudnorm=I=-16:TP=-1.5:LRA=11[a]"
Path("out").mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-ar", "44100", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/minibag_v12_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/minibag_v12_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/minibag_v12.mp4"], check=True)
print("out/minibag_v12.mp4", round(END, 2), "s")
