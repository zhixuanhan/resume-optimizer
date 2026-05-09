"""精确修复7行缩进"""
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixes = {
    5317: 16,  # return in "if not os.path.exists" body
    5333: 16,  # with open(...) in else block
    5341: 16,  # session_data = json.load in with body
    5405: 16,  # return jsonify in "if not career_info" body
    5413: 16,  # "error": f"... in return body
    5429: 16,  # }), 404 in return body
    5882: 12,  # except clause (same level as try)
}

changed = []
for lineno, target in fixes.items():
    idx = lineno - 1
    stripped = lines[idx].rstrip('\r\n')
    current = len(lines[idx]) - len(lines[idx].lstrip())
    if current != target:
        lines[idx] = ' ' * target + stripped + '\n'
        changed.append((lineno, current, target, stripped[:50]))
        print(f"L{lineno}: {current}sp -> {target}sp: {repr(stripped[:50])}")
    else:
        print(f"L{lineno}: already {target}sp")

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n{len(changed)} lines fixed.")

# 编译测试
import ast
new_content = ''.join(lines)
try:
    ast.parse(new_content)
    print("AST OK!")
except SyntaxError as e:
    print(f"SyntaxError L{e.lineno}: {e.msg}")
    ls = new_content.split('\n')
    for j in range(max(0, e.lineno-4), min(len(ls), e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f"{m}{j+1}: {repr(ls[j][:120])}")