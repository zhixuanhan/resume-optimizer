# -*- coding: utf-8 -*-
"""Fix diagnose_resume indentation corruption"""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\韩知璇\.qclaw\workspace\resume-optimizer\app.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find diagnose_resume function boundaries
func_start = content.find('def diagnose_resume(')
if func_start < 0:
    print("ERROR: diagnose_resume not found")
    sys.exit(1)

# Find next function after it
next_func = content.find('\ndef get_job_keywords(', func_start)
if next_func < 0:
    print("ERROR: get_job_keywords not found")
    sys.exit(1)

# Extract the corrupted function body
old_func = content[func_start:next_func]

# Create clean replacement
new_func = '''def diagnose_resume(sections, target_job=""):
    """用 AI 对简历进行深度诊断"""
    all_text = '\\n'.join(f"【{k}】\\n{sections[k]}" for k in sections if sections.get(k))
    prompt = (
        f"你是一个资深HR猎头。请对以下简历进行诊断评分(0-100分)，并给出详细建议。\\n\\n"
        f"目标岗位：{target_job or '未指定'}\\n\\n"
        f"简历内容：\\n{all_text[:3000]}\\n\\n"
        '请严格按以下JSON格式输出(只输出JSON，不要其他文字)：\\n'
        '{"score":数字,"good":["优点1","优点2"],"bad":["问题1","问题2"],"suggestions":["建议1","建议2"]}'
    )
    result = call_ai(prompt, max_tokens=800, temperature=0.3)
    parsed = extract_json(result)
    if parsed:
        return parsed
    return {"score": 50, "good": ["简历已上传"], "bad": ["诊断生成失败，请重试"], "suggestions": ["请检查网络后重试"]}

'''

# Replace
new_content = content[:func_start] + new_func + content[next_func:]

# Check syntax
try:
    import ast
    ast.parse(new_content)
    print("SYNTAX OK")
except SyntaxError as e:
    print(f"SYNTAX ERROR at line {e.lineno}: {e.msg}")
    # Show context
    lines = new_content.split('\n')
    for i in range(max(0, e.lineno-5), min(len(lines), e.lineno+3)):
        print(f"  {i+1}: {repr(lines[i][:100])}")
    sys.exit(1)

# Write back
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("diagnose_resume fixed and written!")
