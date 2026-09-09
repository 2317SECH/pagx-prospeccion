import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius=radius, fill=255)
    return m

def add_shadow(canvas, box, radius, blur=28, alpha=90):
    from PIL import ImageFilter
    x0,y0,x1,y1 = box
    sh = Image.new("RGBA", canvas.size, (0,0,0,0))
    d = ImageDraw.Draw(sh)
    d.rounded_rectangle([x0, y0+14, x1, y1+14], radius=radius, fill=(10,10,20,alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh)

def main():
    desktop_path, mobile_path, out_path, title = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    bg = (18, 16, 26, 255)
    pad = 70
    gap = 60
    label_h = 70

    desk = Image.open(desktop_path).convert("RGB")
    mob = Image.open(mobile_path).convert("RGB")

    target_h = 1500
    desk_w = round(desk.width * target_h / desk.height)
    desk_r = desk.resize((desk_w, target_h), Image.LANCZOS)

    mob_h = target_h
    mob_w = round(mob.width * mob_h / mob.height)
    mob_r = mob.resize((mob_w, mob_h), Image.LANCZOS)

    chrome_h = 40
    desk_frame_h = target_h + chrome_h
    phone_pad = 18
    phone_notch = 26
    mob_frame_w = mob_w + phone_pad*2
    mob_frame_h = mob_h + phone_pad*2 + phone_notch

    canvas_w = pad*2 + desk_w + gap + mob_frame_w
    canvas_h = pad*2 + label_h + max(desk_frame_h, mob_frame_h)
    canvas = Image.new("RGBA", (canvas_w, canvas_h), bg)
    draw = ImageDraw.Draw(canvas)

    try:
        font_lab = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 30)
        font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
    except Exception:
        font_lab = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    x = pad
    y = pad + label_h

    # Desktop browser frame
    dx0, dy0 = x, y
    dx1, dy1 = x + desk_w, y + desk_frame_h
    add_shadow(canvas, (dx0, dy0, dx1, dy1), radius=18)
    frame = Image.new("RGBA", (desk_w, desk_frame_h), (28,26,38,255))
    fd = ImageDraw.Draw(frame)
    fd.rounded_rectangle([0,0,desk_w-1,desk_frame_h-1], radius=18, fill=(28,26,38,255))
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        fd.ellipse([16+i*22, chrome_h//2-6, 16+i*22+12, chrome_h//2+6], fill=c)
    frame.paste(desk_r, (0, chrome_h), Image.new("L", desk_r.size, 255))
    mask = rounded_mask(frame.size, 18)
    canvas.paste(frame, (dx0, dy0), mask)
    draw.text((dx0, pad + label_h - 46), "DESKTOP", font=font_lab, fill=(230,225,245,255))

    # Mobile phone frame
    mx0 = dx1 + gap
    my0 = pad + label_h
    mx1 = mx0 + mob_frame_w
    my1 = my0 + mob_frame_h
    add_shadow(canvas, (mx0, my0, mx1, my1), radius=42)
    pframe = Image.new("RGBA", (mob_frame_w, mob_frame_h), (20,18,28,255))
    pd = ImageDraw.Draw(pframe)
    pd.rounded_rectangle([0,0,mob_frame_w-1,mob_frame_h-1], radius=42, fill=(10,9,14,255))
    pd.rounded_rectangle([6,6,mob_frame_w-7,mob_frame_h-7], radius=36, outline=(60,57,72,255), width=2)
    pframe.paste(mob_r, (phone_pad, phone_pad+phone_notch))
    notch_w = 110
    pd.rounded_rectangle([(mob_frame_w-notch_w)//2, 10, (mob_frame_w-notch_w)//2+notch_w, 30], radius=12, fill=(10,9,14,255))
    mask2 = rounded_mask(pframe.size, 42)
    canvas.paste(pframe, (mx0, my0), mask2)
    draw.text((mx0, pad + label_h - 46), "MOBILE", font=font_lab, fill=(230,225,245,255))

    draw.text((pad, 28), title, font=font_lab, fill=(255,255,255,255))
    draw.text((pad, 28+38), "Boceto conceptual \u00b7 PAGX Studio \u00b7 preview ~20%", font=font_tag, fill=(160,152,185,255))

    canvas.convert("RGB").save(out_path, "PNG", quality=95)
    print(out_path, canvas.size)

if __name__ == "__main__":
    main()
