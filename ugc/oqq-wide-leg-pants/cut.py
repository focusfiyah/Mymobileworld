"""Cut OQQ pants (free; copied from ugc/vans-sequin-v12/cut.py). Music-only, silent track, no text (Ralph 2026-10-25:
"Probably music", "No text"). python3 cut.py oqq -> out/oqq_review.mp4 then out/oqq_final.mp4 (AI finish, last step).
EDIT = clean windows only (QC 2026-10-25): S4 = the 2.1 s before the phone turns, Apple logo painted out free
(tools/logo_out.py -> clips/S4_fixed.mp4); S7 = the walk; S6 ends before her body turns; S2 dropped (feet point both ways).
Black look first (S4 phone in, S1 back as the 2nd shot (Ralph 2026-10-25: "do not start with the back side. Make it the 2nd shot"), S3 front, S5 feet), then brown (S6, S7, S8)."""
import subprocess, sys
from pathlib import Path
EDIT = {
 "oqq": [("S4_fixed", 0, 2.6), ("S1", 0, 2.6), ("S3", 0, 2.6), ("S5", 0, 2.4), ("S6", 0, 2.6), ("S7", 0.4, 3.2)],   # cut 2 (2026-10-26): S4 = Seedance patch-pocket take, logo painted out; S8 out until its pocket is right
}
GRADE = {"oqq": "colorbalance=rs=-0.01:bs=0.008,eq=brightness=0.02:contrast=1.03"}   # bright, neutral: black stays black, brown stays chocolate, oak floor not yellow


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
