import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# Спробуємо отримати стандартний шрифт, щоб не було тофу
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
    draw.rectangle([0, 0, 180, 750], fill="#252538")
    
    # Логотип
    draw.text((20, 30), "МЕГАМАРКЕТ", fill="#cdd6f4", font=get_font(12, True))
    
    # Профіль
    draw.text((20, 75), f"Користувач: {user}", fill="#cdd6f4", font=get_font(10, True))
    draw.text((20, 95), balance, fill="#2ecc71", font=get_font(11, True))
    
    # Кнопка поповнення
    draw.rounded_rectangle([20, 120, 160, 145], 5, fill="#2ecc71")
    draw.text((90, 132), "+ Поповнити", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    # Навігаційні кнопки
    navs = ["Каталог", "Кошик", "Аналітика", "Історія", "Налаштування"]
    for i, nav in enumerate(navs):
        y = 180 + i * 40
        is_active = (nav == active_nav)
        bg = "#3498db" if is_active else "#252538"
        draw.rounded_rectangle([15, y, 165, y + 30], 4, fill=bg)
        draw.text((25, y + 15), nav, fill="#ffffff", anchor="lm", font=get_font(10))
        
    # Вихід
    draw.rounded_rectangle([15, 680, 165, 710], 4, fill="#e74c3c")
    draw.text((90, 695), "Вийти", fill="#ffffff", anchor="mm", font=get_font(10, True))

def create_main_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), "#1e1e2e")
    draw = ImageDraw.Draw(img)
    
    # Сайдбар
    draw_custom_sidebar(draw, "Каталог")
    
    # Верхня панель (Пошук, фільтр)
    draw.rounded_rectangle([200, 15, 340, 43], 5, fill="#252538", outline="#45475a")
    draw.text((210, 29), "Пошук...", fill="#a6adc8", anchor="lm", font=get_font(9))
    
    categories = ["Усі", "Випічка", "Молочне", "Фрукти", "Напої", "Снеки"]
    for i, cat in enumerate(categories):
        x = 355 + i * 50
        bg_col = "#3498db" if i == 0 else "#252538"
        draw.rounded_rectangle([x, 15, x + 44, 43], 4, fill=bg_col)
        draw.text((x + 22, 29), cat, fill="#ffffff", anchor="mm", font=get_font(8, True))
        
    draw.rounded_rectangle([660, 15, 735, 43], 4, fill="#252538")
    draw.text((697, 29), "Дешевші", fill="#ffffff", anchor="mm", font=get_font(8))
    
    # Товари в сітці
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
        cx = 200 + col * 178
        cy = 70 + row * 225
        
        # Картка товару
        draw.rounded_rectangle([cx, cy, cx + 165, cy + 215], 8, fill="#252538", outline="#45475a")
        
        draw.text((cx + 140, cy + 20), "Liked" if i == 0 else "Like", fill="red" if i == 0 else "gray", anchor="mm", font=get_font(9))
        
        # Картинка товару
        prod_img = get_product_image_by_filename(img_file, (65, 65))
        img.paste(prod_img, (cx + 50, cy + 25), prod_img if prod_img.mode == "RGBA" else None)
        
        # Текст
        draw.text((cx + 82, cy + 115), name[:22], fill="#cdd6f4", anchor="mm", font=get_font(9, True))
        draw.text((cx + 82, cy + 135), f"{price}", fill="#2ecc71", anchor="mm", font=get_font(9))
        
        # Кнопка детальніше
        draw.rounded_rectangle([cx + 25, cy + 165, cx + 140, cy + 195], 5, fill="#3498db")
        draw.text((cx + 82, cy + 180), "Детальніше", fill="#ffffff", anchor="mm", font=get_font(9, True))
        
    img.save("screenshot_main_v6.png")
    print("Created mockup: screenshot_main_v6.png")

