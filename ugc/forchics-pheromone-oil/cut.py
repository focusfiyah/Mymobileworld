"""FORCHICS V1: edit of Grace's original (orig/original.mov). Muted: Grace adds her own music.
Crop 40 px each side removes the phone's blue UI bubble (x 1046-1080, y 880-955), scaled back to 1080x1920."""
import subprocess, sys
SRC = "orig/original.mov"
# (start, end, what it shows)
SEGS = [
    (59.0, 60.5, "glowing wrist, bottle + cap on vanity"),
    (1.0, 3.0, "box front"),
    (6.0, 7.0, "opening the box"),
    (8.5, 10.5, "pulling the bottle out"),
    (16.5, 18.5, "FORCHICS label close-up"),
    (28.0, 29.5, "cap off, pump revealed"),
    (32.0, 34.0, "pump onto wrist"),
    (39.0, 41.0, "rubbing it in"),
    (50.0, 51.5, "glow close-up"),
    (72.0, 74.0, "hero hold"),
]
def render(out, preset="slow", crf="17"):
    vf = "crop=1000:1778:40:71,scale=1080:1920:flags=lanczos,fps=30,setsar=1"
    parts, inputs = [], []
    for i, (a, b, _) in enumerate(SEGS):
        inputs += ["-ss", str(a), "-t", f"{b-a:.3f}", "-i", SRC]
        parts.append(f"[{i}:v]{vf},setpts=PTS-STARTPTS[v{i}]")
    n = len(SEGS)
    fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[v]"
    dur = sum(b - a for a, b, _ in SEGS)
    cmd = ["ffmpeg", "-v", "error", "-y", *inputs, "-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
           "-filter_complex", fc, "-map", "[v]", "-map", f"{n}:a", "-c:v", "libx264", "-preset", preset, "-crf", crf,
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-threads", "4", "-movflags", "+faststart", "-shortest", out]
    subprocess.run(cmd, check=True); print(out, round(dur, 2), "s")
if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "out/FORCHICS_V1.mp4")
