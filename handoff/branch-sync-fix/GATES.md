# Gates: branch_sync.py lists only branches with work main lacks (Ralph 2026-10-24: "Yes make the change")

OWNS: handoff/branch_sync.py, handoff/tests/test_branch_sync.py, handoff/branch-sync-fix/**

- [x] G1: test repo scenarios: a new file and a branch edit newer than main's are listed; work already on main (identical or cherry-picked), a file main edited after the branch, and a branch with no commits ahead are not
  CHECK: python3 /home/user/Mymobileworld/handoff/tests/test_branch_sync.py
  EXPECT: ALL CHECKS PASSED
  EVIDENCE: automatic-evidence=v1; definition-sha256=178ac281a0592019e22fc98b19b422ec879fa089678fcea354027dd47ac6e0e5; exit=0; EXPECT=matched; output-sha256=a73380535efd7a8733e426b77a53a812566e0e214ce48f0f6d9b1b1b756fbf7b; output-bytes=267; shell=/bin/sh; cwd=/home/user/Mymobileworld/handoff/branch-sync-fix; path=7f4fb4b02918/15 entries

- [x] G2: on the real repo none of the 25 superseded branches from today's check is listed
  CHECK: cd /home/user/Mymobileworld && python3 handoff/branch_sync.py > /tmp/claude-0/-home-user/a0368911-771c-54f4-84ac-9f59a2c75baa/scratchpad/bs.txt; python3 -c "import re;t=open('/tmp/claude-0/-home-user/a0368911-771c-54f4-84ac-9f59a2c75baa/scratchpad/bs.txt').read();old=['qqug34','df15787b','ee221bb7','gh53m6','nm4dqn','frhutz','054fb6b7','b17c4d0c','c1d3cca7','oqev7r','heater-video','cztrdu','mx5xol','db3a2861','ia89p8','5affdde5','6c8af484','e66acd3b','f62c8642','vans-shoe','0645c5bb','1f315791','aaac3716','fashion-tryon','flashlight-v2-s2'];hit=[o for o in old if re.search(r'^origin/\S*'+o,t,re.M)];print('NO_FALSE_ALARMS' if not hit and ('SYNC_OK' in t or 'not on main' in t) else hit)"
  EXPECT: NO_FALSE_ALARMS
  EVIDENCE: automatic-evidence=v1; definition-sha256=b2925600a2c81fad205aaf8346c2ac082c0795f1d8ef958e14fef303d3bde378; exit=0; EXPECT=matched; output-sha256=97031cfbc9a70b2140096372c8ef2e95cafeb4d21865a4299a4b0b01c61e6c7c; output-bytes=16; shell=/bin/sh; cwd=/home/user/Mymobileworld/handoff/branch-sync-fix; path=7f4fb4b02918/15 entries

- [x] G3: it still runs in Dayone-ai and claude-skills (prints a result line)
  CHECK: n=0; for r in Dayone-ai claude-skills; do (cd /home/user/$r && python3 /home/user/Mymobileworld/handoff/branch_sync.py | tail -1 | grep -qE 'SYNC_OK|not on main') && n=$((n+1)); done; [ $n -eq 2 ] && echo BOTH_REPOS_RAN
  EXPECT: BOTH_REPOS_RAN
  EVIDENCE: automatic-evidence=v1; definition-sha256=6389cb90114e0c2376a063e062a94a397b54f0d75b0992969bfe3864719b7a63; exit=0; EXPECT=matched; output-sha256=8d00a665628f2934f965a85d75f4fe7f5842849fd33b700db3ca609b0e4d5391; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/handoff/branch-sync-fix; path=7f4fb4b02918/15 entries
