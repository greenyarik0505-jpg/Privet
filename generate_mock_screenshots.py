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

def draw_custom_sidebar(draw, active_nav):
    # Прямоугольный сайдбар без скругления слева
    draw.rectangle([0, 0, 180, 550], fill=SIDEBAR_COLOR)
    
    # Круглый аватар пользователя
    draw.ellipse([50, 25, 130, 105], fill="#EBE8F9")
    draw.ellipse([70, 38, 110, 78], outline=PRIMARY_COLOR, width=3)
    draw.arc([58, 70, 122, 115], start=0, end=180, fill=PRIMARY_COLOR, width=3)
    
    # Кнопки навигации
    navs = [
        ("DashBoard", "DashBoard"),
        ("Checkout", "Checkout"),
        ("Categories", "Categories"),
        ("History", "History"),
        ("Setting", "Setting")
    ]
    for i, (name, key) in enumerate(navs):
        y = 140 + i * 42
        is_active = (key == active_nav)
        bg = "white" if is_active else SIDEBAR_COLOR
        draw.rounded_rectangle([15, y, 175, y + 32], 6, fill=bg)
        draw.text((25, y + 16), name, fill="black", anchor="lm", font=get_font(11, is_active))
        
    # Logout кнопка внизу
    draw.text((25, 510), "Logout", fill="black", anchor="lm", font=get_font(11))

