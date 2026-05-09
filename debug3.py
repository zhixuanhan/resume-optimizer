# -*- coding: utf-8 -*-
import ast
app_path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

try:
    ast.parse(content)
    print('Syntax OK!')
except SyntaxError as e:
    print(f'Error: {e.msg}')
    print(f'Line {e.lineno}, offset {e.offset}')
    lines = content.split('\n')
    start = max(0, e.lineno - 10)
    end = min(len(lines), e.lineno + 5)
    for i in range(start, end):
        marker = '>>> ' if i == e.lineno - 1 else '    '
        print(f'{i+1:4d}: {marker}{repr(lines[i])}')
    
    # Check line before error for quote issues
    prev_line = lines[e.lineno - 2] if e.lineno > 1 else ''
    print(f'\nLine before error ({e.lineno}): {repr(prev_line)}')
