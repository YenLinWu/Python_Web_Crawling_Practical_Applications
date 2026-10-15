# W4 課堂練習 - 1（參考解）：DevTools 偵探 —— 找出國家列表每個欄位的 CSS selector
# 用法：把你在 DevTools 找到的 selector 填進 SELECTORS，執行後自動檢查「每個欄位都抓到 250 筆」
import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/simple/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0 (W4 exercise)"}

SELECTORS = {
    "國家卡片": "?",
    "國名": "?",
    "首都": "?",
    "人口": "?",
    "面積": "?"
}

resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

for field, selector in SELECTORS.items():
    found = soup.select(selector)
    status = "[OK]" if len(found) == 250 else "[CHECK]"
    sample = found[0].get_text(" ", strip=True)[:40] if found else "(沒抓到)"
    print(f"{status} {field:<5} {selector:<22} 抓到 {len(found):>3} 筆，第一筆 = {sample}")
