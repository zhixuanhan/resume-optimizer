# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'rb') as f:
    content = f.read()

# Find routes that call AI at module level or during request handling
import re

# Look for @app.route and what follows
routes = []
for m in re.finditer(r'@app\.route\([^)]{1,100}\)[^\n]{0,20}\ndef (\w+)', content):
    routes.append((m.group(1), m.start()))

print(f"Total routes found: {len(routes)}")
for name, pos in routes[:15]:
    print(f"  {name}")