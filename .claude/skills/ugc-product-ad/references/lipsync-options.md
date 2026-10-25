# Lip sync options (Ralph, 2026-10-18)

Goal: a mouth that matches the voice and looks natural on the real face.

1. **Default: ElevenLabs voice + the existing Kie lip sync route** (`scripts/kie_lipsync.py`, `persona_lipsync.py`;
   prices in `persona-per-shot.md`). Always try this first.
2. **Fallback: Fal.ai `minimax/h3-max/lip-sync/image-to-video`.** Use it only when Ralph says the default sync does not
   look the way he likes. Same voice track, same ElevenLabs audio; only the mouth step changes.

Rules for the fallback:
- Ask Ralph before the run with the exact cost (Fal bills per generation); test ONE clip first, run every QC check on it
  (mouth on every frame, face edges at 2x, mux the original mp3 back on afterwards), then the rest.
- Credential: a Fal key stored as an environment network secret / variable (Ralph adds it; never ask him to paste a key
  in chat). Test the endpoint with one small real request in the session before relying on it, and report what it returned.
- Applies to every repo (Grace, Day One AI, personal). Record the model and the cost in the job README.

## Kie talking-avatar models: one portrait + the voice track, no clip first (untested, 2026-10-24)

The default route makes a Seedance clip of the face and then syncs the mouth onto it (about $0.41 for a 5 s line).
These Kie models skip the clip: they animate one still straight from the audio, so a talking-head line costs less and
the face can't drift between the clip and the sync. **None has been run on a job yet.** Offer one only for a
talking-head shot with no hand or product action (the still can't make the hand do anything), ask Ralph first with
the cost for the line's audio length, test ONE line and QC it like any face shot before using it for the rest.
Source of the lead: github.com/Autom8AI/Open-Higgsfield-AI (Ralph, 2026-10-24); fields come from docs.kie.ai,
prices from kie.ai/pricing, both checked 2026-10-24.

| Kie model | $ per s of audio | 5 s line | Output | Limits and fields to know |
| :-- | :-- | :-- | :-- | :-- |
| `kling/ai-avatar-standard` | 0.04 | $0.20 | 720p | audio up to 5 min; `prompt` required (expression, movement, camera) |
| `kling/ai-avatar-pro` | 0.08 | $0.40 | 1080p | same as Standard, more facial detail |
| `omnihuman-2-0` | 0.07 | $0.35 | 720p | audio 4-300 s, wav/mp3; `image_urls` = a one-image list; set `enable_watermark: false` (default true) |
| `omnihuman-1-5` | 0.135 | $0.68 | 720 / 1080 | audio under 60 s, best at 15 s or less; upper-body motion |
| `infinitalk/from-audio` | 0.015 (480p), 0.06 (720p) | $0.08 / $0.30 | 480p / 720p | up to 15 s; `prompt` required |
| `wan/2-2-a14b-speech-to-video-turbo` | 0.06 / 0.09 / 0.12 | $0.30 to $0.60 | 480p / 580p / 720p | `prompt` required; has `negative_prompt` and `guidance_scale` (motion strength) |

Field names differ per model (`image_url` vs `image_urls`), and Kie ignores a wrong one without an error, so
`grace/gate.py` refuses any body whose input has a field the model's doc does not list (`grace/kie_fields.py`).
These models have no `duration` input: the runner passes `usd=<audio seconds> x rate` to `start_task()`.
