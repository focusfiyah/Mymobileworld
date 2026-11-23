import subprocess, sys
f = sys.argv[1]; bad = 0
for t in [0.5,2,4,6,8,10,12,14,16,17]:
    d = subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",f,"-frames:v","1","-vf","crop=60:500:1020:700","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    n = sum(1 for i in range(0,len(d),3) if d[i+2]>150 and d[i+2]-d[i]>80)
    bad += n > 20
print("BUBBLE_OK" if bad == 0 else f"BUBBLE_FOUND in {bad} frames")
