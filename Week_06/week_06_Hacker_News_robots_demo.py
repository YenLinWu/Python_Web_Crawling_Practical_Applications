# ============================================================
#
# 利用 Python 判讀 Hacker News' robots.txt
# 
# ============================================================
import logging
import sys
from pathlib import Path
from urllib import robotparser
import requests

ROBOTS_URL = "https://news.ycombinator.com/robots.txt"  # 指定 robots.txt 網址
MY_USER_AGENT = "MyCustomBot"                           # 自訂的 User-Agent 名稱
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CourseBot/1.0 (W6 demo)"}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("week_06_Hacker_News_Robots_demo.log"), encoding="utf-8"),  
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("week_06_demo_Hacker_News_robots")
logger.info("Python %s", sys.version.split()[0])    # 紀錄 Python 版本 (因為 Python 版本會影響判讀結果)

# 定義函式 : 用 requests 下載 robots.txt ，再由 robotparser 解析
def read_robots(robots_url):
    '''
    讀取與解析 robots.txt 檔。
    作法 : 先用 requests 下載 robots.txt ，再由 robotparser 解析。
    
    爬蟲在請求 robots.txt 時所得到的 HTTP 狀態碼:
      2xx         → 交給 parse() 解析規則
      401 / 403   → 全部禁止（沒權限讀規則，視為整站不開放）
      其他 4xx    → 全部允許（例如 404：網站沒有 robots.txt）
      5xx         → 全部禁止（伺服器出錯，規則不明，保守處理）
    '''
    rp = robotparser.RobotFileParser(robots_url)
    resp = requests.get(robots_url, headers=HEADERS, timeout=10)
    # 2xx 成功存取
    if 200 <= resp.status_code < 300:
        resp.encoding = 'utf-8'                 # RFC 9309 規定 UTF-8
        rp.parse(resp.text.splitlines())
    # 401/403 拒絕存取 → 全部禁止
    elif resp.status_code in (401, 403):   
        rp.disallow_all = True
    # 其他 4xx (不含 401/403) → 全部允許
    elif 400 <= resp.status_code < 500:  
        rp.allow_all = True
    # 5xx 伺服器錯誤 → 全部禁止
    elif resp.status_code >= 500:     
        rp.disallow_all = True
    # 其他狀況，例如 : 少見的 1xx → 全部禁止
    else:
        rp.disallow_all = True

    logger.info("robots.txt 狀態碼 %s：%s", resp.status_code, robots_url)
    return rp


# Step 1: 讀取與解析 robots.txt
try:
    rp = read_robots(ROBOTS_URL)
except requests.RequestException as e:          # 網路錯誤：明確報錯、停止
    logger.error("讀取失敗：%s", e)
    sys.exit(1)

# Step 2: 要測試的目標網址，逐一檢視是否允許抓取
test_urls = {
    "首頁": "https://news.ycombinator.com/",
    "最新文章": "https://news.ycombinator.com/newest",
    "單篇討論頁": "https://news.ycombinator.com/item?id=1",
    "登入頁": "https://news.ycombinator.com/login",
    "投票": "https://news.ycombinator.com/vote?id=1&how=up"
}

for name, url in test_urls.items():
    status = "允許" if rp.can_fetch(MY_USER_AGENT, url) else "禁止"
    logger.info("%-6s [%s] %s", name, status, url)

# Step 3: 請求間隔
delay = rp.crawl_delay(MY_USER_AGENT)
logger.info("Crawl-delay：%s 秒", delay)
