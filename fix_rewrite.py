"""
完全重写 career_analysis 函数的 try 块，智能追踪嵌套缩进。
原始文件 try 块内容缩进 8 空格（应为 12），嵌套 body 8 空格（应为 16）。
"""
import re, ast

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# 找 career_analysis 函数范围
career_start = None
career_end = None
for i, l in enumerate(lines):
    if l.strip() == 'def career_analysis():':
        career_start = i
    elif career_start is not None and l.strip() and not l.startswith('    ') and not l.startswith('\t') and l.strip()[0] not in ' \t\r\n#':
        # 顶级非空行（非缩进）
        if l.strip().startswith('def ') or l.strip().startswith('@') or l.strip().startswith('if ') or l.strip().startswith('class '):
            career_end = i
            break

if career_start is None or career_end is None:
    print(f"ERROR: career_start={career_start}, career_end={career_end}")
    exit(1)
print(f"Function lines {career_start+1} to {career_end} (0-idx: {career_start} to {career_end})")

# 找 try: 和 except:
try_line = except_line = None
for i in range(career_start, career_end):
    if lines[i].strip() == 'try:':
        try_line = i
    elif lines[i].strip().startswith('except ') and try_line is not None:
        except_line = i
        break

if try_line is None or except_line is None:
    print(f"ERROR: try={try_line}, except={except_line}")
    exit(1)
print(f"try at line {try_line+1}, except at line {except_line+1}")

# 缩进级别映射表（目标缩进相对于 try: 本身）
# try: 之后的缩进级别：
#   0 = 紧跟 try: 的语句（8空格原始，对应12目标）
#   1 = 嵌套在 if/for/with/elif 内的语句（12空格原始，对应16目标）
#   2 = 更深层嵌套（16空格原始）

COMPOUND_KEYWORDS = {'if', 'for', 'while', 'with', 'elif', 'else', 'try', 'except', 'finally', 'def'}

def get_target_indent(line, depth):
    """给定原始行的内容（stripped）和当前嵌套深度，返回目标缩进空格数"""
    if not line:
        return None  # 空行不处理缩进
    return depth

# 逐行处理 try 块
new_try_lines = []
depth = 0  # 当前嵌套深度
i = try_line + 1

while i < except_line:
    raw_line = lines[i]
    stripped = raw_line.strip()
    
    if stripped == '':
        # 空行：保留，但后续缩进行需要调整
        new_try_lines.append(raw_line)
        i += 1
        continue
    
    # 确定这行是干什么的
    first_word = stripped.split()[0] if stripped else ''
    
    if first_word in COMPOUND_KEYWORDS:
        # 复合语句（if/for/with/def 等）：深度不变，下一行深度+1
        target_indent = 12  # 12 spaces for compound statement inside try
        new_try_lines.append(' ' * target_indent + stripped)
        depth += 1
    elif stripped.startswith('#'):
        # 注释：保持同级缩进
        new_try_lines.append(' ' * (12 + depth * 4) + stripped)
    elif first_word in ('return', 'break', 'continue', 'pass'):
        # 简单语句：当前深度缩进
        target_indent = 12 + depth * 4
        new_try_lines.append(' ' * target_indent + stripped)
    else:
        # 普通语句或赋值表达式：当前深度缩进
        target_indent = 12 + depth * 4
        new_try_lines.append(' ' * target_indent + stripped)
    
    i += 1

# 组装新的函数内容
new_func_lines = lines[career_start:try_line+1] + new_try_lines + lines[except_line:]
# 在 try: 后面加一个空行
new_func = '\n'.join(new_func_lines) + '\n'

# 替换原函数
new_content = '\n'.join(lines[:career_start]) + '\n' + new_func + '\n'.join(lines[career_end:])

# 语法检查
try:
    ast.parse(new_content)
    print("AST parse: OK!")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    ls = new_content.split('\n')
    for j in range(max(0,e.lineno-5), min(len(ls), e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f"{m}{j+1}: {repr(ls[j][:120])}")
    exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("File written successfully!")