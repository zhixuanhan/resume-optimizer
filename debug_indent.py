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

# 找 L5309 附近的关键行
for i in range(5260, 5340):
    if i < len(lines_n):
        c = lines_n[i]
        indent = get_indent(c)
        txt = c.rstrip(b'\r\n').decode('utf-8','replace').strip()
        if txt:
            print(f'L{i+1:4d}({indent:3d}sp): {txt[:70]}')
