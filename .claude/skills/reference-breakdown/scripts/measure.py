#!/usr/bin/env python3
"""measure.py: measure a reference video so the remake copies numbers, not impressions.

usage:
  python3 measure.py REF_DIR [--video FILE] [--force]

Reads REF_DIR/ref.mp4 (or --video), plus REF_DIR/transcript.json (word timings) and
REF_DIR/audio.wav when present. Writes REF_DIR/measure.txt:
  camera   image motion every 0.5 s (px/s at 1080 wide, phase correlation), each half second
           labelled HOLD / DRIFT / PAN / WHIP / TILT, then a summary (moves, hold lengths)
  palette  the dominant colours of the frame (quantised)
  captions where dark text boxes sit in the top half (y range at 1920 tall), sampled through the video
  pace     words per second, spoken numbers, longest silence
  sound    voice level vs gaps (the music bed), loud non-voice moments (likely sound effects)
An existing measure.txt is kept unless --force is given. breakdown.sh runs this for you.
Local only: needs ffmpeg, ffprobe and numpy.
"""
import argparse, json, os, re, subprocess, sys, wave
import numpy as np

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                             usage="measure.py REF_DIR [--video FILE] [--force]")
ap.add_argument("ref", help="the reference folder (breakdown.sh output)")
ap.add_argument("--video", help="video to measure (default REF_DIR/ref.mp4)")
ap.add_argument("--force", action="store_true", help="replace an existing measure.txt")
args = ap.parse_args()
ref = args.ref
V = args.video or os.path.join(ref, "ref.mp4")
OUT = os.path.join(ref, "measure.txt")
if not os.path.isfile(V):
    ap.error(f"no video at {V}")
if os.path.exists(OUT) and not args.force:
    sys.exit(f"{OUT} already exists: pass --force to measure again")
out = []
P = out.append


def probe(key):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", key,
                           "-of", "csv=p=0", V], capture_output=True, text=True).stdout.strip()


W0, H0 = [int(x) for x in probe("stream=width,height").split(",")[:2]]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", V],
                           capture_output=True, text=True).stdout)
P(f"# measure.txt  {W0}x{H0}  {dur:.2f} s\n")

# ---------- camera ----------
w, h, fps = 135, 240, 12
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-vf", f"fps={fps},scale={w}:{h},format=gray",
                      "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(float)
k = 1080 / w


def shift(a, b):
    a, b = a[int(h * .3):], b[int(h * .3):]          # skip the caption band
    A, B = np.fft.fft2(a - a.mean()), np.fft.fft2(b - b.mean())
    R = A * np.conj(B); R /= np.abs(R) + 1e-9
    r = np.abs(np.fft.ifft2(R)); y, x = np.unravel_index(r.argmax(), r.shape)
    if y > r.shape[0] // 2: y -= r.shape[0]
    if x > r.shape[1] // 2: x -= r.shape[1]
    return x, y


mv = np.array([(i / fps, *shift(fr[i], fr[i - 1]), np.abs(fr[i] - fr[i - 1]).mean()) for i in range(1, len(fr))])
P("## camera (px/s at 1080 wide; + = image moves right/down)")
labels = []
for t0 in np.arange(0, dur, 0.5):
    m = (mv[:, 0] >= t0) & (mv[:, 0] < t0 + .5)
    if not m.any(): continue
    dx, dy, d = mv[m, 1].sum() * k * 2, mv[m, 2].sum() * k * 2, mv[m, 3].mean()
    sp = max(abs(dx), abs(dy))
    lab = "WHIP" if sp > 900 else "PAN" if sp > 150 else "DRIFT" if d > 6 else "HOLD"
    if lab in ("PAN", "WHIP") and abs(dy) > abs(dx): lab = "TILT" if lab == "PAN" else "WHIP-TILT"
    labels.append((t0, lab))
    P(f"{t0:6.1f}  dx {dx:7.0f}  dy {dy:7.0f}  change {d:5.1f}  {lab}")
moves, holds, cur, start = 0, [], None, 0
for t0, lab in labels:
    still = lab in ("HOLD", "DRIFT")
    if still and cur != "still": cur, start = "still", t0
    if not still:
        if cur == "still": holds.append(t0 - start)
        if cur != "move": moves += 1
        cur = "move"
