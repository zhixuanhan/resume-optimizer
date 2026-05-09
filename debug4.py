# -*- coding: utf-8 -*-
# Find unmatched single quotes in the file
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Look for lines starting with a single quote
print("Lines starting with single quote character:")
for i, line in enumerate(lines):
    if line.startswith("'"):
        print(f"  Line {i+1}: {repr(line[:80])}")
        
# Also look for lines that look like they start a string but don't end properly
# Check around line 5791 and 5799
print("\nLines 5788-5808:")
for i in range(5787, 5808):
    print(f"  {i+1}: {repr(lines[i])}")
