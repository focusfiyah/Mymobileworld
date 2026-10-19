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
