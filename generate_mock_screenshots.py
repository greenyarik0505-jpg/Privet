import os
from PIL import Image, ImageDraw, ImageFont

# Семейство цветов convenientshop
PRIMARY_COLOR = "#4F46E5"    # Индиго
BG_COLOR = "#A4A4EB"         # Мягкий фиолетовый фон
FRAME_COLOR = "#E0DDF0"      # Лавандово-серый
HOVER_COLOR = "#D7D2F4"      # Ховер эффект

CARD_COLORS = [
    "#7DABDE",  # Синий
    "#87D7E0",  # Циан
    "#EA7BBE",  # Розовый
    "#BCEAA5",  # Светло-зеленый
    "#B9A5EA",  # Пурпурный
    "#EAA5A6"   # Светло-красный
]

FONT_PATH = "C:/Windows/Fonts/segoeui.ttf"
def get_font(size, bold=False):
    if bold:
        bold_path = "C:/Windows/Fonts/segoeuib.ttf"
        if os.path.exists(bold_path):
            return ImageFont.truetype(bold_path, size)
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def get_product_image_by_filename(filename, size):
    path = os.path.join(os.path.dirname(__file__), "assets", filename)
    if os.path.exists(path):
        try:
            return Image.open(path).resize(size, Image.Resampling.LANCZOS)
        except Exception:
            pass
    img = Image.new("RGBA", size, "#e2e2e2")
    return img

def draw_custom_sidebar(draw, active_nav, user="Yarik", balance="1500 грн"):
    # Рисуем сайдбар скругленным
    draw.rounded_rectangle([10, 10, 190, 540], 12, fill=FRAME_COLOR)
    
    # Логотип
    draw.text((25, 30), "CONVENIENT SHOP", fill=PRIMARY_COLOR, font=get_font(13, True))
    
    # Профиль
    draw.text((100, 75), user, fill="black", anchor="mm", font=get_font(12, True))
    draw.text((100, 95), balance, fill="#2ecc71", anchor="mm", font=get_font(11, True))
    
    # Кнопка пополнения
    draw.rounded_rectangle([35, 120, 165, 145], 12, fill=PRIMARY_COLOR)
    draw.text((100, 132), "+ Поповнити", fill="#ffffff", anchor="mm", font=get_font(10, True))
    
    # Навигационные кнопки
    navs = ["Каталог", "Кошик", "Аналітика", "Історія", "Налаштування"]
    for i, nav in enumerate(navs):
        y = 180 + i * 42
        is_active = (nav == active_nav)
        bg = HOVER_COLOR if is_active else FRAME_COLOR
        draw.rounded_rectangle([20, y, 180, y + 32], 6, fill=bg)
        draw.text((30, y + 16), nav, fill="black", anchor="lm", font=get_font(10, True))
        
    # Выход
    draw.rounded_rectangle([20, 490, 180, 520], 6, fill="#e74c3c")
    draw.text((100, 505), "Вийти", fill="#ffffff", anchor="mm", font=get_font(10, True))

def create_main_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Сайдбар
    draw_custom_sidebar(draw, "Каталог")
    
    # Верхняя панель поиска
    draw.rounded_rectangle([205, 15, 735, 60], 10, fill=FRAME_COLOR)
    draw.rounded_rectangle([215, 23, 350, 51], 6, fill="white", outline=PRIMARY_COLOR, width=2)
    draw.text((225, 37), "Пошук продуктів...", fill="gray", anchor="lm", font=get_font(10))
    
    categories = ["Усі", "Випічка", "Молочне", "Фрукти", "Напої", "Снеки"]
    for i, cat in enumerate(categories):
        x = 365 + i * 48
        bg_col = "#3498db" if i == 0 else PRIMARY_COLOR
        draw.rounded_rectangle([x, 23, x + 44, 51], 4, fill=bg_col)
        draw.text((x + 22, 37), cat, fill="#ffffff", anchor="mm", font=get_font(8, True))
        
    # Товары в сетке
    products = [
        ("Яблука Гала", "45 грн", "Apple.png"),
        ("Авокадо Хасс", "120 грн", "Avocado.png"),
        ("Сир Чеддер", "110 грн", "Cheese.png"),
        ("Кола Дієтична", "28 грн", "Diet_Cola.png"),
        ("Свіжий білий хліб", "22 грн", "SLiced_White_Bread.png"),
        ("Картопляні чіпси", "48 грн", "Potato_Chips.png")
    ]
    
    for i, (name, price, img_file) in enumerate(products):
        row = i // 3
        col = i % 3
        cx = 205 + col * 178
        cy = 75 + row * 230
        
        # Пестрые карточки товаров
        card_bg = CARD_COLORS[i % len(CARD_COLORS)]
        draw.rounded_rectangle([cx, cy, cx + 168, cy + 215], 12, fill=card_bg)
        
        draw.text((cx + 145, cy + 20), "Liked" if i == 0 else "Like", fill="red" if i == 0 else "gray", anchor="mm", font=get_font(9, True))
        
        # Картинка товара
        prod_img = get_product_image_by_filename(img_file, (65, 65))
        img.paste(prod_img, (cx + 50, cy + 25), prod_img if prod_img.mode == "RGBA" else None)
        
        # Текст
        draw.text((cx + 84, cy + 115), name, fill="black", anchor="mm", font=get_font(10, True))
        draw.text((cx + 84, cy + 135), f"{price}", fill="#1e1e2e", anchor="mm", font=get_font(10, True))
        
        # Кнопка подробнее
        draw.rounded_rectangle([cx + 20, cy + 165, cx + 148, cy + 195], 50, fill=PRIMARY_COLOR)
        draw.text((cx + 84, cy + 180), "Детальніше", fill="#ffffff", anchor="mm", font=get_font(10, True))
        
    img.save("screenshot_main_v6.png")
    print("Created mockup: screenshot_main_v6.png")

