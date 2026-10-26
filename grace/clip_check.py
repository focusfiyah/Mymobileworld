"""Clip check (Ralph 2026-10-26, from Sabrina Ramonov's /generate skill email): Kie bills any task that returns a
video, even one that ignored the input image (her first clip came back as a random landscape and was charged). So
every paid clip is checked against the still it was made from, before anyone looks at it, and a still is checked
before it is animated.

  python3 grace/clip_check.py STILL CLIP [--aspect 9:16] [--seconds 4] [--min-short 720]
  python3 grace/clip_check.py STILL --still-only [--aspect 9:16]

Clip checks: it has a video stream; its aspect matches the still (and --aspect) within 3%; the short side is at least
--min-short px (720 = our Seedance 720p; Flow and Omni 1080p takes pass too); the length is within 0.5 s of
--seconds; and the opening second looks like the still (score below). Still-only: the aspect matches --aspect.
Prints CLIP_CHECK_OK or CLIP_CHECK_FAIL with the reasons; exit 0 / 1. A FAIL means: do not send the clip, look at it
first, and fetch it again (recordInfo) before asking Ralph about a paid redo.

Score: the best of 5 frames in the first second vs the still, each = 0.6 x pixel correlation of a blurred grey 36x64
thumbnail + 0.4 x colour histogram overlap (HSV 8x4x4). Threshold MIN_SCORE was set on 242 real still/clip pairs
from ugc/*/ against 242 clips paired with another job's still (tools/clipcheck/calibrate.py, RESULTS.md there).
"""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

MIN_SCORE = 0.50          # set by tools/clipcheck/calibrate.py; see RESULTS.md there
ASPECT_TOL = 0.03
TIMES = (0.0, 0.25, 0.5, 0.75, 1.0)
THUMB = (36, 64)          # w, h for a vertical frame (swapped for landscape)


def probe(clip):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:format=duration", "-of", "json", str(clip)], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout or "{}")
        s = (d.get("streams") or [{}])[0]
        return int(s["width"]), int(s["height"]), float((d.get("format") or {}).get("duration") or 0)
    except (KeyError, ValueError, IndexError):
        return None


def parse_aspect(a):
    w, h = a.split(":")
    return float(w) / float(h)


def _fit(img, ratio):
    """Centre-crop img to the clip's aspect ratio, so a still and a clip of slightly different shape still compare."""
    w, h = img.size
    if abs(w / h - ratio) < 1e-3:
        return img
    if w / h > ratio:
        nw = int(round(h * ratio)); x = (w - nw) // 2
        return img.crop((x, 0, x + nw, h))
    nh = int(round(w / ratio)); y = (h - nh) // 2
    return img.crop((0, y, w, y + nh))


def _feat(img, ratio):
    img = _fit(img.convert("RGB"), ratio)
    size = THUMB if ratio <= 1 else THUMB[::-1]
    g = np.asarray(img.convert("L").resize(size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(1)), dtype=float).ravel()
    hsv = np.asarray(img.resize((96, 96), Image.BILINEAR).convert("HSV"), dtype=int).reshape(-1, 3)
    hist = np.histogramdd(hsv // [32, 64, 64], bins=(8, 4, 4), range=((0, 8), (0, 4), (0, 4)))[0].ravel()
    return (g - g.mean()) / (g.std() + 1e-6), hist / hist.sum()


def similarity(a, b):
    corr = float(np.clip((a[0] * b[0]).mean(), -1, 1))
    hist = float(np.minimum(a[1], b[1]).sum())
    return 0.6 * max(corr, 0.0) + 0.4 * hist


def frames(clip, times=TIMES):
    out = []
    with tempfile.TemporaryDirectory() as d:
        for i, t in enumerate(times):
            f = Path(d) / f"f{i}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(clip), "-frames:v", "1", str(f)],
                           capture_output=True)
            if f.exists():
                out.append(Image.open(f).copy())
    return out


def score(still, clip, info=None):
    info = info or probe(clip)
    ratio = info[0] / info[1]
    s = _feat(Image.open(still), ratio)
    vals = [similarity(s, _feat(f, ratio)) for f in frames(clip)]
    return max(vals) if vals else 0.0


def check_still(still, aspect="9:16"):
    w, h = Image.open(still).size
    want = parse_aspect(aspect)
    if abs(w / h - want) / want > ASPECT_TOL:
        return [f"still is {w}x{h} ({w / h:.3f}), not {aspect} ({want:.3f}): the clip would be cropped or letterboxed"]
    return []


def check_clip(still, clip, aspect=None, seconds=None, min_short=720):
    """List of problems (empty = OK) and the match score."""
    info = probe(clip)
    if not info:
        return [f"{clip}: no video stream (download failed or not a video)"], 0.0
    w, h, dur = info; errs = []
    sw, sh = Image.open(still).size
    if abs((w / h) - (sw / sh)) / (sw / sh) > ASPECT_TOL:
        errs.append(f"clip is {w}x{h}, still is {sw}x{sh}: different shape")
    if aspect and abs(w / h - parse_aspect(aspect)) / parse_aspect(aspect) > ASPECT_TOL:
        errs.append(f"clip is {w}x{h}, not {aspect}")
    if min(w, h) < min_short:
        errs.append(f"clip short side {min(w, h)} px < {min_short}")
    if seconds and abs(dur - float(seconds)) > 0.5:
        errs.append(f"clip is {dur:.2f} s, asked for {seconds} s")
    sc = score(still, clip, info)
    if sc < MIN_SCORE:
        errs.append(f"opening second does not look like the still (score {sc:.2f} < {MIN_SCORE}): the model may have"
                    " ignored the image; look before anyone else does")
    return errs, sc


def report(still, clip, **kw):
    """For runners: print the verdict, return (ok, score)."""
    errs, sc = check_clip(still, clip, **kw)
    if errs:
        print(f"CLIP_CHECK_FAIL {clip} (score {sc:.2f}):\n  - " + "\n  - ".join(errs), flush=True)
    else:
        print(f"CLIP_CHECK_OK {clip} (score {sc:.2f})", flush=True)
    return not errs, round(sc, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("still"); ap.add_argument("clip", nargs="?")
    ap.add_argument("--aspect"); ap.add_argument("--seconds", type=float)
    ap.add_argument("--min-short", type=int, default=720)
    ap.add_argument("--still-only", action="store_true")
    a = ap.parse_args()
    if a.still_only or not a.clip:
        errs = check_still(a.still, a.aspect or "9:16")
        print("CLIP_CHECK_OK still " + a.still if not errs else "CLIP_CHECK_FAIL still:\n  - " + "\n  - ".join(errs))
        return 1 if errs else 0
    ok, _ = report(a.still, a.clip, aspect=a.aspect, seconds=a.seconds, min_short=a.min_short)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
