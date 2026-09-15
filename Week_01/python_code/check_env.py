# check_env.py 驗證安裝套件。
# 目的：一次確認本學期前半段常用的套件都裝好了。
# 用法：在 VS Code 終端機輸入 ->  python check_env.py
# 全部顯示 [OK] 就代表環境完成；出現 [MISSING] 的套件，回去用 pip 安裝。
#
# 註：輸出只用 ASCII 記號（[OK]/[MISSING]），避免 Windows cp950 主控台
#     無法顯示勾勾或 emoji 而出錯。

import sys

# 我們要檢查的套件： (import 時的名稱, pip 安裝時的名稱)
packages = [
    ("requests", "requests"),
    ("bs4", "beautifulsoup4"),
    ("pandas", "pandas"),
    ("lxml", "lxml"),
]

print("=" * 44)
print("Python 版本：", sys.version.split()[0])
print("=" * 44)

all_ok = True
for import_name, pip_name in packages:
    try:
        module = __import__(import_name)
        version = getattr(module, "__version__", "(無版本資訊)")
        print(f"[OK]      {pip_name:<16} {version}")
    except ImportError:
        all_ok = False
        print(f"[MISSING] {pip_name:<16} 請執行：pip install {pip_name}")

print("=" * 44)
if all_ok:
    print("環境完成！可以開始寫第一支爬蟲了。")
else:
    print("有套件還沒裝好，照上面的提示補裝後再跑一次。")
