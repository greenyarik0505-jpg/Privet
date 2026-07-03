"""
take_screenshots.py
-------------------
Запуск:  python take_screenshots.py

Клікає по ТЕКСТУ кнопок (не координатах) через pywinauto.
Фоткає ТІЛЬКИ вікно Silpo.
"""

import subprocess, sys, os, time

# ── Залежності ─────────────────────────────────────────────────────────────────
def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

try:
    import pygetwindow as gw
except ImportError:
    install("pygetwindow"); import pygetwindow as gw

try:
    from PIL import ImageGrab
except ImportError:
    install("pillow"); from PIL import ImageGrab

try:
    import pywinauto
    from pywinauto import Desktop
except ImportError:
    install("pywinauto"); from pywinauto import Desktop

APP_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Знайти вікно ───────────────────────────────────────────────────────────────

def find_silpo_win_gw():
    """pygetwindow: знайти вікно з точним заголовком Silpo."""
    for t in gw.getAllTitles():
        if t.strip() == "Silpo":
            wins = gw.getWindowsWithTitle(t)
            if wins and wins[0].width > 200:
                return wins[0]
    return None


def wait_for_window(timeout=60):
    print(f"⏳  Чекаю вікно 'Silpo' (до {timeout} сек)", end="", flush=True)
    for _ in range(timeout * 2):
        time.sleep(0.5)
        print(".", end="", flush=True)
        w = find_silpo_win_gw()
        if w:
            print(f"\n✅  Знайдено: {w.width}x{w.height}")
            return w
    print("\n❌  Вікно не знайдено!")
    return None


def wait_ui(n=5, label=""):
    if label:
        print(f"  ⌛  {label}", end="", flush=True)
    for _ in range(n):
        time.sleep(1)
        if label:
            print(".", end="", flush=True)
    if label:
        print()

# ── Скріншот тільки вікна ──────────────────────────────────────────────────────

def snap(gw_win, filename):
    """Знімок тільки bbox вікна Silpo."""
    try:
        gw_win.activate()
    except Exception:
        pass
    time.sleep(0.4)

    x, y, w, h = gw_win.left, gw_win.top, gw_win.width, gw_win.height
    img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    path = os.path.join(APP_DIR, filename)
    img.save(path, "PNG")
    kb = os.path.getsize(path) // 1024
    print(f"  📷  {filename}  ({w}x{h} px, {kb} KB)")

# ── Клік по тексту через pywinauto ────────────────────────────────────────────

_pwa_app = None

def get_pwa():
    global _pwa_app
    try:
        _pwa_app = Desktop(backend="uia").window(title="Silpo")
        _pwa_app.wait("exists", timeout=5)
        return _pwa_app
    except Exception as e:
        print(f"  ⚠️  pywinauto (uia) не вдалося: {e}")
        return None


def click_text(text, gw_win=None, timeout=5):
    """
    Шукає елемент з потрібним текстом у вікні Silpo і клікає на нього.
    Якщо pywinauto не знаходить — клікає по центру вікна (fallback).
    """
    print(f"  🖱️   Шукаю '{text}'...", end=" ", flush=True)

    # Спроба 1: pywinauto UIA
    pwa = get_pwa()
    if pwa:
        try:
            # Шукаємо будь-який елемент з таким текстом
            el = pwa.child_window(title=text, found_index=0)
            el.wait("exists visible", timeout=timeout)
            el.click_input()
            print(f"✅ (pywinauto)")
            time.sleep(1.2)
            return True
        except Exception:
            pass

        # Спроба 2: шукаємо часткове співпадіння
        try:
            from pywinauto.findwindows import ElementNotFoundError
            el = pwa.child_window(title_re=f".*{text}.*", found_index=0)
            el.wait("exists visible", timeout=timeout)
            el.click_input()
            print(f"✅ (pywinauto regex)")
            time.sleep(1.2)
            return True
        except Exception as e:
            print(f"⚠️  не знайдено: {e}")

    # Fallback: нічого не знайшли
    print(f"❌  Не знайдено '{text}' — пропускаю")
    return False


# ── Головна логіка ─────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  📸  Silpo Screenshot Tool  (text-based clicks)")
    print("=" * 55)

    # 1. Запускаємо застосунок
    print("\n▶️   Запускаю main.py ...")
    proc = subprocess.Popen(
        [sys.executable, os.path.join(APP_DIR, "main.py")],
        cwd=APP_DIR
    )

    # 2. Чекаємо вікно
    gw_win = wait_for_window(timeout=60)
    if not gw_win:
        proc.terminate(); return

    # 3. Чекаємо завантаження UI + фото
    wait_ui(12, "Завантаження каталогу і фото")

    gw_win = find_silpo_win_gw()
    if not gw_win:
        print("❌  Вікно зникло!"); proc.terminate(); return

    print("\n── Скріншоти ──────────────────────────────────────────")

    # ── [1] Головна ──────────────────────────────────────────────────────────
    print("\n[1/4] Головна — каталог")
    # Спочатку переходимо на Каталог щоб переконатись
    click_text("Каталог")
    wait_ui(2)
    gw_win = find_silpo_win_gw()
    snap(gw_win, "screenshot_main_v7.png")

    # ── [2] Деталі товару ─────────────────────────────────────────────────────
    print("\n[2/4] Деталі товару")
    # Клікаємо на назву першого товару
    click_text("Хліб подовий")
    wait_ui(3, "Завантаження деталей")
    gw_win = find_silpo_win_gw()
    snap(gw_win, "screenshot_details_v7.png")

    # Повертаємось назад
    click_text("← Назад")
    wait_ui(2)
    gw_win = find_silpo_win_gw()

    # ── [3] Кошик ─────────────────────────────────────────────────────────────
    print("\n[3/4] Кошик")
    click_text("Кошик")
    wait_ui(2, "Завантаження кошика")
    gw_win = find_silpo_win_gw()
    snap(gw_win, "screenshot_cart_v7.png")

    # ── [4] Темна тема ────────────────────────────────────────────────────────
    print("\n[4/4] Темна тема")
    # Повертаємось на Каталог
    click_text("Каталог")
    wait_ui(1)
    gw_win = find_silpo_win_gw()

    # Вмикаємо темну тему
    click_text("🌙 Темна тема")
    wait_ui(3, "Застосування теми")
    gw_win = find_silpo_win_gw()
    snap(gw_win, "screenshot_dark_v7.png")

    # ── Підсумок ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  ✅  Готово! Файли:")
    files = ["screenshot_main_v7.png", "screenshot_details_v7.png",
             "screenshot_cart_v7.png", "screenshot_dark_v7.png"]
    for name in files:
        path = os.path.join(APP_DIR, name)
        if os.path.exists(path):
            print(f"     📷  {name}  ({os.path.getsize(path)//1024} KB)")
        else:
            print(f"     ❌  {name}  — НЕ СТВОРЕНО")

    print("\n👇  Запуши:")
    print("     git add screenshot_*_v7.png")
    print('     git commit -m "Update screenshots v7"')
    print("     git push")

    print("\nНатисни Enter щоб закрити застосунок...")
    input()
    proc.terminate()


if __name__ == "__main__":
    main()
