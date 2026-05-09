# -*- coding: utf-8 -*-
content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()
import re

# Find the /api/optimize route - search more carefully
# It's at approximately position 34983 based on earlier check
search = "@app.route('/api/optimize'"
idx = content.find(search)
print('Found at:', idx)

if idx >= 0:
    end = idx + 5000
    # Find the next @app.route after this one
    next_route = content.find("\n@app.route('", idx + 10)
    if next_route > idx and next_route < idx + 5000:
        end = next_route
    print(content[idx:end])