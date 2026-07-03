import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Глобальний список кошика
cart = []
# Активний промокод
applied_discount = 0.0

# Дані про товари (ціна, опис, назва, файл картинки, доступні кольори)
fruits_data = {
    "Яблуко 🍎": {
        "price": 20, 
        "desc": "Соковите червоне або зелене яблуко", 
        "img": "apple.png",
        "colors": [("Червоне 🔴", "#e74c3c"), ("Зелене 🟢", "#2ecc71"), ("Жовте 🟡", "#f1c40f")]
    },
    "Банан 🍌": {
        "price": 15, 
        "desc": "Стиглий солодкий банан імпортний", 
        "img": "banana.png",
        "colors": [("Жовтий 🟡", "#f1c40f"), ("Зелений 🟢", "#2ecc71")]
    },
    "Апельсин 🍊": {
        "price": 25, 
        "desc": "Свіжий соковитий цитрусовий апельсин", 
        "img": "orange.png",
        "colors": [("Оранжевий 🟠", "#e67e22"), ("Червоний 🔴", "#e74c3c")]
    },
    "Полуниця 🍓": {
        "price": 50, 
        "desc": "Солодка та ароматна лісова полуниця", 
        "img": "strawberry.png",
        "colors": [("Червона 🔴", "#e74c3c")]
    },
    "Виноград 🍇": {
        "price": 40, 
        "desc": "Гроно свіжого синього або зеленого винограду", 
        "img": "grapes.png",
        "colors": [("Синій 🔵", "#3498db"), ("Зелений 🟢", "#2ecc71"), ("Фіолетовий 🟣", "#9b59b6")]
    },
    "Кавун 🍉": {
        "price": 100, 
        "desc": "Великий, цукровий та дуже стиглий кавун", 
        "img": "watermelon.png",
        "colors": [("Смугастий 🟢", "#27ae60"), ("Темний 🟢", "#1e824c")]
    }
}

root = tk.Tk()
root.title("Фруктовий Супермаркет 🛒")
root.geometry("600x670")
root.configure(bg="#f8f9fa")

# Завантаження та збереження картинок
loaded_images = {}
for name, data in fruits_data.items():
    img_path = os.path.join(os.path.dirname(__file__), data["img"])
    if os.path.exists(img_path):
        detail_img = Image.open(img_path).resize((80, 80), Image.Resampling.LANCZOS)
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

def add_to_cart(name, price, qty, color, dialog):
    try:
        qty = int(qty)
        if qty <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Помилка", "Будь ласка, введіть коректну кількість!")
        return

    # Перевіряємо, чи є такий товар з таким же кольором в кошику
    for item in cart:
        if item["name"] == name and item["color"] == color:
            item["qty"] += qty
            break
    else:
        cart.append({"name": name, "price": price, "qty": qty, "color": color})
        
    messagebox.showinfo("Успіх", f"Додано {qty} шт. {name} ({color}) до кошика!")
    update_cart_button_text()
    dialog.destroy()

