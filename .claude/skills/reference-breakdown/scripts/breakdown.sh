#!/usr/bin/env bash
# breakdown.sh: everything Claude needs to read a reference video, made locally (no generation,
# no credits used).
#
# usage: breakdown.sh [-f] <video file or URL> [out dir]
#   -f, --force   write into an out dir that already has files in it (existing files are replaced)
#   -h, --help    show this help
#
# Writes into the out dir (default ./ref):
#   ref.mp4         the video (a local copy, or downloaded with yt-dlp, or curl for a direct file link)
#   info.txt        duration, size, fps, audio yes/no, number of cuts, cuts per minute
#   cuts.txt        timestamps of hard cuts (scene change > 0.28)
#   sheet.jpg       24 evenly spaced frames, 8 x 3, for the whole-arc read
#   frames/         one frame per second at 540 px wide, for reading HUD text and numbers
#   sheets/         the same frames tiled 8 x 4 (32 s per sheet): read every second of the arc
#   full/           full-resolution frames at every hard cut and every 5 s, for type and colour
#   measure.txt     camera motion every 0.5 s, palette, caption boxes, pace, sound levels (measure.py)
#   transcript.json word timings, and transcript.txt timed speech, when a local Whisper is found
#                   (set WHISPER_PY=/path/to/python with mlx_whisper or openai-whisper installed).
#                   Music-only videos make Whisper invent words ("Thank you."): trust the frames.
#
# Only download videos you are allowed to download. The reference is for reading and measuring:
# never upload its frames to a generation model.
# Needs: ffmpeg, ffprobe, python3 with numpy; yt-dlp for page URLs.
set -euo pipefail

usage() { sed -n '5,7p' "$0" | sed 's/^# \{0,1\}//'; }

FORCE=0
ARGS=()
while (($#)); do
  case "$1" in
    -f|--force) FORCE=1 ;;
    -h|--help) sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    -*) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    *) ARGS+=("$1") ;;
  esac
  shift
