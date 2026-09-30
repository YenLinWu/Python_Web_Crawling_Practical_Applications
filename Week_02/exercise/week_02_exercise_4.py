scores = ["80", "90", "", "", "60", "100"]

total, valid = 0, 0
for s in scores:
    try:
        total += int(s)   # 空字串轉數字會丟 ValueError
        valid += 1        
    
    except ValueError:
        continue          

print(f"有效 {valid} 筆，總計 = {total}")