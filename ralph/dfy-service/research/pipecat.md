# Pipecat vs ElevenLabs for the Always Answered assistant (2026-10-26)

Ralph asked: "What about pipecat for the ai receptionist." Not tested this session (no account, no deploy); facts from the pages below.

What it is: Pipecat is a free, open-source Python framework (BSD-2) from Daily for building voice agents. You pick and pay each part
yourself: speech-to-text, the AI model, the voice, and the phone line, and you host the program that joins them.

Prices (2026-10-26):
- Pipecat Cloud (Daily's hosting): $0.01 per active session minute; Daily phone (PSTN) dial-in $0.018/min, SIP $0.005/min;
  10 calls at once by default. https://www.daily.co/pricing/pipecat-cloud
- Deepgram speech-to-text listed at $0.0059/min on that page; model and voice billed by their own providers.
- ElevenLabs Agents: about $0.08/min platform rate plus the AI model, phone line separate.
  https://www.getmacha.com/blog/elevenlabs-agents-pricing-explained
- Comparisons: ElevenLabs ranked first for voice quality; Pipecat cheaper per minute but needs engineering; latency has to be
  measured on your own stack. https://futureagi.com/blog/best-ai-voice-agent-platforms-inbound-support-2026/ ,
  https://rywalker.com/research/pipecat

My estimate of the saving: Pipecat parts total roughly $0.04 to $0.07/min with a good voice vs about $0.09 to $0.12 on ElevenLabs,
so about $0.03-0.05/min. At 300 min per client that's $9-15 per client per month.

Recommendation: start on ElevenLabs (Jean's line already runs on it, tested; Ralph manages it from his phone; no server to keep
alive). Revisit Pipecat when (a) 15+ clients make the minute cost matter (~$150-225/month saved), (b) a client needs something
ElevenLabs can't do (custom booking into their software, Haitian Creole speech, WhatsApp calls through Kapso, whose calling
skill supports Pipecat), or (c) ElevenLabs prices go up. Moving later is a rebuild of the agent, not of the offer: numbers,
forwarding and the website stay.
