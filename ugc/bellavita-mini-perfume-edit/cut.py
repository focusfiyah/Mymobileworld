"""Bellavita Mini Perfume Gift Set edit from Grace's original (2026-11-17).
python3 cut.py [review|final]  -> out/bellavita_v1.mp4 (silent: Grace adds music)."""
import subprocess, sys, os
SRC = "orig/orig.mov"
# (start, end, crop) ; crop = (x, y, w) keeps 9:16, scaled back to 1080x1920 (<=1.14x)
HELD = (20, 115, 950)   # hides the blue light on the right edge of the vanity shots
SHOTS = [
    (0.7, 2.6, None),     # box lid opens: hook / reveal
    (20.0, 21.4, None),   # four bottles in the box, close
    (11.2, 11.65, None),   # "A note from our perfumer" card
    (38.5, 40.5, HELD),   # Skai Aquatic (blue)
    (44.6, 46.6, HELD),   # Fresh Unisex (teal)
    (51.3, 52.8, HELD),   # Honey Oud (orange)
    (61.2, 62.9, HELD),   # White Oud
    (69.8, 72.0, None),   # close slide along all four labels
    (73.6, 75.6, None),   # all four standing in the box, end
]
def main(mode="review"):
    os.makedirs("out", exist_ok=True)
    preset = "veryfast" if mode == "review" else "slow"
    parts, n = [], 0
    for i, (a, b, c) in enumerate(SHOTS):
        vf = "fps=30"
        if c:
            x, y, w = c; h = round(w * 16 / 9)
            vf += f",crop={w}:{h}:{x}:{y}"
        vf += ",scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p"
        parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,{vf}[v{i}]")
    fc = ";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(SHOTS))) + f"concat=n={len(SHOTS)}:v=1:a=0[out]"
    out = "out/bellavita_v1.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fc, "-map", "[out]",
                    "-c:v", "libx264", "-preset", preset, "-crf", "17", "-threads", "4",
                    "-movflags", "+faststart", out], check=True)
    print(out, sum(b - a for a, b, _ in SHOTS))
if __name__ == "__main__":
    main(*(sys.argv[1:] or ["review"]))
