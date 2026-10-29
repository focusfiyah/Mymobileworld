# Gates: Always Answered phone line (2026-10-29)

- [x] A1: The agent exists on ElevenLabs with Sarah, New York time, the transfer to Ralph and end_call
  CHECK: curl -sS https://api.elevenlabs.io/v1/convai/agents/agent_9001m6504b34ft0tqkvzndktcpjw | python3 -c "import sys,json;a=json.load(sys.stdin);p=a['conversation_config']['agent']['prompt'];ok=a['conversation_config']['tts']['voice_id']=='EXAVITQu4vr4xnSDxMaL' and p['timezone']=='America/New_York' and {'end_call','transfer_to_number'}<={t['name'] for t in p['tools']};print('AGENT_OK' if ok else 'BAD')"
  EXPECT: AGENT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=e399af5709748ac8da15bffa4411e2784a5261858be13db6da57ce0801b09149; exit=0; EXPECT=matched; output-sha256=9f843291c743b52cd90c6428d6e252706d4e547b6521988807c2496479d4c8dc; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ralph/dfy-service/launch/agent; path=7f4fb4b02918/15 entries
- [ ] A2: (516) 788-7489 is in ElevenLabs with this agent assigned
  CHECK: curl -sS https://api.elevenlabs.io/v1/convai/phone-numbers | python3 -c "import sys,json;d=json.load(sys.stdin);print('NUMBER_OK' if any(p.get('phone_number')=='+15167887489' and (p.get('assigned_agent') or {}).get('agent_id')=='agent_9001m6504b34ft0tqkvzndktcpjw' for p in d) else 'NOT_YET')"
  EXPECT: NUMBER_OK
- [ ] A3: Two test calls answered correctly (one in Ralph's hours with a transfer, one demo/after-hours path), checked in the call transcripts (manual)
- [ ] A4: The site's call buttons point to tel:+15167887489 and are live
  CHECK: curl -sS https://focusfiyah.github.io/always-answered/ | grep -c 'tel:+15167887489' | python3 -c "import sys;print('SITE_OK' if int(sys.stdin.read())>0 else 'NOT_YET')"
  EXPECT: SITE_OK
