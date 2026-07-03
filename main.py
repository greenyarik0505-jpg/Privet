import tkinter as tk

root = tk.Tk()
root.title("Окно")
root.geometry("400x300")

# Створення лабела (мітки)
label = tk.Label(root, text="Привіт! Це мій текст", font=("Arial", 14))
# Розміщення лабела у вікні
label.pack(pady=50)

root.mainloop()
