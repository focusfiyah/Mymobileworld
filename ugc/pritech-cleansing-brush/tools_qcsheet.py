"""Frame sheet per clip (0, 0.5, 1, 2, 3, 3.9 s) for QC. python3 tools_qcsheet.py S2 S3 ... -> qc/sheet_<ids>.jpg"""
import subprocess, sys
from PIL import Image, ImageDraw
T = [0, 0.5, 1, 2, 3, 3.9]; W, H = 230, 409
ids = sys.argv[1:]; sheet = Image.new('RGB', (W * len(T), H * len(ids)), 'white'); d = ImageDraw.Draw(sheet)
for r, sid in enumerate(ids):
    for c, t in enumerate(T):
        f = f'qc/{sid}_{t}.jpg'
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', str(t), '-i', f'clips/{sid}.mp4', '-frames:v', '1', f])
        sheet.paste(Image.open(f).convert('RGB').resize((W, H)), (c * W, r * H)); d.text((c * W + 4, r * H + 4), f'{sid} {t}', fill='red')
out = f"qc/sheet_{'_'.join(ids)}.jpg"; sheet.save(out, quality=82); print(out)