def create_details_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), "#1e1e2e")
    draw = ImageDraw.Draw(img)
    
    # Сайдбар
    draw_custom_sidebar(draw, "Каталог")
    
    # Кнопка назад
    draw.rounded_rectangle([200, 15, 270, 40], 5, fill="#252538")
    draw.text((235, 27), "← Назад", fill="#ffffff", anchor="mm", font=get_font(9))
    
    # Ліва панель (Опис)
    draw.rounded_rectangle([200, 60, 460, 520], 10, fill="#252538", outline="#45475a")
    
    prod_img = get_product_image_by_filename("Apple.png", (120, 120))
    img.paste(prod_img, (270, 80), prod_img if prod_img.mode == "RGBA" else None)
    
    draw.text((330, 220), "Яблука Гала", fill="#cdd6f4", anchor="mm", font=get_font(12, True))
    draw.text((330, 250), "Свіжі хрусткі яблука сорту Гала.", fill="#a6adc8", anchor="mm", font=get_font(9, True))
    draw.text((330, 275), "Ціна: 45 грн/шт", fill="#2ecc71", anchor="mm", font=get_font(12, True))
    
    draw.text((330, 310), "Виберіть сорт/колір:", fill="#cdd6f4", anchor="mm", font=get_font(9, True))
    draw.rectangle([300, 325, 320, 340], fill="#e74c3c", outline="#3498db", width=2)
    draw.rectangle([340, 325, 360, 340], fill="#2ecc71")
    
    draw.text((280, 380), "Кількість:", fill="#cdd6f4", anchor="mm", font=get_font(9))
    draw.rounded_rectangle([320, 368, 370, 392], 3, fill="#1e1e2e")
    draw.text((345, 380), "1", fill="#ffffff", anchor="mm", font=get_font(10))
    
    draw.rounded_rectangle([250, 430, 410, 470], 6, fill="#2ecc71")
    draw.text((330, 450), "Додати в кошик", fill="#ffffff", anchor="mm", font=get_font(11, True))
    
    # Права панель (Відгуки)
    draw.rounded_rectangle([480, 60, 730, 520], 10, fill="#252538", outline="#45475a")
    draw.text((605, 80), "Відгуки та оцінки:", fill="#cdd6f4", anchor="mm", font=get_font(11, True))
    draw.text((605, 110), "Рейтинг: ***** (5.0/5)", fill="#f1c40f", anchor="mm", font=get_font(10, True))
    
    draw.rounded_rectangle([495, 140, 715, 190], 5, fill="#1e1e2e")
    draw.text((505, 155), "• Yarik: Супер солодкі!", fill="#cdd6f4", font=get_font(9))
    
    img.save("screenshot_details_v6.png")
    print("Created mockup: screenshot_details_v6.png")

def create_cart_screenshot():
    w, h = 750, 550
    img = Image.new("RGB", (w, h), "#1e1e2e")
    draw = ImageDraw.Draw(img)
    
    # Сайдбар
    draw_custom_sidebar(draw, "Кошик")
    
    # Ліва панель (Список кошика)
    draw.rounded_rectangle([200, 20, 460, 520], 10, fill="#252538", outline="#45475a")
    draw.text((330, 40), "Кошик товарів (POS)", fill="#cdd6f4", anchor="mm", font=get_font(12, True))
    
    # Елемент кошика 1
    draw.rounded_rectangle([215, 70, 445, 120], 6, fill="#1e1e2e")
    draw.text((225, 95), "Яблука Гала x1", fill="#ffffff", anchor="lm", font=get_font(9, True))
    draw.text((350, 95), "45 грн", fill="#2ecc71", anchor="lm", font=get_font(9))
    draw.rounded_rectangle([415, 85, 435, 105], 3, fill="#e74c3c")
    draw.text((425, 95), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    # Елемент кошика 2
    draw.rounded_rectangle([215, 130, 445, 180], 6, fill="#1e1e2e")
    draw.text((225, 155), "Сир Чеддер x2", fill="#ffffff", anchor="lm", font=get_font(9, True))
    draw.text((350, 155), "220 грн", fill="#2ecc71", anchor="lm", font=get_font(9))
    draw.rounded_rectangle([415, 145, 435, 165], 3, fill="#e74c3c")
    draw.text((425, 155), "X", fill="#ffffff", anchor="mm", font=get_font(8))
    
    # Підсумок
    draw.text((330, 440), "Сума: 265 грн", fill="#a6adc8", anchor="mm", font=get_font(9))
    draw.text((330, 470), "Разом: 265 грн", fill="#2ecc71", anchor="mm", font=get_font(11, True))
    draw.rounded_rectangle([260, 490, 400, 515], 4, fill="#95a5a6")
    draw.text((330, 502), "Очистити кошик", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    # Права панель (Оформлення доставки)
    draw.rounded_rectangle([480, 20, 730, 520], 10, fill="#252538", outline="#45475a")
    draw.text((605, 40), "Дані для доставки", fill="#cdd6f4", anchor="mm", font=get_font(11, True))
    
    fields = ["Номер телефону (+380...)", "Електронна пошта (Email)", "Адреса доставки", "Courier", "Balance"]
    for i, val in enumerate(fields):
        y = 80 + i * 50
        draw.rounded_rectangle([495, y, 715, y + 35], 5, fill="#1e1e2e", outline="#45475a")
        draw.text((505, y + 17), val, fill="#a6adc8", anchor="lm", font=get_font(9))
        
    draw.rounded_rectangle([510, 430, 700, 475], 6, fill="#2ecc71")
    draw.text((605, 452), "Оформити", fill="#ffffff", anchor="mm", font=get_font(12, True))
    
    img.save("screenshot_cart_v6.png")
    print("Created mockup: screenshot_cart_v6.png")

if __name__ == "__main__":
    create_main_screenshot()
    create_details_screenshot()
    create_cart_screenshot()
