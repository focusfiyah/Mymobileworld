"""Free fix S2 (Ralph tapped 'Free text patch' 2026-11-06): redraw 'Extra Strength' and 'Made in the USA' as text masks from
Grace's real front photo, in the still's own white, over the still's own navy (median-filtered). No pixel block pasted."""
import numpy as np
from PIL import Image, ImageFilter
a=Image.open('stills/S2_raw.png').convert('RGB'); real=Image.open('refs/real/2026-11-06 photo-786406539.jpg').convert('L')
def patch(dst, src, pad=3):
    x0,y0,x1,y1=dst; reg=a.crop((x0-pad,y0-pad,x1+pad,y1+pad))
    bg=reg.filter(ImageFilter.MedianFilter(9)).filter(ImageFilter.GaussianBlur(1.5))
    arr=np.asarray(reg).astype(float); white=np.percentile(arr.reshape(-1,3),97,axis=0)
    m=real.crop(src).resize((x1-x0,y1-y0),Image.LANCZOS)
    m=np.clip((np.asarray(m).astype(float)-110)/110,0,1)
    M=np.zeros((y1-y0+2*pad,x1-x0+2*pad)); M[pad:-pad,pad:-pad]=m
    out=np.asarray(bg).astype(float)*(1-M[...,None])+white*M[...,None]
    a.paste(Image.fromarray(out.astype('uint8')),(x0-pad,y0-pad))
patch((326,754,406,767),(335,366,491,388),pad=6)
patch((434,872,482,883),(556,597,667,613))
a.save('stills/S2.png')
