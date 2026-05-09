# -*- coding: utf-8 -*-
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
# Find lines around 1180
for i in range(1175, 1195):
    if i < len(lines):
        print(f"Line {i+1}: {repr(lines[i])}")