def create_main_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Сайдбар
    draw_custom_sidebar(draw, "DashBoard")
    
    # Длинное скругленное фиолетовое поле поиска
    draw.rounded_rectangle([200, 15, 735, 45], 15, fill=SEARCH_BAR_COLOR)
    draw.text((467, 30), "Search", fill="white", anchor="mm", font=get_font(11))
    
    # Заголовок "Categories"
    draw.text((200, 65), "Categories", fill="black", font=get_font(12, True))
    
    # Горизонтальные блоки категорий
    categories = [
        ("Bakeries", "#C2D6EE", "Bread.png"),
        ("Drinks", "#BCE6EB", "Diet_Cola.png"),
        ("Vegetables", "#ECC4EC", "Salad.png"),
        ("Fruits", "#D3EEC2", "Apple.png"),
        ("Snacks", "#DCD2EE", "Potato_Chips.png")
    ]
    for i, (cat, bg, img_file) in enumerate(categories):
        x = 200 + i * 106
        draw.rounded_rectangle([x, 85, x + 96, 155], 10, fill=bg)
        prod_img = get_product_image_by_filename(img_file, (36, 36))
        img.paste(prod_img, (x + 30, 93), prod_img if prod_img.mode == "RGBA" else None)
        draw.text((x + 48, 142), cat, fill="black", anchor="mm", font=get_font(10, False))
        
    # Заголовок "Popular Items" с пагинацией (1-5 из 105)
    draw.text((200, 175), "Popular Items (1-5 / 105)", fill="black", font=get_font(12, True))
    
    # Карточки товаров Popular Items (Украинские и международные гиганты)
    products = [
        ("Хліб", "0.6kg", "$22.00", "Bread.png"),
        ("Кока-Кола", "0.5l", "$28.00", "Diet_Cola.png"),
        ("Сир", "0.2kg", "$110.00", "Cheese.png"),
        ("Чіпси", "0.1kg", "$48.00", "Potato_Chips.png"),
        ("Смарт", "0.1kg", "$1200.00", "sport.png")
    ]
    
    for i, (name, weight, price, img_file) in enumerate(products):
        x = 200 + i * 106
        y = 195
        # Белый фон с круглыми углами
        draw.rounded_rectangle([x, y, x + 96, y + 135], 10, fill="white")
        
        # Картинка
        prod_img = get_product_image_by_filename(img_file, (50, 50))
        img.paste(prod_img, (x + 23, y + 10), prod_img if prod_img.mode == "RGBA" else None)
        
        # Название и вес на одной строке
        draw.text((x + 8, y + 78), name, fill="black", font=get_font(9))
        draw.text((x + 88, y + 78), weight, fill="gray", anchor="rt", font=get_font(8))
        
        # Цена и кнопка (+) на одной строке
        draw.text((x + 8, y + 108), price, fill="black", font=get_font(9, True))
        draw.ellipse([x + 68, y + 98, x + 88, y + 118], fill="black")
        draw.text((x + 78, y + 108), "+", fill="white", anchor="mm", font=get_font(10, True))
        
    # Кнопки пагинации в самом низу
    draw.rounded_rectangle([200, 480, 300, 510], 6, fill=PRIMARY_COLOR)
    draw.text((250, 495), "← Назад", fill="white", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([635, 480, 735, 510], 6, fill=PRIMARY_COLOR)
    draw.text((685, 495), "Далі →", fill="white", anchor="mm", font=get_font(9, True))
    
    draw.text((467, 495), "Page 1 of 3", fill="black", anchor="mm", font=get_font(10, True))
        
    img.save("screenshot_main_v6.png")
    print("Created mockup: screenshot_main_v6.png")

def create_details_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_custom_sidebar(draw, "DashBoard")
    
    draw.rounded_rectangle([200, 15, 270, 40], 5, fill=PRIMARY_COLOR)
    draw.text((235, 27), "← Назад", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([200, 60, 460, 520], 10, fill=SIDEBAR_COLOR)
    
    prod_img = get_product_image_by_filename("Bread.png", (120, 120))
    img.paste(prod_img, (270, 80), prod_img if prod_img.mode == "RGBA" else None)
    
    draw.text((330, 220), "Хліб Київхліб", fill="black", anchor="mm", font=get_font(12, True))
    draw.text((330, 250), "Свіжий український хліб.", fill="black", anchor="mm", font=get_font(9, True))
    draw.text((330, 275), "Ціна: $22.00", fill=PRIMARY_COLOR, anchor="mm", font=get_font(12, True))
    
    draw.text((330, 310), "Виберіть сорт/колір:", fill="black", anchor="mm", font=get_font(9, True))
    draw.rectangle([300, 325, 320, 340], fill="#e74c3c", outline=PRIMARY_COLOR, width=2)
    draw.rectangle([340, 325, 360, 340], fill="#2ecc71")
    
    draw.text((280, 380), "Кількість:", fill="black", anchor="mm", font=get_font(9, True))
    draw.rounded_rectangle([320, 368, 370, 392], 3, fill="white")
    draw.text((345, 380), "1", fill="black", anchor="mm", font=get_font(10))
    
    draw.rounded_rectangle([250, 430, 410, 470], 50, fill="#2ecc71")
    draw.text((330, 450), "Додати в кошик", fill="#ffffff", anchor="mm", font=get_font(11, True))
    
    draw.rounded_rectangle([480, 60, 730, 520], 10, fill=SIDEBAR_COLOR)
    draw.text((605, 80), "Відгуки та оцінки:", fill="black", anchor="mm", font=get_font(11, True))
    draw.text((605, 110), "Рейтинг: ***** (5.0/5)", fill="#f1c40f", anchor="mm", font=get_font(10, True))
    
    draw.rounded_rectangle([495, 140, 715, 190], 5, fill="white")
    draw.text((505, 155), "• Yarik: Дуже смачний!", fill="black", font=get_font(9))
    
    img.save("screenshot_details_v6.png")
    print("Created mockup: screenshot_details_v6.png")

def create_cart_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    draw_custom_sidebar(draw, "Checkout")
    
    draw.rounded_rectangle([200, 20, 460, 520], 10, fill=SIDEBAR_COLOR)
    draw.text((330, 40), "Кошик товарів (POS)", fill=PRIMARY_COLOR, anchor="mm", font=get_font(12, True))
    
    draw.rounded_rectangle([215, 70, 445, 120], 6, fill="white")
    draw.text((225, 95), "Хліб Київхліб x1", fill="black", anchor="lm", font=get_font(9, True))
    draw.text((350, 95), "$22.00", fill="#2e7d32", anchor="lm", font=get_font(9, True))
    draw.rounded_rectangle([415, 85, 435, 105], 3, fill="#e74c3c")
    draw.text((425, 95), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    draw.rounded_rectangle([215, 130, 445, 180], 6, fill="white")
    draw.text((225, 155), "Кока-Кола x2", fill="black", anchor="lm", font=get_font(9, True))
    draw.text((350, 155), "$56.00", fill="#2e7d32", anchor="lm", font=get_font(9, True))
    draw.rounded_rectangle([415, 145, 435, 165], 3, fill="#e74c3c")
    draw.text((425, 155), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    draw.text((330, 440), "Сума: $78.00", fill="black", anchor="mm", font=get_font(9, True))
    draw.text((330, 470), "Разом: $78.00", fill=PRIMARY_COLOR, anchor="mm", font=get_font(11, True))
    draw.rounded_rectangle([260, 490, 400, 515], 50, fill="#95a5a6")
    draw.text((330, 502), "Очистити кошик", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([480, 20, 730, 520], 10, fill=SIDEBAR_COLOR)
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
