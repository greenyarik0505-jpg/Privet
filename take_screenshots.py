"""
take_screenshots.py
-------------------
Запуск:  python take_screenshots.py
Робить скріншоти тільки вікна Silpo і зберігає їх у папці проєкту.
"""

import subprocess, sys, os, time

# ── Залежності ─────────────────────────────────────────────────────────────────
try:
    import pyautogui
    import pygetwindow as gw
    from PIL import ImageGrab
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "pyautogui", "pygetwindow", "pillow", "-q"])
    import pyautogui
    import pygetwindow as gw
    from PIL import ImageGrab

pyautogui.FAILSAFE = True
APP_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Допоміжні функції ──────────────────────────────────────────────────────────

def find_silpo_window():
    """Шукає вікно з точним заголовком 'Silpo'."""
    for title in gw.getAllTitles():
        if title.strip() == "Silpo":
            wins = gw.getWindowsWithTitle(title)
            if wins and wins[0].width > 200:
                return wins[0]
    return None


def wait_for_window(timeout=60):
    """Чекає поки з'явиться вікно Silpo. Повертає вікно або None."""
    print(f"⏳  Чекаю на вікно 'Silpo' (до {timeout} сек)", end="", flush=True)
    for _ in range(timeout * 2):
        time.sleep(0.5)
        print(".", end="", flush=True)
        win = find_silpo_window()
        if win:
            print(f"\n✅  Вікно знайдено: {win.width}x{win.height}")
            return win
    print("\n❌  Вікно не знайдено!")
    return None


def wait_for_load(extra_seconds=8):
    """Додаткове очікування поки інтерфейс повністю завантажиться."""
    print(f"⌛  Чекаю завантаження UI ({extra_seconds} сек)", end="", flush=True)
    for _ in range(extra_seconds):
        time.sleep(1)
        print(".", end="", flush=True)
    print(" Готово!")


def snap(win, filename):
    """Фотографує ТІЛЬКИ вікно застосунку (не весь екран)."""
    try:
        win.activate()
    except Exception:
        pass
    time.sleep(0.4)

    # Беремо точні координати вікна
    x, y, w, h = win.left, win.top, win.width, win.height

    # Захоплюємо тільки область вікна
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    path = os.path.join(APP_DIR, filename)
    img.save(path, "PNG")
    kb = os.path.getsize(path) // 1024
    print(f"  📷  {filename}  ({w}x{h}, {kb} KB)")
    return path


def click_rel(win, rx, ry, label=""):
    """Клік у відносних координатах вікна (0.0–1.0)."""
    x = win.left + int(win.width  * rx)
    y = win.top  + int(win.height * ry)
    if label:
        print(f"  🖱️   Клік: {label} ({x},{y})")
    pyautogui.click(x, y)
    time.sleep(1.5)


# ── Головна логіка ─────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  📸  Silpo Screenshot Tool")
    print("=" * 55)

    # 1. Запуск застосунку
    print("\n▶️   Запускаю main.py ...")
    proc = subprocess.Popen(
        [sys.executable, os.path.join(APP_DIR, "main.py")],
        cwd=APP_DIR
    )

    # 2. Чекаємо поки вікно з'явиться (до 60 сек)
    win = wait_for_window(timeout=60)
    if not win:
        proc.terminate()
        return

    # 3. Чекаємо поки UI повністю завантажиться (каталог + фото)
    wait_for_load(extra_seconds=10)

    # Оновлюємо позицію вікна після завантаження
    win = find_silpo_window()
    if not win:
        print("❌  Вікно зникло під час завантаження!")
        proc.terminate()
        return

    print("\n── Скріншоти ──────────────────────────────────────────")

    # 4. Скріншот головного екрану (каталог)
    print("\n[1/4] Головна — каталог товарів")
    snap(win, "screenshot_main_v7.png")

    # 5. Клік на перший товар у каталозі
    #    Товари починаються приблизно з 35% ширини (після сайдбару)
    #    і ~45% висоти
    click_rel(win, 0.42, 0.48, "перший товар")
    wait_for_load(3)
    win = find_silpo_window()

    print("[2/4] Деталі товару")
    snap(win, "screenshot_details_v7.png")

    # 6. Назад
    click_rel(win, 0.30, 0.07, "← Назад")
    time.sleep(1.5)
    win = find_silpo_window()

    # 7. Кошик — другий пункт у сайдбарі (~8% X, ~52% Y)
    click_rel(win, 0.08, 0.52, "Кошик")
    wait_for_load(2)
    win = find_silpo_window()

    print("[3/4] Кошик / Оформлення")
    snap(win, "screenshot_cart_v7.png")

    # 8. Каталог назад
    click_rel(win, 0.08, 0.46, "Каталог")
    time.sleep(1.5)
    win = find_silpo_window()

    # 9. Темна тема — кнопка ~8% X, ~39% Y (під балансом)
    click_rel(win, 0.08, 0.39, "🌙 Темна тема")
    wait_for_load(3)
    win = find_silpo_window()

    print("[4/4] Каталог (темна тема)")
    snap(win, "screenshot_dark_v7.png")

    # 10. Підсумок
    print("\n" + "=" * 55)
    print("  ✅  Готово! Файли збережено:")
    for name in ["screenshot_main_v7.png", "screenshot_details_v7.png",
                 "screenshot_cart_v7.png", "screenshot_dark_v7.png"]:
        path = os.path.join(APP_DIR, name)
        if os.path.exists(path):
            print(f"     📷  {name}")

    print("\n👇  Запуши скріншоти:")
    print('     git add screenshot_*_v7.png')
    print('     git commit -m "Update screenshots v7"')
    print('     git push')

    print("\nНатисни Enter щоб закрити застосунок...")
    input()
    proc.terminate()


if __name__ == "__main__":
    main()
