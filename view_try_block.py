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

# 从 try(5264) 到 except(5894) 的所有非空行
print("=== Lines 5264 to 5894 (key lines only) ===")
stack = []
for i in range(5263, min(len(lines_n), 5894)):
    c = lines_n[i]
    txt = c.rstrip(b'\r\n').decode('utf-8','replace').strip()
    if not txt:
        continue
    ind = gi(c)
    kw = txt.split()[0] if txt else ''
    is_block = kw in ('if','for','while','with','def','try','elif','else','except','try:')
    
    if is_block and txt.endswith(':'):
        # 找这行开始的实际缩进
        real_ind = gi(c)
        stack.append((real_ind, txt[:50]))
        print(f'L{i+1:4d}({ind:3d}sp) >>> {txt[:60]}')
    elif txt.startswith('return ') or txt in ('pass','break','continue'):
        if stack:
            parent_ind, parent_txt = stack[-1]
            if ind > parent_ind:
                print(f'L{i+1:4d}({ind:3d}sp)     = {txt[:60]}  [BODY of {parent_txt[:30]}]')
            else:
                print(f'L{i+1:4d}({ind:3d}sp)     ? {txt[:60]}  [unclear nesting]')
                if stack: stack.pop()
        else:
            print(f'L{i+1:4d}({ind:3d}sp)     ? {txt[:60]}  [no parent]')
    elif ind > 0:
        if stack:
            parent_ind, parent_txt = stack[-1]
            if ind > parent_ind:
                print(f'L{i+1:4d}({ind:3d}sp)     = {txt[:60]}  [BODY of {parent_txt[:30]}]')
            elif ind == parent_ind:
                print(f'L{i+1:4d}({ind:3d}sp)     = {txt[:60]}  [SIBLING of {parent_txt[:30]}]')
            else:
                print(f'L{i+1:4d}({ind:3d}sp)     = {txt[:60]}  [closing?]')
                if stack: stack.pop()
        else:
            print(f'L{i+1:4d}({ind:3d}sp)     = {txt[:60]}')
    else:
        print(f'L{i+1:4d}({ind:3d}sp)     ? {txt[:60]}')
