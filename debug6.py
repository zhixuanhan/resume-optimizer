# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    lines_raw = f.read().split(b'\n')

# Check line 5839 (0-indexed: 5838)
line = lines_raw[5838]
print(f'Line 5839: {len(line)} bytes')
print('Hex:', line.hex()[:100])
text = line.decode('utf-8', errors='replace')
print('As text:', repr(text[:80]))

# Count triple quotes
tq = b'\x22\x22\x22'  # three double quotes in bytes
positions = []
for i in range(len(line) - 2):
    if line[i:i+3] == tq:
        positions.append(i)
print(f'Triple quote positions (bytes): {positions}')

# Also check line 5831 and before
print('\n--- Lines 5830-5832 ---')
for i in [5830, 5831, 5832]:
    if i < len(lines_raw):
        print(f'Line {i+1}: {lines_raw[i].decode("utf-8", errors="replace")[:60]}')

# Check: is line 5791 really missing )?
print('\n--- Line 5791 raw ---')
line_5791 = lines_raw[5790]
print(f'Bytes: {line_5791}')
print(f'Last 20 bytes: {line_5791[-20:]}')
print(f'As text: {repr(line_5791.decode("utf-8", errors="replace"))}')
