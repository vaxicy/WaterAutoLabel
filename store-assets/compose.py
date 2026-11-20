# -*- coding: utf-8 -*-
"""WaterAutoLabel Nexus 素材：header 1300x372 + gallery 中英两版 1920x1080。"""
import os
import io
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
CAP = r"C:\Users\16704\AppData\Local\CodeBuddyExtension\Data\29778d92-91e1-4369-8953-0334b572f040\VSCode\29778d92-91e1-4369-8953-0334b572f040\history\fc17b2b10a8cdeb8b8a77ff31f062cd8\30f8602e56984219a1ca49f6500f2f67\assets\image.b5d8c40b4e.png"

BG = (18, 21, 28)
PANEL = (28, 32, 42)
BORDER = (44, 50, 64)
WHITE = (238, 242, 248)
MUTED = (150, 162, 180)
DIM = (104, 116, 136)
CYAN = (86, 200, 214)
RED = (214, 74, 82)


def font(size, bold=False, cn=False):
    name = ("msyhbd.ttc" if bold else "msyh.ttc") if cn else \
           ("segoeuib.ttf" if bold else "segoeui.ttf")
    path = os.path.join("C:\\Windows\\Fonts", name)
    if not os.path.exists(path):
        path = os.path.join("C:\\Windows\\Fonts", "arialbd.ttf" if bold else "arial.ttf")
    return ImageFont.truetype(path, size)


def text_fit(d, x, y, txt, size, max_w, fill, bold=False, cn=False):
    f = font(size, bold, cn)
    b = d.textbbox((0, 0), txt, font=f)
    w = b[2] - b[0]
    while w > max_w and size > 12:
        size -= 1
        f = font(size, bold, cn)
        b = d.textbbox((0, 0), txt, font=f)
        w = b[2] - b[0]
    assert w <= max_w, "text overflow: %s (%d>%d)" % (txt, w, max_w)
    d.text((x, y), txt, font=f, fill=fill)
    return size


def save(im, name):
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    with open(os.path.join(OUT, name), "wb") as f:
        f.write(buf.getvalue())
    print("saved", name, im.size)


def crop_screenshot(cap, sw, sh, focus_y=0.5):
    """等比裁切截图填满 sw x sh，focus_y 控制纵向裁切位置比例。"""
    cw, ch = cap.size
    scale = max(sw / cw, sh / ch)
    nw, nh = int(cw * scale), int(ch * scale)
    im = cap.resize((nw, nh), Image.LANCZOS)
    left = (nw - sw) // 2
    top = max(0, min(nh - sh, int((nh - sh) * focus_y)))
    return im.crop((left, top, left + sw, top + sh))


def compose_header(cap):
    W, H = 1300, 372
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 7, H - 1), fill=CYAN)

    SW = 880
    crop = crop_screenshot(cap, SW, H, focus_y=0.5)
    sx = W - SW
    im.paste(crop, (sx, 0))
    d.rectangle((sx - 2, 0, sx, H - 1), fill=BORDER)

    tx = 40
    d.text((tx, 70), "Water Auto", font=font(58, True), fill=WHITE)
    d.text((tx, 146), "Label", font=font(58, True), fill=CYAN)
    text_fit(d, tx + 2, 224, "TRUE WATER QUALITY, AUTOMATICALLY", 18, sx - tx - 40, MUTED, bold=True)
    text_fit(d, tx + 2, 264, "Probably Stolen  /  native mod  /  no MelonLoader", 14, sx - tx - 40, DIM)
    text_fit(d, tx + 2, 306, "Purified water shows its real grade", 15, sx - tx - 44, MUTED)
    assert tx + 375 < sx, "text overlaps screenshot"
    save(im, "header.png")


T_EN = {
    "top_sub": "True Water Quality for Probably Stolen",
    "glance": "AT A GLANCE",
    "f1": "Every water container displays its REAL quality",
    "f2": "based on actual purity - no manual labeling needed",
    "f3": "Pure / high-quality / base / ghost / rust / gutterflow",
    "change": "ONLY UPDATES ON CHANGE",
    "c1": "Manual labels are kept while purity stays the same.",
    "c2": "Purify or contaminate the water, and the label syncs.",
    "fraud": "WORKS WITH FRAUDDETECTION",
    "fr1": "Label and true quality stay consistent. Once synced,",
    "fr2": "no fake-vs-real difference is shown for that water.",
    "install": "INSTALL",
    "ins": ("Unzip, copy WaterAutoLabel into the game's Mods folder",
            "Enable in the Mods menu and restart"),
    "foot": "Toggle in mod settings. Native loader, no MelonLoader.",
}

