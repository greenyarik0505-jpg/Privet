import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import os
import urllib.request
import urllib.parse
import datetime
import random
import math
import threading

# Налаштування стилю (Світла тема, як у convenientshop)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Глобальні налаштування
sound_enabled = True
active_lang = "ua"
current_theme = "light"  # "light" або "dark"
logged_in_user = None
session_discount = 0.0
cart = []
SESSION_FILE = "session.txt"

import sys
def resource_path(relative_path):
    """ Отримує абсолютний шлях до ресурсів, сумісний з PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

ASSETS_DIR = resource_path("assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# ── Палітра тем ──
THEMES = {
    "light": {
        "bg":        "#F0EFF9",
        "sidebar":   "#E5E4F3",
        "hover":     "#D7D2F4",
        "search":    "#8A96EC",
        "text":      "black",
        "text_sec":  "#555",
        "card_bg":   "#FFFFFF",
        "btn_text":  "white",
    },
    "dark": {
        "bg":        "#1E1E2E",
        "sidebar":   "#2A2A3E",
        "hover":     "#3A3A5C",
        "search":    "#3D3D6B",
        "text":      "white",
        "text_sec":  "#AAAACC",
        "card_bg":   "#2D2D44",
        "btn_text":  "white",
    },
}

# Активні кольори (ініціалізуються зі світлої теми)
PRIMARY_COLOR    = "#4F46E5"
BG_COLOR         = THEMES["light"]["bg"]
SIDEBAR_COLOR    = THEMES["light"]["sidebar"]
HOVER_COLOR      = THEMES["light"]["hover"]
SEARCH_BAR_COLOR = THEMES["light"]["search"]

CARD_COLORS = [
    "#7DABDE",  # Синій
    "#87D7E0",  # Циан
    "#EA7BBE",  # Рожевий
    "#BCEAA5",  # Ніжно-зелений
    "#B9A5EA",  # Пурпурний
    "#EAA5A6"   # Ніжно-червоний
]

def play_sound(action):
    pass

import market_db
market_db.init_db()

# Словник локалізації (Українська, Англійська, Російська)
LANGS = {
    "ua": {
        "search_placeholder": "Пошук продуктів...",
        "categories": "Категорії",
        "popular_items": "Популярні товари",
        "new_items": "Нові надходження",
        "add_to_cart_success": "Додано в кошик!",
        "back_btn": "← Назад",
        "details_title": "Деталі товару",
        "price_lbl": "Ціна:",
        "color_lbl": "Виберіть сорт/колір:",
        "qty_lbl": "Кількість:",
        "add_to_cart_btn": "Додати в кошик",
        "reviews_lbl": "Відгуки та оцінки:",
        "rating_lbl": "Рейтинг:",
        "submit_review_btn": "Надіслати",
        "cart_title": "Кошик товарів",
        "cart_empty": "Кошик порожній",
        "total_lbl": "Разом до сплати:",
        "checkout_btn": "Оформити замовлення",
        "clear_cart_btn": "Очистити кошик",
        "delivery_title": "Дані для доставки",
        "phone_lbl": "Номер телефону (+380...)",
        "email_lbl": "Електронна пошта (Email)",
        "address_lbl": "Адреса доставки",
        "history_title": "Історія замовлень",
        "no_orders": "Замовлень ще не було",
        "settings_title": "Налаштування",
        "lang_lbl": "Мова інтерфейсу:",
        "theme_lbl": "Тема оформлення (Фіксовано):",
        "sound_lbl": "Звукові ефекти",
        "login_title": "ВХІД",
        "register_title": "РЕЄСТРАЦІЯ",
        "username_placeholder": "введіть логін",
        "password_placeholder": "введіть пароль",
        "confirm_password_placeholder": "підтвердіть пароль",
        "show_password": "Показати пароль",
        "login_btn": "Увійти",
        "register_btn": "Зареєструватися",
        "dont_have_account": "Немає акаунту?",
        "already_have_account": "Вже є акаунт?",
        "balance_lbl": "Баланс:",
        "topup_btn": "+ Поповнити",
        "logout_btn": "Вийти",
        "next_btn": "Далі →",
        "prev_btn": "← Назад"
    },
    "en": {
        "search_placeholder": "Search products...",
        "categories": "Categories",
        "popular_items": "Popular Items",
        "new_items": "New Items",
        "add_to_cart_success": "Added to cart!",
        "back_btn": "← Back",
        "details_title": "Product Details",
        "price_lbl": "Price:",
        "color_lbl": "Select variety/color:",
        "qty_lbl": "Quantity:",
        "add_to_cart_btn": "Add to Cart",
        "reviews_lbl": "Reviews & Ratings:",
        "rating_lbl": "Rating:",
        "submit_review_btn": "Submit",
        "cart_title": "Cart",
        "cart_empty": "Cart is empty",
        "total_lbl": "Total to pay:",
        "checkout_btn": "Checkout",
        "clear_cart_btn": "Clear Cart",
        "delivery_title": "Delivery details",
        "phone_lbl": "Phone number (+380...)",
        "email_lbl": "Email Address",
        "address_lbl": "Delivery Address",
        "history_title": "Order History",
        "no_orders": "No orders yet",
        "settings_title": "Settings",
        "lang_lbl": "Language:",
        "theme_lbl": "Theme (Fixed):",
        "sound_lbl": "Sound Effects",
        "login_title": "LOGIN",
        "register_title": "REGISTER",
        "username_placeholder": "enter username",
        "password_placeholder": "enter password",
        "confirm_password_placeholder": "confirm password",
        "show_password": "Show password",
        "login_btn": "Login",
        "register_btn": "Register",
        "dont_have_account": "Don't have an account?",
        "already_have_account": "Already have an account?",
        "balance_lbl": "Balance:",
        "topup_btn": "+ Top Up",
        "logout_btn": "Logout",
        "next_btn": "Next →",
        "prev_btn": "← Prev"
    },
    "ru": {
        "search_placeholder": "Поиск продуктов...",
        "categories": "Категории",
        "popular_items": "Популярные товары",
        "new_items": "Новые поступления",
        "add_to_cart_success": "Добавлено в корзину!",
        "back_btn": "← Назад",
        "details_title": "Детали товара",
        "price_lbl": "Цена:",
        "color_lbl": "Выберите сорт/цвет:",
        "qty_lbl": "Количество:",
        "add_to_cart_btn": "Добавить в корзину",
        "reviews_lbl": "Отзывы и оценки:",
        "rating_lbl": "Рейтинг:",
        "submit_review_btn": "Отправить",
        "cart_title": "Корзина товаров",
        "cart_empty": "Корзина пуста",
        "total_lbl": "Итого к оплате:",
        "checkout_btn": "Оформить заказ",
        "clear_cart_btn": "Очистить корзину",
        "delivery_title": "Данные для доставки",
        "phone_lbl": "Номер телефона (+380...)",
        "email_lbl": "Электронная почта (Email)",
        "address_lbl": "Адрес доставки",
        "history_title": "История заказов",
        "no_orders": "Заказов еще не было",
        "settings_title": "Настройки",
        "lang_lbl": "Язык интерфейса:",
        "theme_lbl": "Тема оформления (Фиксированно):",
        "sound_lbl": "Звуковые эффекты",
        "login_title": "ВХОД",
        "register_title": "РЕГИСТРАЦИЯ",
        "username_placeholder": "введите логин",
        "password_placeholder": "введите пароль",
        "confirm_password_placeholder": "подтвердите пароль",
        "show_password": "Показать пароль",
        "login_btn": "Войти",
        "register_btn": "Зарегистрироваться",
        "dont_have_account": "Нет аккаунта?",
        "already_have_account": "Уже есть аккаунт?",
        "balance_lbl": "Баланс:",
        "topup_btn": "+ Пополнить",
        "logout_btn": "Выйти",
        "next_btn": "Далее →",
        "prev_btn": "← Назад"
    }
}

def t(key):
    return LANGS[active_lang].get(key, key)

CONVENIENT_IMAGES = [
    "Apple.png", "Avocado.png", "Bread.png", "Cheese.png", 
    "Chocolate Bar.png", "Diet_Cola.png", "Energy Drink - Red.png", 
    "Orange Juice.png", "Potato_Chips.png", "Salad.png", "Strawberries.png", 
    "Water.png", "Orange.png", "Single Banana.png", "English_Muffins.png", 
    "Honey Wheat Sliced Bread.png", "Flour_Tortillas.png", "Single Plain Bagel.png", 
    "Shake.png", "Oatemeal_Cip.png", "Gum.png", "Salted Peanuts.png", 
    "Sparkling Water.png", "sport.png", "default.png"
]

def download_assets_worker():
    # Точні посилання на реальні українські товари (Prom.ua / Rozetka)
    ua_urls = {
        "Bread.png": "https://images.prom.ua/1595166416_w640_h640_baton-kievhleb.jpg",
        "Shake.png": "https://images.prom.ua/2202685717_w640_h640_yogurt-galichina-klubnika.jpg",
        "Cheese.png": "https://images.prom.ua/4214647321_w640_h640_syr-pyryatin-korol.jpg",
        "Water.png": "https://images.prom.ua/3522253303_w640_h640_voda-morshinskaya-negazirovannaya.jpg",
        "Chocolate Bar.png": "https://images.prom.ua/4106511210_w640_h640_shokolad-roshen-molochnyj.jpg",
        "Salted Peanuts.png": "https://content2.rozetka.com.ua/goods/images/big/284988456.jpg"
    }
    
    # Спочатку скачуємо реальні українські бренди
    for name, url in ua_urls.items():
        dest = os.path.join(ASSETS_DIR, name)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(dest, 'wb') as f:
                    f.write(response.read())
        except Exception:
            pass

    # Решта картинок скачуються з convenientshop
    base_url = "https://raw.githubusercontent.com/SecureAuditX/convenientshop/main/images/"
    for name in CONVENIENT_IMAGES:
        if name in ua_urls: continue
        dest = os.path.join(ASSETS_DIR, name)
        if not os.path.exists(dest):
            try:
                encoded_name = urllib.parse.quote(name)
                url = f"{base_url}{encoded_name}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    with open(dest, 'wb') as f:
                        f.write(response.read())
            except Exception:
                img = Image.new("RGBA", (128, 128), (46, 204, 113, 255))
                img.save(dest)

threading.Thread(target=download_assets_worker, daemon=True).start()

CACHE_DIR = resource_path("cache_images")
os.makedirs(CACHE_DIR, exist_ok=True)

def translate_product_name(name_ua, target_lang):
    if target_lang == "ua":
        return name_ua
        
    words_map = {
        "en": {
            "хліб": "Bread", "батон": "Baton", "булка": "Bun", "круасан": "Croissant",
            "багет": "Baguette", "лаваш": "Pita", "вода": "Water", "сік": "Juice",
            "кола": "Cola", "кока-кола": "Coca-Cola", "фанта": "Fanta", "квас": "Kvas",
            "напій": "Drink", "лимонад": "Lemonade", "енергетик": "Energy", "сир": "Cheese",
            "йогурт": "Yogurt", "молоко": "Milk", "вершки": "Cream", "сметана": "Sour Cream",
            "чіпси": "Chips", "шоколад": "Chocolate", "цукерки": "Candies", "арахіс": "Peanuts",
            "печиво": "Cookies", "сухарики": "Croutons", "вафлі": "Waffles", "яблуко": "Apple",
            "банан": "Banana", "полуниця": "Strawberry", "апельсин": "Orange", "лимон": "Lemon",
            "виноград": "Grapes", "груша": "Pear", "помідор": "Tomato", "огірок": "Cucumber",
            "салат": "Salad", "картопля": "Potato", "морква": "Carrot", "капуста": "Cabbage",
            "цибуля": "Onion", "годинник": "Watch", "браслет": "Band", "скакалка": "Rope",
            "навушники": "Earbuds", "ваги": "Scales", "пульсометр": "HR Monitor",
            "негазована": "still", "газована": "sparkling", "слабогазована": "lightly sparkling",
            "білий": "white", "чорний": "black", "молочний": "milk", "свіжий": "fresh",
            "ваговий": "by weight", "королівський": "royal", "київхліб": "Kyivkhlib",
            "тарас": "Taras", "галичина": "Galychyna", "пирятин": "Pyryatyn", "сандора": "Sandora",
            "боржомі": "Borjomi", "рошен": "Roshen", "козацька розвага": "Kozatska Rozvaha", "орбіт": "Orbit"
        },
        "ru": {
            "хліб": "Хлеб", "батон": "Батон", "булка": "Булка", "круасан": "Круассан",
            "багет": "Багет", "лаваш": "Лаваш", "вода": "Вода", "сік": "Сок",
            "кола": "Кола", "кока-кола": "Кока-Кола", "фанта": "Фанта", "квас": "Квас",
            "напій": "Напиток", "лимонад": "Лимонад", "енергетик": "Энергетик", "сир": "Сыр",
            "йогурт": "Йогурт", "молоко": "Молоко", "вершки": "Сливки", "сметана": "Сметана",
            "чіпси": "Чипсы", "шоколад": "Шоколад", "цукерки": "Конфеты", "арахіс": "Арахис",
            "печиво": "Печенье", "сухарики": "Сухарики", "вафлі": "Вафли", "яблуко": "Яблоко",
            "банан": "Банан", "полуниця": "Клубника", "апельсин": "Апельсин", "лимон": "Лимон",
            "виноград": "Виноград", "груша": "Груша", "помідор": "Помидор", "огірок": "Огурец",
            "салат": "Салат", "картопля": "Картошка", "морква": "Морковь", "капуста": "Капуста",
            "цибуля": "Лук", "годинник": "Часы", "браслет": "Браслет", "скакалка": "Скакалка",
            "навушники": "Наушники", "ваги": "Весы", "пульсометр": "Пульсометр",
            "негазована": "негазированная", "газована": "газированная", "слабогазована": "слабогазированная",
            "білий": "белый", "чорний": "черный", "молочний": "молочный", "свіжий": "свежий",
            "ваговий": "весовой", "королівський": "королевский", "київхліб": "Киевхлеб",
            "тарас": "Тарас", "галичина": "Галычина", "пирятин": "Пирятин", "сандора": "Сандора",
            "боржомі": "Боржоми", "рошен": "Рошен", "козацька розвага": "Козацька розвага", "орбіт": "Орбит"
        }
    }
    
    translated = name_ua.lower()
    mapping = words_map.get(target_lang, {})
    for ua_word, target_word in mapping.items():
        translated = re.sub(r'\b' + re.escape(ua_word) + r'\b', target_word, translated)
        translated = translated.replace(ua_word, target_word)
        
    if translated:
        translated = translated[0].upper() + translated[1:]
    return translated

import numpy as np

# Кеш для CTkImage об'єктів, щоб не зчитувати й не обробляти зображення щоразу з диска
_product_image_cache = {}

def remove_white_bg(img, threshold=230):
    """Replace near-white pixels with transparent — removes white background from product images using numpy (fast)."""
    try:
        img = img.convert("RGBA")
        arr = np.array(img)
        # Маска для пікселів, де R, G, B канали більше за поріг
        mask = (arr[:, :, 0] > threshold) & (arr[:, :, 1] > threshold) & (arr[:, :, 2] > threshold)
        arr[mask, 3] = 0  # робимо прозорими
        img = Image.fromarray(arr)
    except Exception:
        pass
    return img

from PIL import ImageDraw
def remove_white_bg_floodfill(img, threshold=240):
    """Видаляє білий фон навколо об'єкта методом Flood Fill (заливка від кутів), не чіпаючи білий колір всередині."""
    try:
        img = img.convert("RGBA")
        width, height = img.size
        gray = img.convert("L")
        
        # Запускаємо floodfill з кожного кута
        for start_point in [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]:
            x, y = start_point
            val = gray.getpixel((x, y))
            if val > threshold:
                ImageDraw.floodfill(img, start_point, (0, 0, 0, 0), thresh=255-threshold)
    except Exception:
        pass
    return img

