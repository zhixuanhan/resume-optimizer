# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'rb') as f:
    lines_raw = f.read().split(b'\n')

# Check line 4291 (the unclosed prompt = f""" start)
print("=== Line 4291 ===")
print(repr(lines_raw[4290][:200]))

# What closes the prompt on line 4291? Let's check subsequent lines.
# The prompt should end with """ on some later line
# Check lines 4291 onwards for the closing tq
print("\n=== Lines 4291-4310 ===")
for i in range(4290, 4310):
    print(f"Line {i+1:4d}: {repr(lines_raw[i][:120])}")

# Check if line 4291 has "f""" (f-string with triple quote)
print("\n=== Line 4291 bytes analysis ===")
line_4291 = lines_raw[4290]
print(f"Length: {len(line_4291)}")
print(f"Hex: {line_4291.hex()[:60]}")
# Check for f"""
for j in range(len(line_4291)-3):
    if line_4291[j:j+3] == b'f"""' or line_4291[j:j+3] == b'"""':
        print(f"  Quote at byte {j}: {repr(line_4291[j:j+3])}")