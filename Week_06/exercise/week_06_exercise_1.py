# ============================================================
#
# 任務：爬取 Quotes to Scrape 網站全部名言，且存成 quotes_all.csv。
#       欄位名稱：page、quote、author、tags（tags 以 ; 串接）
#
# ============================================================

import random
import time
# if __name__ == "__main__":
#     time.sleep(random.uniform(1, 3))

import logging

from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"
HEADERS = {"User-Agent": "..."}
CSV_PATH = Path(__file__).with_name("quotes_all.csv")
MAX_PAGES = 50                       #  避免無限迴圈

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("week_06_ex1_Quotes_all.log"), encoding="utf-8"),   
        logging.StreamHandler()                            # log 資訊同時顯示在 CMD 或終端機
    ],
)
logger = logging.getLogger("w06_ex1_Quotes")

session = requests.Session()
session.headers.update(HEADERS)      # 之後每一次 session.get() 都會自動帶這組 headers

logger.info("開始爬取 %s（每頁間隔 2-6 秒，全站約 10 頁，約 10-60 秒）", BASE_URL)
rows = []
page = 1
while page <= MAX_PAGES:
    url = f"{BASE_URL}/page/{page}/"
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select("div.quote")
    if not cards:                    # 停止條件：沒有內容（狀態碼仍是 200，不能只看狀態碼）
        logger.info("第 %s 頁沒有資料，停止", page)
        break

    for card in cards:
        rows.append({
            "page": page,
            "quote": card.select_one("span.text").get_text(strip=True),
            "author": card.select_one("small.author").get_text(strip=True),
            "tags": ";".join(t.get_text(strip=True) for t in card.select("a.tag")),
        })
    logger.info("第 %s 頁：%s 句", page, len(cards))
    page += 1
    time.sleep(random.uniform(2, 6))                    
    
if page > MAX_PAGES:                 # 非因「沒有資料」而停止爬取
    logger.warning("達到 MAX_PAGES=%s，資料可能沒抓完，請檢查停止條件或網站是否改版", MAX_PAGES)

df = pd.DataFrame(rows)
df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
logger.info("已存檔 %s：%s 筆", CSV_PATH.name, len(df))

# 驗收：抓到 ≠ 抓對
print(df.shape)                                   # (100, 4)
print("不重複名言：", df["quote"].nunique())       # 100
print("作者人數：", df["author"].nunique())        # 50
