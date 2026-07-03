import tkinter as tk
from tkinter import messagebox

# Глобальний список кошика
cart = []

# Дані про товари (ціна, опис, назва)
fruits_data = {
    "Яблуко 🍎": {"price": 20, "desc": "Соковите червоне яблуко"},
    "Банан 🍌": {"price": 15, "desc": "Стиглий жовтий банан"},
    "Апельсин 🍊": {"price": 25, "desc": "Свіжий цитрусовий"},
    "Полуниця 🍓": {"price": 50, "desc": "Солодка лісова полуниця"},
    "Виноград 🍇": {"price": 40, "desc": "Гроно синього винограду"},
    "Кавун 🍉": {"price": 100, "desc": "Великий стиглий кавун"}
}

root = tk.Tk()
root.title("Фруктовий Маркет")
root.geometry("500x550")
root.configure(bg="#f4f4f9")

def view_cart():
    cart_window = tk.Toplevel(root)
    cart_window.title("Ваш кошик")
    cart_window.geometry("300x400")
    
    tk.Label(cart_window, text="Кошик", font=("Arial", 14, "bold")).pack(pady=10)
    
    total_price = 0
    for item in cart:
        tk.Label(cart_window, text=f"{item['name']} - {item['price']} грн").pack()
        total_price += item['price']
    
    tk.Label(cart_window, text=f"\nРазом до сплати: {total_price} грн", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Button(cart_window, text="Оформити замовлення", bg="green", fg="white", command=lambda: messagebox.showinfo("Успіх", "Дякуємо за покупку!")).pack(pady=10)

def add_to_cart(name, price):
    cart.append({"name": name, "price": price})
    messagebox.showinfo("Кошик", f"{name} додано до кошика!")

def open_details(name):
    data = fruits_data[name]
    dialog = tk.Toplevel(root)
    dialog.title(name)
    dialog.geometry("300x250")
    
    tk.Label(dialog, text=name, font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(dialog, text=f"Опис: {data['desc']}\nЦіна: {data['price']} грн").pack(pady=5)
    
    tk.Button(dialog, text="Додати в кошик", command=lambda: add_to_cart(name, data['price'])).pack(pady=20)

# Інтерфейс
tk.Label(root, text="Наш асортимент", font=("Arial", 18, "bold"), bg="#f4f4f9").pack(pady=20)

buttons_frame = tk.Frame(root, bg="#f4f4f9")
buttons_frame.pack()

# Кнопки товарів
for fruit in fruits_data.keys():
    tk.Button(buttons_frame, text=fruit, width=15, height=2, 
              command=lambda f=fruit: open_details(f)).pack(pady=5)

# Кнопка кошика
tk.Button(root, text="🛒 Переглянути кошик", font=("Arial", 12), bg="#4a90e2", fg="white", command=view_cart).pack(pady=30)

root.mainloop()
