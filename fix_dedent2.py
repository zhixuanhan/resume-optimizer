"""彻底修复 career_analysis 缩进 - 无 emoji print"""
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

TRY_START_IDX = 5264 - 1   # 0-based
EXCEPT_IDX = 5882 - 1
changes = []

for idx in range(TRY_START_IDX, EXCEPT_IDX):
    c = lines[idx]
    if not c.strip():
        continue
    indent = get_indent(c)
    if indent >= 8:
        new_line = dedent(c, 4)
        new_indent = get_indent(new_line)
        if new_indent != indent:
            content = c.decode('utf-8', 'replace').strip()[:50]
            changes.append((idx+1, indent, new_indent, content))
            lines[idx] = new_line

# 写文件（先写，绕过 Unicode 打印问题）
out = b'\r\n'.join(lines)
with open(path, 'wb') as f:
    f.write(out)

# 打印结果（无 emoji）
print(f'Fixed {len(changes)} lines:')
for c in changes:
    print(f'L{c[0]} {c[1]}->{c[2]} {c[3]}')
