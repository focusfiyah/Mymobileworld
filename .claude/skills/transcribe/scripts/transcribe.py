#!/usr/bin/env python3
"""transcribe.py: free local speech-to-text with faster-whisper (no API key, no credits).

usage: python3 transcribe.py FILE [--out DIR] [--model small.en] [--lang en]
FILE is any audio or video file ffmpeg can read. Writes into DIR (default: next to FILE):
  transcript.txt         plain text
  transcript_timed.txt   one line per segment: start-end text
  transcript.json        openai-whisper layout (segments with words), the format reference-breakdown's measure.py reads
First run makes a venv at ~/.cache/transcribe-venv (pip install faster-whisper numpy) and downloads the model from
Hugging Face (small.en ~480 MB, base.en ~145 MB). Needs ffmpeg, python3, network for the first run only.
Music-only audio makes Whisper invent words ("Thank you."): check against the frames.
"""
import argparse, json, os, subprocess, sys

VENV = os.path.expanduser("~/.cache/transcribe-venv")
PY = os.path.join(VENV, "bin", "python")


def bootstrap():
    if os.path.exists(PY):
        return
    subprocess.check_call([sys.executable, "-m", "venv", VENV])
    subprocess.check_call([PY, "-m", "pip", "install", "-q", "faster-whisper", "numpy"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out")
    ap.add_argument("--model", default="small.en", help="tiny.en, base.en, small.en, medium.en, large-v3 (default small.en)")
    ap.add_argument("--lang", default=None, help="language code for multilingual models (e.g. es); use a non-.en model")
    ap.add_argument("--inner", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if not a.inner:
        bootstrap()
        os.execv(PY, [PY, os.path.abspath(__file__), "--inner"] + sys.argv[1:])
    import numpy as np
    from faster_whisper import WhisperModel
    # Decode with ffmpeg ourselves: faster-whisper's own decoder breaks on some PyAV versions.
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.file, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True)
    if raw.returncode or not raw.stdout:
        sys.exit("ffmpeg could not read audio from " + a.file + ": " + raw.stderr.decode()[:300])
    audio = np.frombuffer(raw.stdout, np.float32)
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, info = model.transcribe(audio, word_timestamps=True, language=a.lang, condition_on_previous_text=False)
    out = a.out or os.path.dirname(os.path.abspath(a.file))
    os.makedirs(out, exist_ok=True)
    data, timed, text = [], [], []
    for s in segs:
        data.append({"start": s.start, "end": s.end, "text": s.text,
                     "words": [{"word": w.word, "start": w.start, "end": w.end} for w in (s.words or [])]})
        timed.append(f"{s.start:6.1f}-{s.end:6.1f}  {s.text.strip()}")
        text.append(s.text.strip())
    json.dump({"language": info.language, "segments": data}, open(os.path.join(out, "transcript.json"), "w"))
    open(os.path.join(out, "transcript.txt"), "w").write("\n".join(text) + "\n")
    open(os.path.join(out, "transcript_timed.txt"), "w").write("\n".join(timed) + "\n")
    print(f"{len(data)} segments, {info.duration:.1f} s, language {info.language} -> {out}")


main()
