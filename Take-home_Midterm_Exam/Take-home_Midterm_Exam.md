# Take-home Midterm Exam

**課程**：Python 網路爬蟲實務應用  
**授課教師**：吳彥霖   
**發布日期**：2026 年 11 月 3 日（星期二）　  
**繳交期限**：2026 年 11 月 13 日（星期五）中午 12:00 前(以 email 繳交)


**作答說明**  
1. 是非題、單選題、加分題與實作部分子題，請填寫於答案卷 `Take-home_Midterm_Exam_答案卷.md`，另存為 `學號_姓名_答案卷.md`。
2. 第三部分實作題請撰寫 `.py` 程式檔，須附必要註解，並可直接執行。
3. 作答期間得參閱課程教材與官方文件；得使用 AI 輔助工具，惟須能逐段說明所繳交程式之邏輯。
4. 繳交時，將所有檔案壓縮為 `學號_姓名_期中.zip`，寄至 tom.yenlinwu@gmail.com，信件主旨為「Midterm_Take-Home_學號_姓名」。

---

## 第一部分　是非題（每題 2 分，共 20 分）

請判斷下列敘述是否正確，正確填「○」，錯誤填「✕」。

1. 取得資料時，應優先使用開放資料或官方 API；只有在沒有 API 的情況下，才考慮爬取網頁。
2. 維基百科採 CC BY-SA 授權，因此把維基表格用在報告中時，只要不做商業用途，就不需要標示來源。
3. 虛擬環境 `.venv` 建立後不能直接搬移或複製到其他路徑使用；要換位置，必須在新位置重新建立。
4. 網址中 `#` 後面的片段識別符（Fragment），會隨著請求一起傳送給伺服器。
5. `soup.select("div.country")` 找不到任何符合的元素時，會回傳 `None`。
6. 回應標頭 `Content-Type` 沒有標明 charset 時，requests 會用 ISO-8859-1 解碼 `resp.text`，因此 books.toscrape.com 的價格會出現 `Â£51.77` 亂碼。
7. `re.findall(r"\d+", "Explain Like I'm 10")` 的結果是 `['1', '0']`。
8. 正規表達式中有分組 `( )` 時，`re.findall` 回傳的是各分組的內容（有兩個以上分組時為 tuple 清單），而不是整段匹配的文字。
9. quotes.toscrape.com 第 11 頁已沒有名言，伺服器會回傳 404，所以翻頁迴圈只要判斷 404 就能停止。
10. HTTP 是「無狀態」的協定；`requests.Session()` 可以自動保存伺服器發的 cookie，並在之後的請求中自動帶回。

---

## 第二部分　單選題（每題 3 分，共 30 分）

**1.** 某網站改版，只「換了配色、字體，版面區塊挪動位置」，HTML 標籤與 class 都沒變。哪一種擷取方法**幾乎不受影響**？  
(A) 依畫面座標點擊的 RPA  
(B) 以 CSS 選擇器定位的 Python 爬蟲  
(C) 兩者都會壞，要重建  
(D) 兩者都要重寫選擇器

**2.** 想把目前虛擬環境裡的套件與版本記錄下來，讓同學可以重建一模一樣的環境，應執行哪個指令？  
(A) `pip list`  
(B) `pip install -r requirements.txt`  
(C) `pip freeze > requirements.txt`  
(D) `python -m venv .venv`  

**3.** 在 `HEADERS` 中設定 `User-Agent` 的主要目的為何？  
(A) 隱藏爬蟲身分，避免被網站發現  
(B) 讓請求自動帶上登入狀態  
(C) 加快伺服器回應速度  
(D) 誠實標明是程式及其用途，讓網站知道請求來自誰

**4.** 執行下列程式後，`resp.url` 最可能是哪一個？

```python
resp = requests.get("https://www.scrapethissite.com/pages/forms/",
                    params={"q": "new york", "per_page": 100}, timeout=10)
```

(A) `https://www.scrapethissite.com/pages/forms/?q=new+york&per_page=100`  
(B) `https://www.scrapethissite.com/pages/forms/?q=new york&per_page=100`  
(C) `https://www.scrapethissite.com/pages/forms/`（參數放在 body）  
(D) `https://www.scrapethissite.com/pages/forms/#q=new+york&per_page=100`

**5.** 下列哪一個寫法，和 `soup.find_all("div", class_="country")` 找到的元素相同？  
(A) `soup.select_one("div.country")`    
(B) `soup.select("div.country")`  
(C) `soup.find("div", class_="country")`  
(D) `soup.select("#country")`  

**6.** `re.findall(r"\b\d{1,2}\b", "March 14, 1879")` 的結果為何？  
(A) `['14', '18', '79']`  
(B) `['14', '1879']`  
(C) `[]`  
(D) `['14']`

**7.** 執行下列程式，結果為何？

```python
m = re.search(r"(?P<level>[A-Z]+) (?P<date>\d{4}-\d{2}-\d{2}): (?P<msg>.+)",
              "ERROR: 2026-10-21: Retry failed")
print(m.groupdict())
```

