import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Глобальний список кошика
cart = []
# Активний промокод
applied_discount = 0.0

# Дані про товари (ціна, опис, назва, файл картинки)
fruits_data = {
    "Яблуко 🍎": {"price": 20, "desc": "Соковите червоне яблуко", "img": "apple.png"},
    "Банан 🍌": {"price": 15, "desc": "Стиглий жовтий банан", "img": "banana.png"},
    "Апельсин 🍊": {"price": 25, "desc": "Свіжий цитрусовий апельсин", "img": "orange.png"},
    "Полуниця 🍓": {"price": 50, "desc": "Солодка лісова полуниця", "img": "strawberry.png"},
    "Виноград 🍇": {"price": 40, "desc": "Гроно синього винограду", "img": "grapes.png"},
    "Кавун 🍉": {"price": 100, "desc": "Великий стиглий кавун", "img": "watermelon.png"}
}

root = tk.Tk()
root.title("Фруктовий Супермаркет 🛒")
root.geometry("600x650")
root.configure(bg="#f8f9fa")

# Завантаження та збереження картинок для використання в інтерфейсі
loaded_images = {}
for name, data in fruits_data.items():
    img_path = os.path.join(os.path.dirname(__file__), data["img"])
    if os.path.exists(img_path):
        # Велика картинка для вікна деталей (80x80)
        detail_img = Image.open(img_path).resize((80, 80), Image.Resampling.LANCZOS)
        # Маленька картинка для головного екрану (40x40)
        btn_img = Image.open(img_path).resize((40, 40), Image.Resampling.LANCZOS)
        
        loaded_images[name] = {
            "detail": ImageTk.PhotoImage(detail_img),
            "btn": ImageTk.PhotoImage(btn_img)
        }
    else:
        loaded_images[name] = {"detail": None, "btn": None}

def update_cart_button_text():
    total_items = sum(item['qty'] for item in cart)
    cart_btn.configure(text=f"🛒 Кошик ({total_items} шт.)")

def add_to_cart(name, price, qty, dialog):
    try:
        qty = int(qty)
        if qty <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Помилка", "Будь ласка, введіть коректну кількість!")
        return

    # Перевіряємо, чи є вже такий товар в кошику
    for item in cart:
        if item["name"] == name:
            item["qty"] += qty
            break
    else:
        cart.append({"name": name, "price": price, "qty": qty})
        
    messagebox.showinfo("Успіх", f"Додано {qty} шт. {name} до кошика!")
    update_cart_button_text()
    dialog.destroy()

