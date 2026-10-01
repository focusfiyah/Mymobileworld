"""Recast clips (Ralph as Az, Grace as the wife) on Seedance Mini.

Reuses kie_seedance_mini's submit/poll/verify; only the prompts and reference sets change.
Usage: python kie_recast.py clip1_recast v1   |   python kie_recast.py clip2_recast v1
"""
import kie_seedance_mini as k

HEAD = (
    "Vertical 9:16 family-friendly sitcom-style comedy sketch, filmed like a realistic TikTok phone video, late at night. "
    "A married couple, both fully dressed in sleepwear, in bed. "
)
ROOM = (
    "Bedroom: dark espresso-brown wooden headboard, dusty mauve pillows, brown-grey checked duvet, window with sheer "
    "curtains, warm bedside-lamp light, faces clearly lit. "
)
CAST = (
    "Reference image 2 is the husband, Az: keep his EXACT identity - bald head, full black beard, deep-brown skin, face "
    "shape, eyes, nose, lips, heavier build; heather-grey sleep t-shirt and navy plaid pajama pants. "
    "Reference image 3 is the wife: keep her EXACT identity - face, skin tone, long black boho box braids with curly "
    "ends, thin gold chain; buttoned cream satin long-sleeve pajama top. "
    "No morphing, no facial drift. The husband is on the LEFT side of the bed and the wife on the RIGHT, the whole time. "
)
LEG = (
    "THE RESTLESS LEG MUST BE CLEARLY VISIBLE AND IT IS THE WHOLE LEG, LYING ON THE BED: Az's bare lower leg sticks out "
    "from under the duvet and rests on the mattress - never hanging over the edge of the bed. The knee bends and "
    "straightens and the calf kicks along the mattress in sudden jerks, the duvet over his knee jumping - not just the "
    "foot. "
)
AUDIO = (
    "Audio: only those spoken lines, in natural American English with light comedic timing - the wife exasperated in a "
    "female voice, the husband sleepy and apologetic in a deep male voice. Quiet room tone. No background music. No "
    "other dialogue. No on-screen text or captions."
)

k.PROMPTS["clip1_recast"] = (
    HEAD
    + "Reference image 1 shows the exact bedroom, both people asleep and the Restlex bottle on the wife's nightstand. "
    + ROOM + CAST
    + "The bottle stays on the nightstand; nobody holds it in this clip. "
    + LEG
    + "Shot 1 (0-2.5s): close-up of Az's leg on the mattress at the edge of the duvet, jerking and kicking from the knee. "
    "Shot 2 (2.5-6.5s): close-up of the wife jolting awake on her pillow, eyes snapping open, annoyed, turning toward "
    "him. She says loudly: \"Az! What the heck?! I hate when your legs start shaking like that!\" "
    "Shot 3 (6.5-10s): close-up of Az, groggy and apologetic, eyes half open. He says: "
    "\"I know, baby. I'm sorry. I can't help it.\" "
    + AUDIO
)

k.PROMPTS["clip2_recast"] = (
    HEAD
    + "Reference image 1 shows the exact bedroom, both people and how the Restlex bottle looks when she holds it. "
    + ROOM + CAST
    + "Reference image 4 is the product: a white Approved Science RESTLEX +BIOPERINE supplement bottle with a white "
    "ribbed cap and navy-striped label; a real bottle about the size of her hand, lit by the room, label readable. "
    "At the start the bottle stands on the wife's nightstand. "
    + LEG
    + "Shot 1 (0-2s): close-up of Az's leg on the mattress at the edge of the duvet, jerking and kicking from the knee "
    "again. "
    "Shot 2 (2-4s): medium close-up of the wife propped on one elbow, looking at her husband, tired and fed up. She "
    "says: \"Then take your leg pill!\" "
    "Shot 3 (4-6.5s): two-shot from beside the bed. She picks up the Restlex bottle from her nightstand and holds it up "
    "next to his face, label facing the camera. He takes it and says just once: \"Okay, okay.\" "
    "Shot 4 (6.5-10s): wide shot from the foot of the bed. After a short pause she says: \"Because I'm not losing "
    "sleep over your legs tonight.\" She turns over, facing away from him, and pulls the blanket up over her head. He "
    "lies there holding the bottle, label toward the camera, with an apologetic look, while his leg twitches on the "
    "mattress. "
    + AUDIO
)

k.CLIP_REFS["clip1_recast"] = ["wide_asleep_recast", "ralph_night", "grace_night"]
k.CLIP_REFS["clip2_recast"] = ["bottle_recast", "ralph_night", "grace_night", "product"]

if __name__ == "__main__":
    k.main()
