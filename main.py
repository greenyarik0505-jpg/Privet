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

# Налаштування стилю за замовчуванням (Світла тема, як у convenientshop)
ctk.set_appearance_mode("light")
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

# Кольорова палітра дизайну SecureAuditX/convenientshop
PRIMARY_COLOR = "#4F46E5"    # Індиго
BG_COLOR = "#A4A4EB"         # М'який фіолетово-блакитний фон
FRAME_COLOR = "#E0DDF0"      # Лавандово-сірий фон карток/сайдбару
HOVER_COLOR = "#D7D2F4"      # Світлий фіолетовий для ховеру

CARD_COLORS = [
    "#7DABDE",  # Синій
    "#87D7E0",  # Циан
    "#EA7BBE",  # Рожевий
    "#BCEAA5",  # Ніжно-зелений
    "#B9A5EA",  # Пурпурний
    "#EAA5A6"   # Ніжно-червоний
]

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
except ImportError:
    def play_sound(action):
        pass

import market_db
market_db.init_db()

# Список файлів зображень з репозиторію SecureAuditX/convenientshop
CONVENIENT_IMAGES = [
    "Apple.png", "Avocado.png", "SLiced_White_Bread.png", "Cheese.png", 
    "Chocolate Bar.png", "Diet_Cola.png", "Energy Drink - Red.png", 
    "Orange Juice.png", "Potato_Chips.png", "Salad.png", "Strawberries.png", 
    "Water.png", "Orange.png", "Single Banana.png", "English_Muffins.png", 
    "Honey Wheat Sliced Bread.png", "Flour_Tortillas.png", "Single Plain Bagel.png", 
    "Shake.png", "Oatemeal_Cip.png", "Gum.png", "Salted Peanuts.png", 
    "Sparkling Water.png", "default.png"
]

def download_assets_worker():
    base_url = "https://raw.githubusercontent.com/SecureAuditX/convenientshop/main/images/"
    for name in CONVENIENT_IMAGES:
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

def get_product_image_local(filename, size):
    dest = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(dest):
        try:
            img = Image.open(dest)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception:
            pass
    fallback_dest = os.path.join(ASSETS_DIR, "default.png")
    if os.path.exists(fallback_dest):
        try:
            img = Image.open(fallback_dest)
            return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception:
            pass
    img = Image.new("RGBA", size, (149, 165, 166, 255))
    return ctk.CTkImage(light_image=img, dark_image=img, size=size)

fruits_data = {}

# Товари та категорії
groceries = [
    # Фрукти (fruits)
    ("Яблука Гала", 45, "Свіжі хрусткі яблука сорту Гала.", "fruits", "Apple.png", [("Червоні", "#e74c3c"), ("Зелені", "#2ecc71")]),
    ("Авокадо Хасс", 120, "Стиглі плоди авокадо Хасс преміум якості.", "fruits", "Avocado.png", [("Стиглий", "#27ae60")]),
    ("Полуниця свіжа", 180, "Ароматна літня полуниця з фермерського господарства.", "fruits", "Strawberries.png", [("Червона", "#e74c3c")]),
    ("Апельсини соковиті", 65, "Солодкі добірні апельсини з Іспанії.", "fruits", "Orange.png", [("Помаранчевий", "#e67e22")]),
    ("Банан еквадорський", 55, "Добірні банани, багаті на калій.", "fruits", "Single Banana.png", [("Жовтий", "#f1c40f")]),
    
    # Випічка (bakeries)
    ("Свіжий білий хліб", 22, "М'який нарізний хліб на кожен день.", "bakeries", "SLiced_White_Bread.png", [("Класичний", "#f39c12")]),
    ("Мафіни англійські", 48, "Традиційні пишні англійські мафіни.", "bakeries", "English_Muffins.png", [("Ваніль", "#f1c40f"), ("Шоколад", "#34495e")]),
    ("Пшеничний хліб", 26, "Ароматний корисний хліб з цільного зерна.", "bakeries", "Honey Wheat Sliced Bread.png", [("Медовий", "#d35400")]),
    ("Пшенична тортилья", 35, "М'які тонкі коржі для мексиканських тако та буріто.", "bakeries", "Flour_Tortillas.png", [("Класична", "#f1c40f")]),
    ("Бублик класичний", 18, "Смачний бублик, ідеальний для сніданку.", "bakeries", "Single Plain Bagel.png", [("Звичайний", "#f5b041")]),
    
    # Молочне (dairy)
    ("Сир Чеддер", 110, "Натуральний сир Чеддер середньої витримки.", "dairy", "Cheese.png", [("Твердий", "#f1c40f")]),
    ("Молочний коктейль", 45, "Густий молочний коктейль із полуничним смаком.", "dairy", "Shake.png", [("Полуничний", "#ff7979"), ("Шоколадний", "#8d6e63")]),
    
    # Напої (drinks)
    ("Кола Дієтична", 28, "Освіжаючий напій без цукру.", "drinks", "Diet_Cola.png", [("Класична", "#2c3e50")]),
    ("Енергетик Red Bull", 55, "Напій для підвищення енергії та концентрації.", "drinks", "Energy Drink - Red.png", [("Червоний", "#e74c3c"), ("Синій", "#3498db")]),
    ("Сік апельсиновий", 42, "Свіжовичавлений апельсиновий сік без консервантів.", "drinks", "Orange Juice.png", [("Натуральний", "#e67e22")]),
    ("Мінеральна вода", 15, "Очищена питна мінеральна вода негазована.", "drinks", "Water.png", [("Негазована", "#3498db")]),
    ("Вода газована", 18, "Освіжаюча газована вода з мікроелементами.", "drinks", "Sparkling Water.png", [("Газована", "#85c1e9")]),
    
    # Снеки (snacks)
    ("Шоколадний батончик", 25, "Поживний батончик з молочного шоколаду з горіхами.", "snacks", "Chocolate Bar.png", [("Молочний", "#8d6e63")]),
    ("Картопляні чіпси", 48, "Хрусткі золотисті чіпси зі смаком паприки.", "snacks", "Potato_Chips.png", [("Паприка", "#e74c3c"), ("Сіль", "#f1c40f")]),
    ("Вівсяне печиво", 38, "Ніжне вівсяне печиво з шматочками шоколаду.", "snacks", "Oatemeal_Cip.png", [("Шоколад", "#34495e")]),
    ("Жувальна гумка", 15, "Жувальна гумка з освіжаючим смаком м'яти.", "snacks", "Gum.png", [("М'ята", "#2ecc71")]),
    ("Солоний арахіс", 30, "Смажений солоний арахіс до напоїв.", "snacks", "Salted Peanuts.png", [("Солоний", "#f39c12")])
]

