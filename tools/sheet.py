import sys,os,urllib.request
from PIL import Image,ImageDraw
ids=sys.argv[2:];out=sys.argv[1];th=[]
for i in ids:
    p=f"u/{i}.jpg"
    if not os.path.exists(p):
        try:
            urllib.request.urlretrieve(f"https://images.unsplash.com/photo-{i}?w=360&h=240&fit=crop&q=60",p)
        except Exception as e:
            print("FAIL",i);continue
    try: th.append((i,Image.open(p).convert("RGB").resize((360,240))))
    except: print("BAD",i)
cols=4;rows=(len(th)+cols-1)//cols
S=Image.new("RGB",(cols*360,rows*262),"white");d=ImageDraw.Draw(S)
for k,(i,im) in enumerate(th):
    x,y=(k%cols)*360,(k//cols)*262;S.paste(im,(x,y));d.text((x+4,y+244),f"{k}:{i}",fill="black")
S.save(out);print("ok",len(th))
