path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path,'rb') as f: raw = f.read()
lines_n = raw.split(b'\n')
for i,l in enumerate(lines_n):
    if b'except Exception' in l:
        s = l.lstrip(b'\r')
        indent = len(s) - len(s.lstrip())
        print(f'L{i+1} ({indent}sp): {repr(l[:70])}')
        for j in range(max(0,i-3), min(len(lines_n),i+6)):
            c2 = lines_n[j].lstrip(b'\r')
            i2 = len(c2) - len(c2.lstrip())
            txt = c2.decode('utf-8','replace').strip()
            if txt: print(f'  L{j+1}({i2}sp): {txt[:60]}')
