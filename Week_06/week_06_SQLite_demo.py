# ============================================================
#
# SQLite 資料寫入、查詢、更新、刪除
#
# ============================================================
import logging
import sqlite3
from pathlib import Path

import pandas as pd

# Step 0: 設定 log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("w06_demo_SQLiteCRUD.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("w06_demo_SQLiteCRUD")

# Step 1: 連線 SQLite
#         若，資料庫名稱不存在，會建立一個以此為名稱的新資料庫。
DB_PATH = Path(__file__).with_name("books_demo.db")
conn = sqlite3.connect(DB_PATH)
logger.info("已連線 SQLite：%s", DB_PATH.name)

# Step 2: 建立資料表 books
#         SQL 指令 IF NOT EXISTS：已經存在就略過
#         PRIMARY KEY：主鍵欄位中的內容絕不能重複
conn.execute("""
    CREATE TABLE IF NOT EXISTS books (
        url    TEXT PRIMARY KEY,
        title  TEXT NOT NULL,
        price  REAL,
        rating INTEGER
    )
""")
logger.info("已建立資料表 books")

# Step 3: 寫入資料表
#         模擬已從 https://books.toscrape.com/ 上爬取到的資料  # (url, title, price, rating)
BOOKS = [ 
    ("catalogue/a-light-in-the-attic_1000/index.html", "A Light in the Attic", 51.77, 3),
    ("catalogue/tipping-the-velvet_999/index.html", "Tipping the Velvet", 53.74, 1),
    ("catalogue/soumission_998/index.html", "Soumission", 50.10, 1),
    ("catalogue/sharp-objects_997/index.html", "Sharp Objects", 47.82, 4),
    ("catalogue/sapiens-a-brief-history-of-humankind_996/index.html", "Sapiens: A Brief History of Humankind", 54.23, 5),
]
# ? 佔位符＋executemany 一次寫多筆；OR IGNORE 遇到重複主鍵就跳過
conn.executemany(
    "INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?)", 
    BOOKS
    )
conn.commit()
logger.info("已寫入資料表 books")


# ------------------------------------------------------------
# 補充 A：佔位符的兩種寫法（p.49）
#   用一個暫時的記憶體資料庫示範，不影響 books_demo.db
# ------------------------------------------------------------
demo = sqlite3.connect(":memory:")
demo.execute("CREATE TABLE books (url TEXT PRIMARY KEY, title TEXT NOT NULL, price REAL, rating INTEGER)")
url, title, price, rating = BOOKS[0]

# ? ＋ tuple（qmark style）：照「順序」對應，第 1 個值填第 1 個 ?
demo.execute(
    "INSERT INTO books VALUES (?, ?, ?, ?)",
    (url, title, price, rating),
)
# :名稱 ＋ dict（named style）：照「名字」對應，:price 拿 dict 的 "price"
url2, title2, price2, rating2 = BOOKS[1]
demo.execute(
    "INSERT INTO books VALUES (:url, :title, :price, :rating)",
    {"url": url2, "title": title2, "price": price2, "rating": rating2},
)
# 只寫入一個值的 tuple 要有逗號：(url, )
one = demo.execute("SELECT title FROM books WHERE url = ?", (url,)).fetchone()
logger.info("補充 A：兩種寫法都寫入成功，共 %s 筆；只帶一個值 (url, ) → %s",
            demo.execute("SELECT COUNT(*) FROM books").fetchone()[0], one)

# ? 的注意事項：順序寫錯不會報錯，資料會默默存錯
demo.execute("INSERT INTO books VALUES (?, ?, ?, ?)", ("u-wrong", 51.77, "A Light", 3))   # title 和 price 寫反
logger.info("補充 A：順序寫反 → %s", demo.execute(
    "SELECT title, price FROM books WHERE url = ?", ("u-wrong",)).fetchone())


# ------------------------------------------------------------
# 補充 B：為什麼要用佔位符（p.50）
# ------------------------------------------------------------
# (1) SQL 資料隱碼攻擊：f-string 拼 SQL，輸入的內容被當成 SQL 指令
#     投影片用 quotes 的作者示範；這裡改用 books 的書名，原理相同
#     （課堂可改成 name = input("要查哪本書？") 讓學生自己輸入）
for name in ["Sharp Objects", "' OR '1'='1"]:
    sql = f"SELECT title FROM books WHERE title = '{name}'"
    print(sql)      # 印出來看看拼成什麼
    rows = conn.execute(sql).fetchall()
    logger.info("補充 B (1) f-string 輸入 %r → %s 筆", name, len(rows))
# 改用 ? 佔位符：同樣的惡意輸入，只會被當成一個奇怪的書名
rows = conn.execute("SELECT title FROM books WHERE title = ?", ("' OR '1'='1",)).fetchall()
logger.info("補充 B (1) ? 佔位符輸入 \"' OR '1'='1\" → %s 筆", len(rows))

