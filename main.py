import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import urllib.request
import datetime
import random
import math
import threading

# Глобальні змінні налаштувань
sound_enabled = True
current_theme = "light"
active_lang = "ua"
logged_in_user = None
session_discount = 0.0
cart = []
order_history = []

# Спробуємо імпортувати winsound для звуків на Windows
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

# Кольорові палітри для тем
THEMES = {
    "light": {
        "bg": "#f8f9fa",
        "card_bg": "#ffffff",
        "header_bg": "#ffffff",
        "text": "#212529",
        "text_secondary": "#6c757d",
        "accent": "#4a90e2",
        "border": "#e0e0e0"
    },
    "dark": {
        "bg": "#1e1e2e",
        "card_bg": "#252538",
        "header_bg": "#252538",
        "text": "#cdd6f4",
        "text_secondary": "#a6adc8",
        "accent": "#89b4fa",
        "border": "#45475a"
    }
}

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache_images")
os.makedirs(CACHE_DIR, exist_ok=True)

CATEGORY_URLS = {
    "tech": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f4bb.png",
    "fruits": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f34e.png",
    "home": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f6cb.png",
    "sport": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/26bd.png",
    "clothing": "https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/1f455.png"
}

# Завантаження зображень з інтернету
def download_image(cat, url):
    dest = os.path.join(CACHE_DIR, f"{cat}.png")
    if not os.path.exists(dest):
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print(f"Помилка завантаження зображення для {cat}: {e}")

for cat, url in CATEGORY_URLS.items():
    t = threading.Thread(target=download_image, args=(cat, url))
    t.daemon = True
    t.start()

# Генерація 500+ товарів
fruits_data = {}
for i in range(1, 101):
    fruits_data[f"Ноутбук Pro-{i} 💻"] = {
        "price": 15000 + i * 200,
        "desc": f"Високопродуктивний ноутбук Pro версії {i} для роботи та ігор.",
        "category": "tech",
        "colors": [("Сріблястий 💿", "#bdc3c7"), ("Чорний 🌑", "#2c3e50")]
    }
for i in range(1, 101):
    fruits_data[f"Яблуко Голден-{i} 🍎"] = {
        "price": 20 + (i % 15),
        "desc": f"Свіжі соковиті добірні яблука Голден, партія #{i}.",
        "category": "fruits",
        "colors": [("Жовте 🟡", "#f1c40f"), ("Червоне 🔴", "#e74c3c")]
    }
for i in range(1, 101):
    fruits_data[f"Лампа Loft-{i} 💡"] = {
        "price": 300 + i * 15,
        "desc": f"Стильна дизайнерська настільна лампа в стилі Loft #{i}.",
        "category": "home",
        "colors": [("Чорний 🌑", "#2c3e50"), ("Білий ⚪", "#ffffff")]
    }
for i in range(1, 101):
    fruits_data[f"Футбольний М'яч-{i} ⚽"] = {
        "price": 400 + i * 10,
        "desc": f"Міцний професійний м'яч для гри на будь-якому покритті #{i}.",
        "category": "sport",
        "colors": [("Біло-чорний ⚽", "#ffffff"), ("Червоний 🔴", "#e74c3c")]
    }
for i in range(1, 101):
    fruits_data[f"Футболка Класик-{i} 👕"] = {
        "price": 250 + i * 5,
        "desc": f"Зручна бавовняна футболка класичного крою #{i}.",
        "category": "clothing",
        "colors": [("Синій 🔵", "#3498db"), ("Чорний 🌑", "#2c3e50")]
    }

