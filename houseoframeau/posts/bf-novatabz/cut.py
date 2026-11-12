"""NovaTabz, House of Rameau holiday version (Black Friday challenge, Ralph 2026-11-12): Ralph's free Chatterbox voice (vo/ralph_cbx.wav, vo_gen.py + join.py; was ElevenLabs vo/ralph.mp3 until Ralph 2026-11-12),
Grace's approved NovaTabz clips (ugc/novatabz-tablets/clips) in a new order and framing, two free Pexels holiday clips
(broll/SOURCES.md), hook text card from frame 0 (HofR keeps hook text, no captions), bright neutral grade, AI finish last.
Every clip plays at 1.0x. Shots start on their line's first word (vo/line_starts.json from readback.py).
  python3 cut.py -> out/bf_novatabz_review.mp4 (veryfast) + out/bf_novatabz.mp4 (AI finish)"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
C = "../../../ugc/novatabz-tablets/clips/"
HOOK = "This immediately made me|think of my wife"
END = 25.20 + 0.4   # last word ends 25.20 s (vo/words.json)
# (source, in-point, start on the VO timeline, crop "w:h:x:y" of a 1080x1920 frame)
SEG = [(C + "S1.mp4", 0.3, 0.00, "980:1742:50:60"),
       (C + "S2.mp4", 0.0, 2.54, "1000:1778:40:100"),
       (C + "S4.mp4", 1.0, 6.56, "920:1636:80:160"),
       (C + "S3.mp4", 0.0, 9.34, "1000:1778:0:80"),
       ("broll/gift_wrap.mp4", 2.0, 13.38, "1080:1920:0:0"),
       (C + "S5.mp4", 0.3, 17.56, "960:1707:60:120"),
       ("broll/stockings.mp4", 1.0, 21.16, "1080:1920:0:0"),
       (C + "S6.mp4", 1.5, 24.34, "1000:1778:40:60")]
Path("out").mkdir(exist_ok=True)
ins, ch = [], []
for i, (src, ss, t0, crop) in enumerate(SEG):
    d = (SEG[i + 1][2] if i + 1 < len(SEG) else END) - t0
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    assert ss + d <= dur + 0.01, f"{src} needs {ss + d:.2f} s, has {dur:.2f} (never stretch)"
    ins += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", src]
    ch.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop={crop},"
              f"scale=1080:1920:flags=lanczos,fps=30,format=yuv420p,setsar=1[v{i}]")
n = len(SEG)
card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
f = ImageFont.truetype("../../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 60)
dr.rounded_rectangle((110, 380, 970, 560), radius=36, fill=(255, 255, 255, 240))
for k, line in enumerate(HOOK.split("|")): dr.text((540, 430 + k * 80), line, fill=(20, 40, 70), font=f, anchor="mm")
card.save("out/hook.png")
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,eq=brightness=0.02:contrast=1.03,colorbalance=bs=0.02:rs=-0.02[g];" \
     f"[g][{n + 1}:v]overlay=0:0:enable='lt(t,{SEG[1][2]})'[v];[{n}:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{END}[a]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-i", "vo/ralph_cbx.wav", "-i", "out/hook.png", "-filter_complex", fc,
                "-map", "[v]", "-map", "[a]", "-t", f"{END}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", "out/bf_novatabz_review.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/bf_novatabz_review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/bf_novatabz.mp4"], check=True)
print("OK out/bf_novatabz.mp4", END, "s")
