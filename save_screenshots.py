import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageGrab
import os
import time
import sys

# Ми імпортуємо вміст з main.py, але налаштовуємо його на авто-виконання сценарію знімків екрану
# Для цього ми запустимо додаток і будемо керувати ним програмно.

def run_screenshot_sequence():
    print("Запуск автоматичної зйомки екрану...")
    
    # 1. Чекаємо завантаження головного вікна та робимо перший знімок
    time.sleep(1.0)
    root.update()
    
    try:
        # Розраховуємо координати головного вікна
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        
        # Захоплюємо область екрану
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        screenshot.save("screenshot_main.png")
        print("Знімок головного екрану збережено: screenshot_main.png")
        
        # 2. Відкриваємо вікно деталей першого фрукта (Яблуко 🍎)
        open_details("Яблуко 🍎")
        time.sleep(1.0)
        
        # Знаходимо активне вікно деталей (Toplevel)
        detail_win = None
        for child in root.winfo_children():
            if isinstance(child, tk.Toplevel):
                detail_win = child
                break
                
        if detail_win:
            detail_win.update()
            dx = detail_win.winfo_rootx()
            dy = detail_win.winfo_rooty()
            dw = detail_win.winfo_width()
            dh = detail_win.winfo_height()
            
            screenshot_det = ImageGrab.grab(bbox=(dx, dy, dx + dw, dy + dh))
            screenshot_det.save("screenshot_details.png")
            print("Знімок вікна деталей збережено: screenshot_details.png")
            
            # Додаємо у кошик програмно
            # qty_spin за замовчуванням має значення 1. Натискаємо кнопку додавання.
            # Знайдемо кнопку додавання
            for btn in detail_win.winfo_children():
                if isinstance(btn, tk.Button) and btn.cget("text") == "Додати в кошик":
                    btn.invoke()
                    break
                    
        time.sleep(1.0)
        
        # 3. Відкриваємо кошик
        view_cart()
        time.sleep(1.0)
        
        cart_win = None
        for child in root.winfo_children():
            if isinstance(child, tk.Toplevel) and child.title() == "Ваш кошик":
                cart_win = child
                break
                
        if cart_win:
            cart_win.update()
            cx = cart_win.winfo_rootx()
            cy = cart_win.winfo_rooty()
            cw = cart_win.winfo_width()
            ch = cart_win.winfo_height()
            
            screenshot_cart = ImageGrab.grab(bbox=(cx, cy, cx + cw, cy + ch))
            screenshot_cart.save("screenshot_cart.png")
            print("Знімок вікна кошика збережено: screenshot_cart.png")
            
        print("Всі знімки екрану успішно створено!")
        
    except Exception as e:
        print(f"Помилка при створенні знімків: {e}")
        print("Переконайтеся, що вікно програми повністю видно на екрані та не згорнуто.")
        
    finally:
        root.destroy()
        sys.exit(0)

if __name__ == "__main__":
    # Щоб запустити автоматичний скріншотер, імпортуємо і запускаємо логіку головного вікна
    # Переписуємо запуск root.mainloop на наш таймер
    
    # Створюємо хук у головний цикл
    import main
    # Замінюємо main_loop на відкладений запуск скріншотера
    main.root.after(500, run_screenshot_sequence)
    main.root.mainloop()