# (2) 單引號破壞結構：資料本身有單引號（例如 O'Connor）
author = "O'Connor"
try:
    demo.execute(f"INSERT INTO books VALUES ('u-oc', '{author}', 10.0, 3)")
except sqlite3.OperationalError as e:
    logger.info("補充 B (2) f-string 遇到 %s → OperationalError：%s", author, e)
demo.execute("INSERT INTO books VALUES (?, ?, ?, ?)", ("u-oc", author, 10.0, 3))
logger.info("補充 B (2) 改用 ? → 正常寫入 %s", author)

# (3) 缺值轉換錯誤：None 經過 f-string 變成文字 None，不是 SQL 的 NULL
missing_price = None
try:
    demo.execute(f"INSERT INTO books VALUES ('u-none', 'Some Book', {missing_price}, 3)")
except sqlite3.OperationalError as e:
    logger.info("補充 B (3) f-string 遇到 None → OperationalError：%s", e)
demo.execute("INSERT INTO books VALUES (?, ?, ?, ?)", ("u-none", "Some Book", missing_price, 3))
logger.info("補充 B (3) 改用 ? → price 存成 %s", demo.execute(
    "SELECT typeof(price) FROM books WHERE url = ?", ("u-none",)).fetchone()[0])
demo.close()


# Step 4: 擷取資料
# fetchall：全部取回 → list，每一列是 tuple（擷取四星以上的資訊）
rows = conn.execute(
    "SELECT title, price FROM books WHERE rating >= 4 ORDER BY price DESC").fetchall()
logger.info("擷取：4 星以上 → %s", rows)

# 逐列資料處理
for title, price in conn.execute(
        "SELECT title, price FROM books WHERE rating >= 4 ORDER BY price DESC"):
    logger.info("4 星以上  %s , %s", title, price)

# fetchone：只取一列 → 常用在 COUNT、AVG（計算資料筆數）
n = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
logger.info("目前寫入 %s 筆資料", n)

# read_sql_query( ) 查詢回來的資料型態為 DataFrame
df = pd.read_sql_query(
    "SELECT title, price, rating FROM books WHERE price > ? ORDER BY price DESC",
    conn, 
    params=(50,)
)
logger.info("價格 > 50 共 %s 本\n%s", len(df), df.to_string(index=False))


# Step 5: 更新資料
# Sharp Objects 從 47.82 降價到 45.00 —— 用主鍵 url 指定要改哪一筆
url = "catalogue/sharp-objects_997/index.html"
cur = conn.execute(
    "UPDATE books SET price = ? WHERE url = ?",
    (45.00, url)
)
conn.commit()   # 要 commit 才修改資料
logger.info("UPDATE：改了 %s 筆", cur.rowcount)

# 常見的 2 個錯誤：在一份「複本」上示範，不影響 books_demo.db
copy_db = sqlite3.connect(":memory:")
conn.backup(copy_db)                                  # 把目前的資料庫整份複製到記憶體
# 錯誤 1：沒有 WHERE → 整張表都被改
cur = copy_db.execute("UPDATE books SET price = ?", (45.00,))
logger.info("錯誤 1 沒有 WHERE：改了 %s 筆 → %s", cur.rowcount,
            copy_db.execute("SELECT DISTINCT price FROM books").fetchall())
copy_db.close()

# 錯誤 2：沒有 commit → 關閉後修改就不見
tmp = sqlite3.connect(DB_PATH)
tmp.execute("UPDATE books SET price = ? WHERE url = ?", (99.0, url))
logger.info("錯誤 2 沒有 commit：改完當下 → %s",
            tmp.execute("SELECT price FROM books WHERE url = ?", (url,)).fetchone()[0])
tmp.close()                                           # 沒有 commit 就關閉
logger.info("錯誤 2 沒有 commit：重新查詢 → %s（剛剛的修改不見了）",
            conn.execute("SELECT price FROM books WHERE url = ?", (url,)).fetchone()[0])

# Step 6: 刪除資料
# 刪除 rating 為 1 的資料 —— 執行前先用 SELECT 驗證，完全符合預期再刪除
targets = conn.execute("SELECT title FROM books WHERE rating = ?", (1,)).fetchall()
logger.info("DELETE 前確認：會刪掉 %s", targets)
cur = conn.execute("DELETE FROM books WHERE rating = ?", (1,))
conn.commit()   # 要 commit 才刪除資料
logger.info("DELETE：刪了 %s 筆，剩 %s 筆", cur.rowcount,
            conn.execute("SELECT COUNT(*) FROM books").fetchone()[0])

conn.close()
