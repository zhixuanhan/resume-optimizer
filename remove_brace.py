# -*- coding: utf-8 -*-
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Remove line 1180 (index 1179) - the extra })
del lines[1179]

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.writelines(lines)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import ast
try:
    compile(content, path, 'exec')
    print('SYNTAX OK')
except SyntaxError as e:
    print(f'Still error at line {e.lineno}: {e.msg}')
