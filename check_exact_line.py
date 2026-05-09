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

# 显示 L5309 和 L5317 的确切内容
for ln in [5309, 5310, 5317, 5318, 5319, 5320]:
    idx = ln - 1
    if idx < len(lines_n):
        c = lines_n[idx]
        ind = gi(c)
        txt = c.rstrip(b'\r\n').decode('utf-8','replace').strip()
        print(f'L{ln:4d}({ind:3d}sp): {repr(c[:100])}')
