# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Fix line 5329 (0-indexed: 5328)
# The line has the return statement and @app.route on the same line
# Split them into two separate lines
old = lines[5328]
print(f"Line 5329: {repr(old)}")

# The line should be split between the return statement and the decorator
# Find the position after the closing ) of jsonify
idx = old.find('})@app.route')
if idx != -1:
    # Split at the decorator
    lines[5328] = old[:idx+2] + '\n' + old[idx+2:]
    print("Fixed!")
else:
    print("Pattern not found, trying alternative...")
    # Maybe there's no closing })@app.route pattern
    for sep in ['})@app', ')@app', '}@app']:
        idx2 = old.find(sep)
        if idx2 != -1:
            lines[5328] = old[:idx2+2] + '\n' + old[idx2+2:]
            print(f"Fixed with sep: {repr(sep)}")
            break

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verify
with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8', errors='replace') as f:
    lines2 = f.readlines()
print(f"Lines 5329-5331 now:")
for i in range(5328, 5331):
    print(f"  {i+1}: {repr(lines2[i])}")