"""Shared cut builder for the HofR Black Friday silent-C posts (Ralph 2026-11-12): Grace's real footage re-cut to Ralph's
Chatterbox VO, hook text card from frame 0 (HofR keeps hook text; no captions, no product cards), bright neutral grade,
every clip 1.0x (trim only, never stretch), no AI finish (Grace's footage is real).

A post's cut.py calls build(name, segs, hook, ...). Each seg = (line, offset, src, in_s, crop):
  the shot starts at VO line <line>'s start + <offset> (vo/words.json), plays src from in_s at 1.0x until the next seg starts,
  crop "w:h:x:y" in a 1080x1920 frame (then scaled back to 1080x1920) gives each post its own framing.
Writes out/<name>_review.mp4 (veryfast, for the first look) and out/<name>.mp4 (final, medium crf 18).
  REVIEW_ONLY=1 python3 cut.py   -> review render only
"""
import json, os, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
FONT = str(Path(__file__).resolve().parents[3] / ".claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout)


def hook_card(text, path, y0=380, size=60):
    """Whole hook in one white rounded card; lines split by '|'; stays inside x 60-940 / y 360-1340."""
    card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
    f = ImageFont.truetype(FONT, size); ls = text.split("|"); lh = int(size * 1.33)
    w = max(dr.textlength(l, font=f) for l in ls)
    x0, x1 = 500 - w / 2 - 40, 500 + w / 2 + 40
    assert x0 >= 60 and x1 <= 940, f"hook too wide: {w}"
    h = lh * len(ls) + 60
    dr.rounded_rectangle((x0, y0, x1, y0 + h), radius=36, fill=(255, 255, 255, 240))
    for k, l in enumerate(ls):
        dr.text((500, y0 + 30 + lh * k + lh / 2), l, fill=(20, 40, 70), font=f, anchor="mm")
    card.save(path)
    return (int(x0), y0, int(x1 - x0), h)


def build(name, segs, hook, hook_hold=None, tail=0.45, grade="eq=brightness=0.015:contrast=1.03:saturation=1.02", hook_y=380):
    words = json.loads(Path("vo/words.json").read_text())
    starts = [words[l]["start"] + off for l, off, *_ in segs]; starts[0] = 0.0
    end = round(words[-1]["end"] + tail, 3)
    assert starts == sorted(starts), "segs must run in time order"
    Path("out").mkdir(exist_ok=True)
    ins, ch = [], []
    for i, (l, off, src, ss, crop) in enumerate(segs):
        d = (starts[i + 1] if i + 1 < len(segs) else end) - starts[i]
        have = dur(src)
        assert ss + d <= have + 0.01, f"seg {i} {src} needs {ss + d:.2f} s, has {have:.2f} (never stretch)"
        pre = min(2.0, ss)  # coarse seek, then an exact trim (HEVC .mov input seek leaked a pre-roll frame at t=0)
        ins += ["-ss", f"{ss - pre:.3f}", "-t", f"{d + pre + 0.5:.3f}", "-i", str(src)]
        ch.append(f"[{i}:v]trim=start={pre:.3f}:duration={d:.3f},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,crop={crop},"
                  f"scale=1080:1920:flags=lanczos,format=yuv420p,setsar=1[v{i}]")
    n = len(segs)
    box = hook_card(hook, "out/hook.png", y0=hook_y)
    hold = hook_hold or max(2.2, starts[1] if n > 1 else 2.2)
    fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,{grade}[g];" \
         f"[g][{n + 1}:v]overlay=0:0:enable='lt(t,{hold:.3f})'[v];" \
         f"[{n}:a]loudnorm=I=-14.5:TP=-1.5:LRA=11,aresample=44100,apad,atrim=0:{end}[a]"
    common = [*ins, "-i", "vo/ralph.wav", "-i", "out/hook.png", "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{end}",
              "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", "-threads", "4"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *common, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    f"out/{name}_review.mp4"], check=True)
    if not os.environ.get("REVIEW_ONLY"):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *common, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-pix_fmt", "yuv420p", f"out/{name}.mp4"], check=True)
    plan = {"name": name, "end": end, "hook": hook.replace("|", " "), "hook_box": box, "hook_hold": round(hold, 3),
            "segs": [{"start": round(s, 3), "src": str(g[2]), "in": g[3], "crop": g[4]} for s, g in zip(starts, segs)]}
    Path(f"out/{name}_plan.json").write_text(json.dumps(plan, indent=1))
    print(f"BUILT out/{name}.mp4 {end:.2f}s hook_box={box} hold={hold:.2f}")
