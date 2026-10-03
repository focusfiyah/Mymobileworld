"""Free cut: hands-only clips on the trimmed Grace B voiceover, classic hook caption on S1, real-packshot pop-up on "ninety-five percent".

  python3 cut.py   -> out/gtt_kn95.mp4 (720x1280, 24fps)

Windows come from shots.json (vo/words_trimmed.json). Pop-up = refs/crop_black_set.png (the listing's real box + mask).
Hook caption = Ralph's classic style (ugc-product-ad/scripts/classic_caption.py). SFX are CC0 (sfx/LICENSE.md).
Piece = ("clip", file, start[, dur]) or ("hold", png, cx, cy, z): a still frame with a slow push-in toward (cx, cy) by z.
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/ugc-product-ad/scripts"))
from classic_caption import classic_png

J = json.loads(Path("shots.json").read_text())
PIECES = {   # first ~1.5s of a clip is the reliable part (Seedance redraws late), so holds fill the rest
    "S1": [("clip", "clips/S1.mp4", 0.0, 0.5), ("hold", "inserts/s1_hold.png", 0.5, 0.55, 0.08)],   # box tilts and its small print warps after ~0.8s: front-on frame + push-in
    "S3": [("clip", "clips/S3.mp4", 0.0, 5.0), ("hold", "inserts/s3_hold.png", 0.5, 0.45, 0.05)],   # window 6.3s > clip 5s
    "S5c": [("clip", "clips/S5c.mp4", 1.0)],                                                       # the set-down, not the lift
    "S6": [("clip", "clips/S6.mp4", 1.5, 2.5), ("hold", "inserts/s6_hold.png", 0.5, 0.6, 0.03)],   # skips a 1.0s glitch (mask in the air)
    "S7": [("clip", "clips/S7.mp4", 3.0, 3.0), ("hold", "inserts/s7_hold.png", 0.5, 0.55, 0.05)],   # first 3s the box slides AWAY: use the 3-6s half, where it slides toward the lens with the hand on its side
}
HOOK = None   # on-screen hook text removed (Ralph 2026-10-03: "remove why fifty")
POPUP = ("inserts/popup.png", 11.55, 1.6)
SFX = [("click", 11.55, 0.25)]


Path("inserts").mkdir(exist_ok=True)
shots = J["shots"]
inputs, chains, labels = [], [], []
def add(args):
    inputs.extend(args); return sum(1 for x in inputs if x == "-i") - 1
for i, s in enumerate(shots):
    win = s["t"][1] - s["t"][0]
    parts = PIECES.get(s["id"], [("clip", f"clips/{s['id']}.mp4", 0.0)])
    plabels, left = [], win
    for k, p in enumerate(parts):
        last = k == len(parts) - 1
        if p[0] == "clip":
            d = left if last else min(p[3], left)
            j = add(["-i", p[1]])
            chains.append(f"[{j}:v]trim=start={p[2]},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1,"
                          f"trim=duration={d:.3f},setpts=PTS-STARTPTS,scale=720:1280,setsar=1,fps=24[p{i}_{k}]")
        else:
            d = left; nf = int(round(d * 24)) + 1
            j = add(["-i", p[1]])
            chains.append(f"[{j}:v]scale=1440:2560,zoompan=z='1+{p[4]}*on/{nf}':x='iw*{p[2]}-iw/zoom*{p[2]}':"
                          f"y='ih*{p[3]}-ih/zoom*{p[3]}':d={nf}:s=720x1280:fps=24,trim=duration={d:.3f},"
                          f"setpts=PTS-STARTPTS,setsar=1[p{i}_{k}]")
        left -= d; plabels.append(f"[p{i}_{k}]")
    chains.append(f"{''.join(plabels)}concat=n={len(plabels)}:v=1:a=0[v{i}]")
    labels.append(f"[v{i}]")
n = len(shots); total = shots[-1]["t"][1]
chains.append(f"{''.join(labels)}concat=n={n}:v=1:a=0[c0]")
png, st, d = POPUP
j = add(["-loop", "1", "-t", f"{d + 0.2}", "-i", png])
chains.append(f"[{j}:v]format=rgba,scale=w='440*min(1,0.9+t*0.8)':h=-1:eval=frame,"
              f"fade=t=out:st={d - 0.15:.2f}:d=0.15:alpha=1,setpts=PTS-STARTPTS+{st}/TB[bn]")
chains.append(f"[c0][bn]overlay=x=30:y=760:enable='between(t,{st},{st + d})':eof_action=pass[c1]")
chains.append("[c1]format=yuv420p[vout]")
a = add(["-i", "vo/voiceover_tight.mp3"])
mix = []
for k, (name, st, vol) in enumerate(SFX):
    j = add(["-i", f"sfx/{name}.ogg"])
    chains.append(f"[{j}:a]volume={vol},adelay={int(st * 1000)}:all=1[d{k}]"); mix.append(f"[d{k}]")
chains.append(f"[{a}:a]{''.join(mix)}amix=inputs={len(mix) + 1}:normalize=0:duration=first,apad,atrim=duration={total},"
              f"loudnorm=I=-16:TP=-1.5,aresample=44100[aout]")
Path("out").mkdir(exist_ok=True)
out = "out/gtt_kn95.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains),
                "-map", "[vout]", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "160k", "-t", str(total), "-movflags", "+faststart", out], check=True)
print(out)
