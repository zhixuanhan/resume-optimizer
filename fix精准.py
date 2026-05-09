"""精准修复 career_analysis 函数的三处缩进问题"""
import ast

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

changes = []

# 1. Line 5317: return jsonify(...) 应该是 16 空格（if 块内），当前 12
# 2. Line 5333: with open(...) 应该是 16 空格（else 块），当前 12
# 3. Line 5882: except Exception as e: 应该是 12 空格（与 try 同级），当前 8

fixes = {
    5317: 16,  # return jsonify(...) in if block
    5333: 16,  # with open(...) in else block  
    5882: 12,  # except clause
}

for lineno_1based, target_spaces in fixes.items():
    idx = lineno_1based - 1
    line = lines[idx]
    stripped = line.rstrip('\r\n')
    current_spaces = len(line) - len(line.lstrip())
    if current_spaces != target_spaces:
        lines[idx] = ' ' * target_spaces + stripped + '\n'
        changes.append(f"Line {lineno_1based}: {current_spaces}sp -> {target_spaces}sp")
        print(f"Fixed line {lineno_1based}: {current_spaces}sp -> {target_spaces}sp: {repr(stripped[:60])}")
    else:
        print(f"Line {lineno_1based}: already correct ({current_spaces}sp)")

new_content = '\n'.join(lines)

# 语法检查
try:
    ast.parse(new_content)
    print("\nAST parse: OK!")
except SyntaxError as e:
    print(f"\nSyntaxError at line {e.lineno}: {e.msg}")
    ls = new_content.split('\n')
    for j in range(max(0, e.lineno-5), min(len(ls), e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f"{m}{j+1}: {repr(ls[j][:120])}")
    exit(1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"\nDone! Fixed {len(changes)} lines.")