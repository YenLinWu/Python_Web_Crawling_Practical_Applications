# Take-home Midterm Exam

**Course**: Python Web Crawling: Practical Applications  
**Instructor**: Yen-Lin Wu  
**Release date**: Tuesday, November 3, 2026  
**Due**: Friday, November 13, 2026, before 12:00 noon (submit by email)


**Instructions**  
1. Write your answers to the true/false questions, the multiple-choice questions, the bonus question, and the short-answer parts of the practical tasks in the answer sheet `Take-home_Midterm_Exam_Answer_Sheet_EN.md`. Save it as `StudentID_Name_AnswerSheet.md`.
2. For Part 3 (practical tasks), write `.py` program files. Add the necessary comments, and make sure the programs can run directly.
3. You may use the course materials and official documentation. You may also use AI tools, but you must be able to explain every part of the code you submit.
4. Put all your files into one zip file named `StudentID_Name_Midterm.zip` and email it to tom.yenlinwu@gmail.com. Use this email subject: "Midterm_Take-Home_StudentID_Name".

---

## Part 1　True or False (2 points each, 20 points in total)

Decide whether each statement is correct. Write "O" if it is correct, or "X" if it is wrong.

1. When collecting data, you should use open data or an official API first. Only scrape web pages when no API is available.
2. Wikipedia uses the CC BY-SA license. So if you use a Wikipedia table in a report for non-commercial purposes, you do not need to credit the source.
3. After you create a virtual environment `.venv`, you cannot simply move or copy it to another folder. To change its location, you must create it again in the new location.
4. The fragment identifier (the part of a URL after `#`) is sent to the server together with the request.
5. If `soup.select("div.country")` finds no matching elements, it returns `None`.
6. If the `Content-Type` response header does not include a charset, requests decodes `resp.text` as ISO-8859-1. This is why prices on books.toscrape.com appear as the garbled text `Â£51.77`.
7. The result of `re.findall(r"\d+", "Explain Like I'm 10")` is `['1', '0']`.
8. When a regular expression contains groups `( )`, `re.findall` returns the content of the groups (a list of tuples if there is more than one group), not the full matched text.
9. Page 11 of quotes.toscrape.com has no quotes, so the server returns 404. Therefore, a pagination loop only needs to check for 404 to know when to stop.
10. HTTP is a "stateless" protocol. `requests.Session()` automatically saves the cookies sent by the server and sends them back in later requests.

---

## Part 2　Multiple Choice (3 points each, 30 points in total)

**1.** A website is redesigned. Only the colors, fonts, and positions of page sections change; the HTML tags and classes stay the same. Which scraping method is **almost unaffected**?  
(A) RPA that clicks based on screen coordinates  
(B) A Python scraper that finds elements with CSS selectors  
(C) Both will break and must be rebuilt  
(D) Both must rewrite their selectors

**2.** You want to record the packages and versions in your current virtual environment, so that a classmate can rebuild exactly the same environment. Which command should you run?  
(A) `pip list`  
(B) `pip install -r requirements.txt`  
(C) `pip freeze > requirements.txt`  
(D) `python -m venv .venv`  

**3.** What is the main purpose of setting `User-Agent` in `HEADERS`?  
(A) To hide the scraper's identity so that the website cannot detect it  
(B) To send the login status with every request automatically  
(C) To make the server respond faster  
(D) To honestly identify the program and its purpose, so the website knows who is sending the request

**4.** After you run the code below, what is `resp.url` most likely to be?

```python
resp = requests.get("https://www.scrapethissite.com/pages/forms/",
                    params={"q": "new york", "per_page": 100}, timeout=10)
```

(A) `https://www.scrapethissite.com/pages/forms/?q=new+york&per_page=100`  
(B) `https://www.scrapethissite.com/pages/forms/?q=new york&per_page=100`  
(C) `https://www.scrapethissite.com/pages/forms/` (the parameters are sent in the body)  
(D) `https://www.scrapethissite.com/pages/forms/#q=new+york&per_page=100`

**5.** Which of the following finds the same elements as `soup.find_all("div", class_="country")`?  
(A) `soup.select_one("div.country")`  
(B) `soup.select("div.country")`  
(C) `soup.find("div", class_="country")`  
(D) `soup.select("#country")`  

**6.** What is the result of `re.findall(r"\b\d{1,2}\b", "March 14, 1879")`?  
(A) `['14', '18', '79']`  
(B) `['14', '1879']`  
(C) `[]`  
(D) `['14']`

**7.** What happens when you run the code below?

```python
m = re.search(r"(?P<level>[A-Z]+) (?P<date>\d{4}-\d{2}-\d{2}): (?P<msg>.+)",
              "ERROR: 2026-10-21: Retry failed")
print(m.groupdict())
```

(A) `{'level': 'ERROR', 'date': '2026-10-21', 'msg': 'Retry failed'}`  
(B) `{'level': 'ERROR:', 'date': '2026-10-21', 'msg': 'Retry failed'}`  
(C) An `AttributeError` occurs, because `m` is `None`  
(D) `{}`

