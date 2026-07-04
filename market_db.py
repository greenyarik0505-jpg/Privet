import sqlite3
import hashlib
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "market.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Створюємо таблиці, якщо вони не існують
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT DEFAULT '',
            balance INTEGER DEFAULT 1000
        )
    """)
    
    # Додаткова міграція для існуючих баз даних
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT DEFAULT ''")
    except sqlite3.OperationalError:
        pass
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            fruit_name TEXT NOT NULL,
            UNIQUE(username, fruit_name)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fruit_name TEXT NOT NULL,
            username TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            order_date TEXT NOT NULL,
            total INTEGER NOT NULL,
            items_count INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(username, password, email=''):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, hashed, email))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

def login_user(username, password):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hashed))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_balance(username):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    balance = row[0] if row else 0
    conn.close()
    return balance

def add_balance(username, amount):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()

def deduct_balance(username, amount):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = balance - ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()

def get_favorites(username):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fruit_name FROM favorites WHERE username = ?", (username,))
    favs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return favs

def toggle_favorite(username, fruit_name):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM favorites WHERE username = ? AND fruit_name = ?", (username, fruit_name))
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM favorites WHERE username = ? AND fruit_name = ?", (username, fruit_name))
        is_fav = False
    else:
        cursor.execute("INSERT INTO favorites (username, fruit_name) VALUES (?, ?)", (username, fruit_name))
        is_fav = True
    conn.commit()
    conn.close()
    return is_fav

def get_reviews(fruit_name):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, rating, review_text FROM reviews WHERE fruit_name = ?", (fruit_name,))
    rows = cursor.fetchall()
    conn.close()
    return [{"username": r[0], "rating": r[1], "text": r[2]} for r in rows]

def add_review(fruit_name, username, rating, review_text):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (fruit_name, username, rating, review_text) VALUES (?, ?, ?, ?)",
                   (fruit_name, username, rating, review_text))
    conn.commit()
    conn.close()

def get_orders(username):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT order_date, total, items_count FROM orders WHERE username = ? ORDER BY id DESC", (username,))
    rows = cursor.fetchall()
    conn.close()
    return [{"date": r[0], "total": r[1], "items_count": r[2]} for r in rows]

def add_order(username, total, items_count, date_str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (username, order_date, total, items_count) VALUES (?, ?, ?, ?)",
                   (username, date_str, total, items_count))
    conn.commit()
    conn.close()

def delete_user(username):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    cursor.execute("DELETE FROM favorites WHERE username = ?", (username,))
    cursor.execute("DELETE FROM reviews WHERE username = ?", (username,))
    cursor.execute("DELETE FROM orders WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def delete_order(username, date_str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE username = ? AND order_date = ?", (username, date_str))
    conn.commit()
    conn.close()

def verify_and_reset_password(username, email, new_password):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(?) AND LOWER(email) = LOWER(?)", (username, email))
    user = cursor.fetchone()
    if user:
        hashed = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user[0]))
        conn.commit()
        success = True
    else:
        success = False
    conn.close()
    return success
