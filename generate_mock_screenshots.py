import os
from PIL import Image, ImageDraw, ImageFont

# Цветовая гамма точ-в-точ как на скриншоте
PRIMARY_COLOR = "#4F46E5"        # Основной индиго
BG_COLOR = "#F0EFF9"             # Светло-серый фон контента
SIDEBAR_COLOR = "#E5E4F3"        # Лавандовый фон сайдбару
HOVER_COLOR = "#D7D2F4"          # Ховер
SEARCH_BAR_COLOR = "#8A96EC"     # Поиск

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

def draw_custom_sidebar(draw, active_nav, height=750):
    # Прямоугольный сайдбар без скругления слева
    draw.rectangle([0, 0, 180, height], fill=SIDEBAR_COLOR)
    
    # Круглый аватар пользователя
    draw.ellipse([50, 25, 130, 105], fill="#EBE8F9")
    draw.ellipse([70, 38, 110, 78], outline=PRIMARY_COLOR, width=3)
    draw.arc([58, 70, 122, 115], start=0, end=180, fill=PRIMARY_COLOR, width=3)
    
    # Кнопки навигации
    navs = [
        ("Каталог", "Каталог"),
        ("Кошик", "Кошик"),
        ("Аналітика", "Аналітика"),
        ("Історія", "Історія"),
        ("Налаштування", "Налаштування")
    ]
    for i, (name, key) in enumerate(navs):
        y = 140 + i * 42
        is_active = (key == active_nav)
        bg = "white" if is_active else SIDEBAR_COLOR
        draw.rounded_rectangle([15, y, 175, y + 32], 6, fill=bg)
        draw.text((25, y + 16), name, fill="black", anchor="lm", font=get_font(11, is_active))
        
    # Logout кнопка внизу
    draw.text((25, height - 40), "Logout", fill="black", anchor="lm", font=get_font(11))

