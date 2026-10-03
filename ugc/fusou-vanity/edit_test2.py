"""Edit-the-real-photo test: base = real listing photo A padded to 9:16 (free), model fills the padding + adds the hand."""
import json
import kie
J = kie.J
prompt = ("Edit the FIRST reference image into a vertical 9:16 phone photo. KEEP THE VANITY EXACTLY AS IT IS in the first "
 "image: do not redraw, move, resize or change anything on it: the same top row of 4 cubbies, the same two shelf columns "
 "with the same items, the same wide landscape makeup mirror, the same 4 glass-top drawers, the same two drawer towers, "
 "the same stool, the same tall mirror door on the right, the same crystal knobs. Only do three things: (1) the blurry bands above and below the photo are empty placeholders: repaint the TOP band as continuing beige wall and "
 "the BOTTOM band (about a quarter of the frame) as SHARP light oak plank floor with the same soft sunlight patches, planks "
 "running toward the camera in the same perspective, so nothing in the frame stays blurred; (2) switch both LED light lines "
 "(the makeup mirror and the tall mirror door) on to a warm white glow, like the second reference image; (3) add ONE small "
 "hand reaching up from the bottom left of the frame, only the index finger extended and pressing the small round touch "
 "button at the lower left corner of the makeup mirror's glass, the other fingers curled; the hand stays SMALL, no bigger "
 "than a fifth of the frame height, and covers almost none of the vanity. "
 + J["blocks"]["hand"] + " The third and fourth reference images show the hands. Camera stays straight-on, daylight, nothing else changes. "
 + J["blocks"]["phone"])
refs = ["refs/base_A_916.jpg", "refs/vanity_lit_room.jpg"] + kie.HAND_REFS
body = {"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in refs],
                                              "aspect_ratio": "9:16", "resolution": "1K"}}
url = kie.run_task(body)
if url:
    kie.fetch(url, "stills/EDIT_TEST2.png"); print("EDIT_TEST2 ok")
