# LGXNDS creatine redo (2026-10-18), phase 1: script + model test plan

- [ ] G1: script v2 has no "girls" and no "the label says"
  CHECK: python3 -c "import re,sys;t=open('research/v2_script.txt').read().lower();sys.exit(1 if re.search(r'girls|label says',t) else 0);print('CLEAN')"
  EXPECT: ^$|CLEAN
- [ ] G2: script gate passes on v2
  CHECK: cd ../.. && python3 grace/gate.py ugc/lgxnds-creatine
  EXPECT: GATE OK
- [ ] G3: readability grade <= 6
  CHECK: python3 -c "import re;g=float(re.search(r'Kincaid\): ([0-9.]+)',open('research/v2_readability.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'GRADE_BAD')"
  EXPECT: GRADE_OK
- [ ] G4: bake-off runner exists and goes through the gate (kie.run_task)
  CHECK: python3 -c "t=open('modeltest/run.py').read();print('RUNNER_OK' if 'kie.run_task' in t and 'last_frame_url' in t else 'NO')"
  EXPECT: RUNNER_OK
- [ ] G5: plan reply sent to Ralph with the $0.705 test cost (manual)
