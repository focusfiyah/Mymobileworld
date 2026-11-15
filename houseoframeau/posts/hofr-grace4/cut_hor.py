"""HofR versions of 4 approved Grace cuts (Ralph 2026-11-15: "make a HofR versions of cleanwaste and others if they do not exist").
Source = Grace's approved cut from Drive (720x1280; the jobs' own clips are 720x1280 too and the cuts carry the label
fixes), so the HofR file is upscaled to 1080x1920 (lanczos). Own cut: shot order changed where the words allow, every
segment its own 1.13x crop with a slow pan, brighter cool-neutral grade, hook card frame 0 (HofR keeps hook text, no
captions, no product cards), AI finish last. Same approved voiceover (Grace's cut audio), loudness -15 LUFS.
  python3 cut_hor.py sofyre|throw|mute|night [--final]     -> out/<name>_review.mp4 (+ out/<name>.mp4 with --final)
SRC env HOFR_SRC = folder holding grace/<key>.mp4 (downloaded with Composio GOOGLEDRIVE_DOWNLOAD_FILE)."""
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "_bf_c_tools"))
from build import hook_card

SRC = Path(os.environ.get("HOFR_SRC", "/tmp/claude-0/-home-user-Mymobileworld/51ac50b9-7e30-5689-9468-bfbffe972254/scratchpad/grace"))
CF = 1.13
# seg = (grace in, grace out, pan from (x,y), pan to (x,y)) with x,y in 0..1 of the spare crop margin
V = {
 "sofyre": dict(name="hofr_sofyre_v1", hook="One thing I wouldn't|wait until winter for", hook_y=400,
   audio=[(0, 17.917)],
   segs=[(3.5, 6.5, (0, .2), (.4, .3)),          # hook line on the mouse running at the house (was the bag held up)
         (0.0, 3.5, (.5, .1), (.5, .4)),          # "Mouse prevention" + "temperatures drop": bag in front of the snowy window
         (6.5, 8.5, (.5, .8), (.5, .5)),         # mouse slips in the gap on "your house could be their next stop"
         (8.5, 12.5, (.2, 1), (.6, .6)), (12.5, 13.458, (.8, .5), (.6, .5)), (13.458, 14.375, (.3, .3), (.5, .5)),
         (14.375, 17.917, (.5, 0), (.5, .4))]),
 "throw": dict(name="hofr_throw_hands_v1", hook="Game night, but|everyone's on|their phone?", hook_y=400,
   audio=[(0, 29.375)],
   segs=[(0, 3.417, (0, .3), (.5, .5)), (3.417, 6.333, (1, .5), (.6, .2)), (6.333, 8.208, (.5, .9), (.5, .5)),
         (8.208, 11.583, (.2, .2), (.6, .6)), (11.583, 12.292, (.7, .4), (.7, .4)), (12.292, 14.417, (.3, .7), (.6, .3)),
         (14.417, 17.792, (.5, .2), (.5, .7)), (17.792, 19.333, (.8, .8), (.4, .4)), (19.333, 20.667, (.1, .5), (.4, .5)),
         (20.667, 22.042, (.9, .3), (.6, .6)), (22.042, 23.583, (.4, .9), (.4, .4)), (23.583, 29.375, (.5, 0), (.5, .6))]),
 "mute": dict(name="hofr_mute_v1", hook="When their snoring|sends you to the couch", hook_y=400,
   audio=[(0, 29.917)],
   segs=[(2.625, 5.208, (0, 0), (.4, .3)),         # opens on the sleeper (was the dilator held up)
         (0.0, 2.625, (1, .6), (.6, .4)),          # dilator, still inside line 1 ("...will not stop snoring")
         (5.208, 8.583, (.3, .2), (.6, .6)), (8.583, 13.333, (.5, .9), (.5, .4)), (13.333, 14.833, (.8, .3), (.5, .5)),
         (14.833, 16.292, (.2, .6), (.5, .4)), (16.292, 20.792, (.6, .1), (.4, .5)), (20.792, 21.167, (.5, .5), (.5, .5)),
         (21.167, 24.667, (.1, .4), (.5, .6)), (24.667, 29.917, (.5, 0), (.5, .5))]),
 "night": dict(name="hofr_night_glasses_v1", hook="Blinding headlights|at night?", hook_y=400,
   audio=[(0, 28.13), (32.43, 36.267)],           # drops "The clocks go back November first..." (past by Nov 23)
   segs=[(0, 3.367, (.5, 0), (.5, .4)), (3.367, 7.7, (.2, .5), (.6, .5)), (7.7, 11.267, (.8, .2), (.5, .6)),
         (11.267, 13.0, (.3, .8), (.5, .4)), (13.0, 14.967, (.6, .3), (.4, .6)), (14.967, 17.267, (.2, .2), (.6, .5)),
         (17.267, 19.367, (.5, .7), (.5, .3)), (19.367, 23.3, (.9, .4), (.5, .5)), (23.3, 24.867, (.5, .5), (.5, .5)),
         (24.867, 28.13, (.1, .3), (.5, .6)), (32.43, 36.267, (.5, 0), (.5, .5))]),
}
GRADE = {"night": "eq=gamma=1.08:contrast=1.03:saturation=1.0,colorbalance=bs=0.03:rs=-0.02",
         "_": "eq=brightness=0.05:contrast=1.04:saturation=1.0,colorbalance=bs=0.03:rs=-0.025:bm=0.015"}