(A) `{'level': 'ERROR', 'date': '2026-10-21', 'msg': 'Retry failed'}`  
(B) `{'level': 'ERROR:', 'date': '2026-10-21', 'msg': 'Retry failed'}`  
(C) 發生 `AttributeError`，因為 `m` 是 `None`  
(D) `{}`

**8.** Hacker News 最新文章的下一頁網址是 `/newest?next=50249973&n=31`，其中 `next` 的值無法事先推算。最適合的翻頁寫法是？  
(A) 從本頁找出「More」連結的 href，再用 urljoin 組出完整網址  
(B) 用 `for page in range(1, 11)` 組出 `?page=N`  
(C) 把 `next` 的數字每次加 30  
(D) 改用 POST 送出頁碼  

**9.** 爬蟲收到 `429 Too Many Requests` 時，最適當的處理方式是？  
(A) 立刻重送，直到成功為止  
(B) 換一個 User-Agent 後立刻重送  
(C) 依回應的 Retry-After 秒數等待；若沒有，就逐步拉長等待時間（如 4、6、8 秒）再重試  
(D) 視同 404，檢查網址拼接

**10.** 某網站的 robots.txt 如下。依 **RFC 9309** 的規則，爬蟲 `MyBot` 能否爬取 `/search/help/faq`？

```
User-agent: *
Disallow: /search/
Allow: /search/help
```

(A) 允許，因為 `Allow: /search/help` 比 `Disallow: /search/` 長  
(B) 禁止，因為 Disallow 寫在前面  
(C) 禁止，因為 Disallow 永遠優先於 Allow  
(D) 無法判斷，因為沒有寫 `User-agent: MyBot`  
    
---

## 第三部分　實作題（共 50 分）

### 實作一　每日星座運勢（30 分）

**網站**：科技紫微網 星座頻道　https://astro.click108.com.tw/  
**每日運勢網址**：`https://astro.click108.com.tw/daily_{代碼}.php?iAstro={代碼}&iType=0&iAcDay={日期}`

| 代碼 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 星座 | 牡羊 | 金牛 | 雙子 | 巨蟹 | 獅子 | 處女 | 天秤 | 天蠍 | 射手 | 摩羯 | 水瓶 | 雙魚 |
  
**任務**

1. 檢視 https://astro.click108.com.tw/robots.txt ，於答案卷回答：
   - `User-agent: *` 明確標示哪些禁止項目？
   - 一般爬蟲的 Crawl-delay 是幾秒？依此說明你的程式一天可以對這個網站請求幾次，以及你在程式中如何遵守。

2. 爬取**自己星座、執行當日**的每日運勢，存成 `p1_daily_horoscope.csv`。須記錄整體運勢、愛情運勢、事業運勢、財務運勢四項，每項皆要有**幾顆星**（整數）與**文字說明**。欄位如下（一列一天）：

   | 日期 | 星座 | 整體運勢_星數 | 整體運勢_說明 | 愛情運勢_星數 | 愛情運勢_說明 | 事業運勢_星數 | 事業運勢_說明 | 財務運勢_星數 | 財務運勢_說明 |
   |---|---|---|---|---|---|---|---|---|---|

   註 : 須記錄 Python 執行 log，存檔成 `p1.log`。
</br>  
**提示**：  
撰寫程式時會反覆執行除錯，建議**第一次把網頁存成 HTML 快取檔，之後的執行改讀快取，不再連網**，log 要記錄「讀取快取／重新請求」，以便在程式除錯期間仍遵守 Crawl-delay 的規定。

**繳交**：`p1_daily_horoscope.py`、`p1_daily_horoscope.csv`、`p1.log`

---

### 實作二　正規表達式整理 log（20 分）

下列 log 為記錄爬取 Quotes to Scrape 網站的過程，且已寫入 `crawl.log` 檔案中。

```
INFO 2026-11-02: Start crawling quotes.toscrape.com
INFO 2026-11-02: Page 1 saved 10 quotes
WARNING 2026-11-02: 429 Too Many Requests, retry after 4s
INFO 2026-11-02: Page 2 saved 10 quotes
ERROR 2026-11-02: Connection timed out /page/3/
INFO 2026-11-03: Page 3 saved 10 quotes
WARNING: 2026-11-03: Tag not found in quote 27
ERROR 2026-11-03: 404 Not Found /author/Albert-Einsten
INFO 2026-11-03: Finished, 30 quotes
```

**任務**
1. 用**具名分組**把每一列拆成 dict（level、date、message），格式不符的行要跳過，且將列號寫入 log。解析結果轉成 DataFrame，存成 `p2_log_table.csv` (欄位 level、date、message)。  
   註 : 須記錄 Python 執行 log，存檔成 `p2.log` 。  

2. 統計各等級筆數，結果寫入 `p2.log` 。  

3. 若要採用 regex 從 message 抽出所有 HTTP 狀態碼（4xx 的 3 位數），請問 regex 的寫法為何? regex 寫法寫入 `p2.log` 。   

**繳交**：`p2_regex.py`、`p2_log_table.csv`、`p2.log`

---

## 加分題（10 分）

這幾週你學到了什麼？請舉一個你在課堂練習或作業中**實際遇到的問題**，說明你怎麼發現、怎麼解決，以及它讓你對網路爬蟲有什麼新的理解。（300 字以內，填寫於答案卷）
