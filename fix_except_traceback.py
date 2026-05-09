path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path,'rb') as f: raw = f.read()
lines_n = raw.split(b'\n')

def get_indent(line):
    s = line.lstrip(b'\r')
    n = 0
    for b in s:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

def fix_indent(lines_n, target_line, target_indent):
    """修改指定行的缩进"""
    idx = target_line - 1
    c = lines_n[idx].rstrip(b'\r')
    s = c.lstrip()
    si = len(c) - len(s)
    lines_n[idx] = b' ' * target_indent + s + b'\r\n'

changes = []

# except at L5894: 16sp -> 8sp
for ln in [5894, 5895, 5896, 5897, 5898]:
    idx = ln - 1
    if idx < len(lines_n):
        old_indent = get_indent(lines_n[idx])
        old_content = lines_n[idx].rstrip(b'\r\n').decode('utf-8','replace').strip()
        if ln == 5894:
            new_indent = 8
        elif ln == 5896:
            new_indent = 12  # import traceback (in except)
        elif ln == 5898:
            new_indent = 12  # traceback.print_exc()
        else:
            new_indent = old_indent
        if old_indent != new_indent:
            lines_n[idx] = b' ' * new_indent + lines_n[idx].lstrip(b'\r').lstrip()
            changes.append((ln, old_indent, new_indent, old_content[:50]))
        elif old_content:
            changes.append((ln, old_indent, old_indent, old_content[:50] + ' (unchanged)'))

for c in changes:
    print(f'L{c[0]}: {c[1]}sp -> {c[2]}sp: {c[3][:55]}')

out = b'\n'.join(lines_n)
if not out.endswith(b'\n'):
    out += b'\n'
with open(path,'wb') as f:
    f.write(out)
print(f'Written {len(out)} bytes')
