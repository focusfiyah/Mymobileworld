"""Cut the Vans videos (free). Music-only: no voiceover, no text (Ralph: no text unless asked); a silent audio track so
players and TikTok treat it as video; Grace adds a trending sound when she posts.
  python3 cut.py V1 [V2 ...]     -> out/V1_review.mp4 (veryfast) then out/V1_final.mp4 (ai_finish.sh, last step)
EDIT: per video, the clips in order with (in, out) seconds; GRADE: a different bright, neutral look per video (rule 6)."""
import subprocess, sys
from pathlib import Path
EDIT = {  # clean windows only (QC 2026-10-21: no grip switch, no extra hands, no product change inside a window)
 "V1": [("V1S1_r1", 0, 3.2), ("V1S2", 0, 4.0)],   # r8: back to round 5 (Ralph: the Kling holds read as still images)
 "V2": [("V2S1", 0, 3.6), ("V2S3", 0, 4.6)],   # r9: Ralph (sparkle, still): new Kling walk off the rug, no held shoe
 "V3": [("V3S3", 0, 4.6), ("V3S4", 0, 4.0)],   # r9: Ralph (still image): new Kling walk + crossed-leg foot bounce, no held shoe
 "V4": [("V4S3", 0, 3.1), ("V4S1", 0, 4.0)],   # r9: Ralph (jumps sides, 3 shoes): new Kling heel-rock, cut before the pivot at 3.0 s
 "V5": [("V5S1", 2.3, 4.0), ("V5S3", 0.8, 4.2), ("V5S4", 0, 3.6)],   # Ralph r4: the sole cut read as a flip; r10 (Ralph: "jumps from left to right"): start after the toe flip at 2.2 s
 "V6": [("V6S1", 0, 4.6), ("V6S2_r0", 0, 4.0), ("V6S3", 0, 4.6)],   # r8: back to round 5
 "V7": [("V7S2", 1.2, 4.0), ("V7S3", 0, 4.8)],   # Ralph r4: V7S1 walked in place
 "V8": [("V8S1", 0, 5.0), ("V8S2", 0, 4.0), ("V8S3", 0, 4.6)],
 "V9": [("V9S1", 0, 1.4), ("V9S1", 2.6, 3.4), ("V9S2", 0.9, 4.8), ("V9S3", 0, 4.0)],
 "V10": [("V10S1", 0, 4.6), ("V10S2", 0, 4.0), ("V10S3", 0, 2.5)],
}
GRADE = {  # all bright and neutral; small differences so no two videos share a look
 "V1": "eq=brightness=0.02:contrast=1.03", "V2": "eq=brightness=0.035:saturation=0.97",
 "V3": "colorbalance=bs=0.03:bm=0.02,eq=brightness=0.03", "V4": "eq=contrast=1.06:saturation=1.04:brightness=0.02",
 "V5": "eq=contrast=1.04:brightness=0.015", "V6": "eq=brightness=0.03:saturation=1.02",
 "V7": "colorbalance=bs=0.02,eq=contrast=1.05:brightness=0.02", "V8": "eq=brightness=0.04:contrast=1.02",
 "V9": "eq=brightness=0.035:saturation=0.98", "V10": "colorbalance=bs=0.015,eq=brightness=0.03:contrast=1.03",
}


def cut(v):
    Path("out").mkdir(exist_ok=True); ins, parts = [], []
    for i, (cid, a, b, *opt) in enumerate(EDIT[v]):
        ins += ["-ss", str(a), "-t", str(b - a), "-i", f"clips/{cid}.mp4"]
        push = (opt[0] if opt else {}).get("push")   # free smooth push-in on a near-still real clip (PLAYBOOK FUSOU V3: locked-off clips read as photos)
        zoom = (f",scale=w='trunc(1080*(1+{push - 1}*t/{b - a})/2)*2':h=-2:eval=frame:flags=lanczos,crop=1080:1920" if push else "")
        parts.append(f"[{i}:v]scale=1080:1920:flags=lanczos,fps=30,setsar=1{zoom},{GRADE[v]},setpts=PTS-STARTPTS[v{i}]")
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
