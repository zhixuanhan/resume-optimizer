# -*- coding: utf-8 -*-
content = open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'r', encoding='utf-8').read()
original = content

# Find the exact pattern in optimize_resume
# Pattern: supplements line followed by optimized = generate_optimized_resume
idx = content.find('def optimize_resume(')
end = content.find('\n@app.route', idx)
segment = content[idx:end]

# The supplements line
old = "    supplements = data.get('supplements', {})\n    optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)\n\n    \n\n    # AI "
new = "    supplements = data.get('supplements', {})\n    try:\n        optimized = generate_optimized_resume(sections, target_job, matched_key, supplements)\n    except Exception as e:\n        optimized = {'_error': str(e), '_original_sections': sections, '_target_job': target_job, '_career_key': matched_key}\n        optimized['求职意向'] = f'**目标岗位：{target_job}**\\n**期望城市：** 待补充\\n**到岗时间：** 一周内'\n\n    # AI "

if old in segment:
    content = content.replace(old, new, 1)
    print('Replace OK')
else:
    print('Pattern not found! Snippet:')
    print(repr(segment[:400]))

import ast
try:
    ast.parse(content)
    print('Syntax: OK')
except SyntaxError as e:
    print('Syntax Error:', e)
    content = original

with open(r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved')