"""字节级精确修复 app.py 缩进"""
path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'rb') as f:
    raw = f.read()
lines = raw.split(b'\r\n')

def get_indent(line):
    c = line.rstrip(b'\r\n')
    n = 0
    for b in c:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

def dedent(line, by):
    c = line.rstrip(b'\r\n')
    s = c.lstrip()
    si = len(c) - len(s)
    new_s = b' ' * max(0, si - by) + s
    return new_s + b'\r\n'

# try at 5264, except at 5882
# 已知问题：if body (return jsonify) 是 28sp -> 应为 16sp
# with 是 24sp -> 应为 12sp (sibling of if)
# session_data 是 28sp -> 应为 16sp (with body)
# dict values 是 28sp -> 应为 16sp

# 需要 dedent 12 的行（原始 indent 28 -> 目标 16）
# 从行 5317 开始到 5429 区域
# 行 5333: 原始 24 -> 目标 12 (with)

changes = []
for idx in range(0, len(lines)):
    indent = get_indent(lines[idx])
    if lines[idx].strip():
        # 行 5317 (idx 5316): return jsonify, 28sp -> 16sp
        if idx == 5316 and indent == 28:
            lines[idx] = dedent(lines[idx], 12)
            changes.append((idx+1, 28, 16, lines[idx].decode('utf-8','replace').strip()[:50]))
        # 行 5333 (idx 5332): with open, 24sp -> 12sp
        elif idx == 5332 and indent == 24:
            lines[idx] = dedent(lines[idx], 12)
            changes.append((idx+1, 24, 12, lines[idx].decode('utf-8','replace').strip()[:50]))
        # 行 5341 (idx 5340): session_data, 28sp -> 16sp
        elif idx == 5340 and indent == 28:
            lines[idx] = dedent(lines[idx], 12)
            changes.append((idx+1, 28, 16, lines[idx].decode('utf-8','replace').strip()[:50]))
        # 行 5405 (idx 5404): return jsonify{, 28sp -> 16sp
        elif idx == 5404 and indent == 28:
            lines[idx] = dedent(lines[idx], 12)
            changes.append((idx+1, 28, 16, lines[idx].decode('utf-8','replace').strip()[:50]))
        # 行 5413 (idx 5412): "error": ..., 28sp -> 16sp
        elif idx == 5412 and indent == 28:
            lines[idx] = dedent(lines[idx], 12)
            changes.append((idx+1, 28, 16, lines[idx].decode('utf-8','replace').strip()[:50]))
        # 行 5421 (idx 5420): "available_jobs": ..., 12sp -> OK (stay)
        # 行 5429 (idx 5428): }), 404, 28sp -> 16sp
        elif idx == 5428 and indent == 28:
            lines[idx] = dedent(lines[idx], 12)
            changes.append((idx+1, 28, 16, lines[idx].decode('utf-8','replace').strip()[:50]))
        # 行 5882 (idx 5881): except, 20sp -> 12sp (same level as try)
        elif idx == 5881 and indent == 20:
            lines[idx] = dedent(lines[idx], 8)
            changes.append((idx+1, 20, 12, lines[idx].decode('utf-8','replace').strip()[:50]))
        # 行 5883 (idx 5882): import traceback, 8sp -> OK (already correct for try-level)
        # 但它现在显示 4sp from my last run... let me check
        elif idx == 5882 and indent == 4:
            lines[idx] = b'        import traceback\r\n'
            changes.append((idx+1, indent, 8, 'import traceback (forced to 8sp)'))
        elif idx == 5883 and indent == 4:
            lines[idx] = b'        traceback.print_exc()\r\n'
            changes.append((idx+1, indent, 8, 'traceback.print_exc() (forced to 8sp)'))

for c in changes:
    print(f'L{c[0]:4d}: {c[1]:3d}sp -> {c[2]:3d}sp: {c[3][:60]}')

out = b'\r\n'.join(lines)
with open(path, 'wb') as f:
    f.write(out)
print(f'\nWritten {len(out)} bytes, {len(changes)} changes')
