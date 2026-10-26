# ============================================================
# 
# 任務：讀取 authors.csv 且回答下列問題
#       Q1  名言頭尾的彎引號 “ ” 去掉
#       Q2  統計各國有幾位作者
#       Q3  誰最早出生
#
# ============================================================
import re
from pathlib import Path

import pandas as pd

df = pd.read_csv(Path(__file__).with_name("authors.csv"))

# Q1 : 首頁 10 句名言是哪幾位作者說的？（10 句、8 位作者）
print("① 作者：", df["name"].unique().tolist(), "共", df["name"].nunique(), "位")

# Q2 : 名言頭尾的彎引號 “ ” 去掉：字元類 [“”] 配到引號，換成空字串
df["quote_clean"] = [re.sub(r"[“”]", "", q) for q in df["quote"]]
print("② 去引號前：", df.loc[0, "quote"][:40])
print("   去引號後：", df.loc[0, "quote_clean"][:40])

# Q3 : 統計各國有幾位作者：同一位作者只算一次，國家＝出生地最後一段（$ 限定結尾）
authors = df.drop_duplicates("name").copy()
authors["country"] = [re.findall(r"[A-Z][^,]*$", loc)[0] for loc in authors["born_location"]]
print("③ 各國作者數：")
print(authors["country"].value_counts().to_string())

# Q4 : 誰最早出生？born_date 是字串，先用 \d{4} 取出年份、轉成 int 才能比大小
authors["born_year"] = [int(re.findall(r"\d{4}", b)[0]) for b in authors["born_date"]]
oldest = authors.loc[authors["born_year"].idxmin()]
print("④ 最早出生：", oldest["name"], oldest["born_year"])