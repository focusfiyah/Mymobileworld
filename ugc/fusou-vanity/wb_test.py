"""Bedroom plate test (Ralph OK 2026-10-03, $0.09): real listing photo F (vanity in a bedroom with door + bed) extended to 9:16."""
import kie
P = ("Edit the FIRST reference image into a vertical 9:16 phone photo of the same bedroom. KEEP EVERYTHING in the first image EXACTLY as it is: the vanity (the top row of 4 cubbies, "
 "the two shelf columns with their items, the wide landscape makeup mirror, the 4 glass-top drawers, the two drawer towers, the stool, the tall mirror door on the right, the crystal knobs), "
 "the white double door on the left, the window with blinds on the right, the bed with its brown headboard and bedding at the right edge, the light oak floor, the warm light-line glow of both mirrors. "
 "Do not move, resize, add or remove anything. The blurry bands above and below the photo are empty placeholders: repaint the TOP band as the continuing beige wall with the tall white door going up to a "
 "ceiling with a thin crown moulding, and the BOTTOM band (about a third of the frame) as SHARP light oak plank floor with the same soft window light and a soft grey rug in the foreground, planks running toward the camera "
 "in the same perspective, so nothing in the frame stays blurred. It must read as a real, tidy bedroom. No people, no hands. Shot on a phone, vertical, natural daylight, realistic, no cinematic grading, no text.")
u = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": P, "image_input": [kie.upload("refs/base_F_916.jpg"), kie.upload("refs/listing_19.jpg")], "aspect_ratio": "9:16", "resolution": "1K"}})
if u: kie.fetch(u, "stills/WB.png"); print("WB ok")