done
if ((${#ARGS[@]} < 1 || ${#ARGS[@]} > 2)); then usage >&2; exit 2; fi
SRC="${ARGS[0]}"
OUT="${ARGS[1]:-ref}"

for tool in ffmpeg ffprobe python3; do
  command -v "$tool" >/dev/null || { echo "breakdown.sh needs $tool on the PATH" >&2; exit 1; }
done
if [[ -d "$OUT" && -n "$(ls -A "$OUT" 2>/dev/null)" && $FORCE -eq 0 ]]; then
  echo "$OUT already has files in it: pass -f to replace them, or choose another out dir" >&2
  exit 1
fi
mkdir -p "$OUT/frames" "$OUT/sheets" "$OUT/full"

if [[ "$SRC" =~ ^https?:// ]]; then
  rm -f "$OUT"/ref.*
  if ! { command -v yt-dlp >/dev/null && yt-dlp -q --no-progress --no-playlist \
         -f "mp4/bestvideo*+bestaudio/best" --merge-output-format mp4 -o "$OUT/ref.%(ext)s" "$SRC" 2>/dev/null; }; then
    curl -sSL --fail -A "Mozilla/5.0" -o "$OUT/ref.mp4" "$SRC"
  fi
  [[ -f "$OUT/ref.mp4" ]] || mv "$OUT"/ref.* "$OUT/ref.mp4"
else
  [[ -f "$SRC" ]] || { echo "no such file: $SRC" >&2; exit 1; }
  # Re-reading the copy already in the out dir (breakdown.sh -f ref/ref.mp4 ref) keeps it as it is.
  [[ -e "$OUT/ref.mp4" && "$SRC" -ef "$OUT/ref.mp4" ]] || cp "$SRC" "$OUT/ref.mp4"
fi
V="$OUT/ref.mp4"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
WH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$V")
HASA=$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$V" | head -1)

ffmpeg -hide_banner -i "$V" -vf "select='gt(scene,0.28)',showinfo" -an -f null - 2>&1 \
  | grep -oE 'pts_time:[0-9.]+' | cut -d: -f2 > "$OUT/cuts.txt" || true
NCUT=$(wc -l < "$OUT/cuts.txt" | tr -d ' ')

rm -f "$OUT"/frames/*.jpg "$OUT"/sheets/*.jpg "$OUT"/full/*.png
FPS24=$(python3 -c "print(24/$DUR)")
ffmpeg -hide_banner -loglevel error -y -i "$V" -vf "fps=$FPS24,scale=240:-2,tile=8x3:padding=4" -frames:v 1 "$OUT/sheet.jpg"
ffmpeg -hide_banner -loglevel error -y -i "$V" -vf "fps=1,scale=540:-2" -q:v 3 "$OUT/frames/%03d.jpg"
N=$(ls "$OUT/frames" | wc -l | tr -d ' ')
for ((S=1; S<=N; S+=32)); do
  ffmpeg -hide_banner -loglevel error -y -start_number $S -i "$OUT/frames/%03d.jpg" -frames:v 1 \
    -vf "scale=270:-2,tile=8x4:padding=4" "$OUT/sheets/sheet_$(printf %03d $S).jpg" || true
done
for T in $(python3 -c "d=$DUR; print(' '.join(str(round(t,2)) for t in sorted(set([x*5 for x in range(int(d//5)+1)]))))") $(cat "$OUT/cuts.txt" 2>/dev/null); do
  ffmpeg -hide_banner -loglevel error -y -ss "$T" -i "$V" -frames:v 1 "$OUT/full/t$(printf %06.2f "$T").png" || true
done

{
  echo "duration_s: $DUR"
  echo "video (w,h,fps): $WH"
  echo "audio: ${HASA:-none}"
  echo "hard_cuts: $NCUT  (per minute: $(python3 -c "print(round($NCUT/($DUR/60),1))"))"
} > "$OUT/info.txt"

rm -f "$OUT/transcript.txt" "$OUT/transcript.json"
if [[ -n "$HASA" ]]; then
  ffmpeg -hide_banner -loglevel error -y -i "$V" -ac 1 -ar 16000 "$OUT/audio.wav"
  for PY in "${WHISPER_PY:-}" python3; do
    [[ -n "$PY" ]] && command -v "$PY" >/dev/null 2>&1 || continue
    if "$PY" -c "import mlx_whisper" 2>/dev/null; then
      "$PY" - "$OUT/audio.wav" "$OUT" <<'PY'
import json, os, sys
import mlx_whisper
r = mlx_whisper.transcribe(sys.argv[1], path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                           condition_on_previous_text=False, word_timestamps=True)
json.dump(r, open(os.path.join(sys.argv[2], "transcript.json"), "w"))
open(os.path.join(sys.argv[2], "transcript.txt"), "w").write(
    "\n".join(f"[{s['start']:.1f}-{s['end']:.1f}] {s['text'].strip()}" for s in r["segments"]))
PY
      break
    elif "$PY" -c "import whisper" 2>/dev/null; then
      "$PY" - "$OUT/audio.wav" "$OUT" <<'PY'
import json, os, sys
import whisper
r = whisper.load_model("small").transcribe(sys.argv[1], condition_on_previous_text=False, word_timestamps=True)
json.dump(r, open(os.path.join(sys.argv[2], "transcript.json"), "w"))
open(os.path.join(sys.argv[2], "transcript.txt"), "w").write(
    "\n".join(f"[{s['start']:.1f}-{s['end']:.1f}] {s['text'].strip()}" for s in r["segments"]))
PY
      break
    fi
  done
  [[ -f "$OUT/transcript.txt" ]] || echo "(no local Whisper found: listen to the audio or read the captions off the frames)" > "$OUT/transcript.txt"
fi

python3 "$(dirname "$0")/measure.py" "$OUT" --force >/dev/null || echo "(measure.py failed: measure by hand)"
cat "$OUT/info.txt"
echo "measure: $OUT/measure.txt   sheets: $OUT/sheets/   full-res: $OUT/full/"
echo "sheet: $OUT/sheet.jpg   frames: $OUT/frames/ ($(ls "$OUT/frames" | wc -l | tr -d ' '))   transcript: $OUT/transcript.txt"