T_ZH = {
    "top_sub": "深空当铺（Probably Stolen）水质自动标注模组",
    "glance": "一眼看懂",
    "f1": "每个水容器都按真实纯度显示水质",
    "f2": "不用再拿标签机手动贴",
    "f3": "纯净水 / 优质水 / 基础水 / 鬼水 / 铁锈水 / 沟渠水",
    "change": "水质变化才更新",
    "c1": "纯度不变时，你手动贴的标签会保留。",
    "c2": "水被净化或污染后，标签自动同步成真实水质。",
    "fraud": "兼容 FraudDetection",
    "fr1": "标签与真实品质保持一致；同步后，",
    "fr2": "该容器不再显示标签与真实的差异。",
    "install": "安装",
    "ins": ("解压，把 WaterAutoLabel 文件夹放进游戏 Mods 目录",
            "在模组菜单启用并重启"),
    "foot": "模组设置里可开关。游戏原生加载器，无需 MelonLoader。",
}


def compose_gallery(cap, lang, t, outname):
    W, H = 1920, 1080
    M = 48
    RIGHT = W - M
    cn = lang == "zh"
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    d.rounded_rectangle((M, 26, RIGHT, 132), radius=10, fill=PANEL, outline=BORDER, width=2)
    d.text((M + 26, 38), "Water Auto Label", font=font(42, True), fill=WHITE)
    text_fit(d, M + 26, 92, t["top_sub"], 18, RIGHT - M - 52, MUTED, cn=cn)

    top, bottom = 156, H - 40
    avail_h = bottom - top
    sw = 900
    sh = int(cap.height * (sw / cap.width))  # 按宽度缩放，保证 tooltip 完整
    main = cap.resize((sw, sh), Image.LANCZOS)
    mx, my = M, top + (avail_h - sh) // 2
    d.rounded_rectangle((mx, my, mx + sw, my + sh), radius=8, fill=PANEL)
    im.paste(main, (mx, my))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((mx, my, mx + sw - 1, my + sh - 1), radius=8, outline=BORDER, width=2)

    px = mx + sw + 40
    pw = RIGHT - px
    assert pw > 500, "info column too narrow"
    d.rounded_rectangle((px, top, RIGHT, bottom), radius=10, fill=PANEL, outline=BORDER, width=2)

    y = top + 32
    d.text((px + 30, y), t["glance"], font=font(28, True, cn), fill=CYAN); y += 54
    for line in (t["f1"], t["f2"], t["f3"]):
        text_fit(d, px + 30, y, line, 17, pw - 60, WHITE, cn=cn); y += 34
    y += 24
    d.text((px + 30, y), t["change"], font=font(23, True, cn), fill=WHITE); y += 44
    for line in (t["c1"], t["c2"]):
        text_fit(d, px + 30, y, line, 17, pw - 60, MUTED, cn=cn); y += 34
    y += 24
    d.text((px + 30, y), t["fraud"], font=font(23, True, cn), fill=WHITE); y += 44
    for line in (t["fr1"], t["fr2"]):
        text_fit(d, px + 30, y, line, 17, pw - 60, MUTED, cn=cn); y += 34
    y += 40
    d.text((px + 30, y), t["install"], font=font(23, True, cn), fill=WHITE); y += 44
    for line in t["ins"]:
        text_fit(d, px + 46, y, "- " + line, 16, pw - 76, WHITE, cn=cn); y += 32
    y += 30
    text_fit(d, px + 30, y, t["foot"], 16, pw - 60, DIM, cn=cn); y += 24

    assert y < bottom - 12, "info text overflow (y=%d bottom=%d)" % (y, bottom)
    save(im, outname)


def main():
    cap = Image.open(CAP).convert("RGB")
    compose_header(cap)
    compose_gallery(cap, "en", T_EN, "gallery-1.png")
    compose_gallery(cap, "zh", T_ZH, "gallery-2-zh.png")


if __name__ == "__main__":
    main()
