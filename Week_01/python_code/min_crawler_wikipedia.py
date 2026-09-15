# min_crawler_wikipedia.py 利用 pandas 的 read_html 將網頁「表格」抓成資料表
# 
#   1) 給一個網址
#   2) 取得網頁內容
#   3) 解析出要的資料
#   4) 存下來 / 看結果
#
# --------------------------------------------------------------

import os
import sys
from io import StringIO
import requests
import pandas as pd

# 1) 給一個網址（維基百科的臺灣行政區人口表；採 CC BY-SA 授權，可自由使用、需標示來源）
URL = "https://zh.wikipedia.org/wiki/臺灣行政區人口列表"

# 有些網站看到「不像瀏覽器」的請求會擋掉，所以我們附上一個瀏覽器的身分（User-Agent）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0"
}


def get_html():
    """步驟 2：取得網頁內容。
    成功回傳 (html文字, 資料來源說明)；
    失敗就印出「真正的原因」並回傳 None——不使用任何假資料。"""
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=20)
        resp.raise_for_status()          # 狀態碼不是 200 就丟出錯誤
        print(f"[OK] 已從網路取得：{URL}（狀態碼 {resp.status_code}）")
        return resp.text, f"線上維基：{URL}"
    except requests.exceptions.RequestException as e:
        # 印出「真正的原因」，方便判斷是網站名稱錯(404)、被擋(403)、還是網路/proxy 問題
        print("[錯誤] 這次沒有成功抓到資料，程式停止（不會用假資料頂替）。")
        print(f"       原因：{repr(e)}")
        print("       請檢查：1) 是否已連上網路　2) 網址是否正確　3) 是否被防火牆／代理擋住")
        return None


def pick_table(tables):
    """步驟 3 的關鍵：一個頁面常有很多表格，挑出「含有『人口』欄位」的那一張。
    用欄位名稱來挑，比寫死 tables[0] 更耐得住網頁改版。"""
    for df in tables:
        columns = [str(c) for c in df.columns]
        if any("人口" in c for c in columns):
            return df
    return tables[0]                      # 真的找不到就先用第一張


def main():
    # 步驟 2：取得網頁內容。抓不到就結束，不產生任何資料。
    result = get_html()
    if result is None:
        sys.exit(1)
    html, source = result

    # 步驟 3：解析出所有表格
    try:
        tables = pd.read_html(StringIO(html))
    except ValueError as e:
        print("[錯誤] 網頁有抓到，但裡面找不到可解析的表格，程式停止。")
        print(f"       原因：{repr(e)}")
        sys.exit(1)

    if not tables:
        print("[錯誤] 這個頁面沒有任何表格，程式停止（不會用假資料頂替）。")
        sys.exit(1)

    print(f"這個頁面總共找到 {len(tables)} 個表格")

    df = pick_table(tables)
    print("\n抓到的資料（前 5 列）：")
    print(df.head())

    # 步驟 4：存成 CSV。encoding 用 utf-8-sig，Excel 打開中文才不會亂碼。
    out_path = os.path.join(os.path.dirname(__file__), "output.csv")
    df.to_csv(out_path, index=False, encoding="utf-8-sig")

    print(f"\n[完成] 已存檔：{out_path}（共 {len(df)} 列）")
    print(f"[資料來源] {source}")          # 一眼看出資料到底從哪來，方便驗證
    print("這就是你的第一次『網路資料蒐集』——七步地圖的第 1、2 步。")


if __name__ == "__main__":
    main()