# Створюємо 100+ товарів
for idx, (base_name, price, desc, cat, img_name, colors) in enumerate(groceries):
    for sub in range(5):
        unique_name = f"{base_name} ({sub + 1} партія)" if sub > 0 else base_name
        fruits_data[unique_name] = {
            "price": price + (sub * 3),
            "desc": desc,
            "category": cat,
            "image": img_name,
            "colors": colors
        }

LANGS = {
    "ua": {
        "title": "Мегамаркет Все-в-Одному",
        "search_label": "Пошук:",
        "balance_label": "Баланс:",
        "topup_btn": "+ Поповнити",
        "history_btn": "Історія",
        "cart_btn": "Кошик",
        "details_btn": "Детальніше",
        "all_cat": "Усі",
        "tech_cat": "Випічка",
        "fruits_cat": "Фрукти",
        "home_cat": "Молочне",
        "sport_cat": "Напої",
        "clothing_cat": "Снеки",
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
        "title": "ConvenientShop",
        "search_label": "Search:",
        "balance_label": "Balance:",
        "topup_btn": "+ Top Up",
        "history_btn": "History",
        "cart_btn": "Cart",
        "details_btn": "Details",
        "all_cat": "All",
        "tech_cat": "Bakeries",
        "fruits_cat": "Fruits",
        "home_cat": "Dairy",
        "sport_cat": "Drinks",
        "clothing_cat": "Snacks",
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
        "cart_btn": "Корзина",
        "details_btn": "Подробнее",
        "all_cat": "Все",
        "tech_cat": "Выпечка",
        "fruits_cat": "Фрукты",
        "home_cat": "Молочное",
        "sport_cat": "Напитки",
        "clothing_cat": "Снеки",
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
        self.geometry("1020x760")
        self.title("ConvenientShop")
        
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

# --- ЕКРАН АВТОРИЗАЦІЇ (ДИЗАЙН 100% ВІДПОВІДАЄ CONVENIENTSHOP) ---
class AuthScreen(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = app_controller
        
        self.card = ctk.CTkFrame(
            self, 
            corner_radius=16, 
            width=800, 
            height=660, 
            fg_color=BG_COLOR
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_columnconfigure(1, weight=1)
        self.card.grid_rowconfigure(0, weight=1)
        
        self.left_branding_frame = ctk.CTkFrame(self.card, fg_color=BG_COLOR)
        self.left_branding_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.left_branding_frame.grid_columnconfigure(0, weight=1)
        self.left_branding_frame.grid_rowconfigure(0, weight=1)
        
        # Логотип (Малюємо векторний стікер логотипу)
        self.left_canvas = tk.Canvas(self.left_branding_frame, width=240, height=340, bg=BG_COLOR, bd=0, highlightthickness=0)
        self.left_canvas.pack(fill="both", expand=True)
        self.draw_vector_graphics()
        
        # Форма авторизації (Кольори та розміри з оригінального репозиторію!)
        self.login_frame = ctk.CTkFrame(self.card, fg_color=FRAME_COLOR, corner_radius=20, width=380, height=520)
        self.login_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=50)
        self.login_frame.pack_propagate(False)
        
        self.is_register_mode = False
        
        self.lbl_title = ctk.CTkLabel(self.login_frame, text="LOGIN", font=("Arial", 36, "bold"), text_color=PRIMARY_COLOR)
        self.lbl_title.pack(pady=(40, 30))
        
        # Поля введення
        self.user_lbl = ctk.CTkLabel(self.login_frame, text="EMAIL / USERNAME", font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR, anchor="w")
        self.user_lbl.pack(fill="x", padx=45, pady=(5, 2))
        
        self.user_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="enter username", font=("Arial", 14), 
            width=290, height=45, fg_color=PRIMARY_COLOR, text_color="white", 
            placeholder_text_color=FRAME_COLOR, border_color=PRIMARY_COLOR, 
            corner_radius=10, border_width=2
        )
        self.user_entry.pack(padx=40, pady=(0, 10))
        
        self.pass_lbl = ctk.CTkLabel(self.login_frame, text="PASSWORD", font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR, anchor="w")
        self.pass_lbl.pack(fill="x", padx=45, pady=(5, 2))
        
        self.pass_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="enter password", show="*", font=("Arial", 14), 
            width=290, height=45, fg_color=PRIMARY_COLOR, text_color="white", 
            placeholder_text_color=FRAME_COLOR, border_color=PRIMARY_COLOR, 
            corner_radius=10, border_width=2
        )
        self.pass_entry.pack(padx=40, pady=(0, 5))
        
        self.confirm_pass_lbl = ctk.CTkLabel(self.login_frame, text="CONFIRM PASSWORD", font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR, anchor="w")
        self.confirm_pass_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="confirm password", show="*", font=("Arial", 14), 
            width=290, height=45, fg_color=PRIMARY_COLOR, text_color="white", 
            placeholder_text_color=FRAME_COLOR, border_color=PRIMARY_COLOR, 
            corner_radius=10, border_width=2
        )
        
        # Кнопка входу (Кругла кнопка з радіусом 50)
        self.btn_action = ctk.CTkButton(
            self.login_frame, text="Login", command=self.handle_action, 
            width=290, height=45, font=("Arial", 20, "bold"), 
            fg_color=PRIMARY_COLOR, hover_color="#4338CA", text_color="white", 
            corner_radius=50
        )
        self.btn_action.pack(padx=40, pady=(15, 10))
        
        # Перемикання режимів
        self.toggle_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.toggle_frame.pack(pady=(5, 20))
        
        self.toggle_lbl = ctk.CTkLabel(self.toggle_frame, text="Don't have an account?", font=("Arial", 12), text_color=PRIMARY_COLOR)
        self.toggle_lbl.pack(side="left", padx=2)
        self.btn_toggle = ctk.CTkButton(
            self.toggle_frame, text="Register", command=self.toggle_mode, 
            fg_color="transparent", text_color=PRIMARY_COLOR, hover_color=None, 
            width=60, height=20, font=("Arial", 12, "underline"), cursor="hand2"
        )
        self.btn_toggle.pack(side="left")
        
        # Показати пароль
        self.show_pass_var = tk.BooleanVar(value=False)
        self.chk_show_pass = ctk.CTkCheckBox(self.login_frame, text="Показати пароль", variable=self.show_pass_var, command=self.toggle_password_visibility, font=("Arial", 10), text_color=PRIMARY_COLOR, border_color=PRIMARY_COLOR)
        self.chk_show_pass.pack(pady=2)

    def toggle_mode(self):
        play_sound("click")
        self.is_register_mode = not self.is_register_mode
        
        if self.is_register_mode:
            self.lbl_title.configure(text="REGISTER")
            self.btn_action.configure(text="Register")
            self.toggle_lbl.configure(text="Already have an account?")
            self.btn_toggle.configure(text="Login")
            
            self.btn_action.pack_forget()
            self.toggle_frame.pack_forget()
            self.chk_show_pass.pack_forget()
            
            self.confirm_pass_lbl.pack(fill="x", padx=45, pady=(5, 2))
            self.confirm_pass_entry.pack(padx=40, pady=(0, 5))
            
            self.btn_action.pack(padx=40, pady=(15, 10))
            self.toggle_frame.pack(pady=(5, 20))
            self.chk_show_pass.pack(pady=2)
        else:
            self.lbl_title.configure(text="LOGIN")
            self.btn_action.configure(text="Login")
            self.toggle_lbl.configure(text="Don't have an account?")
            self.btn_toggle.configure(text="Register")
            
            self.confirm_pass_lbl.pack_forget()
            self.confirm_pass_entry.pack_forget()
            
            self.btn_action.pack_forget()
            self.toggle_frame.pack_forget()
            self.chk_show_pass.pack_forget()
            
            self.btn_action.pack(padx=40, pady=(15, 10))
            self.toggle_frame.pack(pady=(5, 20))
            self.chk_show_pass.pack(pady=2)

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

    def draw_vector_graphics(self):
        self.left_canvas.delete("all")
        circle_color = FRAME_COLOR
        stroke_color = PRIMARY_COLOR
        
        # Круглий фоновий елемент
        self.left_canvas.create_oval(50, 90, 190, 230, fill=circle_color, outline="")
        self.left_canvas.create_oval(30, 70, 42, 82, outline="#00f2fe", width=2)
        self.left_canvas.create_polygon(210, 80, 220, 95, 200, 95, outline="#2ecc71", fill="", width=2)
        self.left_canvas.create_polygon(25, 230, 35, 245, 15, 245, outline="#e74c3c", fill="", width=2)
        self.left_canvas.create_oval(215, 240, 225, 250, outline="#3498db", width=2)
        
        # Стилізований 3D-ноутбук (вектор)
        self.left_canvas.create_rectangle(90, 125, 150, 165, fill=BG_COLOR, outline=stroke_color, width=2)
        self.left_canvas.create_polygon(80, 165, 160, 165, 165, 172, 75, 172, fill=circle_color, outline=stroke_color, width=2)
        self.left_canvas.create_line(115, 170, 125, 170, fill=stroke_color, width=2)
        self.left_canvas.create_oval(115, 133, 125, 143, fill="", outline=stroke_color, width=2)
        self.left_canvas.create_arc(107, 145, 133, 165, start=0, extent=180, style="arc", outline=stroke_color, width=2)

    def switch_theme(self):
        # Оскільки в convenientshop тема фіксована (light), ми залишаємо цей метод для сумісності
        pass

