# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    lines_raw = f.read().split(b'\n')

# Check lines around 5840
print("=== Lines 5835-5845 ===")
for i in range(5834, 5845):
    print(f"Line {i+1:4d}: {repr(lines_raw[i][:100])}")

print()
# Find the NEXT triple-quote line after 5840
print("=== Next tq lines after 5840 ===")
for i in range(5840, min(len(lines_raw), 5900)):
    if b'\x22\x22\x22' in lines_raw[i]:
        print(f"Line {i+1:4d}: {repr(lines_raw[i][:100])}")
        break

# Count total tq pairs end-to-end
print()
tq_positions = []
for i, line in enumerate(lines_raw):
    for j in range(len(line) - 2):
        if line[j:j+3] == b'\x22\x22\x22':
            tq_positions.append(i+1)

# Find consecutive pairs in same line
# A properly closed tq string: two tqs on same line OR one tq on two consecutive lines
print("Triple quote line numbers:", tq_positions)
print(f"Total: {len(tq_positions)}")

# Check the structure around line 5840
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print()
print("=== Text lines 5835-5850 ===")
for i in range(5834, 5850):
    if i < len(lines):
        print(f"Line {i+1:4d}: {repr(lines[i][:80])}")