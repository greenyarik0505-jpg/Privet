"""
take_screenshots.py
-------------------
Запуск:  python take_screenshots.py

Знаходить текст РЕАЛЬНО на екрані через EasyOCR (без координат).
Перший запуск: скачає OCR-модель ~100 MB (один раз).
"""

import subprocess, sys, os, time
import numpy as np

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Залежності ─────────────────────────────────────────────────────────────────
def pip(*pkgs):
    subprocess.check_call([sys.executable, "-m", "pip", "install", *pkgs, "-q"])

try:
    import pygetwindow as gw
except ImportError:
    pip("pygetwindow"); import pygetwindow as gw

try:
    from PIL import ImageGrab, Image
except ImportError:
    pip("pillow"); from PIL import ImageGrab, Image

try:
    import pyautogui
except ImportError:
    pip("pyautogui"); import pyautogui

try:
    import easyocr
except ImportError:
    print("📦  Встановлюю easyocr (один раз)...")
    pip("easyocr"); import easyocr

pyautogui.FAILSAFE = True

# ── OCR reader (ініціалізується один раз) ─────────────────────────────────────
print("🔤  Ініціалізую OCR (перший раз завантажує ~100 MB)...")
reader = easyocr.Reader(['uk', 'en'], verbose=False)
print("✅  OCR готовий")

# ── Робота з вікном ────────────────────────────────────────────────────────────

def find_win():
    for t in gw.getAllTitles():
        if t.strip() == "Silpo":
            wins = gw.getWindowsWithTitle(t)
            if wins and wins[0].width > 200:
                return wins[0]
    return None


def wait_win(timeout=70):
    print(f"\n⏳  Чекаю вікно 'Silpo' (до {timeout} сек)", end="", flush=True)
    for _ in range(timeout * 2):
        time.sleep(0.5)
        print(".", end="", flush=True)
        w = find_win()
        if w:
            print(f"\n✅  Знайдено: {w.width}x{w.height}")
            return w
    print("\n❌  Вікно не знайдено!")
    return None


def wait(n, label=""):
    if label:
        print(f"  ⌛  {label}", end="", flush=True)
    for _ in range(n):
        time.sleep(1)
        if label:
            print(".", end="", flush=True)
    if label:
        print()

# ── Знімок ТІЛЬКИ вікна ────────────────────────────────────────────────────────

def snap_win(win):
    """Повертає PIL.Image тільки вікна Silpo."""
    try: win.activate()
    except: pass
    time.sleep(0.35)
    x, y, w, h = win.left, win.top, win.width, win.height
    return ImageGrab.grab(bbox=(x, y, x + w, y + h)), (x, y)


def save_snap(win, filename):
    img, _ = snap_win(win)
    path = os.path.join(APP_DIR, filename)
    img.save(path, "PNG")
    kb = os.path.getsize(path) // 1024
    print(f"  📷  {filename}  ({img.width}x{img.height} px, {kb} KB)")


# ── Знайти текст через OCR і клікнути ─────────────────────────────────────────

def click_by_text(win, search_text, timeout=8):
    """
    Шукає текст на скріншоті вікна за допомогою EasyOCR.
    Клікає в центр знайденого рядка (екранні координати).
    """
    print(f"  🖱️   Шукаю '{search_text}'...", end=" ", flush=True)
    deadline = time.time() + timeout
    while time.time() < deadline:
        img, (wx, wy) = snap_win(win)
        img_np = np.array(img)

        results = reader.readtext(img_np, detail=1, paragraph=False)

        best = None
        best_score = 0
        for (bbox, text, conf) in results:
            # Нечітке порівняння — шукаємо часткове входження
            if search_text.lower() in text.lower() and conf > 0.25:
                if conf > best_score:
                    best_score = conf
                    best = bbox

        if best:
            # bbox = [[x1,y1],[x2,y1],[x2,y2],[x1,y2]]
            cx = int((best[0][0] + best[2][0]) / 2)
            cy = int((best[0][1] + best[2][1]) / 2)
            # Перетворюємо в екранні координати
            screen_x = wx + cx
            screen_y = wy + cy
            pyautogui.click(screen_x, screen_y)
            print(f"✅  (OCR conf={best_score:.2f}, pos={cx},{cy})")
            time.sleep(1.3)
            return True

        time.sleep(1.0)

    print(f"❌  Не знайдено '{search_text}' за {timeout} сек")
    return False


# ── Головна логіка ─────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  📸  Silpo Screenshot Tool  (OCR text-based clicks)")
    print("=" * 55)

    print("\n▶️   Запускаю main.py ...")
    proc = subprocess.Popen(
        [sys.executable, os.path.join(APP_DIR, "main.py")],
        cwd=APP_DIR
    )

    win = wait_win(timeout=70)
    if not win:
        proc.terminate(); return

    wait(12, "Завантаження каталогу і фото")
    win = find_win()
    if not win:
        print("❌  Вікно зникло!"); proc.terminate(); return

    print("\n── Скріншоти ──────────────────────────────────────────")

    # [1] Каталог
    print("\n[1/4] Головна — каталог товарів")
    click_by_text(win, "Каталог")
    wait(2)
    win = find_win()
    save_snap(win, "screenshot_main_v7.png")

    # [2] Деталі товару — клік на назву першого хліба
    print("\n[2/4] Деталі товару")
    click_by_text(win, "Хліб")          # перше входження "Хліб" у назві товару
    wait(3, "Деталі")
    win = find_win()
    save_snap(win, "screenshot_details_v7.png")

    # Назад
    click_by_text(win, "Назад")
    wait(2)
    win = find_win()

    # [3] Кошик
    print("\n[3/4] Кошик")
    click_by_text(win, "Кошик")
    wait(2, "Кошик")
    win = find_win()
    save_snap(win, "screenshot_cart_v7.png")

    # [4] Темна тема
    print("\n[4/4] Темна тема")
    click_by_text(win, "Каталог")
    wait(1)
    win = find_win()

    click_by_text(win, "тема")          # "Темна тема" / "Світла тема"
    wait(3, "Тема застосовується")
    win = find_win()
    save_snap(win, "screenshot_dark_v7.png")

    # Підсумок
    print("\n" + "=" * 55)
    print("  ✅  Готово! Файли:")
    for name in ["screenshot_main_v7.png", "screenshot_details_v7.png",
                 "screenshot_cart_v7.png", "screenshot_dark_v7.png"]:
        path = os.path.join(APP_DIR, name)
        if os.path.exists(path):
            print(f"     📷  {name}  ({os.path.getsize(path)//1024} KB)")
        else:
            print(f"     ❌  {name}  — не створено")

    print("\n👇  Запуши:")
    print("     git add screenshot_*_v7.png")
    print('     git commit -m "Update screenshots v7"')
    print("     git push")
    print("\nНатисни Enter щоб закрити...")
    input()
    proc.terminate()


if __name__ == "__main__":
    main()
