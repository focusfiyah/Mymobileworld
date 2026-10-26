"""G3: both test videos exist, within 0.5 s of the voice line, each with an audio track."""
import subprocess
def probe(f, what):
    return subprocess.run(["ffprobe", "-v", "error", "-show_entries", what, "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
vo = float(probe("vo/line.mp3", "format=duration")); bad = []
for f in ("out/h3max.mp4", "out/kling_avatar.mp4"):
    d = probe(f, "format=duration"); a = probe(f, "stream=codec_type")
    if not d or abs(float(d) - vo) > 0.5 or "audio" not in a: bad.append(f"{f}: dur {d} vs {vo:.2f}, streams {a.split()}")
print("CLIPS_OK" if not bad else "CLIPS_BAD " + "; ".join(bad))
