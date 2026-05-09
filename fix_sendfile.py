# -*- coding: utf-8 -*-
"""Fix the send_file syntax error and resume optimization issues"""
import re

app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
print(f"Original: {original_len} chars, {content.count(chr(10))} lines")

# Check syntax before fix
import ast
try:
    ast.parse(content)
    print("Already valid Python!")
except SyntaxError as e:
    print(f"Before fix: SyntaxError at line {e.lineno}: {e.msg}")

# FIX 1: Add closing ) after line 5807's mimetype line
# The send_file( opened at line 5791 is never closed.
# Line 5807 ends with "mimetype='text/markdown')" — this closes the mimetype
# string but NOT the send_file(.
# We need an additional ) after it.
old_mimetype_line = "                    mimetype='text/markdown')\n"
new_mimetype_lines = "                    mimetype='text/markdown'\n                    )\n"

if old_mimetype_line in content:
    content = content.replace(old_mimetype_line, new_mimetype_lines, 1)
    print("FIX 1: Added closing ) for send_file()")
else:
    print("FIX 1: Could not find mimetype line — checking...")
    # Try without trailing newline
    idx = content.find("mimetype='text/markdown')")
    if idx >= 0:
        print(f"  Found at index {idx}: {repr(content[idx:idx+50])}")

# Check syntax after fix
try:
    ast.parse(content)
    print("After fix: Syntax OK!")
except SyntaxError as e:
    print(f"After fix: Still SyntaxError at line {e.lineno}: {e.msg}")
    lines = content.split('\n')
    start = max(0, e.lineno - 5)
    for i in range(start, min(len(lines), e.lineno + 3)):
        marker = '>>> ' if i == e.lineno - 1 else '    '
        print(f"  {i+1}: {marker}{repr(lines[i][:80])}")

# Write if fixed
try:
    ast.parse(content)
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"File written: {len(content)} chars, {content.count(chr(10))} lines")
except SyntaxError as e:
    print(f"Could not fix: {e.msg}")