**8.** On Hacker News, the URL of the next page of the newest posts is `/newest?next=50249973&n=31`. The value of `next` cannot be predicted in advance. What is the best way to move to the next page?  
(A) Find the href of the "More" link on the current page, then build the full URL with urljoin  
(B) Use `for page in range(1, 11)` to build `?page=N`  
(C) Add 30 to the value of `next` each time  
(D) Send the page number with POST instead  

**9.** Your scraper receives `429 Too Many Requests`. What is the best way to handle it?  
(A) Resend the request immediately until it succeeds  
(B) Change the User-Agent and resend the request immediately  
(C) Wait for the number of seconds given in the Retry-After header. If there is no Retry-After header, wait longer each time (for example, 4, 6, then 8 seconds) before you retry  
(D) Treat it like a 404 and check how the URL is built

**10.** A website's robots.txt is shown below. According to the rules of **RFC 9309**, can the crawler `MyBot` crawl `/search/help/faq`?

```
User-agent: *
Disallow: /search/
Allow: /search/help
```

(A) Allowed, because `Allow: /search/help` is longer than `Disallow: /search/`  
(B) Not allowed, because the Disallow rule comes first  
(C) Not allowed, because Disallow always has priority over Allow  
(D) Cannot be decided, because there is no `User-agent: MyBot` line  

---

## Part 3　Practical Tasks (50 points in total)

### Task 1　Daily Horoscope (30 points)

**Website**: Click108 Astrology Channel (科技紫微網 星座頻道)　https://astro.click108.com.tw/  
**Daily horoscope URL**: `https://astro.click108.com.tw/daily_{code}.php?iAstro={code}&iType=0&iAcDay={date}`

| Code | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sign | Aries 牡羊 | Taurus 金牛 | Gemini 雙子 | Cancer 巨蟹 | Leo 獅子 | Virgo 處女 | Libra 天秤 | Scorpio 天蠍 | Sagittarius 射手 | Capricorn 摩羯 | Aquarius 水瓶 | Pisces 雙魚 |

> The website is in Traditional Chinese. Save the text exactly as it appears on the page. You do not need to translate it.

**Tasks**

1. Read https://astro.click108.com.tw/robots.txt and answer these questions in the answer sheet:
   - Which items are explicitly disallowed for `User-agent: *`?
   - What is the Crawl-delay for general crawlers, in seconds? Based on this, explain how many requests your program may send to this website per day, and how your program follows this rule.

2. Scrape the daily horoscope for **your own zodiac sign on the day you run your program**, and save it as `p1_daily_horoscope.csv`. Record four items: overall (整體運勢), love (愛情運勢), career (事業運勢), and finance (財務運勢). For each item, record the **number of stars** (an integer) and the **text description**. Use the columns below (one row per day). Keep the column names in Chinese exactly as shown, so that all submissions can be graded in the same way.

   | 日期 | 星座 | 整體運勢_星數 | 整體運勢_說明 | 愛情運勢_星數 | 愛情運勢_說明 | 事業運勢_星數 | 事業運勢_說明 | 財務運勢_星數 | 財務運勢_說明 |
   |---|---|---|---|---|---|---|---|---|---|
   | Date | Zodiac sign | Overall: stars | Overall: description | Love: stars | Love: description | Career: stars | Career: description | Finance: stars | Finance: description |

   Note: Save the execution log of your Python program as `p1.log`.
</br>  
**Hint**:  
You will run your program many times while debugging. We suggest that **the first time, you save the web page as an HTML cache file; after that, read the cache file instead of connecting to the website again**. Your log should record whether each run "read the cache" or "sent a new request". This way, you still follow the Crawl-delay rule while debugging.

**Submit**: `p1_daily_horoscope.py`, `p1_daily_horoscope.csv`, `p1.log`

---

### Task 2　Organizing a Log File with Regular Expressions (20 points)

The log below records the process of crawling the Quotes to Scrape website. It has been saved in the file `crawl.log`.

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

**Tasks**
1. Use **named groups** to split each line into a dict (level, date, message). Skip any line that does not match the format, and write its line number to the log. Convert the results into a DataFrame and save it as `p2_log_table.csv` (columns: level, date, message).  
   Note: Save the execution log of your Python program as `p2.log`.  

2. Count the number of lines for each level, and write the results to `p2.log`.  

3. You want to use a regex to extract all HTTP status codes (3-digit 4xx codes) from message. What regex pattern would you use? Write the pattern to `p2.log`.   

**Submit**: `p2_regex.py`, `p2_log_table.csv`, `p2.log`

---

## Bonus Question (10 points)

What have you learned in the past few weeks? Describe one **real problem** you met in a class exercise or assignment. Explain how you found it, how you solved it, and what new understanding it gave you about web crawling. (Within 200 words. Write your answer in the answer sheet.)
