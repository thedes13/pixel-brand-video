"""把任意 Logo 產生三段由粗到細的像素版（logo_px1~3.png），給影片結尾「Logo 轉 8-bit」用。
用法：python pixelate_logo.py logo.png            # 輸出到同一個資料夾
需求：pip install pillow
"""
import sys, os
from PIL import Image

src = sys.argv[1] if len(sys.argv) > 1 else "logo.png"
out_dir = os.path.dirname(os.path.abspath(src))
im = Image.open(src).convert("RGBA")
W, H = im.size
for name, block in [("logo_px1", 28), ("logo_px2", 16), ("logo_px3", 8)]:
    s = im.resize((max(W // block, 1), max(H // block, 1)), Image.BILINEAR)
    px = s.load()
    for y in range(s.size[1]):                      # 透明邊緣改成硬邊，才像像素圖
        for x in range(s.size[0]):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255 if a > 110 else 0)
    if name == "logo_px3":                          # 最細的一段再減色，更有 8-bit 味道
        rgb = s.convert("RGB").quantize(12).convert("RGB")
        rgb.putalpha(s.getchannel("A"))
        s = rgb
    s.resize(im.size, Image.NEAREST).save(os.path.join(out_dir, name + ".png"))
    print("saved", name + ".png")
