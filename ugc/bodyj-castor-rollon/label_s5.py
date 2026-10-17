"""Paste the real BodyJ label (refs/bottle_front.png) onto the S5 bottle, free. Corners in the 768x1365 crop."""
import sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
A,B,C,D=[tuple(map(int,p.split(','))) for p in sys.argv[1:5]]  # cap-left, cap-right, roller-right, roller-left
ref=Image.open('refs/bottle_front.png').convert('RGB')
lab=ref.crop((62,316,300,706)); w,h=lab.size
src=[(0,0),(w,0),(w,h),(0,h)]
dst=[C,D,A,B]
M=[];b=[]
for (x,y),(u,v) in zip(dst,src):
    M.append([x,y,1,0,0,0,-u*x,-u*y]); b.append(u); M.append([0,0,0,x,y,1,-v*x,-v*y]); b.append(v)
co=np.linalg.solve(np.array(M,float),np.array(b,float))
base=Image.open(sys.argv[5]).convert('RGB')
warped=lab.transform(base.size,Image.PERSPECTIVE,tuple(co),Image.BICUBIC)
mask=Image.new('L',base.size,0); ImageDraw.Draw(mask).polygon(dst,fill=255); mask=mask.filter(ImageFilter.GaussianBlur(1.5))
a=np.asarray(base).astype(int); r,g,bb=a[...,0],a[...,1],a[...,2]
skin=((r>120)&(r-bb>35)&(r-g>12)&(g>70)).astype(np.uint8)*255
skin=Image.fromarray(skin).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
m=np.clip(np.asarray(mask).astype(float)-np.asarray(skin).astype(float),0,255)
lum=np.asarray(base.convert('L').filter(ImageFilter.GaussianBlur(12))).astype(float)
shade=np.clip(lum/max(1,np.percentile(lum[np.asarray(mask)>200],90)),0.6,1.05)[...,None]
out=a*(1-m[...,None]/255)+np.clip(np.asarray(warped).astype(float)*shade,0,255)*(m[...,None]/255)
o=Image.fromarray(out.astype('uint8')); o.save(sys.argv[6]); o.crop((60,180,620,820)).save('/tmp/claude-0/s5paste_zoom.png')
