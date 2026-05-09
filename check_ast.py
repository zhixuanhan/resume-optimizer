import ast, traceback

try:
    with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
        source = f.read()
    ast.parse(source)
    print('AST parse: OK')
except SyntaxError as e:
    print(f'SyntaxError at line {e.lineno}: {e.msg}')
    print(f'Text: {repr(e.text)}')
    # 显示错误行前后10行
    lines = source.split('\n')
    start = max(0, e.lineno - 10)
    end = min(len(lines), e.lineno + 5)
    for i in range(start, end):
        marker = '>>> ' if i == e.lineno - 1 else '    '
        print(f'{marker}{i+1}: {repr(lines[i])}')