def get_product_image_local(img_src, size):
    cache_key = (img_src, size)
    if cache_key in _product_image_cache:
        return _product_image_cache[cache_key]

    # Якщо це віддалена URL-адреса з CDN Сільпо
    if img_src.startswith("http://") or img_src.startswith("https://"):
        filename = img_src.split("/")[-1].split("?")[0]
        dest = os.path.join(CACHE_DIR, filename)
        if os.path.exists(dest):
            try:
                from PIL import ImageEnhance, ImageFilter
                img = Image.open(dest)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                # Робимо зображення чітким, щоб текст на упаковках легко читалися
                img = remove_white_bg(img)
                img = img.filter(ImageFilter.SHARPEN)
                enh = ImageEnhance.Sharpness(img)
                img = enh.enhance(2.2)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                _product_image_cache[cache_key] = ctk_img
                return ctk_img
            except Exception:
                pass
        
        # Фонове завантаження зображення
        def download_img(url=img_src, dst=dest):
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=10) as response:
                    with open(dst, "wb") as f:
                        f.write(response.read())
            except Exception:
                pass
        threading.Thread(target=download_img, daemon=True).start()
        
        fallback_dest = os.path.join(ASSETS_DIR, "default.png")
        if os.path.exists(fallback_dest):
            try:
                from PIL import ImageEnhance, ImageFilter
                img = Image.open(fallback_dest)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                img = img.filter(ImageFilter.SHARPEN)
                enh = ImageEnhance.Sharpness(img)
                img = enh.enhance(2.0)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                _product_image_cache[cache_key] = ctk_img
                return ctk_img
            except Exception:
                pass
        img = Image.new("RGBA", size, (149, 165, 166, 255))
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
        _product_image_cache[cache_key] = ctk_img
        return ctk_img
    else:
        # Локальні асети
        dest = os.path.join(ASSETS_DIR, img_src)
        if os.path.exists(dest):
            try:
                from PIL import ImageEnhance, ImageFilter
                img = Image.open(dest)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                img = remove_white_bg(img)
                img = img.filter(ImageFilter.SHARPEN)
                enh = ImageEnhance.Sharpness(img)
                img = enh.enhance(2.0)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                _product_image_cache[cache_key] = ctk_img
                return ctk_img
            except Exception:
                pass
        fallback_dest = os.path.join(ASSETS_DIR, "default.png")
        if os.path.exists(fallback_dest):
            try:
                from PIL import ImageEnhance, ImageFilter
                img = Image.open(fallback_dest)
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA")
                img = remove_white_bg(img)
                img = img.filter(ImageFilter.SHARPEN)
                enh = ImageEnhance.Sharpness(img)
                img = enh.enhance(2.0)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
                _product_image_cache[cache_key] = ctk_img
                return ctk_img
            except Exception:
                pass
        img = Image.new("RGBA", size, (149, 165, 166, 255))
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
        _product_image_cache[cache_key] = ctk_img
        return ctk_img


# Продукти: Завантажуємо 250+ повністю унікальних товарів прямо з Сільпо
fruits_data = {}
try:
    import sys
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        
    import silpo_products
    for idx, item in enumerate(silpo_products.products):
        if item["category"] in ["sport", "vegetables"]:
            continue
        key_name = item["names"]["en"]
        
        # Робимо назви товарів строго українською мовою
        ua_name = item["names"]["ua"]
        item["names"]["en"] = ua_name
        item["names"]["ru"] = ua_name
        
        fruits_data[key_name] = item
