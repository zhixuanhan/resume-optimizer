import re

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ========== 1. 检查 call_ai 重试逻辑是否完整 ==========
# 现在 call_ai 应该有 for attempt in range(2) 了
# 找 call_ai 函数结束位置（下一个顶级 def 或 app = Flask）
call_ai_match = re.search(r"def call_ai\([\s\S]*?def [a-zA-Z_]\w+\(|$", content)
if call_ai_match:
    end_pos = call_ai_match.end()
    func_body = content[content.find("def call_ai("):end_pos]
    has_for_loop = "for attempt in range(2)" in func_body
    has_except_socket = "socket.timeout" in func_body
    print(f"call_ai has for loop: {has_for_loop}, has socket.timeout: {has_except_socket}")

# ========== 2. 修复 career_analysis 函数的缩进 ==========
# 找到 career_analysis 函数开始和结束
career_start = content.find("def career_analysis():")
app_flask = content.find("app = Flask(__name__)")
career_end = app_flask

if career_start == -1:
    print("ERROR: career_analysis not found")
    exit(1)

func = content[career_start:career_end]
print(f"career_analysis length: {len(func)}")

# 找 try 块开始和结束
try_start_in_func = func.find("    try:")
if try_start_in_func == -1:
    print("ERROR: try: not found in career_analysis")
    exit(1)

# 找 except
except_match = re.search(r"\n    except ", func[try_start_in_func+10:])
if except_match:
    try_end_in_func = try_start_in_func + except_match.start()
    print(f"try block: {try_start_in_func} to {try_end_in_func}")
else:
    print("ERROR: except not found")
    exit(1)

# 在 try 块内，所有应该缩进的内容应该是 12 空格
# 当前 8 空格缩进的语句需要改成 12
try_block = func[try_start_in_func:try_end_in_func]
func_before_try = func[:try_start_in_func+7]  # up to "try:"

# 重新处理 try 块内容
# 去掉原来多余的空行，重新整理缩进
# 保留：try: 之后的内容缩进 12 空格
lines_in_try = try_block[7:].split('\n')  # 去掉 'try:\n'
new_try_lines = []
for line in lines_in_try:
    stripped = line.strip()
    if stripped == '':
        new_try_lines.append('')
    elif line.startswith('        ') and not line.startswith('            '):
        # 8 spaces -> 12 spaces
        new_try_lines.append('            ' + line.lstrip())
    elif line.startswith('    ') and not line.startswith('        '):
        # 4 spaces -> this is top-level, shouldn't be in try
        # 但如果这是 try 块的唯一内容缩进...
        new_try_lines.append(line)
    else:
        new_try_lines.append(line)

new_try_block = '\n'.join(new_try_lines)
new_career_func = func_before_try + '\n' + new_try_block

# 加上 except 块
except_block = func[try_end_in_func:]
new_career_func = new_career_func + except_block

new_content = content[:career_start] + new_career_func + content[career_end:]

# ========== 3. 检查整体语法 ==========
import ast
try:
    ast.parse(new_content)
    print("AST parse: OK")
except SyntaxError as e:
    print(f"SyntaxError at line {e.lineno}: {e.msg}")
    print(f"Text: {repr(e.text)}")
    lines = new_content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+3)):
        marker = '>>> ' if i == e.lineno-1 else '    '
        print(f"{marker}{i+1}: {repr(lines[i][:100])}")
    exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("File written successfully!")