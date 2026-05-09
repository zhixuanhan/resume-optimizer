# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    data = f.read()

lines = data.split(b'\n')
print(f'Total lines: {len(lines)}')

# Check line 5791
line = lines[5790]
print(f'\nLine 5791 ({len(line)} bytes):')
print(f'  First 10 bytes: {line[:10]}')
print(f'  First char code: {line[0] if line else None}')
print(f'  As utf-8 text: {line.decode("utf-8", errors="replace")[:80]}')

# Check line 5799
line2 = lines[5798]
print(f'\nLine 5799 ({len(line2)} bytes):')
print(f'  First 10 bytes: {line2[:10]}')
print(f'  As utf-8 text: {line2.decode("utf-8", errors="replace")[:80]}')

# Check line 5807
line3 = lines[5806]
print(f'\nLine 5807 ({len(line3)} bytes):')
print(f'  As utf-8 text: {line3.decode("utf-8", errors="replace")[:80]}')

# Find unmatched quotes by scanning from line 5788
print('\n--- Scanning lines 5788-5810 for string issues ---')
for i in range(5787, 5810):
    l = lines[i]
    text = l.decode('utf-8', errors='replace')
    print(f'{i+1}: {repr(text)}')
