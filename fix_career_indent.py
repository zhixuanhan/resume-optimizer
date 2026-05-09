import re

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 if/elif/else/for/while/with 块体缩进
# 在 try 块内，所有块体应该是 12 空格（原来是 8）
# 策略：在 try: 之后，所有 8 空格的非空行如果是语句开头，改成 12 空格
# 但要注意函数定义等不应该被改

# 更安全的方法：找所有 '        if ' / '        return ' / '        with ' / '        for ' 等
# 这些是 try 块内的语句，应该缩进到 12 空格

# 先找到 call_ai 函数结束的位置（app = Flask(__之前）
# 然后处理 career_analysis 函数

# 精确定位 career_analysis 函数内容并重写
# 找到 def career_analysis 到下一个 def 或 @app

# 找到所有需要缩进的语句（8空格开头，顶级语句）
old_content = content

# 找 career_analysis 函数区域
start_marker = "def career_analysis():"
end_marker = "app = Flask(__name__)"
start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"ERROR: start={start_idx}, end={end_idx}")
    exit(1)

print(f"career_analysis region: {start_idx} to {end_idx}")

# 提取函数内容
func_content = content[start_idx:end_idx]
print(f"Function content length: {len(func_content)}")

# 重写函数内容：去掉所有多余的空白行，并修正缩进
lines = func_content.split('\n')
new_lines = []
in_try = False
try_depth = 0
for line in lines:
    stripped = line.strip()
    
    if stripped == 'try:':
        in_try = True
        new_lines.append(line)  # try: 保持原样
        continue
    
    if stripped.startswith('except ') or stripped.startswith('finally:'):
        in_try = False
        new_lines.append(line)
        continue
    
    if not in_try:
        new_lines.append(line)
        continue
    
    # 现在在 try 块内
    if stripped == '':
        new_lines.append(line)
        continue
    
    # 非空行，检查缩进
    # 如果是 8 空格开头（4 space indent），改成 12 空格（6 space indent）
    if line.startswith('        ') and not line.startswith('            '):
        # 8 spaces → 12 spaces
        new_lines.append('            ' + line.lstrip())
    elif line == 'def career_analysis():' or line.startswith('def '):
        # 函数定义行，保持
        new_lines.append(line)
    else:
        new_lines.append(line)

new_func_content = '\n'.join(new_lines)
print("New function content preview:")
print(new_func_content[:500])
print("...")
print(new_func_content[-200:])

# 替换回原内容
new_content = content[:start_idx] + new_func_content + content[end_idx:]

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\nFile written. Old length: {len(content)}, New length: {len(new_content)}")
