"""Plan v2 step 3 (Ralph OK 2026-10-03): 10 Seedance Mini clips, 4 s, $0.164 each = $1.64 (M6a = free ffmpeg push-in).

  python3 step3.py ID ...   -> clips/<ID>_raw.mp4 + clips/<ID>.mp4 (pasted back onto refs/base_<still>.png; B1 clips have no product, no paste-back)
"""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import kie
LOCK = ("Locked-off camera on a tripod: the camera does NOT move, no zoom, no push-in, no pan, no shake; the frame stays exactly the same for the "
        "whole clip. ")
HAND = (" Only the hand is in frame: the wrist stays at the frame edge, the forearm never enters. Fingers stay anatomically correct (five fingers), "
        "long almond nails with glossy dusty mauve polish and thin white French tips. Movements are slow and natural. ")
KEEP = "Nothing else moves or changes: every drawer, knob, shelf item and the wall stay exactly the same. No sound. No on-screen text."
# id: (still, action, pasteback args)
CLIPS = {
 "M2a": ("M2", "The index fingertip moves a little closer and points at the two USB ports, then at the outlet below, then holds still.", []),
 "M2b": ("M2", "The fingers take hold of the black plug in the top outlet and press it firmly in, then let go and the hand rests.", ["--ai-box", "0,560,220,1000"]),
 "M2c": ("M2", "The index fingertip taps the two USB ports once, then moves down and points at the outlet below, then holds.", []),
 "M3a": ("M3", "The thumb and index finger pick one lipstick out of the small lipstick tray on the glass top and lift it up a few centimetres, then hold it.",
         ["--ai-box", "290,190,540,430"]),
 "M3b": ("M3", "The index fingertip taps the clear glass desk top twice, right above the open top drawer, then the hand rests on the glass.", []),
 "M3c": ("M3", "The fingers pick up one lipstick from the tray, then set it back down neatly in the tray, and the hand lifts away slightly.",
         ["--ai-box", "290,190,540,430"]),
 "M4a": ("M4", "The fingertips hold the crystal knob and slowly pull the stool's top drawer open a few inches, then stop.", ["--ai-box", "110,540,600,960"]),
 "M5a": ("M5", "The fingertips grip the left edge of the tall mirror door and pull it open only a few inches, slowly, then stop.", ["--ai-box", "240,40,660,1280"]),
 "B1a": ("B1", "Both hands slowly sweep the messy makeup together into one pile in the middle of the counter.", None),
 "B1b": ("B1", "Both hands gather the makeup into a neat pile, then straighten the lipsticks into a row.", None),
}


def clip(cid):
    sid, action, pb = CLIPS[cid]
    prompt = LOCK + action + HAND + (KEEP if sid != "B1" else "The counter, sink and wall stay the same. No sound. No on-screen text. No brand names.")
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": kie.upload(f"stills/{sid}.png"),
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 4}})
    if not url: return print(cid, "FAILED (failed Kie tasks cost $0)")
    kie.fetch(url, f"clips/{cid}_raw.mp4")
    if pb is None:
        subprocess.run(["cp", f"clips/{cid}_raw.mp4", f"clips/{cid}.mp4"])
    else:
        r = subprocess.run(["python3", "pasteback.py", "video", f"refs/base_{sid}.png", f"clips/{cid}_raw.mp4", f"clips/{cid}.mp4", "--no-light"] + pb,
                           capture_output=True, text=True)
        print(cid, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:])
    print(cid, "ok", flush=True)


if __name__ == "__main__":
    ids = sys.argv[1:]
    if not ids: sys.exit("name the clip ids (ask Ralph before any paid call)")
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(clip, ids))
