import sqlite3 as sql
import requests
import random
import time

conn = sql.connect('catolog.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    haracteristici TEXT,
    art TEXT,
    price INT
)
''')
c.execute("CREATE INDEX IF NOT EXISTS idx_art ON products(art)")
c.execute("CREATE INDEX IF NOT EXISTS idx_price ON products(price)")

proxies = {
    "http": " ",
    "https": " "
}

def product_info(art):
    headers = {
        "user-agent": "Mozilla/5.0",
        "referer": f"https://global.wildberries.ru/catalog/{art}/detail.aspx"
    }
    url = f"https://basket-01.wbbasket.ru/vol{art[0:2]}/part{art[0:4]}/{art}/info/ru/card.json"
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        if response.status_code == 200:
            data = response.json()
            name = data.get("imt_name", " Название не найдено")
            info_product = data.get("grouped_options", "Инфорация не найдено")
            return name, info_product, art
        else:
            return None, None, art
    except Exception as e:
        print(f"Ошибка запроса info: {e}")
        return None, None, art

base_art = 5007120

for i in range(10): 
    art = str(base_art + random.randint(0, 500000))
    print(f"{art}")

    name, info, art = product_info(art)

    if name and info:
        price = random.randint(500, 20000)  
        c.execute("INSERT INTO products (name, haracteristici, art, price) VALUES (?, ?, ?, ?)",
                  (name, str(info), art, price))
        conn.commit()
        print(f"Save db: {name}, art: {art}, цена: {price}")
    else:
        print(f"Error!")

    time.sleep(1.5)

print("Все товары")
for row in c.execute("SELECT * FROM products"):
    print(row)

print("Товары без названия (id, name)")
for row in c.execute("SELECT id, name FROM products WHERE name IS NULL OR name = ''"):
    print(row)

print("Товары дешевле 10.000")
for row in c.execute("SELECT * FROM products WHERE price < 10000"):
    print(row)



conn.commit()
conn.close()






