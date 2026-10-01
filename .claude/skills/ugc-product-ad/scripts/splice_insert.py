"""Replace clip 2's opening leg shot with a stretch of the whole-leg insert.

Clip 2's first cut lands after frame 28 (1.21s at 24fps), so the insert fills frames 0-28
and clip 2 resumes at frame 29. Clip 2's own audio runs underneath unchanged.

Usage: python splice_leg_insert.py <insert_start_seconds> [out_suffix]
"""
import subprocess
import sys
from pathlib import Path

R = Path("C:/dev/OpenMontage/projects/restlex-couple-skit/renders")
CLIP = R / "clip2_mini_v1.mp4"
INSERT = R / "leg_insert_mini_v2.mp4"
FPS = 24
CUT_FRAME = 29  # first frame of clip 2's second shot


def main() -> None:
    start = float(sys.argv[1])
    suffix = sys.argv[2] if len(sys.argv) > 2 else "legfix"
    start_frame = round(start * FPS)
    out = R / f"clip2_mini_v1_{suffix}.mp4"
    graph = (
        f"[0:v]fps={FPS},scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
        f"trim=start_frame={start_frame}:end_frame={start_frame + CUT_FRAME},setpts=PTS-STARTPTS,format=yuv420p[leg];"
        f"[1:v]fps={FPS},trim=start_frame={CUT_FRAME},setpts=PTS-STARTPTS,format=yuv420p[rest];"
        f"[leg][rest]concat=n=2:v=1:a=0[v]"
    )
    cmd = [
        "ffmpeg", "-hide_banner", "-v", "error", "-y",
        "-i", str(INSERT), "-i", str(CLIP),
        "-filter_complex", graph,
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True)
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-show_entries",
         "stream=codec_type,width,height", "-of", "default=noprint_wrappers=1", str(out)],
        capture_output=True, text=True)
    print(out)
    print(probe.stdout.strip())


if __name__ == "__main__":
    main()
