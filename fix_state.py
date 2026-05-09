"""精准修复 career_analysis 函数所有缩进问题"""
import ast

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 策略：从 try: 之后，逐行用状态机追踪缩进深度
# 状态：当前应该在几空格
# Compound语句(if/for/with/def等)：保持在当前深度，下一行+4
# 空行：跳过
# 普通语句：在当前深度

state_depth = 0  # 0=try体(12空格基础)，1=if/with体(16空格)
# 注意：12空格对应depth=0，16空格对应depth=1
STATE_BASE = 12  # 基础缩进

state = 0  # 0=looking for first non-empty, 1=in compound body, 2=regular

# 找 career_analysis 的 try 块
career_start = None
for i, l in enumerate(lines):
    if l.strip() == 'def career_analysis():':
        career_start = i
        break

if career_start is None:
    print("ERROR: career_analysis not found")
    exit(1)

# 找 try: 和 except:
try_line = except_line = None
for i in range(career_start, len(lines)):
    if lines[i].strip() == 'try:':
        try_line = i
    elif lines[i].strip().startswith('except ') and try_line is not None:
        except_line = i
        break

print(f"try at line {try_line+1}, except at line {except_line+1}")

# 逐行处理
i = try_line + 1
state = 0  # 0=in compound/looking for content, 1=in body
depth = 0  # 0=try body, 1=nested in if/with/for
changes = []

while i < except_line:
    raw = lines[i]
    # 原始空格数
    orig_spaces = len(raw) - len(raw.lstrip())
    stripped = raw.strip()
    
    if stripped == '':
        # 空行：保留，但重置 state
        state = 0
        i += 1
        continue
    
    first_word = stripped.split()[0] if stripped else ''
    COMPOUND = {'if', 'for', 'while', 'with', 'elif', 'else:', 'try:', 'except', 'finally', 'def', 'class'}
    is_compound = first_word in COMPOUND and not stripped.startswith('#')
    
    if state == 0:
        # 刚进入 try 块或刚结束一个子块，等待内容
        if is_compound:
            # 这是 try 块内的第一个语句（if/for/with等）
            target = 12  # 12 spaces
            state = 1  # next content is in body
            depth = 1  # now in nested block
        else:
            # 简单语句
            target = 12
            state = 0  # stay
    else:
        # 在复合语句体内（depth >= 1）
        if is_compound:
            target = 12 + depth * 4
            depth += 1
        elif stripped in ('pass', 'break', 'continue'):
            target = 12 + depth * 4
        elif stripped.startswith('return ') or stripped.startswith('return"') or stripped.startswith("return'"):
            target = 12 + depth * 4
        elif first_word == 'return':
            target = 12 + depth * 4
        else:
            # 普通语句或赋值
            target = 12 + depth * 4
            # 如果这行后面跟了复合语句，depth 不变（depth在下一行+1）
            # 如果是语句结束（比如 `}), 404` 或 `]),`），保持当前 depth
    
    # 但要注意：某些行的 first_word 不在 COMPOUND 里但也是多行结构的一部分
    # 比如 `}), 404` 或 `"available_jobs": list(...)` 这些应该维持当前 depth
    
    if orig_spaces != target:
        new_line = ' ' * target + stripped
        lines[i] = new_line + '\n'
        changes.append(f"L{i+1}: {orig_spaces}sp->{target}sp: {repr(stripped[:50])}")
        print(f"  Fixed L{i+1}: {orig_spaces}sp -> {target}sp: {repr(stripped[:50])}")
    else:
        print(f"  OK   L{i+1}: {target}sp: {repr(stripped[:50])}")
    
    # 如果是复合语句（if/for/with等），下一行深度+1
    if is_compound and stripped not in ('else:', 'elif ', 'except ', 'finally:', 'def ', 'class '):
        # 特殊处理：检查是否以冒号结尾
        if stripped.endswith(':'):
            depth += 1
            state = 0
        else:
            pass
    elif is_compound and stripped in ('else:', 'elif ', 'except ', 'finally:'):
        # else/elif/except 保持同级
        depth = max(0, depth - 1)  # pop one level
    
    i += 1

print(f"\nTotal changes: {len(changes)}")

# 写回
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# 语法检查
new_content = ''.join(lines)
try:
    ast.parse(new_content)
    print("AST parse: OK!")
except SyntaxError as e:
    print(f"\nSyntaxError at line {e.lineno}: {e.msg}")
    ls = new_content.split('\n')
    for j in range(max(0, e.lineno-5), min(len(ls), e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f"{m}{j+1}: {repr(ls[j][:120])}")
    exit(1)

print("File written!")