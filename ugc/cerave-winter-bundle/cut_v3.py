"""CeraVe Winter Skin Bundle cut v3 (10.0 s, silent: music added later). python3 cut.py
Edit list (clip, in, out). S3 back (Ralph 2026-11-02: redo, Kling OK). Green cleanser first, the group of four at the end (Ralph)."""
import subprocess
EDL = [("S1k", 1.8, 3.6), ("S2", 0.4, 1.8), ("S3", 0.6, 2.2),        # pump into palm, push-in, lift to camera (Kling)
       ("S4", 2.0, 3.6),                                             # set down beside the group
       ("S1", 3.2, 3.7), ("S3", 3.5, 4.0), ("S2", 3.2, 3.8),        # fast run
       ("S5", 1.8, 3.8)]                                             # end: arc on all four
inp, flt = [], []
for i, (c, a, b) in enumerate(EDL):
    inp += ["-ss", f"{a}", "-t", f"{b-a:.3f}", "-i", ("clips/S1_kling.mp4" if c == "S1k" else f"clips/{c}.mp4")]
    flt.append(f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=30,trim=duration={b-a:.3f},setpts=PTS-STARTPTS[v{i}]")
flt.append("".join(f"[v{i}]" for i in range(len(EDL))) + f"concat=n={len(EDL)}:v=1:a=0[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(flt), "-map", "[out]", "-an",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-threads", "4", "out/cut_v3_raw.mp4"], check=True)
subprocess.run(["bash", "../../.claude/skills/ugc-product-ad/scripts/ai_finish.sh", "out/cut_v3_raw.mp4", "out/cut_v3.mp4"], check=True)
print("cut ok")
