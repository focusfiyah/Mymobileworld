"""Christmas Fridge Magnets V1 cut (2026-11-07). Shot windows follow vo/windows.json; S4 and S7 trimmed before Wan's
built-in cross-fades (S4 at 1.2 s, S7 at 2.8 s), S3 and S8 hold longer to cover them; S5 uses 0.2-1.86 s (cut at 2.8 s).
No text, no music (Grace adds music if she wants). Never slowed (all clips 1.0x)."""
import subprocess, json
W = json.load(open("vo/words.json"))
PLAN = [("S1",0,4.05),("S2",0,3.64),("S3",0,4.88),("S4",0,1.10),("S5",0.2,1.66),("S6",0,3.30),("S7",0,2.70),("S8",0,3.32),("S9",0,5.00)]
# punch-in cuts (2026-11-07, compare vs @hannahv2246: 2.7 vs 6.9 cuts/10 s): a shot over 2.6 s is split at the word start
# nearest its middle; the clip keeps running, the second part is zoomed 1.12x (under the 1.2x cap), so the cut is visible.
SEG, t0 = [], 0.0
for k, ss, d in PLAN:
    if d > 2.6:
        mids = [w["start"] for w in W if t0 + 1.0 < w["start"] < t0 + d - 1.0]
        m = min(mids, key=lambda s: abs(s - (t0 + d / 2))) - t0 if mids else d / 2
        SEG += [(k, ss, m, 1.0), (k, ss + m, d - m, 1.12)]
    else: SEG.append((k, ss, d, 1.0))
    t0 += d
inp, f = [], ""
for i,(k,ss,d,z) in enumerate(SEG):
    inp += ["-ss",str(ss),"-t",str(d),"-i",f"clips/{k}.mp4"]
    f += f"[{i}:v]scale=1080:1920:flags=lanczos,crop=iw/{z}:ih/{z},scale=1080:1920:flags=lanczos,fps=30,setsar=1,format=yuv420p,trim=duration={d},setpts=PTS-STARTPTS[v{i}];"
f += "".join(f"[v{i}]" for i in range(len(SEG))) + f"concat=n={len(SEG)}:v=1:a=0[v]"
inp += ["-i","vo/voiceover_final.mp3"]
subprocess.run(["ffmpeg","-y","-v","error",*inp,"-filter_complex",f,"-map","[v]","-map",f"{len(SEG)}:a","-c:v","libx264","-preset","veryfast","-crf","18",
                "-threads","4","-c:a","aac","-b:a","192k","-shortest","cut/v1_raw.mp4"],check=True)
print("total", round(sum(s[2] for s in SEG),2), "segments", len(SEG)); json.dump(SEG, open("cut/v1_segments.json","w"), indent=1)
