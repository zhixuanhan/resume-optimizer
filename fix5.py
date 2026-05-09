"""精确修复4行 - 用 \n 分割并 strip \r"""
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(path, 'rb') as f:
    raw = f.read()

# 用 \n 分割，保留 \r 在行末（后面 strip 掉）
lines = raw.split(b'\n')  # 每行含 \r\n 结尾或纯内容

def gi(line):
    """获取缩进字节数（去掉行尾 \r）"""
    c = line.rstrip(b'\r')
    n = 0
    for b in c:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

def set_indent(line, new_indent):
    """设置行缩进"""
    c = line.rstrip(b'\r')
    s = c.lstrip()
    return b' ' * new_indent + s + b'\r\n'

def content(line):
    return line.rstrip(b'\r').decode('utf-8','replace').strip()

# 检查行 5317, 5333, 5342, 5882
print("=== 当前状态 ===")
for idx in [5317-1, 5333-1, 5342-1, 5882-1]:
    if idx < len(lines):
        c = lines[idx]
        print(f'L{idx+1} ({gi(c):3d}sp): {content(c)[:65]}')

print("\n=== 修复 ===")
fixes = {
    5317-1: 12,  # return jsonify (from 28)
    5333-1: 12,  # with open (from 24)
    5342-1: 12,  # session_data (from 24)
    5882-1: 8,   # except Exception (from 12)
}
changed = []
for idx, target in fixes.items():
    if idx < len(lines):
        old_indent = gi(lines[idx])
        if old_indent != target:
            old = content(lines[idx])[:50]
            lines[idx] = set_indent(lines[idx], target)
            changed.append((idx+1, old_indent, target, old))
        else:
            changed.append((idx+1, old_indent, target, 'OK'))

for c in changed:
    print(f'L{c[0]:4d}: {c[1]:3d}sp -> {c[2]:3d}sp: {c[3][:55]}')

# 写回（用 \n 分隔）
out = b'\n'.join(lines)
# 确保末尾有换行符
if not out.endswith(b'\n'):
    out += b'\n'
with open(path, 'wb') as f:
    f.write(out)
print(f'\nWritten {len(out)} bytes')