# --- ГОЛОВНИЙ ЕКРАН З БІЧНОЮ НАВІГАЦІЄЮ ---
class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, app_controller):
        super().__init__(parent, fg_color=BG_COLOR)
        self.controller = app_controller
        
        # Сайдбар в лавандових тонах як у convenientshop
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=FRAME_COLOR, corner_radius=10)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="CONVENIENT SHOP", font=("Arial", 18, "bold"), text_color=PRIMARY_COLOR)
        self.lbl_logo.pack(pady=20)
        
        # Аватар користувача
        self.profile_lbl = ctk.CTkLabel(self.sidebar, text="👤", font=("Arial", 48), text_color=PRIMARY_COLOR)
        self.profile_lbl.pack(pady=5)
        
        self.username_lbl = ctk.CTkLabel(self.sidebar, text=logged_in_user, font=("Arial", 14, "bold"), text_color="black")
        self.username_lbl.pack(pady=2)
        
        self.balance_lbl = ctk.CTkLabel(self.sidebar, text="0 грн", font=("Arial", 12, "bold"), text_color="#2ecc71")
        self.balance_lbl.pack(pady=2)
        
        btn_topup = ctk.CTkButton(self.sidebar, text="+ Поповнити", command=self.topup_balance, width=120, height=28, font=("Arial", 10, "bold"), fg_color=PRIMARY_COLOR, hover_color="#4338CA")
        btn_topup.pack(pady=5)
        
        self.nav_buttons = {}
        navs = [
            ("Каталог", self.show_catalog),
            ("Кошик", self.show_cart),
            ("Аналітика", self.show_analytics),
            ("Історія", self.show_history),
            ("Налаштування", self.show_settings)
        ]
        for name, cmd in navs:
            # Навігаційні кнопки як у convenientshop: прозорі з жирним шрифтом на ховері
            btn = ctk.CTkButton(self.sidebar, text=name, anchor="w", fg_color="transparent", text_color="black", hover_color=HOVER_COLOR, command=cmd, font=("Arial", 14, "bold"), height=42)
            btn.pack(fill="x", padx=10, pady=5)
            self.nav_buttons[name] = btn
            
        btn_logout = ctk.CTkButton(self.sidebar, text="Вийти", anchor="w", fg_color="#e74c3c", hover_color="#c0392b", command=self.logout, font=("Arial", 12, "bold"))
        btn_logout.pack(side="bottom", fill="x", padx=10, pady=20)
        
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.active_panel = None
        self.show_catalog()
        self.update_profile_info()

    def update_sidebar_state(self, active_name):
        cart_count = sum(item["qty"] for item in cart)
        cart_text = f"Кошик ({cart_count})" if cart_count > 0 else "Кошик"
        
        for name, btn in self.nav_buttons.items():
            if name == "Кошик":
                btn.configure(text=cart_text)
            
            if name == active_name:
                btn.configure(fg_color=HOVER_COLOR, text_color="black")
            else:
                btn.configure(fg_color="transparent", text_color="black")

    def update_profile_info(self):
        balance = market_db.get_balance(logged_in_user)
        self.balance_lbl.configure(text=f"{balance} грн")
        if self.active_panel:
            panel_name = "Каталог"
            if isinstance(self.active_panel, CartPanel): panel_name = "Кошик"
            elif isinstance(self.active_panel, AnalyticsPanel): panel_name = "Аналітика"
            elif isinstance(self.active_panel, HistoryPanel): panel_name = "Історія"
            elif isinstance(self.active_panel, SettingsPanel): panel_name = "Налаштування"
            self.update_sidebar_state(panel_name)

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

    def switch_panel(self, panel_class, active_name, *args, **kwargs):
        if self.active_panel:
            self.active_panel.pack_forget()
            self.active_panel.destroy()
        self.active_panel = panel_class(self.content_container, self, *args, **kwargs)
        self.active_panel.pack(fill="both", expand=True)
        self.update_sidebar_state(active_name)

    def show_catalog(self):
        self.switch_panel(CatalogPanel, "Каталог")

    def show_cart(self):
        self.switch_panel(CartPanel, "Кошик")

    def show_analytics(self):
        self.switch_panel(AnalyticsPanel, "Аналітика")

    def show_history(self):
        self.switch_panel(HistoryPanel, "Історія")

    def show_settings(self):
        self.switch_panel(SettingsPanel, "Налаштування")

