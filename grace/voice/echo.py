"""Blind room-echo meter for speech (free, local).

Usage: python3 echo.py FILE [FILE ...]   -> one line per file: rt60_est_ms, tail_db, speech_s

How it works: room echo stops speech energy from dropping fast after a syllable ends, so
the fastest energy decays in a clip are bounded by the room. rt60_est_ms = 60 dB divided by
the median slope of the steepest 25% of decays (10 ms frames, decays of >=12 dB). Lower = drier.
tail_db = median level 60-120 ms after a syllable offset relative to its peak (more negative = drier).
Only compares clips with each other; it is not a calibrated RT60.
"""
import subprocess, sys
import numpy as np


def load(path, sr=16000):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768, sr


def measure(path):
    x, sr = load(path)
    hop = sr // 100
    n = len(x) // hop
    e = np.array([np.mean(x[i * hop:(i + 1) * hop] ** 2) for i in range(n)]) + 1e-10
    db = 10 * np.log10(e)
    db = np.convolve(db, np.ones(2) / 2, mode="same")
    floor = np.percentile(db, 10)
    loud = np.percentile(db, 90)
    speech_s = float(np.sum(db > floor + 15)) / 100
    slopes, tails = [], []
    i = 1
    while i < n - 1:
        # local peak in loud speech
        if db[i] > loud - 12 and db[i] >= db[i - 1] and db[i] >= db[i + 1]:
            j = i
            while j + 1 < n and db[j + 1] < db[j] + 0.5 and j - i < 40:
                j += 1
            drop = db[i] - db[j]
            if drop >= 12 and db[j] > floor + 3 - 30:
                # slope over the first 12 dB of the fall
                k = i
                while k < j and db[i] - db[k] < 12:
                    k += 1
                slopes.append(12 / max(k - i, 1) * 100)  # dB/s
                if i + 12 < n:
                    tails.append(float(np.mean(db[i + 6:i + 12]) - db[i]))
            i = max(j, i + 1)
        else:
            i += 1
    if len(slopes) < 8:
        return None, None, speech_s, len(slopes)
    s = np.sort(slopes)[::-1]
    fast = s[: max(4, len(s) // 4)]
    rt = 60 / np.median(fast) * 1000
    return float(rt), float(np.median(tails)), speech_s, len(slopes)


def phrase_end(path, need=25, win=40):
    """Decay at pauses: ms from -5 dB to -25 dB below a syllable peak that is followed by a pause
    (5 ms frames, the level must fall 25 dB within 200 ms). Free decay with no speech after it, so the
    cleanest echo reading; echo also fills pauses, so an echoey voice yields fewer of them. Lower = drier.
    Returns (median ms, count)."""
    x, sr = load(path)
    hop = sr // 200
    n = len(x) // hop
    db = 10 * np.log10(np.array([np.mean(x[i * hop:(i + 1) * hop] ** 2) for i in range(n)]) + 1e-10)
    loud, floor = np.percentile(db, 90), np.percentile(db, 5)
    out, i = [], 1
    while i < n - win:
        if db[i] > loud - 18 and db[i] >= db[i - 1] and db[i + 1:i + win].max() < db[i] \
                and db[i + win - 6:i + win].max() < db[i] - need and db[i] - need > floor + 3:
            a = next(k for k in range(i, i + win) if db[k] < db[i] - 5)
            b = next(k for k in range(i, i + win) if db[k] < db[i] - need)
            out.append((b - a) * 5)
            i += win
        else:
            i += 1
    return (float(np.median(out)) if out else None), len(out)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        pe, npe = phrase_end(p)
        print(f"{p}\tphrase_end_ms={pe}\tends={npe}")
        rt, tail, sp, nd = measure(p)
        if rt is None:
            print(f"{p}\trt60_est_ms=NA\ttail_db=NA\tspeech_s={sp:.1f}\tdecays={nd}")
        else:
            print(f"{p}\trt60_est_ms={rt:.0f}\ttail_db={tail:.1f}\tspeech_s={sp:.1f}\tdecays={nd}")
