"""用 tokenize 模块精确重建 career_analysis 函数"""
import tokenize, io

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'rb') as f:
    tokens = list(tokenize.tokenize(f.readline))

# 找 career_analysis 函数的 token 范围
func_start = func_end = None
# 函数名 token 的位置
for i, tok in enumerate(tokens):
    if tok.type == tokenize.NAME and tok.string == 'career_analysis':
        # 往前找 def
        for j in range(i-1, -1, -1):
            if tokens[j].string == 'def':
                func_start = tokens[j].start[0]  # line number
                break
        break

if func_start is None:
    print("ERROR: career_analysis not found")
    exit(1)
print(f"Function starts at line {func_start}")

# 函数结束：下一个同级或更外层的 def/class/async
# 找下一个缩进 <= 函数定义缩进的 def
func_indent = None
for i, tok in enumerate(tokens):
    if tok.string == 'career_analysis' and tokens[i-1].string == 'def':
        # 找这个 def 行的缩进
        # 需要往前找到行首
        line_num = tok.start[0]
        indent = 0
        for j in range(i-2, -1, -1):
            if tokens[j].start[0] < line_num:
                break
            if tokens[j].type == tokenize.INDENT:
                indent = tok.start[1] - tokens[j].string.__len__() if hasattr(tokens[j].string, '__len__') else 1
                break
        func_indent = tok.start[1]
        print(f"Function indent: {func_indent}")
        break

# 找函数结束（下一个同级或更外层的 def）
depth = 0
func_end = None
for i, tok in enumerate(tokens):
    if tok.type in (tokenize.INDENT, tokenize.DEDENT):
        continue
    if tok.start[0] > func_start:
        if tok.string == 'def' and tok.type == tokenize.NAME:
            # 找这个 def 的缩进
            line_toks = [t for t in tokens if t.start[0] == tok.start[0]]
            this_indent = tok.start[1]
            if this_indent <= func_indent:
                func_end = tok.start[0]
                print(f"Function ends at line {func_end} (next def at indent {this_indent})")
                break

if func_end is None:
    func_end = tokens[-1].start[0] + 1
    print(f"Function ends at line {func_end} (EOF)")

# 提取函数 token 并重建
func_tokens = []
in_func = False
for tok in tokens:
    if tok.start[0] == func_start:
        in_func = True
    if in_func:
        func_tokens.append(tok)
    if in_func and tok.start[0] >= func_end:
        break

# 重建代码（保留原始缩进和格式）
# 用原始文本行来重建
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 用 token 信息修正缩进
# 对于 career_analysis 函数体：
# try: 12空格
# try块内: 12 + depth*4 空格

# 找 try: 和 except: 的行号
try_line = except_line = None
for i, l in enumerate(lines):
    if l.strip() == 'try:' and i >= func_start:
        try_line = i
    if l.strip().startswith('except ') and try_line is not None:
        except_line = i
        break

print(f"try at line {try_line+1}, except at line {except_line+1}")

# 重建 try 块体
# 用缩进状态机
depth = 0  # 当前深度（0=try体基础12空格）
state_block_stack = []  # 记录当前在哪个块里（if/for/with等）

new_try_lines = []
for lineno in range(try_line+1, except_line):
    line = lines[lineno]
    stripped = line.strip()
    
    if stripped == '':
        new_try_lines.append((lineno, line))
        continue
    
    first_word = stripped.split()[0]
    
    # compound 语句：if/for/while/with/def/elif/else:/except/finally
    is_compound = first_word in ('if', 'for', 'while', 'with', 'def', 'elif', 'else', 'except', 'finally', 'try')
    ends_block = stripped in ('pass',) or stripped.startswith('return ') or (first_word == 'return')
    
    if stripped.endswith(':') and not stripped.startswith('#'):
        # 复合语句头
        target = 12 + depth * 4
        new_try_lines.append((lineno, ' ' * target + stripped + '\n'))
        if first_word not in ('elif', 'def'):
            depth += 1
        state_block_stack.append(first_word)
    elif first_word in ('elif', 'else:', 'except '):
        # 跳出当前块，进入同级
        depth = max(0, depth - 1)
        target = 12 + depth * 4
        new_try_lines.append((lineno, ' ' * target + stripped + '\n'))
        if first_word in ('else:', 'except '):
            depth += 1
    elif is_compound:
        target = 12 + depth * 4
        new_try_lines.append((lineno, ' ' * target + stripped + '\n'))
    elif ends_block:
        target = 12 + depth * 4
        new_try_lines.append((lineno, ' ' * target + stripped + '\n'))
        # return 之后可能跟 else 等
    else:
        target = 12 + depth * 4
        new_try_lines.append((lineno, ' ' * target + stripped + '\n'))

# 现在统计需要修复的行
for lineno, line in new_try_lines:
    orig_spaces = len(lines[lineno]) - len(lines[lineno].lstrip())
    new_spaces = len(line) - len(line.lstrip())
    if orig_spaces != new_spaces:
        lines[lineno] = line

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

# 语法检查
new_content = ''.join(lines)
try:
    compile(new_content, path, 'exec')
    print("COMPILE OK!")
except SyntaxError as e:
    print(f"SyntaxError L{e.lineno}: {e.msg}")
    ls = new_content.split('\n')
    for j in range(max(0,e.lineno-3), min(len(ls), e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f"{m}{j+1}: {repr(ls[j][:120])}")