def open_details(name):
    data = fruits_data[name]
    dialog = tk.Toplevel(root)
    dialog.title(f"Деталі: {name}")
    dialog.geometry("380x450")
    dialog.configure(bg="#ffffff")
    dialog.grab_set()
    dialog.transient(root)
    
    # Фото фрукта
    if loaded_images[name]["detail"]:
        img_label = tk.Label(dialog, image=loaded_images[name]["detail"], bg="#ffffff")
        img_label.pack(pady=10)
    
    # Назва та опис
    tk.Label(dialog, text=name, font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#212529").pack()
    tk.Label(dialog, text=data["desc"], font=("Segoe UI", 10, "italic"), bg="#ffffff", fg="#6c757d").pack(pady=3)
    tk.Label(dialog, text=f"Ціна: {data['price']} грн/шт", font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#2e7d32").pack(pady=3)
    
    # Вибір кольору/сорту (кнопки)
    tk.Label(dialog, text="Виберіть сорт/колір:", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(pady=5)
    
    color_frame = tk.Frame(dialog, bg="#ffffff")
    color_frame.pack(pady=5)
    
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
            color_frame,
            bg=c_hex,
            activebackground=c_hex,
            width=4,
            height=1,
            relief="flat",
            cursor="hand2",
            command=lambda name_key=c_name: select_color(name_key)
        )
        btn_c.pack(side="left", padx=5)
        color_buttons[c_name] = btn_c
        
    select_color(data["colors"][0][0])  # Активуємо перший колір за замовчуванням
    
    # Вибір кількості
    qty_frame = tk.Frame(dialog, bg="#ffffff")
    qty_frame.pack(pady=10)
    tk.Label(qty_frame, text="Кількість:", font=("Segoe UI", 10), bg="#ffffff").pack(side="left", padx=5)
    qty_spin = tk.Spinbox(qty_frame, from_=1, to=50, width=5, font=("Segoe UI", 10), justify="center")
    qty_spin.pack(side="left", padx=5)
    
    # Кнопка додавання
    tk.Button(
        dialog, text="Додати в кошик", 
        font=("Segoe UI", 11, "bold"), bg="#2ecc71", fg="white", relief="flat", padx=15, pady=5,
        command=lambda: add_to_cart(name, data['price'], qty_spin.get(), selected_color.get(), dialog),
        cursor="hand2"
    ).pack(pady=15)

def view_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("Ваш кошик")
    cart_window.geometry("420x520")
    cart_window.configure(bg="#ffffff")
    cart_window.grab_set()
    
    tk.Label(cart_window, text="🛒 Список товарів", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#212529").pack(pady=10)
    
    list_frame = tk.Frame(cart_window, bg="#ffffff")
    list_frame.pack(fill="both", expand=True, padx=15, pady=5)
    
    def refresh_cart_view():
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
            
            item_row = tk.Frame(list_frame, bg="#f8f9fa", pady=5)
            item_row.pack(fill="x", pady=2)
            
            # Текст описує назву фрукта та його обраний колір/сорт
            tk.Label(item_row, text=f"{item['name']} ({item['color']}) x{item['qty']}", font=("Segoe UI", 9, "bold"), bg="#f8f9fa").pack(side="left", padx=10)
            tk.Label(item_row, text=f"{item_total} грн", font=("Segoe UI", 10), bg="#f8f9fa", fg="#555").pack(side="left", padx=10)
            
            del_btn = tk.Button(
                item_row, text="❌", font=("Segoe UI", 8), bg="#ff4d4d", fg="white", relief="flat",
                command=lambda idx=index: remove_item(idx), cursor="hand2"
            )
            del_btn.pack(side="right", padx=10)

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
            
        # Запит імені отримувача перед підтвердженням
        checkout_dialog = tk.Toplevel(cart_window)
        checkout_dialog.title("Доставка")
        checkout_dialog.geometry("300x180")
        checkout_dialog.configure(bg="#ffffff")
        checkout_dialog.grab_set()
        
        tk.Label(checkout_dialog, text="Введіть ім'я отримувача:", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(pady=10)
        name_entry = tk.Entry(checkout_dialog, width=25, font=("Segoe UI", 10), bd=1, relief="solid")
        name_entry.pack(pady=5)
        name_entry.insert(0, "Ваше ім'я")
        
        def on_entry_click(event):
            if name_entry.get() == "Ваше ім'я":
                name_entry.delete(0, "end")
        def on_focus_out(event):
            if name_entry.get() == "":
                name_entry.insert(0, "Ваше ім'я")
                
        name_entry.bind("<FocusIn>", on_entry_click)
        name_entry.bind("<FocusOut>", on_focus_out)
        
        def finish_order():
            name = name_entry.get().strip()
            if not name or name == "Ваше ім'я":
                messagebox.showwarning("Помилка", "Введіть коректне ім'я!")
                return
            
            messagebox.showinfo("Успіх", f"Дякуємо за покупку, {name}!\nВаше замовлення успішно оформлено та прямує до вас! 🚚")
            cart.clear()
            update_cart_button_text()
            checkout_dialog.destroy()
            cart_window.destroy()
            
        tk.Button(checkout_dialog, text="Підтвердити замовлення", font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", relief="flat", padx=10, command=finish_order).pack(pady=15)

    # Панель промокоду
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

# Фрейм для карток
grid_frame = tk.Frame(root, bg="#f8f9fa")
grid_frame.pack(pady=15)

for index, fruit_name in enumerate(fruits_data.keys()):
    row = index // 3
    col = index % 3
    
    card = tk.Frame(grid_frame, bg="#ffffff", bd=1, relief="groove", padx=10, pady=10)
    card.grid(row=row, column=col, padx=12, pady=12)
    
    if loaded_images[fruit_name]["btn"]:
        img_lbl = tk.Label(card, image=loaded_images[fruit_name]["btn"], bg="#ffffff")
        img_lbl.pack(pady=5)
        
    tk.Label(card, text=fruit_name, font=("Segoe UI", 11, "bold"), bg="#ffffff").pack()
    tk.Label(card, text=f"{fruits_data[fruit_name]['price']} грн/шт", font=("Segoe UI", 9), bg="#ffffff", fg="#2e7d32").pack(pady=2)
    
    btn = tk.Button(
        card, text="Детальніше", font=("Segoe UI", 9), 
        bg="#4a90e2", fg="white", relief="flat", padx=10, pady=2,
        command=lambda f=fruit_name: open_details(f),
        cursor="hand2"
    )
    btn.pack(pady=5)

cart_btn = tk.Button(
    root, text="🛒 Кошик (0 шт.)", font=("Segoe UI", 12, "bold"), 
    bg="#2c3e50", fg="white", relief="flat", width=25, height=2,
    command=view_cart, cursor="hand2"
)
cart_btn.pack(pady=35)

root.mainloop()
