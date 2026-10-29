"""QC every cut (the verify_fix checks for this job). python3 tools/cutqc.py V13 ...  -> prints CUTQC_OK <V> or CUTQC FAIL lines.
flash: no frame-to-frame brightness jump > 18 (0-255) except within 2 frames of a planned cut; black: no frame darker than 30;
sync: the cut's audio = Grace's VO (correlation peak at lag 0 +-20 ms, r > 0.9); levels: peak <= -0.5 dBFS, mean -30..-14 dB;
format: 1080x1920, length = VO +-0.2 s."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
J = Path(__file__).resolve().parent.parent


def frames_luma(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-vf", "scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(-1, 96 * 54).astype(float)
    return a.mean(1), float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.strip().split("/")[0])


def audio(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(float) / 32768


def check(v):
    f = J / f"out/{v}.mp4"; errs = []
    edl = json.loads((J / f"out/{v}_edl.json").read_text())
    starts = np.cumsum([0] + [p[2] for p in edl["pieces"]])[:-1]
    wh = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.strip()
    if wh != "1080,1920": errs.append(f"format {wh}")
    lum, fps = frames_luma(f); n = len(lum); dur = n / fps
    vo = audio(J / "vo/grace_vo.wav"); au = audio(f)
    if abs(dur - len(vo) / 8000) > 0.2: errs.append(f"length {dur:.2f}s vs VO {len(vo)/8000:.2f}s")
    jumps = np.abs(np.diff(lum)); cutf = [round(s * fps) for s in starts]
    bad = [i for i in np.where(jumps > 18)[0] if min(abs(i + 1 - c) for c in cutf) > 2]
    if bad: errs.append(f"flash at {[round((i+1)/fps,2) for i in bad[:6]]}")
    if lum.min() < 30: errs.append(f"dark frame {lum.min():.0f} at {lum.argmin()/fps:.2f}s")
    m = min(len(vo), len(au)); a, b = vo[:m], au[:m]
    lags = range(-160, 161, 4); r = [np.corrcoef(a[max(0, l):m + min(0, l)], b[max(0, -l):m - max(0, l)])[0, 1] for l in lags]
    best = int(np.argmax(r)); lag_ms = list(lags)[best] / 8
    if abs(lag_ms) > 20 or r[best] < 0.9: errs.append(f"sync lag {lag_ms:.0f} ms r {r[best]:.3f}")
    peak = 20 * np.log10(np.abs(au).max() + 1e-9); mean = 20 * np.log10(np.sqrt((au ** 2).mean()) + 1e-9)
    if peak > -0.5 or not (-30 <= mean <= -14): errs.append(f"levels peak {peak:.1f} mean {mean:.1f}")
    print(f"CUTQC_OK {v} ({dur:.2f}s, {len(edl['pieces'])} pieces, sync r {r[best]:.3f}, peak {peak:.1f} dB)" if not errs else f"CUTQC FAIL {v}: " + "; ".join(errs))
    return not errs


if __name__ == "__main__":
    ok = all([check(v) for v in sys.argv[1:]])
    sys.exit(0 if ok else 1)
