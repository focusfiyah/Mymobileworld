"""Boo-Boo Gel, House of Rameau Black Friday version (Ralph 2026-11-12: "we can just increase the time. Maybe add some
more B-roll"): same words as HofR V2 re-voiced with Ralph's free Chatterbox clone (vo/ralph.wav, vo_build.py), the job's
approved clips (../clips) in new windows + two free Pexels clips (broll/SOURCES.md), hook card from frame 0 (HofR keeps
hook text, no captions), bright neutral grade, AI finish last. Every clip 1.0x; each shot starts on its line's first word
(vo/starts.json). Never uses S3_seedance_r1 (gel beside the scrape, REMOVED.md).
  python3 cut.py -> out/bf_boo_boo_review.mp4 (veryfast) + out/bf_boo_boo.mp4 (AI finish)"""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
C = "../clips/"
HOOK = "the bandaid fight|is officially over"
st = json.loads(Path("vo/starts.json").read_text()); L = st["starts"]; END = round(st["end"] + 0.4, 3)
# (source, in-point, start on the VO timeline, punch-in)  line: words
SEG = [(C + "S3_seedance.mp4", 0.30, L[0], 1.06),        # L0 "...until a scraped knee": gel goes ON the scrape
       ("broll/scooter_girl.mp4", 0.20, L[1], 1.00),     # L1 "Usually it's tears": kid on a scooter
       (C + "S2_seedance.mp4", 1.70, L[1] + 1.50, 1.08), # L1 "...and a bandaid fight": the scooter on the grass
       (C + "S1.mp4", 1.00, L[2], 1.05),                 # L2 "No sting, so they dab it on themselves": the pump
       ("broll/snow_slide.mp4", 0.00, L[3], 1.00),       # L3 "Only problem?": kid slides into the snow
       (C + "S6.mp4", 0.30, L[3] + 1.90, 1.04),          # L3 "...every bump": bottle outside
       (C + "S5.mp4", 2.00, L[4], 1.06),                 # L4 "Grab one per bag": backpack pocket
       (C + "S4.mp4", 3.00, L[5], 1.05)]                 # L5 "It's in the orange cart": counter
Path("out").mkdir(exist_ok=True)
ins, ch = [], []
for i, (src, ss, t0, z) in enumerate(SEG):
    d = (SEG[i + 1][2] if i + 1 < len(SEG) else END) - t0
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    assert ss + d <= dur + 0.01, f"{src} needs {ss + d:.2f} s, has {dur:.2f} (never stretch)"
    w, h = round(1080 * z / 2) * 2, round(1920 * z / 2) * 2
    ins += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", src]
    ch.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
              f"scale={w}:{h}:flags=lanczos,crop=1080:1920,fps=30,format=yuv420p,setsar=1[v{i}]")
n = len(SEG)
Path("out/seg_times.json").write_text(json.dumps([[s[0], s[2]] for s in SEG]))
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
f = ImageFont.truetype("../../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 62)
dr.rounded_rectangle((170, 420, 910, 610), radius=36, fill=(255, 255, 255, 240))
for k, line in enumerate(HOOK.split("|")): dr.text((540, 475 + k * 80), line, fill=(20, 40, 70), font=f, anchor="mm")
card.save("out/hook.png")
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.02:saturation=0.98,colorbalance=bs=0.02:bm=0.01[g];" \
     f"[g][{n + 1}:v]overlay=0:0:enable='lt(t,{SEG[1][2]})'[v];[{n}:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{END},afade=t=out:st={END - 0.2}:d=0.2[a]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", "vo/ralph.wav", "-i", "out/hook.png", "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-t", f"{END}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", "out/bf_boo_boo_review.mp4"], check=True)
# AI finish = ai_finish.sh values (grain 6, sharpen 0.6, saturation 0.92) with a 20 Mb/s cap (the plain script made 108 MB)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/bf_boo_boo_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/bf_boo_boo.mp4"], check=True)
# review-page copy (the page takes files up to 15 MB)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/bf_boo_boo.mp4", "-c:v", "libx264", "-b:v", "4.5M", "-maxrate", "5M", "-bufsize", "10M",
                "-preset", "veryfast", "-threads", "4", "-c:a", "copy", "-movflags", "+faststart", "review/bf_boo_boo.mp4"], check=True)
print("OK out/bf_boo_boo.mp4", END, "s")
