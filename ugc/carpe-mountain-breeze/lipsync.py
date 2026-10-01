"""Lip-sync Grace's face shots to the Grace B voiceover: Kie volcengine/video-to-video-lip-sync, $0.04/s of audio.

  python3 lipsync.py S10            # one shot (test first), or several: S1 V2 V5 S10

Each shot = the exact piece cut.py uses (full frame) + the voiceover slice under it -> lipsync/<ID>.mp4.
cut.py uses lipsync/<ID>.mp4 when it exists and always mixes the ORIGINAL voiceover (the lip-sync step re-encodes
and degrades the audio; the mouth still matches because that same audio drove it).
"""
import subprocess, sys
from pathlib import Path

sys.argv, ids = sys.argv[:1], sys.argv[1:]
exec(open("kie.py").read().split("if __name__")[0])          # upload, run_task, fetch, log

# shot: (clip, in, length used, voiceover start, voiceover end)  -- times match cut.py's EDL
SEG = {
    "S1": ("clips/S1.mp4", 0.0, 4.13, 0.0, 4.13),
    "V2": ("clips/V2.mp4", 0.0, 5.83, 4.13, 9.96),
    "V5": ("clips/V5.mp4", 0.0, 3.35, 27.47, 30.82),
    "S10": ("clips/S10.mp4", 0.0, 4.04, 30.82, 35.03),
}
Path("lipsync/src").mkdir(parents=True, exist_ok=True)
for sid in ids:
    clip, t_in, length, a0, a1 = SEG[sid]
    v, a = f"lipsync/src/{sid}.mp4", f"lipsync/src/{sid}.mp3"
    pad = max(0.0, (a1 - a0) - length) + 0.1                    # video must cover the whole audio slice
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clip, "-vf",
                    f"trim=start={t_in}:end={t_in + length},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={pad:.2f}",
                    "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", v], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "vo/voiceover.mp3", "-af", f"atrim={a0}:{a1},asetpts=N/SR/TB",
                    "-c:a", "libmp3lame", "-b:a", "192k", a], check=True)
    print(sid, f"audio {a1 - a0:.2f}s -> ${(a1 - a0) * 0.04:.2f}", flush=True)
    url = run_task({"model": "volcengine/video-to-video-lip-sync",
                    "input": {"mode": "lite", "video_url": upload(v), "audio_url": upload(a), "align_audio": True}})
    if url:
        fetch(url, f"lipsync/{sid}.mp4"); print(sid, "ok", flush=True)
