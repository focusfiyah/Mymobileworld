"""House of Rameau version of the approved PRITECH V1 (Ralph 2026-11-15: "make a HofR versions of cleanwaste and others").
From cut.py + ugc/cleanwaste-toilet-kit/cut_hor.py: same approved Grace voiceover (vo/vo_final.wav) and clips, same word slots, own cut:
S8/S9 swapped (both the brush on its dock), S4 plays its later close-up of the bristles, new in-points, ~1.1x crops, brighter cool-neutral
grade, hook card from frame 0 to 3.0 s, no captions. No eyes or mouth (REMOVED.md): crops only zoom in. Every clip at 1.0x (assert). $0.
  python3 cut_hor.py   -> out/pritech_hor_review.mp4 + out/pritech_hor.mp4"""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

NAME = "pritech_hor"
HOOK = ["Not using a cleansing brush?", "What are you doing?"]
HOOK_Y, HOOK_HOLD = 1120, 3.0
VO = "vo/vo_final.wav"
HOLD = 0.6
S = {s["id"]: s for s in json.load(open("shots.json"))}
ids = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9"]
SHIFT = {"S2": 0.10}                     # as cut.py
slot = {}
for k, i in enumerate(ids):
    a, b = S[i]["t"]
    slot[i] = b - a + (HOLD if k == len(ids) - 1 else 0) + SHIFT.get(i, 0) - (SHIFT.get(ids[k - 1], 0) if k else 0)
# (slot, clip file, in-point, crop of the 1080x1920 frame)
EDIT = [("S1", "S1c", 0.40, "980:1742:60:120"), ("S2", "S2_fix", 0.05, "980:1742:50:60"), ("S3", "S3", 0.03, "980:1742:100:100"),
        ("S4", "S4", 1.60, "1000:1778:40:40"), ("S5", "S5", 2.00, "980:1742:50:100"), ("S6", "S6_final", 0.0, "980:1742:50:110"),
        ("S7", "S7", 0.30, "980:1742:100:0"), ("S8", "S9", 0.30, "980:1742:50:100"), ("S9", "S8", 0.60, "980:1742:50:120")]
rows, pos, ej = [], 0.0, []
for sl, c, a, crop in EDIT:
    d = slot[sl]; f = f"clips/{c}.mp4"
    L = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
    assert a + d <= L + 1e-3, f"{c}: {a}+{d:.2f}s > {L:.2f}s clip (never stretch)"
    rows.append((f, a, d, crop)); ej.append({"id": c, "slot": sl, "in": a, "len": round(d, 3), "at": round(pos, 3)}); print(sl, c, f"in {a:.2f} len {d:.2f}"); pos += d
END = pos
Path("out").mkdir(exist_ok=True); json.dump(ej, open("out/hor_edit.json", "w"), indent=1)
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
fo = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 58)
h = 100 + 80 * (len(HOOK) - 1) + 40
dr.rounded_rectangle((80, HOOK_Y, 920, HOOK_Y + h), radius=36, fill=(255, 255, 255, 240))
for k, line in enumerate(HOOK):
    dr.text((500, HOOK_Y + 70 + k * 80), line, fill=(20, 40, 70), font=fo, anchor="mm")
    bb = dr.textbbox((500, HOOK_Y + 70 + k * 80), line, font=fo, anchor="mm"); assert bb[0] >= 100 and bb[2] <= 900, (line, bb)
assert HOOK_Y >= 360 and HOOK_Y + h <= 1340
card.save("out/hor_hook.png"); json.dump({"box": f"80,{HOOK_Y},840,{h}", "hold": HOOK_HOLD}, open("out/hor_hookbox.json", "w"))
ins, ch, cum = [], [], 0.0
for i, (f, a, d, crop) in enumerate(rows):   # frame-exact segment ends, as cut.py
    nf = round((cum + d) * 30) - round(cum * 30); cum += d
    ins += ["-ss", f"{a:.3f}", "-i", f]
    ch.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,trim=end_frame={nf},setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,crop={crop},scale=1080:1920:flags=lanczos,format=yuv420p,setsar=1[v{i}]")
n = len(rows)
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(n)) + \
     f"concat=n={n}:v=1:a=0,eq=brightness=0.05:contrast=1.03:saturation=1.0,colorbalance=bs=0.06:rs=-0.04:bm=0.03:rm=-0.02[g];[g][{n + 1}:v]overlay=0:0:enable='lt(t,{HOOK_HOLD})'[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO, "-af", f"aresample=44100,loudnorm=I=-15:TP=-1.5:LRA=11,apad,atrim=0:{END:.3f},afade=t=out:st={END - 0.3:.3f}:d=0.3",
                "-ar", "44100", "out/_hor_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", "out/_hor_vo.wav", "-i", "out/hor_hook.png", "-filter_complex", fc,
                "-map", "[v]", "-map", f"{n}:a", "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"out/{NAME}_review.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
