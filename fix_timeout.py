# -*- coding: utf-8 -*-
"""修复 call_ai 超时设置"""

app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 将超时从 90 秒改为 180 秒
content = content.replace(
    'with urllib.request.urlopen(req, timeout=90) as resp:',
    'with urllib.request.urlopen(req, timeout=180) as resp:'
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: call_ai timeout 90s -> 180s")
