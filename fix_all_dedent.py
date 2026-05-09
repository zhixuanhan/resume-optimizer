"""彻底修复：把 try 块内所有内容 dedent 4空格"""
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

# try at 5264 (idx 5263), except at 5882 (idx 5881)
TRY_START = 5264
EXCEPT_LINE = 5882
changes = []

for idx in range(TRY_START, EXCEPT_LINE - 1):
    c = lines[idx]
    if not c.strip():  # skip blank
        continue
    indent = get_indent(c)
    if indent >= 8:  # only dedent content lines
        # content: should be at 8 (inside try at 4)
        # currently at 12,16,20,24,28... dedent by 4
        new_line = dedent(c, 4)
        new_indent = get_indent(new_line)
        if new_indent != indent:
            content = c.decode('utf-8','replace').strip()[:55]
            changes.append((idx+1, indent, new_indent, content))
            lines[idx] = new_line

print(f'Fixed {len(changes)} lines:')
for c in changes:
    print(f'  L{c[0]:4d}: {c[1]:3d}sp -> {c[2]:3d}sp: {c[3][:60]}')

out = b'\r\n'.join(lines)
with open(path, 'wb') as f:
    f.write(out)
print(f'Done. Written {len(out)} bytes.')