# --- ПАНЕЛЬ КАТАЛОГУ (РІЗНОКОЛЬОРОВІ КАРТКИ З КОЛІРНОЇ ПАЛІТРИ CONVENIENTSHOP) ---
class CatalogPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        top_bar = ctk.CTkFrame(self, fg_color=FRAME_COLOR, corner_radius=10)
        top_bar.pack(fill="x", pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(top_bar, placeholder_text="Пошук продуктів...", width=200, fg_color="white", text_color="black", border_color=PRIMARY_COLOR)
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self.filter_products)
        
        self.active_cat = "all"
        self.cat_buttons = {}
        
        cats = [("Усі", "all"), ("Випічка", "bakeries"), ("Молочне", "dairy"), ("Фрукти", "fruits"), ("Напої", "drinks"), ("Снеки", "snacks")]
        for text, key in cats:
            btn = ctk.CTkButton(top_bar, text=text, command=lambda k=key: self.set_category(k), width=70, height=28, font=("Arial", 10, "bold"), fg_color=PRIMARY_COLOR, hover_color="#4338CA")
            btn.pack(side="left", padx=3)
            self.cat_buttons[key] = btn
            
        self.sort_menu = ctk.CTkOptionMenu(top_bar, values=["Дешевші", "Дорожчі"], command=self.set_sorting, width=110, fg_color=PRIMARY_COLOR, button_color=PRIMARY_COLOR)
        self.sort_menu.pack(side="right", padx=10, pady=10)
        self.active_sort = "cheap"
        
        self.fav_only_var = tk.BooleanVar(value=False)
        self.fav_btn = ctk.CTkCheckBox(top_bar, text="Обране", variable=self.fav_only_var, command=self.draw_grid, font=("Arial", 10, "bold"), text_color="black", border_color=PRIMARY_COLOR)
        self.fav_btn.pack(side="right", padx=10)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)
        
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
            
        for key, btn in self.cat_buttons.items():
            if key == self.active_cat:
                btn.configure(fg_color="#3498db")
            else:
                btn.configure(fg_color=PRIMARY_COLOR)
                
        search_query = self.search_entry.get().strip().lower()
        favorites = market_db.get_favorites(logged_in_user)
        
        filtered = []
        for name, data in fruits_data.items():
            if search_query and search_query not in name.lower(): continue
            if self.active_cat != "all" and data["category"] != self.active_cat: continue
            if self.fav_only_var.get() and name not in favorites: continue
            filtered.append((name, data))
            
        def sort_key(item):
            name, data = item
            is_fav = 0 if name in favorites else 1
            price_val = data["price"] if self.active_sort == "cheap" else -data["price"]
            return (is_fav, price_val)
            
        filtered.sort(key=sort_key)
        
        cols = 4
        col = 0
        row = 0
        for idx, (name, data) in enumerate(filtered[:36]):
            # Динамічно фарбуємо картки у пастельні кольори як у convenientshop!
            card_bg = CARD_COLORS[idx % len(CARD_COLORS)]
            
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=12, width=170, height=240, fg_color=card_bg)
            card.grid(row=row, column=col, padx=8, pady=8)
            card.grid_propagate(False)
            
            # Ефект ховеру
            def on_enter(e, c=card):
                c.configure(border_width=2, border_color="white")
            def on_leave(e, c=card):
                c.configure(border_width=0)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
            
            is_fav = name in favorites
            heart_text = "Liked" if is_fav else "Like"
            heart_color = "red" if is_fav else "gray"
            heart_btn = ctk.CTkButton(card, text=heart_text, text_color=heart_color, width=38, height=18, fg_color="transparent", hover_color=None, font=("Arial", 9, "bold"), command=lambda n=name: self.toggle_favorite(n))
            heart_btn.place(relx=0.82, rely=0.08, anchor="center")
            
            photo = get_product_image_local(data["image"], (80, 80))
            img_lbl = ctk.CTkLabel(card, image=photo, text="")
            img_lbl.pack(pady=(12, 2))
            
            lbl_name = ctk.CTkLabel(card, text=name, font=("Arial", 12, "bold"), text_color="black", wraplength=150)
            lbl_name.pack(pady=2, fill="x", padx=6)
            
            lbl_price = ctk.CTkLabel(card, text=f"{data['price']} грн", font=("Arial", 12, "bold"), text_color="#1e1e2e")
            lbl_price.pack(pady=1)
            
            btn_details = ctk.CTkButton(card, text="Детальніше", command=lambda n=name: self.main_screen.switch_panel(DetailsPanel, "Каталог", n), width=130, height=28, font=("Arial", 11, "bold"), fg_color=PRIMARY_COLOR, hover_color="#4338CA", text_color="white")
            btn_details.pack(side="bottom", pady=8)
            
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
        
        btn_back = ctk.CTkButton(self, text="← Назад", command=lambda: self.main_screen.show_catalog(), width=80, height=28, fg_color=PRIMARY_COLOR, hover_color="#4338CA")
        btn_back.pack(anchor="w", pady=10)
        
        left_box = ctk.CTkFrame(self, corner_radius=12, fg_color=FRAME_COLOR)
        left_box.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        photo = get_product_image_local(self.data["image"], (140, 140))
        self.img_lbl = ctk.CTkLabel(left_box, image=photo, text="")
        self.img_lbl.pack(pady=20)
        
        lbl_title = ctk.CTkLabel(left_box, text=name, font=("Arial", 16, "bold"), text_color="black", wraplength=280)
        lbl_title.pack(pady=5)
        
        lbl_desc = ctk.CTkLabel(left_box, text=self.data["desc"], font=("Arial", 12, "italic"), text_color="black", wraplength=280)
        lbl_desc.pack(pady=5)
        
        lbl_price = ctk.CTkLabel(left_box, text=f"Ціна: {self.data['price']} грн", font=("Arial", 15, "bold"), text_color=PRIMARY_COLOR)
        lbl_price.pack(pady=10)
        
        ctk.CTkLabel(left_box, text="Виберіть сорт/колір:", font=("Arial", 12, "bold"), text_color="black").pack()
        self.selected_color = ctk.StringVar(value=self.data["colors"][0][0])
        color_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        color_frame.pack(pady=5)
        
        for color_name, color_hex in self.data["colors"]:
            btn_c = tk.Button(color_frame, bg=color_hex, width=4, height=1, relief="groove", command=lambda c=color_name: self.selected_color.set(c))
            btn_c.pack(side="left", padx=5)
            
        qty_frame = ctk.CTkFrame(left_box, fg_color="transparent")
        qty_frame.pack(pady=10)
        ctk.CTkLabel(qty_frame, text="Кількість:", text_color="black", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        self.qty_spin = ttk.Spinbox(qty_frame, from_=1, to=50, width=5, font=("Arial", 11), justify="center")
        self.qty_spin.pack(side="left", padx=5)
        self.qty_spin.set(1)
        
        btn_add = ctk.CTkButton(left_box, text="Додати в кошик", command=self.add_to_cart, fg_color="#2ecc71", hover_color="#27ae60", font=("Arial", 13, "bold"))
        btn_add.pack(pady=10)
        
        right_box = ctk.CTkFrame(self, corner_radius=12, fg_color=FRAME_COLOR)
        right_box.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(right_box, text="Відгуки та оцінки:", font=("Arial", 14, "bold"), text_color="black").pack(pady=10)
        
        self.reviews_frame = ctk.CTkScrollableFrame(right_box, height=220, fg_color="white")
        self.reviews_frame.pack(fill="both", expand=True, padx=10)
        
        form_frame = ctk.CTkFrame(right_box, fg_color="transparent")
        form_frame.pack(fill="x", padx=10, pady=15)
        
        self.rating_spin = ttk.Spinbox(form_frame, from_=1, to=5, width=3, justify="center")
        self.rating_spin.grid(row=0, column=0, padx=5, pady=5)
        self.rating_spin.set(5)
        
        self.rev_entry = ctk.CTkEntry(form_frame, placeholder_text="Ваш відгук...", width=160, fg_color="white", text_color="black")
        self.rev_entry.grid(row=0, column=1, padx=5, pady=5)
        
        btn_submit = ctk.CTkButton(form_frame, text="Надіслати", command=self.submit_review, width=80, fg_color=PRIMARY_COLOR, hover_color="#4338CA")
        btn_submit.grid(row=0, column=2, padx=5, pady=5)
        
        self.refresh_reviews()

    def refresh_reviews(self):
        for w in self.reviews_frame.winfo_children():
            w.destroy()
            
        revs = market_db.get_reviews(self.name)
        if revs:
            avg = sum(r['rating'] for r in revs) / len(revs)
            stars_text = "*" * int(round(avg)) + "." * (5 - int(round(avg)))
            ctk.CTkLabel(self.reviews_frame, text=f"Рейтинг: {stars_text} ({avg:.1f}/5)", font=("Arial", 12, "bold"), text_color="#f1c40f").pack(anchor="w")
            for r in revs[-5:]:
                ctk.CTkLabel(self.reviews_frame, text=f"• {r['username']} ({r['rating']}/5): {r['text']}", font=("Arial", 11), anchor="w", justify="left", text_color="black").pack(fill="x", pady=2)
        else:
            ctk.CTkLabel(self.reviews_frame, text="Відгуків ще немає.", font=("Arial", 11, "italic"), text_color="black").pack(anchor="w")

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

# --- ПАНЕЛЬ КОШИКА З POS-ТАБЛИЦЕЮ ---
class CartPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        left_box = ctk.CTkFrame(self, corner_radius=12, fg_color=FRAME_COLOR)
        left_box.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(left_box, text="Кошик товарів (POS Специфікація)", font=("Arial", 16, "bold"), text_color=PRIMARY_COLOR).pack(pady=10)
        
        header_frame = ctk.CTkFrame(left_box, height=30, fg_color="#2b2b3d")
        header_frame.pack(fill="x", padx=10, pady=(5, 0))
        
        ctk.CTkLabel(header_frame, text="Товар", font=("Arial", 10, "bold"), width=160, anchor="w", text_color="white").pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="К-сть", font=("Arial", 10, "bold"), width=60, anchor="center", text_color="white").pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="Ціна", font=("Arial", 10, "bold"), width=70, anchor="e", text_color="white").pack(side="left", padx=10)
        ctk.CTkLabel(header_frame, text="Дія", font=("Arial", 10, "bold"), width=40, anchor="center", text_color="white").pack(side="right", padx=10)
        
        self.items_frame = ctk.CTkScrollableFrame(left_box, fg_color="white")
        self.items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.total_lbl = ctk.CTkLabel(left_box, text="Разом до сплати: 0 грн", font=("Arial", 14, "bold"), text_color=PRIMARY_COLOR)
        self.total_lbl.pack(pady=10)
        
        btn_clear = ctk.CTkButton(left_box, text="Очистити кошик", command=self.clear_cart, fg_color="#95a5a6", hover_color="#7f8c8d")
        btn_clear.pack(pady=5)
        
        self.right_box = ctk.CTkFrame(self, corner_radius=12, fg_color=FRAME_COLOR)
        self.right_box.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(self.right_box, text="Дані для доставки замовлення", font=("Arial", 14, "bold"), text_color="black").pack(pady=15)
        
        self.phone_entry = ctk.CTkEntry(self.right_box, placeholder_text="Номер телефону (+380...)", fg_color="white", text_color="black")
        self.phone_entry.pack(pady=6, padx=20, fill="x")
        self.phone_entry.insert(0, "+380")
        
        self.email_entry = ctk.CTkEntry(self.right_box, placeholder_text="Електронна пошта (Email)", fg_color="white", text_color="black")
        self.email_entry.pack(pady=6, padx=20, fill="x")
        
        self.address_entry = ctk.CTkEntry(self.right_box, placeholder_text="Адреса доставки", fg_color="white", text_color="black")
        self.address_entry.pack(pady=6, padx=20, fill="x")
        
        self.deliv_combo = ctk.CTkOptionMenu(self.right_box, values=["Courier", "Nova Poshta", "Self-pickup"], fg_color=PRIMARY_COLOR, button_color=PRIMARY_COLOR)
        self.deliv_combo.pack(pady=6, padx=20, fill="x")
        
        self.pay_combo = ctk.CTkOptionMenu(self.right_box, values=["Balance", "Card on delivery", "Cash"], fg_color=PRIMARY_COLOR, button_color=PRIMARY_COLOR)
        self.pay_combo.pack(pady=6, padx=20, fill="x")
        
        btn_order = ctk.CTkButton(self.right_box, text="Оформити замовлення", command=self.checkout, fg_color="#2ecc71", hover_color="#27ae60", font=("Arial", 13, "bold"))
        btn_order.pack(pady=20)
        
        self.refresh_cart_list()

    def refresh_cart_list(self):
        for w in self.items_frame.winfo_children():
            w.destroy()
            
        if not cart:
            ctk.CTkLabel(self.items_frame, text="Кошик порожній", font=("Arial", 11), text_color="black").pack(pady=30)
            self.total_lbl.configure(text="Разом до сплати: 0 грн")
            return
            
        total_price = 0
        for index, item in enumerate(cart):
            sub = item["price"] * item["qty"]
            total_price += sub
            
            row = ctk.CTkFrame(self.items_frame, fg_color="#f8f9fa")
            row.pack(fill="x", pady=4)
            
            ctk.CTkLabel(row, text=f"{item['name']} ({item['color']})", font=("Arial", 11, "bold"), width=160, anchor="w", wraplength=150, text_color="black").pack(side="left", padx=10)
            
            qty_spin = ttk.Spinbox(row, from_=1, to=99, width=3, justify="center")
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
            self.total_lbl.configure(text=f"Разом до сплати: {total_price} грн")

    def update_qty(self, idx, sp):
        try:
            val = int(sp.get())
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

