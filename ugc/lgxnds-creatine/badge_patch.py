import cv2,numpy as np
def anchor(im,y,x0,x1,below):
    rows=im[y:y+3] if below else im[y-3:y]
    R=rows.astype(np.float32).mean(0); hsv=cv2.cvtColor(rows,cv2.COLOR_BGR2HSV).astype(np.float32).mean(0)
    xs=np.arange(x0-6,x1+7); med=np.median(R[xs],0); good=[x for x in xs if np.abs(R[x]-med).max()<14 and np.abs(R[x,0]-R[x,2])<abs(med[0]-med[2])+6]
    out=np.stack([np.interp(xs,good,R[good,c]) for c in range(3)],1)
    out=cv2.blur(out[None],(7,1))[0]; return {x:out[i] for i,x in enumerate(xs)}
def fill(im,x0,x1,y0,y1):
    T=anchor(im,y0,x0,x1,False); L=im.astype(np.float32); d=L[y1-1:y1+2,x0-5:x0-2].reshape(-1,3).mean(0)-L[y0-3:y0,x0-5:x0-2].reshape(-1,3).mean(0); B={x:T[x]+d for x in T}
    for x in range(x0,x1+1):
        for y in range(y0,y1+2):
            a=(y-y0+1)/(y1-y0+3); im[y,x]=np.clip(T[x]*(1-a)+B[x]*a,0,255).astype(np.uint8)
P={'S4':(318,337,801,811),'S5':(503,529,790,805),'S7':(458,486,778,784)}
for s,r in P.items():
    im=cv2.imread(f'stills_v2/{s}_label_full.png'); fill(im,*r)
    if s=='S7':
        for y in range(779,823):
            im[y,485:490]=im[y-2:y+3,490:493].reshape(-1,3).mean(0).astype(np.uint8)
    cv2.imwrite(f'stills_v2/{s}_label_full.png',im)
