# ============================================================
#
# 任務：用 re.sub 整理電話號碼、re.fullmatch 驗證、count 遮罩
#      (1) +886 轉換成 0 
#      (2) 刪掉數字以外的符號 
#      (3) 檢查清理前、後是否為 09 開頭的 10 碼 
#      (4) 只顯示末 4 碼
#
# ============================================================
import re

phones = ["+886912-345-678", "+886 922 111 886",
          "0928 888-666", "0966-123-345"]

# (1) 開頭的 +886（後面可能接空白或 -）換成 0；^ 只看開頭、+ 要跳脫 → 號碼中間的 886 不會被換掉
step1 = [re.sub(r"^\+886[ -]?", "0", phone) for phone in phones]
print("①", step1)

# (2) 不是數字的字元（- 空白 .）全部換成空字串
step2 = [re.sub(r"[^0-9]", "", phone) for phone in step1]
print("②", step2)

# (3) fullmatch 驗證「整段」是不是 09 + 8 個數字：清理前有符號 → 全部 False；清理後 → 全部 True
print("③ 清理前", [re.fullmatch(r"09\d{8}", phone) is not None for phone in step1])
print("   清理後", [re.fullmatch(r"09\d{8}", phone) is not None for phone in step2])

# (4) 個資遮罩：\d 配到每個數字，count=6 只換前 6 個 → 末 4 碼保留
# 註：count 一定要寫成關鍵字參數；Python 3.13 起用位置參數會出現 DeprecationWarning。
masked = [re.sub(r"\d", "*", phone, count=6) for phone in step2]
print("④", masked)
