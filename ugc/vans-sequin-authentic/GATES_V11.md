# Gates: Vans sequin V11, night + phone flash (Grace's request 2026-10-21)

OWNS: ugc/vans-sequin-authentic/**

Scope: ONE new 7-15 s vertical AI video of the real Vans Premium Authentic sequin checkerboard at night with the phone flash on, all-new footage (no V1-V10 clips), product shots on Google Omni (product lock), approved by Ralph, delivered to the Vans Drive folder.

- [ ] G1: Script gate passes on the current script (V11 section, proofs refreshed)
  CHECK: python3 grace/gate.py ugc/vans-sequin-authentic
  EXPECT: GATE OK
  CWD: ../..

- [x] G2: Ralph approved the one-message V11 plan + total cost before any paid call (his words quoted in README)
  EVIDENCE: Ralph 2026-10-21 "Outfit ok, free on Gemini, no sound she will use music" (stills $0 via his Gemini app, Omni clips $1.52, music-only)

- [ ] G3: Test still V11S1 QC'd at full size + 2x (night flash look, real shoe details, tab, anklet, feet parallel) before the other 3 stills; all 4 stills QC'd before any clip is paid for

- [ ] G4: Riskiest clip (V11S2 walk) made and QC'd at 2x on several frames (tab, heel label, shoe count, no flip, no light effects) before the other clips

- [ ] G5: V11 final exists, 7-15 s, 1080x1920
  CHECK: python3 -c "import json,subprocess;d=json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height:format=duration','-of','json','out/V11_final.mp4'],capture_output=True,text=True).stdout);s=d['streams'][0];t=float(d['format']['duration']);print('V11_OK' if (s['width'],s['height'])==(1080,1920) and 7<=t<=15 else 'BAD',t)"
  EXPECT: V11_OK
  CWD: .

- [ ] G6: Cut gate passes (coach compare V11 vs the #sparklyshoes reference done, no text overlay)
  CHECK: python3 grace/gate.py ugc/vans-sequin-authentic --stage cut
  EXPECT: GATE OK
  CWD: ../..

- [ ] G7: V11 checked against REMOVED.md and frame by frame (no shimmer, shoe never changes, max 2 shoes, no sparkle effects, feet parallel), ai_finish applied last

- [ ] G8: V11 on the Artifact review page, Ralph emailed + pushed, Ralph approved

- [ ] G9: V11 in Drive "Vans sequin (Grace)" as "CURRENT - Vans V11.mp4", link in README; Kie + Omni spend vs quote recorded
