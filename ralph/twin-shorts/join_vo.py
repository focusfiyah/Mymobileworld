"""Join vo/line*.wav with 0.2 s gaps, trim each line's edge silence, loudnorm -16 LUFS -> vo/vo.wav (48 kHz mono)."""
import subprocess, glob
fs = sorted(glob.glob("vo/line[0-9].wav"))
inp = sum([["-i", f] for f in fs], [])
trim = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=0.2"
fc = "".join(f"[{i}:a]{trim},aresample=48000[a{i}];" for i in range(len(fs))) + "".join(f"[a{i}]" for i in range(len(fs))) + f"concat=n={len(fs)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", fc, "-map", "[o]", "-ac", "1", "-ar", "48000", "vo/vo.wav"], check=True)
print("JOINED")