# --- ПАНЕЛЬ АНАЛІТИКИ ---
class AnalyticsPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text="Панель аналітики та звітів", font=("Arial", 16, "bold"), text_color="black").pack(pady=10)
        
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", pady=10)
        
        orders = market_db.get_orders(logged_in_user)
        total_spent = sum(o["total"] for o in orders)
        total_items = sum(o["items_count"] for o in orders)
        avg_receipt = int(total_spent / len(orders)) if orders else 0
        
        self.create_kpi_card(cards_frame, "Загальні витрати", f"{total_spent} грн", "#2ecc71").pack(side="left", fill="both", expand=True, padx=5)
        self.create_kpi_card(cards_frame, "Куплено товарів", f"{total_items} шт", "#3498db").pack(side="left", fill="both", expand=True, padx=5)
        self.create_kpi_card(cards_frame, "Середній чек", f"{avg_receipt} грн", "#e67e22").pack(side="left", fill="both", expand=True, padx=5)
        
        chart_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=FRAME_COLOR)
        chart_frame.pack(fill="both", expand=True, pady=10, padx=5)
        
        ctk.CTkLabel(chart_frame, text="Динаміка замовлень", font=("Arial", 13, "bold"), text_color="black").pack(pady=5)
        
        self.canvas = tk.Canvas(chart_frame, bg="white", bd=0, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)
        self.canvas.bind("<Configure>", lambda e: self.draw_chart(orders))

    def create_kpi_card(self, parent, title, value, accent_color):
        card = ctk.CTkFrame(parent, corner_radius=10, height=80, fg_color=FRAME_COLOR)
        card.pack_propagate(False)
        ctk.CTkLabel(card, text=title, font=("Arial", 11, "bold"), text_color="gray").pack(pady=(10, 2))
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
            self.canvas.create_line(40, y, w - 20, y, fill="#e2e2e2", width=1)
            
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
        
        ctk.CTkLabel(self, text="Історія замовлень", font=("Arial", 16, "bold"), text_color="black").pack(pady=10)
        
        orders = market_db.get_orders(logged_in_user)
        if not orders:
            ctk.CTkLabel(self, text="Замовлень ще не було", font=("Arial", 11, "italic"), text_color="black").pack(pady=40)
            return
            
        for index, order in enumerate(orders):
            row = ctk.CTkFrame(self, fg_color=FRAME_COLOR)
            row.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(row, text=f"Замовлення #{len(orders)-index} [{order['date']}]", font=("Arial", 11, "bold"), text_color="black").pack(anchor="w", padx=15, pady=4)
            ctk.CTkLabel(row, text=f"Товарів: {order['items_count']} шт. | Сума: {order['total']} грн", font=("Arial", 10), text_color="#2e7d32").pack(anchor="w", padx=15, pady=2)

