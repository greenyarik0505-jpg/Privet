import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import os
import urllib.request
import datetime
import random
import math

# Налаштування стилю CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Глобальні налаштування
sound_enabled = True
active_lang = "ua"
logged_in_user = None
session_discount = 0.0
cart = []
SESSION_FILE = "session.txt"
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Спробуємо імпортувати winsound для звуків
try:
    import winsound
    def play_sound(action):
        if not sound_enabled:
            return
        if action == "click":
            winsound.Beep(800, 80)
        elif action == "success":
            winsound.Beep(1200, 100)
            winsound.Beep(1500, 150)
        elif action == "error":
            winsound.Beep(400, 300)
        elif action == "spin":
            winsound.Beep(1000, 50)
except ImportError:
    def play_sound(action):
        pass

import market_db
market_db.init_db()

# Високоякісні прямі посилання на 3D стікери (прозорі PNG)
STICKER_URLS = {
    "tech": "https://cdn-icons-png.flaticon.com/512/3063/3063822.png",      # 3D Ноутбук
    "fruits": "https://cdn-icons-png.flaticon.com/512/415/415733.png",        # 3D Червоне Яблуко
    "home": "https://cdn-icons-png.flaticon.com/512/10437/10437090.png",     # 3D Настільна лампа
    "sport": "https://cdn-icons-png.flaticon.com/512/3076/3076840.png",      # 3D Футбольний м'яч
    "clothing": "https://cdn-icons-png.flaticon.com/512/863/863684.png"      # 3D Синя футболка
}

# Завантажуємо круті 3D стікери локально при запуску, якщо їх немає
def download_assets():
    for cat, url in STICKER_URLS.items():
        dest = os.path.join(ASSETS_DIR, f"{cat}.png")
        if not os.path.exists(dest):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    with open(dest, 'wb') as f:
                        f.write(response.read())
            except Exception as e:
                # Створюємо резервну заглушку, якщо інтернет недоступний
                img = Image.new("RGBA", (128, 128), (52, 152, 219, 255))
                img.save(dest)

download_assets()

# Функція швидкого завантаження локальних 3D стікерів (абсолютно без лагів)
def get_local_sticker_image(category, size):
    dest = os.path.join(ASSETS_DIR, f"{category}.png")
    if os.path.exists(dest):
        try:
            img = Image.open(dest)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception:
            pass
    # Резервна кольорова плашка
    img = Image.new("RGBA", size, (149, 165, 166, 255))
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)

fruits_data = {}

# Списки для генерації РЕАЛІСТИЧНИХ унікальних назв
tech_brands = ["ASUS", "Lenovo", "Dell", "HP", "Acer", "MSI", "Apple MacBook", "Xiaomi", "Huawei", "Gigabyte"]
tech_models = ["ZenBook", "IdeaPad", "Inspiron", "Pavilion", "Swift", "Cyborg", "Air M2", "RedmiBook Pro", "MateBook D", "Aorus"]
tech_specs = ["Core i5 16GB", "Core i7 32GB", "Ryzen 5 8GB", "Ryzen 7 16GB", "M2 8GB", "M3 16GB", "Core i9 64GB", "Ryzen 9 32GB", "Intel Ultra 7", "Ryzen 3 8GB"]

fruit_varieties = ["Голден Делішес", "Ред Чіф", "Гренні Сміт", "Гала", "Фуджі", "Пінк Леді", "Чемпіон", "Айдаред", "Джонаголд", "Муцу"]
fruit_origins = ["Поділля", "Закарпаття", "Буковина", "імпорт Італія", "екологічні", "садові", "преміум", "відбірні", "фермерські", "соковиті"]
fruit_sizes = ["великі", "середні", "добірні", "солодкі", "кислі", "хрусткі", "ранні", "зимові", "домашні", "свіжі"]

lamp_styles = ["Loft", "Modern", "Hi-Tech", "Classic", "Minimalism", "Retro", "Scandinavian", "Industrial", "Art Deco", "Vintage"]
lamp_types = ["настільна лампа", "торшер", "бра", "підвісний світильник", "нічник", "офісна лампа", "діодна лампа", "смарт-лампа", "декоративна лампа", "світлодіодна панель"]
lamp_colors = ["чорний матовий", "білий глянець", "бронза", "дерево", "хром", "золото", "латунь", "сірий графіт", "мідь", "антрацит"]

sport_brands = ["Adidas", "Nike", "Puma", "Select", "Molten", "Wilson", "Jogel", "Mikasa", "Derbystar", "Umbro"]
sport_editions = ["Al Rihla Match", "Flight Pro", "Orbita Serie A", "Brillant Super", "Europa League", "Champions League", "Premier League", "World Cup", "Street Graff", "Indoor Felt"]
sport_types = ["професійний", "тренувальний", "ігровий", "класичний", "матчевий", "полегшений", "дитячий", "шкіряний", "поліуретановий", "всепогодний"]

cloth_brands = ["Zara", "H&M", "Nike", "Adidas", "Levi's", "Puma", "Uniqlo", "Tommy Hilfiger", "Calvin Klein", "Lacoste"]
cloth_types = ["Футболка", "Поло", "Теніска", "Лонгслів", "Майка", "Спортивна футболка", "Футболка оверсайз", "Класична футболка", "Базова футболка", "Футболка з принтом"]
cloth_materials = ["бавовна 100%", "органічний котон", "еластан", "поліестер Dry-Fit", "льон", "трикотаж", "сумішова тканина", "віскоза", "бамбук", "стрейч"]