LANGS = {
    "ua": {
        "title": "Мегамаркет Все-в-Одному 🛒",
        "search_label": "🔍 Пошук:",
        "balance_label": "Баланс:",
        "topup_btn": "+ Поповнити",
        "history_btn": "📜 Історія",
        "wheel_btn": "🎡 Колесо Фортуни",
        "cart_btn": "🛒 Кошик",
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
        "cart_empty": "Кошик порожній 😔",
        "subtotal_lbl": "Сума:",
        "discount_lbl": "Знижка:",
        "total_lbl": "Разом до сплати:",
        "checkout_btn": "Оформити",
        "clear_cart_btn": "Очистити кошик",
        "history_title": "Історія замовлень",
        "no_orders": "Замовлень ще не було 🤷‍♂️",
        "order_str": "Замовлення",
        "items_count_str": "Товарів",
        "fortune_title": "🎡 Колесо Фортуни",
        "spin_btn": "Крутити 🎡",
        "congrats": "Вітаємо!",
        "win_discount": "Ви виграли знижку",
        "try_again": "Спробуйте ще раз! 🍀",
        "insufficient_balance": "Недостатньо коштів на балансі! Поповніть його.",
        "success_purchase": "Дякуємо за замовлення! Чек збережено 📄",
        "settings_btn": "⚙️ Налаштування",
        "settings_title": "Налаштування програми",
        "lang_lbl": "Мова інтерфейсу:",
        "theme_lbl": "Тема оформлення:",
        "theme_light": "Світла ☀️",
        "theme_dark": "Темна 🌙",
        "sound_chk": "Звукові ефекти (Beep)"
    },
    "en": {
        "title": "Megamarket All-in-One 🛒",
        "search_label": "🔍 Search:",
        "balance_label": "Balance:",
        "topup_btn": "+ Top Up",
        "history_btn": "📜 History",
        "wheel_btn": "🎡 Fortune Wheel",
        "cart_btn": "🛒 Cart",
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
        "cart_empty": "Cart is empty 😔",
        "subtotal_lbl": "Subtotal:",
        "discount_lbl": "Discount:",
        "total_lbl": "Total to pay:",
        "checkout_btn": "Checkout",
        "clear_cart_btn": "Clear Cart",
        "history_title": "Order History",
        "no_orders": "No orders yet 🤷‍♂️",
        "order_str": "Order",
        "items_count_str": "Items",
        "fortune_title": "🎡 Wheel of Fortune",
        "spin_btn": "Spin 🎡",
        "congrats": "Congratulations!",
        "win_discount": "You won a discount of",
        "try_again": "Try again! 🍀",
        "insufficient_balance": "Insufficient balance! Please top up.",
        "success_purchase": "Thank you! Receipt saved 📄",
        "settings_btn": "⚙️ Settings",
        "settings_title": "Application Settings",
        "lang_lbl": "Interface Language:",
        "theme_lbl": "Color Theme:",
        "theme_light": "Light ☀️",
        "theme_dark": "Dark 🌙",
        "sound_chk": "Sound Effects (Beep)"
    },
    "ru": {
        "title": "Мегамаркет Все-в-Одном 🛒",
        "search_label": "🔍 Поиск:",
        "balance_label": "Баланс:",
        "topup_btn": "+ Пополнить",
        "history_btn": "📜 История",
        "wheel_btn": "🎡 Колесо Фортуны",
        "cart_btn": "🛒 Корзина",
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
        "cart_empty": "Корзина пуста 😔",
        "subtotal_lbl": "Сумма:",
        "discount_lbl": "Скидка:",
        "total_lbl": "Итого к оплате:",
        "checkout_btn": "Оформить",
        "clear_cart_btn": "Очистить корзину",
        "history_title": "История заказов",
        "no_orders": "Заказов еще не было 🤷‍♂️",
        "order_str": "Заказ",
        "items_count_str": "Товаров",
        "fortune_title": "🎡 Колесо Фортуны",
        "spin_btn": "Крутить 🎡",
        "congrats": "Поздравляем!",
        "win_discount": "Вы выиграли скидку",
        "try_again": "Попробуйте еще раз! 🍀",
        "insufficient_balance": "Недостаточно средств на балансе! Пожалуйста, пополните его.",
        "success_purchase": "Спасибо за покупку! Чек сохранен 📄",
        "settings_btn": "⚙️ Настройки",
        "settings_title": "Настройки программы",
        "lang_lbl": "Язык интерфейса:",
        "theme_lbl": "Тема оформления:",
        "theme_light": "Светлая ☀️",
        "theme_dark": "Темная 🌙",
        "sound_chk": "Звуковые эффекты (Beep)"
    }
}

market_db.init_db()

# Головне вікно
main_app = tk.Tk()
main_app.geometry("700x820")

# Завантажуємо зображення
loaded_images = {}
def load_cached_images():
    for cat in CATEGORY_URLS.keys():
        path = os.path.join(CACHE_DIR, f"{cat}.png")
        if os.path.exists(path):
            try:
                detail_img = Image.open(path).resize((80, 80), Image.Resampling.LANCZOS)
                btn_img = Image.open(path).resize((40, 40), Image.Resampling.LANCZOS)
                loaded_images[cat] = {
                    "detail": ImageTk.PhotoImage(detail_img),
                    "btn": ImageTk.PhotoImage(btn_img)
                }
            except Exception:
                loaded_images[cat] = {"detail": None, "btn": None}
        else:
            loaded_images[cat] = {"detail": None, "btn": None}

load_cached_images()
main_app.after(1500, load_cached_images)

def tr(key):
    return LANGS[active_lang].get(key, key)

# Оновлення кольорів інтерфейсу під тему
def apply_theme_colors():
    theme = THEMES[current_theme]
    main_app.configure(bg=theme["bg"])
    main_frame.configure(bg=theme["bg"])
    header_frame.configure(bg=theme["header_bg"], bd=1, relief="groove")
    profile_lbl.configure(bg=theme["header_bg"], fg=theme["text"])
    balance_lbl.configure(bg=theme["header_bg"])
    
    controls_frame.configure(bg=theme["bg"])
    search_frame.configure(bg=theme["bg"])
    search_lbl.configure(bg=theme["bg"], fg=theme["text"])
    cat_frame.configure(bg=theme["bg"])
    
    canvas_container.configure(bg=theme["bg"])
    grid_frame.configure(bg=theme["bg"])
    
    # Кнопки товарів
    for name, card in card_widgets.items():
        card.configure(bg=theme["card_bg"], bd=1, relief="groove")
        # Шукаємо дочірні віджети картки та перефарбовуємо їх
        for child in card.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=theme["card_bg"], fg=theme["text"])
            elif isinstance(child, tk.Frame):
                child.configure(bg=theme["card_bg"])
                for f_child in child.winfo_children():
                    if isinstance(f_child, tk.Button) and f_child.cget("text") in ["🤍", "❤️"]:
                        f_child.configure(bg=theme["card_bg"], activebackground=theme["card_bg"])

