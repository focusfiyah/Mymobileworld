"""Video model shootout on one shot (Ralph 2026-10-14): same still, same motion prompt, one clip per model.

  python3 modelfight.py [SHOT] [MODEL ...]   default S4, every model below -> fight/<SHOT>_<model>.mp4 + preview/fight_<SHOT>.png

Prices are Kie's own rows (api.kie.ai/client/v1/model-pricing/page, read 2026-10-14), audio off, first frame = stills/<SHOT>.png.
Reuses kie.py (gate, upload, run_task, fetch), so the script gate still guards every paid call.
"""
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

os.chdir(Path(__file__).parent)
import kie

SEEDANCE = lambda m: lambda p, img, d: {"model": m, "input": {"prompt": p, "first_frame_url": img, "generate_audio": False,
                                                              "resolution": "720p", "aspect_ratio": "9:16", "duration": d}}
MODELS = {  # name: (body builder, seconds billed, USD)
    "seedance2mini": (SEEDANCE("bytedance/seedance-2-mini"), 5, 0.205),   # $0.041/s 720p (current default)
    "seedance2fast": (SEEDANCE("bytedance/seedance-2-fast"), 5, 0.62),    # $0.124/s 720p
    "seedance2": (SEEDANCE("bytedance/seedance-2"), 5, 1.025),            # $0.205/s 720p
    "hailuo23std": (lambda p, img, d: {"model": "hailuo/2-3-image-to-video-standard", "input": {
        "prompt": p, "image_url": img, "duration": "6", "resolution": "768P"}}, 6, 0.15),  # $0.15 per 6s 768p
    "hailuo02pro": (lambda p, img, d: {"model": "hailuo/02-image-to-video-pro", "input": {
        "prompt": p[:1500], "image_url": img, "prompt_optimizer": False}}, 6, 0.285),       # $0.285 per 6s 1080p, no duration field
}


def one(shot, name):
    build, secs, usd = MODELS[name]
    s = kie.SHOTS[shot]
    prompt = f"{s['video']} {kie.J['cards_block'] if s['cards'] else ''} {kie.J['video_suffix']}".strip()
    url = kie.run_task(build(prompt, kie.upload(f"stills/{shot}.png"), secs))
    if url:
        kie.fetch(url, f"fight/{shot}_{name}.mp4"); print(name, "ok", f"${usd}", flush=True)


def sheet(shot):
    files = [f for n in MODELS if (f := Path(f"fight/{shot}_{n}.mp4")).exists()]
    rows = []
    for f in files:  # 5 frames per model, one row each, label = model
        row = f"preview/_fight_{f.stem}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf",
                        "fps=1,scale=200:-2,tile=6x1,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                        f"text='{f.stem.split('_', 1)[1]}':x=6:y=6:fontsize=20:fontcolor=white:box=1:boxcolor=black@0.6",
                        "-frames:v", "1", row], check=True)
        rows.append(row)
    if rows:
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum([["-i", r] for r in rows], []), "-filter_complex",
                        f"{''.join(f'[{i}]' for i in range(len(rows)))}vstack={len(rows)}" if len(rows) > 1 else "null",
                        "-frames:v", "1", f"preview/fight_{shot}.png"], check=True)
        print("preview:", f"preview/fight_{shot}.png")


if __name__ == "__main__":
    shot = sys.argv[1] if len(sys.argv) > 1 else "S4"
    names = sys.argv[2:] or list(MODELS)
    if not Path(f"stills/{shot}.png").exists():
        sys.exit(f"stills/{shot}.png missing: run `python3 kie.py stills {shot}` first (and QC it)")
    print("quote:", f"${sum(MODELS[n][2] for n in names):.3f}", names)
    with ThreadPoolExecutor(len(names)) as ex:
        list(ex.map(lambda n: one(shot, n), names))
    sheet(shot)
