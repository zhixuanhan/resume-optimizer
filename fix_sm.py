"""状态机：精确重建 career_analysis try 块缩进"""
import ast

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    raw = f.read()

lines = raw.split('\n')

# ========== 找函数范围 ==========
career_start = next(i for i, l in enumerate(lines) if l.strip() == 'def career_analysis():')
career_end = next(i for i in range(career_start+1, len(lines))
                  if lines[i].strip() and not lines[i].startswith('    '))

# ========== 找 try / except ==========
try_line = next(i for i in range(career_start, career_end) if lines[i].strip() == 'try:')
except_line = next(i for i in range(try_line+1, career_end)
                   if lines[i].strip().startswith('except '))
print(f"try L{try_line+1}, except L{except_line+1}")

# ========== 逐行状态机处理 try 块体 ==========
# 状态：
#   depth=0: try体基础（12空格）
#   depth=1: 在if/for/with/elif体内（16空格）
#   depth=2+:更深嵌套（20+空格）

new_lines = lines[:try_line+1]  # 到 try: 为止
depth = 0
i = try_line + 1

while i < except_line:
    raw_line = lines[i]
    stripped = raw_line.strip()

    if not stripped:
        new_lines.append(raw_line)
        i += 1
        continue

    # 判断这行是什么类型的语句
    first = stripped.split()[0]

    # 顶层的复合语句（直接在 try 体内的 if/with/for/elif/def）
    if first in ('if', 'for', 'while', 'with', 'elif', 'def'):
        # 复合语句本身：depth 保持，声明行在 depth*4+12
        target = 12 + depth * 4
        new_lines.append(' ' * target + stripped)
        # 下一行进入更深一层（除非是 elif/else）
        if first not in ('elif', 'def'):
            depth += 1
        # 如果是 elif，depth 不变（它和 if 同级）
        # 如果是 def，def 内部是另一个函数，暂时保持 depth
    elif first == 'else:':
        # else 和 if 同级，所以 depth 应该不变（或者 depth-1 因为 if 结束了）
        depth = max(0, depth - 1)
        target = 12 + depth * 4
        new_lines.append(' ' * target + stripped)
        depth += 1  # else 体内 depth+1
    elif first == 'return':
        target = 12 + depth * 4
        new_lines.append(' ' * target + stripped)
    elif stripped == 'pass':
        target = 12 + depth * 4
        new_lines.append(' ' * target + stripped)
    else:
        # 普通语句
        target = 12 + depth * 4
        new_lines.append(' ' * target + stripped)

    # 检测复合语句是否结束（下一行是回到上级缩进的内容）
    # 简单启发式：如果这行是复合语句（以:结尾），depth += 1 已处理
    # 如果是 return/赋值等语句，depth 不变
    i += 1

# 加上 except 和之后的内容
new_lines += lines[except_line:]

new_content = '\n'.join(new_lines)

# ========== 语法检查 ==========
try:
    ast.parse(new_content)
    print("AST OK!")
except SyntaxError as e:
    print(f"SyntaxError L{e.lineno}: {e.msg}")
    ls = new_content.split('\n')
    for j in range(max(0,e.lineno-5), min(len(ls), e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f"{m}{j+1}: {repr(ls[j][:120])}")
    exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Written!")