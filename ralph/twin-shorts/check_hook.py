"""G4: hook_check.py (hook whole from frame 0, held 2 s, safe zone) on both cuts. Prints HOOK_BOTH_OK."""
import subprocess
ok = 0
for f in ["final/twin_kit7_A.mp4", "final/twin_kit7_B.mp4"]:
    r = subprocess.run(["python3", "/home/user/Mymobileworld/tools/hookcheck/hook_check.py", f, "--hook", "130,395,820,250"], capture_output=True, text=True)
    print(f, r.stdout.strip()[-200:]); ok += "HOOK_OK" in r.stdout
print("HOOK_BOTH_OK" if ok == 2 else "HOOK_FAIL")
