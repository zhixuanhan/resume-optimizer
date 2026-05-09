# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    raw = f.read()
lines_raw = raw.split(b'\n')

# Find the line with "请直接输出6个Q&A"
for i, line in enumerate(lines_raw):
    if b'\xe8\xaf\xb7\xe7\x9b\xb4\xe6\x8e\xa5\xe8\xbe\x93\xe5\x87\xba6\xe4\xb8\xaaQ&A' in line:
        print(f"Found at line {i+1} (0-indexed {i})")
        print(f"  Raw: {repr(line[:80])}")
        # Show previous lines
        for j in range(max(0, i-3), i+3):
            print(f"  {j+1}: {repr(lines_raw[j][:60])}")
        break

# Also check: line 4315 in 1-indexed = index 4314
print("\nLine 4316 (index 4315):", repr(lines_raw[4314][:80]))
print("Line 4317 (index 4316):", repr(lines_raw[4315][:80]))
print("Line 4318 (index 4317):", repr(lines_raw[4316][:80]))