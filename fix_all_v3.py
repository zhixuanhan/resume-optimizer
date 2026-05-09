import re, ast

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} chars")

# 找 career_analysis 函数：用字节位置而不是 regex
# 找 "def career_analysis" 后面第一个 app = Flask
idx = content.find("def career_analysis():")
if idx == -1:
    print("ERROR: career_analysis not found")
    exit(1)

# 找 app = Flask
flask_idx = content.find("app = Flask(", idx)
if flask_idx == -1:
    flask_idx = content.find("app = Flask(__name__)")
if flask_idx == -1:
    print("ERROR: app = Flask not found")
    exit(1)

career_func = content[idx:flask_idx]
print(f"career_analysis: chars {idx} to {flask_idx}, length={len(career_func)}")

# 找 try:
try_idx = career_func.find("    try:")
if try_idx == -1:
    print("ERROR: try: not found")
    exit(1)
print(f"try: at offset {try_idx}")

# 找 except (在 try: 之后的第一个)
except_idx = career_func.find("\n    except ", try_idx + 10)
if except_idx == -1:
    print("ERROR: except not found")
    exit(1)
print(f"except: at offset {except_idx}")

# 重写 try 块内容
before_try = career_func[:try_idx + 6]  # up to "try:"
old_try_body = career_func[try_idx + 6:except_idx]
after_except = career_func[except_idx:]

# 处理 try 块体：把所有 8 空格的语句改成 12 空格
lines = old_try_body.split('\n')
new_lines = []
for line in lines:
    stripped = line.strip()
    if stripped == '':
        new_lines.append('')  # 保留空行，保持行号
    elif line.startswith('        ') and not line.startswith('            '):
        new_lines.append('            ' + line.lstrip())  # 8->12 spaces
    else:
        new_lines.append(line)

new_try_body = '\n'.join(new_lines)
new_career_func = before_try + '\n' + new_try_body + after_except

new_content = content[:idx] + new_career_func + content[flask_idx:]

# 语法检查
try:
    ast.parse(new_content)
    print("AST parse: OK")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    print(f"Text: {repr(e.text)}")
    lines_split = new_content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines_split), e.lineno+3)):
        marker = '>>> ' if i == e.lineno-1 else '    '
        print(f"{marker}{i+1}: {repr(lines_split[i][:100])}")
    exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("File written!")