P(f"summary: {moves} camera moves in {dur:.0f} s; holds median {np.median(holds) if holds else 0:.1f} s, "
  f"max {max(holds) if holds else 0:.1f} s\n")

# ---------- palette and caption boxes ----------
P("## palette (share of frame) and caption boxes")
samples = np.linspace(dur * .05, dur * .95, 12)
cols = []
cap_rows = []
for t in samples:
    img = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", V, "-frames:v", "1", "-vf", "scale=270:480",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = np.frombuffer(img, np.uint8).reshape(480, 270, 3).astype(int)
    cols.append((a // 24 * 24 + 12).reshape(-1, 3))
    dark = a.sum(2) < 110
    rows = [y for y in np.where(dark.sum(1) > 270 * .18)[0] if y < 240]   # top half only
    if rows:                                   # first band plus any band within 40 px under it
        y0 = y1 = rows[0]
        for y in rows[1:]:
            if y - y1 <= 10: y1 = y
            else: break
        cap_rows.append((t, int(y0 * 4), int(y1 * 4)))
c = np.concatenate(cols)
u, n = np.unique(c, axis=0, return_counts=True)
for i in np.argsort(n)[::-1][:8]:
    P(f"  #{u[i][0]:02x}{u[i][1]:02x}{u[i][2]:02x}  {n[i] / n.sum() * 100:4.1f}%")
for t, y0, y1 in cap_rows:
    P(f"  top dark box at {t:5.1f}s: y {y0} to {y1} (of 1920)")
P("")

# ---------- pace and sound ----------
tj = os.path.join(ref, "transcript.json")
words = []
if os.path.exists(tj):
    with open(tj) as fh:
        words = [w_ for s in json.load(fh)["segments"] for w_ in s.get("words", [])]
if words:
    text = " ".join(w_["word"] for w_ in words)
    nums = re.findall(r"\$?\d[\d,.]*\s*(?:%|million|billion|thousand|k)?|\b(?:one|two|three|ten|hundred|thousand|million|billion)\b", text, re.I)
    gaps = [(words[i]["end"], words[i + 1]["start"]) for i in range(len(words) - 1)]
    lg = max(gaps, key=lambda g: g[1] - g[0]) if gaps else (0, 0)
    P(f"## pace\n  {len(words)} words, {len(words) / dur:.2f} words/s; spoken numbers ~{len(nums)} (one every {dur / max(1, len(nums)):.1f} s); "
      f"longest silence {lg[1] - lg[0]:.2f} s at {lg[0]:.1f}\n")
wav = os.path.join(ref, "audio.wav")
if os.path.exists(wav):
    wf = wave.open(wav); sr = wf.getframerate()
    x = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(float) / 32768

    def db(s): return 20 * np.log10(np.sqrt(np.mean(s ** 2)) + 1e-9)
    P("## sound")
    P(f"  overall {db(x):.1f} dB RMS, peak {20 * np.log10(np.abs(x).max() + 1e-9):.1f} dB")
    if words:
        vo = np.concatenate([x[int(w_["start"] * sr):int(w_["end"] * sr)] for w_ in words])
        gl = [db(x[int((a + .04) * sr):int((b - .04) * sr)]) for a, b in gaps if b - a > .2]
        P(f"  voice {db(vo):.1f} dB; gaps median {np.median(gl) if gl else float('nan'):.1f} dB "
          f"(music bed ~{db(vo) - (np.median(gl) if gl else 0):.0f} dB under the voice)")
    win = int(.05 * sr)
    env = np.array([db(x[i:i + win]) for i in range(0, len(x) - win, win)])
    inw = np.zeros(len(env), bool)
    for w_ in words: inw[int(w_["start"] / .05):int(w_["end"] / .05) + 1] = True
    hits = [i * .05 for i in np.where((env > np.percentile(env, 60)) & ~inw)[0]]
    merged = [t for j, t in enumerate(hits) if j == 0 or t - hits[j - 1] > .2]
    P(f"  loud non-voice moments (likely SFX): {', '.join(f'{t:.2f}' for t in merged[:40])}")
with open(OUT, "w") as fh:
    fh.write("\n".join(out) + "\n")
print("\n".join(out[-12:]))
