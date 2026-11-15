"""House of Rameau version of the approved BodyJ v2g cut (Grace's script; Ralph 2026-11-15: "make a HofR versions of cleanwaste and others").
From cut_v2g.py + ugc/cleanwaste-toilet-kit/cut_hor.py: same Grace voiceover (v2g/vo/voiceover_tight.mp3) and approved clips, same word slots,
but its own cut: the two S8 halves swapped (close push-in on "Freaking genius", wide on "USDA organic"), the two S9 halves from other
moments, new in-points on every shot, ~1.1x crops, brighter cool-neutral grade, hook card from frame 0 to 3.0 s low over the counter
(clear of the pour and of every label), no captions. Every clip at 1.0x (assert), AI finish last. $0.
  python3 cut_hor_v2g.py   -> out/bodyj_v2g_hor_review.mp4 + out/bodyj_v2g_hor.mp4"""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAME = "bodyj_v2g_hor"
HOOK = ["The only thing I don't like", "about castor oil..."]
HOOK_Y, HOOK_HOLD = 1110, 3.0
VO = "v2g/vo/voiceover_tight.mp3"
LABEL = {"S1", "S5", "S7", "S8", "S9", "N4"}       # same as cut_v2g.py: real label pasted (label_track.py)
PRE = {"N3": "crop=562:1000:80:40,"}               # brows: crop out the lips, as in cut_v2g.py
# (clip, in-point, slot length = Grace's, crop of the 1080x1920 frame)
EDIT = [
    ("S3", 0.50, 4.41, "980:1742:50:90"),     # thick and messy
    ("N1", 0.35, 4.64, "980:1742:100:60"),    # dripping down your hands
    ("N2", 0.60, 4.30, "980:1742:100:120"),   # the smell
    ("S1", 1.10, 3.82, "980:1742:50:100"),    # liquid gold
    ("S8", 2.60, 2.42, "980:1742:50:60"),     # this roll-on? Freaking genius (Grace: 0.0, wide)
    ("S4", 0.90, 4.10, "980:1742:30:120"),    # no pouring, roll it where you want it
    ("S8", 0.40, 1.72, "1000:1778:40:80"),    # USDA organic (Grace: 2.42, close)
    ("S5", 1.50, 3.36, "980:1742:50:40"),     # rose quartz roller
    ("S9", 0.30, 2.58, "980:1742:100:120"),   # link it in the orange cart
    ("N3", 1.50, 1.64, "1000:1778:40:60"),    # conditioned brows
    ("N4", 2.00, 1.20, "980:1742:50:100"),    # softer cuticles
    ("S6", 2.50, 1.08, "980:1742:50:100"),    # moisturized skin
    ("S7", 1.80, 2.64, "980:1742:50:90"),     # hair growing longer
    ("S9", 3.60, None, "980:1742:50:120"),    # you know what to do (runs to the end of the VO + tail)
]
TAIL = 0.25
vo_len = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VO], capture_output=True, text=True).stdout)
END = vo_len + TAIL
pos, rows = 0.0, []
for k, (c, a, d, crop) in enumerate(EDIT):
    if d is None: d = END - pos
    src = f"clips_label/{c}.mp4" if c in LABEL else f"clips/{c}.mp4"
    clip = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    assert a + d <= clip + 0.01, f"{c}: {a}+{d:.2f}s > {clip:.2f}s clip (never stretch)"
    rows.append((c, a, d, crop, src)); print(c, f"in {a:.2f} len {d:.2f} at {pos:.2f}"); pos += d
Path("out").mkdir(exist_ok=True)
at = 0.0; ej = []
for c, a, d, crop, src in rows: ej.append({"id": c, "in": a, "len": round(d, 3), "at": round(at, 3)}); at += d
json.dump(ej, open("out/hor_edit.json", "w"), indent=1)

card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
f = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 58)
h = 100 + 80 * (len(HOOK) - 1) + 40
dr.rounded_rectangle((80, HOOK_Y, 920, HOOK_Y + h), radius=36, fill=(255, 255, 255, 240))
for k, line in enumerate(HOOK):
    dr.text((500, HOOK_Y + 70 + k * 80), line, fill=(20, 40, 70), font=f, anchor="mm")
    bb = dr.textbbox((500, HOOK_Y + 70 + k * 80), line, font=f, anchor="mm"); assert bb[0] >= 100 and bb[2] <= 900, (line, bb)
assert HOOK_Y >= 360 and HOOK_Y + h <= 1340, "hook outside the 9:16 safe zone"
card.save("out/hor_hook.png")
json.dump({"box": f"80,{HOOK_Y},840,{h}", "hold": HOOK_HOLD}, open("out/hor_hookbox.json", "w"))

ins, ch = [], []
for i, (c, a, d, crop, src) in enumerate(rows):
    ins += ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", src]
    ch.append(f"[{i}:v]setpts=PTS-STARTPTS,{PRE.get(c, '')}scale=1080:1920:flags=lanczos,crop={crop},scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setsar=1[v{i}]")
n = len(rows)
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(n)) + \
     f"concat=n={n}:v=1:a=0,eq=brightness=0.035:contrast=1.03:saturation=1.0,colorbalance=bs=0.06:rs=-0.04:bm=0.03:rm=-0.02[g];[g][{n + 1}:v]overlay=0:0:enable='lt(t,{HOOK_HOLD})'[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO, "-af", f"aresample=44100,loudnorm=I=-15:TP=-1.5:LRA=11,apad,atrim=0:{END:.3f},afade=t=out:st={END - TAIL:.3f}:d={TAIL}",
                "-ar", "44100", "out/_hor_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", "out/_hor_vo.wav", "-i", "out/hor_hook.png", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{n}:a", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"out/{NAME}_review.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
