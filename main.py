import tkinter as tk
from tkinter import messagebox

# Кольори та шрифти
BG_COLOR = "#f4f4f9"
BTN_COLOR = "#ffffff"
BTN_HOVER = "#e0e0e0"
ACCENT_COLOR = "#4a90e2"
TEXT_COLOR = "#333333"

root = tk.Tk()
root.title("Фруктовий Маркет")
root.geometry("500x450")
root.configure(bg=BG_COLOR)

# Заголовок
tk.Label(root, text="Оберіть свій фрукт", font=("Segoe UI", 18, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

# Фрейм для кнопок
buttons_frame = tk.Frame(root, bg=BG_COLOR)
buttons_frame.pack(pady=10)

# Лабел для статуса
status_label = tk.Label(root, text="Очікування вибору...", font=("Segoe UI", 12), bg=BG_COLOR, fg="#666")
status_label.pack(pady=30)

fruits = [
    ("Яблуко 🍎", "Яблуко"), ("Банан 🍌", "Банан"),
    ("Апельсин 🍊", "Апельсин"), ("Полуниця 🍓", "Полуниця"),
    ("Виноград 🍇", "Виноград"), ("Кавун 🍉", "Кавун")
]

def start_delivery(fruit_name):
    dialog = tk.Toplevel(root)
    dialog.title(f"Замовлення: {fruit_name}")
    dialog.geometry("350x320")
    dialog.configure(bg="#ffffff")
    dialog.grab_set()

    tk.Label(dialog, text=f"Налаштування: {fruit_name}", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=15)
    
    # Вибір
    color_var = tk.StringVar(value="Стандартний")
    tk.OptionMenu(dialog, color_var, "Червоний 🔴", "Зелений 🟢", "Жовтий 🟡").pack(pady=5)
    
    qty_spin = tk.Spinbox(dialog, from_=1, to=20, width=10, font=("Segoe UI", 10))
    qty_spin.pack(pady=5)
    
    name_entry = tk.Entry(dialog, width=30, font=("Segoe UI", 10), bd=1, relief="solid")
    name_entry.pack(pady=5)
    name_entry.insert(0, "Ваше ім'я")

    def confirm():
        if not name_entry.get() or name_entry.get() == "Ваше ім'я":
            messagebox.showwarning("Помилка", "Введіть ім'я!")
            return
        
        status_label.config(text=f"✅ Замовлено: {fruit_name} для {name_entry.get()}", fg=ACCENT_COLOR)
        dialog.destroy()

    tk.Button(dialog, text="Підтвердити", command=confirm, bg=ACCENT_COLOR, fg="white", 
              font=("Segoe UI", 10, "bold"), relief="flat", padx=20).pack(pady=20)

# Створення красивих кнопок
for index, (label_text, name) in enumerate(fruits):
    btn = tk.Button(
        buttons_frame, text=label_text, font=("Segoe UI", 10),
        width=14, height=2, bg=BTN_COLOR, relief="flat",
        activebackground=BTN_HOVER, cursor="hand2",
        command=lambda f=name: start_delivery(f)
    )
    btn.grid(row=index // 3, column=index % 3, padx=10, pady=10)

root.mainloop()
