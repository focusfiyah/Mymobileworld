"""One Nano Banana Pro image edit on Kie ($0.09): python3 edit.py IN OUT "instruction". Uses kie.py's gate, upload and logging."""
import sys
import kie
src, out, instr = sys.argv[1:4]
url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": instr, "image_input": [kie.upload(src)],
                                                          "aspect_ratio": "9:16", "resolution": "1K"}})
if url:
    kie.fetch(url, out); print("edit ok", out)
