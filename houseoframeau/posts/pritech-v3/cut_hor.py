"""PRITECH V3, House of Rameau own cut (2026-10-28). Free: the approved V3 clips + V3 voiceover (ugc/pritech-15s), re-cut in
Grace's edit style (grace/winners/STYLE_pritech.md): long shots split into two framings (~1.5-2 s shots), the close is a fast
run of product-in-hand moments ending on the product, its own grade. Never the same file Grace posts (houseoframeau/README.md).
  python3 cut_hor.py  -> out/review.mp4 (veryfast) + out/pritech_v3_hor.mp4 (AI finish)"""
import json, subprocess
HOLD = 0.6
W = dict(json.load(open("vo/V3/windows.json")))
# (clip, start s in clip, length s or a window id, zoom, centre x, centre y)
def win(k): a, b = W[k]; return b - a
EDIT = [
    ("V3S1", 0.0, 1.9, 1.15, .5, .42),      # "This looked like a normal face brush": tighter than Grace's V3
    ("V3S1", 1.9, win("V3S1") - 1.9, 1.3, .45, .78),   # "until I noticed the silver end": punch-in on the metal end
    ("V3S2", 0.0, win("V3S2"), 1.12, .5, .45),        # "It warms up to a hundred and four degrees"
    ("V3S3", 0.0, 1.5, 1.0, .5, .5, "hflip"),  # "Who has time or money": room mirrored (no product, no print in this shot)
    ("V3S3", 1.5, win("V3S3") - 1.5, 1.35, .45, .72, "hflip"), # "for a facial every week?": punch-in on the towels + tub
    ("V3S4", 0.0, win("V3S4"), 1.1, .5, .5),          # "Wash with the soft bristles,"
    ("V3S5", 0.0, win("V3S5"), 1.12, .45, .5),        # "then rub the warm end in little circles."
    ("V3S6", 0.0, win("V3S6") + 0.32, 1.15, .45, .55),# "I hate how much I look forward to it."
]
close = win("V3S7") - 0.32 + HOLD                    # "Cold weather's coming, so get one for your mom too. It's in the orange cart."
RUN = [("V3S2", 2.6, .55, 1.25, .5, .4), ("V3S4", 2.5, .55, 1.15, .5, .5), ("V3S1", 0.8, .5, 1.25, .5, .4), ("V3S5", 1.5, .5, 1.25, .45, .5)]   # unused tails of S2/S4 first
EDIT += RUN + [("V3S7", 0.0, close - sum(r[2] for r in RUN), 1.0, .5, .5)]
GRADE = "eq=brightness=0.045:contrast=1.05:saturation=1.03"   # bright punchy (Grace's V3 used the plain clip look)
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
inputs, chains, cum = [], [], 0.0
for i, (c, st, d, z, cx, cy, *fx) in enumerate(EDIT):
    f = f"clips/{c}.mp4"; assert st + d <= dur(f) + 1e-3, (c, st, d)
    nf = round((cum + d) * 30) - round(cum * 30); cum += d
    w, h = round(1080 / z / 2) * 2, round(1920 / z / 2) * 2
    x, y = min(max(0, round(1080 * cx - w / 2)), 1080 - w), min(max(0, round(1920 * cy - h / 2)), 1920 - h)
    inputs += ["-ss", f"{st:.3f}", "-i", f]
    chains.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,trim=end_frame={nf},setpts=PTS-STARTPTS,scale=1080:1920,crop={w}:{h}:{x}:{y},scale=1080:1920:flags=lanczos,{fx[0] + ',' if fx else ''}{GRADE},format=yuv420p[v{i}]")
n = len(EDIT); end = cum
fc = ";".join(chains) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-i", "vo/V3/voiceover_paced.mp3", "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a",
                "-af", f"apad,atrim=0:{end:.3f},loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-t", f"{end:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-threads", "4",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "out/review.mp4"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/review.mp4", "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart", "out/pritech_v3_hor.mp4"], check=True)
json.dump([{"clip": c, "start": st, "len": round(d, 3), "zoom": z} for c, st, d, z, *_ in EDIT], open("out/edit.json", "w"), indent=1)
print("out/pritech_v3_hor.mp4", round(end, 2), "s,", n, "shots")
