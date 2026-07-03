import tkinter as tk
from tkinter import simpledialog, messagebox

root = tk.Tk()
root.title("Фруктовый Магазин")
root.geometry("450x400")

# Заголовок
title_label = tk.Label(root, text="Выберите фрукт для доставки:", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Фрейм для кнопок
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

# Лабел для статуса доставки
status_label = tk.Label(root, text="Ожидание выбора...", font=("Arial", 12), fg="blue")
status_label.pack(pady=20)

fruits = [
    ("Яблоко 🍎", "Яблоко"), ("Банан 🍌", "Банан"),
    ("Апельсин 🍊", "Апельсин"), ("Клубника 🍓", "Клубника"),
    ("Виноград 🍇", "Виноград"), ("Арбуз 🍉", "Арбуз")
]

def start_delivery(fruit_name):
    # Створення модального вікна для вибору параметрів
    dialog = tk.Toplevel(root)
    dialog.title(f"Замовлення: {fruit_name}")
    dialog.geometry("320x280")
    dialog.grab_set()  # Робимо вікно модальним
    dialog.transient(root)
    
    tk.Label(dialog, text=f"Параметри для {fruit_name}", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Вибір кольору
    tk.Label(dialog, text="Виберіть колір:", font=("Arial", 10)).pack()
    color_var = tk.StringVar(value="Стандартний")
    colors = ["Червоний 🔴", "Зелений 🟢", "Жовтий 🟡", "Оранжевий 🟠"]
    color_menu = tk.OptionMenu(dialog, color_var, *colors)
    color_menu.pack(pady=5)
    
    # Вибір кількості
    tk.Label(dialog, text="Кількість (шт):", font=("Arial", 10)).pack()
    qty_spin = tk.Spinbox(dialog, from_=1, to=20, width=10, justify="center")
    qty_spin.pack(pady=5)
    
    # Введення імені
    tk.Label(dialog, text="Ім'я отримувача:", font=("Arial", 10)).pack()
    name_entry = tk.Entry(dialog, width=25)
    name_entry.pack(pady=5)
    
    def confirm():
        user_name = name_entry.get().strip()
        selected_color = color_var.get()
        quantity = qty_spin.get()
        
        if not user_name:
            messagebox.showwarning("Попередження", "Будь ласка, введіть ім'я отримувача!")
            return
            
        dialog.destroy()
        
        # Симуляція доставки
        status_label.config(text=f"Оформлення: {fruit_name} ({selected_color}, {quantity} шт) для {user_name}...", fg="orange")
        root.after(1500, lambda: status_label.config(
            text=f"В дорозі: {fruit_name} ({selected_color}, {quantity} шт) для {user_name}! 🚚", fg="purple"
        ))
        root.after(3000, lambda: status_label.config(
            text=f"Доставлено: {fruit_name} ({selected_color}, {quantity} шт) для {user_name}! 🎉", fg="green"
        ))
        
    tk.Button(dialog, text="Оформити замовлення", command=confirm, bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5).pack(pady=15)

# Створення кнопок
for index, (label_text, name) in enumerate(fruits):
    row = index // 3
    col = index % 3
    btn = tk.Button(
        buttons_frame, 
        text=label_text, 
        font=("Arial", 11), 
        width=12, 
        height=2, 
        command=lambda f=name: start_delivery(f)
    )
    btn.grid(row=row, column=col, padx=10, pady=10)

root.mainloop()
