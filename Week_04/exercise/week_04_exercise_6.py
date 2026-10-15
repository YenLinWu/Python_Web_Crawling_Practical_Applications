# 來源：https://books.toscrape.com/ （爬蟲練習用虛構書店）

import requests
from bs4 import BeautifulSoup

URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "..."}

resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()
soup = BeautifulSoup(resp.content, "html.parser")

cards = soup.select("article.product_pod")
if len(cards) == 0:
    raise RuntimeError("找不到 article.product_pod：請用 DevTools 重新確認網頁結構")

for card in cards[:5]:
    link = card.select_one("h3 a")
    shown = link.get_text(strip=True)   # 畫面上的書名（可能被截斷）
    full = link.get("title")            # 完整書名藏在 title 屬性
    print(f"{shown:<30} → {full}")
