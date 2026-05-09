path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path,'rb') as f: raw = f.read()

pos = raw.find(b'if not os.path.exists')
start = raw.rfind(b'\n', 0, pos)
end = raw.find(b'\n', pos)
chunk = raw[start:end+200]
lines = chunk.split(b'\n')
for l in lines:
    s = l.lstrip(b'\r')
    indent = len(s) - len(s.lstrip())
    content = s.decode('utf-8','replace').strip()
    if content:
        print(f'{indent:3d}sp: {content[:70]}')