except Exception as e:
    import traceback
    try:
        messagebox.showerror("Помилка імпорту Сільпо", f"Не вдалося завантажити базу товарів silpo_products.py:\n{e}\n\nСпробуйте запустити додаток через консоль у правильній папці.\n\nTraceback:\n{traceback.format_exc()}")
    except Exception:
        pass
    # Запасний варіант, якщо імпорт не вдався
    fruits_data = {
        "Gala Apples": {
            "names": {"ua": "Яблука Гала", "en": "Gala Apples", "ru": "Яблоки Гала"},
            "price": 45, "desc": "Свіжі яблука.", "category": "fruits", "image": "Apple.png",
            "weight": "1 кг", "unit": "kg", "section": "popular", "colors": [("Стандарт", "#4F46E5")]
        }
    }

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1240x820")
        self.title("Silpo")
        
        self.container = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.container.pack(fill="both", expand=True)
        
        self.current_screen = None
        self.check_auto_login()

    def check_auto_login(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    username = f.read().strip()
                if username:
                    global logged_in_user
                    logged_in_user = username
                    self.show_main_screen()
                    return
            except Exception:
                pass
        self.show_auth_screen()

    def show_screen(self, screen_class, *args, **kwargs):
        if self.current_screen:
            self.current_screen.pack_forget()
            self.current_screen.destroy()
        
        self.current_screen = screen_class(self.container, self, *args, **kwargs)
        self.current_screen.pack(fill="both", expand=True)

    def show_auth_screen(self):
        self.show_screen(AuthScreen)

    def show_main_screen(self):
        self.show_screen(MainScreen)

class ResetPasswordWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Відновлення паролю")
        self.geometry("380x380")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)
        
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        
        lbl_title = ctk.CTkLabel(self, text="Відновлення паролю", font=("Arial", 18, "bold"), text_color=PRIMARY_COLOR)
        lbl_title.pack(pady=15)
        
        ctk.CTkLabel(self, text="Введіть логін (Username):", font=("Arial", 11, "bold"), text_color=THEMES[current_theme]["text"]).pack(anchor="w", padx=40, pady=(10, 2))
        self.user_entry = ctk.CTkEntry(self, width=300, fg_color=THEMES[current_theme]["card_bg"], text_color=THEMES[current_theme]["text"])
        self.user_entry.pack(padx=40, pady=2)
        
        ctk.CTkLabel(self, text="Введіть пошту (Email):", font=("Arial", 11, "bold"), text_color=THEMES[current_theme]["text"]).pack(anchor="w", padx=40, pady=(10, 2))
        self.email_entry = ctk.CTkEntry(self, width=300, fg_color=THEMES[current_theme]["card_bg"], text_color=THEMES[current_theme]["text"])
        self.email_entry.pack(padx=40, pady=2)
        
        ctk.CTkLabel(self, text="Введіть новий пароль:", font=("Arial", 11, "bold"), text_color=THEMES[current_theme]["text"]).pack(anchor="w", padx=40, pady=(10, 2))
        self.pass_entry = ctk.CTkEntry(self, show="*", width=300, fg_color=THEMES[current_theme]["card_bg"], text_color=THEMES[current_theme]["text"])
        self.pass_entry.pack(padx=40, pady=2)
        
        self.btn_reset = ctk.CTkButton(self, text="Змінити пароль", command=self.reset_password, font=("Arial", 13, "bold"), fg_color=PRIMARY_COLOR, hover_color="#4338CA")
        self.btn_reset.pack(pady=25, padx=40, fill="x")
        
    def reset_password(self):
        username = self.user_entry.get().strip()
        email = self.email_entry.get().strip()
        new_pass = self.pass_entry.get().strip()
        
        if not username or not email or not new_pass:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі поля!")
            return
            
        if len(new_pass) < 4:
            play_sound("error")
            messagebox.showerror("Помилка", "Пароль має бути не менше 4 символів!")
            return
            
        if market_db.verify_and_reset_password(username, email, new_pass):
            play_sound("success")
            messagebox.showinfo("Успіх", "Пароль успішно оновлено! Увійдіть з новим паролем.")
            self.destroy()
        else:
            play_sound("error")
            messagebox.showerror("Помилка", "Користувача з такою комбінацією логіну та пошти не знайдено!")

# --- ЕКРАН АВТОРИЗАЦІЇ ---
class AuthScreen(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = app_controller
        
        self.card = ctk.CTkFrame(self, corner_radius=16, width=800, height=660, fg_color=BG_COLOR)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_columnconfigure(1, weight=1)
        
        self.left_branding_frame = ctk.CTkFrame(self.card, fg_color=BG_COLOR)
        self.left_branding_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        self.left_canvas = tk.Canvas(self.left_branding_frame, width=240, height=340, bg=BG_COLOR, bd=0, highlightthickness=0)
        self.left_canvas.pack(fill="both", expand=True)
        self.draw_vector_graphics()
        
        self.login_frame = ctk.CTkFrame(self.card, fg_color=SIDEBAR_COLOR, corner_radius=20, width=380, height=590)
        self.login_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=35)
        self.login_frame.pack_propagate(False)
        
        self.is_register_mode = False
        self.draw_auth_content()

    def draw_auth_content(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()
            
        title_key = "register_title" if self.is_register_mode else "login_title"
        self.lbl_title = ctk.CTkLabel(self.login_frame, text=t(title_key), font=("Arial", 36, "bold"), text_color=PRIMARY_COLOR)
        self.lbl_title.pack(pady=(20, 15))
        
        user_lbl_text = "USERNAME" if self.is_register_mode else "USERNAME / EMAIL"
        if self.is_register_mode:
            placeholder = t("username_placeholder")
        else:
            if active_lang == "ua":
                placeholder = "введіть логін або пошту"
            elif active_lang == "ru":
                placeholder = "введите логин или почту"
            else:
                placeholder = "enter username or email"
                
        self.user_lbl = ctk.CTkLabel(self.login_frame, text=user_lbl_text, font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR, anchor="w")
        self.user_lbl.pack(fill="x", padx=45, pady=(5, 2))
        
        self.user_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text=placeholder, font=("Arial", 14), 
            width=290, height=45, fg_color=PRIMARY_COLOR, text_color="white", 
            placeholder_text_color=SIDEBAR_COLOR, border_color=PRIMARY_COLOR, 
            corner_radius=10, border_width=2
        )
        self.user_entry.pack(padx=40, pady=(0, 10))
        
        if self.is_register_mode:
            self.email_lbl = ctk.CTkLabel(self.login_frame, text="EMAIL", font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR, anchor="w")
            self.email_lbl.pack(fill="x", padx=45, pady=(5, 2))
            self.email_entry = ctk.CTkEntry(
                self.login_frame, placeholder_text="Введіть пошту...", font=("Arial", 14), 
                width=290, height=45, fg_color=PRIMARY_COLOR, text_color="white", 
                placeholder_text_color=SIDEBAR_COLOR, border_color=PRIMARY_COLOR, 
                corner_radius=10, border_width=2
            )
            self.email_entry.pack(padx=40, pady=(0, 10))
        
        self.pass_lbl = ctk.CTkLabel(self.login_frame, text="PASSWORD", font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR, anchor="w")
        self.pass_lbl.pack(fill="x", padx=45, pady=(5, 2))
        
        self.pass_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text=t("password_placeholder"), show="*", font=("Arial", 14), 
            width=290, height=45, fg_color=PRIMARY_COLOR, text_color="white", 
            placeholder_text_color=SIDEBAR_COLOR, border_color=PRIMARY_COLOR, 
            corner_radius=10, border_width=2
        )
        self.pass_entry.pack(padx=40, pady=(0, 5))
        
        if self.is_register_mode:
            self.confirm_pass_lbl = ctk.CTkLabel(self.login_frame, text="CONFIRM PASSWORD", font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR, anchor="w")
            self.confirm_pass_lbl.pack(fill="x", padx=45, pady=(5, 2))
            self.confirm_pass_entry = ctk.CTkEntry(
                self.login_frame, placeholder_text=t("confirm_password_placeholder"), show="*", font=("Arial", 14), 
                width=290, height=45, fg_color=PRIMARY_COLOR, text_color="white", 
                placeholder_text_color=SIDEBAR_COLOR, border_color=PRIMARY_COLOR, 
                corner_radius=10, border_width=2
            )
            self.confirm_pass_entry.pack(padx=40, pady=(0, 5))
            
        action_key = "register_btn" if self.is_register_mode else "login_btn"
        self.btn_action = ctk.CTkButton(
            self.login_frame, text=t(action_key), command=self.handle_action, 
            width=290, height=45, font=("Arial", 20, "bold"), 
            fg_color=PRIMARY_COLOR, hover_color="#4338CA", text_color="white", 
            corner_radius=50
        )
        self.btn_action.pack(padx=40, pady=(15, 10))
        
        self.toggle_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.toggle_frame.pack(pady=(5, 20))
        
        toggle_lbl_key = "already_have_account" if self.is_register_mode else "dont_have_account"
        self.toggle_lbl = ctk.CTkLabel(self.toggle_frame, text=t(toggle_lbl_key), font=("Arial", 12), text_color=PRIMARY_COLOR)
        self.toggle_lbl.pack(side="left", padx=2)
        
        toggle_btn_text = "Login" if self.is_register_mode else "Register"
        self.btn_toggle = ctk.CTkButton(
            self.toggle_frame, text=toggle_btn_text, command=self.toggle_mode, 
            fg_color="transparent", text_color=PRIMARY_COLOR, hover_color=None, 
            width=60, height=20, font=("Arial", 12, "underline"), cursor="hand2"
        )
        self.btn_toggle.pack(side="left")
        
        self.show_pass_var = tk.BooleanVar(value=False)
        self.chk_show_pass = ctk.CTkCheckBox(self.login_frame, text=t("show_password"), variable=self.show_pass_var, command=self.toggle_password_visibility, font=("Arial", 10), text_color=PRIMARY_COLOR, border_color=PRIMARY_COLOR)
        self.chk_show_pass.pack(pady=2)
        
        if not self.is_register_mode:
            self.btn_forgot = ctk.CTkButton(
                self.login_frame, text="Забули пароль?", command=self.forgot_password,
                fg_color="transparent", text_color="gray", hover_color=None,
                width=100, height=20, font=("Arial", 11, "underline"), cursor="hand2"
            )
            self.btn_forgot.pack(pady=5)

    def toggle_mode(self):
        play_sound("click")
        self.is_register_mode = not self.is_register_mode
        self.draw_auth_content()

    def handle_action(self):
        if self.is_register_mode:
            self.try_register()
        else:
            self.try_login()

    def try_login(self):
        username_or_email = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not username_or_email or not password:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі поля!")
            return
            
        matched_user = market_db.login_user(username_or_email, password)
        if matched_user:
            global logged_in_user
            logged_in_user = matched_user
            try:
                with open(SESSION_FILE, "w", encoding="utf-8") as f:
                    f.write(matched_user)
            except Exception:
                pass
            play_sound("success")
            self.controller.show_main_screen()
        else:
            play_sound("error")
            messagebox.showerror("Помилка", "Невірний логін або пароль!")

    def try_register(self):
        username = self.user_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.pass_entry.get().strip()
        c_password = self.confirm_pass_entry.get().strip()
        
        if not username or not email or not password or not c_password:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі поля!")
            return
            
        if "@" not in email or "." not in email:
            play_sound("error")
            messagebox.showerror("Помилка", "Некоректний формат електронної пошти!")
            return
            
        if password != c_password:
            play_sound("error")
            messagebox.showerror("Помилка", "Паролі не співпадають!")
            return
            
        if market_db.register_user(username, password, email):
            play_sound("success")
            messagebox.showinfo("Успіх", "Користувач зареєстрований! Увійдіть.")
            self.toggle_mode()
        else:
            play_sound("error")
            messagebox.showerror("Помилка", "Такий логін вже існує!")

    def toggle_password_visibility(self):
        show_char = "" if self.show_pass_var.get() else "*"
        self.pass_entry.configure(show=show_char)
        if self.is_register_mode:
            self.confirm_pass_entry.configure(show=show_char)

    def forgot_password(self):
        ResetPasswordWindow(self)

    def draw_vector_graphics(self):
        self.left_canvas.delete("all")
        self.left_canvas.create_oval(50, 90, 190, 230, fill=SIDEBAR_COLOR, outline="")
        self.left_canvas.create_oval(30, 70, 42, 82, outline="#00f2fe", width=2)
        self.left_canvas.create_polygon(210, 80, 220, 95, 200, 95, outline="#2ecc71", fill="", width=2)
        self.left_canvas.create_polygon(25, 230, 35, 245, 15, 245, outline="#e74c3c", fill="", width=2)
        self.left_canvas.create_oval(215, 240, 225, 250, outline="#3498db", width=2)
        
        self.left_canvas.create_rectangle(90, 125, 150, 165, fill=BG_COLOR, outline=PRIMARY_COLOR, width=2)
        self.left_canvas.create_polygon(80, 165, 160, 165, 165, 172, 75, 172, fill=SIDEBAR_COLOR, outline=PRIMARY_COLOR, width=2)
        self.left_canvas.create_line(115, 170, 125, 170, fill=PRIMARY_COLOR, width=2)
        self.left_canvas.create_oval(115, 133, 125, 143, fill="", outline=PRIMARY_COLOR, width=2)
        self.left_canvas.create_arc(107, 145, 133, 165, start=0, extent=180, style="arc", outline=PRIMARY_COLOR, width=2)

