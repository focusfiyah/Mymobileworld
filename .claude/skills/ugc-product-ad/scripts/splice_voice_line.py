"""Replace one spoken line in a generated clip with a new audio take, video stream copied untouched.
Only valid when the speaker's mouth is NOT visible during the line (off camera, B-roll, insert).

Fades the original out/in around the line (50ms), fills the gap with low pink-noise room tone matched to a quiet
pause, trims the take's edge silence, matches its loudness to the original line's voiced RMS, and overlays it at the
old start time. Loudnorm the result afterwards with the rest of the assembly.

Usage:
  python splice_voice_line.py <clip.mp4> <take.mp3> <out.mp4> --line 6.92:8.76 --gap 6.85:8.95 --pause 12.66:12.90 [--tone 0.5]
  --line   original line start:end (from the whisper transcript); the take is placed at the start
  --gap    region to replace; must end before the next line starts, and the take must fit inside it
  --pause  a quiet moment between lines, used only to measure the room-tone level
"""
import argparse
import subprocess

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("clip"); ap.add_argument("take"); ap.add_argument("out")
ap.add_argument("--line", required=True); ap.add_argument("--gap", required=True); ap.add_argument("--pause", required=True)
ap.add_argument("--tone", type=float, default=0.5)
a = ap.parse_args()
rng = lambda s: tuple(float(x) for x in s.split(":"))
L0, L1 = rng(a.line); G0, G1 = rng(a.gap); P0, P1 = rng(a.pause)
SR = 44100


def pcm(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16) / 32768.0


rms = lambda y: float(np.sqrt(np.mean(y ** 2)))
voiced = lambda y: y[np.abs(y) > 0.02]
orig, new = pcm(a.clip), pcm(a.take)
act = np.abs(new) > 10 ** (-45 / 20)
new = new[np.argmax(act): len(new) - np.argmax(act[::-1])]
dur = len(new) / SR
if L0 + dur > G1:
    raise SystemExit(f"take is {dur:.2f}s and would run past the gap end ({G1}s): pick a shorter take")
gain = rms(voiced(orig[int(L0 * SR): int(L1 * SR)])) / rms(voiced(new))
tone = rms(orig[int(P0 * SR): int(P1 * SR)])

fc = (
    f"[0:a]atrim=0:{G0},asetpts=PTS-STARTPTS,afade=t=out:st={max(0.0, G0 - 0.05):.3f}:d={min(0.05, G0):.3f}[a];"  # clamp: a line at 0.0s gave afade st=-0.05
    f"anoisesrc=d={G1 - G0}:c=pink:r={SR}:a={tone * a.tone:.5f},lowpass=f=5000,"
    f"afade=t=in:d=0.05,afade=t=out:st={G1 - G0 - 0.05}:d=0.05[g];"
    f"[0:a]atrim={G1},asetpts=PTS-STARTPTS,afade=t=in:d=0.05[c];"
    f"[a][g][c]concat=n=3:v=0:a=1[base];"
    f"[1:a]aresample={SR},silenceremove=start_periods=1:start_threshold=-45dB,volume={gain:.3f},"
    f"afade=t=out:st={dur - 0.03:.3f}:d=0.03,adelay={int(L0 * 1000)}:all=1[line];"
    f"[base][line]amix=inputs=2:duration=first:normalize=0[aout]"
)
subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", a.clip, "-i", a.take, "-filter_complex", fc,
                "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), a.out],
               check=True)
print(f"gain {gain:.2f}, take {dur:.2f}s at {L0}s, room tone rms {tone:.4f} -> {a.out}")
