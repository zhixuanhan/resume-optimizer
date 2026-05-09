# -*- coding: utf-8 -*-
"""Find all triple-quoted strings and identify the unclosed one"""
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    raw = f.read()

lines_raw = raw.split(b'\n')
tq = b'\x22\x22\x22'

open_count = 0
open_line = None
print("=== Triple-quote pair analysis ===")
for i, line in enumerate(lines_raw):
    positions = []
    for j in range(len(line) - 2):
        if line[j:j+3] == tq:
            positions.append(j)
    count = len(positions)
    if count > 0:
        open_count += count % 2  # if odd, toggle
        if count % 2 != 0 and open_line is None:
            open_line = i + 1
            print(f"  *** Potential unclosed start at line {i+1}: {repr(line[:80])}")
        print(f"Line {i+1:4d}: tq={positions} (net_open now: {open_count%2})")
        if open_count % 2 == 0:
            open_line = None

print(f"\nFinal net triple-quote balance: {open_count % 2}")
if open_count % 2 != 0:
    print(f"UNCLOSED string! Started somewhere before line with odd count.")