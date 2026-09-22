import os
from io import StringIO

import requests
import pandas as pd

URL = "https://zh.wikipedia.org/wiki/臺灣行政區人口列表"   
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0"
    }

resp = requests.get(URL, headers=HEADERS)
resp.raise_for_status()                      
print(f"{URL}（狀態碼 {resp.status_code}）")
html = resp.text                            

tables = pd.read_html(StringIO(html))
df = tables[0]                                

base = os.path.join(os.path.dirname(__file__), "output")
df.to_csv(base + ".csv", index=False, encoding="utf-8-sig")   
df.to_excel(base + ".xlsx", index=False)   