# ============================================================
#
# 任務：讀取 authors.csv 且利用「字元類＋量詞」完成下列分析
#      (1) born_date 的完整年份
#      (2) born_date 的月份
#      (3) born_location 的每一個英文單字
#      (4) tags 裡的標籤（包含 - 的字串）
# 
# ============================================================
import re
from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).with_name("authors.csv"))
row = df.iloc[0]                       # 第一列：Albert Einstein
born, loc, tags = row["born_date"], row["born_location"], row["tags"]

print("①", re.findall(r"\d{4}", born))           # 完整年份： 4 個數字組合
print("②", re.findall(r"[A-Z][a-z]+", born))     # 月份：大寫開頭＋一個以上小寫
print("③", re.findall(r"[A-Za-z]+", loc))        # 出生地的每一個英文單字
print("④", re.findall(r"[a-z-]+", tags))         # 標籤：方括號內放 -，deep-thoughts 不會被拆開

# 延伸：套用到整欄，每位作者的出生年份
df["born_year"] = [int(re.findall(r"\d{4}", b)[0]) for b in df["born_date"]]
print(df[["name", "born_year"]].drop_duplicates().to_string(index=False))