# ============================================================
#
# 任務：登入 Quotes to Scrape 網站，爬取第一頁所有的名言，存成 quotes_all.csv 。
#       欄位：page、quote、author、tags（多個 tags 以 ; 串接）
#
# ============================================================
import logging
import sys
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

LOGIN_URL = "http://quotes.toscrape.com/login"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0 (W6 exercise)"}
ACCOUNT = {"username": "student", "password": "demo"}       # 練習站不檢查帳密

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("week_06_ex2_Quotes_login.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("week_06_exercise_2_Quotes_login")

session = requests.Session()
session.headers.update(HEADERS)      # 之後每一次 session.get() / session.post() 都會自動帶這組 headers

try:
    # Step 1: GET 登入頁，取出隱藏欄位 csrf_token；伺服器發的 cookie 存進 session
    resp = session.get(LOGIN_URL, timeout=10)
    resp.raise_for_status()
    token = BeautifulSoup(resp.text, "html.parser").select_one("input[name=csrf_token]")["value"]
    logger.info("GET /login：狀態碼 %s，Session 保存的 cookie：%s", resp.status_code, list(session.cookies.keys()))

    # Step 2: POST 登入：送出 csrf_token＋帳密，cookie 由 Session 自動帶回
    resp = session.post(LOGIN_URL, data={"csrf_token": token, **ACCOUNT}, timeout=10)
    resp.raise_for_status()
except requests.RequestException as e:                    # 網路錯誤：明確報錯、停止
    logger.error("請求失敗：%s", e)
    sys.exit(1)

# Step 3: 用頁面內容判斷是否登入成功（不能只看狀態碼）
soup = BeautifulSoup(resp.text, "html.parser")
if soup.select_one('a[href="/logout"]') is None:
    logger.error("登入失敗：頁面沒有 Logout 連結（狀態碼仍是 %s）", resp.status_code)
    sys.exit(1)
logger.info("登入成功：狀態碼 %s，轉址到 %s", resp.status_code, resp.url)

# Step 4: 擷取第一頁所有名言
rows = []
for card in soup.select("div.quote"):
    rows.append({
        "page": 1,
        "quote": card.select_one("span.text").get_text(strip=True),
        "author": card.select_one("small.author").get_text(strip=True),
        "tags": ";".join(t.get_text(strip=True) for t in card.select("a.tag")),
    })
if not rows:                                              # 抓不到資料要明確報錯，不能安靜結束
    logger.error("第一頁找不到任何 div.quote")
    sys.exit(1)
logger.info("第 1 頁：%s 句", len(rows))

# Step 5: 存檔
df = pd.DataFrame(rows)
CSV_PATH = Path(__file__).with_name("quotes_first_page.csv")
df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
logger.info("已存檔 %s：%s 筆", CSV_PATH.name, len(df))

# 驗收：抓到 ≠ 抓對
print(df.shape)                                   # (10, 4)
print("作者人數：", df["author"].nunique())        # 8
print(df.head(3).to_string(index=False))
