# -*- coding: utf-8 -*-
content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()

# Find the /api/optimize route
idx = content.find('@app.route')
while idx >= 0:
    next_idx = content.find('@app.route', idx + 1)
    segment = content[idx:next_idx if next_idx > 0 else idx + 3000]
    if 'optimize' in segment and "methods=['POST']" in segment:
        print('=== /api/optimize ===')
        print(segment[:2500])
        break
    idx = next_idx

# Find the optimize_resume function definition 
idx2 = content.find('def optimize_resume(')
if idx2 >= 0:
    end2 = content.find('\ndef ', idx2 + 10)
    func2 = content[idx2:end2 if end2 > 0 else idx2 + 2000]
    print('\n=== optimize_resume() ===')
    print(func2[:2000])