# --- ФЕЙКОВА ПЛАТІЖНА СТОРІНКА (МОДАЛЬНЕ ВІКНО) ---
class FakePaymentWindow(ctk.CTkToplevel):
    def __init__(self, parent, amount, on_success_callback):
        super().__init__(parent)
        self.title("Банківський переказ - Безпечна оплата")
        self.geometry("420x450")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)
        
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        self.grab_set()
        
        self.amount = amount
        self.on_success = on_success_callback
        
        bank_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR, height=60, corner_radius=0)
        bank_frame.pack(fill="x")
        
        lbl_bank = ctk.CTkLabel(bank_frame, text="🛡️ MegaBank Secure Pay", font=("Arial", 16, "bold"), text_color="white")
        lbl_bank.pack(pady=15)
        
        lbl_amount_title = ctk.CTkLabel(self, text="Сума до сплати:", font=("Arial", 11), text_color=("#333333", "#E0E0E0"))
        lbl_amount_title.pack(pady=(15, 0))
        
        lbl_amount = ctk.CTkLabel(self, text=f"{amount} грн", font=("Arial", 22, "bold"), text_color=("#2e7d32", "#4ADE80"))
        lbl_amount.pack(pady=(0, 8))
        
        btn_quick = ctk.CTkButton(
            self, text="⚡ Заповнити тестові дані", font=("Arial", 10, "bold"),
            fg_color="#3b82f6", hover_color="#2563eb", height=24, corner_radius=12,
            command=self.fill_test_data
        )
        btn_quick.pack(pady=(0, 10))
        
        card_frame = ctk.CTkFrame(self, fg_color=("white", "#2D2D44"), corner_radius=10)
        card_frame.pack(padx=20, pady=5, fill="both", expand=True)
        
        ctk.CTkLabel(card_frame, text="Номер картки:", font=("Arial", 10, "bold"), text_color=("black", "white")).pack(anchor="w", padx=15, pady=(10, 2))
        self.card_entry = ctk.CTkEntry(card_frame, placeholder_text="4441  1111  2222  3333", fg_color=("#F3F4F6", "#1E1E2E"), text_color=("black", "white"), placeholder_text_color=("gray50", "gray60"), border_width=0, height=32)
        self.card_entry.pack(fill="x", padx=15, pady=2)
        
        row_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        row_frame.pack(fill="x", padx=15, pady=(10, 2))
        
        col1 = ctk.CTkFrame(row_frame, fg_color="transparent")
        col1.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(col1, text="Термін дії:", font=("Arial", 10, "bold"), text_color=("black", "white")).pack(anchor="w")
        self.exp_entry = ctk.CTkEntry(col1, placeholder_text="MM/YY", fg_color=("#F3F4F6", "#1E1E2E"), text_color=("black", "white"), placeholder_text_color=("gray50", "gray60"), border_width=0, height=32)
        self.exp_entry.pack(fill="x", pady=2)
        
        col2 = ctk.CTkFrame(row_frame, fg_color="transparent")
        col2.pack(side="right", fill="x", expand=True, padx=(10, 0))
        ctk.CTkLabel(col2, text="CVV:", font=("Arial", 10, "bold"), text_color=("black", "white")).pack(anchor="w")
        self.cvv_entry = ctk.CTkEntry(col2, placeholder_text="•••", show="•", fg_color=("#F3F4F6", "#1E1E2E"), text_color=("black", "white"), placeholder_text_color=("gray50", "gray60"), border_width=0, height=32)
        self.cvv_entry.pack(fill="x", pady=2)
        
        ctk.CTkLabel(card_frame, text="Власник картки:", font=("Arial", 10, "bold"), text_color=("black", "white")).pack(anchor="w", padx=15, pady=(10, 2))
        self.name_entry = ctk.CTkEntry(card_frame, placeholder_text="IVAN IVANOV", fg_color=("#F3F4F6", "#1E1E2E"), text_color=("black", "white"), placeholder_text_color=("gray50", "gray60"), border_width=0, height=32)
        self.name_entry.pack(fill="x", padx=15, pady=(2, 15))
        
        self.btn_pay = ctk.CTkButton(self, text="Підтвердити оплату", command=self.process_payment, font=("Arial", 13, "bold"), fg_color="#2ecc71", hover_color="#27ae60", height=38, corner_radius=19)
        self.btn_pay.pack(pady=15, padx=20, fill="x")
        
    def fill_test_data(self):
        self.card_entry.delete(0, "end")
        self.card_entry.insert(0, "4441 1111 2222 3333")
        self.exp_entry.delete(0, "end")
        self.exp_entry.insert(0, "12/30")
        self.cvv_entry.delete(0, "end")
        self.cvv_entry.insert(0, "123")
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, "TEST USER")

    def process_payment(self):
        card = self.card_entry.get().replace(" ", "")
        exp = self.exp_entry.get().strip()
        cvv = self.cvv_entry.get().strip()
        name = self.name_entry.get().strip()
        
        if len(card) < 16 or not exp or len(cvv) < 3 or not name:
            messagebox.showerror("Помилка оплати", "Будь ласка, введіть коректні дані картки!")
            return
            
        self.btn_pay.configure(state="disabled", text="Обробка платежу...")
        self.update()
        self.after(1500, self.complete_payment)
        
    def complete_payment(self):
        self.destroy()
        self.on_success()

