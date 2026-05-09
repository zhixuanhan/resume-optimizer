# -*- coding: utf-8 -*-
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Line 5807 (0-indexed = 5806)
print('Line 5807:', repr(lines[5806]))
print('Line 5808:', repr(lines[5807]))

# Check if already fixed
if "                    )\n" in lines[5807]:
    print('Already fixed!')
else:
    # The line ends with "mimetype='text/markdown')\n" 
    # We need to change it to: mimetype='text/markdown'\n                    )\n
    old = "                    mimetype='text/markdown')\n"
    new = "                    mimetype='text/markdown'\n                    )\n"
    
    if old in lines[5806]:
        lines[5806] = new
        print('Fixed!')
    else:
        print('Pattern not found! Trying other variant...')
        # Check what's actually there
        for i in range(5805, 5810):
            print(f"  Line {i+1}: {repr(lines[i])}")

with open(app_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('File written!')

# Verify syntax
import ast
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()
try:
    ast.parse(content)
    print("SYNTAX OK!")
except SyntaxError as e:
    print(f"Still broken: {e.msg} at line {e.lineno}")