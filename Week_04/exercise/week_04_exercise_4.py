# ============================================================
# 
# 任務 1：利用 BeautifulSoup 的 find 系列方法，爬取全部 250 個國家，存成 countries.csv 。
#         欄位：name、capital、population、area_km2
# 任務 2：列出「人口數前五大」與「國土面積前五大」的國家
# 來源：https://www.scrapethissite.com/pages/simple/
#      
# ============================================================

import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/simple/"
HEADERS = {"User-Agent": "..."}

# Step 1：取得網頁 HTML 字串
resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()
html_text = resp.text

# Step 2：把 HTML 文字轉成 DOM 樹
soup = BeautifulSoup(html_text, "html.parser")
print("網頁標題：", soup.title.text)

#Step 3：用 find_all 找出所有國家卡片 
# find_all("標籤名", class_="class 名稱")
#   - class 是 Python 保留字，所以參數要寫成 class_（多一個底線）
#   - class_="country" 只要其中一個 class 是 country 就算（卡片是 class="col-md-4 country"）
cards = soup.find_all("div", class_="country")
print("共找到", len(cards), "個國家")         # 共找到 250 國家
if len(cards) == 0:
    raise RuntimeError("找不到國家卡片：請用 DevTools 重新確認網頁結構")

# Step 4：取出每個國家的資訊
countries = []
for card in cards:
    # card.find(...)：只在這張卡片裡找第一個符合的元素
    name = card.find("h3", class_="country-name").get_text(strip=True)
    capital = card.find("span", class_="country-capital").get_text(strip=True)
    population = card.find("span", class_="country-population").get_text(strip=True)
    area = card.find("span", class_="country-area").get_text(strip=True)

    countries.append({
        "name": name,
        "capital": capital,
        "population": int(population),     # 轉成整數才能排序
        "area_km2": float(area),           # 面積有小數，也有科學記號，例如 : 1.71E7
    })

# Step 5：存成 CSV 檔
df = pd.DataFrame(countries)
output_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries.csv")
df.to_csv(output_filepath, index=False, encoding="utf-8-sig")
print("[OK] 已存檔：", output_filepath, "共", len(df), "筆")

# Step 6：人口數前五大、國土面積前五大 
# nlargest(5, "欄位")：依該欄位由大到小，取前 5 筆（等同 sort_values(ascending=False).head(5)）
print("\n人口數前五大：")
print(df.nlargest(5, "population")[["name", "population"]].to_string(index=False))

print("\n國土面積前五大：")
print(df.nlargest(5, "area_km2")[["name", "area_km2"]].to_string(index=False))