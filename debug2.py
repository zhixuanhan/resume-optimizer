# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    data = f.read()

lines = data.split(b'\n')
print(f'Total lines: {len(lines)}')

# Check raw bytes of lines 5788-5810
for i in range(5787, 5810):
    l = lines[i]
    print(f'Line {i+1} ({len(l)} bytes): {repr(l[:100])}')
