import subprocess, sys
f = sys.argv[1]
r = subprocess.run(["ffmpeg","-v","info","-i",f,"-vf","freezedetect=n=0.003:d=0.5","-an","-f","null","-"],capture_output=True,text=True).stderr
print("FREEZES_NONE" if "freeze_start" not in r else "FREEZES_FOUND")
print("NOTEXT_OK" if "drawtext" not in open("cut.py").read() else "TEXT_FOUND")
