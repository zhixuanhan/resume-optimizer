# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer')
content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()

# Find the optimize route
idx = content.find('@app.route("/api/optimize"')
if idx < 0:
    print("Route not found!")
    sys.exit(1)

end = content.find('\n@app.route', idx + 100)
if end < 0:
    end = content.find('\ndef ', idx + 100)
if end < 0:
    end = len(content)

route_code = content[idx:end]
print("Route code length:", len(route_code))
print()

import re

# Find all function calls
all_calls = re.findall(r'(\w+)\(', route_code)
unique_calls = sorted(set(all_calls))
print("Functions called:", unique_calls)

# Check generate_optimized_resume call with arguments
matches = re.findall(r'generate_optimized_resume\([^)]+\)', route_code, re.DOTALL)
for m in matches:
    print("generate_optimized_resume call:", m[:300])

# Check generate_interview_answers
matches2 = re.findall(r'generate_interview_answers\([^)]+\)', route_code, re.DOTALL)
for m in matches2:
    print("generate_interview_answers call:", m)

# Check definitions of those functions
for fn in ['generate_optimized_resume', 'generate_interview_answers', 'generate_personal_summary', 'optimize_experience', 'optimize_skills']:
    idx2 = content.find(f'def {fn}(')
    if idx2 >= 0:
        end2 = content.find('\ndef ', idx2 + 10)
        sig = content[idx2:end2 if end2 > 0 else idx2 + 300]
        sig_lines = [l for l in sig.split('\n') if 'def ' in l or fn in l][:5]
        print('\n' + fn + ' definition:')
        print('\n'.join(sig_lines))