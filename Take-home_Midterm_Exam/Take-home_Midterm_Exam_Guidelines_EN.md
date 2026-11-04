# Take-home Midterm Exam Guidelines: Basic Skills in Web Data Scraping

**Course**: Python Web Crawling: Practical Applications (Fall Semester, Academic Year 2026–2027)  
**Instructor**: Yen-Lin Wu  
**Release date**: Tuesday, November 3, 2026  
**Due**: Friday, November 13, 2026, before 12:00 noon (submit by email)

---

## 1. Purpose

This take-home exam is a formative midterm assessment. It checks your understanding of the course content from Weeks 1 to 6. It also checks whether you follow these basic principles when you write a web crawler: checking robots.txt and following the Crawl-delay, keeping execution logs, saving data to CSV files, and using regular expressions to organize text data.

## 2. Format

- This is individual work, completed at home.
- You may use the course materials and official documentation. You may also use AI tools, but you must be able to explain every part of the code you submit.

## 3. Scope

Course materials from Weeks 1 to 6:

| Week | Topics |
|---|---|
| Week 1 | Introduction to web crawling, data sources, and CC licenses |
| Week 2 | Virtual environments, Python basics, and exception handling |
| Week 3 | HTTP requests and responses, status codes, headers, logging, query parameters, and the Network panel in Developer Tools |
| Week 4 | HTML structure, CSS selectors, BeautifulSoup, character encoding, and urljoin |
| Week 5 | Regular expressions and the re module |
| Week 6 | Pagination, sessions and cookies, polite crawling, robots.txt, and RFC 9309 |

## 4. Question Types and Points

| Part | Question type | Questions × points | Subtotal |
|---|---|---|---|
| Part 1 | True or false | 10 × 2 points | 20 points |
| Part 2 | Multiple choice | 10 × 3 points | 30 points |
| Part 3 | Task 1: Daily Horoscope | 1 | 30 points |
| Part 3 | Task 2: Organizing a Log File with Regular Expressions | 1 | 20 points |
| Bonus | Learning reflection | 1 | 10 points |
| | | Total | 110 points |

## 5. Requirements for the Practical Tasks

1. **Task 1: Daily Horoscope**
   - Before scraping, read the target website's robots.txt. In the answer sheet, write down the items disallowed for `User-agent: *` and the Crawl-delay.
   - Your program must follow the Crawl-delay rule. While debugging, we suggest that you save the web page as an HTML cache file, read the cache in later runs instead of connecting again, and record "read the cache" or "sent a new request" in the log.
   - Save the execution log as `p1.log` (UTF-8 encoding). Record the robots.txt check result, the status code, and the number of stars for each item.
   - Save the data as `p1_daily_horoscope.csv` (`encoding="utf-8-sig"`), with the columns given in the exam.
   - Set a User-Agent and a timeout in your program. Use `try/except` to handle request errors, and write the error messages to the log.
2. **Task 2: Organizing a Log File with Regular Expressions**
   - Use the file `crawl.log` provided by the instructor as your data source. No internet connection is needed.
   - Save the execution log as `p2.log` (UTF-8 encoding). Record the line numbers that do not match the format, the number of lines for each level, and your regex pattern.
   - Save the results as `p2_log_table.csv`, with the columns level, date, and message.

For Task 1, scrape only the website named in the exam, and follow its robots.txt and terms of service. Use the scraped data only for this exam. Do not upload it publicly (including to a public GitHub repository) or share it with others.

## 6. How to Submit

1. Email your work to the instructor (tom.yenlinwu@gmail.com) with the subject "Midterm_Take-Home_StudentID_Name".
2. Attach one zip file named `StudentID_Name_Midterm.zip`. It must include:

| Item | Files |
|---|---|
| Answer sheet | `StudentID_Name_AnswerSheet.md` (saved from `Take-home_Midterm_Exam_Answer_Sheet_EN.md`, with your answers to the true/false questions, the multiple-choice questions, the short-answer parts of the practical tasks, and the bonus question) |
| Task 1 | `p1_daily_horoscope.py`, `p1_daily_horoscope.csv`, `p1.log` |
| Task 2 | `p2_regex.py`, `p2_log_table.csv`, `p2.log` |

3. Your program files must include the necessary comments and must run directly.
