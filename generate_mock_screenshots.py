from PIL import Image, ImageDraw, ImageFont
import os

FONT_PATH = "C:\\Windows\\Fonts\\segoeui.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:\\Windows\\Fonts\\arial.ttf"

def get_font(size, bold=False):
    if bold:
        bold_path = "C:\\Windows\\Fonts\\segoeuib.ttf"
        if os.path.exists(bold_path):
            try: return ImageFont.truetype(bold_path, size)
            except: pass
        arial_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
        if os.path.exists(arial_bold):
            try: return ImageFont.truetype(arial_bold, size)
            except: pass
            
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def create_main_screenshot():
    w, h = 600, 750
    img = Image.new("RGB", (w, h), "#f8f9fa")
    draw = ImageDraw.Draw(img)
    
    # Хедер
    draw.rectangle([0, 0, w, 45], fill="#ffffff", outline="#e0e0e0", width=1)
    draw.text((15, 22), "👤 Yarik", fill="#212529", anchor="lm", font=get_font(10, True))
    draw.text((90, 22), "Баланс: 1000 грн", fill="#2e7d32", anchor="lm", font=get_font(10, True))
    draw.rounded_rectangle([190, 10, 280, 35], 3, fill="#2ecc71")
    draw.text((235, 22), "+ Поповнити", fill="#ffffff", anchor="mm", font=get_font(8, True))
    
    draw.text((w - 90, 22), "UA", fill="#4a90e2", anchor="mm", font=get_font(9, True))
    draw.text((w - 60, 22), "EN", fill="#888888", anchor="mm", font=get_font(9))
    draw.text((w - 30, 22), "RU", fill="#888888", anchor="mm", font=get_font(9))
    
    # Керування
    draw.rounded_rectangle([15, 60, 100, 85], 4, fill="#95a5a6")
    draw.text((57, 72), "📜 Історія", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    draw.rounded_rectangle([110, 60, 260, 85], 4, fill="#f1c40f")
    draw.text((185, 72), "🎡 Колесо Фортуни", fill="#2c3e50", anchor="mm", font=get_font(9, True))
    
    # Заголовок
    draw.text((w//2, 125), "Мегамаркет Все-в-Одному", fill="#212529", anchor="mm", font=get_font(22, True))
    
    # Пошук
    draw.rounded_rectangle([w//2 - 180, 155, w//2 + 180, 185], 5, outline="#212529", width=1, fill="#ffffff")
    draw.text((w//2 - 170, 170), "🔍 Пошук:", fill="#212529", anchor="lm", font=get_font(11, True))
    
    # Категорії
    categories = ["Усі", "Техніка", "Фрукти", "Для дому", "Спорт", "Одяг"]
    for i, cat in enumerate(categories):
        x = w//2 - 170 + i * 65
        bg_col = "#4a90e2" if i == 0 else "#e0e0e0"
        fg_col = "#ffffff" if i == 0 else "#212529"
        draw.rounded_rectangle([x - 28, 200, x + 28, 222], 3, fill=bg_col)
        draw.text((x, 211), cat, fill=fg_col, anchor="mm", font=get_font(9, True))
        
    # Сортування
    draw.rounded_rectangle([w//2 - 60, 235, w//2 + 60, 255], 3, fill="#e0e0e0")
    draw.text((w//2, 245), "⇅ Сортування", fill="#212529", anchor="mm", font=get_font(9, True))
    
    # Товари
    products = [
        ("Ноутбук Pro-1", "15200 грн/шт", True),
        ("Яблуко Голден-1", "20 грн/шт", False),
        ("Лампа Loft-1", "315 грн/шт", True),
        ("Футбольний М'яч-1", "410 грн/шт", False),
        ("Футболка Класик-1", "255 грн/шт", False),
        ("Ноутбук Pro-2", "15400 грн/шт", False)
    ]
    
    products.sort(key=lambda x: 0 if x[2] else 1)
    
    for i, (name, price, is_fav) in enumerate(products):
        row = i // 3
        col = i % 3
        cx = 50 + col * 175
        cy = 280 + row * 165
        
        draw.rounded_rectangle([cx, cy, cx + 150, cy + 145], 8, fill="#ffffff", outline="#e0e0e0", width=1)
        
        heart = "❤️" if is_fav else "🤍"
        draw.text((cx + 135, cy + 15), heart, fill="red" if is_fav else "#888", anchor="mm", font=get_font(11))
        
        draw.text((cx + 75, cy + 40), "📸", fill="#888888", anchor="mm", font=get_font(20))
        draw.text((cx + 75, cy + 80), name, fill="#212529", anchor="mm", font=get_font(11, True))
        draw.text((cx + 75, cy + 100), price, fill="#2e7d32", anchor="mm", font=get_font(10))
        
        draw.rounded_rectangle([cx + 25, cy + 115, cx + 125, cy + 135], 4, fill="#4a90e2")
        draw.text((cx + 75, cy + 125), "Детальніше", fill="#ffffff", anchor="mm", font=get_font(9, True))
        
    draw.rounded_rectangle([w//2 - 150, 670, w//2 + 150, 720], 6, fill="#2c3e50")
    draw.text((w//2, 695), "🛒 Переглянути Кошик (0 шт.)", fill="#ffffff", anchor="mm", font=get_font(14, True))
    
    img.save("screenshot_main_v3.png")
    print("Created mockup: screenshot_main_v3.png")

def create_details_screenshot():
    w, h = 380, 520
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    draw.text((w//2, 50), "📸", fill="#888888", anchor="mm", font=get_font(30))
    draw.text((w//2, 120), "Ноутбук Pro-1", fill="#212529", anchor="mm", font=get_font(18, True))
    draw.text((w//2, 145), "Високопродуктивний ноутбук Pro версії", fill="#6c757d", anchor="mm", font=get_font(10))
    draw.text((w//2, 170), "Ціна: 15200 грн/шт", fill="#2e7d32", anchor="mm", font=get_font(12, True))
    
    draw.text((w//2, 205), "Виберіть сорт/колір:", fill="#212529", anchor="mm", font=get_font(11, True))
    colors = ["#bdc3c7", "#2c3e50"]
    for i, hex_color in enumerate(colors):
        x = w//2 - 35 + i * 40
        y = 220
        if i == 0:
            draw.rectangle([x - 2, y - 2, x + 32, y + 22], outline="#4a90e2", width=2)
        draw.rectangle([x, y, x + 30, y + 20], fill=hex_color)
        
    draw.text((w//2 - 40, 280), "Кількість:", fill="#212529", anchor="mm", font=get_font(11, True))
    draw.rounded_rectangle([w//2 + 10, 265, w//2 + 60, 295], 3, outline="#cccccc", fill="#ffffff")
    draw.text((w//2 + 35, 280), "1", fill="#212529", anchor="mm", font=get_font(11))
    
    draw.rounded_rectangle([w//2 - 90, 320, w//2 + 90, 360], 6, fill="#2ecc71")
    draw.text((w//2, 340), "Додати в кошик", fill="#ffffff", anchor="mm", font=get_font(12, True))
    
    draw.text((20, 390), "Відгуки та оцінки:", fill="#2c3e50", anchor="lm", font=get_font(11, True))
    draw.text((20, 415), "Рейтинг: ★★★★★ (5.0/5)", fill="#f1c40f", anchor="lm", font=get_font(10, True))
    draw.text((20, 440), "• Yarik (5★): Чудовий швидкий ноутбук!", fill="#555555", anchor="lm", font=get_font(9))
    
    img.save("screenshot_details_v3.png")
    print("Created mockup: screenshot_details_v3.png")

def create_cart_screenshot():
    w, h = 420, 520
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)
    
    draw.text((w//2, 30), "🛒 Список товарів", fill="#212529", anchor="mm", font=get_font(16, True))
    
    # Товар 1
    draw.rounded_rectangle([15, 60, w - 15, 100], 4, fill="#f8f9fa")
    draw.text((30, 80), "Ноутбук Pro-1 (Сріблястий) x1", fill="#212529", anchor="lm", font=get_font(11, True))
    draw.text((250, 80), "15200 грн", fill="#555555", anchor="lm", font=get_font(11))
    draw.rectangle([w - 45, 70, w - 25, 90], fill="#ff4d4d")
    draw.text((w - 35, 80), "❌", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    # Товар 2
    draw.rounded_rectangle([15, 110, w - 15, 150], 4, fill="#f8f9fa")
    draw.text((30, 130), "Лампа Loft-1 (Чорний) x2", fill="#212529", anchor="lm", font=get_font(11, True))
    draw.text((250, 130), "630 грн", fill="#555555", anchor="lm", font=get_font(11))
    draw.rectangle([w - 45, 120, w - 25, 140], fill="#ff4d4d")
    draw.text((w - 35, 130), "❌", fill="#ffffff", anchor="mm", font=get_font(9, True))
    
    # Знижка
    draw.text((w//2, 210), "Сума: 15830 грн", fill="#555555", anchor="mm", font=get_font(11))
    draw.text((w//2, 235), "Знижка (10%): -1583 грн", fill="#ff4d4d", anchor="mm", font=get_font(11))
    draw.text((w//2, 270), "Разом до сплати: 14247 грн", fill="#2e7d32", anchor="mm", font=get_font(14, True))
    
    # Кнопки
    draw.rounded_rectangle([60, 360, 200, 400], 4, fill="#95a5a6")
    draw.text((130, 380), "Очистити кошик", fill="#ffffff", anchor="mm", font=get_font(11, True))
    
    draw.rounded_rectangle([220, 360, 360, 400], 4, fill="#2ecc71")
    draw.text((290, 400), "Оформити", fill="#ffffff", anchor="mm", font=get_font(11, True))
    
    img.save("screenshot_cart_v3.png")
    print("Created mockup: screenshot_cart_v3.png")

if __name__ == "__main__":
    create_main_screenshot()
    create_details_screenshot()
    create_cart_screenshot()
    print("All upgraded megamarket mock screenshots generated successfully!")
