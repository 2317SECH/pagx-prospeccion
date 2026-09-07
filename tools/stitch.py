import sys, json
from PIL import Image
out = sys.argv[1]
ih  = float(sys.argv[2])
items = json.loads(sys.argv[3])
items = sorted(((p,int(y)) for p,y in items), key=lambda t:t[1])
# drop exact-duplicate trailing scrollY
dd=[]
for p,y in items:
    if dd and dd[-1][1]==y: continue
    dd.append((p,y))
imgs=[(Image.open(p).convert("RGB"), y) for p,y in dd]
w=imgs[0][0].width
last_im,last_y=imgs[-1]
H=round(last_y*(last_im.height/ih))+last_im.height
canvas=Image.new("RGB",(w,H),(15,17,22))
for im,y in imgs:
    s=im.height/ih
    canvas.paste(im,(0,round(y*s)))
canvas.save(out,"PNG")
print(out, canvas.size)
