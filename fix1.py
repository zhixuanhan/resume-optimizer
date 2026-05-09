# -*- coding: utf-8 -*-
# Fix 1: call_ai timeout 15s → 60s
content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()
old = 'with urllib.request.urlopen(req, timeout=15) as resp:'
new = 'with urllib.request.urlopen(req, timeout=60) as resp:'
count = content.count(old)
print('call_ai timeout 15s → 60s: found', count)
content2 = content.replace(old, new, 1)

# Fix 2: diagnose_resume call - add timeout param
# The call is inside diagnose() which already has flask's default request timeout
# But the internal call_ai is what's taking too long - already fixed above

# Fix 3: Check generate_optimized_resume returns flat keys properly
# Find and print the function to verify it returns 个人总结 etc.
idx = content2.find('def generate_optimized_resume(')
if idx >= 0:
    end = content2.find('\ndef ', idx+10)
    func = content2[idx:end if end > 0 else idx+3000]
    print('=== generate_optimized_resume returns: ===')
    import re
    keys = re.findall(r"optimized\['([^']+)'\]\s*=", func)
    print('Keys set:', keys)
    print('Has return optimized?', 'return optimized' in func)

open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8').write(content2)
print('Fixed and saved')
print('New timeout 60s found:', new in open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read())