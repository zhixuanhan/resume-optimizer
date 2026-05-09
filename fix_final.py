import re, ast

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# 找 career_analysis 函数开始行 (1-indexed: 5260, 0-indexed: 5259)
career_start = None
for i, l in enumerate(lines):
    if l.strip() == 'def career_analysis():':
        career_start = i
        break

if career_start is None:
    print("ERROR: career_analysis not found")
    exit(1)
print(f"career_analysis starts at line {career_start+1}")

# 找 career_analysis 函数结束（下一个同缩进的 def）
career_end = None
for i in range(career_start + 1, len(lines)):
    l = lines[i].rstrip('\r')
    # 顶级 def: 4 spaces indent
    if l.startswith('def ') and not l.startswith('    def '):
        career_end = i
        break

if career_end is None:
    career_end = len(lines)
print(f"career_analysis ends at line {career_end+1}")

# 在函数内找 try: 和 except:
try_line = None
for i in range(career_start, career_end):
    if lines[i].strip() == 'try:':
        try_line = i
        break

if try_line is None:
    print("ERROR: try: not found")
    exit(1)
print(f"try: at line {try_line+1}")

except_line = None
for i in range(try_line + 1, career_end):
    if lines[i].strip().startswith('except '):
        except_line = i
        break

if except_line is None:
    print("ERROR: except not found")
    exit(1)
print(f"except at line {except_line+1}")

# 重写 try 块内容
# 把 try_line+1 到 except_line-1 的内容，8空格改成12空格
changed = []
for i in range(try_line + 1, except_line):
    line = lines[i]
    stripped = line.strip()
    if stripped == '':
        changed.append(i)  # 空行保留
    elif line.startswith('        ') and not line.startswith('            '):
        lines[i] = '            ' + line.lstrip()
        changed.append(i)

print(f"Changed {len(changed)} lines: {changed}")

# 写回
with open(path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

# 语法检查
try:
    ast.parse('\n'.join(lines))
    print("AST parse: OK")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    ls = '\n'.join(lines).split('\n')
    for i in range(max(0,e.lineno-5), min(len(ls), e.lineno+3)):
        m = '>>> ' if i == e.lineno-1 else '    '
        print(f"{m}{i+1}: {repr(ls[i][:100])}")