def create_main_screenshot():
    # Масштабовані розміри під реальний інтерфейс 1240х820 додатку
    w, h = 1320, 780
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Сайдбар
    draw_custom_sidebar(draw, "Каталог", height=h)
    
    # Поле поиска
    draw.rounded_rectangle([200, 15, 1300, 45], 15, fill=SEARCH_BAR_COLOR)
    draw.text((750, 30), "Search", fill="white", anchor="mm", font=get_font(11))
    
    # Категорії
    draw.text((200, 65), "Categories", fill="black", font=get_font(12, True))
    
    # Збільшені іконки категорій (150x150)
    categories = [
        ("Випічка", "#C2D6EE", "cat_bakeries.png"),
        ("Напої", "#BCE6EB", "cat_drinks.png"),
        ("Фрукти", "#D3EEC2", "cat_fruits.png"),
        ("Снеки", "#DCD2EE", "cat_snacks.png")
    ]
    for i, (cat, bg, img_file) in enumerate(categories):
        x = 200 + i * 260
        draw.rounded_rectangle([x, 85, x + 240, 255], 12, fill=bg)
        prod_img = get_product_image_by_filename(img_file, (150, 150))
        img.paste(prod_img, (x + 45, 93), prod_img if prod_img.mode == "RGBA" else None)
        draw.text((x + 120, 240), cat, fill="black", anchor="mm", font=get_font(11, True))
        
    # Заголовок "Popular Items" з пагінацією (1-5 з 210)
    draw.text((200, 275), "Popular Items (1-5 / 210)", fill="black", font=get_font(12, True))
    
    # Великі карточки товарів (220x310) з великими HD фотографіями (150x150)
    products = [
        ("Хліб Київхліб", "0.6 кг", "22 грн", "cat_bakeries.png", "1 шт"),
        ("Кока-Кола", "0.5 л", "28 грн", "cat_drinks.png", "1 шт"),
        ("Сир Пирятин", "1 кг", "110 грн", "Cheese.png", "1.0 кг"),
        ("Чіпси Lay's", "0.1 кг", "48 грн", "cat_snacks.png", "1 шт"),
        ("Яблука Гала", "1 кг", "45 грн", "cat_fruits.png", "1.0 кг")
    ]
    
    for i, (name, weight, price, img_file, qty_text) in enumerate(products):
        x = 200 + i * 224
        y = 300
        draw.rounded_rectangle([x, y, x + 210, y + 300], 10, fill="white")
        
        prod_img = get_product_image_by_filename(img_file, (140, 140))
        img.paste(prod_img, (x + 35, y + 10), prod_img if prod_img.mode == "RGBA" else None)
        
        draw.text((x + 12, y + 160), name, fill="black", font=get_font(10, True))
        draw.text((x + 198, y + 160), weight, fill="gray", anchor="rt", font=get_font(9))
        
        # Регулятор кількості
        draw.rounded_rectangle([x + 12, y + 195, x + 198, y + 225], 5, fill="#F3F4F6")
        draw.text((x + 25, y + 210), "-", fill="black", anchor="mm", font=get_font(12, True))
        draw.text((x + 105, y + 210), qty_text, fill="black", anchor="mm", font=get_font(10, True))
        draw.text((x + 185, y + 210), "+", fill="black", anchor="mm", font=get_font(12, True))
        
        # Ціна та Додати
        draw.text((x + 12, y + 255), price, fill="black", font=get_font(11, True))
        draw.rounded_rectangle([x + 100, y + 245, x + 198, y + 275], 15, fill=PRIMARY_COLOR)
        draw.text((x + 149, y + 260), "+ Додати", fill="white", anchor="mm", font=get_font(9, True))
        
    draw.rounded_rectangle([200, 710, 300, 740], 6, fill=PRIMARY_COLOR)
    draw.text((250, 725), "← Назад", fill="white", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([1200, 710, 1300, 740], 6, fill=PRIMARY_COLOR)
    draw.text((1250, 725), "Далі →", fill="white", anchor="mm", font=get_font(9, True))
    
    draw.text((750, 725), "Page 1 of 14", fill="black", anchor="mm", font=get_font(10, True))
        
    img.save("screenshot_main_v6.png")
    print("Created mockup: screenshot_main_v6.png")

def create_details_screenshot():
    w, h = 850, 580
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_custom_sidebar(draw, "Каталог")
    
    draw.rounded_rectangle([200, 15, 270, 40], 5, fill=PRIMARY_COLOR)
    draw.text((235, 27), "← Назад", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([200, 60, 500, 550], 10, fill=SIDEBAR_COLOR)
    
    prod_img = get_product_image_by_filename("cat_bakeries.png", (120, 120))
    img.paste(prod_img, (290, 80), prod_img if prod_img.mode == "RGBA" else None)
    
    draw.text((350, 220), "Хліб Київхліб", fill="black", anchor="mm", font=get_font(12, True))
    draw.text((350, 250), "Свіжий український хліб.", fill="black", anchor="mm", font=get_font(9, True))
    draw.text((350, 275), "Ціна: 22 грн", fill=PRIMARY_COLOR, anchor="mm", font=get_font(12, True))
    
    draw.text((350, 310), "Виберіть сорт/колір:", fill="black", anchor="mm", font=get_font(9, True))
    draw.rectangle([320, 325, 340, 340], fill="#e74c3c", outline=PRIMARY_COLOR, width=2)
    draw.rectangle([360, 325, 380, 340], fill="#2ecc71")
    
    draw.text((300, 380), "Кількість:", fill="black", anchor="mm", font=get_font(9, True))
    draw.rounded_rectangle([340, 368, 390, 392], 3, fill="white")
    draw.text((365, 380), "1", fill="black", anchor="mm", font=get_font(10))
    
    draw.rounded_rectangle([270, 430, 430, 470], 50, fill="#2ecc71")
    draw.text((350, 450), "Додати в кошик", fill="#ffffff", anchor="mm", font=get_font(11, True))
    
    draw.rounded_rectangle([520, 60, 835, 550], 10, fill=SIDEBAR_COLOR)
    draw.text((677, 80), "Відгуки та оцінки:", fill="black", anchor="mm", font=get_font(11, True))
    draw.text((677, 110), "Рейтинг: ***** (5.0/5)", fill="#f1c40f", anchor="mm", font=get_font(10, True))
    
    draw.rounded_rectangle([535, 140, 820, 190], 5, fill="white")
    draw.text((545, 155), "• Yarik: Дуже смачний!", fill="black", font=get_font(9))
    
    img.save("screenshot_details_v6.png")
    print("Created mockup: screenshot_details_v6.png")

def create_cart_screenshot():
    w, h = 850, 580
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_custom_sidebar(draw, "Кошик")
    
    draw.rounded_rectangle([200, 20, 500, 550], 10, fill=SIDEBAR_COLOR)
    draw.text((350, 40), "Кошик (грн)", fill=PRIMARY_COLOR, anchor="mm", font=get_font(12, True))
    
    draw.rounded_rectangle([215, 70, 485, 120], 6, fill="white")
    draw.text((225, 95), "Хліб Київхліб x1", fill="black", anchor="lm", font=get_font(9, True))
    draw.text((370, 95), "22 грн", fill="#2e7d32", anchor="lm", font=get_font(9, True))
    draw.rounded_rectangle([455, 85, 475, 105], 3, fill="#e74c3c")
    draw.text((465, 95), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    draw.rounded_rectangle([215, 130, 485, 180], 6, fill="white")
    draw.text((225, 155), "Сир Пирятин x1.5 кг", fill="black", anchor="lm", font=get_font(9, True))
    draw.text((370, 155), "165 грн", fill="#2e7d32", anchor="lm", font=get_font(9, True))
    draw.rounded_rectangle([455, 145, 475, 165], 3, fill="#e74c3c")
    draw.text((465, 155), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    draw.text((350, 460), "Сума: 187 грн", fill="black", anchor="mm", font=get_font(9, True))
    draw.text((350, 490), "Разом: 187 грн", fill=PRIMARY_COLOR, anchor="mm", font=get_font(11, True))
    draw.rounded_rectangle([280, 510, 420, 535], 50, fill="#95a5a6")
    draw.text((350, 522), "Очистити кошик", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([520, 20, 835, 550], 10, fill=SIDEBAR_COLOR)
    draw.text((677, 40), "Дані для доставки", fill="black", anchor="mm", font=get_font(11, True))
    
    fields = ["Номер телефону (+380...)", "Електронна пошта (Email)", "Адреса доставки", "Courier", "Balance"]
    for i, val in enumerate(fields):
        y = 80 + i * 55
        draw.rounded_rectangle([535, y, 820, y + 35], 5, fill="white", outline=PRIMARY_COLOR, width=1)
        draw.text((545, y + 17), val, fill="gray", anchor="lm", font=get_font(9))
        
    draw.rounded_rectangle([550, 450, 800, 495], 50, fill="#2ecc71")
    draw.text((677, 472), "Оформити", fill="#ffffff", anchor="mm", font=get_font(12, True))
    
    img.save("screenshot_cart_v6.png")
    print("Created mockup: screenshot_cart_v6.png")

if __name__ == "__main__":
    create_main_screenshot()
    create_details_screenshot()
    create_cart_screenshot()
