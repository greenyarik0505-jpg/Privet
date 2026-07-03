"""
take_screenshots.py
-------------------
Запусти цей скрипт окремо (не через агента):
    python take_screenshots.py

Що робить:
1. Запускає main.py
2. Чекає поки вікно з'явиться
3. Робить скріншоти: головна, деталі товару, кошик
4. Зберігає як screenshot_main_v7.png і т.д.
5. Потім просто зроби: git add *.png && git commit && git push

Залежності: pip install pyautogui pillow pygetwindow
"""

import subprocess
import sys
import os
import time

# ── Перевірка залежностей ──────────────────────────────────────────────────────
try:
    import pyautogui
    import pygetwindow as gw
    from PIL import ImageGrab
except ImportError:
    print("Встановлення залежностей...")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "pyautogui", "pygetwindow", "pillow", "-q"])
    import pyautogui
    import pygetwindow as gw
    from PIL import ImageGrab

pyautogui.FAILSAFE = True
APP_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = APP_DIR  # Скріншоти зберігаємо прямо в папці проєкту

def find_window():
    """Знаходить вікно застосунку за заголовком."""
    for title in gw.getAllTitles():
        if "Silpo" in title or "silpo" in title.lower() or "Сільпо" in title or "Market" in title:
            return gw.getWindowsWithTitle(title)[0]
    # Fallback — будь-яке вікно tkinter/python
    for title in gw.getAllTitles():
        if title and title not in ("", "Program Manager"):
            wins = gw.getWindowsWithTitle(title)
            if wins:
                return wins[0]
    return None


def capture_window(win, filename):
    """Робить скріншот вікна і зберігає у файл."""
    # Переконаємося що вікно активне і на передньому плані
    try:
        win.activate()
    except Exception:
        pass
    time.sleep(0.5)

    x, y, w, h = win.left, win.top, win.width, win.height
    # Невелика затримка щоб UI встиг перемалюватися
    time.sleep(0.3)
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    path = os.path.join(OUT_DIR, filename)
    img.save(path)
    print(f"  ✅ Збережено: {filename} ({w}x{h})")
    return path


def click_in_window(win, rel_x_ratio, rel_y_ratio):
    """Клік відносно вікна (0.0–1.0 = відносні координати)."""
    x = win.left + int(win.width * rel_x_ratio)
    y = win.top + int(win.height * rel_y_ratio)
    pyautogui.click(x, y)
    time.sleep(1.0)


def main():
    print("=" * 55)
    print("  📸  Silpo Screenshot Tool")
    print("=" * 55)

    # ── Запуск застосунку ──────────────────────────────────────────────────────
    print("\n▶️  Запускаю main.py ...")
    proc = subprocess.Popen(
        [sys.executable, os.path.join(APP_DIR, "main.py")],
        cwd=APP_DIR
    )

    # Чекаємо поки вікно з'явиться (до 15 секунд)
    print("⏳  Чекаю на вікно застосунку", end="")
    win = None
    for _ in range(30):
        time.sleep(0.5)
        print(".", end="", flush=True)
        win = find_window()
        if win and win.width > 200:
            break
    print()

    if not win:
        print("❌  Вікно не знайдено! Перевір що застосунок запускається.")
        proc.terminate()
        return

    print(f"✅  Вікно знайдено: «{win.title}» ({win.width}x{win.height})")
    time.sleep(2.0)  # Чекаємо повного завантаження UI

    # ── Скріншот 1: Авторизація / Головна ──────────────────────────────────────
    print("\n📸  Скріншот 1: Головна сторінка (каталог)")
    capture_window(win, "screenshot_main_v7.png")

    # ── Клік на перший товар ───────────────────────────────────────────────────
    print("\n🖱️   Кліком відкриваю перший товар...")
    # Товари знаходяться в правій частині, приблизно 55% по X, 45% по Y
    click_in_window(win, 0.55, 0.48)
    time.sleep(1.5)

    # ── Скріншот 2: Деталі товару ──────────────────────────────────────────────
    print("📸  Скріншот 2: Деталі товару")
    capture_window(win, "screenshot_details_v7.png")

    # ── Клік «← Назад» ────────────────────────────────────────────────────────
    print("\n🖱️   Натискаю «Назад» ...")
    click_in_window(win, 0.28, 0.08)
    time.sleep(1.0)

    # ── Клік на «Кошик» у сайдбарі ────────────────────────────────────────────
    print("🖱️   Відкриваю Кошик...")
    # Кошик — другий пункт меню у лівому сайдбарі (~13% X, 52% Y)
    click_in_window(win, 0.08, 0.52)
    time.sleep(1.5)

    # ── Скріншот 3: Кошик ─────────────────────────────────────────────────────
    print("📸  Скріншот 3: Кошик / Оформлення замовлення")
    capture_window(win, "screenshot_cart_v7.png")

    # ── Бонус: темна тема ──────────────────────────────────────────────────────
    print("\n🖱️   Перемикаю темну тему...")
    # Кнопка теми ~13% X, 38% Y (під балансом у сайдбарі)
    click_in_window(win, 0.08, 0.38)
    time.sleep(1.0)

    # Повертаємось на каталог
    click_in_window(win, 0.08, 0.46)
    time.sleep(1.5)

    print("📸  Скріншот 4: Каталог у темній темі")
    capture_window(win, "screenshot_dark_v7.png")

    # ── Завершення ─────────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  ✅  Всі скріншоти збережено!")
    print("=" * 55)
    print("\nФайли:")
    for name in ["screenshot_main_v7.png", "screenshot_details_v7.png",
                 "screenshot_cart_v7.png", "screenshot_dark_v7.png"]:
        path = os.path.join(OUT_DIR, name)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  📷  {name}  ({size // 1024} KB)")

    print("\n👇  Далі виконай у терміналі:")
    print("  git add screenshot_*_v7.png")
    print("  git commit -m 'Update screenshots v7'")
    print("  git push")
    print("\nНатисни Enter щоб закрити застосунок...")
    input()
    proc.terminate()


if __name__ == "__main__":
    main()