def create_details_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_custom_sidebar(draw, "Каталог")
    
    draw.rounded_rectangle([205, 15, 275, 40], 5, fill=PRIMARY_COLOR)
    draw.text((240, 27), "← Назад", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([205, 60, 460, 520], 10, fill=FRAME_COLOR)
    
    prod_img = get_product_image_by_filename("Apple.png", (120, 120))
    img.paste(prod_img, (270, 80), prod_img if prod_img.mode == "RGBA" else None)
    
    draw.text((330, 220), "Яблука Гала", fill="black", anchor="mm", font=get_font(12, True))
    draw.text((330, 250), "Свіжі хрусткі яблука сорту Гала.", fill="black", anchor="mm", font=get_font(9, True))
    draw.text((330, 275), "Ціна: 45 грн/шт", fill=PRIMARY_COLOR, anchor="mm", font=get_font(12, True))
    
    draw.text((330, 310), "Виберіть сорт/колір:", fill="black", anchor="mm", font=get_font(9, True))
    draw.rectangle([300, 325, 320, 340], fill="#e74c3c", outline=PRIMARY_COLOR, width=2)
    draw.rectangle([340, 325, 360, 340], fill="#2ecc71")
    
    draw.text((280, 380), "Кількість:", fill="black", anchor="mm", font=get_font(9, True))
    draw.rounded_rectangle([320, 368, 370, 392], 3, fill="white")
    draw.text((345, 380), "1", fill="black", anchor="mm", font=get_font(10))
    
    draw.rounded_rectangle([250, 430, 410, 470], 50, fill="#2ecc71")
    draw.text((330, 450), "Додати в кошик", fill="#ffffff", anchor="mm", font=get_font(11, True))
    
    draw.rounded_rectangle([480, 60, 730, 520], 10, fill=FRAME_COLOR)
    draw.text((605, 80), "Відгуки та оцінки:", fill="black", anchor="mm", font=get_font(11, True))
    draw.text((605, 110), "Рейтинг: ***** (5.0/5)", fill="#f1c40f", anchor="mm", font=get_font(10, True))
    
    draw.rounded_rectangle([495, 140, 715, 190], 5, fill="white")
    draw.text((505, 155), "• Yarik: Супер солодкі!", fill="black", font=get_font(9))
    
    img.save("screenshot_details_v6.png")
    print("Created mockup: screenshot_details_v6.png")

def create_cart_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_custom_sidebar(draw, "Кошик")
    
    draw.rounded_rectangle([205, 20, 460, 520], 10, fill=FRAME_COLOR)
    draw.text((330, 40), "Кошик товарів (POS)", fill=PRIMARY_COLOR, anchor="mm", font=get_font(12, True))
    
    draw.rounded_rectangle([215, 70, 445, 120], 6, fill="white")
    draw.text((225, 95), "Яблука Гала x1", fill="black", anchor="lm", font=get_font(9, True))
    draw.text((350, 95), "45 грн", fill="#2e7d32", anchor="lm", font=get_font(9, True))
    draw.rounded_rectangle([415, 85, 435, 105], 3, fill="#e74c3c")
    draw.text((425, 95), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    draw.rounded_rectangle([215, 130, 445, 180], 6, fill="white")
    draw.text((225, 155), "Сир Чеддер x2", fill="black", anchor="lm", font=get_font(9, True))
    draw.text((350, 155), "220 грн", fill="#2e7d32", anchor="lm", font=get_font(9, True))
    draw.rounded_rectangle([415, 145, 435, 165], 3, fill="#e74c3c")
    draw.text((425, 155), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    draw.text((330, 440), "Сума: 265 грн", fill="black", anchor="mm", font=get_font(9, True))
    draw.text((330, 470), "Разом: 265 грн", fill=PRIMARY_COLOR, anchor="mm", font=get_font(11, True))
    draw.rounded_rectangle([260, 490, 400, 515], 50, fill="#95a5a6")
    draw.text((330, 502), "Очистити кошик", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([480, 20, 730, 520], 10, fill=FRAME_COLOR)
    draw.text((605, 40), "Дані для доставки", fill="black", anchor="mm", font=get_font(11, True))
    
    fields = ["Номер телефону (+380...)", "Електронна пошта (Email)", "Адреса доставки", "Courier", "Balance"]
    for i, val in enumerate(fields):
        y = 80 + i * 50
        draw.rounded_rectangle([495, y, 715, y + 35], 5, fill="white", outline=PRIMARY_COLOR, width=1)
        draw.text((505, y + 17), val, fill="gray", anchor="lm", font=get_font(9))
        
    draw.rounded_rectangle([510, 430, 700, 475], 50, fill="#2ecc71")
    draw.text((605, 452), "Оформити", fill="#ffffff", anchor="mm", font=get_font(12, True))
    
    img.save("screenshot_cart_v6.png")
    print("Created mockup: screenshot_cart_v6.png")

if __name__ == "__main__":
    create_main_screenshot()
    create_details_screenshot()
    create_cart_screenshot()
