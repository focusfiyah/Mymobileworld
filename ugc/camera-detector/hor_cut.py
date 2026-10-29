"""House of Rameau version (2026-10-29, Ralph: every AI video gets a HofR version "with the version and the extras"):
the same voiceover, its own look so TikTok doesn't see a copy of Grace's post: later windows of each clip, a 1.12x
reframe that alternates left/right, a brighter, cooler grade, the hook on screen from frame 0 (whole, held 5 s, inside
the safe zone) and TikTok Classic captions after it. AI finish last.
  python3 hor_cut.py  -> out/camera_detector_hor_v1.mp4"""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, "../../.claude/skills/ugc-product-ad/scripts")
from classic_caption import classic_png, FONT
from PIL import Image, ImageDraw, ImageFont


def bubble_png(rows, size=62, y=430, w=1080, h=1920):
    """Hook: dark text on a white rounded bubble (TikTok's background text style), readable over any frame."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); f = ImageFont.truetype(str(FONT), size)
    lh = int(size * 1.35)
    for i, r in enumerate(rows):
        tw = d.textlength(r, font=f); cy = y + i * lh
        d.rounded_rectangle((w / 2 - tw / 2 - 28, cy - lh / 2 - 4, w / 2 + tw / 2 + 28, cy + lh / 2 + 4), radius=22, fill=(255, 255, 255, 245))
    for i, r in enumerate(rows): d.text((w // 2, y + i * lh), r, font=f, fill=(20, 20, 20), anchor="mm")
    return img


def caption_png(text, size=58, y=1180, w=1080, h=1920):
    """Captions: white semibold, lowercase, a thin dark outline so they read on bright rooms."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); f = ImageFont.truetype(str(FONT), size)
    d.text((w // 2, y), text, font=f, fill="white", anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0, 220))
    return img

NAME, HOLD = "camera_detector_hor_v1", 0.6
HOOK, HOOK_END = "check your hotel room|like this 👀".replace(" 👀", ""), None
CLIPLEN = {"S1": 6.0, "S5": 3.25}
FILE = {"S5": "clips/S5_view.mp4"}
S = json.load(open("shots.json"))["shots"]
W = json.load(open("vo/words_trimmed.json"))
starts = [s["t"][0] for s in S]; END_VO = S[-1]["t"][1]
EDIT, pos = [], 0.0
for k, s in enumerate(S):
    b = starts[k + 1] if k + 1 < len(S) else END_VO + HOLD
    d = b - pos; clip = CLIPLEN.get(s["id"], 4.0); d = min(d, clip)
    ss = max(0.0, clip - d - 0.05) if s["id"] != "S5" else 0.0      # the LATE part of each clip (Grace's cut uses the start)
    EDIT.append((s["id"], ss, d)); pos += d
END = pos; HOOK_END = S[1]["t"][0]                                 # hook up for all of S1 (5.2 s), then captions
Path("out/hor").mkdir(parents=True, exist_ok=True)
bubble_png(HOOK.split("|")).save("out/hor/hook.png")
# captions: 3-4 word groups, lowercase, no "orange cart" line (classic style rule); start after the hook
caps, cur = [], []
for w in W:
    if w["start"] < HOOK_END: continue
    cur.append(w)
    if len(cur) >= 4 or w["text"][-1] in ".,?!":
        caps.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"] for x in cur).lower().strip(".,!?"))); cur = []
if cur: caps.append((cur[0]["start"], cur[-1]["end"], " ".join(x["text"] for x in cur).lower().strip(".,!?")))
caps = [c for c in caps if "orange cart" not in c[2]]
for i, (a, b, t) in enumerate(caps): caption_png(t).save(f"out/hor/cap{i:02d}.png")
inputs, chains = [], []
for i, (c, ss, d) in enumerate(EDIT):
    inputs += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", FILE.get(c, f"clips/{c}_seedance.mp4")]
    x = "0" if i % 2 else "iw-iw/1.12"                              # reframe 1.12x, alternate the side
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,crop=iw/1.12:ih/1.12:{x}:(ih-ih/1.12)/2,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p[v{i}]")
n = len(EDIT)
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.03:contrast=1.04,colorbalance=bs=0.04:rs=-0.02[base]"
ov = ["-i", "out/hor/hook.png"] + sum((["-i", f"out/hor/cap{i:02d}.png"] for i in range(len(caps))), [])
last = "base"; fc += f";[base][{n}:v]overlay=0:0:enable='between(t,0,{HOOK_END:.3f})'[o0]"; last = "o0"
for i, (a, b, t) in enumerate(caps):
    fc += f";[{last}][{n + 1 + i}:v]overlay=0:0:enable='between(t,{a:.3f},{b + 0.12:.3f})'[o{i + 1}]"; last = f"o{i + 1}"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/voiceover_paced.mp3", "-af", "aresample=44100,loudnorm=I=-16:TP=-2.5:LRA=11", "-ar", "44100", "out/_vo.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/_vo.wav", "-af", f"apad=whole_dur={END:.3f}", "-t", f"{END:.3f}", "-ar", "44100", "out/_mix.wav"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, *ov, "-i", "out/_mix.wav", "-filter_complex", fc, "-map", f"[{last}]", "-map", f"{n + 1 + len(caps)}:a",
                "-t", f"{END:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4", "-c:a", "aac", "-b:a", "192k", f"out/{NAME}_review.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"out/{NAME}_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s,", len(caps), "captions, hook 0 -", round(HOOK_END, 2))