# Оновлення текстів
def translate_ui():
    main_app.title(tr("title"))
    search_lbl.configure(text=tr("search_label"))
    history_btn.configure(text=tr("history_btn"))
    wheel_btn.configure(text=tr("wheel_btn"))
    topup_btn.configure(text=tr("topup_btn"))
    settings_btn.configure(text=tr("settings_btn"))
    if logged_in_user:
        profile_lbl.configure(text=f"👤 {logged_in_user}")
        balance_lbl.configure(text=f"{tr('balance_label')} {market_db.get_balance(logged_in_user)} грн")
    
    cat_all_btn.configure(text=tr("all_cat"))
    cat_tech_btn.configure(text=tr("tech_cat"))
    cat_fruits_btn.configure(text=tr("fruits_cat"))
    cat_home_btn.configure(text=tr("home_cat"))
    cat_sport_btn.configure(text=tr("sport_cat"))
    cat_clothing_btn.configure(text=tr("clothing_cat"))
    
    sort_box.entryconfig(0, label=tr("sort_cheap"))
    sort_box.entryconfig(1, label=tr("sort_expensive"))
    
    update_cart_button_text()
    filter_fruits()

def update_cart_button_text():
    total_items = sum(item['qty'] for item in cart)
    cart_btn.configure(text=f"🛒 {tr('cart_btn')} ({total_items} шт.)")

# Вікно налаштувань
def open_settings_window():
    play_sound("click")
    settings_win = tk.Toplevel(main_app)
    settings_win.title(tr("settings_title"))
    settings_win.geometry("340x300")
    settings_win.configure(bg="#ffffff")
    settings_win.grab_set()
    settings_win.transient(main_app)
    
    tk.Label(settings_win, text=tr("settings_title"), font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=15)
    
    # Вибір мови
    tk.Label(settings_win, text=tr("lang_lbl"), bg="#ffffff", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=25, pady=2)
    lang_frame_set = tk.Frame(settings_win, bg="#ffffff")
    lang_frame_set.pack(fill="x", padx=25, pady=2)
    
    def set_lang(lang_code):
        global active_lang
        active_lang = lang_code
        play_sound("click")
        translate_ui()
        # Оновлення модального вікна налаштувань
        settings_win.title(tr("settings_title"))
        settings_title_lbl.configure(text=tr("settings_title"))
        lang_set_lbl.configure(text=tr("lang_lbl"))
        theme_set_lbl.configure(text=tr("theme_lbl"))
        sound_chk_btn.configure(text=tr("sound_chk"))
        theme_light_btn.configure(text=tr("theme_light"))
        theme_dark_btn.configure(text=tr("theme_dark"))
        
    tk.Button(lang_frame_set, text="Українська 🇺🇦", font=("Segoe UI", 9), relief="groove", command=lambda: set_lang("ua")).pack(side="left", padx=5)
    tk.Button(lang_frame_set, text="English 🇬🇧", font=("Segoe UI", 9), relief="groove", command=lambda: set_lang("en")).pack(side="left", padx=5)
    tk.Button(lang_frame_set, text="Русский 🇷🇺", font=("Segoe UI", 9), relief="groove", command=lambda: set_lang("ru")).pack(side="left", padx=5)
    
    # Вибір теми
    tk.Label(settings_win, text=tr("theme_lbl"), bg="#ffffff", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=25, pady=10)
    theme_frame_set = tk.Frame(settings_win, bg="#ffffff")
    theme_frame_set.pack(fill="x", padx=25, pady=2)
    
    def set_theme(theme_name):
        global current_theme
        current_theme = theme_name
        play_sound("click")
        apply_theme_colors()
        
    theme_light_btn = tk.Button(theme_frame_set, text=tr("theme_light"), font=("Segoe UI", 9), relief="groove", command=lambda: set_theme("light"))
    theme_light_btn.pack(side="left", padx=5)
    theme_dark_btn = tk.Button(theme_frame_set, text=tr("theme_dark"), font=("Segoe UI", 9), relief="groove", command=lambda: set_theme("dark"))
    theme_dark_btn.pack(side="left", padx=5)
    
    # Звукові ефекти
    sound_var = tk.BooleanVar(value=sound_enabled)
    def toggle_sound():
        global sound_enabled
        sound_enabled = sound_var.get()
        play_sound("click")
        
    sound_chk_btn = tk.Checkbutton(settings_win, text=tr("sound_chk"), variable=sound_var, command=toggle_sound, bg="#ffffff", font=("Segoe UI", 9))
    sound_chk_btn.pack(anchor="w", padx=25, pady=15)
    
    # Збереження посилань для динамічного оновлення при зміні мови всередині налаштувань
    settings_title_lbl = settings_win.winfo_children()[0]
    lang_set_lbl = settings_win.winfo_children()[1]
    theme_set_lbl = settings_win.winfo_children()[3]

