"""Cut the Vans plaid recreations (free): music only, no text, 1080x1920, original cut times, AI finish last, QC built in.
  python3 cut.py V1 V2  -> out/V1.mp4, out/V2.mp4 (+ out/<V>_edl.json); prints CUTQC_OK <V> or CUTQC FAIL lines."""
import json, subprocess, sys
from pathlib import Path
import numpy as np
J = Path(__file__).resolve().parent
FIN = J.parent.parent / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"
EDL = {  # (clip, in, out); V2 windows moved to cut before V2S1's grip jump (1.96 s) and V2S2's leg kick (1.25 s)
 "V1": [("V1S1", 0.0, 7.42)],
 "V2": [("V2S1", 0.0, 1.9), ("V2S2", 0.0, 1.25), ("V2S3", 0.3, 2.4), ("V2S4", 0.0, 2.72)],
}
MUSIC = {"V1": "505", "V2": "866"}


def music_start(mp3):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.int16).astype(float); r = np.array([np.sqrt((a[i*8000:(i+1)*8000]**2).mean()) for i in range(len(a)//8000)])
    return float(np.argmax(r[2:40] > 0.8 * r.max()) + 2)   # first full-energy second, skipping a soft intro


def cut(v):
    out = J / "out"; out.mkdir(exist_ok=True)
    P = EDL[v]; total = sum(b - a for _, a, b in P)
    ins, fl = [], []
    for i, (c, a, b) in enumerate(P):
        ins += ["-ss", f"{a:.3f}", "-t", f"{b-a:.3f}", "-i", str(J / f"clips/{c}.mp4")]
        fl.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=30,setpts=PTS-STARTPTS[v{i}]")
    mp3 = J / f"music/{MUSIC[v]}.mp3"; ms = music_start(mp3)
    ins += ["-ss", str(ms), "-t", f"{total:.3f}", "-i", str(mp3)]
    fl.append("".join(f"[v{i}]" for i in range(len(P))) + f"concat=n={len(P)}:v=1:a=0[v]")
    fl.append(f"[{len(P)}:a]loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:d=0.15,afade=t=out:st={total-0.4:.3f}:d=0.4,aresample=48000[a]")
    raw = out / f"{v}_raw.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fl), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", str(raw)], check=True)
    subprocess.run(["bash", str(FIN), str(raw), str(out / f"{v}.mp4")], check=True, capture_output=True)
    (out / f"{v}_edl.json").write_text(json.dumps({"pieces": P, "music": MUSIC[v], "music_at": ms}, indent=1))
    return out / f"{v}.mp4", total, [sum(b - a for _, a, b in P[:k]) for k in range(1, len(P))]


def qc(f, total, cuts):
    bad = []
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height:format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout.split()
    if pr[0] != "1080,1920": bad.append(f"size {pr[0]}")
    if abs(float(pr[1]) - total) > 0.1: bad.append(f"length {pr[1]} vs {total:.2f}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-vf", "scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    L = np.frombuffer(raw, np.uint8).reshape(-1, 96*54).astype(float).mean(1); d = np.abs(np.diff(L))
    cf = [round(c*30) for c in cuts]
    for i in np.where(d > 18)[0]:
        if not any(abs(i - c) <= 2 for c in cf): bad.append(f"flash at frame {i} ({d[i]:.0f})")
    if L.min() < 30: bad.append(f"dark frame {L.min():.0f}")
    vol = subprocess.run(["ffmpeg", "-i", str(f), "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mx = float(vol.split("max_volume:")[1].split()[0]); mn = float(vol.split("mean_volume:")[1].split()[0])
    if mx > -0.5: bad.append(f"peak {mx}")
    if not -30 <= mn <= -14: bad.append(f"mean {mn}")
    print(f"CUTQC_OK {f.stem} {total:.2f}s peak {mx} mean {mn}" if not bad else f"CUTQC FAIL {f.stem}: " + "; ".join(bad), flush=True)


if __name__ == "__main__":
    for v in sys.argv[1:]:
        f, t, c = cut(v); qc(f, t, c)
