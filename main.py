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
    # Запит даних користувача через діалогове вікно
    user_name = simpledialog.askstring("Оформлення", f"Куди доставити {fruit_name}?\nВведіть ім'я отримувача:")
    
    if user_name:  # Якщо користувач ввів дані та натиснув OK
        status_label.config(text=f"Оформлення для {user_name}...", fg="orange")
        root.after(1500, lambda: status_label.config(text=f"В пути: {fruit_name} для {user_name}! 🚚", fg="purple"))
        root.after(3000, lambda: status_label.config(text=f"Доставлено: {fruit_name} для {user_name}! 🎉", fg="green"))
    else:
        status_label.config(text="Замовлення скасовано.", fg="red")

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
