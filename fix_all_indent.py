import sys
sys.stdout.reconfigure(encoding='utf-8')
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

def body_indent(parent):
    return parent + 4

TARGET = {
    # (if_line): body_indent
    # if at 12sp -> body at 16sp
    5309: 16,   # if not os.path.exists
    5404: 16,   # if not career_info
    5591: 16,   # if match_score >= 70
    # elif at 12sp -> body at 16sp
    5615: 16,   # elif match_score >= 40
}

# For the with at 12sp -> body at 16sp
WITH_TARGET = {
    5336: 16,   # with open (now at 12sp after fix_real.py)
    # The session_data=json.load is already fixed to 16sp
}

print("=== Fixing if/elif bodies ===")
fixed = 0
for ln, target_ind in sorted(TARGET.items()):
    idx = ln - 1
    # Find first non-blank line after ln
    j = idx + 1
    while j < len(lines_n):
        c = lines_n[j]
        cind = gi(c)
        txt = c.rstrip(b'\r\n').decode('utf-8','replace').strip()
        if txt:  # non-blank
            if txt.startswith(('elif ', 'else:', 'except ', 'finally:')):
                # This if/elif's body ends here
                break
            if txt.startswith(('if ', 'for ', 'while ', 'with ', 'def ', 'try:')):
                # This is a compound statement - its body comes next
                j += 1
                continue
            if cind == target_ind:
                # Already correct
                pass
            else:
                # Fix it
                content = c.rstrip(b'\r\n').lstrip(b' \t')
                lines_n[j] = b' ' * target_ind + content + b'\r\n'
                print(f'  L{j+1}: {cind}sp -> {target_ind}sp: {txt[:50]}')
                fixed += 1
            break
        j += 1

print(f"\n=== Fixing with body ===")
for ln, target_ind in sorted(WITH_TARGET.items()):
    idx = ln - 1
    j = idx + 1
    while j < len(lines_n):
        c = lines_n[j]
        cind = gi(c)
        txt = c.rstrip(b'\r\n').decode('utf-8','replace').strip()
        if txt:
            if cind == target_ind:
                pass
            else:
                content = c.rstrip(b'\r\n').lstrip(b' \t')
                lines_n[j] = b' ' * target_ind + content + b'\r\n'
                print(f'  L{j+1}: {cind}sp -> {target_ind}sp: {txt[:50]}')
                fixed += 1
            break
        j += 1

out = b'\n'.join(lines_n)
if not out.endswith(b'\n'):
    out += b'\n'
with open(path,'wb') as f:
    f.write(out)
print(f'\nTotal fixed: {fixed}, Written {len(out)} bytes')

try:
    compile(out.decode('utf-8'), path, 'exec')
    print('COMPILE OK!')
except SyntaxError as e:
    print(f'SyntaxError L{e.lineno}: {e.msg}')
    ls = out.decode('utf-8').split('\n')
    for j in range(max(0,e.lineno-4), min(len(ls),e.lineno+3)):
        m = '>>> ' if j == e.lineno-1 else '    '
        print(f'{m}{j+1}: {repr(ls[j][:100])}')
