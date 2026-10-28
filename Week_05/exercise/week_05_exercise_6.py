# ============================================================
#
# 任務：爬取 Albert Einstein 作者頁，取出生年、介紹提到的年份、去世年、享年
# 
# ============================================================
import re

import requests
from bs4 import BeautifulSoup

URL = "http://quotes.toscrape.com/author/Albert-Einstein/"
HEADERS = {"User-Agent": "..."}

# 爬取 Albert Einstein 作者頁面 
resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# 取得出生日期與介紹文字
born_text = soup.select_one("span.author-born-date").get_text(strip=True)
desc = soup.select_one("div.author-description").get_text(strip=True)
print("born_text =", repr(born_text))
print("desc =", repr(desc[:30] + " …"), f"（共 {len(desc)} 字）")

# 字串處理：re.findall 
born = int(re.findall(r"\d{4}", born_text)[0])                      # ① 剛好 4 個數字＝年份
print("①", born)

years = sorted(set(re.findall(r"\b\d{4}\b", desc)))                 # ② set 去重複，sorted 排序
print("②", years)

death_part = re.findall(r"death in \d{4}", desc)[0]                 # ③ 先縮小範圍：'death in 1955'
died = int(re.findall(r"\d{4}", death_part)[0])                     # 再從這一小段取數字
print("③", died, "   ← 對照 max(years) =", max(years), "（2008 是引用文章的日期，不是去世年）")

print("④", died - born)                                             # ④ 享年：轉成 int 才能相減