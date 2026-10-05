"""FUSOU V3 MOTION redo (Grace 2026-10-05: 'still pictures, needs a lot of movement, more 3D'). Every shot is a moving clip: new Seedance 3D camera
clips (clips/O*.mp4, v3ab/clips3d.py) + the approved hand clips. No photo zooms (kb), no freezes, no text. Library hooks: A = H095, B = H126.
Run from ugc/fusou-vanity:  python3 v3ab/cut_v3m.py A B  -> v3ab/out/fusou_v3A_motion.mp4, fusou_v3B_motion.mp4
QC windows (2026-10-05, frame by frame): O3 only 1.0-2.2 s, O4 only 0-1.3 s, O8 only 0-1.0 s (later the AI changes the vanity); O1 O2 O6 whole clip. O5 -> O5c = cropped above the rug (Ralph 2026-10-05: "the rug is moving, it needs to stay stationary": Seedance slid the rug ~10 px/frame over the floor)."""
import json, os, subprocess, sys
sys.path.insert(0, os.getcwd()); import cut
from cut import run, dur_of, render_shot
cut.TMP = "/tmp/claude-0/-home-user/c6ea60c5-2908-5332-9d33-6a2836015a65/scratchpad/cut3m"; os.makedirs(cut.TMP, exist_ok=True)
C = lambda f, ss=0, **o: ("clip", f"clips/{f}.mp4", ss, o)
F = None   # fill: the last shot of a line runs to the next line
GRADE = {"A": "eq=brightness=0.02:saturation=1.03",                         # bright daylight neutral
         "B": "eq=brightness=0.03:contrast=1.03:saturation=0.97,colorbalance=bs=0.03:bm=0.02"}   # bright cool (PLAYBOOK: always bright, never yellow/dark)
EDL = {  # per VO line: [(shot, seconds or F)]
 "A": [[(C("P1_O1", done=1), 2.8), (C("O6"), F)],                              # hook: hand points while the camera swings in; then pull back = whole room
       [(C("O5c"), 2.7), (C("O3", 1.0), 1.2), (C("O4"), 1.3), (C("O8"), F)],      # pain: mirror slider, drawers orbit, cabinet, door-frame wipe
       [(C("O2", 2.9, reverse=1), F)],                                         # lit mirror: rise from the stool to the mirror
       [(C("O5c", 3.0), F)],                                                    # full-length mirror
       [(C("M5a", push=(0.08, -20)), F)],                                     # hidden storage: hand opens the mirror door
       [(C("M2a", push=(0.12, 25)), 2.0), (C("M2c", push=(0.10, -25)), F)],                                       # outlets
       [(C("M4a", 0.6, push=(0.12, -20)), F)],                                                   # stool drawer
       [(C("M3a", push=(0.12, 30)), 2.0), (C("O6", 2.75), F)],                                  # five things -> all in one (room pull back)
       [(C("O2"), 2.89), (C("O1", 2.8), F)],                                   # ships: crane down to the stool, push in on the bedroom
       [(C("M6a", push=(0.10, 0)), F)]],                                                       # close
 "B": [[(C("O2", 0, reverse=1), 2.6), (C("O8"), 1.0), (C("O6"), F)],          # hook: rise to the lit mirror, door wipe, room
       [(C("P2_O5c", done=1), 3.2), (C("O3", 1.0), 1.2), (C("O4"), F)],         # pain: hand points at the full-length mirror while the camera slides
       [(C("O1", 2.9), F)],                                                    # lit mirror: push in on the bedroom
       [(C("O5c", 0, reverse=1), F)],                                           # full-length mirror (slide the other way)
       [(C("M5a", push=(0.10, 20)), F)],
       [(C("M2b", push=(0.12, -25)), 2.0), (C("M2a", 1.0, push=(0.10, 25)), F)],
       [(C("M4a", push=(0.12, 20)), F)],
       [(C("M6a", push=(0.12, -25)), 1.5), (C("O6", 0, reverse=1), F)],                          # five things: drawers, then push in from the whole room
       [(C("O3", 1.0), 1.2), (C("O2"), F)],                                    # ships
       [(C("O6", 3.6), F)]],
}


def push(f, z1=0.12, dx=0.0):
    """Free smooth camera push on a hand clip that was shot locked-off (the room never moved, so it read as a photo). Float zoom + INTER_AREA,
    no sway (Ralph: sub-pixel sway makes fine lines crawl). dx = sideways drift in px over the shot, for a little truck."""
    import cv2, numpy as np
    cap = cv2.VideoCapture(f); fr = []
    while True:
        ok, im = cap.read()
        if not ok: break
        fr.append(im)
    n = len(fr); H, W = fr[0].shape[:2]; tmp = f.replace(".mp4", "_p.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "24", "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i, im in enumerate(fr):
        e = i / max(1, n - 1); e = e * e * (3 - 2 * e) * 0.6 + e * 0.4; z = 1 + z1 * e
        M = np.float32([[z, 0, W / 2 * (1 - z) + dx * e], [0, z, H / 2 * (1 - z)]])
        ff.stdin.write(cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REFLECT).tobytes())
    ff.stdin.close(); ff.wait(); os.replace(tmp, f)


def build(v):
    VO = f"v3ab/vo/v{v}h_final.wav"; L = json.load(open(f"v3ab/vo/v{v}h_final_lines.json")); end = dur_of(VO) + 0.4
    starts, shots = [], []
    for i, line in enumerate(EDL[v]):
        t = 0.0 if i == 0 else L[i]["start"]
        for shot, d in line: starts.append(t); shots.append(shot); t += d or 0
    starts.append(end); assert all(b > a for a, b in zip(starts, starts[1:])), starts
    files = [render_shot(i, s, starts[i + 1] - starts[i], f"3m{v}") for i, s in enumerate(shots)]
    for f, s in zip(files, shots):
        if s[3].get("push"): push(f, *s[3]["push"])
    lst = f"{cut.TMP}/list{v}.txt"; open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    cat = f"{cut.TMP}/v{v}_cat.mp4"; run("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-vf", GRADE[v], "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", cat)
    vd = dur_of(cat); assert vd >= dur_of(VO) + 0.2, vd
    run("ffmpeg", "-v", "error", "-y", "-i", cat, "-i", VO, "-f", "lavfi", "-t", f"{vd}", "-i", "anoisesrc=color=brown:amplitude=0.004:sample_rate=44100", "-filter_complex",
        f"[1:a]aresample=44100,apad=whole_dur={vd}[vo];[2:a]lowpass=f=900,volume=0.5[room];[vo][room]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-t", f"{vd}", f"v3ab/out/fusou_v3{v}_motion.mp4")
    print(f"V3{v} motion: {vd:.2f}s, {len(shots)} shots", [round(s, 2) for s in starts], flush=True)


if __name__ == "__main__":
    for v in sys.argv[1:]: build(v)
