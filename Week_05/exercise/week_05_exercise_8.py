# ============================================================
#
# 任務：利用具名分組分析 w05.log
#      (1) 每一行拆成 dict 
#      (2) 把 dict 轉成 DataFrame 
#      (3) 統計各等級筆數、列出所有 ERROR 訊息
#
# ============================================================
import re
from pathlib import Path

import pandas as pd

LOG_PATH = Path(__file__).with_name("w05.log")
LOG = r"(?P<level>[A-Z]+) (?P<date>\d{4}-\d{2}-\d{2}): (?P<message>.+)"

with open(LOG_PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()          # 一行一筆，已去掉結尾的 \n

rows = []
for line in lines:
    m = re.fullmatch(LOG, line)            # 整行都要符合格式
    if m is None:                          # 匹配不到 → None，先判斷再取值
        print("[SKIP]", line)
        continue
    rows.append(m.groupdict())             # {'level': ..., 'date': ..., 'message': ...}

print("①", rows[3])                        # {'level': 'ERROR', 'date': '2026-10-20', 'message': 'Connection timed out'}

df = pd.DataFrame(rows)                    # list[dict] → DataFrame，key 自動變欄位名稱
print("②", df.shape)                       # (5, 3)
print(df)

print("③", df["level"].value_counts().to_dict())          # 各等級筆數
print("  ", df[df["level"] == "ERROR"]["message"].tolist())  # 所有 ERROR 的訊息
