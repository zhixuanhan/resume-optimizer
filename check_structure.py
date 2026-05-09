path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path,'rb') as f: raw = f.read()

def gi(line):
    s = line.lstrip(b'\r')
    n = 0
    for b in s:
        if b == 32: n += 1
        elif b == 9: n += 4
        else: break
    return n

lines_n = raw.split(b'\n')
print(f"Total lines: {len(lines_n)}")
# Show lines 5309-5440
for i in range(5308, 5440):
    c = lines_n[i]
    ind = gi(c)
    txt = c.rstrip(b'\r\n').decode('utf-8','replace')
    stripped = txt.strip()
    if stripped:
        print(f'L{i+1:4d}({ind:3d}sp): {stripped[:70]}')
    else:
        print(f'L{i+1:4d}       : [blank]')