# --- ГОЛОВНИЙ ЕКРАН З БІЧНОЮ НАВІГАЦІЄЮ ---
class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = app_controller
        
        self.sidebar = ctk.CTkFrame(self, width=210, fg_color=SIDEBAR_COLOR, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.avatar_canvas = tk.Canvas(self.sidebar, width=130, height=130, bg=SIDEBAR_COLOR, bd=0, highlightthickness=0)
        self.avatar_canvas.pack(pady=(20, 10))
        self.draw_profile_avatar()
        
        self.balance_lbl = ctk.CTkLabel(self.sidebar, text="0 грн", font=("Arial", 11, "bold"), text_color="#2ecc71")
        self.balance_lbl.pack(pady=2)
        
        self.btn_topup = ctk.CTkButton(self.sidebar, text=t("topup_btn"), command=self.topup_balance, width=110, height=24, font=("Arial", 9, "bold"), fg_color=PRIMARY_COLOR, hover_color="#4338CA")
        self.btn_topup.pack(pady=5)
        
        self.nav_buttons = {}
        self.draw_navigation()
        
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.active_panel = None
        self.show_catalog()
        self.update_profile_info()

    def toggle_theme_to(self, new_theme):
        global current_theme, BG_COLOR, SIDEBAR_COLOR, HOVER_COLOR, SEARCH_BAR_COLOR
        current_theme = new_theme
        ctk.set_appearance_mode(current_theme)  # Синхронізуємо режим з CustomTkinter
        th = THEMES[current_theme]
        BG_COLOR         = th["bg"]
        SIDEBAR_COLOR    = th["sidebar"]
        HOVER_COLOR      = th["hover"]
        SEARCH_BAR_COLOR = th["search"]

        self.configure(fg_color=BG_COLOR)
        self.sidebar.configure(fg_color=SIDEBAR_COLOR)
        self.avatar_canvas.configure(bg=SIDEBAR_COLOR)
        self.draw_profile_avatar()

        for btn in self.nav_buttons.values():
            btn.configure(
                fg_color="transparent",
                text_color=th["text"],
                hover_color=HOVER_COLOR,
            )
        
        self.btn_logout.configure(text_color=th["text"], hover_color=HOVER_COLOR)
        self.btn_delete_acc.configure(hover_color="#ffe5e5" if current_theme == "light" else "#3d2020")

        active_panel_name = "DashBoard"
        if isinstance(self.active_panel, CartPanel): active_panel_name = "Checkout"
        elif isinstance(self.active_panel, AnalyticsPanel): active_panel_name = "Categories"
        elif isinstance(self.active_panel, HistoryPanel): active_panel_name = "History"
        elif isinstance(self.active_panel, SettingsPanel): active_panel_name = "Settings"
        self.update_sidebar_state(active_panel_name)

        self.balance_lbl.configure(text_color="#2ecc71")

        if isinstance(self.active_panel, CatalogPanel):
            self.show_catalog()
        elif isinstance(self.active_panel, CartPanel):
            self.show_cart()
        elif isinstance(self.active_panel, AnalyticsPanel):
            self.show_analytics()
        elif isinstance(self.active_panel, HistoryPanel):
            self.show_history()


    def draw_navigation(self):
        for btn in self.nav_buttons.values():
            btn.destroy()
        self.nav_buttons.clear()
        
        def get_nav_icon(name):
            path = resource_path(os.path.join("assets", name))
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    return ctk.CTkImage(light_image=img, dark_image=img, size=(20, 20))
                except Exception:
                    pass
            return None
            
        navs = [
            ("DashBoard", "Каталог", self.show_catalog, "cat_icon.png"),
            ("Checkout", "Кошик", self.show_cart, "cart_icon.png"),
            ("Categories", "Аналітика", self.show_analytics, "analytics_icon.png"),
            ("History", "Історія", self.show_history, "history_icon.png"),
            ("Settings", "Налаштування", self.show_settings, "settings_icon.png")
        ]
        for key, display_name, cmd, icon_file in navs:
            btn = ctk.CTkButton(
                self.sidebar, text="  " + display_name, anchor="w", fg_color="transparent", 
                text_color=THEMES[current_theme]["text"], hover_color=HOVER_COLOR, command=cmd, 
                font=("Arial", 14), height=42, corner_radius=6, image=get_nav_icon(icon_file)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.nav_buttons[key] = btn
            
        self.btn_logout = ctk.CTkButton(self.sidebar, text="  Вийти", anchor="w", fg_color="transparent", text_color=THEMES[current_theme]["text"], hover_color=HOVER_COLOR, command=self.logout, font=("Arial", 14), height=42, image=get_nav_icon("logout_icon.png"))
        self.btn_logout.pack(side="bottom", fill="x", padx=15, pady=(5, 20))
        
        self.btn_delete_acc = ctk.CTkButton(self.sidebar, text="Видалити акаунт", anchor="w", fg_color="transparent", text_color="#ff4d4d", hover_color="#ffe5e5", command=self.delete_account, font=("Arial", 14), height=42)
        self.btn_delete_acc.pack(side="bottom", fill="x", padx=15, pady=5)

    def draw_profile_avatar(self):
        # Малюємо фірмовий логотип Сільпо із зображення
        logo_path = os.path.join(ASSETS_DIR, "silpo_logo.png")
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                img = remove_white_bg_floodfill(img, threshold=200)
                img = img.resize((115, 115), Image.Resampling.LANCZOS)
                self.avatar_img = ImageTk.PhotoImage(img)
                self.avatar_canvas.create_image(65, 65, image=self.avatar_img)
                return
            except Exception as e:
                print("Failed to load silpo_logo.png:", e)
        # Резервний малюнок
        self.avatar_canvas.create_oval(15, 15, 115, 115, fill="#FF5E00", outline="")
        self.avatar_canvas.create_text(65, 55, text="С", fill="white", font=("Arial", 56, "bold"))
        self.avatar_canvas.create_text(65, 95, text="сільпо", fill="white", font=("Arial", 14, "bold"))

    def update_sidebar_state(self, active_name):
        cart_count = sum(item["qty"] for item in cart)
        cart_text = f"Кошик ({cart_count})" if cart_count > 0 else "Кошик"
        
        # Активна кнопка — акцентний колір залежно від теми
        active_fg = "#3A3A5C" if current_theme == "dark" else "white"
        active_text = "white" if current_theme == "dark" else "black"
        
        for name, btn in self.nav_buttons.items():
            if name == "Checkout":
                btn.configure(text=cart_text)
            
            if name == active_name:
                btn.configure(fg_color=active_fg, font=("Arial", 14, "bold"),
                              text_color=active_text)
            else:
                btn.configure(fg_color="transparent", font=("Arial", 14),
                              text_color=THEMES[current_theme]["text"])

    def update_profile_info(self):
        balance = market_db.get_balance(logged_in_user)
        self.balance_lbl.configure(text=f"{t('balance_lbl')} {balance} грн")
        if self.active_panel:
            panel_name = "DashBoard"
            if isinstance(self.active_panel, CartPanel): panel_name = "Checkout"
            elif isinstance(self.active_panel, AnalyticsPanel): panel_name = "Categories"
            elif isinstance(self.active_panel, HistoryPanel): panel_name = "History"
            self.update_sidebar_state(panel_name)

    def topup_balance(self):
        def on_success():
            market_db.add_balance(logged_in_user, 500)
            self.update_profile_info()
            messagebox.showinfo("Успіх", "Баланс успішно поповнено на 500 грн!")
            
        FakePaymentWindow(self, 500, on_success)

    def delete_account(self):
        if messagebox.askyesno("Видалення акаунту", "Ви дійсно хочете видалити свій акаунт?"):
            market_db.delete_user(logged_in_user)
            self.logout()

    def logout(self):
        global logged_in_user, cart, session_discount
        logged_in_user = None
        cart = []
        session_discount = 0.0
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except Exception:
                pass
        self.controller.show_auth_screen()

    def switch_panel(self, panel_class, active_name, *args, **kwargs):
        if self.active_panel:
            self.active_panel.pack_forget()
            self.active_panel.destroy()
        self.active_panel = panel_class(self.content_container, self, *args, **kwargs)
        self.active_panel.pack(fill="both", expand=True)
        self.update_sidebar_state(active_name)

    def show_catalog(self):
        self.switch_panel(CatalogPanel, "DashBoard")

    def show_cart(self):
        self.switch_panel(CartPanel, "Checkout")

    def show_analytics(self):
        self.switch_panel(AnalyticsPanel, "Categories")

    def show_history(self):
        self.switch_panel(HistoryPanel, "History")

    def show_settings(self):
        self.switch_panel(SettingsPanel, "Setting")

# --- ПАНЕЛЬ КАТАЛОГУ З ПАГІНАЦІЄЮ ---
class CatalogPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        self.current_page = 0
        self.items_per_page = 15  # 5 стовпців x 3 рядки = 15 унікальних товарів на сторінку
        self.active_cat = "all"
        self.card_vars = {}  # Зберігає вибрану кількість/вагу для кожного товару прямо на картці
        
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 15))
        
        self.search_entry = ctk.CTkEntry(
            search_frame, placeholder_text=t("search_placeholder"), font=("Arial", 14), 
            height=36, fg_color=SEARCH_BAR_COLOR, text_color="white", 
            placeholder_text_color="white", border_width=0, corner_radius=50, justify="center"
        )
        self.search_entry.pack(fill="x", padx=10)
        self.search_entry.bind("<KeyRelease>", self.reset_page_and_filter)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)
        
        # Контейнер для кнопок пагінації внизу
        self.pagination_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pagination_frame.pack(fill="x", pady=10)
        
        self.draw_dashboard()

    def reset_page_and_filter(self, event):
        self.current_page = 0
        self.draw_dashboard()

    def set_category(self, cat):
        self.active_cat = cat
        self.current_page = 0
        self.draw_dashboard()

    def draw_dashboard(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        # Категорії
        lbl_cat_title = ctk.CTkLabel(self.scroll_frame, text=t("categories"), font=("Arial", 16, "bold"), text_color=THEMES[current_theme]["text"])
        lbl_cat_title.pack(anchor="w", padx=10, pady=(5, 5))
        
        cats_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        cats_frame.pack(fill="x", padx=5, pady=5)
        
        categories_data = [
            ("Випічка", "bakeries", "#C2D6EE", "cat_bakeries.png"),
            ("Напої", "drinks", "#BCE6EB", "cat_drinks.png"),
            ("Фрукти", "fruits", "#D3EEC2", "cat_fruits.png"),
            ("Молочні", "dairy", "#FFEAA7", "cat_dairy.png"),
            ("М'ясо & Риба", "meat_fish", "#FFD2D2", "cat_meat_fish.png"),
            ("Бакалія", "grocery", "#FFE4D2", "cat_grocery.png"),
            ("Снеки", "snacks", "#DCD2EE", "cat_snacks.png")
        ]
        
        row1 = ctk.CTkFrame(cats_frame, fg_color="transparent")
        row1.pack(fill="x", pady=2)
        row2 = ctk.CTkFrame(cats_frame, fg_color="transparent")
        row2.pack(fill="x", pady=2)
        
        for i, (name, key, bg_col, img_name) in enumerate(categories_data):
            target_row = row1 if i < 4 else row2
            cat_card = ctk.CTkFrame(target_row, width=130, height=110, fg_color=bg_col, corner_radius=12)
            cat_card.pack(side="left", padx=6, expand=True, fill="both")
            cat_card.pack_propagate(False)
            
            def select_cat(e, k=key):
                self.set_category(k)
            cat_card.bind("<Button-1>", select_cat)
            
            photo = get_product_image_local(img_name, (65, 65))
            img_lbl = ctk.CTkLabel(cat_card, image=photo, text="")
            img_lbl.pack(pady=(8, 2))
            img_lbl.bind("<Button-1>", select_cat)
            
            lbl_cat_name = ctk.CTkLabel(cat_card, text=name, font=("Arial", 11, "bold"), text_color="black")
            lbl_cat_name.pack()
            lbl_cat_name.bind("<Button-1>", select_cat)

        search_query = self.search_entry.get().strip().lower()
        
        # Отримуємо відфільтровані товари
        filtered = []
        for name, data in fruits_data.items():
            if search_query and search_query not in name.lower() and search_query not in data["names"][active_lang].lower(): continue
            if self.active_cat != "all" and data["category"] != self.active_cat: continue
            filtered.append((name, data))
            
        # Пагінація: вираховуємо межі
        total_items = len(filtered)
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_items)
        page_items = filtered[start_idx:end_idx]
        
        # Створюємо секцію товарів
        lbl_pop_title = ctk.CTkLabel(self.scroll_frame, text=f"{t('popular_items')} ({start_idx+1}-{end_idx} / {total_items})", font=("Arial", 16, "bold"), text_color=THEMES[current_theme]["text"])
        lbl_pop_title.pack(anchor="w", padx=10, pady=(15, 5))
        
        grid_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=5)
        
        # 5 колонок в ряду (за замовленням користувача)
        cols = 5
        for c in range(cols):
            grid_frame.grid_columnconfigure(c, weight=1)
            
        col = 0
        row = 0
        for name, data in page_items:
            self.draw_product_card(grid_frame, name, data, row, col)
            col += 1
            if col >= cols:
                col = 0
                row += 1
                
        self.draw_pagination_buttons(total_items)

    def draw_product_card(self, parent_frame, name, data, row, col):
        # Преміальна велика картка (220x310) для HD фотографій
        card = ctk.CTkFrame(parent_frame, corner_radius=12, width=220, height=310, fg_color=THEMES[current_theme]["card_bg"])
        card.grid(row=row, column=col, padx=6, pady=6)
        card.grid_propagate(False)
        
        # Велике HD фото (150x150) за побажанням користувача
        photo = get_product_image_local(data["image"], (150, 150))
        img_lbl = ctk.CTkLabel(card, image=photo, text="")
        img_lbl.pack(pady=(10, 2))
        
        def open_details(e, n=name):
            self.main_screen.switch_panel(DetailsPanel, "DashBoard", n)
        img_lbl.bind("<Button-1>", open_details)
        
        name_frame = ctk.CTkFrame(card, fg_color="transparent")
        name_frame.pack(fill="x", padx=12, pady=(2, 2))
        
        display_name = data["names"][active_lang].split()[0]
        if len(data["names"][active_lang].split()) > 1:
            display_name += " " + data["names"][active_lang].split()[1]
            
        lbl_name = ctk.CTkLabel(name_frame, text=display_name, font=("Arial", 12, "bold"),
            text_color=THEMES[current_theme]["text"], anchor="w", wraplength=140, justify="left")
        lbl_name.pack(side="top", anchor="w")
        lbl_name.bind("<Button-1>", open_details)
        
        lbl_weight = ctk.CTkLabel(name_frame, text=data["weight"], font=("Arial", 10),
            text_color=THEMES[current_theme]["text_sec"], anchor="w")
        lbl_weight.pack(side="top", anchor="w", pady=(2, 0))
        
        # Ініціалізуємо змінну вибору кількості прямо на картці
        if name not in self.card_vars:
            self.card_vars[name] = tk.StringVar(value="1" if data["unit"] == "pcs" else "1.0")
            
        # Панель регулювання кількості/ваги
        ctrl_frame = ctk.CTkFrame(card, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=8, pady=4)
        
        def dec_val(n=name, u=data["unit"]):
            val_str = self.card_vars[n].get()
            if u == "pcs":
                new_v = max(1, int(val_str) - 1)
                self.card_vars[n].set(str(new_v))
            else:
                new_v = max(0.5, float(val_str) - 0.5)
                self.card_vars[n].set(f"{new_v:.1f}")
                
        def inc_val(n=name, u=data["unit"]):
            val_str = self.card_vars[n].get()
            if u == "pcs":
                new_v = int(val_str) + 1
                self.card_vars[n].set(str(new_v))
            else:
                new_v = float(val_str) + 0.5
                self.card_vars[n].set(f"{new_v:.1f}")
                
        btn_dec = ctk.CTkButton(
            ctrl_frame, text="-", command=dec_val, width=22, height=22, 
            corner_radius=11, fg_color="black", text_color="white", 
            font=("Arial", 10, "bold"), hover_color="#333333"
        )
        btn_dec.pack(side="left")
        
        lbl_val = ctk.CTkLabel(ctrl_frame, textvariable=self.card_vars[name], font=("Arial", 11, "bold"),
            text_color=THEMES[current_theme]["text"], width=40)
        lbl_val.pack(side="left", padx=2)
        
        btn_inc = ctk.CTkButton(
            ctrl_frame, text="+", command=inc_val, width=22, height=22, 
            corner_radius=11, fg_color="black", text_color="white", 
            font=("Arial", 10, "bold"), hover_color="#333333"
        )
        btn_inc.pack(side="left")
        
        unit_lbl_text = "шт" if data["unit"] == "pcs" else "кг"
        lbl_unit = ctk.CTkLabel(ctrl_frame, text=unit_lbl_text, font=("Arial", 9, "bold"), text_color="gray")
        lbl_unit.pack(side="right", padx=2)
        
        # Нижня лінія ціни та кнопка «Додати»
        price_frame = ctk.CTkFrame(card, fg_color="transparent")
        price_frame.pack(side="bottom", fill="x", padx=8, pady=6)
        
        lbl_price = ctk.CTkLabel(price_frame, text=f"{data['price']} грн", font=("Arial", 12, "bold"),
            text_color=THEMES[current_theme]["text"], anchor="w")
        lbl_price.pack(side="left")
        
        btn_add = ctk.CTkButton(
            price_frame, text="+ Додати", command=lambda n=name: self.quick_add_to_cart(n), 
            width=65, height=24, corner_radius=12, fg_color=PRIMARY_COLOR, 
            text_color="white", font=("Arial", 10, "bold"), hover_color="#4338CA"
        )
        btn_add.pack(side="right")

    def quick_add_to_cart(self, name):
        data = fruits_data[name]
        try:
            val_str = self.card_vars[name].get()
            qty = int(val_str) if data["unit"] == "pcs" else float(val_str)
            if qty <= 0: raise ValueError
        except ValueError:
            qty = 1
            
        for item in cart:
            if item["name"] == name:
                item["qty"] += qty
                break
        else:
            cart.append({"name": name, "price": data["price"], "qty": qty, "color": data["colors"][0][0]})
            
        play_sound("success")
        self.main_screen.update_profile_info()
        messagebox.showinfo("Успіх", t("add_to_cart_success"))

    def draw_pagination_buttons(self, total_items):
        for widget in self.pagination_frame.winfo_children():
            widget.destroy()
            
        max_pages = math.ceil(total_items / self.items_per_page)
        
        if self.current_page > 0:
            btn_prev = ctk.CTkButton(self.pagination_frame, text=t("prev_btn"), command=self.prev_page, fg_color=PRIMARY_COLOR, hover_color="#4338CA", width=120)
            btn_prev.pack(side="left", padx=20)
            
        if (self.current_page + 1) < max_pages:
            btn_next = ctk.CTkButton(self.pagination_frame, text=t("next_btn"), command=self.next_page, fg_color=PRIMARY_COLOR, hover_color="#4338CA", width=120)
            btn_next.pack(side="right", padx=20)
            
        # Показати номер поточної сторінки посередині
        lbl_page_num = ctk.CTkLabel(self.pagination_frame, text=f"Page {self.current_page + 1} of {max(1, max_pages)}", font=("Arial", 11, "bold"), text_color=("black", "white"))
        lbl_page_num.pack(pady=5)

    def next_page(self):
        play_sound("click")
        self.current_page += 1
        self.draw_dashboard()
        self.scroll_frame._parent_canvas.yview_moveto(0) # Прокрутка до верху сторінки

    def prev_page(self):
        play_sound("click")
        self.current_page -= 1
        self.draw_dashboard()
        self.scroll_frame._parent_canvas.yview_moveto(0)