# --- ПАНЕЛЬ НАЛАШТУВАНЬ ---
class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, main_screen):
        super().__init__(parent, fg_color="transparent")
        self.main_screen = main_screen
        
        ctk.CTkLabel(self, text="Налаштування", font=("Arial", 16, "bold"), text_color="black").pack(pady=10)
        
        card = ctk.CTkFrame(self, width=400, height=350, fg_color=FRAME_COLOR)
        card.pack(pady=15, padx=20)
        
        ctk.CTkLabel(card, text="Мова інтерфейсу:", font=("Arial", 11, "bold"), text_color="black").pack(anchor="w", padx=30, pady=10)
        lang_btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        lang_btn_frame.pack(fill="x", padx=30)
        
        ctk.CTkButton(lang_btn_frame, text="Українська", width=90, fg_color=PRIMARY_COLOR, hover_color="#4338CA", command=lambda: self.change_lang("ua")).pack(side="left", padx=5)
        ctk.CTkButton(lang_btn_frame, text="English", width=90, fg_color=PRIMARY_COLOR, hover_color="#4338CA", command=lambda: self.change_lang("en")).pack(side="left", padx=5)
        ctk.CTkButton(lang_btn_frame, text="Русский", width=90, fg_color=PRIMARY_COLOR, hover_color="#4338CA", command=lambda: self.change_lang("ru")).pack(side="left", padx=5)
        
        ctk.CTkLabel(card, text="Тема оформлення (Фіксовано):", font=("Arial", 11, "bold"), text_color="black").pack(anchor="w", padx=30, pady=15)
        self.theme_lbl = ctk.CTkLabel(card, text="Світла тема за замовчуванням (ConvenientShop Style)", font=("Arial", 11, "italic"), text_color="gray")
        self.theme_lbl.pack(padx=30, anchor="w")
        
        self.sound_var = tk.BooleanVar(value=sound_enabled)
        sound_chk = ctk.CTkCheckBox(card, text="Звукові ефекти", variable=self.sound_var, command=self.toggle_sound, text_color="black", border_color=PRIMARY_COLOR)
        sound_chk.pack(anchor="w", padx=30, pady=25)

    def change_lang(self, lang):
        global active_lang
        active_lang = lang
        play_sound("click")
        self.main_screen.lbl_logo.configure(text="CONVENIENT SHOP")
        nav_texts = ["Каталог", "Кошик", "Аналітика", "Історія", "Налаштування"]
        for t in nav_texts:
            if t in self.main_screen.nav_buttons:
                self.main_screen.nav_buttons[t].configure(text=t)
        self.main_screen.show_settings()

    def toggle_theme(self, choice):
        pass

    def toggle_sound(self):
        global sound_enabled
        sound_enabled = self.sound_var.get()
        play_sound("click")

from tkinter import ttk
if __name__ == "__main__":
    main_app = App()
    main_app.mainloop()
