# ============================================================
#
# 任務：登入 Quotes to Scrape 網站，爬取所有頁的名言，存成 quotes_all.csv
#       欄位：page、quote、author、tags（多個 tags 以 ; 串接）
#       另外，利用 logging 記錄爬取過程，記錄每頁抓到幾句名言，log 存成 week_06_ex3_Quotes_login.log
#
# ============================================================
import logging
import random
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE = "http://quotes.toscrape.com"
LOGIN_URL = f"{BASE}/login"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0 (W6 exercise)"}
ACCOUNT = {"username": "student", "password": "demo"}       # 練習站不檢查帳密
MAX_PAGES = 50                       

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("week_06_ex3_Quotes_login.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("week_06_exercise_3_Quotes_login")

session = requests.Session()
session.headers.update(HEADERS)      # 之後每一次 session.get() / session.post() 都會自動帶這組 headers

logger.info("開始爬取 %s", LOGIN_URL)
try:
    # Step 1: GET 登入頁，取出隱藏欄位 csrf_token；伺服器發的 cookie 存進 session
    resp = session.get(LOGIN_URL, timeout=10)
    resp.raise_for_status()
    token = BeautifulSoup(resp.text, "html.parser").select_one("input[name=csrf_token]")["value"]
    logger.info("GET /login：狀態碼 %s，Session 保存的 cookie：%s", resp.status_code, list(session.cookies.keys()))

    time.sleep(random.uniform(2, 6))                      # 網路禮儀：兩次請求之間隨機等待

    # Step 2: POST 登入：送出 csrf_token＋帳密，cookie 由 Session 自動帶回
    resp = session.post(LOGIN_URL, data={"csrf_token": token, **ACCOUNT}, timeout=10)
    resp.raise_for_status()
    logger.info("POST /login：狀態碼 %s，轉址到 %s", resp.status_code, resp.url)
except requests.RequestException as e:                    # 網路錯誤：明確報錯、停止
    logger.error("請求失敗：%s", e)
    sys.exit(1)

# Step 3: 用頁面內容判斷是否登入成功（不能只看狀態碼）
soup = BeautifulSoup(resp.text, "html.parser")
if soup.select_one('a[href="/logout"]') is None:
    logger.error("登入失敗：頁面沒有 Logout 連結")
    sys.exit(1)
logger.info("登入成功")

# Step 4: 登入狀態下逐頁爬取所有名言（同一個 session，cookie 自動帶著，每一頁都是登入後的內容）
rows = []
page = 1
while page <= MAX_PAGES:
    time.sleep(random.uniform(2, 6))                      # 網路禮儀：每頁之間隨機等待
    url = f"{BASE}/page/{page}/"
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:                # 網路錯誤：明確報錯、停止
        logger.error("第 %s 頁請求失敗：%s", page, e)
        sys.exit(1)
    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select("div.quote")
    if not cards:                                         # 停止條件：沒有名言了（狀態碼仍是 200，不能只看狀態碼）
        logger.info("第 %s 頁沒有資料，停止", page)
        break

    for card in cards:
        rows.append({
            "page": page,
            "quote": card.select_one("span.text").get_text(strip=True),
            "author": card.select_one("small.author").get_text(strip=True),
            "tags": ";".join(t.get_text(strip=True) for t in card.select("a.tag")),
        })
    logger.info("第 %s 頁：%s 句（累計 %s 句）", page, len(cards), len(rows))
    page += 1
    time.sleep(random.uniform(2, 6))

if page > MAX_PAGES:                                      # 不是因為「沒有資料」而停，而是保險絲斷了
    logger.warning("達到 MAX_PAGES=%s，資料可能沒抓完，請檢查停止條件或網站是否改版", MAX_PAGES)
if not rows:                                              # 抓不到資料要明確報錯，不能安靜結束
    logger.error("找不到任何 div.quote")
    sys.exit(1)

# Step 5: 存檔
df = pd.DataFrame(rows)
CSV_PATH = Path(__file__).with_name("quotes_all.csv")
df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
logger.info("已存檔 %s：%s 筆", CSV_PATH.name, len(df))

# 驗收：抓到 ≠ 抓對
print(df.shape)                                   # (100, 4)
print("每頁筆數：", df["page"].value_counts().sort_index().tolist())   # 10 頁 × 10 句
print("作者人數：", df["author"].nunique())        # 50
print(df.head(3).to_string(index=False))