def show_auth_window():
    auth_win = tk.Toplevel(main_app)
    auth_win.title(tr("auth_title"))
    auth_win.geometry("320x250")
    auth_win.configure(bg="#ffffff")
    auth_win.grab_set()
    auth_win.transient(main_app)
    
    tk.Label(auth_win, text=tr("auth_title"), font=("Segoe UI", 14, "bold"), bg="#ffffff").pack(pady=10)
    frame = tk.Frame(auth_win, bg="#ffffff")
    frame.pack(pady=5)
    
    tk.Label(frame, text=tr("username_lbl"), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    user_entry = tk.Entry(frame, width=20, font=("Segoe UI", 10))
    user_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame, text=tr("password_lbl"), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    pass_entry = tk.Entry(frame, show="*", width=20, font=("Segoe UI", 10))
    pass_entry.grid(row=1, column=1, padx=5, pady=5)
    
    def try_login():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()
        if not username or not password:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі поля!")
            return
            
        if market_db.login_user(username, password):
            global logged_in_user
            logged_in_user = username
            play_sound("success")
            auth_win.destroy()
            show_main_elements()
        else:
            play_sound("error")
            messagebox.showerror("Помилка", "Невірний логін або пароль!")

    def try_register():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()
        if not username or not password:
            play_sound("error")
            messagebox.showwarning("Помилка", "Заповніть усі поля!")
            return
            
        if market_db.register_user(username, password):
            play_sound("success")
            messagebox.showinfo("Успіх", "Користувач успішно зареєстрований! Тепер ви можете увійти.")
        else:
            play_sound("error")
            messagebox.showerror("Помилка", "Такий логін вже існує!")

    btn_frame = tk.Frame(auth_win, bg="#ffffff")
    btn_frame.pack(pady=15)
    tk.Button(btn_frame, text=tr("login_btn"), bg="#4a90e2", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, command=try_login).pack(side="left", padx=5)
    tk.Button(btn_frame, text=tr("register_btn"), bg="#2ecc71", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, command=try_register).pack(side="left", padx=5)
    
    def disable_close():
        pass
    auth_win.protocol("WM_DELETE_WINDOW", disable_close)

def topup_balance():
    if logged_in_user:
        play_sound("success")
        market_db.add_balance(logged_in_user, 500)
        balance_lbl.configure(text=f"{tr('balance_label')} {market_db.get_balance(logged_in_user)} грн")
        messagebox.showinfo("Баланс", "Баланс поповнено на 500 грн!")

def open_fortune_wheel():
    wheel_win = tk.Toplevel(main_app)
    wheel_win.title(tr("fortune_title"))
    wheel_win.geometry("360x420")
    wheel_win.configure(bg="#ffffff")
    wheel_win.grab_set()
    
    canvas = tk.Canvas(wheel_win, width=300, height=300, bg="#ffffff", bd=0, highlightthickness=0)
    canvas.pack(pady=10)
    
    sectors = [
        ("Спробуй ще 🍀", "white", 0.0),
        ("Знижка 5% 🎁", "#ff8a80", 0.05),
        ("Спробуй ще 🍀", "white", 0.0),
        ("Знижка 10% 🎁", "#ff5252", 0.10),
        ("Спробуй ще 🍀", "white", 0.0),
        ("Знижка 15% 🎁", "#ff1744", 0.15)
    ]
    
    def draw_wheel(rotation_angle):
        canvas.delete("all")
        for i, (text, color, val) in enumerate(sectors):
            start = rotation_angle + i * 60
            canvas.create_arc(10, 10, 290, 290, start=start, extent=60, fill=color, outline="#2c3e50")
            rad = math.radians(start + 30)
            tx = 150 + 80 * math.cos(rad)
            ty = 150 - 80 * math.sin(rad)
            canvas.create_text(tx, ty, text=text.split()[0], font=("Segoe UI", 9, "bold"), fill="#2c3e50")
        canvas.create_polygon(150, 5, 140, 30, 160, 30, fill="#2c3e50")
        
    draw_wheel(0)
    
    def spin():
        play_sound("click")
        spin_btn.configure(state="disabled")
        rotations = random.randint(18, 25)
        
        def animate(step, cur_angle):
            if step > 0:
                cur_angle = (cur_angle + step * 8) % 360
                draw_wheel(cur_angle)
                play_sound("spin")
                wheel_win.after(50, lambda: animate(step - 1, cur_angle))
            else:
                final_angle = (90 - cur_angle) % 360
                sector_idx = int(final_angle // 60) % len(sectors)
                name, color, discount = sectors[sector_idx]
                
                if discount > 0:
                    global session_discount
                    session_discount = discount
                    play_sound("success")
                    messagebox.showinfo(tr("congrats"), f"{tr('win_discount')}: {int(discount*100)}%!")
                else:
                    play_sound("error")
                    messagebox.showinfo("Результат", tr("try_again"))
                wheel_win.destroy()
                
        animate(rotations, 0)
        
    spin_btn = tk.Button(wheel_win, text=tr("spin_btn"), font=("Segoe UI", 11, "bold"), bg="#4a90e2", fg="white", relief="flat", command=spin)
    spin_btn.pack(pady=10)

def open_history():
    history_win = tk.Toplevel(main_app)
    history_win.title(tr("history_title"))
    history_win.geometry("380x420")
    history_win.configure(bg="#ffffff")
    
    tk.Label(history_win, text=tr("history_title"), font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#212529").pack(pady=15)
    
    orders = market_db.get_orders(logged_in_user)
    if not orders:
        tk.Label(history_win, text=tr("no_orders"), font=("Segoe UI", 10), bg="#ffffff", fg="#777").pack(pady=50)
        return
        
    for index, order in enumerate(orders):
        order_row = tk.Frame(history_win, bg="#f8f9fa", pady=8, bd=1, relief="ridge")
        order_row.pack(fill="x", padx=15, pady=5)
        tk.Label(order_row, text=f"{tr('order_str')} #{len(orders)-index} [{order['date']}]", font=("Segoe UI", 9, "bold"), bg="#f8f9fa").pack(anchor="w", padx=10)
        tk.Label(order_row, text=f"{tr('items_count_str')}: {order['items_count']} шт. | Сума: {order['total']} грн", font=("Segoe UI", 9), bg="#f8f9fa", fg="#555").pack(anchor="w", padx=10)

def submit_review(fruit_name, rating_var, text_entry, refresh_callback):
    text = text_entry.get().strip()
    if not text:
        play_sound("error")
        messagebox.showwarning("Помилка", "Введіть текст відгуку!")
        return
    try: rating = int(rating_var.get())
    except: rating = 5
        
    market_db.add_review(fruit_name, logged_in_user, rating, text)
    play_sound("success")
    text_entry.delete(0, "end")
    refresh_callback()

def open_details(name):
    data = fruits_data[name]
    dialog = tk.Toplevel(main_app)
    dialog.title(f"{tr('details_title')}: {name}")
    dialog.geometry("450x580")
    dialog.configure(bg="#ffffff")
    dialog.grab_set()
    dialog.transient(main_app)
    
    cat_img = loaded_images.get(data["category"], {}).get("detail")
    if cat_img:
        img_label = tk.Label(dialog, image=cat_img, bg="#ffffff")
        img_label.pack(pady=10)
    
    tk.Label(dialog, text=name, font=("Segoe UI", 15, "bold"), bg="#ffffff", fg="#212529").pack()
    tk.Label(dialog, text=data["desc"], font=("Segoe UI", 10, "italic"), bg="#ffffff", fg="#6c757d").pack(pady=3)
    tk.Label(dialog, text=f"Ціна: {data['price']} грн/шт", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2e7d32").pack(pady=3)
    
    tk.Label(dialog, text=tr("color_lbl"), font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(pady=3)
    color_frame = tk.Frame(dialog, bg="#ffffff")
    color_frame.pack(pady=3)
    
    selected_color = tk.StringVar(value=data["colors"][0][0])
    color_buttons = {}
    
    def select_color(c_name):
        selected_color.set(c_name)
        for name_key, btn_widget in color_buttons.items():
            if name_key == c_name:
                btn_widget.configure(relief="solid", bd=2, highlightthickness=1, highlightbackground="#4a90e2")
            else:
                btn_widget.configure(relief="flat", bd=1, highlightthickness=0)

    for c_name, c_hex in data["colors"]:
        btn_c = tk.Button(
            color_frame, bg=c_hex, activebackground=c_hex, width=4, height=1, relief="flat", cursor="hand2",
            command=lambda name_key=c_name: select_color(name_key)
        )
        btn_c.pack(side="left", padx=5)
        color_buttons[c_name] = btn_c
        
    select_color(data["colors"][0][0])
    
    qty_frame = tk.Frame(dialog, bg="#ffffff")
    qty_frame.pack(pady=8)
    tk.Label(qty_frame, text=tr("qty_lbl"), font=("Segoe UI", 10), bg="#ffffff").pack(side="left", padx=5)
    qty_spin = tk.Spinbox(qty_frame, from_=1, to=50, width=5, font=("Segoe UI", 10), justify="center")
    qty_spin.pack(side="left", padx=5)
    
    tk.Button(
        dialog, text=tr("add_to_cart_btn"), font=("Segoe UI", 11, "bold"), bg="#2ecc71", fg="white", relief="flat", padx=15, pady=4,
        command=lambda: add_to_cart(name, data['price'], qty_spin.get(), selected_color.get(), dialog), cursor="hand2"
    ).pack(pady=8)
    
    tk.Label(dialog, text=tr("reviews_lbl"), font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=5)
    reviews_container = tk.Frame(dialog, bg="#ffffff")
    reviews_container.pack(fill="both", expand=True, padx=15)
    
    def refresh_reviews():
        for w in reviews_container.winfo_children():
            w.destroy()
        revs = market_db.get_reviews(name)
        if revs:
            avg = sum(r['rating'] for r in revs) / len(revs)
            stars = "★" * int(round(avg)) + "☆" * (5 - int(round(avg)))
            tk.Label(reviews_container, text=f"Рейтинг: {stars} ({avg:.1f}/5)", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#f1c40f").pack(anchor="w")
            for r in revs[-3:]:
                tk.Label(reviews_container, text=f"• {r['username']} ({r['rating']}★): {r['text']}", font=("Segoe UI", 9), bg="#ffffff", fg="#555", anchor="w", justify="left").pack(fill="x")
        else:
            tk.Label(reviews_container, text="Відгуків немає.", font=("Segoe UI", 9, "italic"), bg="#ffffff", fg="#888").pack(anchor="w")

    refresh_reviews()
    
    add_rev_frame = tk.Frame(dialog, bg="#ffffff")
    add_rev_frame.pack(fill="x", padx=15, pady=10)
    tk.Label(add_rev_frame, text=tr("add_review_lbl"), font=("Segoe UI", 9, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, sticky="w")
    
    rating_var = tk.StringVar(value="5")
    rating_spin = tk.Spinbox(add_rev_frame, from_=1, to=5, width=3, font=("Segoe UI", 9), justify="center", textvariable=rating_var)
    rating_spin.grid(row=1, column=0, padx=5, pady=2)
    
    rev_entry = tk.Entry(add_rev_frame, width=28, font=("Segoe UI", 9), bd=1, relief="solid")
    rev_entry.grid(row=1, column=1, padx=5, pady=2)
    tk.Button(add_rev_frame, text=tr("submit_review_btn"), font=("Segoe UI", 8, "bold"), bg="#34495e", fg="white", relief="flat", command=lambda: submit_review(name, rating_var, rev_entry, refresh_reviews)).grid(row=1, column=2, padx=5, pady=2)

def add_to_cart(name, price, qty, color, dialog):
    try:
        qty = int(qty)
        if qty <= 0: raise ValueError
    except ValueError:
        play_sound("error")
        messagebox.showwarning("Помилка", "Будь ласка, введіть коректну кількість!")
        return

    for item in cart:
        if item["name"] == name and item["color"] == color:
            item["qty"] += qty
            break
    else:
        cart.append({"name": name, "price": price, "qty": qty, "color": color})
        
    play_sound("success")
    messagebox.showinfo("Успіх", f"Додано {qty} шт. до кошика!")
    update_cart_button_text()
    dialog.destroy()

def view_cart():
    cart_window = tk.Toplevel(main_app)
    cart_window.title(tr("cart_title"))
    cart_window.geometry("500x550")
    cart_window.configure(bg="#ffffff")
    cart_window.grab_set()
    
    tk.Label(cart_window, text=f"🛒 {tr('cart_title')}", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#212529").pack(pady=10)
    list_frame = tk.Frame(cart_window, bg="#ffffff")
    list_frame.pack(fill="both", expand=True, padx=15, pady=5)
    
    def refresh_cart_view():
        for widget in list_frame.winfo_children():
            widget.destroy()
            
        if not cart:
            tk.Label(list_frame, text=tr("cart_empty"), font=("Segoe UI", 11), bg="#ffffff", fg="#888").pack(pady=50)
            price_label.config(text=f"{tr('total_lbl')} 0 грн")
            return

        total_price = 0
        for index, item in enumerate(cart):
            item_total = item['price'] * item['qty']
            total_price += item_total
            item_row = tk.Frame(list_frame, bg="#f8f9fa", pady=5)
            item_row.pack(fill="x", pady=2)
            tk.Label(item_row, text=f"{item['name']} ({item['color']}) x{item['qty']}", font=("Segoe UI", 9, "bold"), bg="#f8f9fa").pack(side="left", padx=10)
            tk.Label(item_row, text=f"{item_total} грн", font=("Segoe UI", 10), bg="#f8f9fa", fg="#555").pack(side="left", padx=10)
            del_btn = tk.Button(item_row, text="❌", font=("Segoe UI", 8), bg="#ff4d4d", fg="white", relief="flat", command=lambda idx=index: remove_item(idx), cursor="hand2")
            del_btn.pack(side="right", padx=10)

        discounted_price = total_price * (1 - session_discount)
        if session_discount > 0:
            price_label.config(
                text=f"{tr('subtotal_lbl')} {total_price} грн\n{tr('discount_lbl')} ({int(session_discount*100)}%): -{int(total_price * session_discount)} грн\n{tr('total_lbl')} {int(discounted_price)} грн"
            )
        else:
            price_label.config(text=f"{tr('total_lbl')} {total_price} грн")

    def remove_item(index):
        removed_item = cart.pop(index)
        refresh_cart_view()
        update_cart_button_text()
        play_sound("click")
        messagebox.showinfo("Кошик", f"{removed_item['name']} видалено з кошика")

    def clear_cart():
        if cart:
            cart.clear()
            refresh_cart_view()
            update_cart_button_text()
            play_sound("click")
            messagebox.showinfo("Кошик", "Кошик повністю очищено")

    def checkout():
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
            messagebox.showerror("Помилка", tr("insufficient_balance"))
            return
            
        checkout_dialog = tk.Toplevel(cart_window)
        checkout_dialog.title("Деталі Доставки")
        checkout_dialog.geometry("380x380")
        checkout_dialog.configure(bg="#ffffff")
        checkout_dialog.grab_set()
        
        tk.Label(checkout_dialog, text="Дані замовлення", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=10)
        form_frame = tk.Frame(checkout_dialog, bg="#ffffff")
        form_frame.pack(padx=15, pady=5)
        
        tk.Label(form_frame, text="Телефон:", bg="#ffffff").grid(row=0, column=0, sticky="e", pady=3)
        phone_entry = tk.Entry(form_frame, width=22)
        phone_entry.grid(row=0, column=1, pady=3, padx=5)
        phone_entry.insert(0, "+380")
        
        tk.Label(form_frame, text="Email:", bg="#ffffff").grid(row=1, column=0, sticky="e", pady=3)
        email_entry = tk.Entry(form_frame, width=22)
        email_entry.grid(row=1, column=1, pady=3, padx=5)
        
        tk.Label(form_frame, text="Адреса:", bg="#ffffff").grid(row=2, column=0, sticky="e", pady=3)
        address_entry = tk.Entry(form_frame, width=22)
        address_entry.grid(row=2, column=1, pady=3, padx=5)
        
        tk.Label(form_frame, text="Доставка:", bg="#ffffff").grid(row=3, column=0, sticky="e", pady=3)
        deliv_var = tk.StringVar(value="Кур'єр")
        deliv_combo = ttk.Combobox(form_frame, textvariable=deliv_var, values=["Кур'єр 🚚", "Нова Пошта 📦", "Самовивіз 🏪"], state="readonly", width=19)
        deliv_combo.grid(row=3, column=1, pady=3, padx=5)
        
        tk.Label(form_frame, text="Оплата:", bg="#ffffff").grid(row=4, column=0, sticky="e", pady=3)
        pay_var = tk.StringVar(value="Особистий баланс")
        pay_combo = ttk.Combobox(form_frame, textvariable=pay_var, values=["Особистий баланс 💳", "Карткою при отриманні 💳", "Готівка 💵"], state="readonly", width=19)
        pay_combo.grid(row=4, column=1, pady=3, padx=5)
        
        def finish_order():
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            address = address_entry.get().strip()
            
            if len(phone) < 9 or not email or not address:
                play_sound("error")
                messagebox.showwarning("Помилка", "Будь ласка, заповніть усі поля доставки!")
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
            <b>Спосіб доставки:</b> {deliv_var.get()}<br>
            <b>Метод оплати:</b> {pay_var.get()}<br>
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
                    <td>{item['name']} ({item['color']})<br><small>{item['qty']} шт. х {item['price']} грн</small></td>
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
            messagebox.showinfo("Успіх", f"{tr('success_purchase')}\nЧек збережено: {receipt_filename}")
            cart.clear()
            session_discount = 0.0
            update_cart_button_text()
            balance_lbl.configure(text=f"{tr('balance_label')} {market_db.get_balance(logged_in_user)} грн")
            checkout_dialog.destroy()
            cart_window.destroy()

        tk.Button(checkout_dialog, text="Завершити замовлення 🚚", font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", relief="flat", padx=15, pady=5, command=finish_order).pack(pady=15)

    price_label = tk.Label(cart_window, text="Разом до сплати: 0 грн", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2e7d32")
    price_label.pack(pady=15)
    
    actions_frame = tk.Frame(cart_window, bg="#ffffff")
    actions_frame.pack(pady=10)
    tk.Button(actions_frame, text=tr("clear_cart_btn"), font=("Segoe UI", 10), bg="#95a5a6", fg="white", relief="flat", command=clear_cart).pack(side="left", padx=5)
    tk.Button(actions_frame, text=tr("checkout_btn"), font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", relief="flat", padx=10, command=checkout).pack(side="left", padx=5)
    
    refresh_cart_view()

def toggle_fav(fruit_name, heart_btn):
    if not logged_in_user: return
    is_fav = market_db.toggle_favorite(logged_in_user, fruit_name)
    play_sound("click")
    if is_fav: heart_btn.configure(text="❤️", fg="red")
    else: heart_btn.configure(text="🤍", fg="#888")
    filter_fruits()

active_category = "all"
def set_category(cat_name):
    global active_category
    active_category = cat_name
    filter_fruits()

active_sort = "cheap"
def set_sort(sort_mode):
    global active_sort
    active_sort = sort_mode
    filter_fruits()

def filter_fruits(event=None):
    search_query = search_entry.get().strip().lower()
    for widget in grid_frame.winfo_children():
        widget.grid_forget()
        
    favorites = market_db.get_favorites(logged_in_user) if logged_in_user else []
    
    filtered = []
    for f_name, data in fruits_data.items():
        if search_query and search_query not in f_name.lower(): continue
        if active_category != "all" and data["category"] != active_category: continue
        filtered.append((f_name, data))
        
    def sort_key(item):
        name, data = item
        is_fav_val = 0 if name in favorites else 1
        price_val = data["price"] if active_sort == "cheap" else -data["price"]
        return (is_fav_val, price_val)
        
    filtered.sort(key=sort_key)
    
    current_col = 0
    current_row = 0
    for f_name, data in filtered[:30]:
        if f_name in card_widgets:
            card_widgets[f_name].grid(row=current_row, column=current_col, padx=10, pady=10)
            heart_btn = heart_buttons[f_name]
            if f_name in favorites: heart_btn.configure(text="❤️", fg="red")
            else: heart_btn.configure(text="🤍", fg="#888")
            current_col += 1
            if current_col > 2:
                current_col = 0
                current_row += 1

def show_main_elements():
    apply_theme_colors()
    translate_ui()
    main_frame.pack(fill="both", expand=True)

# Створення віджетів
main_frame = tk.Frame(main_app)

header_frame = tk.Frame(main_frame)
header_frame.pack(fill="x", ipady=5)

profile_lbl = tk.Label(header_frame, text="👤 Користувач", font=("Segoe UI", 10, "bold"))
profile_lbl.pack(side="left", padx=15)

balance_lbl = tk.Label(header_frame, text="Баланс: 0 грн", font=("Segoe UI", 10), fg="#2e7d32")
balance_lbl.pack(side="left", padx=10)

topup_btn = tk.Button(header_frame, text="+ Поповнити", font=("Segoe UI", 9), bg="#2ecc71", fg="white", relief="flat", command=topup_balance)
topup_btn.pack(side="left", padx=5)

# Кнопка Налаштувань замість прапорців мов у хедері
settings_btn = tk.Button(header_frame, text="⚙️ Налаштування", font=("Segoe UI", 9), bg="#34495e", fg="white", relief="flat", command=open_settings_window)
settings_btn.pack(side="right", padx=15)

def logout():
    global logged_in_user, cart, session_discount
    logged_in_user = None
    cart = []
    session_discount = 0.0
    main_frame.pack_forget()
    show_auth_window()

logout_btn = tk.Button(header_frame, text="🚪", font=("Segoe UI", 9), bg="#ff4d4d", fg="white", relief="flat", command=logout)
logout_btn.pack(side="right", padx=5)

controls_frame = tk.Frame(main_frame)
controls_frame.pack(fill="x", padx=15, pady=10)

history_btn = tk.Button(controls_frame, text="📜 Історія", font=("Segoe UI", 9), bg="#95a5a6", fg="white", relief="flat", command=open_history)
history_btn.pack(side="left", padx=5)

wheel_btn = tk.Button(controls_frame, text="🎡 Колесо Фортуни", font=("Segoe UI", 9, "bold"), bg="#f1c40f", fg="#2c3e50", relief="flat", command=open_fortune_wheel)
wheel_btn.pack(side="left", padx=5)

search_frame = tk.Frame(main_frame)
search_frame.pack(pady=5)

search_lbl = tk.Label(search_frame, text="🔍 Пошук:", font=("Segoe UI", 10, "bold"))
search_lbl.pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, width=22, font=("Segoe UI", 10), bd=1, relief="solid")
search_entry.pack(side="left", padx=5)
search_entry.bind("<KeyRelease>", filter_fruits)

cat_frame = tk.Frame(main_frame)
cat_frame.pack(pady=5)

cat_all_btn = tk.Button(cat_frame, text="Усі", font=("Segoe UI", 9), relief="flat", bg="#e0e0e0", command=lambda: set_category("all"))
cat_all_btn.pack(side="left", padx=3)
cat_tech_btn = tk.Button(cat_frame, text="Техніка", font=("Segoe UI", 9), relief="flat", bg="#e0e0e0", command=lambda: set_category("tech"))
cat_tech_btn.pack(side="left", padx=3)
cat_fruits_btn = tk.Button(cat_frame, text="Фрукти", font=("Segoe UI", 9), relief="flat", bg="#e0e0e0", command=lambda: set_category("fruits"))
cat_fruits_btn.pack(side="left", padx=3)
cat_home_btn = tk.Button(cat_frame, text="Для дому", font=("Segoe UI", 9), relief="flat", bg="#e0e0e0", command=lambda: set_category("home"))
cat_home_btn.pack(side="left", padx=3)
cat_sport_btn = tk.Button(cat_frame, text="Спорт", font=("Segoe UI", 9), relief="flat", bg="#e0e0e0", command=lambda: set_category("sport"))
cat_sport_btn.pack(side="left", padx=3)
cat_clothing_btn = tk.Button(cat_frame, text="Одяг", font=("Segoe UI", 9), relief="flat", bg="#e0e0e0", command=lambda: set_category("clothing"))
cat_clothing_btn.pack(side="left", padx=3)

sort_btn = tk.Menubutton(main_frame, text="⇅ Сортування", font=("Segoe UI", 9), relief="flat", bg="#e0e0e0")
sort_btn.pack(pady=5)
sort_box = tk.Menu(sort_btn, tearoff=0)
sort_box.add_command(label="Спочатку дешевші", command=lambda: set_sort("cheap"))
sort_box.add_command(label="Спочатку дорожчі", command=lambda: set_sort("expensive"))
sort_btn.configure(menu=sort_box)

canvas_container = tk.Canvas(main_frame, bd=0, highlightthickness=0)
canvas_container.pack(fill="both", expand=True, padx=10, pady=5)

scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas_container.yview)
scrollbar.pack(side="right", fill="y")
canvas_container.configure(yscrollcommand=scrollbar.set)

grid_frame = tk.Frame(canvas_container)
grid_frame_id = canvas_container.create_window((0, 0), window=grid_frame, anchor="nw")

def on_configure(event):
    canvas_container.configure(scrollregion=canvas_container.bbox("all"))
grid_frame.bind("<Configure>", on_configure)

def on_canvas_configure(event):
    canvas_container.itemconfig(grid_frame_id, width=event.width)
canvas_container.bind("<Configure>", on_canvas_configure)

card_widgets = {}
heart_buttons = {}

for name, data in fruits_data.items():
    card = tk.Frame(grid_frame)
    card_widgets[name] = card
    
    top_row = tk.Frame(card)
    top_row.pack(fill="x")
    heart_b = tk.Button(
        top_row, text="🤍", font=("Segoe UI", 11), bd=0, relief="flat",
        command=lambda f=name: toggle_fav(f, heart_buttons[f])
    )
    heart_b.pack(side="right")
    heart_buttons[name] = heart_b
    
    img_lbl = tk.Label(card, text="📸", font=("Segoe UI", 18))
    img_lbl.pack(pady=3)
    
    def update_photo(n=name, lbl=img_lbl, c=data["category"]):
        photo = loaded_images.get(c, {}).get("btn")
        if photo:
            lbl.configure(image=photo, text="")
            lbl.image = photo
        else:
            main_app.after(500, lambda: update_photo(n, lbl, c))
            
    update_photo()
    
    tk.Label(card, text=name, font=("Segoe UI", 10, "bold")).pack()
    tk.Label(card, text=f"{data['price']} грн/шт", font=("Segoe UI", 9)).pack(pady=2)
    
    btn = tk.Button(card, text="Детальніше", font=("Segoe UI", 9), bg="#4a90e2", fg="white", relief="flat", padx=10, pady=2, command=lambda f=name: open_details(f), cursor="hand2")
    btn.pack(pady=5)

cart_btn = tk.Button(
    main_frame, text="🛒 Переглянути Кошик (0 шт.)", font=("Segoe UI", 12, "bold"), 
    bg="#2c3e50", fg="white", relief="flat", width=30, height=2, command=view_cart, cursor="hand2"
)
cart_btn.pack(pady=20)

main_app.after(100, show_auth_window)
main_app.mainloop()
