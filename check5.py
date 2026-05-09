# -*- coding: utf-8 -*-
content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()
import re

# Find generate_optimized_resume and check what field names it returns
idx = content.find('def generate_optimized_resume(')
if idx >= 0:
    end = content.find('\ndef ', idx + 10)
    func = content[idx:end if end > 0 else idx + 3000]
    # Find return statement or key assignments
    print('=== generate_optimized_resume (last 150 lines) ===')
    lines = func.split('\n')
    for line in lines[-150:]:
        print(line)