# --- ПАНЕЛЬ ДЕТАЛЕЙ ТОВАРУ ---
class DetailsPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen, name):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        self.name = name
        self.data = fruits_data[name]
        
        btn_back = ctk.CTkButton(self, text=t("back_btn"), command=lambda: self.main_screen.show_catalog(), width=80, height=28, fg_color=PRIMARY_COLOR, hover_color="#4338CA")
        btn_back.pack(anchor="w", pady=10)
        
        left_box = ctk.CTkFrame(self, corner_radius=12, fg_color=SIDEBAR_COLOR)
        left_box.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        photo = get_product_image_local(self.data["image"], (140, 140))
        self.img_lbl = ctk.CTkLabel(left_box, image=photo, text="")
        self.img_lbl.pack(pady=20)
        
        display_name = self.data["names"][active_lang]
        lbl_title = ctk.CTkLabel(left_box, text=display_name, font=("Arial", 16, "bold"), text_color=THEMES[current_theme]["text"], wraplength=280)
        lbl_title.pack(pady=5)
        
        lbl_desc = ctk.CTkLabel(left_box, text=self.data["desc"], font=("Arial", 12, "italic"), text_color=THEMES[current_theme]["text_sec"], wraplength=280)
        lbl_desc.pack(pady=5)
        
        lbl_price = ctk.CTkLabel(left_box, text=f"{t('price_lbl')} {self.data['price']} грн", font=("Arial", 15, "bold"), text_color=PRIMARY_COLOR)
        lbl_price.pack(pady=10)
        
        # Визначаємо варіанти вибору залежно від категорії
        category = self.data.get("category", "")
        options = []
        selector_label = ""
        
        if category == "bakeries":
            selector_label = "Виберіть нарізку:"
            options = ["Цілий", "Нарізаний"]
        elif category == "drinks":
            selector_label = "Виберіть об'єм:"
            options = ["0.5 л", "1.0 л", "1.5 л"]
        elif category == "dairy":
            selector_label = "Жирність / Вид:"
            options = ["Класичний", "Знежирений"]
            
        self.selected_color = ctk.StringVar(value=options[0] if options else "Стандарт")
        
        if options:
            ctk.CTkLabel(left_box, text=selector_label, font=("Arial", 12, "bold"), text_color=THEMES[current_theme]["text"]).pack(pady=(5, 2))
            seg_button = ctk.CTkSegmentedButton(left_box, values=options, command=lambda v: self.selected_color.set(v), fg_color=BG_COLOR, selected_color=PRIMARY_COLOR, selected_hover_color="#4338CA")
            seg_button.pack(pady=5, padx=10)
            seg_button.set(options[0])
            
        qty_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        qty_frame.pack(pady=10)
        ctk.CTkLabel(qty_frame, text=t("qty_lbl"), text_color=THEMES[current_theme]["text"], font=("Arial", 12, "bold")).pack(side="left", padx=5)
        self.qty_spin = ttk.Spinbox(qty_frame, from_=1, to=50, width=5, font=("Arial", 11), justify="center")
        self.qty_spin.pack(side="left", padx=5)
        self.qty_spin.set(1)
        
        btn_add = ctk.CTkButton(left_box, text=t("add_to_cart_btn"), command=self.add_to_cart, fg_color="#2ecc71", hover_color="#27ae60", font=("Arial", 13, "bold"), corner_radius=50)
        btn_add.pack(pady=10)
        
        right_box = ctk.CTkFrame(self, corner_radius=12, fg_color=SIDEBAR_COLOR)
        right_box.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(right_box, text=t("reviews_lbl"), font=("Arial", 14, "bold"), text_color=THEMES[current_theme]["text"]).pack(pady=10)
        
        self.reviews_frame = ctk.CTkScrollableFrame(right_box, height=220, fg_color=THEMES[current_theme]["bg"])
        self.reviews_frame.pack(fill="both", expand=True, padx=10)
        
        form_frame = ctk.CTkFrame(right_box, fg_color="transparent")
        form_frame.pack(fill="x", padx=10, pady=15)
        
        self.rating_spin = ttk.Spinbox(form_frame, from_=1, to=5, width=3, justify="center")
        self.rating_spin.grid(row=0, column=0, padx=5, pady=5)
        self.rating_spin.set(5)
        
        self.rev_entry = ctk.CTkEntry(form_frame, placeholder_text="Ваш відгук...", width=160, fg_color=THEMES[current_theme]["card_bg"], text_color=THEMES[current_theme]["text"])
        self.rev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        btn_submit = ctk.CTkButton(form_frame, text=t("submit_review_btn"), command=self.submit_review, width=80, fg_color=PRIMARY_COLOR, hover_color="#4338CA")
        btn_submit.grid(row=0, column=2, padx=5, pady=5)
        
        self.refresh_reviews()

    def refresh_reviews(self):
        for w in self.reviews_frame.winfo_children():
            w.destroy()
            
        revs = market_db.get_reviews(self.name)
        if revs:
            avg = sum(r['rating'] for r in revs) / len(revs)
            stars_text = "★" * int(round(avg)) + "☆" * (5 - int(round(avg)))
            ctk.CTkLabel(self.reviews_frame, text=f"{t('rating_lbl')} {stars_text} ({avg:.1f}/5)", font=("Arial", 13, "bold"), text_color="#F1C40F").pack(anchor="w", pady=(0, 10))
            for r in revs[-5:]:
                card = ctk.CTkFrame(self.reviews_frame, fg_color=THEMES[current_theme]["card_bg"], corner_radius=10, border_width=1, border_color=("#E5E7EB", "#374151"))
                card.pack(fill="x", pady=4, padx=2)
                
                header_frame = ctk.CTkFrame(card, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(6, 2))
                
                user_lbl = ctk.CTkLabel(header_frame, text=r['username'], font=("Arial", 11, "bold"), text_color=THEMES[current_theme]["text"])
                user_lbl.pack(side="left")
                
                r_stars = "★" * r['rating'] + "☆" * (5 - r['rating'])
                stars_lbl = ctk.CTkLabel(header_frame, text=f"  {r_stars}", font=("Arial", 10), text_color="#F1C40F")
                stars_lbl.pack(side="left")
                
                text_lbl = ctk.CTkLabel(card, text=r['text'], font=("Arial", 11), text_color=THEMES[current_theme]["text_sec"], anchor="w", justify="left", wraplength=200)
                text_lbl.pack(fill="x", padx=10, pady=(2, 6))
        else:
            ctk.CTkLabel(self.reviews_frame, text="Відгуків ще немає.", font=("Arial", 11, "italic"), text_color=THEMES[current_theme]["text_sec"]).pack(anchor="w", pady=10)

    def submit_review(self):
        text = self.rev_entry.get().strip()
        if not text:
            play_sound("error")
            messagebox.showwarning("Помилка", "Введіть відгук!")
            return
        try: rating = int(self.rating_spin.get())
        except: rating = 5
        
        market_db.add_review(self.name, logged_in_user, rating, text)
        play_sound("success")
        self.rev_entry.delete(0, "end")
        self.refresh_reviews()

    def add_to_cart(self):
        try:
            qty = int(self.qty_spin.get())
            if qty <= 0: raise ValueError
        except ValueError:
            play_sound("error")
            messagebox.showwarning("Помилка", "Будь ласка, введіть коректну кількість!")
            return

        for item in cart:
            if item["name"] == self.name and item["color"] == self.selected_color.get():
                item["qty"] += qty
                break
        else:
            cart.append({"name": self.name, "price": self.data["price"], "qty": qty, "color": self.selected_color.get()})
            
        play_sound("success")
        self.main_screen.update_profile_info()
        messagebox.showinfo("Успіх", t("add_to_cart_success"))

