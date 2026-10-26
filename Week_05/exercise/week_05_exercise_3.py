# ============================================================
# 
# 任務：讀取 authors.csv 且利用「字元類」完成下列分析
#       (1) born_date 的所有數字
#       (2) born_location 的所有大寫字母
#       (3) tags 裡所有「不是小寫字母」的字元
#       (4) quote 裡的標點：不是字、也不是空白
#
# ============================================================
import re
from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).with_name("authors.csv"))
row = df.iloc[0]                       # 第一列：Albert Einstein
born, loc, tags, quote = row["born_date"], row["born_location"], row["tags"], row["quote"]

print("①", re.findall(r"[0-9]", born))        # born_date 的所有數字（也可寫 \d）
print("②", re.findall(r"[A-Z]", loc))         # born_location 的所有大寫字母
print("③", re.findall(r"[^a-z]", tags))       # tags 裡所有「不是小寫字母」的字元
print("④", re.findall(r"[^\w\s]", quote))     # quote 裡的標點：不是字、也不是空白