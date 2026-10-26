# ============================================================
# 
# 任務：爬取 Quotes to Scrape 首頁各名言與作者資訊，且將資訊存成 authors.csv 
#      欄位：name、born_date、born_location、quote、tags、description 
# 來源：http://quotes.toscrape.com/ 
#      
# ============================================================
import os
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/"
HEADERS = {"User-Agent": "..."}

# 送出請求並回傳 BeautifulSoup；失敗就直接報錯
def get_soup(url):
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# Step 1：抓首頁，找出每一張名言卡片
home = get_soup(URL)
cards = home.select("div.quote")
print(f"[Step 1] 首頁找到 {len(cards)} 張名言卡片")

# Step 2：逐張卡片取出名言、標籤、作者頁連結
authors = {}   # 作者頁網址 → 作者資訊；同一位作者只抓一次（Einstein 有 3 句）
rows = []
for card in cards:
    quote = card.select_one("span.text").get_text(strip=True)
    tags = ";".join(t.get_text(strip=True) for t in card.select("a.tag"))   
    href = card.select_one("span a").get("href")       
    link = urljoin(URL, href)                            

    # Step 3：作者頁（沒抓過才抓）
    if link not in authors:
        page = get_soup(link)
        authors[link] = {
            "name": page.select_one("h3.author-title").get_text(strip=True),
            "born_date": page.select_one("span.author-born-date").get_text(strip=True),
            "born_location": page.select_one("span.author-born-location").get_text(strip=True),
            "description": page.select_one("div.author-description").get_text(strip=True),
        }
        print(f"[Step 3] 抓作者頁：{authors[link]['name']}")
        time.sleep(0.5)                                   

    # Step 4：組成一列（作者資訊 ＋ 這句名言）
    rows.append({**authors[link], "quote": quote, "tags": tags})

# Step 5：存成 CSV 檔
df = pd.DataFrame(rows)
output_filepath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "authors.csv"
)
df.to_csv(output_filepath, index=False, encoding="utf-8-sig")   
print("[OK] 已存檔：", output_filepath, "共", len(df), "筆")