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
for i in range(5330, 5360):
    c = lines_n[i]
    ind = gi(c)
    txt = c.rstrip(b'\r\n').decode('utf-8','replace').strip()
    print(f'L{i+1:4d}({ind:3d}sp): {txt[:70]}')