# --- ПАНЕЛЬ КОШИКА З POS-ТАБЛИЦЕЮ ---
class CartPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        left_box = ctk.CTkFrame(self, corner_radius=12, fg_color=SIDEBAR_COLOR)
        left_box.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(left_box, text=t("cart_title"), font=("Arial", 16, "bold"), text_color=PRIMARY_COLOR).pack(pady=10)
        
        header_frame = ctk.CTkFrame(left_box, height=30, fg_color="#2b2b3d")
        header_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        ctk.CTkLabel(header_frame, text="Товар", font=("Arial", 10, "bold"), width=160, anchor="w", text_color="white").pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="К-сть", font=("Arial", 10, "bold"), width=60, anchor="center", text_color="white").pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="Ціна", font=("Arial", 10, "bold"), width=70, anchor="e", text_color="white").pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="Дія", font=("Arial", 10, "bold"), width=40, anchor="center", text_color="white").pack(side="right", padx=10)
        
        self.items_frame = ctk.CTkScrollableFrame(left_box, fg_color=THEMES[current_theme]["bg"])
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.total_lbl = ctk.CTkLabel(left_box, text="Total", font=("Arial", 14, "bold"), text_color=PRIMARY_COLOR)
        self.total_lbl.pack(pady=10)
        
        btn_clear = ctk.CTkButton(left_box, text=t("clear_cart_btn"), command=self.clear_cart, fg_color="#95a5a6", hover_color="#7f8c8d")
        btn_clear.pack(pady=5)
        
        self.right_box = ctk.CTkFrame(self, corner_radius=12, fg_color=SIDEBAR_COLOR)
        self.right_box.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.right_box, text=t("delivery_title"), font=("Arial", 14, "bold"), text_color=THEMES[current_theme]["text"]).pack(pady=15)
        
        entry_bg = THEMES[current_theme]["card_bg"]
        entry_fg = THEMES[current_theme]["text"]
        self.phone_entry = ctk.CTkEntry(self.right_box, placeholder_text=t("phone_lbl"), fg_color=entry_bg, text_color=entry_fg)
        self.phone_entry.pack(pady=6, padx=20, fill="x")
        self.phone_entry.insert(0, "+380")
        
        self.email_entry = ctk.CTkEntry(self.right_box, placeholder_text=t("email_lbl"), fg_color=entry_bg, text_color=entry_fg)
        self.email_entry.pack(pady=6, padx=20, fill="x")
        
        self.address_entry = ctk.CTkEntry(self.right_box, placeholder_text=t("address_lbl"), fg_color=entry_bg, text_color=entry_fg)
        self.address_entry.pack(pady=6, padx=20, fill="x")
        
        self.deliv_combo = ctk.CTkOptionMenu(self.right_box, values=["Кур'єр", "Нова Пошта", "Самовивіз"], fg_color=PRIMARY_COLOR, button_color=PRIMARY_COLOR)
        self.deliv_combo.pack(pady=6, padx=20, fill="x")
        
        self.pay_combo = ctk.CTkOptionMenu(self.right_box, values=["Балансом акаунту", "Карткою при отриманні", "Готівкою при отриманні"], fg_color=PRIMARY_COLOR, button_color=PRIMARY_COLOR)
        self.pay_combo.pack(pady=6, padx=20, fill="x")
        
        btn_order = ctk.CTkButton(self.right_box, text=t("checkout_btn"), command=self.checkout, fg_color="#2ecc71", hover_color="#27ae60", font=("Arial", 13, "bold"), corner_radius=50)
        btn_order.pack(pady=20)
        
        self.refresh_cart_list()

    def refresh_cart_list(self):
        for w in self.items_frame.winfo_children():
            w.destroy()
            
        if not cart:
            ctk.CTkLabel(self.items_frame, text=t("cart_empty"), font=("Arial", 11), text_color=("black", "white")).pack(pady=30)
            self.total_lbl.configure(text=f"{t('total_lbl')} 0 грн")
            return
            
        total_price = 0
        for index, item in enumerate(cart):
            sub = int(item["price"] * item["qty"])
            total_price += sub
            
            row = ctk.CTkFrame(self.items_frame, fg_color="#f8f9fa")
            row.pack(fill="x", pady=4)
            
            display_name = fruits_data[item["name"]]["names"][active_lang]
            ctk.CTkLabel(row, text=f"{display_name} ({item['color']})", font=("Arial", 11, "bold"), width=160, anchor="w", wraplength=150, text_color="black").pack(side="left", padx=10)
            
            unit = fruits_data[item["name"]]["unit"]
            if unit == "kg":
                qty_spin = ttk.Spinbox(row, from_=0.5, to=99.0, increment=0.5, width=4, justify="center")
            else:
                qty_spin = ttk.Spinbox(row, from_=1, to=99, increment=1, width=4, justify="center")
                
            qty_spin.pack(side="left", padx=10)
            qty_spin.set(item["qty"])
            qty_spin.bind("<KeyRelease>", lambda e, idx=index, sp=qty_spin: self.update_qty(idx, sp))
            qty_spin.bind("<<Increment>>", lambda e, idx=index, sp=qty_spin: self.update_qty(idx, sp))
            qty_spin.bind("<<Decrement>>", lambda e, idx=index, sp=qty_spin: self.update_qty(idx, sp))
            
            ctk.CTkLabel(row, text=f"{sub} грн", font=("Arial", 11), text_color="#2e7d32", width=70, anchor="e").pack(side="left", padx=10)
            
            btn_del = ctk.CTkButton(row, text="X", width=24, height=24, fg_color="#ff4d4d", hover_color="#ff3333", command=lambda idx=index: self.remove_item(idx))
            btn_del.pack(side="right", padx=10)

        discounted_price = total_price * (1 - session_discount)
        if session_discount > 0:
            self.total_lbl.configure(
                text=f"Сума: {total_price} грн\nЗнижка ({int(session_discount*100)}%): -{int(total_price*session_discount)} грн\nРазом: {int(discounted_price)} грн"
            )
        else:
            self.total_lbl.configure(text=f"{t('total_lbl')} {total_price} грн")

    def update_qty(self, idx, sp):
        try:
            unit = fruits_data[cart[idx]["name"]]["unit"]
            val = float(sp.get()) if unit == "kg" else int(sp.get())
            if val > 0:
                cart[idx]["qty"] = val
                self.refresh_cart_list()
                self.main_screen.update_profile_info()
        except ValueError:
            pass

    def remove_item(self, idx):
        cart.pop(idx)
        play_sound("click")
        self.refresh_cart_list()
        self.main_screen.update_profile_info()

    def clear_cart(self):
        if cart:
            cart.clear()
            play_sound("click")
            self.refresh_cart_list()
            self.main_screen.update_profile_info()

    def checkout(self):
        global session_discount
        if not cart:
            play_sound("error")
            messagebox.showwarning("Помилка", t("cart_empty"))
            return
            
        total_price = sum(item['price'] * item['qty'] for item in cart)
        discounted_price = int(total_price * (1 - session_discount))
        
        user_balance = market_db.get_balance(logged_in_user)
        if user_balance < discounted_price:
            play_sound("error")
            messagebox.showerror("Помилка", "Недостатньо коштів на балансі!")
            return
            
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()
        
        if len(phone) < 9 or not email or not address:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі дані доставки!")
            return
            
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        safe_date = date_str.replace(" ", "_").replace(":", "-")
        receipt_filename = f"receipt_{logged_in_user}_{safe_date}.html"
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Чек Сільпо</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #f3f3f3; padding: 20px; }}
        .receipt {{ background: white; max-width: 450px; margin: 0 auto; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.15); border-top: 10px solid #4a90e2; }}
        h2 {{ text-align: center; color: #2c3e50; margin-bottom: 5px; }}
        .meta {{ font-size: 13px; color: #555; line-height: 1.6; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        th {{ text-align: left; color: #7f8c8d; font-size: 13px; padding-bottom: 8px; border-bottom: 1px solid #eee; }}
        td {{ padding: 10px 0; font-size: 14px; border-bottom: 1px dashed #eee; }}
        .price {{ text-align: right; }}
        .total-row {{ font-weight: bold; font-size: 17px; color: #2e7d32; }}
        .footer {{ text-align: center; font-size: 13px; color: #95a5a6; margin-top: 25px; border-top: 1px solid #eee; padding-top: 15px; }}
    </style>
</head>
<body>
    <div class="receipt">
        <h2>СІЛЬПО ЧЕК</h2>
        <div class="meta">
            <b>Покупець:</b> {logged_in_user}<br>
            <b>Телефон:</b> {phone}<br>
            <b>Email:</b> {email}<br>
            <b>Адреса доставки:</b> {address}<br>
            <b>Спосіб доставки:</b> {self.deliv_combo.get()}<br>
            <b>Метод оплати:</b> {self.pay_combo.get()}<br>
            <b>Дата:</b> {date_str}
        </div>
        <table>
            <thead>
                <tr>
                    <th>Товар</th>
                    <th class="price">Вартість</th>
                </tr>
            </thead>
            <tbody>"""
        for item in cart:
            subtotal = item['price'] * item['qty']
            display_name = fruits_data[item["name"]]["names"][active_lang]
            html_content += f"""
            <tr>
                <td>{display_name}<br><small>{item['qty']} шт. х {item['price']} грн</small></td>
                <td class="price">{subtotal} грн</td>
            </tr>"""
        html_content += f"""
        </tbody>
    </table>"""
        if session_discount > 0:
            html_content += f"""
        <div style="text-align:right; font-size:14px; margin-bottom:5px;">Сума: {total_price} грн</div>
        <div style="text-align:right; font-size:14px; color:#e74c3c; margin-bottom:5px;">Знижка ({int(session_discount*100)}%): -{int(total_price*session_discount)} грн</div>"""
        html_content += f"""
    <div class="total-row" style="text-align:right; padding-top:10px; border-top: 2px solid #4a90e2;">
        РАЗОМ ДО СПЛАТИ: {discounted_price} грн
    </div>
    <div class="footer">Дякуємо за покупку в нашому Сільпо! 🚚</div>
</div>
</body>
</html>"""
        
        def on_pay_success():
            market_db.deduct_balance(logged_in_user, discounted_price)
            market_db.add_order(logged_in_user, discounted_price, sum(item['qty'] for item in cart), date_str)
            with open(receipt_filename, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            import webbrowser
            try:
                webbrowser.open(os.path.abspath(receipt_filename))
            except Exception:
                pass
                
            play_sound("success")
            messagebox.showinfo("Успіх", f"Замовлення успішно створено! Чек збережено: {receipt_filename}")
            cart.clear()
            session_discount = 0.0
            self.refresh_cart_list()
            self.main_screen.update_profile_info()

        FakePaymentWindow(self.main_screen, discounted_price, on_pay_success)

# --- ПАНЕЛЬ АНАЛІТИКИ ---
class AnalyticsPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text="Панель аналітики та звітів", font=("Arial", 16, "bold"), text_color=THEMES[current_theme]["text"]).pack(pady=10)
        
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=10)
        
        orders = market_db.get_orders(logged_in_user)
        total_spent = sum(o["total"] for o in orders)
        total_items = sum(o["items_count"] for o in orders)
        avg_receipt = int(total_spent / len(orders)) if orders else 0
        
        self.create_kpi_card(cards_frame, "Загальні витрати", f"{total_spent} грн", "#2ecc71").pack(side="left", fill="both", expand=True, padx=5)
        self.create_kpi_card(cards_frame, "Куплено товарів", f"{total_items} шт", "#3498db").pack(side="left", fill="both", expand=True, padx=5)
        self.create_kpi_card(cards_frame, "Середній чек", f"{avg_receipt} грн", "#e67e22").pack(side="left", fill="both", expand=True, padx=5)
        
        chart_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=SIDEBAR_COLOR)
        chart_frame.pack(fill="both", expand=True, pady=10, padx=5)
        
        ctk.CTkLabel(chart_frame, text="Динаміка замовлень", font=("Arial", 13, "bold"), text_color=THEMES[current_theme]["text"]).pack(pady=5)
        
        chart_bg = THEMES[current_theme]["bg"]
        self.canvas = tk.Canvas(chart_frame, bg=chart_bg, bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.draw_chart(orders))

    def create_kpi_card(self, parent, title, value, accent_color):
        card = ctk.CTkFrame(parent, corner_radius=10, height=80, fg_color=SIDEBAR_COLOR)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color=THEMES[current_theme]["text_sec"]).pack(pady=(10, 2))
        ctk.CTkLabel(card, text=value, font=("Arial", 18, "bold"), text_color=accent_color).pack()
        return card

    def draw_chart(self, orders):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
            
        for i in range(5):
            y = 30 + i * (h - 60) // 4
            grid_color = "#3A3A5C" if current_theme == "dark" else "#e2e2e2"
            self.canvas.create_line(40, y, w - 20, y, fill=grid_color, width=1)
            
        if not orders:
            self.canvas.create_text(w // 2, h // 2, text="Дані для аналітики відсутні", fill="gray", font=("Arial", 11, "italic"))
            return
            
        points = []
        max_val = max(o["total"] for o in orders) if orders else 1
        if max_val == 0: max_val = 1
        
        step_x = (w - 80) / max(1, len(orders) - 1) if len(orders) > 1 else (w - 80)
        
        for idx, o in enumerate(orders):
            x = 50 + idx * step_x
            y = (h - 40) - (o["total"] / max_val) * (h - 80)
            points.append((x, y))
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=PRIMARY_COLOR, outline="#ffffff", width=1.5)
            
        if len(points) > 1:
            for idx in range(len(points) - 1):
                self.canvas.create_line(points[idx][0], points[idx][1], points[idx + 1][0], points[idx + 1][1], fill=PRIMARY_COLOR, width=3)
        elif len(points) == 1:
            self.canvas.create_line(50, points[0][1], w - 20, points[0][1], fill=PRIMARY_COLOR, width=3)

# --- ПАНЕЛЬ ІСТОРІЇ ---
class HistoryPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text=t("history_title"), font=("Arial", 16, "bold"), text_color=THEMES[current_theme]["text"]).pack(pady=10)
        
        orders = market_db.get_orders(logged_in_user)
        if not orders:
            ctk.CTkLabel(self, text=t("no_orders"), font=("Arial", 11, "italic"), text_color=THEMES[current_theme]["text"]).pack(pady=40)
            return
            
        for index, order in enumerate(orders):
            row = ctk.CTkFrame(self, fg_color=SIDEBAR_COLOR)
            row.pack(fill="x", padx=20, pady=5)
            
            info_frame = ctk.CTkFrame(row, fg_color="transparent")
            info_frame.pack(side="left", padx=15, pady=4, fill="both", expand=True)
            
            ctk.CTkLabel(info_frame, text=f"Замовлення #{len(orders)-index} [{order['date']}]", font=("Arial", 11, "bold"), text_color=THEMES[current_theme]["text"]).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=f"Товарів: {order['items_count']} шт. | Сума: {order['total']} грн", font=("Arial", 10), text_color="#2e7d32").pack(anchor="w")
            
            def open_receipt(o_date=order['date']):
                import webbrowser
                safe_date = o_date.replace(" ", "_").replace(":", "-")
                receipt_filename = f"receipt_{logged_in_user}_{safe_date}.html"
                if os.path.exists(receipt_filename):
                    webbrowser.open(os.path.abspath(receipt_filename))
                else:
                    messagebox.showerror("Помилка", f"Файл чека не знайдено:\n{receipt_filename}")
                    
            btn_receipt = ctk.CTkButton(
                row, text="Відкрити чек", command=open_receipt, width=110, height=28,
                fg_color=PRIMARY_COLOR, hover_color="#3b7ad2", font=("Arial", 11, "bold")
            )
            btn_receipt.pack(side="right", padx=(0, 10), pady=10)
            
            def delete_order_action(o_date=order['date']):
                if messagebox.askyesno("Видалення", "Ви дійсно хочете видалити це замовлення з історії?"):
                    market_db.delete_order(logged_in_user, o_date)
                    safe_date = o_date.replace(" ", "_").replace(":", "-")
                    receipt_filename = f"receipt_{logged_in_user}_{safe_date}.html"
                    if os.path.exists(receipt_filename):
                        try:
                            os.remove(receipt_filename)
                        except:
                            pass
                    self.main_screen.show_history()
                    
            btn_delete = ctk.CTkButton(
                row, text="Видалити", command=delete_order_action, width=80, height=28,
                fg_color="#ff4d4d", hover_color="#ff3333", font=("Arial", 11, "bold")
            )
            btn_delete.pack(side="right", padx=(0, 15), pady=10)

# --- ПАНЕЛЬ НАЛАШТУВАНЬ ---
class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text="Налаштування застосунку", font=("Arial", 20, "bold"), text_color=THEMES[current_theme]["text"]).pack(pady=(20, 10))
        
        card = ctk.CTkFrame(self, fg_color=THEMES[current_theme]["card_bg"], corner_radius=12, border_width=1, border_color=("#E5E7EB", "#374151"))
        card.pack(pady=15, padx=20, fill="both", expand=True)
        
        # ── Тема ──
        ctk.CTkLabel(card, text="Тема оформлення:", font=("Arial", 13, "bold"), text_color=THEMES[current_theme]["text"]).pack(anchor="w", padx=30, pady=(25, 5))
        
        theme_options = ["Світла тема", "Темна тема"]
        self.theme_switch = ctk.CTkSegmentedButton(card, values=theme_options, command=self.toggle_theme, font=("Arial", 12, "bold"))
        self.theme_switch.pack(anchor="w", padx=30, pady=(5, 15))
        self.theme_switch.set("Світла тема" if current_theme == "light" else "Темна тема")

        # ── Поповнення гаманця ──
        ctk.CTkLabel(card, text="Поповнення балансу гаманця:", font=("Arial", 13, "bold"), text_color=THEMES[current_theme]["text"]).pack(anchor="w", padx=30, pady=(15, 5))
        self.btn_topup_settings = ctk.CTkButton(
            card, text="💳 Поповнити на 500 грн", font=("Arial", 12, "bold"),
            fg_color="#10B981", hover_color="#059669", height=34, corner_radius=6,
            command=self.main_screen.topup_balance
        )
        self.btn_topup_settings.pack(anchor="w", padx=30, pady=(5, 25))

    def toggle_theme(self, choice):
        new_theme = "light" if "Світла" in choice else "dark"
        self.main_screen.toggle_theme_to(new_theme)
        self.main_screen.show_settings()

from tkinter import ttk
if __name__ == "__main__":
    main_app = App()
    main_app.mainloop()
