"""House of Rameau version of the approved Cleanwaste V1 (Ralph 2026-11-15: "make a HofR versions of cleanwaste and others").
Copied from ugc/novatabz-tablets/cut_hor.py: same approved Grace voiceover and clips, own cut so TikTok does not read it as a
copy of Grace's post: S8/S9 swapped (both show the kit going into the emergency bin), other in-points, per-shot crops,
a slightly brighter cool-neutral grade, hook card from frame 0 to 3.0 s (top of frame, clear of every label), no captions.
Every clip plays at 1.0x from its in-point (assert below), AI finish last. $0.
  python3 cut_hor.py        -> out/cleanwaste_hor_review.mp4 (veryfast) + out/cleanwaste_hor.mp4 (AI finish)"""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAME = "cleanwaste_hor"
W = {w["id"]: w for w in json.load(open("vo/windows.json"))}
TAIL = 0.35
HOOK = ["Ready for a power outage?", "What about the toilet?"]
HOOK_Y, HOOK_HOLD = 400, 3.0
# (shot, in-point s, crop of the 1080x1920 frame "w:h:x:y")
ORDER = [("V1S1", 0.8, "960:1707:120:60"), ("V1S2", 1.2, "940:1671:0:200"), ("V1S3", 0.0, "940:1671:0:200"),
         ("V1S4", 0.25, "1080:1920:0:0"), ("V1S5", 0.5, "940:1671:110:120"), ("V1S6", 0.15, "1010:1796:45:62"),
         ("V1S7", 1.0, "940:1671:140:100"), ("V1S9", 2.0, "1000:1778:0:100"), ("V1S8", 2.5, "1000:1778:70:60")]
# slot boundaries = Grace's cut points (word times), with her S7 end moved 0.3 s later as in cut.py
cuts = [W[k]["cut"] for k in ["V1S1", "V1S2", "V1S3", "V1S4", "V1S5", "V1S6", "V1S7", "V1S8"]]
cuts[6] += 0.3
END = W["V1S9"]["cut"] + TAIL
bounds = [0.0] + cuts + [END]
EDIT = []
for k, (sid, ss, crop) in enumerate(ORDER):
    d = bounds[k + 1] - bounds[k]
    clip = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"clips/{sid}.mp4"], capture_output=True, text=True).stdout)
    assert ss + d <= clip + 0.01, f"{sid} needs {ss + d:.2f} s, clip is {clip:.2f} s (never stretch)"
    EDIT.append((sid, ss, d, crop))
    print(sid, f"in {ss:.2f} len {d:.2f}")
Path("out").mkdir(exist_ok=True)
json.dump([{"id": e[0], "in": e[1], "len": round(e[2], 3), "at": round(bounds[i], 3)} for i, e in enumerate(EDIT)], open("out/hor_edit.json", "w"), indent=1)

card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 58)
h = 100 + 80 * (len(HOOK) - 1) + 40
dr.rounded_rectangle((80, HOOK_Y, 920, HOOK_Y + h), radius=36, fill=(255, 255, 255, 240))
for k, line in enumerate(HOOK):
    dr.text((500, HOOK_Y + 70 + k * 80), line, fill=(20, 40, 70), font=f, anchor="mm")
    bb = dr.textbbox((500, HOOK_Y + 70 + k * 80), line, font=f, anchor="mm"); assert bb[0] >= 100 and bb[2] <= 900, (line, bb)
card.save("out/hor_hook.png")
json.dump({"box": f"80,{HOOK_Y},840,{h}", "hold": HOOK_HOLD}, open("out/hor_hookbox.json", "w"))

inputs, chains = [], []
for i, (sid, ss, d, crop) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", f"clips/{sid}.mp4"]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,crop={crop},scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setsar=1[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + \
     f"concat=n={n}:v=1:a=0,eq=brightness=0.04:contrast=1.03:saturation=1.03,colorbalance=bs=0.07:rs=-0.04:bm=0.03:rm=-0.02[g];[g][{n + 1}:v]overlay=0:0:enable='lt(t,{HOOK_HOLD})'[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/voiceover_tight.wav", "-af",
                f"aresample=44100,loudnorm=I=-15:TP=-1.5:LRA=11,apad,atrim=0:{END:.3f},afade=t=out:st={END - TAIL:.3f}:d={TAIL}", "-ar", "44100", "out/_hor_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", "out/_hor_vo.wav", "-i", "out/hor_hook.png", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{n}:a", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"out/{NAME}_review.mp4"], check=True)
# AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK §6 bitrate cap
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
