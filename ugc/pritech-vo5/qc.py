"""QC for the V5-V9 cuts (2026-10-29). Prints QC_OK <video> only when every check passes.
  python3 qc.py V5 [V6 ...]
Checks: length = VO + hold; 1080x1920 30 fps; no brightness flash (> 6 mean luma frame to frame) or hard jump (> 35 mean pixel change) inside a shot; bright neutral grade (mean luma >= 95, no shot under 70); audio = Grace's VO untouched (same length, peak
<= -0.1 dBFS, -18..-15 LUFS) and echo <= 150 ms. Writes qc/sheet_<V>.jpg (a frame every 0.5 s) to look at."""
import json, re, subprocess, sys
import numpy as np
from PIL import Image

S = json.load(open("shots.json"))
WIN = {"V8S7": (15.35, 18.65), "V8S8": (18.65, 20.95)}
run = lambda c: subprocess.run(c, capture_output=True, text=True)


def frames(f, w=108, h=192):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(float)


def qc(v):
    f = f"out/pritech_{v}.mp4"; errs = []
    info = json.loads(run(["ffprobe", "-v", "error", "-show_entries", "stream=width,height,r_frame_rate,codec_type:format=duration", "-of", "json", f]).stdout)
    vs = [s for s in info["streams"] if s["codec_type"] == "video"][0]; dur = float(info["format"]["duration"])
    if (vs["width"], vs["height"]) != (1080, 1920) or vs["r_frame_rate"] != "30/1": errs.append(f"format {vs['width']}x{vs['height']} {vs['r_frame_rate']}")
    if abs(dur - 21.30) > 0.1: errs.append(f"length {dur:.2f} s (want 21.30)")
    cuts = sorted({round(WIN.get(s["id"], s["t"])[0] * 30) for s in S if s["video"] == v} - {0})
    fr = frames(f); m = fr.mean((1, 2)); jumps = np.abs(np.diff(fr, axis=0)).mean((1, 2))
    dm = np.abs(np.diff(m))   # flash = whole-frame brightness change; hard jump = most pixels change at once (a cut inside a clip)
    for i, (j, b) in enumerate(zip(jumps, dm), 1):
        if any(abs(i - c) <= 1 for c in cuts): continue
        if b > 6: errs.append(f"flash: brightness {b:.1f} at {i / 30:.2f} s")
        if j > 35: errs.append(f"hard jump {j:.0f} at {i / 30:.2f} s, not a cut")
    if m.mean() < 95: errs.append(f"mean luma {m.mean():.0f} < 95 (too dark)")
    bounds = [0] + cuts + [len(m)]
    for a, b in zip(bounds, bounds[1:]):
        if m[a:b].mean() < 70: errs.append(f"shot at {a / 30:.2f} s mean luma {m[a:b].mean():.0f} < 70")
    a = run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"]).stderr
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", a)[-1]); peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", a)[-1])
    if not (-18 <= lufs <= -15) or peak > -0.1: errs.append(f"audio {lufs} LUFS peak {peak} dBFS")
    run(["ffmpeg", "-v", "error", "-y", "-i", f, "-vn", "-ac", "1", "-ar", "44100", f"qc/{v}_audio.wav"])
    e = run(["python3", "../../grace/voice/echo.py", f"qc/{v}_audio.wav"]).stdout
    rt = [int(x) for x in re.findall(r"rt60_est_ms=(\d+)", e)]
    if not rt or rt[-1] > 150: errs.append(f"echo {rt}")
    # sheet: a frame every 0.5 s
    ims = []
    for t in np.arange(0.25, dur, 0.5):
        p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=180:320", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        from io import BytesIO; ims.append(Image.open(BytesIO(p)).convert("RGB"))
    cols = 9; sh = Image.new("RGB", (180 * cols, 320 * ((len(ims) + cols - 1) // cols)), "white")
    for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 180, (i // cols) * 320))
    sh.save(f"qc/sheet_{v}.jpg", quality=82)
    print(f"{v}: {dur:.2f} s, luma {m.mean():.0f}, {lufs} LUFS, peak {peak}, echo {rt[-1] if rt else None} ms, max in-shot jump {max([j for i, j in enumerate(jumps, 1) if not any(abs(i - c) <= 1 for c in cuts)] or [0]):.1f}")
    print(f"QC_OK {v}" if not errs else f"QC_FAIL {v}: " + "; ".join(errs))
    return not errs


if __name__ == "__main__":
    ok = all([qc(v) for v in sys.argv[1:]]); sys.exit(0 if ok else 1)
