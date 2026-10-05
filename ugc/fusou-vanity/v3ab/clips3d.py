"""FUSOU V3 motion redo (Grace 2026-10-05: 'still pictures, needs a lot of movement, more 3D'). Hand-free Seedance 2.0 Mini 3D camera clips
from real-photo 9:16 plates (v3ab/plates/O*.png). $0.041/s, 5 s = $0.205 each. Ask Ralph before every run.
Run from ugc/fusou-vanity:  python3 v3ab/clips3d.py O1   -> clips/O1.mp4"""
import os, sys
sys.path.insert(0, "v3ab"); import kie_ab as kie   # gated on v3ab/checklist.json, logs to v3ab/kie_log.json
LOCK = ("The white vanity is a real product and stays EXACTLY as in the first frame for the whole clip: same drawers, knobs, mirrors, LED rings, shelves, "
        "items on the shelves, same size and proportions; nothing appears, disappears or changes. Only the camera moves; nothing in the room moves. "
        "No people, no hands, no arms anywhere in the frame. Bright natural daylight, the lights stay as they are, exposure stays constant. "
        "Smooth gimbal camera move, real 3D parallax (near things pass faster than far things), no zoom-only move, no cuts. No sound, no on-screen text.")
MOVES = {
    "O1": "The camera glides on a slow curved arc to the left around the vanity while moving forward toward it, about fifteen degrees of orbit, the rug and the bed edge in the foreground sliding past faster than the vanity.",
    "O2": "The camera cranes smoothly DOWN from the lit makeup mirror to the stool and lower drawers, staying centred on the vanity, slight forward drift.",
    "O3": "The camera orbits slowly to the right around the corner of the vanity, keeping the open drawers and the stool in the centre, the drawers showing depth as the angle changes.",
    "O4": "The camera trucks slowly sideways to the right past the open cabinet, the cabinet door edge in front sliding past faster than the shelves behind it.",
    "O5": "The camera trucks low and slowly to the left past the tall full-length mirror, close to the floor. The rug and the floor are fixed to each other and never slide; only the camera moves.",
    "O6": "The camera cranes up and pulls back slowly from the rug to show the whole bedroom with the vanity, the floor and rug receding underneath.",
    "O8": "The camera arcs slowly to the right from the double doors toward the vanity, about fifteen degrees of orbit, the door frame in front sliding past faster than the vanity.",
}


def clip(sid, dur=5):
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {
        "prompt": f"{MOVES[sid]} {LOCK}", "first_frame_url": kie.upload(f"v3ab/plates/{sid}.png"), "generate_audio": False,
        "resolution": "720p", "aspect_ratio": "9:16", "duration": dur}})
    if url: kie.fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    ids = sys.argv[1:]
    if not ids: sys.exit("name the clip ids (ask Ralph before any paid call)")
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(clip, ids))
