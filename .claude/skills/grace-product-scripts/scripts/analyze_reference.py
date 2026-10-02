#!/usr/bin/env python3
"""Analyse a reference TikTok for Grace's scripts.

Usage: python3 analyze_reference.py <video.mp4> <out_dir>

Writes to out_dir:
  audio.mp3        mono 16 kHz audio track
  stt.json         ElevenLabs scribe_v2 response (word timestamps, audio events)
  transcript.txt   full text, then one line per sentence with start-end seconds
  sheet1.jpg ...   1 fps contact sheets, 6x4 tiles of 240 px frames

ElevenLabs goes through the cloud proxy, which injects the API key, so no key is needed here.
ffmpeg comes from imageio-ffmpeg (installed on first run) because the container has no system ffmpeg.
"""
import json
import math
import os
import shutil
import subprocess
import sys


def ffmpeg_bin():
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"], check=True)
        import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def duration(ff, video):
    out = subprocess.run([ff, "-i", video], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    video, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    ff = ffmpeg_bin()

    dur = duration(ff, video)
    print(f"duration {dur:.1f}s")

    audio = os.path.join(out, "audio.mp3")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000", audio], check=True)

    sheets = max(1, math.ceil(dur / 24))
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", video, "-vf", "fps=1,scale=240:-1,tile=6x4",
                    "-frames:v", str(sheets), os.path.join(out, "sheet%d.jpg")], check=True)

    stt_path = os.path.join(out, "stt.json")
    subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text",
                    "-F", "model_id=scribe_v2", "-F", f"file=@{audio}", "-F", "tag_audio_events=true",
                    "-o", stt_path], check=True)
    stt = json.load(open(stt_path))
    if "words" not in stt:
        sys.exit(f"speech-to-text failed: {stt}")

    lines, text, start = [], "", None
    for w in stt["words"]:
        if w.get("type") == "spacing":
            continue
        if start is None:
            start = w["start"]
        text += w["text"] + " "
        if w["text"].endswith((".", "?", "!")):
            lines.append(f"{start:5.1f}-{w['end']:5.1f}  {text.strip()}")
            text, start = "", None
    if text:
        lines.append(f"{start:5.1f}-      {text.strip()}")

    words = len(stt.get("text", "").split())
    report = [stt.get("text", ""), "", f"{words} words in {dur:.1f}s", ""] + lines
    open(os.path.join(out, "transcript.txt"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))
    print(f"\nsheets: {sheets} in {out}")


if __name__ == "__main__":
    main()
