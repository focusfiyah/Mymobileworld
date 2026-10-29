# Gates: Always Answered phone line (2026-10-29)

- [ ] A1: The agent exists on ElevenLabs with Sarah, New York time, the transfer to Ralph and end_call
  CHECK: curl -sS https://api.elevenlabs.io/v1/convai/agents/agent_9001m6504b34ft0tqkvzndktcpjw | python3 -c "import sys,json;a=json.load(sys.stdin);p=a['conversation_config']['agent']['prompt'];ok=a['conversation_config']['tts']['voice_id']=='EXAVITQu4vr4xnSDxMaL' and p['timezone']=='America/New_York' and {'end_call','transfer_to_number'}<={t['name'] for t in p['tools']};print('AGENT_OK' if ok else 'BAD')"
  EXPECT: AGENT_OK
- [ ] A2: (516) 788-7489 is in ElevenLabs with this agent assigned
  CHECK: curl -sS https://api.elevenlabs.io/v1/convai/phone-numbers | python3 -c "import sys,json;d=json.load(sys.stdin);print('NUMBER_OK' if any(p.get('phone_number')=='+15167887489' and (p.get('assigned_agent') or {}).get('agent_id')=='agent_9001m6504b34ft0tqkvzndktcpjw' for p in d) else 'NOT_YET')"
  EXPECT: NUMBER_OK
- [ ] A3: Two test calls answered correctly (one in Ralph's hours with a transfer, one demo/after-hours path), checked in the call transcripts (manual)
- [ ] A4: The site's call buttons point to tel:+15167887489 and are live
  CHECK: curl -sS https://focusfiyah.github.io/always-answered/ | grep -c 'tel:+15167887489' | python3 -c "import sys;print('SITE_OK' if int(sys.stdin.read())>0 else 'NOT_YET')"
  EXPECT: SITE_OK
