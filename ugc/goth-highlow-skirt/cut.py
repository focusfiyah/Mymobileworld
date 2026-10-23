"""Cut the goth skirt video (free). Music-only (Ralph 2026-10-22): no voiceover, no text; a silent track so Grace adds the
inspo's sound or a trending one when she posts. Tug-cut (Ralph 2026-10-22): each look is its own moving clip and the length
changes on a cut as her hand tugs the tie (no video model could shorten the skirt and keep it real).
  python3 cut.py   -> out/goth_review.mp4 (veryfast) then out/goth_final.mp4 (AI finish, last step)
EDIT: clips in order with (in, out) seconds = clean windows from QC (qc/*_sheet.jpg)."""
import subprocess
from pathlib import Path
EDIT = [
 ("VB_veo_1", 0.0, 1.3),   # look 2: the back, ruffle tiers sway (she turns to the mirror after 1.3 s with a wrong tiered front)
 ("V1_veo_1", 0.0, 2.7),   # look 1: top of the knee, both hands working the ties (tug)
 # ("R3_seed_1_skin", 0.0, 2.0),  # Ralph 2026-10-22: at 5 s the back turns short = wrong skirt; dropped  # look 3: mid-thigh, she pulls a tie out to the side (skirt swaps shape after 2.2 s)
 ("VO_veo_1_skin", 0.0, 2.5),   # look 4: one leg out, hand holding the pulled tie (slit closes after 2.7 s)
 ("VS_seed_1_skin2", 0.5, 3.7),    # look 5: shortest, both ties held at the hips, weight shift
]
CROP = 0.13   # top crop: her phone hand shows at the top of R3/VO; same crop on every clip so framing matches
# *_skin clips: legs + hands matched to the knee clip's skin (tools/skin_match.py, free; the stills came out lighter)
GRADE = "eq=brightness=0.02:contrast=1.03"   # bright and neutral


def main():
    Path("out").mkdir(exist_ok=True); ins, parts = [], []
    for i, (cid, a, b) in enumerate(EDIT):
        ins += ["-ss", str(a), "-t", str(round(b - a, 3)), "-i", f"clips/{cid}.mp4"]
        parts.append(f"[{i}:v]setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,crop=trunc(iw*{1 - CROP}/2)*2:trunc(ih*{1 - CROP}/2)*2:"
                     f"(iw-ow)/2:ih*{CROP},scale=1080:1920:flags=lanczos,fps=30,setsar=1,{GRADE}[v{i}]")
    n = len(EDIT); fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    dur = round(sum(b - a for _, a, b in EDIT), 3)
    rev = "out/goth_review.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo",
                    "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-threads", "4", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", rev], check=True)
    # AI finish, LAST step (Ralph 2026-10-07): ai_finish.sh values (grain 6, unsharp 0.6, saturation 0.92), bitrate capped
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", rev, "-vf", "eq=saturation=0.92,unsharp=5:5:0.6:5:5:0,noise=alls=6:allf=t",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-maxrate", "7M", "-bufsize", "14M", "-threads", "4",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "out/goth_final.mp4"], check=True)
    print(f"{dur:.1f}s -> out/goth_final.mp4")


if __name__ == "__main__":
    main()
