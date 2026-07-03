"""
gen_dark.py — генерує screenshot_dark_v7.png
Максимально точно повторює реальний вигляд застосунку в темній темі.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

APP   = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(APP, "cache_images")
ASSETS= os.path.join(APP, "assets")

W, H  = 1040, 660
SW    = 140      # sidebar width

# ── Темні кольори (точно як у застосунку) ─────────────────────────────────────
BG      = "#1E1E2E"
SIDEBAR = "#1A1A2A"
CARD    = "#2D2D44"
TEXT    = "#FFFFFF"
TEXT2   = "#8888AA"
ACCENT  = "#6C63FF"
GREEN   = "#2ecc71"
RED     = "#ff4d4d"

# ── Шрифти ────────────────────────────────────────────────────────────────────
def fnt(sz, bold=False):
    for d in [r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu"]:
        for n in (["arialbd.ttf"] if bold else ["arial.ttf","DejaVuSans.ttf"]):
            p = os.path.join(d, n)
            if os.path.exists(p):
                try: return ImageFont.truetype(p, sz)
                except: pass
    return ImageFont.load_default()

F10=fnt(10); F11=fnt(11); F12=fnt(12); F13=fnt(13); F14=fnt(14)
F10B=fnt(10,1); F11B=fnt(11,1); F12B=fnt(12,1); F14B=fnt(14,1); F16B=fnt(16,1)

def rr(d, xy, fill, r=8, ol=None, w=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=ol, width=w)

# ── Завантажити зображення ────────────────────────────────────────────────────
def load_img(path, size):
    try:
        img = Image.open(path).convert("RGBA")
        img.thumbnail(size, Image.LANCZOS)
        c = Image.new("RGBA", size, (0,0,0,0))
        off = ((size[0]-img.width)//2, (size[1]-img.height)//2)
        c.paste(img, off, img)
        return c
    except:
        return Image.new("RGBA", size, (80,80,100,100))

def asset(name, size):
    return load_img(os.path.join(ASSETS, name), size)

# Хліби з кешу (реальні файли що існують)
BREAD_IDS = [
    "972992_480x480wwm_5dc29020-eee3-9e11-091e-d205ef33e8eb",  # Хліб подовий
    "974592_480x480wwm_0e8ed99a-cbd8-479d-0d01-47fa03382330",  # Цар-Хліб Балтійський
    "975472_480x480wwm_d57d9e16-4aa4-b848-7a6f-b4e9d425ee9a",  # Цар-Хліб Панський
    "975473_480x480wwm_7b0488f7-a4af-ead6-57fb-c54680c2af0a",  # Цар-Хліб Житній
    "974919_480x480wwm_294122d6-9321-01af-9c39-55879e70ecaa",  # Хліб Крафтяр
]

def bread_img(idx, size=(120,120)):
    bid = BREAD_IDS[idx % len(BREAD_IDS)]
    path = os.path.join(CACHE, bid + ".png")
    return load_img(path, size)

# ── Побудова зображення ───────────────────────────────────────────────────────
img  = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# ── САЙДБАР ───────────────────────────────────────────────────────────────────
draw.rectangle([0, 0, SW, H], fill=SIDEBAR)

# Логотип
logo = asset("silpo_logo.png", (70, 50))
img.paste(logo, (SW//2 - logo.width//2, 14), logo)

# Баланс
draw.text((SW//2, 72), "Баланс: 1424 грн", fill=GREEN, font=F11B, anchor="mm")

# Кнопка "☀️ Світла тема"
rr(draw, [10, 82, SW-10, 100], fill=ACCENT, r=10)
draw.text((SW//2, 91), "  Світла тема", fill="white", font=F10, anchor="mm")

# "+ Поповнити"
rr(draw, [18, 104, SW-18, 120], fill=ACCENT, r=8)
draw.text((SW//2, 112), "+ Поповнити", fill="white", font=F10, anchor="mm")

# Навігація
NAV = [("Каталог", True), ("Кошик", False), ("Аналітика", False), ("Історія", False)]
for i, (name, active) in enumerate(NAV):
    y = 135 + i*38
    if active:
        rr(draw, [6, y-2, SW-6, y+22], fill="#3A3A5C", r=6)
    draw.text((14, y+10), name, fill=TEXT if active else TEXT2,
              font=F12B if active else F12, anchor="lm")

# Низ сайдбару
draw.text((14, H-50), "Видалити акаунт", fill=RED, font=F11)
draw.text((14, H-25), "Вийти", fill=TEXT2, font=F11)

# ── ПОШУК ─────────────────────────────────────────────────────────────────────
rr(draw, [SW+10, 10, W-10, 36], fill=ACCENT, r=14)
draw.text(((SW+W)//2, 23), "Пошук продуктів...", fill="white", font=F14, anchor="mm")

# ── КАТЕГОРІЇ ─────────────────────────────────────────────────────────────────
draw.text((SW+12, 46), "Категорії", fill=TEXT, font=F14B)

CATS = [
    ("cat_bakeries.png",  "#2A3D52", "Випічка"),
    ("cat_drinks.png",    "#1F3D2F", "Напої"),
    ("cat_fruits.png",    "#2A3A2A", "Фрукти"),
    ("cat_dairy.png",     "#3D3520", "Молочні"),
    ("cat_meat_fish.png", "#3D2020", "М'ясо & Риба"),
    ("cat_grocery.png",   "#3A2F1A", "Бакалія"),
    ("cat_snacks.png",    "#30203D", "Снеки"),
]

cols = 4
cw, ch = 210, 95
gap = 6
sx, sy = SW+10, 60

for i, (icon, col, name) in enumerate(CATS):
    row, c = divmod(i, cols)
    x0 = sx + c*(cw+gap)
    y0 = sy + row*(ch+gap)
    rr(draw, [x0, y0, x0+cw, y0+ch], fill=col, r=10)
    ic = asset(icon, (52, 52))
    ix = x0 + (cw - ic.width)//2
    img.paste(ic, (ix, y0+6), ic)
    draw.text((x0+cw//2, y0+ch-12), name, fill=TEXT, font=F11B, anchor="mm")

# ── ТОВАРИ ────────────────────────────────────────────────────────────────────
prod_y = sy + 2*(ch+gap) + 8
draw.text((SW+12, prod_y), "Популярні товари (1-15 / 504)", fill=TEXT, font=F14B)

PRODS = [
    ("Хліб подовий",          "1 шт", "15 грн"),
    ("Хліб Цар-Хліб\nБалтійський",    "1 шт", "45 грн"),
    ("Хліб Цар-Хліб\nПанський",       "1 шт", "44 грн"),
    ("Хліб Цар-Хліб\nЖитній",         "1 шт", "30 грн"),
    ("Хліб «Крафтяр»",       "1 шт","124 грн"),
]

card_y = prod_y + 20
pcw, pch = 168, 240
for i, (name, wt, price) in enumerate(PRODS):
    x = SW + 10 + i*(pcw+8)
    rr(draw, [x, card_y, x+pcw, card_y+pch], fill=CARD, r=10,
       ol="#3D3D55", w=1)

    # Фото хліба
    bi = bread_img(i, (110, 110))
    img.paste(bi, (x + (pcw-bi.width)//2, card_y+6), bi)

    # Назва (2 рядки)
    lines = name.split("\n")
    for j, ln in enumerate(lines):
        draw.text((x+8, card_y+122+j*16), ln, fill=TEXT, font=F11B)

    # Вага
    draw.text((x+8, card_y+158), wt, fill=TEXT2, font=F10)

    # Кнопки - / +
    for bx, sym in [(x+6, "−"), (x+62, "+")]:
        draw.ellipse([bx, card_y+174, bx+22, card_y+196], fill="#111122")
        draw.text((bx+11, card_y+185), sym, fill="white", font=F12B, anchor="mm")
    draw.text((x+43, card_y+185), "1", fill=TEXT, font=F12B, anchor="mm")
    draw.text((x+88, card_y+185), "шт", fill=TEXT2, font=F10)

    # Ціна + кнопка
    draw.text((x+8, card_y+204), price, fill=TEXT, font=F12B)
    rr(draw, [x+90, card_y+198, x+pcw-6, card_y+220], fill=ACCENT, r=8)
    draw.text(((x+90+x+pcw-6)//2, card_y+209), "+ Додати", fill="white", font=F10, anchor="mm")

# ── НИЗ ───────────────────────────────────────────────────────────────────────
draw.line([(SW, H-30), (W, H-30)], fill="#333355", width=1)
draw.text(((SW+W)//2, H-16), "Page 1 of 34", fill=TEXT2, font=F11, anchor="mm")
rr(draw, [W-100, H-28, W-6, H-6], fill=ACCENT, r=8)
draw.text((W-53, H-17), "Далі →", fill="white", font=F11B, anchor="mm")

# ── ЗБЕРЕГТИ ─────────────────────────────────────────────────────────────────
out = os.path.join(APP, "screenshot_dark_v7.png")
img.save(out, "PNG", optimize=True)
print(f"✅  screenshot_dark_v7.png  ({os.path.getsize(out)//1024} KB)")
