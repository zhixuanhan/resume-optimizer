# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    raw = f.read()
lines_raw = raw.split(b'\n')

# Check line 9 in detail
print("Line 9:", repr(lines_raw[8][:50]))
print()

# Check lines around 33 (which closes line 9's tq)
print("Lines 33-36:")
for i in [32, 33, 34, 35]:
    print(f"  {i+1}: {repr(lines_raw[i][:80])}")

# Find all lines with tq=1 (unclosed potential)
print("\n=== Lines with single triple quote (unclosed start candidates) ===")
for i, line in enumerate(lines_raw):
    if b'\x22\x22\x22' in line:
        positions = [j for j in range(len(line)-2) if line[j:j+3]==b'\x22\x22\x22']
        if len(positions) % 2 != 0:
            text = line.decode('utf-8', errors='replace')
            print(f"Line {i+1:4d}: {positions} = {text[:80]}")

# Total tq count in file
total = sum(b'\x22\x22\x22' in line for line in lines_raw)
print(f"\nTotal triple-quote occurrences: {total}")
print(f"Balance (should be even): {total % 2}")