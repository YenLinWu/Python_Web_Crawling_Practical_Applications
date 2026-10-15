# ============================================================
#
# 任務：利用 BeautifulSoup 的 select 系列方法，爬取冰球隊伍統計表，存成 hockey_teams.csv
# 來源：https://www.scrapethissite.com/pages/forms/
#
# ============================================================

import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/forms/"
HEADERS = {"User-Agent": "..."}

# Step 1：取得網頁 HTML 字串
resp = requests.get(URL, headers=HEADERS, timeout=10)
resp.raise_for_status()                       # 狀態碼不是 2xx 就直接報錯停止
html_text = resp.text

# Step 2：把 HTML 文字轉成 DOM 樹
soup = BeautifulSoup(html_text, "html.parser")
print("網頁標題：", soup.title.text)

# Step 3：用「第一列」隊伍資料，確認選擇器是否正確
# 用 DevTools 觀察：每支隊伍是一個 <tr class="team">，
# 每一格 <td> 都有自己的 class：name、year、wins、losses、ot-losses、pct、gf、ga、diff
first_row = soup.select_one("tr.team")
print("\n第一列的 HTML：")
print(first_row.prettify())

# 在第一列資料中找各欄位資訊
name = first_row.select_one("td.name").get_text(strip=True)
year = first_row.select_one("td.year").get_text(strip=True)
wins = first_row.select_one("td.wins").get_text(strip=True)
print("\n第一筆：", name, year, wins)        # Boston Bruins 1990 44

# Step 4：找所有的隊伍資料列
rows = soup.select("tr.team")
print("\n共找到", len(rows), "列隊伍資料")    # 共找到 25 列隊伍資料
if len(rows) == 0:
    raise RuntimeError("找不到 tr.team：請用 DevTools 重新確認網頁結構")

# Step 5：取出每一列的資訊，且存成一個 dict
teams = []
for row in rows:
    teams.append({
        "team_name": row.select_one("td.name").get_text(strip=True),
        "year": int(row.select_one("td.year").get_text(strip=True)),
        "wins": int(row.select_one("td.wins").get_text(strip=True)),
        "losses": int(row.select_one("td.losses").get_text(strip=True)),
        "ot_losses": row.select_one("td.ot-losses").get_text(strip=True),   # OT Losses 在 1990 年代是空白格（''）
        "win_pct": float(row.select_one("td.pct").get_text(strip=True)),
        "goals_for": int(row.select_one("td.gf").get_text(strip=True)),
        "goals_against": int(row.select_one("td.ga").get_text(strip=True)),
        "diff": int(row.select_one("td.diff").get_text(strip=True)),  
    })

# Step 6：list[dict] → DataFrame → CSV
df = pd.DataFrame(teams)
output_filepath = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hockey_teams.csv"
)
df.to_csv(output_filepath, index=False, encoding="utf-8-sig")   
print("[OK] 已存檔：", output_filepath, "共", len(df), "筆")