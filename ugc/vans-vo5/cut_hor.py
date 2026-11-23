"""House of Rameau version of the approved Vans V13 (Grace's VO; Ralph 2026-11-15: "make a HofR versions of cleanwaste and others").
The V13 source clips were never stored (media-in-drive/ugc__vans-vo5.json holds stills + VO only), so this cuts from Grace's approved
V13 mp4 itself (Drive 1zmlpVDH5ORiTlx8RWYnXefypv_CtQPr0), as the task allows. Its own cut so TikTok does not read it as a copy:
shots C and E swapped (C = cafe walk pushing in to the sequins, now on "the sequins add just the right amount of shine"; E = outdoor front
view, now on "these are the Premium Authentic"), the C/D and D/E cut points moved 2 frames so both fit at 1.0x, the two closing tails
swapped, a ~1.1x crop on every shot, a brighter cool-neutral grade, hook card from frame 0 to 3.0 s (top, over the window, clear of the
shoe), no captions. Every piece plays at 1.0x (frame counts asserted). The source already carries the AI finish (grain/sharpen), so it is
not applied a second time (double grain).
  python3 cut_hor.py GRACE_V13.mp4   -> out/vans_hor.mp4"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SRC = sys.argv[1]
NAME = "vans_hor"
HOOK = ["Who told Vans to come out", "with these sparkly low tops?"]
HOOK_Y, HOOK_HOLD = 380, 3.0
FPS = 30
nb = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", SRC], capture_output=True, text=True).stdout)
# Grace's V13 cut frames (hard cuts measured by frame difference, 2026-11-15): A B C D E F G H I J K tailA tailH
CUTS = [0, 84, 155, 264, 320, 427, 455, 483, 593, 662, 759, 800, 812, nb]
seg = {k: (CUTS[i], CUTS[i + 1]) for i, k in enumerate(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "tA", "tH"])}
# (segment, source frame in, frame count, crop "w:h:x:y" of 1080x1920); slots run back to back
EDIT = [("A", 0, 84, "980:1742:50:0"), ("B", 0, 71, "980:1742:100:90"),
        ("E", 0, 107, "980:1742:0:120"),          # slot C (153..262), E has exactly 107 frames
        ("D", 0, 56, "980:1742:50:60"),           # slot D (262..318)
        ("C", 0, 109, "980:1742:100:178"),        # slot E (318..427): all of C's 109 frames
        ("F", 0, 28, "980:1742:50:100"), ("G", 0, 28, "980:1742:100:120"), ("H", 0, 110, "980:1742:50:178"),
        ("I", 0, 69, "980:1742:100:120"), ("J", 0, 97, "980:1742:50:60"), ("K", 0, 41, "980:1742:50:178"),
        ("tH", 0, None, "980:1742:100:150"), ("tA", 0, 12, "980:1742:50:150")]
# slot C ends 2 frames earlier than Grace's cut (frame 262 = 8.733 s), slot D ends at 318 (10.6 s), so E and D fit at 1.0x
rows, pos = [], 0
for k, a, n, crop in EDIT:
    s0, s1 = seg[k]
    if n is None: n = (nb - CUTS[11]) - 12        # the closing tail fills to the end: tH first (Grace: tA then tH)
    assert s0 + a + n <= s1, f"{k}: needs frames {s0 + a}..{s0 + a + n}, segment is {s0}..{s1} (never stretch)"
    rows.append((k, s0 + a, n, crop)); pos += n
assert pos == nb, f"edit is {pos} frames, Grace's cut is {nb}"
END = nb / FPS
Path("out").mkdir(exist_ok=True)
at = 0; ej = []
for k, s, n, crop in rows: ej.append({"id": k, "in": round(s / FPS, 3), "len": round(n / FPS, 3), "at": round(at / FPS, 3)}); at += n
json.dump(ej, open("out/hor_edit.json", "w"), indent=1)
for e in ej: print(e)

card = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); dr = ImageDraw.Draw(card)
fo = ImageFont.truetype("../../.claude/skills/ugc-product-ad/scripts/OpenSans-SemiBold.ttf", 56)
h = 100 + 80 * (len(HOOK) - 1) + 40
dr.rounded_rectangle((80, HOOK_Y, 920, HOOK_Y + h), radius=36, fill=(255, 255, 255, 240))
for k, line in enumerate(HOOK):
    dr.text((500, HOOK_Y + 70 + k * 80), line, fill=(20, 40, 70), font=fo, anchor="mm")
    bb = dr.textbbox((500, HOOK_Y + 70 + k * 80), line, font=fo, anchor="mm"); assert bb[0] >= 100 and bb[2] <= 900, (line, bb)
assert HOOK_Y >= 360 and HOOK_Y + h <= 1340
card.save("out/hor_hook.png"); json.dump({"box": f"80,{HOOK_Y},840,{h}", "hold": HOOK_HOLD}, open("out/hor_hookbox.json", "w"))

ch = [f"[0:v]trim=start_frame={s}:end_frame={s + n},setpts=PTS-STARTPTS,scale=1080:1920,crop={crop},scale=1080:1920:flags=lanczos,format=yuv420p,setsar=1[v{i}]"
      for i, (k, s, n, crop) in enumerate(rows)]
m = len(rows)
fc = ";".join(ch) + ";" + "".join(f"[v{i}]" for i in range(m)) + \
     f"concat=n={m}:v=1:a=0,eq=brightness=0.035:contrast=1.03:saturation=1.0,colorbalance=bs=0.05:rs=-0.04:bm=0.03:rm=-0.02[g];[g][1:v]overlay=0:0:enable='lt(t,{HOOK_HOLD})'[v];" \
     f"[0:a]aresample=44100,loudnorm=I=-14:TP=-1.5:LRA=11,apad,atrim=0:{END:.3f}[a]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", SRC, "-i", "out/hor_hook.png", "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-t", f"{END:.3f}", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-threads", "4",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", f"out/{NAME}.mp4"], check=True)
print(f"out/{NAME}.mp4", round(END, 2), "s")
