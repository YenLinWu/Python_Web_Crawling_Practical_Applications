# ============================================================
#
# 任務：從 quotes_sqlite.db 中，擷取出下列資訊
#       Q1：資料表共幾句名言、幾位作者
#       Q2：用 ? 查出 author = "Albert Einstein" 有幾句，並印出前 3 句（fetchall）
#       Q3：用 for 迴圈印出：句數最多的前 5 位作者
#       Q4：用 pd.read_sql_query 查詢出「tag 含 love」的名言共幾句？
#       答案用 logging 記錄到 week_06_ex10_Quotes_select.log
#
# ============================================================
import logging
import sqlite3
import sys
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).with_name("quotes_sqlite.db")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("week_06_exercise_10.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("week_06_exercise_10_Quotes_select")

# 確認資料庫存在（sqlite3.connect 遇到不存在的檔案會「新建一個空的」，不會報錯）
if not DB_PATH.exists():
    logger.error("找不到 %s，請先執行課堂練習 - 9", DB_PATH.name)
    sys.exit(1)
conn = sqlite3.connect(DB_PATH)

# Q1: fetchone —— 只有一列答案
total, authors = conn.execute("SELECT COUNT(*), COUNT(DISTINCT author) FROM quotes").fetchone()
logger.info("Q1 : 共 %s 句名言、%s 位作者", total, authors)

# Q2: ? 帶入作者名稱，fetchall 取回全部
author = "Albert Einstein"
rows = conn.execute("SELECT quote FROM quotes WHERE author = ? ORDER BY page", (author,)).fetchall()
logger.info("Q2 : %s 共 %s 句，前 3 句：", author, len(rows))
for (quote,) in rows[:3]:                       # 每一列是只有一個元素的 tuple
    logger.info("   %s", quote[:60])

# Q3: 利用 for 迴圈查詢句數最多的前 5 位作者
logger.info("Q3 : 句數最多的前 5 位作者：")
for name, n in conn.execute("""
        SELECT author, COUNT(*) AS n FROM quotes
        GROUP BY author ORDER BY n DESC, author LIMIT 5"""):
    logger.info("   %-16s %s", name, n)

# Q4: tag 含 love 的名言有幾句?
loose = pd.read_sql_query("SELECT quote, tags FROM quotes WHERE tags LIKE ?", conn, params=("%love%",))
exact = pd.read_sql_query(
    "SELECT quote, tags FROM quotes WHERE ';' || tags || ';' LIKE ?",   # 前後補上 ; 再比對「;love;」
    conn, params=("%;love;%",),
)
logger.info("Q4 : tags LIKE '%%love%%'：%s 句；精確比對 love：%s 句", len(loose), len(exact))
extra = loose[~loose["quote"].isin(exact["quote"])]
logger.info("   多算的：%s", extra["tags"].tolist())
conn.close()
