with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# career_analysis 的 try 块在 line 5264 (0-indexed 5263)
# line 5269: '    data = request.json\n' 应该是 '        data = request.json\n'
# try块内容应该是缩进8个空格

# 从 line 5264 的 try: 往下找到第一个非空行，应该缩进8个空格
# 找 try: 之后的连续内容直到下一个非空行
try_start = 5263  # 0-indexed, line 5264

# 从 try_start+1 开始，找所有应该缩进的内容
# 根据之前的读取，内容应该缩进8个空格
# 我们在 try: 之后插入适当的内容

# 更好的方法：重新构建 try 块
# 找到 try: 的位置，然后找到 except 或者 return 之前的缩进

# 找 line 5269 之后的内容，确定哪些行需要缩进
# 当前的错误：5269 '    data = request.json' 缩进4个空格，应该是8个

# 需要缩进8个空格的行（当前是4个空格的行，从5269到下一个非空内容）
# 根据代码逻辑，try块内容应该从第8个空格开始

lines_to_fix = []
for i in range(try_start + 1, len(lines)):
    line = lines[i]
    if line.strip() == '' or line.strip() == '\n':
        continue
    # 如果是纯空格或空行，跳过
    stripped = line.lstrip()
    if stripped == '':
        continue
    # 检查缩进：如果以4个空格开头，应该改成8个
    if line.startswith('    ') and not line.startswith('        '):
        indent = len(line) - len(line.lstrip())
        if indent == 4:
            lines[i] = '        ' + line.lstrip()
            lines_to_fix.append(i+1)
    # 如果遇到 except: 说明 try 块结束了
    if stripped.startswith('except '):
        break

print(f'Fixed indentation on lines: {lines_to_fix}')

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done')
