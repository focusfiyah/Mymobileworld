"""Clone a generated clip's own voice with ElevenLabs and render several takes of a replacement line.
Uses the REST API directly (the ElevenLabs MCP voice_clone fails with 400 invalid_labels, and its file tools only
accept paths under the Desktop). Key comes from OpenMontage's .env and is never printed.

Usage:
  python eleven_clone_takes.py <clip.mp4> <out_dir> "<new line>" --keep 0:1.58 2.06:3.12 9.02:12.66 [--voice-id ID]
  --keep  time ranges of the SAME speaker's other lines (not the bad one, no SFX), ~10s+ total.
  --voice-id  reuse an existing clone instead of creating a new one (a clone uses a voice slot).
"""
import argparse
import os
import subprocess
from pathlib import Path

import requests
from dotenv import load_dotenv

ap = argparse.ArgumentParser()
ap.add_argument("clip"); ap.add_argument("out_dir"); ap.add_argument("text")
ap.add_argument("--keep", nargs="+", default=[]); ap.add_argument("--voice-id"); ap.add_argument("--name", default="clip voice")
a = ap.parse_args()
out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
load_dotenv("C:/dev/OpenMontage/.env")
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}

vid = a.voice_id
if not vid:
    n = len(a.keep)
    parts = ";".join(f"[s{i}]atrim={r},asetpts=PTS-STARTPTS[k{i}]" for i, r in enumerate(a.keep))
    fc = f"[0:a]asplit={n}" + "".join(f"[s{i}]" for i in range(n)) + ";" + parts + ";" + \
         "".join(f"[k{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1,aresample=44100[o]"
    sample = out / "voice_sample.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.clip, "-vn", "-filter_complex", fc, "-map", "[o]", "-ac", "1",
                    str(sample)], check=True)
    with open(sample, "rb") as f:
        r = requests.post("https://api.elevenlabs.io/v1/voices/add", headers=H, data={"name": a.name},
                          files=[("files", (sample.name, f, "audio/wav"))], timeout=120)
    r.raise_for_status()
    vid = r.json()["voice_id"]
    (out / "voice_id.txt").write_text(vid)
print("voice_id", vid)

TAKES = {  # t2 won on Bruise Cream (clearest once spliced in context); keep the spread
    "t1": ("eleven_multilingual_v2", {"stability": 0.45, "similarity_boost": 0.9, "style": 0.3, "use_speaker_boost": True}),
    "t2": ("eleven_multilingual_v2", {"stability": 0.6, "similarity_boost": 0.9, "style": 0.15, "use_speaker_boost": True}),
    "t3": ("eleven_v3", {"stability": 0.5, "similarity_boost": 0.9}),
}
for name, (model, vs) in TAKES.items():
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128", headers=H,
                      json={"text": a.text, "model_id": model, "voice_settings": vs}, timeout=120)
    print(name, model, r.status_code)
    if r.ok:
        (out / f"take_{name}.mp3").write_bytes(r.content)
