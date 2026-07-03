import tkinter as tk
import time

root = tk.Tk()
root.title("Фруктовый Магазин")
root.geometry("450x350")

# Заголовок
title_label = tk.Label(root, text="Выберите фрукт для доставки:", font=("Arial", 14, "bold"))
title_label.pack(pady=10)

# Фрейм для кнопок
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

# Лабел для статуса доставки
status_label = tk.Label(root, text="Ожидание выбора...", font=("Arial", 12), fg="blue")
status_label.pack(pady=20)

# Список фруктов
fruits = [
    ("Яблоко 🍎", "Яблоко"),
    ("Банан 🍌", "Банан"),
    ("Апельсин 🍊", "Апельсин"),
    ("Клубника 🍓", "Клубника"),
    ("Виноград 🍇", "Виноград"),
    ("Арбуз 🍉", "Арбуз")
]

# Функция симуляции доставки
def start_delivery(fruit_name):
    status_label.config(text=f"Оформление доставки: {fruit_name}...", fg="orange")
    # Через 1.5 секунды меняем статус на "в пути"
    root.after(1500, lambda: status_label.config(text=f"В пути: {fruit_name} доставляется! 🚚", fg="purple"))
    # Еще через 1.5 секунды меняем на "доставлено"
    root.after(3000, lambda: status_label.config(text=f"Успешно доставлено: {fruit_name}! 🎉", fg="green"))

# Создание 6 кнопок (сетка 2x3)
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
