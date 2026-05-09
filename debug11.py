# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    lines_raw = f.read().split(b'\n')

# Check the suspicious lines
for line_num in [4780, 4781, 4782, 4783, 4784, 4969, 4970, 4971, 4972, 4973, 5837, 5838, 5839, 5840, 5841]:
    idx = line_num - 1
    if idx < len(lines_raw):
        line = lines_raw[idx]
        tq_count = len([j for j in range(len(line)-2) if line[j:j+3] == b'\x22\x22\x22'])
        text = line.decode('utf-8', errors='replace')
        print(f"Line {line_num:4d}: tq={tq_count} | {text[:100]}")

print()
# Check line 5838 more carefully - it shows as empty but is the error line
print("Line 5839:", repr(lines_raw[5838][:120]))
print("Line 5840:", repr(lines_raw[5839][:120]))