# Генерація 100 унікальних ноутбуків
for i in range(100):
    b = tech_brands[i % 10]
    m = tech_models[(i // 10) % 10]
    s = tech_specs[(i * 3) % 10]
    name = f"{b} {m} ({s})"
    fruits_data[name] = {
        "price": 15000 + i * 220,
        "desc": f"Сучасний ноутбук {b} серії {m}. Специфікація: {s}.",
        "category": "tech",
        "colors": [("Сріблястий", "#bdc3c7"), ("Чорний", "#2c3e50")]
    }

# Генерація 100 унікальних яблук
for i in range(100):
    v = fruit_varieties[i % 10]
    o = fruit_origins[(i // 10) % 10]
    sz = fruit_sizes[(i * 3) % 10]
    name = f"Яблука {v} ({o}, {sz})"
    fruits_data[name] = {
        "price": 20 + (i % 15),
        "desc": f"Свіжі натуральні яблука сорту {v}, вирощені в регіоні {o}.",
        "category": "fruits",
        "colors": [("Жовте", "#f1c40f"), ("Червоне", "#e74c3c")]
    }

# Генерація 100 унікальних ламп
for i in range(100):
    s = lamp_styles[i % 10]
    t = lamp_types[(i // 10) % 10]
    c = lamp_colors[(i * 3) % 10]
    name = f"Лампа {s} {t} ({c})"
    fruits_data[name] = {
        "price": 300 + i * 18,
        "desc": f"Оригінальна лампа в стилі {s}. Тип пристрою: {t}.",
        "category": "home",
        "colors": [("Чорний", "#2c3e50"), ("Білий", "#ffffff")]
    }

# Генерація 100 унікальних м'ячів
for i in range(100):
    b = sport_brands[i % 10]
    e = sport_editions[(i // 10) % 10]
    t = sport_types[(i * 3) % 10]
    name = f"М'яч {b} {e} ({t})"
    fruits_data[name] = {
        "price": 400 + i * 12,
        "desc": f"Футбольний м'яч бренду {b}, лінійка {e}.",
        "category": "sport",
        "colors": [("Біло-чорний", "#ffffff"), ("Червоний", "#e74c3c")]
    }

# Генерація 100 унікальних футболок
for i in range(100):
    b = cloth_brands[i % 10]
    t = cloth_types[(i // 10) % 10]
    m = cloth_materials[(i * 3) % 10]
    name = f"{t} {b} ({m})"
    fruits_data[name] = {
        "price": 250 + i * 8,
        "desc": f"Брендовий одяг {b}. Тип виробу: {t}.",
        "category": "clothing",
        "colors": [("Синій", "#3498db"), ("Чорний", "#2c3e50")]
    }

LANGS = {
    "ua": {
        "title": "Мегамаркет Все-в-Одному",
        "search_label": "Пошук:",
        "balance_label": "Баланс:",
        "topup_btn": "+ Поповнити",
        "history_btn": "Історія",
        "wheel_btn": "Колесо Фортуни",
        "cart_btn": "Кошик",
        "details_btn": "Детальніше",
        "all_cat": "Усі",
        "tech_cat": "Техніка",
        "fruits_cat": "Фрукти",
        "home_cat": "Для дому",
        "sport_cat": "Спорт",
        "clothing_cat": "Одяг",
        "sort_cheap": "Спочатку дешевші",
        "sort_expensive": "Спочатку дорожчі",
        "auth_title": "Авторизація",
        "login_btn": "Увійти",
        "register_btn": "Реєстрація",
        "username_lbl": "Логін:",
        "password_lbl": "Пароль:",
        "logout_btn": "Вийти",
        "details_title": "Деталі товару",
        "color_lbl": "Виберіть сорт/колір:",
        "qty_lbl": "Кількість:",
        "add_to_cart_btn": "Додати в кошик",
        "reviews_lbl": "Відгуки та оцінки:",
        "add_review_lbl": "Додати відгук:",
        "submit_review_btn": "Надіслати",
        "cart_title": "Ваш кошик",
        "cart_empty": "Кошик порожній",
        "subtotal_lbl": "Сума:",
        "discount_lbl": "Знижка:",
        "total_lbl": "Разом до сплати:",
        "checkout_btn": "Оформити",
        "clear_cart_btn": "Очистити кошик",
        "history_title": "Історія замовлень",
        "no_orders": "Замовлень ще не було",
        "order_str": "Замовлення",
        "items_count_str": "Товарів",
        "fortune_title": "Колесо Фортуни",
        "spin_btn": "Крутити",
        "congrats": "Вітаємо!",
        "win_discount": "Ви виграли знижку",
        "try_again": "Спробуйте ще раз!",
        "insufficient_balance": "Недостатньо коштів на балансі!",
        "success_purchase": "Дякуємо за замовлення! Чек збережено",
        "settings_btn": "Налаштування",
        "settings_title": "Настройки программы",
        "lang_lbl": "Язык интерфейса:",
        "theme_lbl": "Тема оформления:",
        "theme_light": "Светлая",
        "theme_dark": "Темная",
        "sound_chk": "Звуковые эффекты"
    },
    "en": {
        "title": "Megamarket All-in-One",
        "search_label": "Search:",
        "balance_label": "Balance:",
        "topup_btn": "+ Top Up",
        "history_btn": "History",
        "wheel_btn": "Fortune Wheel",
        "cart_btn": "Cart",
        "details_btn": "Details",
        "all_cat": "All",
        "tech_cat": "Tech",
        "fruits_cat": "Fruits",
        "home_cat": "Home",
        "sport_cat": "Sports",
        "clothing_cat": "Clothing",
        "sort_cheap": "Price: Low to High",
        "sort_expensive": "Price: High to Low",
        "auth_title": "Authentication",
        "login_btn": "Login",
        "register_btn": "Register",
        "username_lbl": "Username:",
        "password_lbl": "Password:",
        "logout_btn": "Logout",
        "details_title": "Product Details",
        "color_lbl": "Select variety/color:",
        "qty_lbl": "Quantity:",
        "add_to_cart_btn": "Add to Cart",
        "reviews_lbl": "Reviews & Ratings:",
        "add_review_lbl": "Add a Review:",
        "submit_review_btn": "Submit",
        "cart_title": "Your Cart",
        "cart_empty": "Cart is empty",
        "subtotal_lbl": "Subtotal:",
        "discount_lbl": "Discount:",
        "total_lbl": "Total to pay:",
        "checkout_btn": "Checkout",
        "clear_cart_btn": "Clear Cart",
        "history_title": "Order History",
        "no_orders": "No orders yet",
        "order_str": "Order",
        "items_count_str": "Items",
        "fortune_title": "Wheel of Fortune",
        "spin_btn": "Spin",
        "congrats": "Congratulations!",
        "win_discount": "You won a discount of",
        "try_again": "Try again!",
        "insufficient_balance": "Insufficient balance! Please top up.",
        "success_purchase": "Thank you! Receipt saved",
        "settings_btn": "Settings",
        "settings_title": "Application Settings",
        "lang_lbl": "Interface Language:",
        "theme_lbl": "Color Theme:",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "sound_chk": "Sound Effects"
    },
    "ru": {
        "title": "Мегамаркет Все-в-Одном",
        "search_label": "Поиск:",
        "balance_label": "Баланс:",
        "topup_btn": "+ Пополнить",
        "history_btn": "История",
        "wheel_btn": "Колесо Фортуны",
        "cart_btn": "Корзина",
        "details_btn": "Подробнее",
        "all_cat": "Все",
        "tech_cat": "Техника",
        "fruits_cat": "Фрукты",
        "home_cat": "Для дома",
        "sport_cat": "Спорт",
        "clothing_cat": "Одежда",
        "sort_cheap": "Сначала дешевые",
        "sort_expensive": "Сначала дорогие",
        "auth_title": "Авторизация",
        "login_btn": "Войти",
        "register_btn": "Регистрация",
        "username_lbl": "Логин:",
        "password_lbl": "Пароль:",
        "logout_btn": "Выйти",
        "details_title": "Детали товара",
        "color_lbl": "Выберите сорт/цвет:",
        "qty_lbl": "Количество:",
        "add_to_cart_btn": "Добавить в корзину",
        "reviews_lbl": "Отзывы и оценки:",
        "add_review_lbl": "Добавить отзыв:",
        "submit_review_btn": "Отправить",
        "cart_title": "Ваша корзина",
        "cart_empty": "Корзина пуста",
        "subtotal_lbl": "Сумма:",
        "discount_lbl": "Скидка:",
        "total_lbl": "Итого к оплате:",
        "checkout_btn": "Оформить",
        "clear_cart_btn": "Очистить корзину",
        "history_title": "История заказов",
        "no_orders": "Заказов еще не было",
        "order_str": "Заказ",
        "items_count_str": "Товаров",
        "fortune_title": "Колесо Фортуны",
        "spin_btn": "Крутить",
        "congrats": "Поздравляем!",
        "win_discount": "Вы выиграли скидку",
        "try_again": "Попробуйте еще раз!",
        "insufficient_balance": "Недостаточно средств на балансе!",
        "success_purchase": "Спасибо за покупку! Чек сохранен",
        "settings_btn": "Настройки",
        "settings_title": "Настройки программы",
        "lang_lbl": "Язык интерфейса:",
        "theme_lbl": "Тема оформления:",
        "theme_light": "Светлая",
        "theme_dark": "Темная",
        "sound_chk": "Звуковые эффекты"
    }
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("980x740")
        self.title("Мегамаркет Все-в-Одному")
        
        self.container = ctk.CTkFrame(self)
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

# --- ЕКРАН АВТОРИЗАЦІЇ ---
class AuthScreen(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        self.bg_color_dark = "#171821" 
        self.bg_color_light = "#f3f4f6" 
        
        current_bg = self.bg_color_dark if ctk.get_appearance_mode() == "Dark" else self.bg_color_light
        super().__init__(parent, fg_color=current_bg)
        self.controller = app_controller
        
        card_bg = "#21222e" if ctk.get_appearance_mode() == "Dark" else "#ffffff"
        self.card = ctk.CTkFrame(
            self, 
            corner_radius=16, 
            width=640, 
            height=390, 
            fg_color=card_bg,
            bg_color=current_bg,
            border_width=1, 
            border_color="#34495e" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        self.left_frame = ctk.CTkFrame(self.card, width=280, height=350, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        self.left_canvas = tk.Canvas(self.left_frame, width=240, height=340, bg=card_bg, bd=0, highlightthickness=0)
        self.left_canvas.pack(fill="both", expand=True)
        
        self.draw_vector_graphics()
        
        self.right_frame = ctk.CTkFrame(self.card, width=320, height=350, fg_color="transparent")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        self.is_register_mode = False
        
        self.lbl_title = ctk.CTkLabel(self.right_frame, text="Вхід", font=("Segoe UI", 24, "bold"))
        self.lbl_title.pack(pady=(20, 15))
        
        self.user_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Логін", width=250, height=42)
        self.user_entry.pack(pady=8)
        
        self.pass_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Пароль", show="*", width=250, height=42)
        self.pass_entry.pack(pady=8)
        
        self.confirm_pass_entry = ctk.CTkEntry(self.right_frame, placeholder_text="Повторіть пароль", show="*", width=250, height=42)
        
        self.btn_action = ctk.CTkButton(self.right_frame, text="УВІЙТИ", command=self.handle_action, width=250, height=42, font=("Segoe UI", 12, "bold"), fg_color="#2ecc71", hover_color="#27ae60")
        self.btn_action.pack(pady=12)
        
        self.btn_toggle = ctk.CTkButton(self.right_frame, text="Створити акаунт →", command=self.toggle_mode, fg_color="transparent", text_color="#3498db", hover_color=card_bg, width=200, height=20, font=("Segoe UI", 10, "underline"))
        self.btn_toggle.pack(pady=5)
        
        theme_icon = "🌙" if ctk.get_appearance_mode() == "Dark" else "☀️"
        theme_color = "#f1c40f" if ctk.get_appearance_mode() == "Dark" else "#e67e22"
        self.btn_theme = ctk.CTkButton(
            self, 
            text=theme_icon, 
            command=self.switch_theme, 
            width=45, 
            height=28, 
            fg_color="#252538" if ctk.get_appearance_mode() == "Dark" else "#cccccc", 
            text_color=theme_color,
            bg_color=current_bg,
            font=("Segoe UI", 13, "bold")
        )
        self.btn_theme.place(relx=0.98, rely=0.02, anchor="ne")
        
        self.show_pass_var = tk.BooleanVar(value=False)
        self.chk_show_pass = ctk.CTkCheckBox(self.right_frame, text="Показати пароль", variable=self.show_pass_var, command=self.toggle_password_visibility, font=("Segoe UI", 10))
        self.chk_show_pass.pack(pady=4)

    def toggle_mode(self):
        play_sound("click")
        self.is_register_mode = not self.is_register_mode
        card_bg = "#21222e" if ctk.get_appearance_mode() == "Dark" else "#ffffff"
        
        if self.is_register_mode:
            self.lbl_title.configure(text="Реєстрація")
            self.btn_action.configure(text="ЗАРЕЄСТРУВАТИСЯ", fg_color="#3498db", hover_color="#2980b9")
            self.btn_toggle.configure(text="← Вхід")
            self.btn_action.pack_forget()
            self.btn_toggle.pack_forget()
            self.chk_show_pass.pack_forget()
            
            self.confirm_pass_entry.pack(pady=8)
            self.chk_show_pass.pack(pady=4)
            self.btn_action.pack(pady=12)
            self.btn_toggle.pack(pady=5)
        else:
            self.lbl_title.configure(text="Вхід")
            self.btn_action.configure(text="УВІЙТИ", fg_color="#2ecc71", hover_color="#27ae60")
            self.btn_toggle.configure(text="Створити акаунт →")
            self.confirm_pass_entry.pack_forget()
            self.chk_show_pass.pack_forget()
            self.btn_action.pack_forget()
            self.btn_toggle.pack_forget()
            
            self.chk_show_pass.pack(pady=4)
            self.btn_action.pack(pady=12)
            self.btn_toggle.pack(pady=5)

    def handle_action(self):
        if self.is_register_mode:
            self.try_register()
        else:
            self.try_login()

    def try_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not username or not password:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі поля!")
            return
            
        if market_db.login_user(username, password):
            global logged_in_user
            logged_in_user = username
            try:
                with open(SESSION_FILE, "w", encoding="utf-8") as f:
                    f.write(username)
            except Exception:
                pass
            play_sound("success")
            self.controller.show_main_screen()
        else:
            play_sound("error")
            messagebox.showerror("Помилка", "Невірний логін або пароль!")

    def try_register(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        c_password = self.confirm_pass_entry.get().strip()
        
        if not username or not password or not c_password:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі поля!")
            return
            
        if password != c_password:
            play_sound("error")
            messagebox.showerror("Помилка", "Паролі не співпадають!")
            return
            
        if market_db.register_user(username, password):
            play_sound("success")
            messagebox.showinfo("Успіх", "Користувач зареєстрований! Увійдіть.")
            self.toggle_mode()
        else:
            play_sound("error")
            messagebox.showerror("Помилка", "Такий логін вже існує!")

    def toggle_password_visibility(self):
        show_char = "" if self.show_pass_var.get() else "*"
        self.pass_entry.configure(show=show_char)
        self.confirm_pass_entry.configure(show=show_char)

    def switch_theme(self):
        play_sound("click")
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
            current_bg = self.bg_color_light
            card_bg = "#ffffff"
            self.btn_theme.configure(text="☀️", text_color="#e67e22", fg_color="#cccccc")
        else:
            ctk.set_appearance_mode("dark")
            current_bg = self.bg_color_dark
            card_bg = "#21222e"
            self.btn_theme.configure(text="🌙", text_color="#f1c40f", fg_color="#252538")
            
        self.configure(fg_color=current_bg)
        self.card.configure(fg_color=card_bg, bg_color=current_bg, border_color="#34495e" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0")
        self.btn_theme.configure(bg_color=current_bg)
        self.left_canvas.configure(bg=card_bg)
        self.draw_vector_graphics()
        self.btn_toggle.configure(hover_color=card_bg)

    def draw_vector_graphics(self):
        self.left_canvas.delete("all")
        
        circle_color = "#2a2b3d" if ctk.get_appearance_mode() == "Dark" else "#f3f4f6"
        stroke_color = "#cdd6f4" if ctk.get_appearance_mode() == "Dark" else "#333333"
        screen_fill = "#1e1e2e" if ctk.get_appearance_mode() == "Dark" else "#e2e2e2"
        
        # Малюємо коло по центру
        self.left_canvas.create_oval(50, 90, 190, 230, fill=circle_color, outline="")
        
        # Декоративні плаваючі елементи
        self.left_canvas.create_oval(30, 70, 42, 82, outline="#00f2fe", width=2)
        self.left_canvas.create_polygon(210, 80, 220, 95, 200, 95, outline="#2ecc71", fill="", width=2)
        self.left_canvas.create_polygon(25, 230, 35, 245, 15, 245, outline="#e74c3c", fill="", width=2)
        self.left_canvas.create_oval(215, 240, 225, 250, outline="#3498db", width=2)
        self.left_canvas.create_rectangle(190, 40, 198, 48, outline="#cccccc", fill="")
        self.left_canvas.create_rectangle(70, 280, 78, 288, outline="#cccccc", fill="")
        
        # Векторний стікер ноутбука
        self.left_canvas.create_rectangle(90, 125, 150, 165, fill=screen_fill, outline=stroke_color, width=2)
        self.left_canvas.create_polygon(80, 165, 160, 165, 165, 172, 75, 172, fill=circle_color, outline=stroke_color, width=2)
        self.left_canvas.create_line(115, 170, 125, 170, fill=stroke_color, width=2)
        self.left_canvas.create_oval(115, 133, 125, 143, fill="", outline=stroke_color, width=2)
        self.left_canvas.create_arc(107, 145, 133, 165, start=0, extent=180, style="arc", outline=stroke_color, width=2)

# --- ГОЛОВНИЙ ЕКРАН З БІЧНОЮ НАВІГАЦІЄЮ ---
class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent)
        self.controller = app_controller
        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="МЕГАМАРКЕТ", font=("Segoe UI", 16, "bold"))
        self.lbl_logo.pack(pady=20)
        
        self.profile_lbl = ctk.CTkLabel(self.sidebar, text=f"Користувач: {logged_in_user}", font=("Segoe UI", 11, "bold"))
        self.profile_lbl.pack(pady=5)
        
        self.balance_lbl = ctk.CTkLabel(self.sidebar, text=f"0 грн", font=("Segoe UI", 12), text_color="#2ecc71")
        self.balance_lbl.pack(pady=2)
        
        btn_topup = ctk.CTkButton(self.sidebar, text="+ Поповнити", command=self.topup_balance, width=120, height=26, font=("Segoe UI", 10, "bold"), fg_color="#2ecc71", hover_color="#27ae60")
        btn_topup.pack(pady=5)
        
        self.nav_buttons = {}
        navs = [
            ("Каталог", self.show_catalog),
            ("Кошик", self.show_cart),
            ("Колесо Фортуни", self.show_fortune),
            ("Історія", self.show_history),
            ("Налаштування", self.show_settings)
        ]
        for name, cmd in navs:
            btn = ctk.CTkButton(self.sidebar, text=name, anchor="w", fg_color="transparent", hover_color="#34495e", command=cmd, font=("Segoe UI", 12))
            btn.pack(fill="x", padx=10, pady=5)
            self.nav_buttons[name] = btn
            
        btn_logout = ctk.CTkButton(self.sidebar, text="Вийти", anchor="w", fg_color="#e74c3c", hover_color="#c0392b", command=self.logout, font=("Segoe UI", 12))
        btn_logout.pack(side="bottom", fill="x", padx=10, pady=20)
        
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        
        self.active_panel = None
        self.show_catalog()
        self.update_profile_info()

    def update_profile_info(self):
        balance = market_db.get_balance(logged_in_user)
        self.balance_lbl.configure(text=f"{balance} грн")

    def topup_balance(self):
        play_sound("success")
        market_db.add_balance(logged_in_user, 500)
        self.update_profile_info()
        messagebox.showinfo("Баланс", "Баланс поповнено на 500 грн!")

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

    def switch_panel(self, panel_class, *args, **kwargs):
        if self.active_panel:
            self.active_panel.pack_forget()
            self.active_panel.destroy()
        self.active_panel = panel_class(self.content_container, self, *args, **kwargs)
        self.active_panel.pack(fill="both", expand=True)

    def show_catalog(self):
        self.switch_panel(CatalogPanel)

    def show_cart(self):
        self.switch_panel(CartPanel)

    def show_fortune(self):
        self.switch_panel(FortunePanel)

    def show_history(self):
        self.switch_panel(HistoryPanel)

    def show_settings(self):
        self.switch_panel(SettingsPanel)

# --- ПАНЕЛЬ КАТАЛОГУ ---
class CatalogPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", pady=10)
        
        self.search_entry = ctk.CTkEntry(top_bar, placeholder_text="Пошук товарів...", width=220)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.filter_products)
        
        self.active_cat = "all"
        cats = [("Усі", "all"), ("Техніка", "tech"), ("Фрукти", "fruits"), ("Для дому", "home"), ("Спорт", "sport"), ("Одяг", "clothing")]
        for text, key in cats:
            btn = ctk.CTkButton(top_bar, text=text, command=lambda k=key: self.set_category(k), width=70, height=28, font=("Segoe UI", 10))
            btn.pack(side="left", padx=3)
            
        self.sort_menu = ctk.CTkOptionMenu(top_bar, values=["Дешевші", "Дорожчі"], command=self.set_sorting, width=110)
        self.sort_menu.pack(side="right", padx=5)
        self.active_sort = "cheap"
        
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)
        self.scroll_frame.bind("<Configure>", self.on_resize)
        
        self.draw_grid()

    def on_resize(self, event):
        w = event.width
        if hasattr(self, "_last_width") and abs(self._last_width - w) < 40:
            return
        self._last_width = w
        self.draw_grid()

    def set_category(self, cat):
        self.active_cat = cat
        self.draw_grid()

    def set_sorting(self, choice):
        self.active_sort = "cheap" if choice == "Дешевші" else "expensive"
        self.draw_grid()

    def filter_products(self, event):
        self.draw_grid()

    def draw_grid(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        search_query = self.search_entry.get().strip().lower()
        favorites = market_db.get_favorites(logged_in_user)
        
        filtered = []
        for name, data in fruits_data.items():
            if search_query and search_query not in name.lower(): continue
            if self.active_cat != "all" and data["category"] != self.active_cat: continue
            filtered.append((name, data))
            
        def sort_key(item):
            name, data = item
            is_fav = 0 if name in favorites else 1
            price_val = data["price"] if self.active_sort == "cheap" else -data["price"]
            return (is_fav, price_val)
            
        filtered.sort(key=sort_key)
        
        width = self.scroll_frame.winfo_width()
        if width <= 1:
            width = 740
        card_w = 230 
        cols = max(1, width // card_w)
        
        col = 0
        row = 0
        for name, data in filtered[:36]:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=12, width=210, height=295)
            card.grid(row=row, column=col, padx=10, pady=10)
            card.grid_propagate(False)
            
            is_fav = name in favorites
            heart_text = "Liked" if is_fav else "Like"
            heart_color = "red" if is_fav else "gray"
            heart_btn = ctk.CTkButton(card, text=heart_text, text_color=heart_color, width=45, height=24, fg_color="transparent", hover_color=None, command=lambda n=name: self.toggle_favorite(n))
            heart_btn.place(relx=0.82, rely=0.08, anchor="center")
            
            # Швидке локальне завантаження красивих 3D стікерів
            photo = get_local_sticker_image(data["category"], (180, 110))
            img_lbl = ctk.CTkLabel(card, image=photo, text="")
            img_lbl.pack(pady=(12, 5))
            
            lbl_name = ctk.CTkLabel(card, text=name, font=("Segoe UI", 11, "bold"), wraplength=190)
            lbl_name.pack(pady=2, fill="x", padx=10)
            
            lbl_price = ctk.CTkLabel(card, text=f"{data['price']} грн", font=("Segoe UI", 12), text_color="#2ecc71")
            lbl_price.pack(pady=1)
            
            btn_details = ctk.CTkButton(card, text="Детальніше", command=lambda n=name: self.main_screen.switch_panel(DetailsPanel, n), width=150, height=32, font=("Segoe UI", 11, "bold"), fg_color="#3498db", hover_color="#2980b9")
            btn_details.pack(side="bottom", pady=10)
            
            col += 1
            if col >= cols:
                col = 0
                row += 1

    def toggle_favorite(self, name):
        market_db.toggle_favorite(logged_in_user, name)
        play_sound("click")
        self.draw_grid()

# --- ПАНЕЛЬ ДЕТАЛЕЙ ТОВАРУ ---
class DetailsPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen, name):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        self.name = name
        self.data = fruits_data[name]
        
        btn_back = ctk.CTkButton(self, text="← Назад", command=lambda: self.main_screen.show_catalog(), width=80, height=28)
        btn_back.pack(anchor="w", pady=10)
        
        left_box = ctk.CTkFrame(self, corner_radius=12)
        left_box.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Стікер високої роздільної здатності
        photo = get_local_sticker_image(self.data["category"], (240, 160))
        self.img_lbl = ctk.CTkLabel(left_box, image=photo, text="")
        self.img_lbl.pack(pady=20)
        
        lbl_title = ctk.CTkLabel(left_box, text=name, font=("Segoe UI", 16, "bold"), wraplength=280)
        lbl_title.pack(pady=5)
        
        lbl_desc = ctk.CTkLabel(left_box, text=self.data["desc"], font=("Segoe UI", 11, "italic"), wraplength=280)
        lbl_desc.pack(pady=5)
        
        lbl_price = ctk.CTkLabel(left_box, text=f"Ціна: {self.data['price']} грн", font=("Segoe UI", 14, "bold"), text_color="#2ecc71")
        lbl_price.pack(pady=10)
        
        ctk.CTkLabel(left_box, text="Виберіть сорт/колір:", font=("Segoe UI", 11, "bold")).pack()
        self.selected_color = ctk.StringVar(value=self.data["colors"][0][0])
        color_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        color_frame.pack(pady=5)
        
        for color_name, color_hex in self.data["colors"]:
            btn_c = tk.Button(color_frame, bg=color_hex, width=4, height=1, relief="groove", command=lambda c=color_name: self.selected_color.set(c))
            btn_c.pack(side="left", padx=5)
            
        qty_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        qty_frame.pack(pady=10)
        ctk.CTkLabel(qty_frame, text="Кількість:").pack(side="left", padx=5)
        self.qty_spin = ttk.Spinbox(qty_frame, from_=1, to=50, width=5, font=("Segoe UI", 10), justify="center")
        self.qty_spin.pack(side="left", padx=5)
        self.qty_spin.set(1)
        
        btn_add = ctk.CTkButton(left_box, text="Додати в кошик", command=self.add_to_cart, fg_color="#2ecc71", hover_color="#27ae60", font=("Segoe UI", 12, "bold"))
        btn_add.pack(pady=10)
        
        right_box = ctk.CTkFrame(self, corner_radius=12)
        right_box.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(right_box, text="Відгуки та оцінки:", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        self.reviews_frame = ctk.CTkScrollableFrame(right_box, height=220)
        self.reviews_frame.pack(fill="both", expand=True, padx=10)
        
        form_frame = ctk.CTkFrame(right_box)
        form_frame.pack(fill="x", padx=10, pady=15)
        
        self.rating_spin = ttk.Spinbox(form_frame, from_=1, to=5, width=3, justify="center")
        self.rating_spin.grid(row=0, column=0, padx=5, pady=5)
        self.rating_spin.set(5)
        
        self.rev_entry = ctk.CTkEntry(form_frame, placeholder_text="Ваш відгук...", width=160)
        self.rev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        btn_submit = ctk.CTkButton(form_frame, text="Надіслати", command=self.submit_review, width=80)
        btn_submit.grid(row=0, column=2, padx=5, pady=5)
        
        self.refresh_reviews()

    def refresh_reviews(self):
        for w in self.reviews_frame.winfo_children():
            w.destroy()
            
        revs = market_db.get_reviews(self.name)
        if revs:
            avg = sum(r['rating'] for r in revs) / len(revs)
            stars_text = "*" * int(round(avg)) + "." * (5 - int(round(avg)))
            ctk.CTkLabel(self.reviews_frame, text=f"Рейтинг: {stars_text} ({avg:.1f}/5)", font=("Segoe UI", 12, "bold"), text_color="#f1c40f").pack(anchor="w")
            for r in revs[-5:]:
                ctk.CTkLabel(self.reviews_frame, text=f"• {r['username']} ({r['rating']}/5): {r['text']}", font=("Segoe UI", 10), anchor="w", justify="left").pack(fill="x", pady=2)
        else:
            ctk.CTkLabel(self.reviews_frame, text="Відгуків ще немає.", font=("Segoe UI", 10, "italic")).pack(anchor="w")

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
        messagebox.showinfo("Успіх", f"Додано до кошика!")

# --- ПАНЕЛЬ КОШИКА ТА ОФОРМЛЕННЯ ---
class CartPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        left_box = ctk.CTkFrame(self, corner_radius=12)
        left_box.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(left_box, text="Кошик товарів", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        self.items_frame = ctk.CTkScrollableFrame(left_box)
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.total_lbl = ctk.CTkLabel(left_box, text="Разом до сплати: 0 грн", font=("Segoe UI", 13, "bold"), text_color="#2ecc71")
        self.total_lbl.pack(pady=10)
        
        btn_clear = ctk.CTkButton(left_box, text="Очистити кошик", command=self.clear_cart, fg_color="#95a5a6", hover_color="#7f8c8d")
        btn_clear.pack(pady=5)
        
        self.right_box = ctk.CTkFrame(self, corner_radius=12)
        self.right_box.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.right_box, text="Дані для доставки замовлення", font=("Segoe UI", 14, "bold")).pack(pady=15)
        
        self.phone_entry = ctk.CTkEntry(self.right_box, placeholder_text="Номер телефону (+380...)")
        self.phone_entry.pack(pady=6, padx=20, fill="x")
        self.phone_entry.insert(0, "+380")
        
        self.email_entry = ctk.CTkEntry(self.right_box, placeholder_text="Електронна пошта (Email)")
        self.email_entry.pack(pady=6, padx=20, fill="x")
        
        self.address_entry = ctk.CTkEntry(self.right_box, placeholder_text="Адреса доставки")
        self.address_entry.pack(pady=6, padx=20, fill="x")
        
        self.deliv_combo = ctk.CTkOptionMenu(self.right_box, values=["Courier", "Nova Poshta", "Self-pickup"])
        self.deliv_combo.pack(pady=6, padx=20, fill="x")
        
        self.pay_combo = ctk.CTkOptionMenu(self.right_box, values=["Balance", "Card on delivery", "Cash"])
        self.pay_combo.pack(pady=6, padx=20, fill="x")
        
        btn_order = ctk.CTkButton(self.right_box, text="Оформити замовлення", command=self.checkout, fg_color="#2ecc71", hover_color="#27ae60", font=("Segoe UI", 12, "bold"))
        btn_order.pack(pady=20)
        
        self.refresh_cart_list()

    def refresh_cart_list(self):
        for w in self.items_frame.winfo_children():
            w.destroy()
            
        if not cart:
            ctk.CTkLabel(self.items_frame, text="Кошик порожній", font=("Segoe UI", 11)).pack(pady=30)
            self.total_lbl.configure(text="Разом до сплати: 0 грн")
            return
            
        total_price = 0
        for index, item in enumerate(cart):
            sub = item["price"] * item["qty"]
            total_price += sub
            
            row = ctk.CTkFrame(self.items_frame)
            row.pack(fill="x", pady=4)
            
            ctk.CTkLabel(row, text=f"{item['name']} ({item['color']}) x{item['qty']}", font=("Segoe UI", 10, "bold"), wraplength=180).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"{sub} грн", font=("Segoe UI", 11), text_color="#2ecc71").pack(side="left", padx=15)
            
            btn_del = ctk.CTkButton(row, text="X", width=24, height=24, fg_color="#ff4d4d", hover_color="#ff3333", command=lambda idx=index: self.remove_item(idx))
            btn_del.pack(side="right", padx=10)

        discounted_price = total_price * (1 - session_discount)
        if session_discount > 0:
            self.total_lbl.configure(
                text=f"Сума: {total_price} stroke грн\nЗнижка ({int(session_discount*100)}%): -{int(total_price*session_discount)} грн\nРазом: {int(discounted_price)} грн"
            )
        else:
            self.total_lbl.configure(text=f"Разом до сплати: {total_price} грн")

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
            messagebox.showwarning("Помилка", "Кошик порожній!")
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
            
        market_db.deduct_balance(logged_in_user, discounted_price)
        date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        market_db.add_order(logged_in_user, discounted_price, sum(item['qty'] for item in cart), date_str)
        
        receipt_filename = f"receipt_{logged_in_user}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Чек Мегамаркету</title>
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
        <h2>МЕГАМАРКЕТ ЧЕК</h2>
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
            html_content += f"""
            <tr>
                <td>{item['name']}<br><small>{item['qty']} шт. х {item['price']} грн</small></td>
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
    <div class="footer">Дякуємо за покупку в нашому Мегамаркеті! 🚚</div>
</div>
</body>
</html>"""
        with open(receipt_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        play_sound("success")
        messagebox.showinfo("Успіх", f"Замовлення успешно створено! Чек збережено: {receipt_filename}")
        cart.clear()
        session_discount = 0.0
        self.refresh_cart_list()
        self.main_screen.update_profile_info()

# --- ПАНЕЛЬ КОЛЕСА ФОРТУНИ ---
class FortunePanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text="Колесо Фортуни", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        self.canvas = tk.Canvas(self, width=280, height=280, bg="#2b2b2b", bd=0, highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.sectors = [
            ("Спробуй ще", "#ffffff", 0.0),
            ("Знижка 5%", "#ff8a80", 0.05),
            ("Спробуй ще", "#ffffff", 0.0),
            ("Знижка 10%", "#ff5252", 0.10),
            ("Спробуй ще", "#ffffff", 0.0),
            ("Знижка 15%", "#ff1744", 0.15)
        ]
        self.draw_wheel(0)
        
        self.btn_spin = ctk.CTkButton(self, text="Крутити", command=self.spin, font=("Segoe UI", 11, "bold"), fg_color="#f1c40f", text_color="#2c3e50", hover_color="#f39c12")
        self.btn_spin.pack(pady=15)

    def draw_wheel(self, rot):
        self.canvas.delete("all")
        for i, (text, color, val) in enumerate(self.sectors):
            start = rot + i * 60
            self.canvas.create_arc(10, 10, 270, 270, start=start, extent=60, fill=color, outline="#2c3e50")
            rad = math.radians(start + 30)
            tx = 140 + 75 * math.cos(rad)
            ty = 140 - 75 * math.sin(rad)
            self.canvas.create_text(tx, ty, text=text.split()[0], font=("Segoe UI", 9, "bold"), fill="#2c3e50")
        self.canvas.create_polygon(140, 5, 130, 25, 150, 25, fill="#e74c3c")

    def spin(self):
        play_sound("click")
        self.btn_spin.configure(state="disabled")
        rotations = random.randint(18, 25)
        
        def animate(step, cur_angle):
            if step > 0:
                cur_angle = (cur_angle + step * 8) % 360
                self.draw_wheel(cur_angle)
                play_sound("spin")
                self.after(50, lambda: animate(step - 1, cur_angle))
            else:
                final_angle = (90 - cur_angle) % 360
                sector_idx = int(final_angle // 60) % len(self.sectors)
                name, color, discount = self.sectors[sector_idx]
                
                if discount > 0:
                    global session_discount
                    session_discount = discount
                    play_sound("success")
                    messagebox.showinfo("Вітаємо!", f"Ви виграли знижку: {int(discount*100)}%!")
                else:
                    play_sound("error")
                    messagebox.showinfo("Результат", "Спробуйте ще раз!")
                self.btn_spin.configure(state="normal")
                
        animate(rotations, 0)

# --- ПАНЕЛЬ ІСТОРІЇ ---
class HistoryPanel(ctk.CTkScrollableFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text="Історія замовлень", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        orders = market_db.get_orders(logged_in_user)
        if not orders:
            ctk.CTkLabel(self, text="Замовлень ще не було", font=("Segoe UI", 11, "italic")).pack(pady=40)
            return
            
        for index, order in enumerate(orders):
            row = ctk.CTkFrame(self)
            row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=f"Замовлення #{len(orders)-index} [{order['date']}]", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=15, pady=4)
            ctk.CTkLabel(row, text=f"Товарів: {order['items_count']} шт. | Сума: {order['total']} грн", font=("Segoe UI", 10), text_color="#2ecc71").pack(anchor="w", padx=15, pady=2)

# --- ПАНЕЛЬ НАЛАШТУВАНЬ ---
class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text="Налаштування", font=("Segoe UI", 16, "bold")).pack(pady=10)
        
        card = ctk.CTkFrame(self, width=400, height=350)
        card.pack(pady=15, padx=20)
        
        ctk.CTkLabel(card, text="Мова інтерфейсу:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=30, pady=10)
        lang_btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        lang_btn_frame.pack(fill="x", padx=30)
        
        ctk.CTkButton(lang_btn_frame, text="Українська", width=90, command=lambda: self.change_lang("ua")).pack(side="left", padx=5)
        ctk.CTkButton(lang_btn_frame, text="English", width=90, command=lambda: self.change_lang("en")).pack(side="left", padx=5)
        ctk.CTkButton(lang_btn_frame, text="Русский", width=90, command=lambda: self.change_lang("ru")).pack(side="left", padx=5)
        
        ctk.CTkLabel(card, text="Тема оформлення:", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=30, pady=10)
        self.theme_switch = ctk.CTkSegmentedButton(card, values=["Light", "Dark"], command=self.toggle_theme)
        self.theme_switch.pack(fill="x", padx=30)
        self.theme_switch.set("Dark" if ctk.get_appearance_mode() == "Dark" else "Light")
        
        self.sound_var = tk.BooleanVar(value=sound_enabled)
        sound_chk = ctk.CTkCheckBox(card, text="Звуковые эффекты", variable=self.sound_var, command=self.toggle_sound)
        sound_chk.pack(anchor="w", padx=30, pady=25)

    def change_lang(self, lang):
        global active_lang
        active_lang = lang
        play_sound("click")
        self.main_screen.lbl_logo.configure(text="МЕГАМАРКЕТ")
        nav_texts = ["Каталог", "Кошик", "Колесо Фортуни", "Історія", "Налаштування"]
        for t in nav_texts:
            if t in self.main_screen.nav_buttons:
                self.main_screen.nav_buttons[t].configure(text=t)
        self.main_screen.show_settings()

    def toggle_theme(self, choice):
        play_sound("click")
        if "Dark" in choice:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def toggle_sound(self):
        global sound_enabled
        sound_enabled = self.sound_var.get()
        play_sound("click")

from tkinter import ttk
if __name__ == "__main__":
    main_app = App()
    main_app.mainloop()
