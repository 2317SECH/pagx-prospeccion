#!/bin/bash
# usage: multi.sh slug1 "Title1" slug2 "Title2" ...
SP="${TEMP:-/tmp}"
cd "/c/Users/Sergio/Desktop/PAGX Studio/pagx-prospeccion"
slugs=()
while [ $# -gt 0 ]; do s=$1; t=$2; shift 2; slugs+=("$s")
python tools/cap.py "$s" && python tools/compose_preview.py "bocetos/preview/$s-desktop.png" "bocetos/preview/$s-mobile.png" "bocetos/preview/$s.png" "$t — concepto PAGX Studio" >/dev/null
python -c "from PIL import Image;print('$s',Image.open('bocetos/preview/$s-mobile.png').size[0])"
done
python -c "
from PIL import Image;import sys
ims=[Image.open('bocetos/preview/'+s+'.png') for s in sys.argv[1:]]
ims=[im.resize((int(im.width*1100/im.height),1100)) for im in ims]
W=sum(i.width for i in ims);S=Image.new('RGB',(W,1100));x=0
for i in ims:S.paste(i,(x,0));x+=i.width
S.save('$SP/rev.png')" "${slugs[@]}"
