"""Edit the approved cross-body S6 (stills_raw/S6_r3.png): move only the roller ball onto the elbow tip. $0.09."""
import kie
base = kie.upload("stills_raw/S6_r3.png"); ref = kie.upload("refs/bottle_front.png")
prompt = ("Edit the FIRST image only. Keep everything exactly the same: the woman, her mauve tee, her pose with the right arm reaching across "
          "her body, both hands, the nails, the bedroom, the lighting and framing. Change only this: her right hand moves the roll-on a little "
          "so the pink rose quartz ball presses right on the bony tip of her left elbow (the point at the back of the bent elbow), not on the "
          "side or the inner arm. The bottle and its label must look exactly like the bottle in the SECOND image. No face, no new objects, no text.")
url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [base, ref], "aspect_ratio": "9:16", "resolution": "1K"}})
if url: kie.fetch(url, "stills/S6.png"); print("S6 edit ok")
else: print("S6 edit FAILED")
