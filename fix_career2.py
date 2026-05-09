# -*- coding: utf-8 -*-
import re

filepath = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(filepath, 'rb') as f:
    c = f.read()
s = c.decode('utf-8')

start = s.find('def career_analysis():')
rest = s[start+5:]
m = re.search(r'^(@app\.route|def )', rest, re.MULTILINE)
end_pos = start + 5 + m.start()

# Get the function body
body = s[start:end_pos]

if 'except' not in body:
    # Wrap with try-except
    indent = '    '
    # Remove the 'def career_analysis():' line, keep the rest
    lines = body.split('\n')
    def_line = lines[0]
    rest_lines = lines[1:]
    
    # Add try after def line
    new_lines = [def_line, indent + 'try:']
    for line in rest_lines:
        new_lines.append(line)
    
    # Add except at the end
    except_lines = [
        indent + f'except Exception as e:',
        indent + f'    import traceback',
        indent + f'    traceback.print_exc()',
        indent + f'    return jsonify({{"error": f"职业分析失败: {{str(e)[:80]}}", "match_score": 30, "matched_keywords": [], "missing_keywords": [], "transferable_skills": [], "career_advice": "分析出错，请重试"}})',
    ]
    new_lines.extend(except_lines)
    
    new_body = '\n'.join(new_lines)
    s = s[:start] + new_body + s[end_pos:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(s)
    print('OK: career_analysis now has try-except')
else:
    print('Already has except')
