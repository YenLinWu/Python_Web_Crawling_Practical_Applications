# ============================================================
#
# 任務：讀取 authors.csv 且利用「中介字元」完成下列分析
#      (1) born_date 的日期
#      (2) born_date 的月份
#      (3) born_location 的最後一個地名
#      (4) name 的縮寫
#
# ============================================================
import re
from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).with_name("authors.csv"))


def first_row(name):
    """依作者姓名取出第一筆資料"""
    return df[df["name"] == name].iloc[0]

einstein = first_row("Albert Einstein")
monroe = first_row("Marilyn Monroe")
rowling = first_row("J.K. Rowling")

born = einstein["born_date"]                               # 'March 14, 1879'
print("①", re.findall(r"\b\d{1,2}\b", born))               # ['14']；沒加 \b 會得到 ['14', '18', '79']
print("②", re.findall(r"^[A-Z][a-z]+", born))              # ['March']；^ 只看字串開頭
print("③", re.findall(r"[A-Z][^,]*$", einstein["born_location"]),   # ['Germany']
      "／", re.findall(r"[A-Z][^,]*$", monroe["born_location"]))     # ['The United States']（沒有逗號也對）
print("④", re.findall(r"[A-Z]\.", rowling["name"]))       # ['J.', 'K.']；沒跳脫會多抓到 'Ro'

# 對照：
print("   沒加 \\b：", re.findall(r"\d{1,2}", born))
print("   沒跳脫：", re.findall(r"[A-Z].", rowling["name"]))