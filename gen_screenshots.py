"""
gen_screenshots.py
------------------
Малює фейкові скріншоти застосунку Silpo за допомогою PIL.
Не потребує запускати app.

pip install pillow
python gen_screenshots.py
"""

import os, sys, subprocess, random
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ── Розміри і кольори ─────────────────────────────────────────────────────────
W, H = 1256, 859
SIDEBAR_W = 180

LIGHT = {
    "bg":        "#F5F4FF",
    "sidebar":   "#EEEAF8",
    "card":      "#FFFFFF",
    "text":      "#1a1a2e",
    "text2":     "#666680",
    "accent":    "#6C63FF",
    "green":     "#2ecc71",
    "red":       "#ff4d4d",
    "search":    "#6C63FF",
}
DARK = {
    "bg":        "#1E1E2E",
    "sidebar":   "#2A2A3E",
    "card":      "#2D2D44",
    "text":      "#FFFFFF",
    "text2":     "#8888AA",
    "accent":    "#6C63FF",
    "green":     "#2ecc71",
    "red":       "#ff4d4d",
    "search":    "#5A52D5",
}

APP_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(APP_DIR, "cache_images")
ASSETS_DIR = os.path.join(APP_DIR, "assets")

# ── Шрифти ────────────────────────────────────────────────────────────────────
def font(size, bold=False):
    """Знаходить системний шрифт."""
    names = (
        ["arialbd.ttf", "Arial Bold.ttf"] if bold
        else ["arial.ttf", "Arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    )
    dirs = [
        r"C:\Windows\Fonts",
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts",
    ]
    for d in dirs:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except: pass
    return ImageFont.load_default()

F10  = font(10)
F11  = font(11)
F12  = font(12)
F13  = font(13)
F14  = font(14)
F16  = font(16)
F18  = font(18)
F11B = font(11, bold=True)
F12B = font(12, bold=True)
F14B = font(14, bold=True)
F16B = font(16, bold=True)
F18B = font(18, bold=True)

# ── Округлений прямокутник ────────────────────────────────────────────────────
def rounded_rect(draw, xy, fill, radius=10, outline=None, width=1):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill,
                           outline=outline, width=width)

# ── Зображення товару ─────────────────────────────────────────────────────────
_cached_imgs = None

def get_cached_images():
    global _cached_imgs
    if _cached_imgs is None:
        files = [f for f in os.listdir(CACHE_DIR)
                 if f.lower().endswith(".png")] if os.path.exists(CACHE_DIR) else []
        _cached_imgs = files
    return _cached_imgs

def load_product_img(size=(140, 140), index=0):
    imgs = get_cached_images()
    if not imgs:
        img = Image.new("RGBA", size, (200, 200, 220, 0))
        return img
    fname = imgs[index % len(imgs)]
    try:
        img = Image.open(os.path.join(CACHE_DIR, fname)).convert("RGBA")
        img.thumbnail(size, Image.LANCZOS)
        # Центруємо на прозорому фоні
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
        off = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
        canvas.paste(img, off, img)
        return canvas
    except:
        return Image.new("RGBA", size, (200, 200, 220, 50))

# ── Сайдбар ───────────────────────────────────────────────────────────────────
def draw_sidebar(draw, img, th, active="Каталог"):
    draw.rectangle([0, 0, SIDEBAR_W, H], fill=th["sidebar"])

    # Логотип
    logo_path = os.path.join(ASSETS_DIR, "silpo_logo.png")
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.thumbnail((70, 70), Image.LANCZOS)
            img.paste(logo, (SIDEBAR_W // 2 - logo.width // 2, 18), logo)
        except: pass

    # Баланс
    draw.text((SIDEBAR_W // 2, 100), "Баланс: 1424 грн",
              fill=th["green"], font=F11B, anchor="mm")

    # Кнопка теми
    theme_lbl = "🌙 Темна тема" if th is LIGHT else "☀️ Світла тема"
    rounded_rect(draw, [15, 115, SIDEBAR_W - 15, 138], fill=th["accent"], radius=12)
    draw.text((SIDEBAR_W // 2, 126), theme_lbl, fill="#FFFFFF", font=F10, anchor="mm")

    # Поповнити
    rounded_rect(draw, [25, 143, SIDEBAR_W - 25, 162], fill=th["accent"], radius=10)
    draw.text((SIDEBAR_W // 2, 152), "+ Поповнити", fill="#FFFFFF", font=F10, anchor="mm")

    # Навігація
    navs = ["Каталог", "Кошик", "Аналітика", "Історія"]
    for i, name in enumerate(navs):
        y = 180 + i * 50
        is_active = name == active
        if is_active:
            rounded_rect(draw, [10, y - 2, SIDEBAR_W - 10, y + 30],
                         fill="#3A3A5C" if th is DARK else "#E8E4FF", radius=8)
        draw.text((20, y + 8), name, fill=th["text"],
                  font=F14B if is_active else F14)

    # Низ
    draw.text((20, H - 70), "Видалити акаунт", fill=th["red"], font=F12)
    draw.text((20, H - 40), "Вийти", fill=th["text2"], font=F12)

# ── Пошуковий рядок ───────────────────────────────────────────────────────────
def draw_search(draw, th):
    rounded_rect(draw, [SIDEBAR_W + 10, 15, W - 20, 45],
                 fill=th["search"], radius=14)
    draw.text(((SIDEBAR_W + W) // 2, 30), "Пошук продуктів...",
              fill="#FFFFFF", font=F14, anchor="mm")

# ── Категорії ─────────────────────────────────────────────────────────────────
CATEGORY_COLORS = [
    ("#D6E8FF", "Випічка"),
    ("#D6F5E8", "Напої"),
    ("#D6F5F0", "Фрукти"),
    ("#FFF3D6", "Молочні"),
    ("#FFD6D6", "М'ясо & Риба"),
    ("#FFE8D6", "Бакалія"),
    ("#EDD6FF", "Снеки"),
]

def draw_categories(draw, img, th):
    draw.text((SIDEBAR_W + 14, 58), "Категорії", fill=th["text"], font=F16B)

    cols = 4
    cw, ch = 245, 110
    gap = 8
    start_x = SIDEBAR_W + 10
    start_y = 78

    for i, (color, name) in enumerate(CATEGORY_COLORS):
        row, col = divmod(i, cols)
        x0 = start_x + col * (cw + gap)
        y0 = start_y + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch

        rounded_rect(draw, [x0, y0, x1, y1], fill=color, radius=12)

        # Фото категорії
        cat_img = load_product_img((70, 70), index=i * 7)
        cx = x0 + (cw - 70) // 2
        cy = y0 + 8
        img.paste(cat_img, (cx, cy), cat_img)

        draw.text((x0 + cw // 2, y1 - 16), name,
                  fill=th["text"], font=F11B, anchor="mm")

# ── Картка товару ─────────────────────────────────────────────────────────────
PRODUCT_NAMES = [
    ("Хліб подовий", "1 шт", "15 грн"),
    ("Хліб Цар-Хліб Балтійський", "1 шт", "45 грн"),
    ("Хліб Цар-Хліб Панський", "1 шт", "44 грн"),
    ("Хліб Цар-Хліб Житній", "1 шт", "30 грн"),
    ("Хліб «Крафтяр»", "1 шт", "124 грн"),
]

def draw_product_card(draw, img, th, x, y, idx):
    cw, ch = 215, 295
    rounded_rect(draw, [x, y, x + cw, y + ch],
                 fill=th["card"], radius=12,
                 outline="#E0E0F0" if th is LIGHT else "#3D3D55", width=1)

    # Фото
    prod_img = load_product_img((140, 140), index=idx * 3 + 10)
    px = x + (cw - prod_img.width) // 2
    img.paste(prod_img, (px, y + 8), prod_img)

    name, weight, price = PRODUCT_NAMES[idx % len(PRODUCT_NAMES)]
    # Назва (до 2 рядків)
    words = name.split()
    line1 = " ".join(words[:2])
    line2 = " ".join(words[2:]) if len(words) > 2 else ""
    draw.text((x + 10, y + 156), line1, fill=th["text"], font=F12B)
    if line2:
        draw.text((x + 10, y + 172), line2, fill=th["text"], font=F12B)

    draw.text((x + 10, y + 192), weight, fill=th["text2"], font=F10)

    # Кнопки кількості
    for bx, btext in [(x + 8, "−"), (x + 75, "+")]:
        draw.ellipse([bx, y + 210, bx + 24, y + 234], fill="#1a1a2e")
        draw.text((bx + 12, y + 222), btext, fill="white", font=F12B, anchor="mm")
    draw.text((x + 50, y + 222), "1", fill=th["text"], font=F12B, anchor="mm")
    draw.text((x + 105, y + 222), "шт", fill=th["text2"], font=F10)

    # Ціна і кнопка
    draw.text((x + 10, y + 248), price, fill=th["text"], font=F14B)
    rounded_rect(draw, [x + 120, y + 240, x + cw - 8, y + 265],
                 fill=th["accent"], radius=12)
    draw.text((x + (120 + cw - 8) // 2, y + 252),
              "+ Додати", fill="white", font=F10, anchor="mm")

# ── Заголовок вікна ───────────────────────────────────────────────────────────
def draw_titlebar(draw, img):
    draw.rectangle([0, 0, W, 32], fill="#F0F0F0")
    # Іконка + заголовок
    draw.rectangle([8, 8, 24, 24], fill="#6C63FF", outline="#5A52D5")
    draw.text((30, 16), "Silpo", fill="#333333", font=F12B, anchor="lm")
    # Кнопки вікна
    for i, (clr, sym) in enumerate([("#FF5F57","−"),("#FFBD2E","□"),("#28C840","×")]):
        bx = W - 90 + i * 30
        draw.ellipse([bx, 10, bx + 14, 24], fill=clr)

# ── Нижня панель ─────────────────────────────────────────────────────────────
def draw_bottom(draw, th):
    draw.line([(SIDEBAR_W, H - 38), (W, H - 38)], fill="#DDDDEE", width=1)
    draw.text(((SIDEBAR_W + W) // 2, H - 20),
              "Page 1 of 34", fill=th["text2"], font=F11, anchor="mm")
    rounded_rect(draw, [W - 110, H - 34, W - 10, H - 8],
                 fill=th["accent"], radius=10)
    draw.text((W - 60, H - 21), "Далі →", fill="white", font=F11B, anchor="mm")

# ── Скласти головний екран ────────────────────────────────────────────────────
def make_main(th, filename):
    img = Image.new("RGB", (W, H), th["bg"])
    draw = ImageDraw.Draw(img)

    draw_titlebar(draw, img)

    # Зміщення вниз на заголовок
    orig_paste = img.paste
    def draw_sidebar_wrap():
        draw_sidebar(draw, img, th, active="Каталог")
    draw_sidebar_wrap()
    draw_search(draw, th)

    # Категорії — зміщені вниз на 32px (titlebar)
    # Перемалюємо з offset
    img2 = Image.new("RGB", (W, H - 32), th["bg"])
    draw2 = ImageDraw.Draw(img2)
    draw_sidebar(draw2, img2, th, active="Каталог")
    draw_search(draw2, th)
    draw_categories(draw2, img2, th)

    # Товари
    draw2.text((SIDEBAR_W + 14, 310), "Популярні товари (1-15 / 504)",
               fill=th["text"], font=F16B)
    for i in range(5):
        x = SIDEBAR_W + 10 + i * (215 + 8)
        draw_product_card(draw2, img2, th, x, 338, i)

    draw_bottom(draw2, th)
    img2 = img2.resize((W, H - 32))  # якщо розміри збіглися

    # Вставляємо вміст під titlebar
    img.paste(img2, (0, 32))
    draw_titlebar(draw, img)

    path = os.path.join(APP_DIR, filename)
    img.save(path, "PNG", optimize=True)
    print(f"  ✅  {filename}  ({os.path.getsize(path)//1024} KB)")

# ── Екран деталей товару ──────────────────────────────────────────────────────
def make_details(th, filename):
    img = Image.new("RGB", (W, H), th["bg"])
    draw = ImageDraw.Draw(img)

    draw_sidebar(draw, img, th, active="Каталог")

    # Назад
    rounded_rect(draw, [SIDEBAR_W + 10, 10, SIDEBAR_W + 100, 36],
                 fill=th["accent"], radius=10)
    draw.text((SIDEBAR_W + 55, 23), "← Назад", fill="white", font=F11B, anchor="mm")

    # Ліва панель
    lx = SIDEBAR_W + 10
    rounded_rect(draw, [lx, 45, lx + 450, H - 15], fill=th["card"], radius=14)
    prod = load_product_img((160, 160), index=15)
    img.paste(prod, (lx + (450 - prod.width) // 2, 65), prod)

    draw.text((lx + 225, 240), "Хліб Цар-Хліб Панський",
              fill=th["text"], font=F16B, anchor="mm")
    draw.text((lx + 225, 265), "пшеничний половинка нарізаний",
              fill=th["text"], font=F14, anchor="mm")
    draw.text((lx + 225, 290), "Свіжий та якісний продукт з Сільпо.",
              fill=th["text2"], font=F12, anchor="mm")
    draw.text((lx + 225, 325), "Ціна: 44 грн",
              fill=th["accent"], font=F18B, anchor="mm")
    draw.text((lx + 225, 360), "Виберіть сорт/колір:",
              fill=th["text"], font=F12B, anchor="mm")
    draw.rounded_rectangle([lx + 195, 375, lx + 255, 410],
                           radius=6, fill="#5A52D5")
    draw.text((lx + 225, 430), "Кількість:", fill=th["text"], font=F12B, anchor="mm")
    rounded_rect(draw, [lx + 165, 450, lx + 285, H - 100],
                 fill=th["green"], radius=20)
    draw.text((lx + 225, H - 65), "Додати в кошик",
              fill="white", font=F14B, anchor="mm")

    # Права панель — відгуки
    rx = lx + 460
    rounded_rect(draw, [rx, 45, W - 15, H - 15], fill=th["card"], radius=14)
    draw.text((rx + (W - rx) // 2, 70), "Відгуки та оцінки:",
              fill=th["text"], font=F14B, anchor="mm")
    draw.text((rx + 20, 110), "Відгуків ще немає.",
              fill=th["text2"], font=F12)

    draw_titlebar(draw, img)

    path = os.path.join(APP_DIR, filename)
    img.save(path, "PNG", optimize=True)
    print(f"  ✅  {filename}  ({os.path.getsize(path)//1024} KB)")

# ── Екран кошика ──────────────────────────────────────────────────────────────
def make_cart(th, filename):
    img = Image.new("RGB", (W, H), th["bg"])
    draw = ImageDraw.Draw(img)

    draw_sidebar(draw, img, th, active="Кошик")

    lx = SIDEBAR_W + 10
    mid = lx + 600

    # Ліва частина — список
    rounded_rect(draw, [lx, 10, mid, H - 15], fill=th["card"], radius=14)
    draw.text(((lx + mid) // 2, 38), "Кошик товарів",
              fill=th["accent"], font=F16B, anchor="mm")
    rounded_rect(draw, [lx + 10, 52, mid - 10, 76], fill="#2b2b3d", radius=6)
    for xoff, lbl in [(20, "Товар"), (260, "К-сть"), (380, "Ціна"), (500, "Дія")]:
        draw.text((lx + xoff, 64), lbl, fill="white", font=F11B)
    draw.text(((lx + mid) // 2, H // 2),
              "Кошик порожній", fill=th["text2"], font=F14, anchor="mm")
    draw.text(((lx + mid) // 2, H - 48),
              "Разом до сплати: 0 грн", fill=th["accent"], font=F14B, anchor="mm")
    rounded_rect(draw, [(lx + mid) // 2 - 70, H - 35, (lx + mid) // 2 + 70, H - 15],
                 fill="#95a5a6", radius=10)
    draw.text(((lx + mid) // 2, H - 25), "Очистити кошик",
              fill="white", font=F11B, anchor="mm")

    # Права частина — форма доставки
    rounded_rect(draw, [mid + 10, 10, W - 15, H - 15], fill=th["card"], radius=14)
    draw.text(((mid + W) // 2, 38), "Дані для доставки",
              fill=th["text"], font=F14B, anchor="mm")
    for i, ph in enumerate(["+380", "Електронна пошта (Email)", "Адреса доставки"]):
        ey = 60 + i * 50
        rounded_rect(draw, [mid + 20, ey, W - 25, ey + 36],
                     fill=th["bg"] if th is DARK else "#FFFFFF",
                     radius=8, outline="#CCCCDD", width=1)
        draw.text((mid + 35, ey + 18), ph, fill=th["text2"], font=F12, anchor="lm")
    for i, lbl in enumerate(["Кур'єр", "Балансом акаунту"]):
        ey = 220 + i * 50
        rounded_rect(draw, [mid + 20, ey, W - 25, ey + 36],
                     fill=th["accent"], radius=8)
        draw.text((mid + 35, ey + 18), lbl, fill="white", font=F12, anchor="lm")
    rounded_rect(draw, [(mid + W) // 2 - 90, 340, (mid + W) // 2 + 90, 372],
                 fill=th["green"], radius=18)
    draw.text(((mid + W) // 2, 356), "Оформити замовлення",
              fill="white", font=F12B, anchor="mm")

    draw_titlebar(draw, img)
    path = os.path.join(APP_DIR, filename)
    img.save(path, "PNG", optimize=True)
    print(f"  ✅  {filename}  ({os.path.getsize(path)//1024} KB)")

# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  🖼️   Silpo Screenshot Generator  (PIL)")
    print("=" * 50)

    print("\nГенерую screenshot_main_v7.png ...")
    make_main(LIGHT, "screenshot_main_v7.png")

    print("Генерую screenshot_dark_v7.png ...")
    make_main(DARK, "screenshot_dark_v7.png")

    print("Генерую screenshot_details_v7.png ...")
    make_details(LIGHT, "screenshot_details_v7.png")

    print("Генерую screenshot_cart_v7.png ...")
    make_cart(LIGHT, "screenshot_cart_v7.png")

    print("\n✅  Всі скріншоти готові!")
    print("\n👇  Запушити:")
    print("    git add screenshot_*_v7.png")
    print('    git commit -m "Add screenshots v7"')
    print("    git push")
