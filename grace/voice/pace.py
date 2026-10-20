"""Free pacing fix for a voiceover: cap pauses between words, then time-stretch (pitch and formants kept) to a target.

Usage: python3 pace.py IN OUT [--pause 0.15] [--wps 4.1 | --len SECONDS]
Word times come from local Whisper (faster-whisper base, free). Gaps longer than --pause are cut down to it (the cut
sits in the middle of the gap, so word tails stay). Then rubberband stretches the result to --wps words per second
of speech, or to --len seconds. Levels to -16 LUFS.
"""
import argparse, subprocess, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from echo import load


def words(path):
    from faster_whisper import WhisperModel
    m = WhisperModel("base", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(load(path)[0], language="en", word_timestamps=True)
    return [w for s in segs for w in s.words]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out")
    ap.add_argument("--pause", type=float, default=0.15)
    ap.add_argument("--wps", type=float); ap.add_argument("--len", type=float)
    a = ap.parse_args()
    w = words(a.inp)
    keep, t = [], 0.0
    for i in range(1, len(w)):
        gap = w[i].start - w[i - 1].end
        if gap > a.pause:
            mid = (w[i - 1].end + w[i].start) / 2
            keep.append((t, mid - a.pause / 2)); t = mid + a.pause / 2
    keep.append((t, None))
    parts = "".join(f"[0:a]atrim={s:.3f}" + (f":{e:.3f}" if e else "") + f",asetpts=PTS-STARTPTS[p{k}];" for k, (s, e) in enumerate(keep))
    cut_len = sum((e if e else (w[-1].end + 0.35)) - s for s, e in keep)
    speech = cut_len - 0.35
    if a.wps:
        target = len(w) / a.wps + 0.35
    else:
        target = a.len or cut_len
    tempo = cut_len / target
    fc = parts + "".join(f"[p{k}]" for k in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,rubberband=tempo={tempo:.4f}:pitch=1:formant=preserved:transients=smooth,loudnorm=I=-16:TP=-1.5[o]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.inp, "-filter_complex", fc, "-map", "[o]", "-ar", "44100", "-b:a", "128k", a.out], check=True)
    print(f"{len(keep) - 1} pauses capped at {a.pause}s, tempo x{tempo:.3f}, {cut_len:.2f}s -> {target:.2f}s")


if __name__ == "__main__":
    main()
