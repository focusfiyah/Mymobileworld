"""Cut Vans V12 (free; copied from ugc/vans-sequin-authentic/cut.py). Music-only, silent track, no text (Ralph 2026-10-24:
"silent, no text"). python3 cut.py V12 -> out/V12_review.mp4 then out/V12_final.mp4 (AI finish, last step).
EDIT = clean windows only (QC 2026-10-24): S1 and S3 tip the held shoe onto its side mid-take, so only the insole-up /
side-on parts are used (Ralph: "Use the clean parts")."""
import subprocess, sys
from pathlib import Path
EDIT = {
 "V12": [("S1", 0, 1.3), ("S1", 2.7, 4.0), ("S2", 0, 4.0), ("S3", 2.4, 4.0), ("S4", 1.5, 3.5), ("S5", 0.8, 2.6), ("S6", 0, 3.5)],
}
GRADE = {"V12": "colorbalance=rs=-0.015:bs=0.01,eq=brightness=0.025:contrast=1.03"}   # bright, neutral; brick stays brick red, no warm cast


def cut(v):
    Path("out").mkdir(exist_ok=True); ins, parts = [], []
    for i, (cid, a, b, *opt) in enumerate(EDIT[v]):
        ins += ["-ss", str(a), "-t", str(b - a), "-i", f"clips/{cid}.mp4"]
        push = (opt[0] if opt else {}).get("push")   # free smooth push-in on a near-still real clip (PLAYBOOK FUSOU V3: locked-off clips read as photos)
        zoom = (f",scale=w='trunc(1080*(1+{push - 1}*t/{b - a})/2)*2':h=-2:eval=frame:flags=lanczos,crop=1080:1920" if push else "")
        dark = (opt[0] if opt else {}).get("dark")   # V11: "flash off" for the first N s (dim, cool, grainy like a phone at night), then the flash
        flash = (f",eq=brightness=-0.30:contrast=0.75:saturation=0.55:enable='lt(t,{dark})',colorbalance=bs=0.05:bm=0.03:enable='lt(t,{dark})',"
                 f"noise=alls=10:allf=t:enable='lt(t,{dark})',eq=brightness=0.06:enable='between(t,{dark},{dark + 0.07})'" if dark else "")
        parts.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,fps=30,setsar=1{zoom},{GRADE[v]}{flash}[v{i}]")
    n = len(EDIT[v]); fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    dur = sum(e[2] - e[1] for e in EDIT[v])
    rev = f"out/{v}_review.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo",
                    "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", rev], check=True)
    # AI finish, LAST step (Ralph 2026-10-07): the same values as ai_finish.sh (grain 6, unsharp 0.6, saturation 0.92), with the
    # bitrate capped (BodyJ lesson: uncapped grain = 200 MB) so each final stays under the review page's 16 MB per file.
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", rev, "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "7M", "-bufsize", "14M", "-threads", "4",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", f"out/{v}_final.mp4"], check=True)
    print(v, f"{dur:.1f}s", "-> out/" + v + "_final.mp4")


if __name__ == "__main__":
    for v in sys.argv[1:]: cut(v)
