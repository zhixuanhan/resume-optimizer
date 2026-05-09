# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Find all @app.route and def lines
print("=== ALL ROUTES ===")
for i, line in enumerate(lines):
    if '@app.route' in line:
        print(f'{i+1}: {repr(line.rstrip())}')

print()
print("=== ALL DEF LINES ===")
for i, line in enumerate(lines):
    if line.strip().startswith('def '):
        print(f'{i+1}: {repr(line.rstrip())}')
