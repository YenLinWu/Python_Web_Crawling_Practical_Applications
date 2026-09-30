import os
from io import StringIO

from datetime import date
import requests
import pandas as pd

URL = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'  
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0'
    }

# 發送 HTTP GET 請求
resp = requests.get(URL, headers=HEADERS)
resp.raise_for_status()                      
print(f"{URL}（狀態碼 {resp.status_code}）")

# 取得網頁 HTML 原始碼
html = resp.text      

# 解析 HTML 取得所有資料表格
tables = pd.read_html(StringIO(html))

# 取得第一個資料表格
df = tables[0]                                

# 檢查欄名型態
print('欄名型態：', type(df.columns).__name__)   # -> MultiIndex 

# 檢查每個欄名是否為 tuple 元組
print('\n檢查每個欄名是否為 tuple 元組：')
for c in df.columns:
    print(repr(c), isinstance(c, tuple)) # 每個欄名都是「tuple 元組」

# 將 DataFrame 轉成 numpy 陣列
df_arr = df.values   

# 去掉第一列(因為已經設為欄位名稱)，且保留前五欄
df_arr = df_arr[1:, :5]  

# 將 numpy 陣列轉回 DataFrame，且重新命名欄位名稱
df_ = pd.DataFrame(df_arr)
df_.columns = ['幣別', '現金匯率_本行買入', '現金匯率_本行賣出', '即期匯率_本行買入', '即期匯率_本行賣出']

# 利用正規表示法，將「幣別」欄位中的重複文字去掉，只保留第一段文字
df_['幣別'] = df_['幣別'].replace(r'(\w+).+?\1', r'\1', regex=True)

# 寫入 csv 檔
output_filepath = os.path.join(os.path.dirname(__file__), date.today().strftime("%Y%m%d") + "_output.csv")
df_.to_csv(output_filepath, index=False, encoding="utf-8-sig")