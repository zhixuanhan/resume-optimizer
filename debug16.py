# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    lines_raw = f.read().split(b'\n')

tq = b'\x22\x22\x22'

# Cumulative balance scanning backward from line 5840
balance = 0
open_start = None
print("=== Scanning backward from line 5840 for unclosed triple-quote ===")
for i in range(5839, -1, -1):
    line = lines_raw[i]
    positions = [j for j in range(len(line)-2) if line[j:j+3] == tq]
    count = len(positions)
    balance += count
    if balance % 2 != 0 and open_start is None:
        open_start = i + 1
        text = line.decode('utf-8', errors='replace')
        print(f"  UNCLOSED START found at line {i+1} (balance={balance}, count={count})")
        print(f"  Content: {repr(text[:80])}")
        # Show a few lines around it
        for j in range(max(0, i-1), min(len(lines_raw), i+5)):
            tq_j = len([k for k in range(len(lines_raw[j])-2) if lines_raw[j][k:k+3] == tq])
            marker = " <-- START" if j == i else ""
            print(f"    {j+1}: tq={tq_j} {repr(lines_raw[j][:60])}")
        break

# Also check forward from the identified start
if open_start:
    print(f"\n=== Checking from line {open_start} forward ===")
    balance = 0
    for i in range(open_start-1, min(len(lines_raw), open_start+100)):
        line = lines_raw[i]
        positions = [j for j in range(len(line)-2) if line[j:j+3] == tq]
        count = len(positions)
        balance += count
        tq_pos_str = str([j for j in range(len(line)-2) if line[j:j+3] == tq])
        print(f"  Line {i+1:4d}: tq_count={count} pos={tq_pos_str} balance={balance%2} {repr(line[:60])}")
        if balance % 2 == 0 and i > open_start:
            print(f"  CLOSED at line {i+1}!")
            break