def open_details(name):
    data = fruits_data[name]
    dialog = tk.Toplevel(root)
    dialog.title(f"Деталі: {name}")
    dialog.geometry("350x380")
    dialog.configure(bg="#ffffff")
    dialog.grab_set()
    dialog.transient(root)
    
    # Фото фрукта
    if loaded_images[name]["detail"]:
        img_label = tk.Label(dialog, image=loaded_images[name]["detail"], bg="#ffffff")
        img_label.pack(pady=15)
    
    # Назва та опис
    tk.Label(dialog, text=name, font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#212529").pack()
    tk.Label(dialog, text=data["desc"], font=("Segoe UI", 10, "italic"), bg="#ffffff", fg="#6c757d").pack(pady=5)
    tk.Label(dialog, text=f"Ціна: {data['price']} грн/шт", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2e7d32").pack(pady=5)
    
    # Кількість
    qty_frame = tk.Frame(dialog, bg="#ffffff")
    qty_frame.pack(pady=10)
    tk.Label(qty_frame, text="Кількість:", font=("Segoe UI", 10), bg="#ffffff").pack(side="left", padx=5)
    qty_spin = tk.Spinbox(qty_frame, from_=1, to=50, width=5, font=("Segoe UI", 10), justify="center")
    qty_spin.pack(side="left", padx=5)
    
    # Кнопка додавання
    tk.Button(
        dialog, text="Додати в кошик", 
        font=("Segoe UI", 11, "bold"), bg="#2ecc71", fg="white", relief="flat", padx=15, pady=5,
        command=lambda: add_to_cart(name, data['price'], qty_spin.get(), dialog),
        cursor="hand2"
    ).pack(pady=15)

def view_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("Ваш кошик")
    cart_window.geometry("400x500")
    cart_window.configure(bg="#ffffff")
    cart_window.grab_set()
    
    tk.Label(cart_window, text="🛒 Список товарів", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#212529").pack(pady=10)
    
    # Фрейм для списку товарів з прокруткою
    list_frame = tk.Frame(cart_window, bg="#ffffff")
    list_frame.pack(fill="both", expand=True, padx=15, pady=5)
    
    # Функція для оновлення вмісту кошика у вікні
    def refresh_cart_view():
        # Очищення фрейму
        for widget in list_frame.winfo_children():
            widget.destroy()
            
        if not cart:
            tk.Label(list_frame, text="Кошик порожній 😔", font=("Segoe UI", 11), bg="#ffffff", fg="#888").pack(pady=50)
            price_label.config(text="Разом до сплати: 0 грн")
            return

        total_price = 0
        for index, item in enumerate(cart):
            item_total = item['price'] * item['qty']
            total_price += item_total
            
            # Рядок товару
            item_row = tk.Frame(list_frame, bg="#f8f9fa", pady=5)
            item_row.pack(fill="x", pady=2)
            
            tk.Label(item_row, text=f"{item['name']} x{item['qty']}", font=("Segoe UI", 10, "bold"), bg="#f8f9fa").pack(side="left", padx=10)
            tk.Label(item_row, text=f"{item_total} грн", font=("Segoe UI", 10), bg="#f8f9fa", fg="#555").pack(side="left", padx=10)
            
            # Кнопка видалення товару
            del_btn = tk.Button(
                item_row, text="❌", font=("Segoe UI", 8), bg="#ff4d4d", fg="white", relief="flat",
                command=lambda idx=index: remove_item(idx), cursor="hand2"
            )
            del_btn.pack(side="right", padx=10)

        # Розрахунок знижки
        discounted_price = total_price * (1 - applied_discount)
        if applied_discount > 0:
            price_label.config(
                text=f"Сума: {total_price} грн\nЗнижка ({int(applied_discount*100)}%): -{int(total_price * applied_discount)} грн\nРазом до сплати: {int(discounted_price)} грн"
            )
        else:
            price_label.config(text=f"Разом до сплати: {total_price} грн")

    def remove_item(index):
        removed_item = cart.pop(index)
        refresh_cart_view()
        update_cart_button_text()
        messagebox.showinfo("Кошик", f"{removed_item['name']} видалено з кошика")

    def clear_cart():
        if cart:
            cart.clear()
            refresh_cart_view()
            update_cart_button_text()
            messagebox.showinfo("Кошик", "Кошик повністю очищено")

    def apply_promo():
        global applied_discount
        code = promo_entry.get().strip().upper()
        if code == "FRUIT20":
            applied_discount = 0.20
            messagebox.showinfo("Промокод", "Промокод FRUIT20 успішно активовано! Знижка 20%")
            refresh_cart_view()
        elif code == "":
            messagebox.showwarning("Промокод", "Введіть промокод!")
        else:
            messagebox.showerror("Промокод", "Невірний промокод!")

    def checkout():
        if not cart:
            messagebox.showwarning("Помилка", "Кошик порожній!")
            return
        messagebox.showinfo("Успіх", "Дякуємо за покупку! Ваше замовлення оформлено та відправлено на доставку! 🚚")
        cart.clear()
        update_cart_button_text()
        cart_window.destroy()

    # Поле промокоду
    promo_frame = tk.Frame(cart_window, bg="#ffffff")
    promo_frame.pack(fill="x", padx=15, pady=5)
    tk.Label(promo_frame, text="Промокод:", font=("Segoe UI", 9), bg="#ffffff").pack(side="left", padx=5)
    promo_entry = tk.Entry(promo_frame, width=12, font=("Segoe UI", 9))
    promo_entry.pack(side="left", padx=5)
    tk.Button(promo_frame, text="Застосувати", font=("Segoe UI", 8, "bold"), bg="#34495e", fg="white", relief="flat", command=apply_promo).pack(side="left", padx=5)

    # Лейбл ціни
    price_label = tk.Label(cart_window, text="Разом до сплати: 0 грн", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#2e7d32")
    price_label.pack(pady=10)

    # Кнопки дій
    actions_frame = tk.Frame(cart_window, bg="#ffffff")
    actions_frame.pack(pady=10)
    
    tk.Button(actions_frame, text="Очистити кошик", font=("Segoe UI", 10), bg="#95a5a6", fg="white", relief="flat", command=clear_cart).pack(side="left", padx=5)
    tk.Button(actions_frame, text="Оформити", font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", relief="flat", padx=10, command=checkout).pack(side="left", padx=5)
    
    refresh_cart_view()

# Інтерфейс головного екрану
tk.Label(root, text="🍊 Фруктовий Маркет 🍎", font=("Segoe UI", 20, "bold"), bg="#f8f9fa", fg="#212529").pack(pady=20)
tk.Label(root, text="Оберіть свіжі фрукти з нашого асортименту:", font=("Segoe UI", 11), bg="#f8f9fa", fg="#6c757d").pack(pady=5)

# Фрейм для карток товарів
grid_frame = tk.Frame(root, bg="#f8f9fa")
grid_frame.pack(pady=15)

# Кнопки/Картки товарів
for index, fruit_name in enumerate(fruits_data.keys()):
    row = index // 3
    col = index % 3
    
    card = tk.Frame(grid_frame, bg="#ffffff", bd=1, relief="groove", padx=10, pady=10)
    card.grid(row=row, column=col, padx=12, pady=12)
    
    # Картинка
    if loaded_images[fruit_name]["btn"]:
        img_lbl = tk.Label(card, image=loaded_images[fruit_name]["btn"], bg="#ffffff")
        img_lbl.pack(pady=5)
        
    # Текст та Ціна
    tk.Label(card, text=fruit_name, font=("Segoe UI", 11, "bold"), bg="#ffffff").pack()
    tk.Label(card, text=f"{fruits_data[fruit_name]['price']} грн/шт", font=("Segoe UI", 9), bg="#ffffff", fg="#2e7d32").pack(pady=2)
    
    # Кнопка "Деталі"
    btn = tk.Button(
        card, text="Детальніше", font=("Segoe UI", 9), 
        bg="#4a90e2", fg="white", relief="flat", padx=10, pady=2,
        command=lambda f=fruit_name: open_details(f),
        cursor="hand2"
    )
    btn.pack(pady=5)

# Велика фіксована кнопка Кошика знизу
cart_btn = tk.Button(
    root, text="🛒 Кошик (0 шт.)", font=("Segoe UI", 12, "bold"), 
    bg="#2c3e50", fg="white", relief="flat", width=25, height=2,
    command=view_cart, cursor="hand2"
)
cart_btn.pack(pady=35)

root.mainloop()
