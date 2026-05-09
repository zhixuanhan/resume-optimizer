# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    lines_raw = f.read().split(b'\n')

# Find where the prompt f""" on line 4291 gets closed
print("=== Lines 4310-4350 (searching for closing \"\"\") ===")
for i in range(4309, 4350):
    if i < len(lines_raw):
        line = lines_raw[i]
        has_tq = b'\x22\x22\x22' in line
        marker = " <<<" if has_tq else ""
        print(f"Line {i+1:4d}: {repr(line[:100])}{marker}")

# Also check: does line 4293 start with f-string continuation?
print("\n=== Line 4293 detail ===")
print(repr(lines_raw[4292]))

# Check: maybe the closing """ is on line 4312?
print("\n=== Looking at lines 4311-4315 ===")
for i in range(4310, 4315):
    print(f"Line {i+1:4d}: {repr(lines_raw[i][:100])}")