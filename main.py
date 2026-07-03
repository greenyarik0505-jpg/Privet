import tkinter as tk
from tkinter import messagebox

import tkinter as tk
from tkinter import messagebox

# Кольорові палітри для тем
THEMES = {
    "light": {
        "bg": "#f4f4f9",
        "btn_bg": "#ffffff",
        "btn_fg": "#333333",
        "btn_hover": "#e0e0e0",
        "accent": "#4a90e2",
        "text": "#333333",
        "status": "#666666"
    },
    "dark": {
        "bg": "#1e1e2e",
        "btn_bg": "#313244",
        "btn_fg": "#cdd6f4",
        "btn_hover": "#45475a",
        "accent": "#89b4fa",
        "text": "#cdd6f4",
        "status": "#a6adc8"
    }
}

current_theme = "light"

root = tk.Tk()
root.title("Фруктовий Маркет")
root.geometry("500x480")
root.configure(bg=THEMES[current_theme]["bg"])

# Функція перемикання теми
def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    theme = THEMES[current_theme]
    
    # Оновлення кольорів головного вікна
    root.configure(bg=theme["bg"])
    title_label.configure(bg=theme["bg"], fg=theme["text"])
    buttons_frame.configure(bg=theme["bg"])
    status_label.configure(bg=theme["bg"], fg=theme["status"])
    theme_btn.configure(
        text="☀️ Світла тема" if current_theme == "dark" else "🌙 Темна тема",
        bg=theme["btn_bg"],
        fg=theme["btn_fg"],
        activebackground=theme["btn_hover"],
        activeforeground=theme["btn_fg"]
    )
    
    # Оновлення кнопок фруктів
    for btn in fruit_buttons:
        btn.configure(
            bg=theme["btn_bg"],
            fg=theme["btn_fg"],
            activebackground=theme["btn_hover"],
            activeforeground=theme["btn_fg"]
        )

# Кнопка перемикання теми вгорі
theme_btn = tk.Button(
    root, text="🌙 Темна тема", font=("Segoe UI", 9),
    bg=THEMES[current_theme]["btn_bg"], fg=THEMES[current_theme]["btn_fg"],
    relief="flat", activebackground=THEMES[current_theme]["btn_hover"],
    command=toggle_theme, cursor="hand2"
)
theme_btn.pack(anchor="ne", padx=15, pady=10)

# Заголовок
title_label = tk.Label(
    root, text="Оберіть свій фрукт", 
    font=("Segoe UI", 18, "bold"), 
    bg=THEMES[current_theme]["bg"], 
    fg=THEMES[current_theme]["text"]
)
title_label.pack(pady=10)

# Фрейм для кнопок
buttons_frame = tk.Frame(root, bg=THEMES[current_theme]["bg"])
buttons_frame.pack(pady=10)

# Лабел для статуса
status_label = tk.Label(
    root, text="Очікування вибору...", 
    font=("Segoe UI", 12), 
    bg=THEMES[current_theme]["bg"], 
    fg=THEMES[current_theme]["status"]
)
status_label.pack(pady=25)

fruits = [
    ("Яблуко 🍎", "Яблуко"), ("Банан 🍌", "Банан"),
    ("Апельсин 🍊", "Апельсин"), ("Полуниця 🍓", "Полуниця"),
    ("Виноград 🍇", "Виноград"), ("Кавун 🍉", "Кавун")
]

def start_delivery(fruit_name):
    dialog = tk.Toplevel(root)
    dialog.title(f"Замовлення: {fruit_name}")
    dialog.geometry("350x320")
    # Вікно налаштування замовлення адаптується під поточну тему
    theme = THEMES[current_theme]
    dialog.configure(bg=theme["bg"])
    dialog.grab_set()

    tk.Label(dialog, text=f"Налаштування: {fruit_name}", font=("Segoe UI", 12, "bold"), bg=theme["bg"], fg=theme["text"]).pack(pady=15)
    
    # Вибір кольору
    color_var = tk.StringVar(value="Стандартний")
    # Щоб OptionMenu виглядав охайно
    color_menu = tk.OptionMenu(dialog, color_var, "Червоний 🔴", "Зелений 🟢", "Жовтий 🟡")
    color_menu.configure(bg=theme["btn_bg"], fg=theme["btn_fg"], activebackground=theme["btn_hover"], activeforeground=theme["btn_fg"], relief="flat")
    color_menu.pack(pady=5)
    
    qty_spin = tk.Spinbox(dialog, from_=1, to=20, width=10, font=("Segoe UI", 10), bg=theme["btn_bg"], fg=theme["text"])
    qty_spin.pack(pady=5)
    
    name_entry = tk.Entry(dialog, width=30, font=("Segoe UI", 10), bd=1, relief="solid", bg=theme["btn_bg"], fg=theme["text"], insertbackground=theme["text"])
    name_entry.pack(pady=5)
    name_entry.insert(0, "Ваше ім'я")

    def confirm():
        if not name_entry.get() or name_entry.get() == "Ваше ім'я":
            messagebox.showwarning("Помилка", "Введіть ім'я!")
            return
        
        status_label.config(text=f"✅ Замовлено: {fruit_name} для {name_entry.get()}", fg=theme["accent"])
        dialog.destroy()

    tk.Button(
        dialog, text="Підтвердити", command=confirm, bg=theme["accent"], fg="white", 
        font=("Segoe UI", 10, "bold"), relief="flat", padx=20
    ).pack(pady=20)

fruit_buttons = []

# Створення красивих кнопок з підтримкою кольорових емодзі
for index, (label_text, name) in enumerate(fruits):
    btn = tk.Button(
        buttons_frame, text=label_text, 
        # Використовуємо шрифт "Segoe UI Emoji" для відображення кольорових емодзі на Windows
        font=("Segoe UI Emoji", 10),
        width=14, height=2, 
        bg=THEMES[current_theme]["btn_bg"], 
        fg=THEMES[current_theme]["btn_fg"],
        relief="flat",
        activebackground=THEMES[current_theme]["btn_hover"], 
        activeforeground=THEMES[current_theme]["btn_fg"],
        cursor="hand2",
        command=lambda f=name: start_delivery(f)
    )
    btn.grid(row=index // 3, column=index % 3, padx=10, pady=10)
    fruit_buttons.append(btn)

root.mainloop()
