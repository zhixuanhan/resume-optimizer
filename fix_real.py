path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path,'rb') as f: raw = f.read()
lines_n = raw.split(b'\n')

def gi(line):
    s = line.lstrip(b'\r')
    n = 0
    for b in s:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

# 只修复L5317（return加4空格）和L5336/5347（with及body调整）
changes = {
    5317: 16,   # return jsonify - inside if body
    5336: 12,   # with open - sibling of if, at try body level
    5347: 16,   # session_data = json.load - inside with body
}

print("=== 修复前 ===")
for ln in sorted(changes.keys()):
    idx = ln - 1
    c = lines_n[idx]
    ind = gi(c)
    txt = c.rstrip(b'\r\n').decode('utf-8','replace').strip()
    print(f'L{ln}({ind}sp): {txt[:60]}')

for ln, new_ind in changes.items():
    idx = ln - 1
    c = lines_n[idx]
    # 提取行内容（去掉缩进+换行）
    content = c.rstrip(b'\r\n').lstrip(b' \t')
    lines_n[idx] = b' ' * new_ind + content + b'\r\n'
    old_ind = gi(c)
    print(f'L{ln}: {old_ind}sp -> {new_ind}sp: {content.decode("utf-8","replace").strip()[:50]}')

out = b'\n'.join(lines_n)
if not out.endswith(b'\n'):
    out += b'\n'
with open(path,'wb') as f:
    f.write(out)
print(f'\nWritten {len(out)} bytes')

# 编译测试
try:
    compile(out.decode('utf-8'), path, 'exec')
    print('COMPILE OK!')
except SyntaxError as e:
    print(f'SyntaxError L{e.lineno}: {e.msg}')
    ls = out.decode('utf-8').split('\n')
    for j in range(max(0,e.lineno-4), min(len(ls),e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f'{m}{j+1}: {repr(ls[j][:100])}')
