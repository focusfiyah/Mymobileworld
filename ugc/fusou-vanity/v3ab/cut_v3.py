"""FUSOU V3 (Grace's 'ONE piece of furniture' script), two cuts on the SAME voiceover (free). Run from ugc/fusou-vanity:  python3 v3ab/cut_v3.py A B
-> v3ab/out/fusou_v3A.mp4 (hook = wide pointing hand), v3ab/out/fusou_v3B.mp4 (hook = lit mirror push-in, pointing hand on the lit-mirror line).
Every shot sits on the real Grace B word timings. No dark room, no tap shot, no hand sweep, no 3-boxes card, no tick sounds (v3ab/REMOVED.md)."""
import json, os, subprocess, sys
sys.path.insert(0, os.getcwd()); import cut
from cut import run, dur_of, render_shot, FPS, WIDE, CAB, CAB2, DOOR, PSTRIP, M2CROP
cut.TMP = "/tmp/claude-0/-home-user/9c718d1b-29a5-5a63-b8f9-864e00013653/scratchpad/cut3"; os.makedirs(cut.TMP, exist_ok=True); os.makedirs("v3ab/out", exist_ok=True)
VO = "v3ab/vo/vA_final.wav"; LINES = json.load(open("v3ab/vo/vA_final_lines.json")); L = [l["start"] for l in LINES]   # line starts
BEDW = "stills/BEDROOM_WIDE_2x.png"                                                           # real bedroom wide from the approved Drive Video 2 (doors, bed, rug), 2x
BED = (BEDW, (0, 0, 1440, 2560)); MIRROR = (BEDW, (120, 660, 920, 2082)); RIGHT = (BEDW, (640, 700, 1440, 2122)); LEFT = (BEDW, (0, 700, 800, 2122))
P1, P2 = "clips/P1_bed.mp4", "clips/P2_bed.mp4"                                                # free pointing-hand clips on the bedroom wide (v3ab/hand_bedroom.py)


def edl(v):
    if v == "A":      # hook = wide bedroom with the pointing hand; hands close on mirror door / outlet / stool drawer
        return [(0, ("clip", P1, 0, {"done": 1})), (L[1], ("kb",) + BED + ({},)), (L[1] + 3.13, ("kb",) + CAB + ({},)), (L[2], ("kb",) + MIRROR + ({},)),
                (L[3], ("clip", P2, 0, {"done": 1})),                                              # full-length mirror: hand points from the right edge
                (L[3] + 1.6, ("clip", "clips/M5a.mp4", 0, {})),                                     # mirror door opens (hidden storage)
                (L[5], ("clip", "clips/M2a.mp4", 0, {"crop": M2CROP})),                             # outlets
                (L[6] - 0.13, ("clip", "clips/M4a.mp4", 0.6, {})),                                  # stool drawer
                (L[7], ("kb",) + CAB2 + ({},)), (L[7] + 2.67, ("kb",) + BED + ({"pull": 1},)),      # five things -> all in one
                (L[8], ("kb",) + RIGHT + ({},)), (L[8] + 4.03, ("kb",) + BED + ({},))]              # ships in three boxes (cabinet, window, bed edge), close
    # B: different order and sources: opens on the lit mirror, pointing hand on the pain line (4 s), real-photo pushes for storage/outlets, drawer hands later, bedroom left side + wide close
    return [(0, ("kb",) + MIRROR + ({},)), (L[1], ("clip", P1, 0, {"done": 1})), (L[1] + 4.0, ("kb",) + CAB + ({},)),
            (L[2], ("kb",) + BED + ({"pull": 1},)),                                                 # lit mirror line: pull back from the mirror to the whole bedroom
            (L[3], ("kb",) + DOOR + ({},)),                                                         # full-length mirror (real photo push)
            (L[4] - 0.12, ("kb",) + CAB2 + ({},)),                                                  # hidden storage (real photo, bags)
            (L[5], ("kb",) + PSTRIP + ({},)),                                                       # outlets (real listing photo)
            (L[6] - 0.13, ("clip", "clips/M4a.mp4", 0, {})),                                        # stool drawer opens
            (L[7], ("clip", "clips/M3a.mp4", 0, {})),                                               # drawers + lipsticks: five things in one
            (L[7] + 4.04, ("kb",) + LEFT + ({},)),                                                  # ships in three boxes: door, left drawers, rug
            (L[8] + 4.03, ("kb",) + BED + ({},))]                                                   # close push-in on the whole bedroom


def build(v):
    shots = edl(v); n = f"3{v}"; end = dur_of(VO) + 0.4; starts = [s for s, _ in shots] + [end]
    assert all(b > a for a, b in zip(starts, starts[1:])), starts
    files = [render_shot(i, shot, starts[i + 1] - starts[i], n) for i, (_, shot) in enumerate(shots)]
    lst = f"{cut.TMP}/list{n}.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    cat = f"{cut.TMP}/v{n}_cat.mp4"; run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", cat)
    vd = dur_of(cat); assert vd >= dur_of(VO) + 0.2, vd
    run("ffmpeg", "-v", "error", "-y", "-i", cat, "-i", VO, "-f", "lavfi", "-t", f"{vd}", "-i", "anoisesrc=color=brown:amplitude=0.004:sample_rate=44100", "-filter_complex",
        f"[1:a]aresample=44100,apad=whole_dur={vd}[vo];[2:a]lowpass=f=900,volume=0.5[room];[vo][room]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{vd}", f"v3ab/out/fusou_v3{v}.mp4")
    print(f"V3{v}: {vd:.2f}s, {len(shots)} shots -> v3ab/out/fusou_v3{v}.mp4", [round(s, 2) for s in starts], flush=True)


if __name__ == "__main__":
    for v in sys.argv[1:]: build(v)
