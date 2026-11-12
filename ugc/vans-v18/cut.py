"""Cut Vans V18-V37 (free): music-only, no text, 1080x1920, AI finish last. python3 cut.py V18 V21 ...
Pieces come from shots.json minus qc/dropped.json; a shot's clean window can be shortened in WIN (clip turned after it).
Each video gets its own Mixkit track (music/, Stock Music Free License) and its own small bright-neutral grade.
Writes out/<V>.mp4 + out/<V>_edl.json; QC with tools/cutqc.py --len 16."""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

J = Path(__file__).resolve().parent
S = json.loads((J / "shots.json").read_text())
D = json.loads((J / "qc/dropped.json").read_text())
FIN = J.parent.parent / ".claude/skills/ugc-product-ad/scripts/ai_finish.sh"
LEN = 16.0
WIN = {}   # clean windows for clips that turn (filled after QC of each batch)
TRACKS = ["catwalk", "gimme", "onemore", "funkee", "midnightfunk", "mornings"]
GRADES = ["eq=brightness=0.02:contrast=1.03:saturation=1.0", "eq=brightness=0.03:contrast=1.0:saturation=0.97",
          "eq=brightness=0.01:contrast=1.05:saturation=1.02", "eq=brightness=0.04:contrast=1.02:saturation=0.98",
          "eq=brightness=0.02:contrast=1.04:saturation=0.96", "eq=brightness=0.03:contrast=1.03:saturation=1.01"]
MUSIC_AT = [8.0, 12.0, 6.0, 10.0, 14.0, 9.0]


def pieces(v):
    ks = [k for k in S if S[k]["video"] == v and k not in D]
    fixed = {k: WIN[k] for k in ks if k in WIN}
    rest = [k for k in ks if k not in fixed]
    each = min(4.0, (LEN - sum(fixed.values())) / len(rest))
    return [(k, 0.0 if k in fixed else max(0.0, (4.0 - each) / 2), fixed.get(k, round(each, 3))) for k in ks]


def cut(v):
    n0 = int(v[1:]) - 18; i = n0 // 3 + n0 % 3   # each of a link's 3 videos gets its own track and grade
    P = pieces(v); out = J / "out"; out.mkdir(exist_ok=True)
    total = sum(p[2] for p in P)
    ins, fl = [], []
    for n, (k, ss, d) in enumerate(P):
        ins += ["-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", str(J / f"clips/{k}_sd.mp4")]
        fl.append(f"[{n}:v]scale=1080:1920:flags=lanczos,fps=30,{GRADES[i % 6]},setsar=1[v{n}]")
    tr = J / f"music/{TRACKS[i % 6]}.mp3"
    ins += ["-ss", str(MUSIC_AT[i % 6]), "-t", f"{total:.3f}", "-i", str(tr)]
    fl.append("".join(f"[v{n}]" for n in range(len(P))) + f"concat=n={len(P)}:v=1:a=0[v]")
    fl.append(f"[{len(P)}:a]afade=t=in:d=0.15,afade=t=out:st={total - 0.6:.3f}:d=0.6,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100[a]")
    raw = out / f"{v}_raw.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fl), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-threads", "4", "-t", f"{total:.3f}", str(raw)], check=True)
    fin = out / f"{v}_fin.mp4"
    subprocess.run(["bash", str(FIN), str(raw), str(fin)], check=True, capture_output=True)
    # ai_finish's grain at crf 18 runs ~45 Mbps; cap the final at 15 Mbps (as V13-V17) and make a 6.5 Mbps review copy
    for dst, rate in ((out / f"{v}.mp4", "15M"), (J / f"review/media/{v}.mp4", "6.5M")):
        dst.parent.mkdir(exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(fin), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                        "-maxrate", rate, "-bufsize", "2M" if rate == "6.5M" else "30M", "-pix_fmt", "yuv420p", "-c:a", "copy",
                        "-movflags", "+faststart", "-threads", "4", str(dst)], check=True)
    raw.unlink(); fin.unlink()
    (out / f"{v}_edl.json").write_text(json.dumps({"pieces": P, "track": TRACKS[i % 6], "music_at": MUSIC_AT[i % 6], "grade": GRADES[i % 6]}, indent=1))
    print(v, f"{total:.2f}s", len(P), "shots", TRACKS[i % 6], flush=True)


if __name__ == "__main__":
    with ThreadPoolExecutor(3) as ex: list(ex.map(cut, sys.argv[1:]))
