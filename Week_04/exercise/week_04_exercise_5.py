# ============================================================
# 
# 任務：利用 BeautifulSoup 的 select 系列方法，爬取 14 種烏龜家族的資訊，存成 turtles.csv
#       欄位：family、common_name、discovered_year、discovered_by、image_url
# 來源：https://www.scrapethissite.com/pages/frames/
#       
# 重點：① iframe：畫面上看得到的內容，其實來自另一個網址
#       ② 兩層爬取：列表頁 → 每一家族的詳細頁
#
# ============================================================
import os
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/frames/"
HEADERS = {"User-Agent": "..."}

# Step 1：取得網頁 HTML 字串
resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()
html_text = resp.text

# Step 2：把 HTML 文字轉成 DOM 樹
soup = BeautifulSoup(html_text, "html.parser")
print("網頁標題：", soup.title.text)

# Step 3：找出 iframe 的「真正資料網址」 
iframe = soup.select_one("iframe")
if iframe is None:
    raise RuntimeError("找不到 <iframe>：請用 DevTools 重新確認網頁結構")

list_url = urljoin(URL, iframe.get("src"))
print("iframe 的真正網址：", list_url)

# 烏龜卡片在 iframe 的網址裡，所以要對 list_url 再送一次請求，並重建 soup
resp = requests.get(list_url, headers=HEADERS, timeout=10)
resp.raise_for_status()
html_text = resp.text
soup = BeautifulSoup(html_text, "html.parser")

# Step 4：用「第一張」烏龜卡片，確認選擇器是否正確
#   用 DevTools 觀察：每個家族是一張 <div class="col-md-4 turtle-family-card">
first_card = soup.select_one("div.turtle-family-card")
if first_card is None:
    raise RuntimeError("找不到 div.turtle-family-card：請確認是否已改用 iframe 的網址")
print("\n第一張卡片的 HTML：")
print(first_card.prettify())

# Step 5：從第一張卡片中取出各欄位，確認選擇器是否正確
family = first_card.select_one(".family-name").get_text(strip=True)
image_url = first_card.select_one("img").get("src")         # 取屬性：圖片網址
detail_href = first_card.select_one("a").get("href")        # 取屬性：詳細頁連結（相對路徑）
print("\n第一筆：", family, detail_href)                     # Carettochelyidae /pages/frames/?frame=i&family=...


# Step 6：找所有的烏龜卡片
cards = soup.select("div.turtle-family-card")
print("共找到 %d 張烏龜卡片" % len(cards))     # 共找到 14 張烏龜卡片

# Step 7：取出每個烏龜卡片的資訊，且存成一個 dict 
turtles = []
skipped = 0
for i, card in enumerate(cards, start=1):
    # ---- 第一層（列表頁）：家族名稱、圖片網址、詳細頁網址 ----
    family = card.select_one(".family-name").get_text(strip=True)
    image_url = card.select_one("img").get("src")
    detail_url = urljoin(list_url, card.select_one("a").get("href"))

    # ---- 第二層（詳細頁）：俗名、發現年份、發現者 ----
    detail_resp = requests.get(detail_url, headers=HEADERS, timeout=10)
    detail_resp.raise_for_status()
    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
    detail = detail_soup.select_one("div.turtle-family-detail")

    common_name = detail.select_one(".common-name").get_text(strip=True)

    # 年份與發現者「沒有自己的標籤」，只是一段文字的一部分：
    #   "... more commonly known as "Pig-nosed turtle" — were first discovered in 1887 by Boulenger."
    # 用字串方法（W2）切出來；W5 會改用正規表達式，更穩健
    lead = detail.select_one("p.lead").get_text(" ", strip=True)
    year_and_by = lead.split("discovered in ")[1].rstrip(".")   # → "1887 by Boulenger"
    year, discovered_by = year_and_by.split(" by ")             # → "1887", "Boulenger"

    turtles.append({
        "family": family,
        "common_name": common_name,
        "discovered_year": int(year),
        "discovered_by": discovered_by,
        "image_url": image_url,
    })
    print("(%d/%d) 取得詳細頁：%s" % (i, len(cards), family))
    time.sleep(1)   # 禮貌爬取：每進一個詳細頁就休息 1 秒（W6 會詳談）

# Step 8：存成 CSV 
df = pd.DataFrame(turtles)
output_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "turtles.csv")
df.to_csv(output_filepath, index=False, encoding="utf-8-sig")
print("\n[OK] 已存檔：", output_filepath, "共", len(df), "筆")
