"""Measure the dead air in each generated shot and print trim points for the assembly.

Grok (and most video models) leave ~0.5-1.0s of silence at the head and tail of every clip. On a
7-shot ad that is ~5s of slack, and Ralph WILL ask for it to be removed.

    python trim_pauses.py shot1.mp4 shot2.mp4 ...

Measures the FIRST and LAST WORD with the transcriber, not silencedetect alone: silencedetect also
fires on the pauses between sentences, and on a breath before the first word.

**Keep a longer tail wherever the tail is a visual beat** - a coffee sip finishing, a held
finger-point under a CTA, a prop being set down. Cutting on the last word clips the action, so this
script only suggests; you decide per shot. After trimming, recompute EVERY overlay window and the
CTA start from the new shot boundaries.
"""
import subprocess
import sys
from pathlib import Path

FFB = ("C:/Users/ralph/AppData/Local/Microsoft/WinGet/Packages/"
       "Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin/")
LEAD, TAIL = 0.15, 0.25   # handles kept around the speech


def duration(path: Path) -> float:
    out = subprocess.run([FFB + "ffprobe.exe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout
    return float(out.strip())


def main(paths):
    sys.path.insert(0, "C:/dev/OpenMontage")
    from tools.tool_registry import registry
    registry.discover()
    total_in = total_out = 0.0
    for p in map(Path, paths):
        dur = duration(p)
        tr = registry._tools["transcriber"].execute(
            {"input_path": str(p), "model_size": "small", "language": "en"})
        words = [w for s in (tr.data or {}).get("segments", []) for w in s.get("words", [])]
        if not words:
            print(f"{p.name}: NO SPEECH (dur {dur:.2f}) - trim by hand")
            continue
        start = max(0.0, words[0]["start"] - LEAD)
        end = min(dur, words[-1]["end"] + TAIL)
        total_in += dur
        total_out += end - start
        print(f"{p.name}: dur {dur:.2f} | speech {words[0]['start']:.2f}-{words[-1]['end']:.2f} "
              f"| trim {start:.2f}:{end:.2f} | saves {dur - (end - start):.2f}s")
    if total_in:
        print(f"\nTOTAL {total_in:.1f}s -> {total_out:.1f}s (saves {total_in - total_out:.1f}s)")
        print("Remember: give visual-beat tails (sip, held point) more room than the handle above.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    main(sys.argv[1:])
