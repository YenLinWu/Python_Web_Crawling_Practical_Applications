# ============================================================
#
# 任務：爬取 Quotes to Scrape 網站每一頁所有的名言，且將相關資訊寫入 SQLite 資料庫中。
# 
# ============================================================
import logging
import re
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

BASE = "http://quotes.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0 (W6 exercise)"}
DB_PATH = Path(__file__).with_name("quotes_sqlite.db")
MAX_PAGES = 50                       
SLEEP_SECONDS = 1                    # 禮貌爬取：每頁之間停 1 秒

# Step 0: 設定 log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("week_06_exercise_9.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("week_06_exercise_9_Quotes_sqlite")

# Step 1: 連線 SQLite、建立資料表
conn = sqlite3.connect(DB_PATH)
conn.execute("""
    CREATE TABLE IF NOT EXISTS quotes (
        quote      TEXT PRIMARY KEY,     -- 名言本身不會重複 → 當主鍵
        author     TEXT NOT NULL,
        tags       TEXT,                 -- 多個 tag 以 ; 串接
        page       INTEGER,
        scraped_at TEXT                  -- 爬取時間（ISO 8601 文字）
    )
""")
logger.info("已連線 SQLite：%s，資料表 quotes 準備好", DB_PATH.name)

session = requests.Session()
session.headers.update(HEADERS)     

try:
    # Step 2: 查詢 robots.txt（requests 下載 → RobotFileParser 判讀）
    robots_url = urljoin(BASE, "/robots.txt")
    resp = session.get(robots_url, timeout=10)
    logger.info("robots.txt 狀態碼：%s", resp.status_code)
    if 200 <= resp.status_code < 300:            # 有 robots.txt：依規則判斷
        rp = RobotFileParser()
        rp.parse(resp.text.splitlines())
        allowed = rp.can_fetch(HEADERS["User-Agent"], BASE)
    elif 400 <= resp.status_code < 500:          # 4xx（例如 404 沒有 robots.txt）：依 RFC 9309 視為全部允許
        allowed = True
    else:                                        # 其他（例如 5xx）：保守起見視為禁止
        allowed = False

    if not allowed:
        logger.error("robots.txt 不允許爬取 %s，停止", BASE)
        conn.close()
        sys.exit(1)
    logger.info("robots.txt 檢查：允許爬取 %s", BASE)

    # Step 3: while 迴圈翻頁
    page = 1
    inserted_total = 0                   # 本次總共新增幾筆
    quote_with_apostrophe = 0            # 含單引號 ' 的名言或作者（第 50 頁會用到）
    while page <= MAX_PAGES:
        url = urljoin(BASE, f"/page/{page}/")
        resp = session.get(url, timeout=10)
        logger.info("第 %s 頁 狀態碼 %s：%s", page, resp.status_code, url)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("div.quote")
        if not cards:                    # 停止條件：狀態碼仍是 200，但這一頁沒有名言
            logger.info("第 %s 頁沒有資料，停止", page)
            break

        # Step 4: 解析這一頁的每一句名言，整理成 tuple，順序對應資料表欄位
        now = datetime.now().isoformat(timespec="seconds")       # 爬取時間，例如 : '2026-11-24T20:30:40'
        rows = []
        for card in cards:
            text = card.select_one("span.text").get_text(strip=True)
            quote = re.sub(r'^[“"]|[”"]$', "", text)              # 去掉前後的 “ ”
            author = card.select_one("small.author").get_text(strip=True)
            tags = ";".join(t.get_text(strip=True) for t in card.select("a.tag"))
            rows.append((quote, author, tags, page, now))
            if "'" in quote or "'" in author:
                quote_with_apostrophe += 1

        # Step 5: 寫入 SQLite（重複的主鍵自動跳過），每頁 commit 一次
        cur = conn.executemany("INSERT OR IGNORE INTO quotes VALUES (?, ?, ?, ?, ?)", rows)
        conn.commit()
        inserted_total += cur.rowcount
        logger.info("第 %s 頁：抓到 %s 句、新增 %s 筆", page, len(rows), cur.rowcount)

        page += 1
        time.sleep(SLEEP_SECONDS)

    if page > MAX_PAGES:                
        logger.warning("達到 MAX_PAGES=%s，資料可能沒抓完", MAX_PAGES)

except requests.RequestException as e:
    logger.error("請求失敗：%s", e)
    conn.close()
    sys.exit(1)

# Step 6: 檢核驗收
total = conn.execute("SELECT COUNT(*) FROM quotes").fetchone()[0]
authors = conn.execute("SELECT COUNT(DISTINCT author) FROM quotes").fetchone()[0]
logger.info("本次新增 %s 筆；資料表共 %s 筆、%s 位作者", inserted_total, total, authors)
logger.info("觀察：本次爬到的名言或作者中，有 %s 句含單引號 '（下一段會用到）", quote_with_apostrophe)
conn.close()
