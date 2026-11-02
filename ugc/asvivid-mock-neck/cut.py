"""Music-only fast edit of Grace's own try-on (Asvivid reversible mock neck), in her edit style
(grace/winners/STYLE_pritech.md): product moving in her hands from frame 0, ~1.5 s middle shots, fast end run,
ends on the product. Cuts sit on the song's beat grid (first beat 0.25 s, period 0.738 s). Her song runs
continuous from 0.0 under the whole cut. No text, no overlays.
  python3 -I cut.py            render out/edit_v1.mp4 (veryfast review render)
  python3 -I cut.py --check    CUTS_OK / AUDIO_OK
"""
import json, subprocess, sys
from pathlib import Path

J = Path(__file__).parent
RAW = J / "raw/raw.mov"
OUT = J / "out/edit_v1.mp4"
B0, P = 0.25, 0.738

# (source start s, length in beats, what it shows)
SHOTS = [
    (14.30, 2 + B0 / P, "close: her hands stretch the cuff"),   # first shot also covers the 0.25 s lead-in
    (1.40, 2, "steps back: full front, mock neck"),
    (5.30, 2, "turns to the side"),
    (8.00, 2, "back view, oversized fit"),
    (22.10, 2, "lifts the hem: layered hem at the waist"),
    (25.30, 2, "close: soft fabric and hem"),
    (39.00, 2, "push-in, hands on the front"),
    (31.30, 2, "arms out, drape"),
    (57.00, 2, "close: ribbed cuff"),
    (50.10, 1, "fast: arms swing"),
    (34.00, 0.5, "fast: side turn"),
    (64.00, 0.5, "fast: full length with shoes"),
    (93.00, 0.5, "fast: arms up"),
    (46.60, 0.5, "fast: walks in"),
    (56.00, 1.5, "end: front close, the sweatshirt"),
]


def plan():
    t, rows = 0.0, []
    for src, beats, what in SHOTS:
        d = beats * P
        rows.append({"out": round(t, 3), "src": src, "dur": round(d, 3), "what": what})
        t += d
    return rows, t


def check():
    rows, total = plan()
    ok = True
    for r in rows[1:]:
        k = (r["out"] - B0) / P
        if abs(k * 2 - round(k * 2)) > 0.01:  # on a beat or half-beat
            print("off beat", r); ok = False
    mids = [r["dur"] for r in rows[1:9]]
    ends = [r["dur"] for r in rows[10:14]]
    if not all(1.2 <= d <= 3 for d in mids) or not all(0.2 <= d <= 0.8 for d in ends):
        print("pacing off", mids, ends); ok = False
    print("CUTS_OK" if ok else "CUTS_BAD", f"{len(rows)} shots, {total:.2f} s")
    if OUT.exists():
        # audio = one continuous slice of the raw from 0: compare cut audio vs raw audio sample by sample
        a = subprocess.run(["ffmpeg", "-v", "error", "-i", str(OUT), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                           capture_output=True).stdout
        b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(RAW), "-t", f"{total:.3f}", "-ac", "1", "-ar", "8000",
                            "-f", "s16le", "-"], capture_output=True).stdout
        import numpy as np
        x = np.frombuffer(a, np.int16).astype(float); y = np.frombuffer(b, np.int16).astype(float)
        n = min(len(x), len(y)); c = np.corrcoef(x[:n], y[:n])[0, 1]
        print("AUDIO_OK" if c > 0.98 else "AUDIO_BAD", f"corr {c:.4f}")


def render():
    rows, total = plan()
    OUT.parent.mkdir(exist_ok=True)
    parts, labels = [], []
    for i, r in enumerate(rows):
        parts.append(f"[0:v]trim=start={r['src']}:duration={r['dur']},setpts=PTS-STARTPTS,fps=30,"
                     f"scale=1080:1920,setsar=1[v{i}]")
        labels.append(f"[v{i}]")
    fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(rows)}:v=1:a=0[v];" \
         f"[0:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={total-0.3:.3f}:d=0.3[a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(RAW), "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-threads", "4",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(OUT)], check=True)
    json.dump(rows, open(J / "out/shots.json", "w"), indent=1)
    print("rendered", OUT, f"{total:.2f} s")


if __name__ == "__main__":
    check() if "--check" in sys.argv else render()
