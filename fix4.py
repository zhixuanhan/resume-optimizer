"""精确修复4行 - 不动其他内容"""
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'

with open(path, 'rb') as f:
    raw = f.read()

# 按 CRLF 分割行
lines = raw.split(b'\r\n')  # 正确处理 Windows CRLF

def gi(line):
    """获取缩进字节数"""
    c = line.rstrip(b'\r\n')
    n = 0
    for b in c:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

def set_indent(line, new_indent):
    """设置行缩进为指定空格数，保留内容"""
    c = line.rstrip(b'\r\n')
    s = c.lstrip()  # 去掉现有缩进
    si = len(c) - len(s)
    # 计算需要的空格
    new_c = b' ' * new_indent + s
    return new_c + b'\r\n'

# 检查当前状态
print("=== 当前状态 ===")
for idx in [5309, 5317, 5333, 5342]:
    if idx < len(lines):
        c = lines[idx]
        print(f'L{idx+1} ({gi(c):3d}sp): {c.decode("utf-8","replace").strip()[:60]}')

# 目标：
# L5309: if not os.path.exists: 12sp (OK)
# L5317: return jsonify: 12sp (from 28)
# L5333: with open: 12sp (from 24)
# L5342: session_data: 12sp (from 24)
# except: 8sp (OK, already correct)

print("\n=== 修复 ===")
fixes = {
    5317: 12,  # return (from 28)
    5333: 12,  # with (from 24)
    5342: 12,  # session_data (from 24)
}
for idx, target in fixes.items():
    if idx < len(lines):
        old_indent = gi(lines[idx])
        if old_indent != target:
            old = lines[idx].decode('utf-8','replace').strip()[:50]
            lines[idx] = set_indent(lines[idx], target)
            new_indent = gi(lines[idx])
            print(f'L{idx+1}: {old_indent}sp -> {new_indent}sp: {old}')
        else:
            print(f'L{idx+1}: already {target}sp (OK)')

out = b'\r\n'.join(lines)
with open(path, 'wb') as f:
    f.write(out)
print(f'\nWritten {len(out)} bytes')
