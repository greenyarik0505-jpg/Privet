<div align="center">

<img src="assets/silpo_logo.png" alt="Silpo Logo" width="120"/>

# ✦ SILPO MARKETPLACE ✦
### *Твій персональний супермаркет прямо на робочому столі*

<br/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-FF6B6B?style=for-the-badge&logo=python&logoColor=white)](https://github.com/TomSchimansky/CustomTkinter)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)](LICENSE)
[![Products](https://img.shields.io/badge/Products-504_items-blueviolet?style=for-the-badge)](https://github.com/greenyarik0505-jpg/Privet)

<br/>

> 🌟 **504 реальних товари Сільпо** · **7 категорій** · **Замовлення з чеком** · **Аналітика** · **Відгуки**

</div>

---

<div align="center">

## 📸 Вигляд програми

</div>

| 🏠 Каталог | 📄 Деталі товару | 🛒 Кошик |
|:----------:|:----------------:|:--------:|
| ![Main](screenshot_main_v6.png) | ![Details](screenshot_details_v6.png) | ![Cart](screenshot_cart_v6.png) |
| *504 товари, 7 категорій, пошук в реальному часі* | *Опис, сорт/варіант, відгуки та рейтинг* | *Кошик з формою доставки та оплатою* |

---

<div align="center">

## ⚡ Ключові можливості

</div>

```
╔══════════════════════════════════════════════════════════════════╗
║  🛒  504 реальних товари Сільпо у 7 категоріях                   ║
║  🌍  3 мови: Українська · English · Русский                      ║
║  🎨  Темна та світла теми — перемикання в один клік              ║
║  ⚡  Пошук в реальному часі серед сотень товарів                  ║
║  📦  Завантаження зображень у фоні — без зависань                 ║
║  ⭐  Відгуки та рейтинги на кожен товар                           ║
║  🧾  HTML-чек після кожного замовлення                            ║
║  📊  Аналітика витрат та історія замовлень                        ║
║  💰  Гаманець з поповненням балансу                               ║
╚══════════════════════════════════════════════════════════════════╝
```

<br/>

<table>
<tr>
<td width="50%">

### 🛍️ Каталог та Пошук
- **504 реальних товари** з фото, цінами та описами
- Миттєвий пошук без затримок
- Фільтрація по 7 категоріях
- Пагінація по 15 товарів на сторінці

</td>
<td width="50%">

### 🔐 Авторизація
- Реєстрація та вхід через логін/пароль
- Дані зберігаються в локальній SQLite БД
- Авто-вхід через `session.txt`
- Видалення акаунту

</td>
</tr>
<tr>
<td width="50%">

### 🌍 Мови та Теми
- Перемикання між 🇺🇦 🇬🇧 🇷🇺 без перезапуску
- Темна 🌙 та світла ☀️ теми
- Все зберігається між сесіями

</td>
<td width="50%">

### 🧾 Замовлення та Чеки
- Форма доставки (телефон, email, адреса)
- Вибір доставки: Кур'єр / Нова Пошта
- Оплата балансом або карткою
- Генерація HTML чека після оплати

</td>
</tr>
</table>

---

<div align="center">

## 📦 Категорії товарів

</div>

<div align="center">

| Категорія | Назва | Приклади товарів |
|:---------:|:-----:|:-----------------|
| 🥖 | **Випічка** | Хліб подовий, Батон, Булочки, Круасани, Лаваш |
| 🥛 | **Молочні** | Молоко, Сир, Йогурт, Масло, Сметана |
| 🥩 | **М'ясо & Риба** | Куряче філе, Яловичина, Форель, Ковбаса |
| 🍎 | **Фрукти & Овочі** | Яблука, Банани, Томати, Огірки, Морква |
| 🛒 | **Бакалія** | Крупи, Макарони, Консерви, Олія, Борошно |
| 🍫 | **Снеки** | Чіпси, Горішки, Шоколад, Жуйка, Батончики |
| 🥤 | **Напої** | Сік, Вода, Кола, Енергетики, Чай |

</div>

---

<div align="center">

## ⚙️ Архітектура системи

</div>

```mermaid
graph TD
    A["🖥️ CustomTkinter GUI"] --> B["🔐 Login / Register"]
    B -->|Успіх| C["🏠 Головний екран"]
    C --> D["⚙️ Налаштування"]
    C --> E["🛒 Кошик"]
    C --> F["📄 Деталі товару"]
    C --> G["📊 Аналітика"]
    C --> H["📜 Історія"]
    D -->|Мова / Тема| C
    F -->|Читати відгуки| I[("🗄️ SQLite")]
    F -->|Писати відгуки| I
    E -->|Зберегти замовлення| I
    E -->|Списати баланс| I
    E -->|Генерувати| J["🧾 HTML Чек"]
    K["🔄 Фонові потоки"] -->|Завантажити фото| L["📥 Image Cache"]
    L -->|PNG файли| M["📁 cache_images/"]
    C -->|Відображати| M
```

---

<div align="center">

## 🛠️ Технологічний стек

</div>

<div align="center">

| Бібліотека | Версія | Призначення |
|:----------:|:------:|:-----------:|
| ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | 3.8+ | Основна мова |
| ![CTk](https://img.shields.io/badge/-CustomTkinter-FF6B6B?logo=python&logoColor=white) | Latest | Сучасний GUI |
| ![Pillow](https://img.shields.io/badge/-Pillow-yellow?logo=python&logoColor=black) | 10.0+ | Обробка зображень |
| ![SQLite](https://img.shields.io/badge/-SQLite3-07405E?logo=sqlite&logoColor=white) | Built-in | База даних |
| ![Threading](https://img.shields.io/badge/-threading-lightgrey?logo=python&logoColor=black) | Built-in | Фоновий завантажувач |
| ![urllib](https://img.shields.io/badge/-urllib-lightblue?logo=python&logoColor=black) | Built-in | HTTP запити |

</div>

---

<div align="center">

## 🚀 Встановлення та Запуск

</div>

**1. Клонуй репозиторій:**
```bash
git clone https://github.com/greenyarik0505-jpg/Privet.git
cd Privet
```

**2. Встанови залежності:**
```bash
pip install customtkinter pillow
```

**3. Запусти:**
```bash
python main.py
```

> ✅ При першому запуску зображення завантажаться автоматично у фоні.

---

<div align="center">

## 📖 Інструкція користувача

</div>

<details>
<summary><b>👤 Реєстрація та вхід</b></summary>

- Запусти `main.py`
- Натисни **Реєстрація** → введи логін та пароль → **Зареєструватися**
- Або **Увійти** якщо вже є акаунт
- При наступному запуску вхід буде автоматичним

</details>

<details>
<summary><b>🛍️ Пошук та покупки</b></summary>

- Введи назву товару в поле **"Пошук продуктів..."** — результати оновлюються миттєво
- Клікни на категорію щоб відфільтрувати товари
- Натисни **"+"** або **"-"** щоб змінити кількість, потім **"+ Додати"**
- Або відкрий картку товару для детального перегляду та відгуків

</details>

<details>
<summary><b>🧾 Оформлення замовлення</b></summary>

- Перейди в **Кошик** у лівому меню
- Перевір товари та загальну суму
- Заповни: телефон (+380...), email, адресу доставки
- Вибери спосіб доставки та оплати
- Натисни **"Оформити замовлення"** — HTML чек збережеться у папці проєкту

</details>

<details>
<summary><b>⚙️ Налаштування</b></summary>

- **Налаштування** → вибір мови (🇺🇦 / 🇬🇧 / 🇷🇺)
- Перемикач теми: **Темна 🌙** або **Світла ☀️**
- **"+ Поповнити"** → додати 500 грн до балансу

</details>

---

<div align="center">

## 💻 Схема бази даних

</div>

```sql
-- Користувачі
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    balance  INTEGER DEFAULT 1000
);

-- Відгуки та рейтинги
CREATE TABLE reviews (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    username     TEXT,
    rating       INTEGER CHECK(rating BETWEEN 1 AND 5),
    text         TEXT
);

-- Замовлення
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT,
    total       INTEGER,
    items_count INTEGER,
    date        TEXT
);
```

---

<div align="center">

## 📊 Таблиця функцій

| Функція | Статус | Деталі |
|:--------|:------:|:-------|
| 504 реальних товари Сільпо | ✅ | 7 категорій |
| Завантаження зображень у фоні | ✅ | Кеш у `cache_images/` |
| Реєстрація та вхід | ✅ | SQLite, авто-сесія |
| 3 мови (UA / EN / RU) | ✅ | Миттєве перемикання |
| Темна / Світла тема | ✅ | Динамічне перемикання |
| Пошук в реальному часі | ✅ | 504 товари, без затримок |
| Відгуки та рейтинги | ✅ | На кожен товар окремо |
| Кошик та оформлення | ✅ | З формою доставки |
| HTML чек після оплати | ✅ | `receipt_*.html` |
| Поповнення балансу | ✅ | +500 грн за клік |
| Аналітика витрат | ✅ | Графіки і статистика |
| Історія замовлень | ✅ | Всі минулі покупки |

</div>

---

<div align="center">

## 🤝 Внесок у проєкт

Будемо раді pull request-ам!

1. Fork репозиторію
2. Створи гілку: `git checkout -b feature/MyFeature`
3. Зроби коміт: `git commit -m 'Add MyFeature'`
4. Запуш: `git push origin feature/MyFeature`
5. Відкрий Pull Request

---

<br/>

*Розроблено з ❤️ на Python · Дані з реального каталогу супермаркету Сільпо*

[![GitHub](https://img.shields.io/badge/GitHub-greenyarik0505--jpg-181717?style=for-the-badge&logo=github)](https://github.com/greenyarik0505-jpg/Privet)

</div>