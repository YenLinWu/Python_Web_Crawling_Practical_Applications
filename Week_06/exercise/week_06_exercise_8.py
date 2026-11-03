# ============================================================
#
# 任務：用 Python 判讀 iThome 的 robots.txt，且擷取 Content-Signal 相關資訊。
# 
# ============================================================
import logging
import sys
import time
from pathlib import Path
from urllib import robotparser
import requests

ROBOTS_URL = "https://www.ithome.com.tw/robots.txt"      
MY_USER_AGENT = "MyCustomBot"
AI_BOTS = ["GPTBot", "ClaudeBot"]
HEADERS = {"User-Agent": "..."}

# Content-Signal 
SIGNAL_MEANING = {
    "search": "建立搜尋索引、提供搜尋結果（不含 AI 摘要）",
    "ai-input": "把內容即時餵給 AI 模型（例如 RAG、AI 回答時引用）",
    "ai-train": "拿來訓練或微調 AI 模型"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(Path(__file__).with_name("w06_ex8_RobotsiThome.log"), encoding="utf-8"), 
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("week_06_exercise_8_iThome_robots")
logger.info("Python %s", sys.version.split()[0])          # 紀錄 Python 版本 (因為 Python 版本會影響判讀結果)

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


# 定義函式 : Content-Signal 資訊擷取
def fetch_robots_text(robots_url):
    '''
    下載 robots.txt 原文。
    '''
    resp = requests.get(robots_url, headers=HEADERS, timeout=10)
    if not 200 <= resp.status_code < 300:
        return ""
    resp.encoding = "utf-8-sig"            # RFC 9309 規定 UTF-8；-sig 會去掉檔頭 BOM
    return resp.text

def parse_content_signals(robots_text):
    '''
    把 robots.txt 整理成 {User-agent: {訊號: 值}}，每個群組都會列出(沒宣告就是空 dict)。
    例如:「User-agent: *」下有「Content-Signal: search=yes, ai-train=no」
          → {"*": {"search": "yes", "ai-train": "no"}}
    '''
    groups = {}
    agents = []                            # 目前這一組的 User-agent
    seen_rule = False                      # 這一組是否已經出現過規則行
    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()             # 去掉 # 後面的註解
        if ":" not in line:
            continue                                     # 空行、純註解行
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if seen_rule:                                # 規則之後又出現 User-agent → 新的一組
                agents, seen_rule = [], False
            agents.append(value.lower())
            groups.setdefault(value.lower(), {})
            continue
        seen_rule = True
        if key == "content-signal" and agents:           # 不屬於任何群組的 Content-Signal 不採計
            for item in value.split(","):                # 「search=yes, ai-train=no」→ 逐一拆開
                if "=" in item:
                    name, val = (x.strip().lower() for x in item.split("=", 1))
                    for agent in agents:
                        groups[agent][name] = val
    return groups

def content_signals_for(groups, user_agent):
    '''
    擷取某個 User-agent 的 Content-Signal 資訊。 
    '''
    ua = user_agent.lower()
    if ua in groups:
        return ua, groups[ua]
    return "*", groups.get("*", {})


# Step 1: 讀取與解析 robots.txt
try:
    rp = read_robots(ROBOTS_URL)
except requests.RequestException as e:                    # 網路錯誤：明確報錯、停止
    logger.error("讀取失敗：%s", e)
    sys.exit(1)

# Step 2: 要測試的目標網址，逐一檢視是否允許抓取
test_urls = {
    "首頁": "https://www.ithome.com.tw/",
    "最新新聞": "https://www.ithome.com.tw/latest",
    "單篇新聞": "https://www.ithome.com.tw/news/171234",
    "站內搜尋": "https://www.ithome.com.tw/search/python",
    "會員登入": "https://www.ithome.com.tw/user/login/",
    "CSS 檔": "https://www.ithome.com.tw/misc/a.css"
}

for name, url in test_urls.items():
    status = "允許" if rp.can_fetch(MY_USER_AGENT, url) else "禁止"
    logger.info("%-6s [%s] %s", name, status, url)

# Step 3: 請求間隔與 AI 爬蟲
delay = rp.crawl_delay(MY_USER_AGENT)
logger.info("Crawl-delay：%s 秒", delay)
for bot in AI_BOTS:
    status = "允許" if rp.can_fetch(bot, test_urls["最新新聞"]) else "禁止"
    logger.info("%-10s 爬 /latest：[%s]", bot, status)

# Step 4: Content-Signal
wait = delay or 3                                         # 第二次請求前，遵守網站要求的間隔
logger.info("再下載一次 robots.txt 原文前，先等 %s 秒", wait)
time.sleep(wait)
try:
    groups = parse_content_signals(fetch_robots_text(ROBOTS_URL))
except requests.RequestException as e:
    logger.error("讀取原文失敗：%s", e)
    sys.exit(1)

declared = {agent: sig for agent, sig in groups.items() if sig}
if not declared:
    logger.info("Content-Signal：沒有宣告")
else:
    logger.info("Content-Signal：有宣告，出現在群組 %s", list(declared))
    group, signals = content_signals_for(groups, MY_USER_AGENT)
    logger.info("%s 適用 User-agent: %s 群組", MY_USER_AGENT, group)
    for name in list(SIGNAL_MEANING) + [n for n in signals if n not in SIGNAL_MEANING]:
        value = signals.get(name, "未宣告")                     # 未宣告＝不授權也不限制
        meaning = SIGNAL_MEANING.get(name, "（本程式未收錄的訊號）")
        logger.info("  %-8s = %-6s %s", name, value, meaning)