def run(key, final):
    c = V[key]; src = SRC / f"{key}.mp4"; Path("out").mkdir(exist_ok=True)
    pic = sum(b - a for a, b, *_ in c["segs"]); aud = sum(b - a for a, b in c["audio"])
    assert abs(pic - aud) < 0.02, f"{key}: picture {pic:.3f} vs audio {aud:.3f}"
    W, H = round(1080 / CF / 2) * 2, round(1920 / CF / 2) * 2; mx, my = 1080 - W, 1920 - H
    ins, ch = [], []
    for i, (a, b, p0, p1) in enumerate(c["segs"]):
        d = b - a
        ins += ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(src)]
        x = f"{mx}*({p0[0]}+({p1[0]}-{p0[0]})*t/{d:.3f})"; y = f"{my}*({p0[1]}+({p1[1]}-{p0[1]})*t/{d:.3f})"
        ch.append(f"[{i}:v]setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,crop={W}:{H}:'{x}':'{y}',"
                  f"scale=1080:1920:flags=lanczos,setsar=1,trim=duration={d:.3f}[v{i}]")
    n = len(c["segs"])
    box = hook_card(c["hook"], f"out/{key}_hook.png", y0=c["hook_y"], size=70)
    hold = 2.6
    ains = []
    for j, (a, b) in enumerate(c["audio"]):
        ains += ["-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", str(src)]
    k0 = n; ka = [f"[{k0 + j}:a]asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b - a - 0.012:.3f}:d=0.012[a{j}]" for j, (a, b) in enumerate(c["audio"])]
    na = len(c["audio"]); hk = k0 + na
    g = GRADE.get(key, GRADE["_"])
    fc = ";".join(ch + ka) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,{g},format=yuv420p[g];" \
         f"[g][{hk}:v]overlay=0:0:enable='lt(t,{hold})'[v];" + "".join(f"[a{j}]" for j in range(na)) + \
         f"concat=n={na}:v=0:a=1,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=44100[a]"
    out = f"out/{c['name']}_review.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, *ains, "-loop", "1", "-t", f"{aud:.3f}", "-i", f"out/{key}_hook.png",
                    "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{aud:.3f}", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "17", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    plan = {"key": key, "name": c["name"], "len": round(aud, 3), "hook": c["hook"].replace("|", " "), "hook_box": box, "hook_hold": hold,
            "segs": [[a, b] for a, b, *_ in c["segs"]], "audio": c["audio"]}
    json.dump(plan, open(f"out/{key}_plan.json", "w"), indent=1)
    if final:   # AI finish = ai_finish.sh's filter (grain 6, sharpen 0.6, saturation 0.92) with the PLAYBOOK bitrate cap
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                        "-c:v", "libx264", "-crf", "18", "-maxrate", "20M", "-bufsize", "40M", "-preset", "medium", "-threads", "4",
                        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", f"out/{c['name']}.mp4"], check=True)
    print("BUILT", c["name"], round(aud, 2), "s hook_box", box)

if __name__ == "__main__":
    run(sys.argv[1], "--final" in sys.argv)
