content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()
# Find diagnose route - look for the decorator
import re
matches = list(re.finditer(r'@app\.route.*diagnose', content))
for m in matches:
    start = m.start()
    end = content.find('\n@app.route', start + 10)
    if end < 0:
        end = content.find('\ndef ', start + 10)
    if end < 0:
        end = start + 5000
    route_code = content[start:end]
    print('=== Diagnose Route ===')
    print(route_code[:3000])